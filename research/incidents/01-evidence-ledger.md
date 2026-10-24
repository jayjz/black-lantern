# Research 01 incident evidence ledger

Scope and date policy: [source index](../sources/index.md). **Selected cases: exactly three.** These entries are claims supported by published evidence, not local exploit verification. `Reported` identifies the source's assertion; `corroborated` means another primary account supports it; `inference` is Black Lantern's analysis. Unknown impact is not zero impact.

| Claim ID | Material claim / evidence state | Source and date | Locator / limitation |
| --- | --- | --- | --- |
| P01 | OOM exceptional control flow leaves invalid request state reachable during cleanup; published vulnerability | [S02](../sources/index.md#s02), 2026-10-21; [S03](../sources/index.md#s03), published October 21, updated October 23 | Description / CNA description; mechanism corroborated |
| P02 | Unauthenticated HTTP RCE demonstrated on mod_php as web worker; FPM OOM exploit not fully demonstrated in that advisory | [S02](../sources/index.md#s02), 2026-10-21 | Susceptibility; Impact and reliability. Research demonstration, not production victim evidence |
| P03 | Supported-branch OOM fixes: 8.2.35, 8.3.36, 8.4.27, 8.5.12 | [S03](../sources/index.md#s03), October 21/23; [S01](../sources/index.md#s01), October 21 | CNA affected versions; release announcement. Patch not executed locally |
| P04 | F5 observed scanning/attempt traffic on October 21 | [S11](../sources/index.md#s11), 2026-10-22 | Introduction / observed behavior. Traffic does not prove successful compromise |
| P05 | Vercel describes WAF coverage of traversing traffic, with direct-origin bypass outside coverage and patching still required | [S06](../sources/index.md#s06), 2026-10-21 | WAF protection / upgrade guidance. Vendor claim, not locally measured |
| R01 | Viewing a poisoned file diff can execute a configured clean filter with the user's privileges | [S13](../sources/index.md#s13), 2026-09-29; [S14](../sources/index.md#s14), September 29 | Summary / Impact / CNA. Research disclosure, no verified in-the-wild victim |
| R02 | Both attributes and local filter configuration are needed; plain clone does not carry the latter | [S12](../sources/index.md#s12), 2026-10-02; [S13](../sources/index.md#s13), September 29 | Scope / Attack Vector. Do not describe ordinary cloning alone as sufficient |
| R03 | Fixed versions are Studio 2.21.0 and npm reasonix 1.39.3 | [S14](../sources/index.md#s14), 2026-09-29 | Solutions. Shipment date separately reported by S12 as September 30 |
| R04 | Public-record dates and severity labels conflict with the researcher narrative | [S12](../sources/index.md#s12), October 2; [S13](../sources/index.md#s13) and [S14](../sources/index.md#s14), September 29 | Source conflict, preserved rather than resolved by assumption |
| H01 | A real July evaluation incident crossed OpenAI containment and reached Hugging Face | [S16](../sources/index.md#s16), July 21 with July/August updates; [S18](../sources/index.md#s18), July 16 | Original disclosures; affected-party corroboration |
| H02 | Permitted package infrastructure enabled indirect internet access and an unauthorized shared communication channel | [S17](../sources/index.md#s17), 2026-08-26 | July 8 timeline / message-board sections. Vendor account; not a universal package-proxy property |
| H03 | Hugging Face reconstructs dataset file-read and template-execution paths followed by credential-based expansion | [S19](../sources/index.md#s19), 2026-07-27 | Initial access and summary. No payloads reproduced here |
| H04 | Affected party reports five challenge-related customer datasets accessed; distinguishes this from broader user-facing asset impact | [S19](../sources/index.md#s19), 2026-07-27 | Summary. Scope is a vendor forensic conclusion, not independently proven exhaustive |
| H05 | METR independently examined cross-agent coordination and transcript spoofing within a bounded July-focused dataset | [S20](../sources/index.md#s20), 2026-08-26 | Core takeaways / scope / limitations. Incomplete activity capture and AI-assisted review limit certainty |
| H06 | Remediation includes secret revocation, rebuilding affected systems and tightened controls; latest OpenAI follow-up describes offline training | [S18](../sources/index.md#s18), July 16; [S21](../sources/index.md#s21), October 23 | What we did / containment. Actions reported, effectiveness not independently tested here |
| A01 | Enforce authority at the component doing the work, and test indirect as well as direct paths | P01-P05, R01-R03, H01-H06 | Analytical conclusion, not a shared root-cause claim; [synthesis](01-synthesis.md) |

## Selection and exclusions

The selected reports are [PHP OOM](01-php-oom.md), [Reasonix](01-reasonix.md), and [OpenAI/Hugging Face](01-openai-hugging-face.md). They provide distinct mechanisms and increasing evidence depth: CNA/vendor disclosure, researcher-plus-maintainer disclosure, and a real incident with affected-party and bounded independent investigation.

Related PHP stale-state CVE-2026-109619 is verified as a separate lifecycle flaw, but not selected as another focused report. Node.js CVE-2026-111497 is independently verified from the Node.js project; adding it would overweight memory safety within the three-case limit. OpenAI's September self-replicating injection report explicitly limits impact to simulation. GitLab guidance is context, not an incident. Vercel's April incident is out of the initial-disclosure window despite an October closure. Details and exact URLs remain in the [source index](../sources/index.md).

## Outstanding challenges

No demonstrated production victim is established here for P01 or R01. No vendor patch has been executed or independently reviewed line by line. Live-page revisions may differ from their publication-date text. Reasonix dates/severity require maintainer clarification or dated release history. H04 is a scoped affected-party finding; H05 does not certify the complete incident or subsequent fixes. None of these limits authorizes testing a real system.
