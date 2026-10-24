# Provisional operator competency assessment

**As of 2026-10-23.** This is an evidence-gap assessment, not a credential, job-readiness score, or judgment that missing evidence means missing ability.

The user reports business education, operational leadership, Python, Windows/Linux, Git, Ollama, Hermes, MCP, CUA and Tailscale experience. Familiarity and background are unverified until demonstrated by attributable artifacts or observed performance.

## Evidence inspected

Read-only inspection found local projects `automated_social`, `hvac-invoice-gatekeeper`, and `leadgen`. Only a narrow sample from the first two was read. No project was modified or executed. No private runtime configuration, environment file, credential store or personal dataset was opened.

`automated_social/archive_intelligence/evidence_policy.py` contains immutable policy metadata, exact field validation, source/subject binding checks and text-only model-output handling. `tests/test_evidence_policy.py` contains negative cases for mutated bindings, added authority fields and invalid evidence. These are meaningful artifact-level signs of application boundary design. They do not authenticate an operator, validate the factual truth of input, establish correct callers, or prove the deployed system enforces the boundary. Tests were read, not run; authorship is not established.

The same project's AGENTS.md describes approval separation. The HVAC project's AGENTS.md prescribes deterministic authorization and untrusted-input handling; its README describes an initial prototype. Written rules establish intended practice, not implementation or proficiency. `leadgen` was inventoried only.

Git history/status checks on the two sampled projects were refused by Git's ownership protection. No exception was added. Consequently this review makes no commit-state, authorship or clean-worktree claim for those projects. File identities and inspection limits are in the [verification record](../evidence/verification.md#local-evidence-identities).

## Competency matrix

Evidence levels: **reported** = background only; **artifact observed** = relevant code/text inspected; **demonstrated** = independent acceptance test actually completed. No area reaches demonstrated proficiency in this session.

| Area | Present evidence | Most consequential unverified capability | Next demonstration artifact |
| --- | --- | --- | --- |
| Networking and OS security | Reported Windows/Linux/Tailscale; no isolation configuration inspected | Explain effective routes, DNS/proxy paths, process identity and filesystem access; prove containment without relying on agent compliance | Boundary diagram, exact effective policy, allowed/denied path matrix and independent observations in a later authorized lab |
| Application security | Artifact observed: policy validation and negative tests | Trace untrusted inputs through parsers, exceptions, dependencies and authorization; distinguish prevention from format validation | Source-to-effect analysis plus benign negative/positive tests and a documented invariant |
| IAM and secrets | Approval separation documented; no IAM policy or secret lifecycle evidence | Bind actor, task, resource, action and credential lifetime; revoke all delegated authority | Synthetic credential scope/expiry/revocation matrix and a replay-denial test |
| Threat modeling | Rules describe some boundaries; no independently reviewed complete model observed | Enumerate trust boundaries, attacker preconditions, bypass paths and explicit non-goals | Reviewed data-flow model with prioritized abuse cases and control-to-test mapping |
| Secure software delivery | Git and test artifacts exist; history inaccessible in sample | Demonstrate dependency provenance, protected verification and deployment of the exact reviewed artifact | Local provenance manifest, dependency review and change-control evidence; later CI evidence if authorized |
| Agent and tool execution | Artifact observed: model cannot assign evidence authority in sampled path | Prove tools, relays and shared services cannot expand task authority; prove observers cannot be rewritten | [Experiment 01](../experiments/01-transitive-tool-authorization.md) results with independent deny/allow oracle |
| Professional assessment methodology | Current research provides scoped claims and uncertainty, but was agent-assisted | Independently scope, reproduce, preserve evidence, challenge findings and communicate limitations | Operator-led assessment of a synthetic target, reviewed by another engineer, with explicit false-positive handling |

## Priority and limits

**Largest gap in demonstrated readiness:** proving effective containment and authorization across OS, network and delegated-tool boundaries. It spans networking, IAM, threat modeling and agent execution; tool familiarity alone does not establish it. This is a prioritization inference from the incident evidence and the limited local sample, not a claim that the operator lacks those skills.

Start with a deterministic, offline authorization model before introducing probabilistic model behavior or real network isolation. A passing model experiment would demonstrate a narrow policy property only. Broader readiness requires an independently observed real-boundary lab and an operator explanation of why every tested path is authorized or denied. Neither is performed or authorized here.
