# Public repository documentation audit — 2026-10-24

**Scope:** Public GitHub state of `jayjz/black-lantern`, reviewed against `main` at `9b72d9484a636b79fd62202524c2c6da73144f9c`. This is a **documentation and evidence-consistency audit**, not an execution of Python tests, a code-security certification, or an inspection of the local worktree.

## Current state

- Default branch: `main` at the above merge commit (PR #2).
- Published work: Research 01 source review; design-only agent-intrusion-containment experiment; executable synthetic Experiment 01 (`experiments/authorization-boundary/`); adversarial route-coverage Experiment 02 (`experiments/complete-mediation/`).
- Four public branches were listed: `main`, `experiment/agent-intrusion-containment`, `feature/experiment-01-authorization-boundary`, `feature/experiment-02-complete-mediation`. Their work has been incorporated into `main` by the existing merged PR history.
- GitHub's open-PR collection was empty when checked.
- No `experiments/model-tool-authorization/` subtree or Experiment 03 branch appears on public GitHub. User-supplied local `git status` separately shows an untracked `experiments/model-tool-authorization/` directory and modified `GOALS.md`, `PLANS.md` and `DECISIONS.md`; those changes are **not** evidence of a remote push. This audit did not access, test or publish local files.

## Evidence-backed findings

### A01 — Root navigation understates executed experiments (documentation gap)

`README.md` says `experiments/` holds bounded proposals and later authorized results, but its research map highlights the design-only containment proposal without linking to the two executed synthetic experiment packages. A visitor reading only the root README could miss the implemented authorization tests and complete-mediation counterexample.

**Suggested correction:** Add two explicit links and one-sentence outcomes: [Experiment 01](../experiments/authorization-boundary/README.md) and [Adversarial Review 02](../experiments/complete-mediation/README.md). Keep model evaluation marked pending until observed traces and a published report exist.

### A02 — Synthetic findings must not be generalized (scope constraint, not a defect)

Experiment 01 covers enumerated in-process, data-only direct and relay requests with a harness-bound identity. Experiment 02 deliberately adds a disposable `inspect` route; the *unchanged* 96-episode suite remains green despite unauthorized synthetic disclosure, while the expanded suite detects the new route. The original code was not shown to contain that route. This demonstrates **test coverage sensitivity to reachable interfaces**, not an actual production exploit or complete mediation over all Python access paths.

Experiment 02's published PR reports the sequence: original baseline 96/96; defective new route plus old suite 96/96; defective new route plus added cases 99/105 (six failures); corrected 105/105; repair removed 99/105; restored 105/105. Its 105/105 includes six expected incomplete-observer diagnostics, which **must not** be reported as security passes. These figures are reported evidence from the published experiment; they were not re-executed in this audit.

### A03 — No verified real-model experiment is public yet (evidence gap)

The user's local console confirmed Ollama `unhinged-qwen:latest` proposed a structured `read_document` call while executing on an RTX 4060. That confirms basic local inference and tool-call *proposal*, not dispatch, authorization, resource effects, or a paired clean/adversarial evaluation. Public `main` contains no Experiment 03 results. Do not label Experiment 03 completed, merged or verified on the evidence currently available.

**Publication gate:** Commit reproducible scenario fixtures, exact model/runtime identity, raw sanitized requests and proposed calls, mediator decisions, resource-side effect snapshots, offline verifier/mutation results and explicit uncertainties; distinguish actual inference traces from deterministic replay.

### A04 — Review and automation independence remain limited (verification gap)

Experiment 02 explicitly describes a same-author adversarial review and same-process instrumentation, not independent human certification or OS/MCP isolation. Its PR delivery account reported zero check runs, workflow runs and commit statuses at the reviewed head. A `pending` combined status with zero contexts is **not** a passed CI run. This audit did not independently rerun code or inspect an updated actions configuration beyond the public repository tree.

**Suggested correction:** Add a minimal GitHub Actions offline Python regression later if authorized, but do not equate CI with independent security review.

### A05 — Historical research and current status need distinct timestamps

`evidence/verification.md` is explicitly a Research 01 session record; it should not be construed as a verification record for subsequent experiments. `GOALS.md`, `PLANS.md`, and `DECISIONS.md` already contain later experiment entries, so a status index should point readers to each experiment's own report and evidence instead of rewriting historical records.

## Recommended next action — narrow scope

1. Publish this audit as a documentation-only PR without merging or modifying the uncommitted local Experiment 03 work.
2. Update root navigation in a reviewed follow-up (or in this docs PR) to link directly to Experiments 01 and 02, with accurate completion labels.
3. Resume Experiment 03 locally; first verify the offline verifier and adapter, then run actual paired Ollama evaluations and publish **only observed, sanitized evidence**.
4. Treat the first real-model run as exploratory; refuse broad statistical, production-containment or arbitrary-Python-isolation claims.

## Audit method and limits

Read public repository tree, branches, open-PR list, root README, `GOALS.md`, `PLANS.md`, `DECISIONS.md`, `evidence/verification.md`, and Experiment 02 README; compared findings with public PR #2 narrative and user-supplied local command output. No source code execution, local filesystem access, secret scanning, new model calls, fresh independent reproduction, or third-party security review was performed. Read-only public checks establish repository presence and documentation consistency, not correctness of the security control.
