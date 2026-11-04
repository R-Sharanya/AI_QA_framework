"""Repeatable diagnostic checks, not a semantic correctness classifier."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from src.rag import ROOT, ask, load_chunks

def check(case, result):
    expected = set(case["expected_sources"])
    retrieved = {c["id"] for c in result["contexts"]}
    citations = set(re.findall(r"\[([a-z0-9_-]+:[a-z0-9-]+)\]", result["answer"]))
    recall = len(expected & retrieved) / len(expected) if expected else None
    answer = result["answer"].lower().replace(",", "")
    facts = all(s.lower().replace(",", "") in answer for s in case["required_phrases"])
    checks = {"retrieval": expected <= retrieved if expected else not retrieved,
              "required_phrases": facts,
              "citation_ids_valid": citations <= retrieved,
              "expected_source_cited": bool(citations & expected) if expected else not citations}
    return {"test_id": case["id"], "category": case["category"], "passed": all(checks.values()),
            "checks": checks, "retrieval_recall_at_k": recall, **result}

def run(mode="offline", top_k=2, repeats=1, output=Path("reports")):
    if repeats < 1:
        raise ValueError("repeats must be positive")
    dataset_path = ROOT / "data/evaluation/rag_cases.json"
    raw = dataset_path.read_bytes()
    cases = json.loads(raw)
    chunks = load_chunks()
    results = []
    for repeat in range(repeats):
        for case in cases:
            try:
                result = check(case, ask(case["question"], mode, top_k, chunks=chunks))
            except Exception as error:
                result = {"test_id": case["id"], "passed": False, "error": str(error)}
            results.append({"repeat": repeat+1, **result})
    report = {"created_at": datetime.now(timezone.utc).isoformat(), "mode": mode,
              "dataset_sha256": hashlib.sha256(raw).hexdigest(),
              "corpus_sha256": hashlib.sha256(json.dumps(chunks, sort_keys=True).encode()).hexdigest(),
              "top_k": top_k, "repeats": repeats,
              "notice": "Diagnostic lexical and citation-ID checks only. Not semantic correctness or hallucination rate.",
              "passed": sum(r["passed"] for r in results), "total": len(results), "results": results}
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    (output / "evaluation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["# Evaluation report", "", report["notice"], "", f"Mode: {mode}; passed {report['passed']}/{report['total']}", "",
             "| Case | Repeat | Passed |", "|---|---|---|"]
    lines += [f"| {r['test_id']} | {r['repeat']} | {r['passed']} |" for r in results]
    (output / "evaluation.md").write_text("\n".join(lines), encoding="utf-8")
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["offline", "ollama"], default="offline")
    p.add_argument("--top-k", type=int, default=2)
    p.add_argument("--repeats", type=int, default=1)
    p.add_argument("--output", type=Path, default=Path("reports"))
    args = p.parse_args()
    report = run(args.mode, args.top_k, args.repeats, args.output)
    print(f"{report['passed']}/{report['total']} checks passed ({args.mode}). See {args.output}")
    raise SystemExit(0 if report["passed"] == report["total"] else 1)
if __name__ == "__main__":
    main()
