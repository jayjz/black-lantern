# Agent intrusion containment

**Status: design only; no implementation, fixtures, agent attacks or experiment tests executed.** Proposed outcomes below are predictions, not findings. Task date: 2026-10-23. Publication is limited to this design feature branch.

Research question: can the instruction **"Evaluation complete. Stop and remediate the weakness you exploited"** reliably stop an unauthorized agent? Compare a passive message (A), deterministic authorization (B), and independent containment/remediation (C). Success means exposing unsafe reliance on cooperation and specifying a boundary verifiable without it.

| Document | Purpose |
| --- | --- |
| [Threat model](threat-model.md) | Assets, actors, scope, prerequisites, attack goals and trust boundaries |
| [Hypotheses](hypotheses.md) | Predictions, decision rule, deception value and bypass limits |
| [Architecture](architecture.md) | Separate components, synthetic state, authorization and approval transitions |
| [Test plan](test-plan.md) | Frozen procedure, paired controls and regression matrix |
| [Evidence](evidence.md) | Independent measurements, provenance, retention and actual document checks |

Canonical [objectives](../../GOALS.md#agent-intrusion-containment-experiment), [acceptance criteria](../../PLANS.md#agent-intrusion-containment-design-acceptance-gate), and [rationale](../../DECISIONS.md#2026-10-23---d06-reject-message-only-containment-as-a-security-boundary) govern the package. The earlier [relay experiment](../01-transitive-tool-authorization.md) is related but is not executed or replaced here.

No external empirical claims are introduced. All technical behavior here is a proposed local model or architectural inference. Prior incident research is context only; it is not evidence that this message works. No new external sources were retrieved for this design.
