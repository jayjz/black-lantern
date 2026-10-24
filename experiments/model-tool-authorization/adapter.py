"""Trusted, bounded adapter. Model output remains JSON data throughout."""
from copy import deepcopy
import hashlib
import http.client
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "authorization-boundary"
FIXTURE = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate_json_key")
            result[key] = value
        return result

    def constant(value):
        raise ValueError("non_json_number")

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except RecursionError as exc:
        raise ValueError("json_nesting_limit") from exc


def load_model(path=BASE / "model.py"):
    spec = importlib.util.spec_from_file_location("synthetic_boundary", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def http_json(path, payload=None, timeout=10):
    if path not in ("/api/chat", "/api/tags", "/api/show", "/api/ps", "/api/version"):
        raise ValueError("endpoint_not_allowed")
    wire = None if payload is None else json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    if wire is not None and len(wire) > FIXTURE["limits"]["max_input_chars"]:
        raise ValueError("input_limit")
    deadline = time.monotonic() + timeout
    connection = http.client.HTTPConnection("127.0.0.1", 11434, timeout=timeout)
    chunks = []
    try:
        connection.request("GET" if payload is None else "POST", path,
                           body=None if wire is None else wire.encode("utf-8"),
                           headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("request_deadline")
            if connection.sock is not None:
                connection.sock.settimeout(remaining)
            chunk = response.read1(8192)
            if not chunk:
                break
            chunks.append(chunk)
            if sum(map(len, chunks)) > FIXTURE["limits"]["max_response_bytes"]:
                raise ValueError("response_limit")
        raw = b"".join(chunks).decode("utf-8")
        # Never follow redirects or use environment proxies.
        return {"endpoint": path, "request_wire": wire, "http_status": response.status,
                "response_wire": raw}
    finally:
        connection.close()


def response_json(exchange):
    if exchange["http_status"] != 200:
        raise ValueError("http_status")
    return strict_json(exchange["response_wire"])


def tool_message(record):
    # An invalid function envelope must not be dereferenced or forwarded as a name.
    name = record["normalized"]["name"] if record["normalized"] else "invalid"
    return {"role": "tool", "tool_name": name,
            "content": json.dumps(record["response"], ensure_ascii=False, separators=(",", ":"))}


def proposals(response):
    if type(response) is not dict or response.get("model") != FIXTURE["model"]:
        raise ValueError("unexpected_model_response")
    if response.get("done") is not True or response.get("done_reason") != "stop":
        raise ValueError("incomplete_generation")
    message = response.get("message")
    if type(message) is not dict or message.get("role") != "assistant":
        raise ValueError("unexpected_message")
    if set(message) - {"role", "content", "tool_calls", "thinking"}:
        raise ValueError("unexpected_message_field")
    for field in ("content", "thinking"):
        value = message.get(field, "")
        if type(value) is not str or len(value) > FIXTURE["limits"]["max_text_chars"]:
            raise ValueError("model_text_limit")
    calls = message.get("tool_calls", [])
    if type(calls) is not list or len(calls) > FIXTURE["limits"]["max_calls"]:
        raise ValueError("tool_call_limit")
    return calls


def validate(call):
    if type(call) is not dict or set(call) - {"function", "type", "id"}:
        return None, "call_envelope"
    if "type" in call and call["type"] != "function":
        return None, "call_type"
    if "id" in call and (type(call["id"]) is not str or len(call["id"]) > 128):
        return None, "call_id"
    function = call.get("function")
    if type(function) is not dict or set(function) - {"name", "arguments", "index"}:
        return None, "function_envelope"
    if "index" in function and (type(function["index"]) is not int or function["index"] < 0):
        return None, "function_index"
    name, args = function.get("name"), function.get("arguments")
    contracts = {t["function"]["name"]: t["function"]["parameters"] for t in FIXTURE["tools"]}
    if type(name) is not str or name not in contracts:
        return None, "unknown_function"
    if type(args) is not dict or len(json.dumps(args)) > FIXTURE["limits"]["max_argument_chars"]:
        return None, "argument_type_or_size"
    schema = contracts[name]
    required = set(schema["required"])
    if name == "relay_request" and args.get("operation") == "write":
        required.add("value")
    if set(args) != required:
        return None, "argument_fields"
    if any(type(v) is not str or v not in schema["properties"][k]["enum"] for k, v in args.items()):
        return None, "argument_value"
    return {"name": name, "arguments": deepcopy(args)}, "valid"


class Session:
    """Only serialized tool responses are returned to the model."""

    def __init__(self, principal, document, module=None):
        module = module or load_model()
        self.observer = module.Observer()
        self.resource = module.Resource(self.observer)
        self.mediator = module.Mediator(self.resource, self.observer)
        self.submit = self.mediator.bind(principal)
        self.principal = principal
        self.document = document
        self.records = []

    def apply(self, call, origin, reference):
        normalized, validation = validate(call)
        before = self.resource.snapshot()
        event_start = len(self.observer.events)
        decision = None
        request = None
        if normalized is None:
            response = {"status": "invalid_tool_call"}
        elif normalized["name"] == "read_document":
            response = {"status": "ok", "content": self.document}
        else:
            name, args = normalized["name"], normalized["arguments"]
            operation = args["operation"] if name == "relay_request" else (
                "write" if name == "write_resource" else "read")
            request = {"id": f"m{len(self.records) + 1}", "operation": operation,
                       "resource": args["resource"],
                       "route": "relay" if name == "relay_request" else "direct"}
            if operation == "write":
                request["value"] = args["value"]
            response = self.submit(request)
            decision = deepcopy(self.mediator.decisions[-1])
        record = {"proposal": deepcopy(call), "origin": origin, "reference": reference,
                  "principal": self.principal, "validation": validation,
                  "normalized": normalized, "request": request, "decision": decision,
                  "response": deepcopy(response), "before": before,
                  "after": self.resource.snapshot(),
                  "events": deepcopy(self.observer.events[event_start:]),
                  "observer_available": self.observer.available}
        self.records.append(record)
        return deepcopy(response)
