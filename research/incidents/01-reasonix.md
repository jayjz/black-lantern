# Case 2 — Reasonix repository configuration becomes execution

**CVE-2026-102437 / GHSA-grg2-7gc6-36m6.** Classification: disclosed command-execution vulnerability in developer tooling; no production breach established. Claim IDs R01-R04 in the [ledger](01-evidence-ledger.md).

## Event, boundary and prerequisites

GitLab's October 2 research describes a diff viewer invoking Git with several hardening flags while leaving content filters active. A per-file attribute selects a clean filter defined in local repository configuration. Viewing a changed file's diff can therefore execute the filter command. The boundary is untrusted repository metadata becoming executable tool configuration. [Original research, 2026-10-02](https://about.gitlab.com/blog/deepseek-reasonix-vulnerability-discovered/).

The maintainer confirms execution with the privileges of the user running Reasonix. Both `.gitattributes` and a malicious local `.git/config` are required. An archive, shared folder, cache or image can preserve both; a normal clone transfers attributes but not the local configuration. Existing filesystem write access could also supply configuration, but that is an additional prerequisite, not an exploit step demonstrated here. [Maintainer advisory, published 2026-09-29](https://github.com/esengine/DeepSeek-Reasonix/security/advisories/GHSA-grg2-7gc6-36m6), [research scope, 2026-10-02](https://about.gitlab.com/blog/deepseek-reasonix-vulnerability-discovered/).

## Impact, remediation and chronology

The CNA identifies local attack vector and required user interaction, with CVSS 3.1 7.8 High. Affected Studio versions are below 2.21.0 and npm `reasonix` below 1.39.3; those versions are listed as fixes. [GitLab CNA, published/updated 2026-09-29](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/102xxx/CVE-2026-102437.json).

The GHSA is labeled Critical and published September 29; GitLab's narrative places publication, CVE assignment and fix shipment on September 30. The public CNA timestamp supports September 29 for the record; fix shipment date remains researcher-reported. Neither label establishes a victim count. [Date and severity conflict](../sources/index.md#conflicts-and-unavailable-evidence).

The maintainer suggests removing filter invocation from byte-diff rendering or explicitly controlling permitted drivers. A flag that disables external diffs does not disable clean filters. [Maintainer remediation, 2026-09-29](https://github.com/esengine/DeepSeek-Reasonix/security/advisories/GHSA-grg2-7gc6-36m6).

## Unknowns and lesson

Published evidence includes researcher command execution and maintainer acknowledgement; this review did not run the demonstration, inspect the complete patch, or independently confirm fix efficacy. In-the-wild exploitation and affected-user counts remain unverified. This is not a breach of GitLab's hosted service.

**Engineering inference:** a read-oriented UI action can have execution side effects in its dependencies. Model the entire call chain and treat project configuration as untrusted input. Test hostile configuration with a harmless local sentinel only in an authorized disposable environment. Process-tree telemetry around diff rendering could detect unexpected filter children. This flaw requires no LLM persuasion; it is conventional command execution in agent-adjacent tooling.
