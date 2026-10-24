"""Harness-only mutation: copy model to temporary directory, run, discard."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import write_report

ROOT = Path(__file__).resolve().parent
GUARD = 'if principal != "operator-1" or target != "vault-1":'
BROKEN = 'if route != "relay" and (principal != "operator-1" or target != "vault-1"):'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    original = (ROOT / "model.py").read_bytes()
    text = original.decode("utf-8")
    if text.count(GUARD) != 1:
        raise RuntimeError("mutation site must be unique")
    mutant = text.replace(GUARD, BROKEN).encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="black-lantern-synthetic-") as temp:
        work = Path(temp)
        for name in ("model.py", "oracle.py", "run.py", "cases.json", "prove_regression.py"):
            shutil.copyfile(ROOT / name, work / name)
        (work / "model.py").write_bytes(mutant)
        output = work / "observations.json"
        # sys.path is inserted explicitly under -I -S; actor has no process API.
        bootstrap = "import runpy,sys;sys.path.insert(0,sys.argv.pop(1));runpy.run_module('run',run_name='__main__')"
        command = [sys.executable, "-I", "-S", "-c", bootstrap, str(work),
                   "--output", str(output)]
        completed = subprocess.run(command, capture_output=True, text=True,
                                   timeout=60, check=False)
        report = json.loads(output.read_text(encoding="utf-8"))
    unchanged = (ROOT / "model.py").read_bytes() == original
    counterexamples = [r for r in report["results"]
                       if r["expected"]["id"].startswith("forbidden-relay-")
                       and not r["accepted"]]
    reads = any(s["response"].get("value") == "SYNTHETIC-DATA-001"
                for r in counterexamples for s in r["observed"]["steps"])
    writes = any(s["snapshot"] == {"value": "SYNTHETIC-WRITE-001", "version": 1}
                 for r in counterexamples for s in r["observed"]["steps"])
    detected = completed.returncode == 1 and unchanged and reads and writes
    report["mutation"] = {
        "before": GUARD, "after": BROKEN, "runner_exit": completed.returncode,
        "runner_stdout": completed.stdout.strip(), "runner_stderr": completed.stderr,
        "original_sha256": hashlib.sha256(original).hexdigest(),
        "mutant_sha256": hashlib.sha256(mutant).hexdigest(),
        "original_unchanged": unchanged, "unauthorized_read_observed": reads,
        "unauthorized_write_observed": writes, "detected": detected,
        "command_template": ["PYTHON", "-I", "-S", "-c", bootstrap,
                             "DISPOSABLE_COPY", "--output", "TEMP_OBSERVATIONS"],
    }
    write_report(args.output, report)
    print(json.dumps(report["mutation"], sort_keys=True))
    return 0 if detected else 1


if __name__ == "__main__":
    raise SystemExit(main())
