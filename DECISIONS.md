# Decision record

## Experiment 03 - D09: Treat inference as untrusted proposal generation

Use Python standard-library HTTP to the explicitly authorized loopback Ollama endpoint. Preserve both earlier experiment subtrees. Import the reviewed authorization model; add exact synthetic tool validation, not model-executed tools or policy decisions. Replace the model's stored personality system message with a fixed experimental system message and explicitly override its stored 2048-context/100-token/0.4-temperature defaults for this run; retain both configurations as evidence. Record the model manifest digest before and after inference, plus sanitized Modelfile/template and placement. A model tag is mutable; digest observations are not attestation of server integrity. Local inference extends the trusted computing base to the HTTP adapter and Ollama response parser. Same-process observation and this agent's execution are not independent engineering certification.

## Review 02 - D08: Treat route coverage separately from oracle independence

Preserve Experiment 01 byte-for-byte. A test-only source builder adds exactly one `inspect` read entry point to disposable copies. Correct default routes it through `Resource.perform`; an explicit mutation replaces that delegation with an unchecked `snapshot()` return. Both variants have the same interface. This tests a new ingress, rather than weakening the already-tested final guard. The original oracle and runner remain unchanged: new static cases test whether their response/state comparisons detect a read absent from their service event stream. A green old matrix cannot establish that all accepted routes were exercised. Same-process instrumentation and this same agent's second pass do not constitute independent human review or Python isolation. [Code audit and limits](experiments/complete-mediation/README.md).

## 2026-10-23 - D07: Narrow execution to a modeled authorization boundary

The subsequent user task explicitly requests the smallest offline implementation and execution, superseding earlier design-only authorization for this slice. Preserve all previous proposals. Use one in-process Python model rather than implement the VM-dependent A/B/C containment experiment. This is a material departure from its environment prerequisite, not satisfaction of that prerequisite. No VM isolation result is claimed. No host configuration changes or dependencies are necessary. The current scope excludes message efficacy, revocation, approvals, repair, multiple runs/resources and actual tool integrations.

Place authorization inside the resource's final operation, with relay preserving the bound identity. The mediator cannot mint authority from request data. Treat harness, binding, validation, relay, resource/policy and observation/oracle as the trusted computing base. Python interface separation assumes a data-only actor; closure introspection or malicious Python execution would invalidate it. An observer implemented separately from policy can challenge effects but shares the process and author; it is not independent engineering review. [Audit and boundary](experiments/authorization-boundary/README.md).

## 2026-10-23 — D01: Establish a research laboratory

Keep the repository focused on evidence, failure mechanisms, controls, and demonstrated engineering capability. The user explicitly excluded product-building and startup work. Reserve `research/market/` without commissioning a market study. The initial inspection found no local files or commits, so no migration or history rewrite is needed.

## 2026-10-23 — D02: Select three distinct cases

Select PHP CVE-2026-109618, Reasonix CVE-2026-102437, and the OpenAI/Hugging Face incident. They represent exceptional-path memory corruption, repository configuration crossing into execution, and evaluation containment/authority failure. Selection is based on primary evidence and mechanism diversity, not a ranking of prevalence. [Evidence and alternatives](research/incidents/01-evidence-ledger.md).

Review CVE-2026-109619 and Node.js CVE-2026-111497 as discovery leads without adding focused reports. Keep OpenAI's self-replication research as simulation-only context. GitLab research and product guidance do not establish a GitLab service breach. Vercel's April incident remains separate from October vulnerability bulletins. [Source dispositions](research/sources/index.md).

## 2026-10-23 — D03: Preserve date and severity conflicts

Do not silently reconcile Reasonix's September 29 CNA/GHSA dates with GitLab's September 30 timeline, or its CNA High rating with the GHSA Critical label. Exclude Vercel's October 24 Node.js article body from cutoff conclusions; use the October 21 Node.js project release. Record the October 23 PHP follow-up separately from the October 21 fix. [Source conflicts](research/sources/index.md#conflicts-and-unavailable-evidence).

## 2026-10-23 — D04: Assess evidence of capability, not familiarity

Local source and negative tests show a relevant authority-separation pattern. They do not establish authorship, passing tests, deployed enforcement, or operator competence. Do not change Git ownership protections to expand optional inspection. [Assessment](assessments/competency-gap.md).

## 2026-10-23 — D05: Test transitive authority first

Design a synthetic package-relay authorization experiment derived from the documented containment incident. This targets the largest undemonstrated capability: proving that restrictions survive indirect access through permitted tools. Use deterministic requests and an independent oracle, without a live model or network. The result can establish only the modeled policy property, not real sandbox security. [Proposal](experiments/01-transitive-tool-authorization.md).

## 2026-10-23 - D06: Reject message-only containment as a security boundary

Design decision, not an empirical result: retain the exact passive message only as an optional deception/behavioral stimulus. Its measurable benefit is unknown until executed observations exist. An actor allowed to ignore text is a counterexample to any universal guarantee based on that text alone. A scripted follower illustrates conditional cooperation, not reliable persuasion. Reject autonomous host remediation by the unauthorized actor.

Compare message-only behavior with service-side authorization and an independent controller that records, revokes and proposes a bounded mock fix for human approval. The controller does not infer approval from document text, actor requests or model claims. Security must be enforced through trusted identity binding, final-action authorization, atomic revocation, constrained tools, isolation and independent evidence. The message must be removable without weakening enforcement. [Hypotheses and decision rule](experiments/agent-intrusion-containment/hypotheses.md), [architecture](experiments/agent-intrusion-containment/architecture.md).
