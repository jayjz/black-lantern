# Black Lantern

**Agentic AI security research, tooling, and reproducible testing.**

Black Lantern is a public research laboratory examining how AI agents, developer tools, and the systems connecting them cross trust boundaries. The goal is to turn security claims into narrow, testable hypotheses—and publish enough code, fixtures, observed effects, and limitations for another engineer to challenge the results.

**Core question:** When an AI agent requests an action, what actually determines whether that action is allowed—and how do we know the control held?

## What we investigate

- **Agent/tool authorization:** Identity binding, delegation, transitive tool access, and authorization at the final resource effect.
- **Prompt injection and untrusted inputs:** Whether lower-trust content changes an agent's proposed actions; whether enforcement still prevents unauthorized effects.
- **Evaluation integrity:** Whether an oracle detects unexpected execution paths, missing observations, and intentionally broken controls.
- **Containment and evidence:** Separating model output, attempted tool calls, authorization decisions, and resource-side effects.
- **Failure analysis:** Learning from disclosed vulnerabilities and AI-system incidents without treating reported claims as locally reproduced results.

## How the lab works

```text
Source / hypothesis
        |
        v
Frozen synthetic fixtures + threat boundary
        |
        v
Scripted actor or local-model tool proposal
        |
        v
Schema validation -> harness-bound identity -> authorization at effect
        |
        v
Protected synthetic state + observer
        |
        v
Independent expectations, mutation test, reproducible evidence
```

Models may **propose** tool calls. They do not receive authority to execute those calls directly. We measure *attempt*, *authorization decision*, and *actual effect* separately. A model's refusal, a green test suite, or a generated explanation is not by itself a security result.

## Current work

| Area | Published state | Start here |
| --- | --- | --- |
| **Experiment 01 — Authorization boundary** | Executed, synthetic Python model; direct and relay authorization with a deliberately broken guard | [Source, cases, report, and evidence](experiments/authorization-boundary/README.md) |
| **Adversarial Review 02 — Complete-mediation coverage** | Executed, synthetic counterexample: a new unchecked route escapes the old tests; added regression detects it | [Review and exact evidence](experiments/complete-mediation/README.md) |
| **Agent intrusion containment** | Design only; proposed comparison of passive messaging, authorization, and independent containment | [Threat model and test plan](experiments/agent-intrusion-containment/README.md) |
| **Research 01 — Failure mechanisms** | Source review of three public disclosures; not locally exploited or reproduced | [Evidence ledger](research/incidents/01-evidence-ledger.md) |
| **Experiment 03 — Local-model tool evaluation** | Published on open PR #5; unmerged at this audit | [Pinned report](https://github.com/jayjz/black-lantern/blob/a3e0dc07a39d39ab4a2c55152bcbebe66a381b23/experiments/model-tool-authorization/README.md) |

### A concrete finding

Experiment 02 introduced a **disposable, actor-reachable** `inspect` route that returned a synthetic protected value without the final authorization check. The **unchanged** Experiment 01 suite still reported 96/96 expected episodes. With new coverage, the deliberately defective route triggered six failing episodes; after repair, all 105 expected outcomes were met, including six explicitly incomplete observer diagnostics—not security passes.

This is a demonstration of an **interface-coverage blind spot in synthetic tests**, not evidence that the original implementation contained that route, nor proof of production agent containment. [Read the full result](experiments/complete-mediation/README.md).

## Run the published synthetic tests

Requires Python 3.11+; no additional Python packages for these experiment drivers. From repository root:

```sh
python -I -S experiments/authorization-boundary/prove_regression.py --output evidence-review-01.json
python -I -S experiments/complete-mediation/review.py --output-dir evidence-review-02
```

These are documented reproduction commands, **not tests executed by this README edit**. Use a disposable output directory or scratch paths; inspect each report's expected child-process failures to distinguish a *detected defect* from a passing security control. The local-model experiment is not part of this reproduction path until published and verified.

## Evidence standard

Every published experiment should identify:

1. The exact hypothesis, actor capabilities, trust boundary, and excluded capabilities.
2. Source and fixture identities, model/runtime identity where relevant, and reproduction commands.
3. Raw or sanitized proposed actions, independent authorization decisions, and actual synthetic resource effects.
4. What an intentionally defective control changes and whether the oracle notices it.
5. Negative, inconclusive, incomplete-observer, and unverifiable outcomes without relabeling them as passes.

**Boundaries:** This is not a production security product, an exploitation service, or a certification of arbitrary Python, OS, network, or MCP isolation. Synthetic resources and explicitly authorized tests only. No real credentials, third-party targeting, or uncontrolled execution. Reported events are cited evidence, not proof of local reproduction.

## Explore the repository

- [Goals and exclusions](GOALS.md) · [Experiment acceptance gates](PLANS.md) · [Engineering decisions](DECISIONS.md)
- [Research sources](research/sources/index.md) · [Verification record](evidence/verification.md)
- [Public documentation audit](assessments/public-repository-audit-2026-10-24.md)
- [Working rules](AGENTS.md)

**Direction:** Develop small, inspectable security research tools and tests for agentic systems, with enforcement outside the model and evidence strong enough to falsify our own assumptions.

## Repository and local runtime

[Canonical Phase 04 plan](roadmap/PHASE-04.md) · [Version control policy](docs/VERSION_CONTROL.md) · [Git/PR reconciliation](docs/GIT_AUDIT.md) · [Local llama.cpp audit and launcher](docs/LLAMA_RUNTIME_AUDIT.md).

Phase 04 research remains prospective. The local runtime audit measures bounded synthetic completion throughput without host tools; it does not rerun Experiment 03 or establish a model-security result.
