"""Offline controlled bypass review; every model runs in a disposable copy."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrypoint import build, remove_repair, DELEGATION, UNCHECKED

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "authorization-boundary"
BASE_COMMIT = "5121161b826b22485c7e79461199677d195869e6"
INPUTS = ("model.py", "oracle.py", "run.py", "cases.json", "prove_regression.py")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_variant(label, source, cases, output_dir):
    output = output_dir / (label + ".json")
    with tempfile.TemporaryDirectory(prefix="black-lantern-review-") as temporary:
        work = Path(temporary)
        for name in INPUTS:
            shutil.copyfile(BASE / name, work / name)
        (work / "model.py").write_bytes(source.encode("utf-8"))
        (work / "cases.json").write_text(json.dumps(cases, indent=2) + "\n",
                                         encoding="utf-8", newline="\n")
        completed = subprocess.run(
            [sys.executable, "-I", "-S", str(work / "run.py"),
             "--output", str(output)], capture_output=True, text=True,
            timeout=60, check=False,
        )
        if completed.returncode not in (0, 1) or not output.is_file():
            raise RuntimeError("runner did not produce test evidence")
        # Preserve exact generated model bytes for independent reproduction.
        model_bytes = (work / "model.py").read_bytes()
    report = json.loads(output.read_text(encoding="utf-8"))
    if report["source_sha256"]["model.py"] != sha(model_bytes):
        raise RuntimeError("generated source identity mismatch")
    return {"label": label, "output": output.name,
            "model_sha256": sha(model_bytes), "runner_exit": completed.returncode,
            "command_template": ["PYTHON", "-I", "-S", "DISPOSABLE_COPY/run.py",
                                 "--output", "OUTPUT_DIR/" + output.name],
            "stdout": completed.stdout.strip(), "stderr": completed.stderr,
            "summary": report["summary"]}, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    original_bytes = {name: (BASE / name).read_bytes() for name in INPUTS}
    original_hashes = {name: sha(data) for name, data in original_bytes.items()}
    recorded = json.loads((BASE / "results/correct-after.json").read_text(encoding="utf-8"))
    if original_hashes != recorded["source_sha256"]:
        raise RuntimeError("Experiment 01 differs from recorded tested inputs")
    original = original_bytes["model.py"].decode("utf-8")
    old_cases = json.loads(original_bytes["cases.json"])
    new_cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    corrected = build(original)
    defective = remove_repair(corrected)
    restored = build(original)
    runs, reports = [], {}
    for label, source, cases in (
        ("original-baseline", original, old_cases),
        ("defective-old-suite", defective, old_cases),
        ("defective-new-regression", defective, old_cases + new_cases),
        ("corrected", corrected, old_cases + new_cases),
        ("repair-removed", remove_repair(corrected), old_cases + new_cases),
        ("restored", restored, old_cases + new_cases),
    ):
        result, report = run_variant(label, source, cases, output_dir)
        runs.append(result)
        reports[label] = report

    # Independent, hand-stated expectation for the original rejected route.
    original_probe = deepcopy(new_cases[0])
    original_probe["calls"][0]["expected"] = {
        "response": {"status": "invalid"},
        "state": {"value": "SYNTHETIC-DATA-001", "version": 0},
        "dispatch": False, "target": None,
    }
    model = load("review_baseline", BASE / "model.py")
    oracle = load("review_oracle", BASE / "oracle.py")
    original_observed = model.execute(original_probe)
    original_verdict = oracle.compare(original_probe, original_observed)

    counterexample = next(
        row for row in reports["defective-new-regression"]["results"]
        if row["expected"]["id"] == "forbidden-inspect-read" and row["repetition"] == 1
    )
    step = counterexample["observed"]["steps"][0]
    exact_disclosure = (
        step["response"] == {"status": "ok", "value": "SYNTHETIC-DATA-001"}
        and step["events"] == []
        and step["snapshot"] == {"value": "SYNTHETIC-DATA-001", "version": 0}
        and step["decision"]["principal"] == "intruder-1"
    )
    authorized_row = next(row for row in reports["restored"]["results"]
                          if row["expected"]["id"] == "authorized-inspect-read")
    missing_event = deepcopy(authorized_row["observed"])
    missing_event["steps"][0]["events"] = []
    missing_verdict = oracle.compare(authorized_row["expected"], missing_event)
    fault_rows = [row for row in reports["restored"]["results"]
                  if row["expected"]["id"] == "inspect-observer-loss"]
    unchanged = all((BASE / name).read_bytes() == data
                    for name, data in original_bytes.items())
    checks = {
        "original_route_rejected": original_verdict["security_pass"],
        "original_suite_passes_defect": runs[1]["runner_exit"] == 0,
        "old_suite_observations_identical": reports["original-baseline"]["results"]
            == reports["defective-old-suite"]["results"],
        "unlogged_disclosure_observed": exact_disclosure,
        "new_test_detects_defect": runs[2]["runner_exit"] == 1
            and reports["defective-new-regression"]["summary"]["failed_episodes"]
            == [f"{case_id}#{n}" for n in (1, 2, 3)
                for case_id in ("forbidden-inspect-read", "authorized-inspect-read")],
        "corrected_passes": runs[3]["runner_exit"] == 0,
        "repair_removal_detected": runs[4]["runner_exit"] == 1,
        "repair_removal_reproduces_counterexample":
            reports["defective-new-regression"]["results"]
            == reports["repair-removed"]["results"],
        "restored_passes": runs[5]["runner_exit"] == 0,
        "restoration_identical": corrected == restored
            and reports["corrected"]["results"] == reports["restored"]["results"],
        "missing_service_event_rejected": not missing_verdict["security_pass"],
        "observation_failure_withholds_security_pass": len(fault_rows) == 3 and all(
            row["accepted"] and not row["verdict"]["security_pass"]
            and row["verdict"]["errors"] == ["observer evidence incomplete: no security pass"]
            for row in fault_rows
        ),
        "original_inputs_unchanged": unchanged,
        "original_baseline_passes": runs[0]["runner_exit"] == 0,
    }
    summary = {
        "passed": all(checks.values()), "checks": checks,
        "original_commit": BASE_COMMIT, "original_sha256": original_hashes,
        "review_sha256": {name: sha((ROOT / name).read_bytes())
                          for name in ("entrypoint.py", "review.py", "cases.json")},
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "isolated": sys.flags.isolated, "no_site": sys.flags.no_site},
        "defect": {"before": DELEGATION, "after": UNCHECKED},
        "runs": runs,
        "original_route_probe": {"expected": original_probe,
                                 "observed": original_observed, "verdict": original_verdict},
        "counterexample": counterexample,
        "missing_event_control": {"expected": authorized_row["expected"],
                                  "observed": missing_event, "verdict": missing_verdict},
    }
    (output_dir / "review.json").write_text(json.dumps(summary, indent=2) + "\n",
                                           encoding="utf-8", newline="\n")
    print(json.dumps({"passed": summary["passed"], "checks": checks}, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
