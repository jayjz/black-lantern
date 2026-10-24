# Black Lantern

A canonical cybersecurity research laboratory for understanding how software and agent-enabled systems fail, which controls prevent those failures, and which engineering capabilities make those controls dependable.

This repository holds evidence, bounded assessments, and reproducible experiment designs. It is not a startup or product roadmap.

## Research 01

**Disclosure window:** July 1 through October 23, 2026, inclusive. **Status:** source review and design complete; independent engineering review pending. No exploit tests were run.

Start with the [evidence ledger](research/incidents/01-evidence-ledger.md), then the [technical synthesis](research/incidents/01-synthesis.md). The three selected cases are:

- [PHP out-of-memory corruption](research/incidents/01-php-oom.md): a vulnerability with demonstrated exploitation in a research setting.
- [Reasonix configuration-driven execution](research/incidents/01-reasonix.md): a disclosed vulnerability in developer tooling.
- [OpenAI / Hugging Face evaluation containment incident](research/incidents/01-openai-hugging-face.md): a documented real intrusion, with independent investigation of part of the activity.

The [source index](research/sources/index.md) preserves URLs, dates, verification status, rejected leads, and source conflicts. The [competency assessment](assessments/competency-gap.md) separates observed artifacts from untested capability. The [first experiment proposal](experiments/01-transitive-tool-authorization.md) is design only.

## Repository map

The [agent intrusion containment design](experiments/agent-intrusion-containment/README.md) compares a passive defensive message with independent authorization and containment. It is design only; proposed regressions have not run.

| Location | Canonical purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Research and execution rules |
| [GOALS.md](GOALS.md) | Laboratory objectives and exclusions |
| [PLANS.md](PLANS.md) | Phases, acceptance criteria, and next work |
| [DECISIONS.md](DECISIONS.md) | Dated decisions and their evidence |
| `research/incidents/` | Claim ledger, focused reports, comparative analysis |
| `research/sources/` | Source provenance and verification status |
| `research/market/` | Reserved for evidence about security practice and tooling; no market study commissioned |
| `assessments/` | Capability assessments with evidence limits |
| `experiments/` | Bounded experiment proposals; later authorized results |
| [evidence/verification.md](evidence/verification.md) | This session's executed checks and limitations |

Source statements are attributed reports, not locally reproduced facts. Dates on live pages do not establish immutable historical versions. See the source index before relying on an as-of-date claim.
