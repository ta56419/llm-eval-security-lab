"""Command line entry point."""

import argparse
import json
from pathlib import Path

from .evaluator import evaluate_suite


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate saved RAG/LLM responses against a JSONL suite.")
    parser.add_argument("cases", type=Path, help="JSONL case file")
    parser.add_argument("--out", type=Path, help="optional JSON report path")
    args = parser.parse_args()
    cases = [json.loads(line) for line in args.cases.read_text(encoding="utf-8").splitlines() if line.strip()]
    report = evaluate_suite(cases)
    output = json.dumps(report, indent=2, ensure_ascii=False)
    print(f"Passed {report['passed']}/{report['total']} cases ({report['pass_rate']:.0%})")
    for result in report["results"]:
        print(f"{'PASS' if result['passed'] else 'FAIL'} {result['id']}")
        for reason in result["reasons"]:
            print(f"  - {reason}")
    if args.out:
        args.out.write_text(output + "\n", encoding="utf-8")
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
