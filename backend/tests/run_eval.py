import json
import time
import sys
import os

# Add the retrieval directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "retrieval"))

from src.retrieval.hybrid_retriever import build_graph

def run_evaluation():
    # Load test queries
    eval_path = os.path.join(os.path.dirname(__file__), "eval", "test_queries.json")
    with open(eval_path, "r") as f:
        test_queries = json.load(f)

    if not test_queries:
        print("ERROR: test_queries.json is empty. Paste the generated queries first.")
        return

    # Compile graph ONCE
    app = build_graph()

    # --- Metric Counters ---
    total = len(test_queries)
    retrieval_triggered = 0
    retrieval_skipped = 0
    routing_correct = 0
    total_latency = 0.0
    latencies = []

    # Per-category tracking
    category_stats = {}

    print(f"\n{'='*80}")
    print(f"  FRIDAY RAG EVALUATION — {total} queries")
    print(f"{'='*80}\n")

    for i, item in enumerate(test_queries):
        query = item["query"]
        expected_retrieval = item["expected_retrieval"]
        category = item["category"]

        # Init category stats
        if category not in category_stats:
            category_stats[category] = {"total": 0, "correct": 0, "retrieved": 0, "skipped": 0}
        category_stats[category]["total"] += 1

        # Measure latency
        start = time.time()

        try:
            res = app.invoke({
                "question": query,
                "need_retrieval": False,
                "docs": [],
                "relevant_docs": [],
                "answer": "",
                "context": ""
            })
            elapsed = time.time() - start
        except Exception as e:
            print(f"  [{i+1:02d}] ERROR on query: {query}")
            print(f"       {e}")
            continue

        latencies.append(elapsed)
        total_latency += elapsed

        actual_retrieval = res.get("need_retrieval", False)

        # Count
        if actual_retrieval:
            retrieval_triggered += 1
            category_stats[category]["retrieved"] += 1
        else:
            retrieval_skipped += 1
            category_stats[category]["skipped"] += 1

        # Check if routing matched expectation
        is_correct = actual_retrieval == expected_retrieval
        if is_correct:
            routing_correct += 1
            category_stats[category]["correct"] += 1

        # Display
        status = "✅" if is_correct else "❌"
        action = "🔍 RETRIEVED" if actual_retrieval else "⚡ SKIPPED  "
        print(f"  [{i+1:02d}] {status} {action} | {elapsed:.2f}s | [{category}] {query}")

    # --- Summary ---
    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else 0
    p95_idx = int(len(latencies) * 0.95)
    p95 = latencies[min(p95_idx, len(latencies) - 1)] if latencies else 0
    avg_latency = total_latency / total if total else 0

    print(f"\n{'='*80}")
    print(f"  RESULTS")
    print(f"{'='*80}")
    print(f"")
    print(f"  Total queries:             {total}")
    print(f"  Retrieval triggered:       {retrieval_triggered}")
    print(f"  Retrieval skipped:         {retrieval_skipped}")
    print(f"")
    print(f"  ┌─────────────────────────────────────────────────┐")
    print(f"  │  RETRIEVAL REDUCTION:  {retrieval_skipped/total*100:.1f}%                     │")
    print(f"  │  ({retrieval_skipped}/{total} queries skipped retrieval)              │")
    print(f"  │                                                 │")
    print(f"  │  ROUTING ACCURACY:     {routing_correct/total*100:.1f}%                     │")
    print(f"  │  ({routing_correct}/{total} queries routed correctly)              │")
    print(f"  └─────────────────────────────────────────────────┘")
    print(f"")
    print(f"  Latency:")
    print(f"    Average:  {avg_latency:.2f}s")
    print(f"    P50:      {p50:.2f}s")
    print(f"    P95:      {p95:.2f}s")
    print(f"")

    # Per-category breakdown
    print(f"  Per-Category Breakdown:")
    print(f"  {'Category':<25} {'Total':>5} {'Retrieved':>10} {'Skipped':>8} {'Accuracy':>9}")
    print(f"  {'-'*25} {'-'*5} {'-'*10} {'-'*8} {'-'*9}")
    for cat, stats in category_stats.items():
        acc = stats["correct"] / stats["total"] * 100 if stats["total"] else 0
        print(f"  {cat:<25} {stats['total']:>5} {stats['retrieved']:>10} {stats['skipped']:>8} {acc:>8.1f}%")

    print(f"\n{'='*80}")
    print(f"  CV BULLET POINT (copy-paste ready):")
    print(f"{'='*80}")
    print(f"")
    print(f'  "Reduced unnecessary retrieval calls by {retrieval_skipped/total*100:.0f}% via')
    print(f'   LLM-powered adaptive routing (evaluated on {total}-query test set),')
    print(f'   achieving {routing_correct/total*100:.0f}% routing accuracy at p95 latency of {p95:.1f}s"')
    print(f"")

    # Save results to JSON
    results = {
        "total_queries": total,
        "retrieval_triggered": retrieval_triggered,
        "retrieval_skipped": retrieval_skipped,
        "retrieval_reduction_pct": round(retrieval_skipped / total * 100, 1),
        "routing_accuracy_pct": round(routing_correct / total * 100, 1),
        "latency_avg_s": round(avg_latency, 2),
        "latency_p50_s": round(p50, 2),
        "latency_p95_s": round(p95, 2),
        "category_breakdown": category_stats
    }

    results_path = os.path.join(os.path.dirname(__file__), "eval", "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to: {results_path}")


if __name__ == "__main__":
    run_evaluation()

