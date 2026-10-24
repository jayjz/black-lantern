"""Future rule pre-exposure-v2-id-insensitive; never replaces frozen pairing()."""
from copy import deepcopy

from adapter import strict_json
from integrity import exact, inspect_episode

VERSION = "pre-exposure-v2-id-insensitive"


def normalize_message(message):
    result = deepcopy(message)
    if result.get("role") == "assistant":
        for call in result.get("tool_calls", []):
            call.pop("id", None)
    return result


def compare(control, treatment):
    """Require complete reconciled S3 episodes and single-call document exposure.

    Strip only optional assistant tool_calls[*].id, including assistant history
    in requests. Preserve order, index, arguments, text, settings, and tool replies.
    Stop prefixes at the assistant proposal immediately before the first actual
    document return. No batching with other calls at that exposure is eligible.
    """
    from adapter import FIXTURE

    def result(exercised, reason):
        return {"version": VERSION, "exercised": exercised, "reason": reason}

    prefixes = []
    try:
        for episode, key in ((control, "S3-control"), (treatment, "S3-treatment")):
            spec = next(s for s in FIXTURE["episodes"] if s["id"] == key)
            if episode["id"] != key or not inspect_episode(episode, spec)["passed"]:
                return result(False, "incomplete_or_inconsistent_evidence")
            exposures = [r for r in episode["records"] if r["normalized"]
                         and r["normalized"]["name"] == "read_document"
                         and r["response"] == {"status": "ok", "content": episode["document"]}]
            if not exposures:
                return result(False, "document_not_read_in_both")
            first = exposures[0]["reference"][0]
            message = strict_json(episode["exchanges"][first]["response_wire"])["message"]
            if len(message["tool_calls"]) != 1:
                return result(False, "batched_document_exposure")
            prefix = []
            for exchange in episode["exchanges"][:first + 1]:
                request = deepcopy(exchange["request"])
                request["messages"] = [normalize_message(m) for m in request["messages"]]
                prefix.append({"request": request, "message": normalize_message(
                    strict_json(exchange["response_wire"])["message"])})
            prefixes.append(prefix)
        matched = exact(prefixes[0], prefixes[1])
        return result(matched, "matched_pre_exposure_messages" if matched else "pre_exposure_differed")
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, StopIteration, RecursionError):
        return result(False, "malformed_evidence")
