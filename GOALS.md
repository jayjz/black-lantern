# Laboratory goals

1. Explain failure mechanisms at concrete boundaries: memory lifetime, identity, configuration, network access, dependencies, and agent/tool execution.
2. Distinguish controls that prevent a path from controls that merely reduce exposure or improve detection.
3. Produce compact, source-linked assessments another engineer can reproduce, challenge, and correct.
4. Develop demonstrated security-engineering capability through isolated experiments and independent evidence.

Research 01 is the initial bounded baseline, not an exhaustive incident census. Its source window and deliverables are defined in [PLANS.md](PLANS.md).

Excluded: startup validation, product development, live exploitation, unsolicited scanning, third-party testing, credential use, deployment, and publication. Implementation of experiment proposals requires a subsequent scoped task.

## Agent intrusion containment experiment

Design an isolated, reproducible comparison of a passive defensive message, deterministic authorization, and independent containment/remediation. Challenge the assumption that an unauthorized agent can be made safe by asking it to stop and repair its entry path. Establish observable boundaries without giving the actor host repair authority. [Design package](experiments/agent-intrusion-containment/README.md).

The 2026-10-23 task authorizes design documents and their commit/push to a feature branch on `jayjz/black-lantern`, overriding the earlier publication exclusion only for this package and its canonical-document updates. It does not authorize implementing or executing the experiment.

## Experiment 01: final-action authorization

The subsequent Experiment 01 task authorizes implementing, executing and publishing only a synthetic offline Python authorization model on a separate feature branch. Establish one falsifiable result for direct/delegated access; include a deliberately broken local control, independent effect observations, findings and a TLDR. No broader containment study or infrastructure work. [Scope and audit](experiments/authorization-boundary/README.md).

## Adversarial Review 02: complete mediation

Challenge Experiment 01's interface-coverage assumption using one temporary read-only entry point; preserve the original implementation and evidence. Compare the unchanged suite with a minimal new regression, repair the new entry point, and publish the bounded finding through the requested GitHub workflow. [Review](experiments/complete-mediation/README.md).

## Next phase: agentic AI security evaluation and commercial discovery (2026-10-24)

Prospective mission: develop reproducible, effect-based security tests for tool-using AI agents, and determine whether a narrowly defined customer pays for credible staging-workflow authorization assessments. Four prioritized goals: independently reproduce Experiment 03; compare a provenance-checked Dolphin candidate with the existing model under frozen synthetic controls; obtain qualified external engineering criticism; interview actual owners of agent-authorization problems and test a consent-based pilot hypothesis. [Gated roadmap](roadmap/next-phase-agent-security.md).

**Scope update:** The initial Research 01 exclusion of startup validation was specific to that earlier commissioned work and remains part of its historical record. This subsequent phase now authorizes *planning and consent-based customer discovery*, not product implementation, claims of certified expertise, or real-world testing. All existing prohibitions on unauthorized access, uncontrolled execution and publishing secrets remain in force.
