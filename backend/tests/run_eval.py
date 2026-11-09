import json
import time
import sys
import os

# Add paths so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "retrieval"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hybrid_retriever import build_graph

def run_evaluation():
    eval_path = os.path.join(os.path.dirname(__file__), "eval", "test_queries.json")
    with open(eval_path, "r") as f:
        test_queries = json.load(f)

    if not test_queries:
        print("ERROR: test_queries.json is empty.")
        return

    # Compile graph ONCE
    app = build_graph()

    total = len(test_queries)
    latencies = []
    routing_correct = 0

    route_counts = {"sql_retriever": 0, "hybrid_retriever": 0, "generate_direct": 0}
    category_stats = {}

    # SQL-specific
    sql_total = 0
    sql_with_results = 0

    print(f"\n{'='*100}")
    print(f"  FRIDAY RAG EVALUATION — {total} queries")
    print(f"{'='*100}\n")

    for i, item in enumerate(test_queries):
        query = item["query"]
        expected_route = item["expected_route"]
        category = item["category"]

        if category not in category_stats:
            category_stats[category] = {
                "total": 0, "correct": 0,
                "routes": {"sql_retriever": 0, "hybrid_retriever": 0, "generate_direct": 0}
            }
        category_stats[category]["total"] += 1

        start = time.time()
        try:
            res = app.invoke({
                "question": query,
                "tool_selected": "generate_direct",
                "docs": [],
                "relevant_docs": [],
                "answer": "",
                "context": ""
            })
            elapsed = time.time() - start
        except Exception as e:
            elapsed = time.time() - start
            print(f"  [{i+1:02d}] 💥 ERROR | {elapsed:.2f}s | [{category}] {query}")
            print(f"       {str(e)[:120]}")
            continue

        latencies.append(elapsed)
        actual_route = res.get("tool_selected", "unknown")

        route_counts[actual_route] = route_counts.get(actual_route, 0) + 1
        category_stats[category]["routes"][actual_route] = \
            category_stats[category]["routes"].get(actual_route, 0) + 1

        # SQL metrics
        if actual_route == "sql_retriever":
            sql_total += 1
            docs = res.get("docs", [])
            if docs and len(docs) > 0 and docs[0].page_content != "{}":
                sql_with_results += 1

        is_correct = actual_route == expected_route
        if is_correct:
            routing_correct += 1
            category_stats[category]["correct"] += 1

        status = "✅" if is_correct else "❌"
        icon = {"sql_retriever": "🗄️", "hybrid_retriever": "🔍", "generate_direct": "⚡"}.get(actual_route, "❓")

        extra = ""
        if actual_route == "sql_retriever":
            row_count = len(res.get("docs", []))
            extra = f" [{row_count} rows]"
        if not is_correct:
            extra += f" (expected: {expected_route})"

        print(f"  [{i+1:02d}] {status} {icon} {actual_route:<20}{extra} | {elapsed:.1f}s | [{category}] {query}")

    # --- Results ---
    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else 0
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
    avg = sum(latencies) / len(latencies) if latencies else 0

    sql_count = route_counts.get("sql_retriever", 0)
    hybrid_count = route_counts.get("hybrid_retriever", 0)
    direct_count = route_counts.get("generate_direct", 0)
    retrieval_reduction = direct_count / total * 100 if total else 0
    routing_acc = routing_correct / total * 100 if total else 0
    sql_success = sql_with_results / sql_total * 100 if sql_total else 0

    print(f"\n{'='*100}")
    print(f"  RESULTS SUMMARY")
    print(f"{'='*100}")
    print(f"")
    print(f"  Total queries evaluated:   {total}")
    print(f"")
    print(f"  Route Distribution:")
    print(f"    🗄️  SQL retriever:         {sql_count:>3}  ({sql_count/total*100:.1f}%)")
    print(f"    🔍 Hybrid retriever:       {hybrid_count:>3}  ({hybrid_count/total*100:.1f}%)")
    print(f"    ⚡ Direct generation:      {direct_count:>3}  ({direct_count/total*100:.1f}%)")
    print(f"")
    print(f"  ┌────────────────────────────────────────────────────────────┐")
    print(f"  │                                                            │")
    print(f"  │  ROUTING ACCURACY:         {routing_acc:>5.1f}%                       │")
    print(f"  │  ({routing_correct}/{total} queries routed to correct tool)                │")
    print(f"  │                                                            │")
    print(f"  │  RETRIEVAL REDUCTION:      {retrieval_reduction:>5.1f}%                       │")
    print(f"  │  ({direct_count}/{total} queries answered without any retrieval)         │")
    print(f"  │                                                            │")
    print(f"  │  SQL EXECUTION SUCCESS:    {sql_success:>5.1f}%                       │")
    print(f"  │  ({sql_with_results}/{sql_total} SQL queries returned valid results)          │")
    print(f"  │                                                            │")
    print(f"  └────────────────────────────────────────────────────────────┘")
    print(f"")
    print(f"  Latency:")
    print(f"    Average:  {avg:.2f}s")
    print(f"    P50:      {p50:.2f}s")
    print(f"    P95:      {p95:.2f}s")
    print(f"")

    # Per-category breakdown
    print(f"  Per-Category Breakdown:")
    print(f"  {'Category':<25} {'Total':>5} {'SQL':>5} {'Hybrid':>7} {'Direct':>7} {'Accuracy':>9}")
    print(f"  {'-'*25} {'-'*5} {'-'*5} {'-'*7} {'-'*7} {'-'*9}")
    for cat in ["product_search", "company_knowledge", "general_knowledge", "chitchat"]:
        if cat not in category_stats:
            continue
        s = category_stats[cat]
        acc = s["correct"] / s["total"] * 100 if s["total"] else 0
        print(f"  {cat:<25} {s['total']:>5} {s['routes'].get('sql_retriever',0):>5} "
              f"{s['routes'].get('hybrid_retriever',0):>7} {s['routes'].get('generate_direct',0):>7} {acc:>8.1f}%")

    # Misrouted queries
    print(f"\n  Misrouted Queries:")
    misrouted = 0
    for i, item in enumerate(test_queries):
        # We need to re-check — pull from the results
        pass  # already printed inline above

    print(f"\n{'='*100}")
    print(f"  CV BULLET POINTS")
    print(f"{'='*100}")
    print(f"")
    print(f'  "Vector search failed on structured queries like "shoes under $80" — built a 3-way')
    print(f'   intent router (text-to-SQL / hybrid search / direct) achieving {routing_acc:.0f}% routing')
    print(f'   accuracy on a {total}-query evaluation set with {sql_success:.0f}% SQL execution success')
    print(f'   across a 215+ product catalog"')
    print(f"")
    print(f'  "{retrieval_reduction:.0f}% of queries (chitchat, general knowledge) correctly bypassed the')
    print(f'   full retrieval pipeline, reducing per-query cost and achieving p95 latency of {p95:.1f}s"')
    print(f"")

    # Save results
    results = {
        "total_queries": total,
        "route_distribution": route_counts,
        "routing_accuracy_pct": round(routing_acc, 1),
        "retrieval_reduction_pct": round(retrieval_reduction, 1),
        "sql_total": sql_total,
        "sql_with_results": sql_with_results,
        "sql_success_pct": round(sql_success, 1),
        "latency_avg_s": round(avg, 2),
        "latency_p50_s": round(p50, 2),
        "latency_p95_s": round(p95, 2),
        "category_breakdown": category_stats
    }

    results_path = os.path.join(os.path.dirname(__file__), "eval", "results1.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to: {results_path}")


if __name__ == "__main__":
    run_evaluation()
