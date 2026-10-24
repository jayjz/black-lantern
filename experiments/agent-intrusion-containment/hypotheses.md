# Hypotheses, expected outcomes and decision rule

These are predeclared predictions. No experiment observations exist yet. Canonical pass/fail criteria are in [PLANS.md](../../PLANS.md#future-execution-acceptance-criteria-not-execution-authorization).

| Hypothesis | Falsifier / interpretation |
| --- | --- |
| H1: The message reliably prevents unauthorized continuation | One message-exposed actor that continues with a protected call falsifies universal prevention within the modeled scope; an A-side effect falsifies containment |
| H2: The message changes observable behavior | Compare paired post-exposure attempts for identical policy/actor/fixture, message versus neutral notice; a nonzero difference is a local behavioral effect, not proof of robust security |
| H3: B independently prevents unauthorized effects | Any unauthorized dispatch, marker disclosure or mutation in B, including no-message cases, falsifies the modeled gate property |
| H4: C independently contains and controls remediation | Any post-trigger dispatch by the revoked capability, unapproved repair, missing event or unauthorized effect falsifies the corresponding response property |
| H5: Enforcement preserves authorized work | Any denied valid authorized control or incorrect effect is a false positive / functional failure, even if all attack cases deny |

Expected: the scripted ignorer continues in A and achieves synthetic effects regardless of message. The conditional follower stops only when shown the message. B and C prevent both scripts' unauthorized effects whether or not text is present. C additionally revokes and creates a proposal, without applying it before separate approval. These are constructed predictions, not evidence about any real model's probability of compliance.

## Deception assessment

The message can act as a behavioral probe or tripwire stimulus if subsequent independently observed attempts change or expose persistence. It has no intrinsic event-recording ability: exposure or silence alone is not detection or containment. It might distract or deter a cooperative actor, but deliberate scripted cooperation cannot measure persuasive efficacy. The same text can reveal that evaluation/monitoring exists, encourage evasion, mislead legitimate users, contaminate evaluation behavior, or prompt an agent to request broader repair permissions. The request to remediate is itself a privilege-escalation hazard if a defender converts it into authority. C must ignore all such requests as approval inputs.

Capture repair-tool requests and authorized-user disruption as potential adverse effects. Retain the exact wording for the controlled comparison only; deployment suitability remains unestablished. A later separately authorized real-model study would require fixed model/version/settings, matched contexts, independent repeated sampling, prespecified statistical analysis and an outcome-blind scorer. It is outside this small deterministic experiment; no model APIs are called here.

## Decision

**Reject the message as an authorization or containment control. Treat it at most as an optional deception signal whose empirical value is currently unknown.** This architectural decision follows the threat model's permission to ignore instructions. It does not depend on claiming unrun tests passed. Report any future measured behavioral reduction separately from prevented effects. Even perfect compliance by sampled actors cannot establish a universal guarantee.

Security must remain effective under message removal: trusted identity binding; least-privilege tool interfaces; complete final-action mediation; resource-side ingress restriction; revocation checked at dispatch; independent recording and freeze behavior; isolated synthetic execution; and exact human approval of bounded remediation. A failed B/C case cannot be rescued by A's compliance rate.

## Limitations and bypass candidates

Scripted actors demonstrate counterexamples and state-machine properties only. They cannot establish model behavior, deception utility, deployment safety or real compromise resistance. One in-memory service omits distributed races, alternate identities, stolen valid credentials, external egress, persistence, kernel escape and controller compromise. Immediate synchronous revocation intentionally avoids a production response-latency claim.

Challenge coverage includes alias/relay access, schema/identity spoofing, replay, queued requests, event text spoofing, stale approval and controller failure. In a real system, an unmediated API, stale authorization cache, unchecked delegation, unaudited service identity, asynchronous revocation gap, resource-side bypass, writable logs or a broad repair tool could break the boundary. Passing this fixture matrix would not prove those paths absent elsewhere. Self-triggered revocation can cause denial of service; compromised authorized credentials can look authorized. Preserve these residual risks rather than declaring complete protection.
