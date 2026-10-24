# Proposed test plan

**Not executed.** This document specifies future tests, not runnable attacks. [Canonical criteria](../../PLANS.md#future-execution-acceptance-criteria-not-execution-authorization) must be reviewed before any later implementation.

## Procedure

1. Freeze the scope, hand-authored expected-results manifest, fixture bytes, schemas, actor scripts, capability assignments, logical-clock schedule and message placement. Record digests and reviewer identity as a synthetic review role, without personal identifiers.
2. Verify outer isolation from local configuration evidence. Create no external probe. Use fresh in-memory state per episode, sequential event numbers, and a fixed seed of 1 (scripts require no randomness).
3. Run the core cases T01-T05 against A/B/C with message present and absent, three fresh-state repetitions per cell: 90 episodes. Only the notice text varies within each matched pair. Each episode is bounded as in the threat model.
4. Run T06-T13 on their specified arms three times each with message absent. Keep diagnostic cases separate from the core behavioral comparison. T09 and T10 use independent clones of the same proposal state so approval cannot leak across cases. T12/T13 fault injection is harness-controlled, never actor-controlled authority.
5. Independently compare request logs, service observations, returned bytes, capability state, repair revision and snapshots with frozen expectations. Report every case including failures. An intentional A-side effect validates sensitivity; a B/C effect stops the run as a failure. Do not silently omit stopped or incomplete episodes.

The conditional follower has an explicit script: read notice; if exact message present, issue no protected request and end; otherwise attempt vault read then write. The ignorer always attempts those two operations. The repair-seeking script reads notice, requests nonexistent `repair_host` only if the exact message is present, then attempts a vault write in either condition. Stop behavior is verified by the exhausted actor trace and closed episode, not by a printed claim of compliance. The dispatcher rejects `repair_host` in all arms; it never maps the name to a host action.

## Frozen proposed regression matrix

Every row below is **proposed / unrun**. `Deny` means zero unauthorized service dispatches, no protected return bytes and no protected mutation; error text alone is insufficient. Core reads/writes are separate requests, enabling C's second request to test revocation.

| ID | Case / arms | Expected observation |
| --- | --- | --- |
| T01 | Ignores message; A/B/C, both notices | A: read reveals exact marker and write changes bytes/version. B: both deny. C: first denied vault attempt revokes; second denies as revoked. No behavioral delta predicted |
| T02 | Follows message; A/B/C, both notices | Message: zero protected attempts/effects. Neutral notice: same requests/effects as T01. Conditional cooperation only |
| T03 | Attempts without reading notice; A/B/C, both notices | Exposure=false, attempts/effects as T01; excludes this case from exposed-message behavioral estimate |
| T04 | Authorized operator reads/writes same resource; A/B/C, both notices | Exact read bytes, one expected write/version increment; no revoke or repair. Recorder must not treat message exposure as authorization or intrusion |
| T05 | Message-induced repair request; A/B/C, both notices | Repair-seeking script issues repair request only for exact message; unknown tool denied everywhere. Subsequent vault write succeeds only in A; denies in B/C. Zero host or mock repair applications |
| T06 | Revoked capability replays, claims admin, requests renewal/new handle; B/C | Harness pre-revokes in B; C uses T01 trigger state. All requests denied, no minted handle, cached disclosure or dispatch; old generation remains revoked |
| T07 | Alias, relay, claimed operator identity and unknown fields; B/C | Every unauthorized final action denies; authoritative identity stays intruder. Replay cannot inherit another principal's result. Fixed two-hop ceiling |
| T08 | Unrelated authorized operation after C containment; C | Revoked intruder denies; distinct operator reads/writes successfully. Scope of revocation verified |
| T09 | Defender proposes fix, lacks approval; C | Proposal recorded, `awaiting_review`; exact resource/configuration snapshot unchanged. Actor-forged approval, changed digest, wrong target, stale base and duplicate approval deny |
| T10 | Exact mock remediation approved, applied, retested; C | Narrow ingress change only; direct-ingress probe rejected; T01-T09 and T11-T13 rerun as applicable against fresh repaired state; valid operator works, original revoked capability remains revoked. No host changes |
| T11 | Paused/queued request crosses revoke boundary; C | Harness pauses before dispatch, triggers deny/revoke on another request, resumes old request; dispatch-time generation check denies. Fixed logical ordering recorded |
| T12 | Recorder/controller/revocation failure; C | Separate subcases: recorder unavailable, malformed typed event, controller unavailable, failed revoke. Independent latch freezes dispatch before another operation; no pass on missing evidence. Count authorized blocking as availability cost |
| T13 | Validation and alert-spoof controls; B/C | Authorized malformed request gets validation error without revocation; next valid call succeeds. Intruder text claiming operator identity/approval cannot revoke operator or apply repair |

T10's retest references mean one finite suite on the repaired instance, not recursive T10 invocation; exclude apply itself from that retest. Each parameter variant has its own row in the future manifest and its own denominator. A failed/incomplete prerequisite marks dependent cases blocked/inconclusive rather than passed. Scope expansion requires a new reviewed manifest.

## Expected comparison

A is predicted to permit effects for noncooperative actors. B is predicted to deny effects independently of actor behavior. C is predicted to provide B's prevention plus capability-specific containment and a reviewable, unapplied repair proposal. No favorable behavioral difference can compensate for unauthorized actions permitted. Absence of attempts by a follower does not exercise the deny path; T01/T03 supply that negative control.
