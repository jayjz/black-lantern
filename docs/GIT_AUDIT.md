# Git and planning audit — 2026-10-24

Local observations after `git fetch origin` (exit 0); retrieval/review date 2026-10-24. Repository [jayjz/black-lantern](https://github.com/jayjz/black-lantern). Initial worktree clean on Experiment 03 head `a3e0dc0`; one worktree. Local main `3effa4d` is 10 commits behind `origin/main` `315ff71b56f625320e1f286041d5b42cfbd85166`. No local-only commits found. No local or remote tags. Fetch did not prune. `git ls-remote --heads --tags origin` independently matched all nine remote branch tips below. No branch/history was deleted, merged, reset, force-pushed or rewritten.

## Branch inventory before this feature branch

Abbreviations below resolve uniquely in the 24-commit inventory. All remote heads were explicitly checked for ancestry to origin/main.

| Remote branch | Tip | Local counterpart | In main? |
| --- | --- | --- | --- |
| main | 315ff71 | main at 3effa4d | yes |
| experiment/agent-intrusion-containment | 106e621 | same tip | yes |
| feature/experiment-01-authorization-boundary | 5121161 | same tip | yes, through PR #2 |
| feature/experiment-02-complete-mediation | cf114ae | same tip | yes |
| docs/public-repository-audit-2026-10-24 | f65a2bb | none | yes |
| docs/agentic-security-public-readme | 2f22cbf | none | yes |
| feature/experiment-03-model-tool-authorization | a3e0dc0 | same tip | no |
| docs/phase-04-validation-roadmap | 3544df4 | none | no |
| docs/next-phase-dolphin-roadmap | b961acd | none | no |

The dedicated `feature/version-control-llama-audit` branch starts at current origin/main, without importing PR #5 code/evidence. Existing refs and ignored/untracked work were preserved. Clean checkout switching removes tracked Experiment 03 files from this branch's working tree; their committed bytes remain on its unchanged local/remote branch.

## Complete reachable commit inventory at inspection

`git rev-list --all --count` = 24. All commits are dated 2026-10-23 or 2026-10-24, local offset -04:00. Ordered by lineage/group for readability; `git log --all --format='%H %cI %s'` reproduces exact identities/dates.

| Revision | Commit subject |
| --- | --- |
| 3effa4d | research: establish Black Lantern foundation and incident analysis |
| 106e621 | research: design agent intrusion containment experiment |
| 8502afe | Merge pull request #1 from jayjz/experiment/agent-intrusion-containment |
| 5121161 | experiment: verify final-action authorization with relay counterexample |
| 1b1c7f4 | Merge remote-tracking branch origin/main into feature/experiment-02-complete-mediation |
| cf114ae | test(security): challenge complete mediation with bypass regression |
| 9b72d94 | Merge pull request #2: adversarial complete-mediation review |
| f65a2bb | docs: audit published Black Lantern evidence and experiment status |
| 06375f5 | Merge pull request #3 from jayjz/docs/public-repository-audit-2026-10-24 |
| 2f22cbf | docs: present Black Lantern as agentic AI security research lab |
| 315ff71 | Merge pull request #4 from jayjz/docs/agentic-security-public-readme |
| f7c940c | experiment: evaluate local model tool authorization and measurement integrity |
| a3e0dc0 | fix: fail closed on incomplete Experiment 03 evidence |
| c268a47 | docs: define gated Phase 04 independent verification and Dolphin evaluation |
| 536fd8c | docs: link prospective Phase 04 gates in README.md |
| c94be2e | docs: link prospective Phase 04 gates in GOALS.md |
| 7fac5e2 | docs: link prospective Phase 04 gates in PLANS.md |
| 32c9ad5 | docs: link prospective Phase 04 gates in DECISIONS.md |
| 3544df4 | docs: link Experiment 03 sources on unmerged PR branch |
| e2e331d | docs: define gated next phase for Dolphin and commercialization research |
| fa65595 | docs: align README.md with next-phase gated roadmap |
| ff3c5f4 | docs: align GOALS.md with next-phase gated roadmap |
| 0433cce | docs: align PLANS.md with next-phase gated roadmap |
| b961acd | docs: align DECISIONS.md with next-phase gated roadmap |

## PR inventory and dependencies

GitHub connector inspection of all seven owner PRs (state=all, limit=100) agreed with local ancestry. A direct public [REST inventory](https://api.github.com/repos/jayjz/black-lantern/pulls?state=all&per_page=100) independently returned exactly the same seven PRs, with no pagination link, covering other authors as well. All target main. Original publication/last revision dates below are GitHub metadata, retrieved 2026-10-24. PR bodies describe source-reported tests, not execution by this audit.

| PR | Published / last updated (UTC, 2026-10-24) | Observed state | Scope |
| --- | --- | --- | --- |
| [#1](https://github.com/jayjz/black-lantern/pull/1) | 03:41:08 / 03:41:19 | merged | containment design |
| [#2](https://github.com/jayjz/black-lantern/pull/2) | 04:04:23 / 04:07:02 | merged | Experiment 01 plus Review 02 |
| [#3](https://github.com/jayjz/black-lantern/pull/3) | 04:53:09 / 04:53:38 | merged | public evidence audit |
| [#4](https://github.com/jayjz/black-lantern/pull/4) | 04:55:29 / 12:57:05 | merged | public README |
| [#5](https://github.com/jayjz/black-lantern/pull/5) | 13:34:44 / 14:54:01 | open | Experiment 03 and verifier hardening |
| [#6](https://github.com/jayjz/black-lantern/pull/6) | 19:06:33 / 19:06:33 | open | Phase 04 plan |
| [#7](https://github.com/jayjz/black-lantern/pull/7) | 19:06:50 / 19:06:50 | open | duplicate next-phase plan |

Metadata reports no reviews or review threads for #5–#7. Absence of threads is not approval. All three modify README, GOALS, PLANS and DECISIONS. #6 and #7 append parallel future sections and each uses decision ID D11. They can be textually mergeable yet leave two competing sources of truth. #5 adds D09/D10 and historical evidence gates; it is not a duplicate roadmap and must receive separate review. Both roadmap branches fork from 315ff71 and contain none of #5's two commits. Their references to Experiment 03 therefore require a pinned unmerged source or a separately reviewed merge.

Exact plan inputs, revised/retrieved 2026-10-24: [#6 plan at 3544df42de47f17fa94de6a275d3c2dcc2453ddc](https://github.com/jayjz/black-lantern/blob/3544df42de47f17fa94de6a275d3c2dcc2453ddc/roadmap/PHASE-04.md), [#7 plan at b961acd8169e5db4d60c6132beadea2b6fa12657](https://github.com/jayjz/black-lantern/blob/b961acd8169e5db4d60c6132beadea2b6fa12657/roadmap/next-phase-agent-security.md), [#5 hardening at a3e0dc07a39d39ab4a2c55152bcbebe66a381b23](https://github.com/jayjz/black-lantern/blob/a3e0dc07a39d39ab4a2c55152bcbebe66a381b23/experiments/model-tool-authorization/HARDENING.md).

Recommendation: review this reconciliation as the replacement for the planning content of #6/#7; after human acceptance, explicitly close those duplicate PRs as superseded without merging their parallel sections. Retain their branches until separately approved cleanup. Review #5 separately; whichever PR merges second must reconcile the four root documents against fresh main. Do not cherry-pick all roadmap commits or merge all three indiscriminately. The canonical plan retains #6's gate identifiers and #7's independence/provenance/demand details; the alternate filename is a pointer. Interview/pilot work remains prospective. This is a recommendation, not a performed closure or merge.

## Commands and limits

Executed: status/remote inspection; `git fetch origin`; `git branch -avv`; `git tag -n`; `git log --all --oneline --decorate --graph`; full log/date inventory; `git rev-list --all --count`; `git ls-tree` on main and plan branches; `git show` both plans; three-dot diffs and stats; `git branch -r --no-merged origin/main`; `git for-each-ref`; `git worktree list`; `git ls-remote --heads --tags origin`. All successful after sandbox escalation where required. `gh` was unavailable; GitHub connector supplied PR metadata and reviews. Sandbox denied the first branch switch and direct remote HTTP/ref reads; approved reruns succeeded. No ownership/protection settings were changed. Full GitHub control/ruleset audit and independent review are not claimed; merging is intentionally outside this task.
