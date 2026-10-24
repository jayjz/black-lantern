# Version control policy

This is the review policy adopted by this change, not a claim that GitHub branch protection or hosted CI is configured. Follow [AGENTS.md](../AGENTS.md); preserve canonical [objectives](../GOALS.md), [acceptance](../PLANS.md) and [rationale](../DECISIONS.md).

## Branches and commits

Start narrow branches from freshly fetched `origin/main`: `feature/<topic>` for scripts/behavior, `fix/<topic>` for corrections, `docs/<topic>` for documentation, `experiment/<id>-<topic>` for expressly scoped experiments. Existing names remain valid historical refs. Inspect status, worktrees and refs before switching. Preserve dirty work in its existing branch/worktree; never reset, stash, overwrite or move it implicitly. A clean dedicated worktree is preferred when concurrent work exists.

Use small descriptive commits with reviewed explicit paths. Do not commit credentials, personal identifiers, weights, private model configuration, unreviewed logs or generated caches. Do not force-push shared branches; reconcile main with a normal merge commit when necessary. Recheck scope and tests after conflicts. Do not infer authorization to merge or delete from authorization to commit/push.

## Pull requests and gates

Every PR targets current main and states the concrete problem/result, authorized scope, base/head identities, dependencies/overlap, exact executed commands/exits, expected negative outcomes, evidence links and remaining limits. Distinguish proposed tests from executed tests and local checks from hosted CI. A required review must be attributable to a reviewer; an agent's self-review is not independent certification. Missing statuses are not passing checks.

Required before merge:

- Re-fetch and inspect current main/head, mergeability, reviews, comments, unresolved threads, active repository rules and status/check runs. Respect required reviews/checks; no administration bypass.
- Run `git diff --check` and inspect every changed/staged file for scope and private data. Verify local Markdown links and canonical navigation for documentation changes.
- Parse changed PowerShell/Python source. For launcher changes verify identity handling, localhost-only arguments, inherited configuration isolation, no host tools, bad-path/hash/context rejection and occupied-port refusal. Run an owned loading/inference check only when authorized and resources permit; an explicitly skipped live path must remain visible in the PR and receive reviewer disposition.
- Authorization/evidence changes require the affected positive, negative and mutation regressions with fresh ignored outputs; inspect expected failing child results. Frozen original evidence must have no diff. Do not regenerate it to make tests green.
- Verify the normal pushed head with `git ls-remote origin refs/heads/<branch>`. Review the exact immutable head; stale approvals/checks require fresh assessment after changes.

This task leaves merge and historical deletion for explicit review. [Audit](GIT_AUDIT.md) and [runtime limitations](LLAMA_RUNTIME_AUDIT.md) record this PR's exceptions and skipped checks.

## Evidence retention

Use ignored `evidence/runs/`, `evidence/raw/` or `evidence/private/` for unreviewed local output. Keep frozen published captures immutable. Publish minimal reviewed, sanitized observations with source revision, command, environment, UTC retrieval/execution date, source publication/revision date, exact URL and claim-level provenance. Separate source reports, local observations, corroboration, inference and unknowns. Hashes prove byte identity, not authenticity. Avoid stable private identifiers in published summaries.

Retain published source, fixtures, reports and release evidence through Git history. Keep local scratch until the reviewer accepts the sanitized report and reproducibility requirements; deletion requires explicit owner approval and excludes canonical/frozen evidence. Do not promise indefinite retention of private raw data or upload it automatically.

## Tags and release notes

Only tag a reviewed merged revision after release approval. Use immutable annotated `vMAJOR.MINOR.PATCH` tags for coherent tooling releases, with patch for compatible fixes, minor for compatible additions and major for incompatible contracts. Use `experiment-<id>-baseline-<date>` for separately approved frozen research baselines; research tags do not imply product readiness. Record full commit SHA, tag intent and evidence index; sign if signing is configured, and state when unsigned. Never move/reuse a published tag or rewrite prior results; correct through a new commit/tag.

Release notes must list changes and PRs, behavior/contracts affected, exact validation and expected failures, preserved evidence identities, dependency/runtime/model compatibility, migration/rollback steps and unresolved limits. Distinguish an executed experiment from a launcher utility or research proposal. No release/tag is created automatically by this policy.

## Safe merged-branch cleanup

Cleanup is a separate explicitly approved action. Fetch without pruning first; inventory local/remote refs and worktrees. Confirm PR merged, exact branch tip reachable from current main (`git merge-base --is-ancestor <tip> origin/main`), no unique commits (`git log origin/main..<branch>`), no active dependency/review/worktree and no dirty work. Squash/rebase merges need a separate patch-equivalence/history review; PR state alone is insufficient. Record the full tip in retained release/audit evidence or an approved archival ref before removal.

After approval, use `git branch -d <branch>` locally and an explicitly named normal remote deletion only for the reviewed ref. Never use bulk deletion, `-D`, force pushes, branch-name guesses or pruning as a substitute for inspection. Local stale main may be fast-forwarded only when clean and after inspecting its own work. No branch is deleted by this audit.
