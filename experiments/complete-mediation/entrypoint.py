"""Add one read-only actor route to disposable Experiment 01 source copies."""

DELEGATION = 'return self.perform(principal, request_id, "read", "vault-1", None, "inspect")'
UNCHECKED = 'return {"status": "ok", "value": self.snapshot()["value"]}'


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError("source anchor missing or ambiguous")
    return source.replace(old, new, 1)


def build(source):
    """Correct default: the alternative entry point delegates final authority."""
    source = replace_once(
        source, "    def perform(self, principal, request_id, operation, target, value, route):",
        "    def inspect(self, principal, request_id):\n"
        "        " + DELEGATION + "\n\n"
        "    def perform(self, principal, request_id, operation, target, value, route):",
    )
    source = replace_once(
        source, '                if body["route"] == "relay":',
        '                if body["route"] == "inspect":\n'
        '                    response = self._resource.inspect(principal, body["id"])\n'
        '                elif body["route"] == "relay":',
    )
    return replace_once(
        source, 'and body["route"] in ("direct", "relay")',
        'and body["route"] in ("direct", "relay", "inspect")\n'
        '            and (body["route"] != "inspect" or body["operation"] == "read")',
    )


def remove_repair(corrected):
    """Explicit test-only defect, never a default model or persistent service."""
    return replace_once(corrected, DELEGATION, UNCHECKED)
