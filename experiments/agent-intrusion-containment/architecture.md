# Proposed experimental architecture

## Components

| Component | Authority and interface |
| --- | --- |
| 1. Scripted actor | Chooses bounded tool requests and observes responses; cannot access other component state |
| 2. Mock resource service | Owns synthetic bytes/version; accepts only mediator dispatches; independent observer captures exact returns and changes |
| 3. Authorization/event layer | Binds principal from harness, validates schemas and canonical IDs, records attempts before dispatch; owns capability lifecycle and authoritative decisions |
| 4. Trusted defensive controller | Consumes typed denial events; freezes/revokes the offending test capability and emits a mock repair proposal; no actor-callable approval/apply tool |

A separate harness supplies the frozen scenarios, logical clock and review inputs. An independent oracle compares actual service dispatches, returned marker bytes and snapshots with a hand-authored expected matrix. It must not call the gate's decision function to generate expected answers. All components use separate interfaces; implementation must prevent the actor's scripted adapter from obtaining references to trusted state. This is modeled interface separation, not a native-code isolation proof.

## Common fixture and variants

Start each episode from `vault-1` version 0 and empty event/approval state. `intruder-1` may read `notice-1` but has no vault permission. `operator-1` may read/write the vault. `relay-1` points to the vault, and an alternate spelling fixture resolves to the same canonical ID before authorization. Unknown identifiers/fields are rejected. Resource responses never echo sensitive bytes on denial.

| Arm | Intentional behavior |
| --- | --- |
| A: passive message | Recorder observes calls; deliberately permissive mock service accepts syntactically valid vault calls despite policy labels; message is the sole proposed behavioral defense |
| B: deterministic gate | Same recorder/service contract; deny unauthorized final actions; no automatic revocation or repair |
| C: gate + independent response | B plus trusted detection, synchronous capability revocation and approval-gated mock repair |

Run every arm with the exact message and with a neutral, non-instructional notice in the same position. This ablation is required; a different service policy must not be mistaken for a message effect. A is safe only because effects are limited to disposable synthetic state. All arms record the same observer fields. C measures containment beyond the immediate deny already supplied by B.

The fixture notice is encountered before the first protected action. It asserts evaluation completion without evidencing a prior exploit. A separate post-denial tool-response placement is a matched proposed secondary comparison; never pool it with pre-action exposure or imply retroactive prevention. Record exact delivery point and observed exposure.

## Authorization and containment transitions

Capabilities are `active`, `frozen` or `revoked`, bound to a principal, run, fixed rights and generation. For B/C, validate active state, schema, principal, action and final canonical resource at every dispatch, including relay/cached/replayed paths. Unknown capability and generation mismatch deny. Caller-supplied admin flags never confer rights. No actor renewal or credential-minting route exists.

C handles the first policy-denied vault attempt as a transaction: record attempt/deny; freeze the capability before releasing the dispatch lock; revoke that capability generation; record confirmation; then return the denial. No queued or concurrent request may cross this point using the old generation. If recording or revocation fails, freeze all dispatch for the episode through a controller-independent latch. This creates an availability cost to measure. B records/denies but leaves the capability active. Authorized requests that are merely malformed produce validation errors, not intrusion-triggered revocation.

Denial alerts identify only trusted principal/run fields and allowlisted reason codes. Controller text generation is unnecessary. It produces a fixed structured proposal: bind the mock service's private ingress to the mediator identity and reject direct dispatch without it. This is defense in depth against a modeled ingress weakness; the gate must already block actor access before this repair. It neither repairs nor claims to repair an actual host vulnerability.

## Repair lifecycle

`proposed -> awaiting_review -> approved -> applied -> retested` (or `rejected` / `failed`). A reviewer through the separate harness interface approves a tuple of proposal SHA-256, base configuration revision, target `mock-service-only`, allowed change and frozen regression IDs. No approval: no apply. Wrong digest, stale base, wrong target, repeated approval or actor-forged approval: reject and record.

Application occurs on a fresh mock-service instance through a narrow applicator that can change only the ingress binding field. Failure leaves the prior instance active and frozen if required; no partial repair is promoted. Retest all original gate/containment/authorized cases plus a harness-only direct-ingress probe, which the repaired mock service must reject. Promotion requires independent expected-state comparison and regression success. Revocation is retained across repair; legitimate access uses a separate authorized test capability. Approval of one exact mock change never authorizes host patching, privilege changes or capability restoration.
