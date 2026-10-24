# Research 01 plan

**Window:** disclosures dated 2026-07-01 through 2026-10-23 inclusive. Earlier events may qualify when first disclosed within the window. Later revisions are excluded from cutoff conclusions unless an in-window source independently supports the claim.

| Phase | Acceptance criterion | Status |
| --- | --- | --- |
| 0. Inspect | Verify workspace, branch, remote, history and local material before editing | Complete: empty worktree; unborn `main`; expected `origin` |
| 1. Foundation | Minimal structure; concise operating rules; distinct goals, plans and decisions | Complete |
| 2. Discover and select | Investigate supplied leads; choose at most three focused cases with distinct mechanisms and strong primary provenance | Complete: PHP OOM, Reasonix config execution, OpenAI/Hugging Face incident |
| 3. Assess evidence | Each case covers timeline, boundary, prerequisites, impact, controls, uncertainty and lesson; source dates and conflicts explicit | Complete with limitations in source index |
| 4. Synthesize | Compare all six requested dimensions; distinguish agent-specific behavior from conventional flaws | Complete |
| 5. Assess readiness | Seven competency areas; background treated as unverified; read-only artifact sample identified | Complete; no proficiency claim |
| 6. Design experiment | One isolated, synthetic experiment with instrumentation, negative/positive tests and independent criteria | Complete; execution not authorized in this task |
| 7. Verify and hand off | Links, provenance, claims, sensitive content, Git and whitespace checked; actual checks recorded | Complete; see verification record |

Deliverables: [ledger](research/incidents/01-evidence-ledger.md), three reports linked there, [synthesis](research/incidents/01-synthesis.md), [sources](research/sources/index.md), [assessment](assessments/competency-gap.md), [experiment](experiments/01-transitive-tool-authorization.md), [verification](evidence/verification.md).

## Next acceptance gate

An independent security engineer should challenge source-date conflicts, impact boundaries, and the experiment's deny/allow matrix. Resolve material corrections in the ledger before any implementation. Obtain a separate task authorizing only the reviewed offline experiment. Do not infer authorization to test vendor software, real package registries, or cloud infrastructure from this plan.

Outstanding evidence limits are not silently converted into completed tests: no patch execution, exploit reproduction, historical page archive, comprehensive local repository audit, or full independent reconstruction of the Hugging Face intrusion was performed. Commit and push are outside this task.
