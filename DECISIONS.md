# Decision record

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
