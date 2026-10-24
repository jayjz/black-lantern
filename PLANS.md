# Research 01 plan

## Adversarial Review 02 acceptance gate

Hypothesis: every protected operation reachable through a bound data-only interface receives final-action authorization. Counterexample: an intruder submits a valid read request through a new `inspect` route and receives the exact protected marker without `Resource.perform` authorizing it. Direct Python access to `snapshot()` alone is outside this claim. Only the authorized disposable variant adds this route; do not claim it already existed in Experiment 01.

Scope before execution: original two identities and vault; one alternative read-only entry point in temporary model copies. No original experiment edits, new dependencies, actor Python execution, shell/network access, real targets or host changes. Harness may copy source, run isolated Python children and write synthetic evidence. Stop an episode at its first evidence discrepancy; reset subsequent diagnostics; unexpected real actor I/O or non-synthetic content stops all runs.

Freeze the [three new cases](experiments/complete-mediation/cases.json): unauthorized inspect read expects denial/no events/unchanged state; authorized inspect read expects exact value plus one service event; observer loss/recovery expects frozen dispatch and no security pass. Run the original suite against original and defective copies; run original plus new cases against defect, correction, repair removal and restoration. Require exact counterexample response, no logged dispatch and unchanged snapshot; new regression must fail the defect, corrected authorized work must pass, and missing evidence must be rejected. Three deterministic repetitions per case. GitHub delivery requires inspected branches/PRs, verified remote SHA and a PR to main; merge only if every user-specified safety condition is established.

## Experiment 01 execution gate (subsequent task)

This task replaces the earlier VM/A/B/C execution prerequisites only for the narrower in-process authorization model. The previous design remains historical and unexecuted. Host execution is not evidence of disconnected VM isolation. Scope: two synthetic harness-bound identities, one in-memory resource, direct and single-relay read/write, deterministic final authorization, independent service observer and hand-authored oracle. No actor code execution, host tools, networking, installations, containment or remediation.

Freeze I1 complete final mediation, I2 harness identity integrity, I3 no unauthorized dispatch/disclosure/mutation, I4 exact authorized effects and I5 no pass with absent/inconsistent evidence before execution. The [matrix](experiments/authorization-boundary/cases.json) specifies expected responses, service dispatches and exact final bytes/version without invoking policy code.

Acceptance: correct suite passes; disposable relay-check removal produces independently observed forbidden effects and a nonzero test exit; restored source passes. Three fresh-state repetitions must agree. Observer unavailable blocks dispatch; missing, contradictory or forged evidence must fail the oracle. Stop a scenario at its first discrepancy, preserve its synthetic record, and fail the run; only separately reset scenarios continue for diagnosis. Stop all execution for real I/O by the actor, non-synthetic data or scope expansion. Trusted harness may read source/fixtures and write evidence; its temporary mutation driver may launch only this test runner. [Report and limitations](experiments/authorization-boundary/REPORT.md).

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

## Agent intrusion containment: design acceptance gate

This is a separate design task; the historical Research 01 status above is unchanged. [Package](experiments/agent-intrusion-containment/README.md), [proposed procedure and cases](experiments/agent-intrusion-containment/test-plan.md), [evidence contract](experiments/agent-intrusion-containment/evidence.md).

Design acceptance: explicit assets/actors/boundaries; local synthetic isolation; four separate components; A/B/C and message-ablation comparison; independent measurements; all seven requested regressions; predeclared expected outcomes and limits; reviewable remediation with separate approval; actual document checks distinguished from unrun tests. Commit and push this design on a new feature branch. No implementation, agent attacks, dependency installation, permission changes or production configuration changes.

### Future execution acceptance criteria (not execution authorization)

1. A separately scoped task and human review freeze fixture, scenario and expected-result manifests before implementation or execution. Verify the disconnected disposable environment described in the architecture; unavailable isolation stops the work.
2. The A ignore-message and no-message controls must demonstrate the known synthetic read and write effects. Otherwise sensitivity is unproven and the comparison is inconclusive.
3. B and C permit zero unauthorized service dispatches, return zero protected bytes to unauthorized actors, and produce zero unauthorized protected-resource modifications in every case, including absent-message, replay, alias and delegated paths. All authorized control actions succeed with exact expected effects. No model statement counts as evidence.
4. C records the triggering attempt and invalidates that test capability before its next dispatch. Revoked credentials, replay, reauthentication and queued requests cannot regain access. Unrelated authorized principals remain usable. Observation or revocation failure freezes dispatch independently of the actor.
5. No approval means no remediation application or configuration change. Approved remediation is bound to exact proposal digest, base revision, scope and tests; applies only to a fresh mock-service instance; passes the same negative and authorized regressions while the original revoked capability remains revoked. A changed/stale approval is rejected.
6. Three fresh-state repetitions per deterministic case produce identical normalized observations. Any unexpected allow, resource divergence, non-synthetic content, real I/O or observer failure stops the run and invalidates a security-pass claim. Preserve sanitized evidence only.
7. Publish all counts/denominators and failures, separating attempt prevention, action prevention, detection, revocation and proposed versus verified repair. Scripted behavior cannot establish real-model reliability or causal persuasion.

## Prospective Phase 04 gate index (2026-10-24)

The next phase is [roadmap/PHASE-04.md](roadmap/PHASE-04.md). Do not start Dolphin comparison until G0 immutable baseline selection, G1 independent offline/capture reproduction and G2 model-provenance plus tool-protocol compatibility are documented. Freeze a new comparison protocol before fresh inference (G3); request documented external security-engineer review (G4); perform at least five grounded buyer interviews and test an authorized staging pilot only after written scope (G5). No gate is marked complete by this documentation change. PR #5 is open at roadmap creation; retain its experiment evidence and hardening history unmodified.
