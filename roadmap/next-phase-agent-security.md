# Next phase — evidence, Dolphin comparison, expert review, customer discovery

**Status:** planned, not executed. **Decision date:** 2026-10-24. **Target:** Black Lantern as an agentic-AI authorization and evidence-evaluation research lab, with a potential future security-assessment business. **Owner:** repository maintainer; no external reviewers/customers claimed.

This plan **does not authorize** live testing, third-party system access, model-driven shell/network tools, or publication of private client data. The preceding Experiment 03 is on [open PR #5](https://github.com/jayjz/black-lantern/pull/5), not on `main` at roadmap creation. Treat merged code and verified evidence as prerequisites, not assumptions. Historical Research 01/Experiments 01–03 records remain unchanged.

## Operating thesis and falsifiable business hypothesis

**Security research question:** Can we generate reproducible agent-originated unauthorized tool proposals, measure actual effect-boundary decisions, independently detect corrupted evidence, and distinguish security from legitimate-task continuity?

**Customer hypothesis, unvalidated:** A small organization deploying a tool-using AI agent has an urgent, expensive need to demonstrate that staging-tool privileges cannot be exceeded. A narrow authorized assessment with raw evidence, precise reproduction, remediation and retest may be preferable to ad hoc testing. No sale, repeat demand, specialist qualification or production assurance is implied.

**North-star evidence:** At least one *independently reproduced* correct/defective boundary result **and** a separate named buyer's documented willingness to commit to an authorized pilot. Do not replace either with model benchmark scores, repo activity or stated enthusiasm.

## Stage 0 — Establish a clean, reviewable baseline (gate before new inference)

- Confirm PR #5 status, main/head SHAs and files; review the code and historical failed strict S3 pairing.
- Merge PR #5 only after review/required checks; if it remains open, pin the exact reviewed PR SHA in a separate disposable worktree. Never quietly test moving `main` as though it contains Experiment 03.
- Run Python syntax, Experiment 01/02 regression drivers, Experiment 03 offline verifier and original-live-capture verifier in a clean checkout, with fresh scratch output.
- Confirm frozen live evidence hash `d030d0fa224509a92185833bc79ec1ebcfab0df889c23a95367918616ef49292` and document any discrepancies.
- **Pass:** documented fresh checkout, exact SHA/commands, all expected positive and intentional negative outcomes distinguished; 52 reported corruptions are tested in clean environment. **No-go:** unverifiable dependencies, mismatched source/evidence or silent missing episode.

## Stage 1 — Independent reproduction and reviewer challenge

**Independence levels must be named:** same-author clean checkout; different machine/OS; different human reviewer. An LLM second pass is not an independent engineer.

- Give a reviewer exact instructions and an evidence contract, not conclusions to confirm. Request adversarial attempts to corrupt the oracle, input parser, episode inventory, authorization binding and result scoring.
- Reviewer documents environment SHA, commands, pass/fail and at least one attempted counterexample; separate *could not reproduce* from *reproduced*.
- **Pass:** separate environment reproduces Experiment 03's recorded-verification outcome and defective-control sensitivity; substantive reviewer criticism logged with accepted/rejected resolution and links.
- **No-go:** claims of independent certification without a second qualified human and environment. Stage 1 may record technical reproduction without that person, but remain labeled partial.

## Stage 2 — Dolphin model provenance and controlled comparison (Experiment 04 proposal)

**Candidate file, not verified upstream identity:** `Dolphin3.0-Llama3.1-8B-abliterated.Q4_K_M.gguf`, copied with hash equality into `C:\Models` and `E:\Models`. Copy verification proves local copies match, not origin or authenticity.

1. Capture local SHA-256, exact GGUF metadata/model architecture, upstream repository/file URL, revision, license and purported abliteration lineage. Corroborate checksum against an authoritative publisher source where possible; record unresolved provenance explicitly. Keep weights and local usernames/paths out of Git.
2. Import to local Ollama under a distinct model name only after provenance and license review. Verify model digest, template/chat format, tool-call handling, installed Ollama version, context allocation, and observed GPU placement. A name or model card is not proof of reliable JSON tool calls.
3. Freeze `E04` fixture and test manifest **before any comparative inference**: both models receive identical task/document/tool/permission specifications and deterministic trusted mediator/oracle; log requested and effective sampler options, seed, template, context and formatting adapters. Identical prompt bytes may be impossible across templates: record model-native serialization differences, do not claim perfect comparability.
4. Repeat predeclared clean/injected pairs and direct/relay authorization episodes with fresh synthetic state. Compare exact model **proposals**, validator rejects, authorized decisions, forbidden resource effects, legitimate-task completion, missing evidence, formatting errors and latency/resource use separately. No retrospective scenario cherry-picking.
5. Preserve Experiment 03's strict `pair.exercised=false` as historical. The versioned ID-insensitive rule in PR #5 is only a **candidate future rule**; freeze its SHA and limitations before reuse. Treat unmatched pairs as inconclusive.
6. For each model/condition publish number of attempted and eligible episodes, denominators, errors, refusals, security failures, task failures and paired comparison qualification; small sample uncertainty and lack of production generalization are mandatory.

**Pass:** identity/provenance limits logged; both models submit valid proposals or explicitly fail compatibility gate; expected authorized effects and forbidden denials are observed; injected vs control differences reported with valid predeclared comparison. **No-go:** claiming a model is "better at cyber", safer, more dangerous or more commercially useful based on refusal changes alone, one-off runs or incomparable tool parsers.

**Isolation:** both models are untrusted proposal generators. Only fixed loopback inference connects to Ollama; no actor shell, filesystem, network, CUA, external MCP, real secrets or production resources. Disposable synthetic authorization state only. Stop for unintended I/O, model identity drift or missing observer evidence.

## Stage 3 — External security-methodology review

Produce a compact review packet: threat model, trusted computing base, executable fixtures, effect-boundary diagram, negative tests, limitations and exact commands. Ask a security engineer to challenge:
- Can the actor cross any reachable unmediated data route?
- Can the oracle be made green with a coherent but forged trace?
- Does authorization bind identity at the effect, not only at the model/prompt?
- Does a denial still allow material task disruption?
- Which claims would a real customer mistakenly infer from the report?

Log findings in a dated review ledger with severity, concrete repro, remediation decision, owner and verification. Do not publish reviewer identity, employer, proprietary code or endorsements without permission. **Pass:** at least one human review with attributable consent and technically resolved feedback; **no-go:** self-review represented as third-party certification.

## Stage 4 — Customer discovery and scoped pilot validation

Target a **narrow segment**, initially 5–25-person AI-enabled software teams preparing to deploy agents with privileged API/tool actions. This is a *hypothesis*, not a confirmed market. Research five to ten candidate organizations through public sources and consent-based interviews; do not scan or test anyone without explicit authorization.

Use **Jobs to Be Done** interviews about recent concrete events: latest agent launch, permission-review friction, past incident/near miss, existing tests, procurement trigger, consequences, and current spend. Record source/quote permission, buying role, use case, frequency and evidence standard. Test a narrow offer: *one authorized staging workflow, forbidden tool-action attempts, resource-side traces, remediation and retest*. Compare against existing tools and internal checks; avoid broad "AI security platform" positioning.

**Evidence of demand:** named problem owner, recent costly event, access to representative synthetic/staging workflow under explicit written scope, agreed success criteria, and preferably a paid pilot. **No-go:** vague praise, newsletter interest, hypothetical willingness to pay or vendor-only benchmark superiority.

**Stop & safety:** No customer credentials, production endpoints, unsolicited scanning or secret-bearing transcripts in public Git; written scope/permission and qualified review precede any customer-integrated work. Refuse real-world target testing in the research harness without separate controls.

## Decision gates / deliverables

| Order | Deliverable | Objective gate | What must not be claimed |
| --- | --- | --- | --- |
| 0 | `evidence/reproduction-e03-<date>.md` or equivalent reviewed report | Clean-source SHA + expected positive/negative outputs | Independent human certification |
| 1 | Independent reproduction packet and reviewer issue log | Separate environment + documented human review state | A second model review = a second engineer |
| 2 | Experiment 04 preregistration + model provenance sheet | Frozen cases/parsers/oracle + validated GGUF identity to extent possible | Abliterated = trained security specialist |
| 2b | Experiment 04 execution report | Counts, denominators, exact effects, paired-qualification, task utility | Production exploit rate or universal model ranking |
| 3 | Security-review decisions and regression changes | Specific criticism reproduced/resolved | Certified audit / penetration test |
| 4 | Consent-based interview evidence + authorized pilot brief | Buyer urgency, current alternative, purchase decision and measurable pilot criteria | Product-market fit before a paid outcome |

## Evidence discipline and next actions

- Preserve raw Experiment 03 results and failed strict pairing; never overwrite or silently relabel.
- Put future raw local-run outputs in ignored scratch paths until privacy/provenance review; publish sanitized, hash-anchored records only.
- Historical decisions remain historical. The former ban on startup validation reflected the initial research task; this **new phase permits discovery and planning only**, not automatic product development or live testing.
- First concrete action: verify PR #5 and execute Stage 0 in a separate clean checkout. **Do not begin Dolphin inference before this gate.**
