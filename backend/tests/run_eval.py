import json
import time
import sys
import os

# Ensure backend root and src/retrieval are in sys.path
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
retrieval_dir = os.path.join(backend_root, "src", "retrieval")

if backend_root not in sys.path:
    sys.path.insert(0, backend_root)
if retrieval_dir not in sys.path:
    sys.path.insert(0, retrieval_dir)

from src.retrieval.hybrid_retriever import build_graph

def run_evaluation():
    # Load test queries
    eval_path = os.path.join(os.path.dirname(__file__), "eval", "test_queries.json")
    with open(eval_path, "r", encoding="utf-8") as f:
        test_queries = json.load(f)

    if not test_queries:
        print("ERROR: test_queries.json is empty. Paste the test queries first.")
        return

    # Compile graph ONCE
    print("Compiling LangGraph application...")
    app = build_graph()

    # --- Metric Counters ---
    total = len(test_queries)
    routing_correct = 0
    total_latency = 0.0
    latencies = []

    # 3-way Tool selection counters
    tool_counts = {
        "sql_retriever": 0,
        "hybrid_retriever": 0,
        "generate_direct": 0
    }

    # Per-category tracking
    category_stats = {}

    print(f"\n{'='*95}")
    print(f"  FRIDAY AGENT EVALUATION — {total} Queries (3-way Tool Routing)")
    print(f"{'='*95}\n")

    for i, item in enumerate(test_queries):
        query = item["query"]
        expected_retrieval = item["expected_retrieval"]
        category = item["category"]

        # Init category stats
        if category not in category_stats:
            category_stats[category] = {
                "total": 0,
                "correct": 0,
                "sql_retriever": 0,
                "hybrid_retriever": 0,
                "generate_direct": 0
            }
        category_stats[category]["total"] += 1

        # Measure latency
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
            print(f"  [{i+1:02d}] ❌ ERROR on query: '{query}'")
            print(f"       Details: {e}")
            continue

        latencies.append(elapsed)
        total_latency += elapsed

        # Get actual tool selected from hybrid_retriever
        actual_tool = res.get("tool_selected", "generate_direct")
        tool_counts[actual_tool] = tool_counts.get(actual_tool, 0) + 1
        category_stats[category][actual_tool] = category_stats[category].get(actual_tool, 0) + 1

        # Actual retrieval was performed if tool was sql_retriever or hybrid_retriever
        actual_retrieved = actual_tool in ("sql_retriever", "hybrid_retriever")

        # Check if routing matched expected retrieval need
        is_correct = (actual_retrieved == expected_retrieval)
        if is_correct:
            routing_correct += 1
            category_stats[category]["correct"] += 1

        # Icon and label for console output
        tool_icons = {
            "sql_retriever": "🗄️ SQL  ",
            "hybrid_retriever": "🔍 HYBRID",
            "generate_direct": "⚡ DIRECT"
        }
        icon_label = tool_icons.get(actual_tool, "❓ UNKNOWN")
        status = "✅" if is_correct else "❌"

        docs_count = len(res.get("docs", []))
        docs_info = f"({docs_count} docs)" if docs_count > 0 else ""

        print(f"  [{i+1:02d}] {status} [{icon_label}] {docs_info:<9} | {elapsed:.2f}s | [{category}] {query}")

    # --- Summary Calculations ---
    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else 0
    p95_idx = int(len(latencies) * 0.95)
    p95 = latencies[min(p95_idx, len(latencies) - 1)] if latencies else 0
    avg_latency = total_latency / total if total else 0

    retrieval_skipped = tool_counts.get("generate_direct", 0)
    retrieval_reduction_pct = (retrieval_skipped / total * 100) if total else 0
    routing_acc_pct = (routing_correct / total * 100) if total else 0

    print(f"\n{'='*95}")
    print(f"  EVALUATION RESULTS SUMMARY")
    print(f"{'='*95}")
    print(f"")
    print(f"  Total queries evaluated:       {total}")
    print(f"")
    print(f"  Tool Routing Distribution:")
    print(f"    🗄️  SQL Retriever (Postgres):     {tool_counts.get('sql_retriever', 0):>2} queries ({tool_counts.get('sql_retriever', 0)/total*100:.1f}%)")
    print(f"    🔍 Hybrid Retriever (Elastic):   {tool_counts.get('hybrid_retriever', 0):>2} queries ({tool_counts.get('hybrid_retriever', 0)/total*100:.1f}%)")
    print(f"    ⚡ Direct (No retrieval):        {tool_counts.get('generate_direct', 0):>2} queries ({retrieval_reduction_pct:.1f}%)")
    print(f"")
    print(f"  ┌────────────────────────────────────────────────────────┐")
    print(f"  │  ROUTING ACCURACY:       {routing_acc_pct:>5.1f}%                       │")
    print(f"  │  ({routing_correct}/{total} queries selected the appropriate strategy)    │")
    print(f"  │                                                        │")
    print(f"  │  RETRIEVAL REDUCTION:    {retrieval_reduction_pct:>5.1f}%                       │")
    print(f"  │  ({retrieval_skipped}/{total} queries skipped expensive vector retrieval)     │")
    print(f"  └────────────────────────────────────────────────────────┘")
    print(f"")
    print(f"  Latency Performance:")
    print(f"    Average:  {avg_latency:.2f}s")
    print(f"    P50:      {p50:.2f}s")
    print(f"    P95:      {p95:.2f}s")
    print(f"")

    # Per-category breakdown table
    print(f"  Per-Category Breakdown:")
    print(f"  {'Category':<22} {'Total':>5} {'SQL':>6} {'Hybrid':>8} {'Direct':>8} {'Accuracy':>10}")
    print(f"  {'-'*22} {'-'*5} {'-'*6} {'-'*8} {'-'*8} {'-'*10}")
    for cat, stats in category_stats.items():
        acc = stats["correct"] / stats["total"] * 100 if stats["total"] else 0
        print(f"  {cat:<22} {stats['total']:>5} {stats.get('sql_retriever', 0):>6} "
              f"{stats.get('hybrid_retriever', 0):>8} {stats.get('generate_direct', 0):>8} {acc:>9.1f}%")

    print(f"\n{'='*95}")
    print(f"  CV BULLET POINTS (Copy & Paste Ready):")
    print(f"{'='*95}")
    print(f"")
    print(f'  • "Architected a 3-way adaptive routing agent (text-to-SQL / hybrid vector search / direct LLM)')
    print(f'     achieving {routing_acc_pct:.0f}% routing accuracy and skipping unnecessary retrieval for {retrieval_reduction_pct:.0f}% of queries')
    print(f'     on a {total}-query evaluation dataset at p95 latency of {p95:.1f}s."')
    print(f"")

    # Save results to JSON
    results = {
        "total_queries": total,
        "tool_distribution": tool_counts,
        "routing_accuracy_pct": round(routing_acc_pct, 1),
        "retrieval_reduction_pct": round(retrieval_reduction_pct, 1),
        "latency_avg_s": round(avg_latency, 2),
        "latency_p50_s": round(p50, 2),
        "latency_p95_s": round(p95, 2),
        "category_breakdown": category_stats
    }

    results_path = os.path.join(os.path.dirname(__file__), "eval", "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to: {results_path}\n")


if __name__ == "__main__":
    run_evaluation()
