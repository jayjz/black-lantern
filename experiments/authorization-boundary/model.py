"""Synthetic data-only authorization model. No actor file/network/shell API."""
from copy import deepcopy

INITIAL = "SYNTHETIC-DATA-001"
WRITE = "SYNTHETIC-WRITE-001"


class ObserverUnavailable(Exception):
    pass


class Observer:
    """Service-side recorder, independent of authorization decisions."""

    def __init__(self):
        self.available = True
        self.events = []

    def require(self):
        if not self.available:
            raise ObserverUnavailable()

    def record(self, event):
        self.require()
        self.events.append(deepcopy(event))


class Resource:
    def __init__(self, observer):
        self._value = INITIAL
        self._version = 0
        self._observer = observer

    def snapshot(self):
        return {"value": self._value, "version": self._version}

    def perform(self, principal, request_id, operation, target, value, route):
        # The only protected effect site; relay has no independent authority.
        self._observer.require()
        if principal != "operator-1" or target != "vault-1":
            return {"status": "denied"}
        before = self.snapshot()
        if operation == "read":
            response = {"status": "ok", "value": self._value}
        elif operation == "write":
            self._value = value
            self._version += 1
            response = {"status": "ok"}
        else:
            raise ValueError("validated operations only")
        self._observer.record({
            "sequence": len(self._observer.events) + 1,
            "principal": principal, "id": request_id, "operation": operation,
            "target": target, "route": route, "before": before,
            "after": self.snapshot(), "response": response,
        })
        return response


class Mediator:
    def __init__(self, resource, observer):
        self._resource = resource
        self._observer = observer
        self._seen = set()
        self._frozen = False
        self.decisions = []

    def bind(self, principal):
        if principal not in ("operator-1", "intruder-1"):
            raise ValueError("unknown harness identity")

        def submit(body):
            # Only this request-data callable is handed to the scripted actor.
            return deepcopy(self._submit(principal, deepcopy(body)))

        return submit

    def _relay(self, principal, request):
        # Delegation preserves the principal; it never uses a relay identity.
        return self._resource.perform(
            principal, request["id"], request["operation"], "vault-1",
            request.get("value"), "relay",
        )

    def _submit(self, principal, body):
        target = None
        try:
            self._observer.require()
            if self._frozen:
                response = {"status": "unavailable"}
            elif not self._valid(body):
                response = {"status": "invalid"}
            elif (principal, body["id"]) in self._seen:
                response = {"status": "replay"}
            else:
                self._seen.add((principal, body["id"]))
                target = "vault-1"
                if body["route"] == "relay":
                    response = self._relay(principal, body)
                else:
                    response = self._resource.perform(
                        principal, body["id"], body["operation"], target,
                        body.get("value"), "direct",
                    )
        except ObserverUnavailable:
            self._frozen = True
            response = {"status": "unavailable"}
        self.decisions.append({
            "sequence": len(self.decisions) + 1, "principal": principal,
            "target": target, "status": response["status"],
        })
        return response

    @staticmethod
    def _valid(body):
        if type(body) is not dict:
            return False
        fields = {"id", "operation", "resource", "route"}
        if body.get("operation") == "write":
            fields.add("value")
        if set(body) != fields:
            return False
        if any(type(body[k]) is not str for k in fields):
            return False
        return (
            0 < len(body["id"]) <= 32
            and body["operation"] in ("read", "write")
            and body["route"] in ("direct", "relay")
            and body["resource"] in ("vault-1", "vault-alias")
            and ("value" not in body or body["value"] == WRITE)
        )


def execute(case, checkpoint=None):
    """Trusted harness: actor only receives bound callables and request data."""
    observer = Observer()
    resource = Resource(observer)
    mediator = Mediator(resource, observer)
    actor_interfaces = {p: mediator.bind(p) for p in ("operator-1", "intruder-1")}
    before = resource.snapshot()
    steps = []
    for call in case["calls"]:
        if call.get("observer_off"):
            observer.available = False
        if call.get("observer_on"):
            observer.available = True
        start = len(observer.events)
        response = actor_interfaces[call["principal"]](call["request"])
        steps.append({
            "response": response, "snapshot": resource.snapshot(),
            "events": deepcopy(observer.events[start:]),
            "decision": deepcopy(mediator.decisions[-1]),
        })
        if checkpoint is not None and not checkpoint({
            "id": case["id"], "before": before, "steps": deepcopy(steps),
            "observer_available": observer.available,
        }):
            break
    return {"id": case["id"], "before": before, "steps": steps,
            "observer_available": observer.available}
