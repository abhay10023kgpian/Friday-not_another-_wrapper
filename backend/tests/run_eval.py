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
        print("ERROR: test_queries.json is empty.")
        return

    # Compile graph ONCE
    print("Compiling LangGraph application...")
    app = build_graph()

    # --- Metric Counters ---
    total = len(test_queries)
    routing_correct = 0
    total_latency = 0.0
    latencies = []

    # Valid tools
    tools = ["sql_retriever", "hybrid_retriever", "generate_direct"]

    # Tool counts & Confusion Matrix: matrix[expected][actual]
    predicted_counts = {t: 0 for t in tools}
    expected_counts = {t: 0 for t in tools}
    confusion_matrix = {e: {a: 0 for a in tools} for e in tools}

    # Per-category tracking
    category_stats = {}

    print(f"\n{'='*105}")
    print(f"  FRIDAY 3-WAY ROUTER BENCHMARK — {total} Queries")
    print(f"  Tools: [sql_retriever] vs [hybrid_retriever] vs [generate_direct]")
    print(f"{'='*105}\n")

    for i, item in enumerate(test_queries):
        query = item["query"]
        expected_tool = item["expected_tool"]
        category = item.get("category", "general")

        expected_counts[expected_tool] = expected_counts.get(expected_tool, 0) + 1

        if category not in category_stats:
            category_stats[category] = {"total": 0, "correct": 0}
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
            print(f"  [{i+1:03d}] ❌ ERROR on query: '{query}'")
            print(f"        Details: {e}")
            continue

        latencies.append(elapsed)
        total_latency += elapsed

        # Get actual tool selected by router
        actual_tool = res.get("tool_selected", "generate_direct")
        if actual_tool not in tools:
            actual_tool = "generate_direct"

        predicted_counts[actual_tool] += 1
        confusion_matrix[expected_tool][actual_tool] += 1

        # Check match
        is_match = (actual_tool == expected_tool)
        if is_match:
            routing_correct += 1
            category_stats[category]["correct"] += 1

        # Format visual logs
        status = "✅" if is_match else "❌"
        docs_len = len(res.get("docs", []))
        docs_info = f"({docs_len} docs)" if docs_len > 0 else ""

        if is_match:
            route_display = f"[{actual_tool:<16}]"
        else:
            route_display = f"[EXP: {expected_tool} | GOT: {actual_tool}]"

        print(f"  [{i+1:03d}] {status} {route_display:<38} {docs_info:<9} | {elapsed:.2f}s | [{category}] {query[:45]}")

    # --- Calculations ---
    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else 0
    p95_idx = int(len(latencies) * 0.95)
    p95 = latencies[min(p95_idx, len(latencies) - 1)] if latencies else 0
    avg_latency = total_latency / total if total else 0

    overall_accuracy = (routing_correct / total * 100) if total else 0

    print(f"\n{'='*105}")
    print(f"  BENCHMARK SUMMARY RESULTS")
    print(f"{'='*105}")
    print(f"")
    print(f"  Total queries:               {total}")
    print(f"  Overall Routing Accuracy:    {overall_accuracy:.1f}% ({routing_correct}/{total} correct)")
    print(f"  Average Latency:             {avg_latency:.2f}s (P50: {p50:.2f}s | P95: {p95:.2f}s)")
    print(f"")

    # Confusion Matrix Table
    print(f"  Confusion Matrix (Rows = Expected, Columns = Predicted by Router):")
    print(f"  {'-'*75}")
    print(f"  {'Expected Tool':<22} | {'SQL Pred':>10} | {'Hybrid Pred':>12} | {'Direct Pred':>12} | {'Accuracy':>10}")
    print(f"  {'-'*75}")
    for exp_t in tools:
        row = confusion_matrix[exp_t]
        exp_total = expected_counts[exp_t]
        correct_in_row = row[exp_t]
        row_acc = (correct_in_row / exp_total * 100) if exp_total else 0
        print(f"  {exp_t:<22} | {row['sql_retriever']:>10} | {row['hybrid_retriever']:>12} | {row['generate_direct']:>12} | {row_acc:>9.1f}%")
    print(f"  {'-'*75}")

    # Category breakdown
    print(f"\n  Per-Category Accuracy:")
    for cat, stat in category_stats.items():
        cat_acc = (stat["correct"] / stat["total"] * 100) if stat["total"] else 0
        print(f"    • {cat:<20}: {stat['correct']:>2}/{stat['total']:>2} ({cat_acc:.1f}%)")

    # CV Bullet Points
    direct_skipped = predicted_counts["generate_direct"]
    reduction_pct = (direct_skipped / total * 100) if total else 0
    sql_accuracy = (confusion_matrix["sql_retriever"]["sql_retriever"] / expected_counts["sql_retriever"] * 100) if expected_counts["sql_retriever"] else 0

    print(f"\n{'='*105}")
    print(f"  CV BULLET POINTS (Measured with 3-Way Routing):")
    print(f"{'='*105}")
    print(f'  • "Engineered an intelligent 3-way router (PostgreSQL Text-to-SQL, Elasticsearch Hybrid RAG, Direct LLM)')
    print(f'     achieving {overall_accuracy:.0f}% routing accuracy and {sql_accuracy:.0f}% SQL intent detection across a {total}-query benchmark,')
    print(f'     reducing expensive vector retrieval overhead by {reduction_pct:.0f}% at p95 latency of {p95:.1f}s."')
    print(f"{'='*105}\n")

    # Save to JSON
    results = {
        "total_queries": total,
        "overall_accuracy_pct": round(overall_accuracy, 1),
        "latency": {"avg_s": round(avg_latency, 2), "p50_s": round(p50, 2), "p95_s": round(p95, 2)},
        "confusion_matrix": confusion_matrix,
        "category_stats": category_stats,
        "tool_distribution": predicted_counts
    }

    results_path = os.path.join(os.path.dirname(__file__), "eval", "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"  Full report saved to: {results_path}\n")


if __name__ == "__main__":
    run_evaluation()
