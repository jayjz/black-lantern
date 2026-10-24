"""Compare exact service observations to static expectations, never call policy."""
from copy import deepcopy


def compare(case, actual):
    errors = []
    state = {"value": "SYNTHETIC-DATA-001", "version": 0}
    sequence = 0
    if actual.get("id") != case["id"] or actual.get("before") != state:
        errors.append("fixture/episode mismatch")
    steps = actual.get("steps", [])
    if len(steps) != len(case["calls"]):
        errors.append("missing/extra request evidence")
    for index, (call, observed) in enumerate(zip(case["calls"], steps), 1):
        expected = call["expected"]
        events = []
        if expected["dispatch"]:
            sequence += 1
            events = [{
                "sequence": sequence, "principal": call["principal"],
                "id": call["request"]["id"],
                "operation": call["request"]["operation"],
                "target": "vault-1", "route": call["request"]["route"],
                "before": deepcopy(state), "after": expected["state"],
                "response": expected["response"],
            }]
        decision = {
            "sequence": index, "principal": call["principal"],
            "target": expected["target"],
            "status": expected["response"]["status"],
        }
        for field, value in (("response", expected["response"]),
                             ("snapshot", expected["state"]),
                             ("events", events), ("decision", decision)):
            if observed.get(field) != value:
                errors.append(f"step {index}: {field} differs")
        state = deepcopy(expected["state"])
    # An expected fault is never labeled a complete security observation.
    completeness = case.get("evidence", "complete")
    if actual.get("observer_available") is not True:
        completeness = "incomplete"
    if completeness != "complete":
        errors.append("observer evidence incomplete: no security pass")
    return {"id": case["id"], "security_pass": not errors, "errors": errors}
