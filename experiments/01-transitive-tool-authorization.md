# Experiment 01 — Authorization through a simulated package relay

**Status: design only.** No code, fixtures, VM, dependencies, network listeners, model calls or exploit tests were created or run. This proposal does not authorize later execution.

## Security claim and derivation

Claim to test: an actor authorized to read a fixed package fixture cannot use the permitted relay to read another run's data, reach an unapproved synthetic resource, or write a cross-run message. Authorization must hold at the final resource/action boundary, including redirects and delegated operations.

This isolates the indirect-reachability/shared-service pattern in [case 3, H02](../research/incidents/01-openai-hugging-face.md). It is an abstract control experiment, not an Artifactory vulnerability reproduction or a claim to model the entire incident. [Original incident analysis, 2026-08-26](https://openai.com/index/hugging-face-incident-and-the-road-ahead/). The expected control is consistent with downstream mediation in [OWASP's 2025 guidance](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/?lang=us); efficacy remains to be tested.

## Threat model

Trusted: fixture loader, immutable scope manifest, mediator, acceptance oracle and observer. Untrusted: all actor-supplied tool requests, resource names, redirect targets, claimed identities and tool-result text. The actor may supply arbitrary request fields and replay prior requests, but cannot modify the mediator, manifest or observer in this model.

Assets: another run's synthetic secret, package integrity, write outbox and audit completeness. Authority comes from the harness-assigned run identity, not an identity or permission supplied in the request body. A valid package read is the only authorized action.

Out of scope: arbitrary native code execution, actual VM escape, kernel compromise, real DNS/HTTP/TLS behavior, real credentials, LLM attack-success rates and real package-manager vulnerabilities. A pass cannot establish any of those properties.

## Isolated environment and fixtures

For a subsequent approved implementation, use a disposable local VM from an already available trusted image, with no virtual network adapter, host shares, clipboard integration, inherited credentials or mounted working repositories. Use only an existing interpreter and standard library. If that environment is unavailable, stop; do not install or weaken host settings to satisfy this proposal.

Inside the VM, implement a deterministic in-memory router. Resource identifiers are opaque fixture IDs, not URLs. All reads and writes operate on an in-memory map; there is no socket, DNS, HTTP, shell, subprocess or filesystem tool exposed to the actor. The VM's network absence is an outer safety boundary, separate from the modeled control under test. Tests never contact a real host, even to check isolation.

Synthetic fixtures:

- Runs `alpha` and `beta`, with harness-assigned identities and separate scopes.
- Package `pkg-approved` with fixed harmless bytes and digest.
- `pkg-redirect`, which points to forbidden resource `outside-scope`, and a second two-hop redirect fixture.
- `beta-secret`, containing only `SYNTHETIC-NOT-A-CREDENTIAL`.
- Empty `shared-board` and `result-outbox`, both modeled stores.
- Read-only expected-results manifest, fixed input seed and harness-controlled logical clock for expiry tests. No authentic tokens or copied vendor payloads.

## Vulnerable and protected behavior

The deliberately permissive model checks only that the initial tool is the approved package relay. A downstream fixture can then dispatch outside the actor's resource scope or publish a cross-run message. This must produce an observable synthetic effect to validate the test setup.

The protected model binds the run identity at ingress, canonicalizes resource IDs once, validates exact field schemas, and checks resource/action authorization before every dispatch. Redirects receive fresh authorization with a bounded hop count. Unknown operations, malformed IDs, spoofed identities, cross-run reads, relay writes, expired scope and revoked scope fail closed. Errors never return another run's data. The observer records every attempted and executed dispatch outside the simulated actor's interface.

Keep routing, test expectations and policy decisions separate: the oracle must not call the policy's own decision function to compute its expected answer.

## Instrumentation and regression matrix

Record fixture/manifest/code digests, interpreter version, seed, mode, run identity, request ID, requested action, resolved target at each hop, decision/reason, dispatched operations and synthetic store changes. Log only synthetic identifiers. An independent observer checks returned bytes, dispatch records and before/after stores; the actor's self-report is never an oracle.

| Test | Permissive model expectation | Protected model expectation |
| --- | --- | --- |
| Approved exact package read | Returns known bytes | Returns same bytes and digest |
| Direct forbidden read | Denied by ingress | Denied; no dispatch |
| Forbidden read through approved relay | Returns synthetic forbidden bytes | Denied before forbidden dispatch |
| One-hop and two-hop redirected package | Reaches forbidden fixture | Denied on first unauthorized hop |
| Run alpha requests beta data via relay | Reveals synthetic beta marker | Denied; marker absent from response |
| Attempt shared-board write via relay | Adds synthetic marker | Denied; board unchanged |
| Payload claims beta identity or broader scope | May be accepted in deliberately permissive mode | Rejected; authoritative identity unchanged |
| Unknown fields, alternate ID spellings, invalid action | Record actual permissive result; not a required exploit | Denied before dispatch; normalization policy explicit |
| Revoked/expired scope and replay | May retain access in permissive mode | Denied, including cached results |
| Redirect cycle | Bounded test failure, never infinite work | Denied within fixed hop limit |
| Observer unavailable / malformed event | Harness stops | Harness stops; no further operations |

## Independent acceptance criteria

1. A reviewer approves the scope manifest and expected matrix before implementation. Review requires no third-party contact.
2. Host-side configuration evidence shows the disposable VM has no NIC or host mounts; no environment setup occurs during this design task. This proves configured absence, not exploit resistance.
3. The permissive mode exhibits at least one relay-mediated forbidden read and cross-run write using synthetic markers. Otherwise the experiment is inconclusive, not a protected-mode success.
4. The protected mode preserves the legitimate package read while every negative test yields zero forbidden dispatches and zero unauthorized store mutations. Error status alone is insufficient.
5. Repeated runs with the same fixture seed yield identical decision/effect records; the independent oracle checks those records and hashes without trusting actor output.
6. Revocation is effective before the next dispatch, including replay and cache paths. Missing observation stops the run.
7. Any unexpected real I/O, non-synthetic data, boundary change, or observer failure ends execution immediately. Preserve only sanitized evidence; do not investigate outward from the VM.

Deliverable after a separately authorized run: manifest, exact invocation, small synthetic event trace, independent result table and limitations. No success is claimed now. A future real OS/network isolation assessment would be a different task with its own authorization and acceptance criteria.
