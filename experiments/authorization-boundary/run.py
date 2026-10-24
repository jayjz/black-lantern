"""Offline stdlib runner. Exit 1 for any unexpected evidence/result."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import execute
from oracle import compare

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_report(path, report):
    metadata = {key: value for key, value in report.items() if key != "results"}
    header = json.dumps(metadata, indent=2).rstrip()[:-1].rstrip()
    episodes = ",\n".join("    " + json.dumps(row, separators=(",", ":"))
                           for row in report["results"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + ',\n  "results": [\n' + episodes + '\n  ]\n}\n',
                    encoding="utf-8")


def evidence_checks(case, actual):
    """Sensitivity controls against lost/contradictory observer evidence."""
    variants = {}
    for name in ("missing-event", "false-deny", "wrong-principal", "wrong-state",
                 "missing-response", "missing-step"):
        altered = deepcopy(actual)
        first = altered["steps"][0]
        if name == "missing-event":
            first["events"] = []
        elif name == "false-deny":
            first["decision"]["status"] = "denied"
        elif name == "wrong-principal":
            first["events"][0]["principal"] = "intruder-1"
        elif name == "wrong-state":
            first["snapshot"]["version"] += 1
        elif name == "missing-response":
            del first["response"]
        else:
            altered["steps"].pop()
        variants[name] = not compare(case, altered)["security_pass"]
    return variants


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    results = []
    controls = {}
    for repetition in range(1, 4):
        for case in cases:
            def checkpoint(partial):
                prefix = {**case, "calls": case["calls"][:len(partial["steps"])]}
                return compare(prefix, partial)["security_pass"]

            actual = execute(case, None if case.get("evidence") else checkpoint)
            verdict = compare(case, actual)
            expected_incomplete = case.get("evidence") == "incomplete"
            accepted = (verdict["errors"] == [
                "observer evidence incomplete: no security pass"
            ]) if expected_incomplete else verdict["security_pass"]
            results.append({"repetition": repetition, "accepted": accepted,
                            "expected": case, "observed": actual, "verdict": verdict})
            if repetition == 1 and case["id"] == "authorized-direct":
                controls = evidence_checks(case, actual)
    repeatable = all(
        [r["observed"] for r in results if r["repetition"] == n]
        == [r["observed"] for r in results if r["repetition"] == 1]
        for n in (2, 3)
    )
    failures = [f'{r["expected"]["id"]}#{r["repetition"]}'
                for r in results if not r["accepted"]]
    passed = not failures and repeatable and all(controls.values())
    report = {
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "isolated": sys.flags.isolated, "no_site": sys.flags.no_site},
        "source_sha256": {p: digest(ROOT / p) for p in
                          ("model.py", "oracle.py", "run.py", "cases.json",
                           "prove_regression.py")},
        "determinism": "fixed cases, no randomness, fresh state per case",
        "summary": {"passed": passed, "cases": len(cases), "repetitions": 3,
                    "accepted_episodes": len(results) - len(failures),
                    "episodes": len(results), "failed_episodes": failures,
                    "repeatable": repeatable, "evidence_controls": controls},
        "results": results,
    }
    write_report(args.output, report)
    print(json.dumps(report["summary"], sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
