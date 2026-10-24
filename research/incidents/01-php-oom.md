# Case 1 — PHP out-of-memory corruption

**CVE-2026-109618 / GHSA-w8hw-w9fx-j79w.** Classification: vulnerability with demonstrated research exploitation; production compromise not established in this review. Claim IDs P01-P05 in the [ledger](01-evidence-ledger.md).

## Event, boundary and prerequisites

PHP disclosed the issue on October 21. OOM handling uses an abrupt control-flow exit that can expose partially initialized request state to cleanup. An unauthenticated attacker needs HTTP reachability and a request that reaches the vulnerable allocation/cleanup path. PHP reports RCE on mod_php before application code, with execution as the web-worker account. Its advisory distinguishes FPM: startup failure kills the child; application-stage susceptibility remains, but that advisory does not demonstrate a complete OOM FPM exploit. [PHP advisory, published 2026-10-21](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w).

The PHP CNA records CVSS 4.0 9.2, no prior privileges or user interaction, and fixes for the supported branches at 8.2.35, 8.3.36, 8.4.27 and 8.5.12. These are runtime fixes, not application authentication changes. [CNA record, published 2026-10-21; updated 2026-10-23](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/109xxx/CVE-2026-109618.json).

## Impact and controls

The verified published impact is a successful research RCE demonstration. F5 separately reports October 21 scanning and exploit attempts in its sensor network; those observations establish hostile traffic, not successful execution on production victims. [F5, 2026-10-22](https://www.f5.com/labs/articles/php2shell-exploitation-attempts-observed).

PHP describes replacing unsafe OOM exits with safe-point handling and process termination at a higher threshold. Updating is the complete mitigation for this flaw; configuration workarounds are incomplete. [PHP advisory, 2026-10-21](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w).

Vercel's WAF statement covers requests through its network, including proxied PHP backends, but excludes direct-origin traffic and does not replace runtime patching. It also recommends verifying the runtime actually serving requests. [Vercel PHP bulletin, 2026-10-21](https://vercel.com/kb/bulletin/php2shell-security-bulletin).

## Unknowns and lesson

Black Lantern did not reproduce RCE, inspect deployed builds, validate the patch, or measure WAF efficacy. Exploit portability and FPM reachability cannot be assumed from the mod_php demonstration. Related CVE-2026-109619 concerns stale state across requests, not the identical OOM failure. PHP's October 23 session-upload-progress follow-up also prevents a blanket claim that the October 21 releases remove every PHP RCE condition. [PHP dated announcements, 2026-10-21 and 2026-10-23](https://www.php.net/archive/2026.php).

**Engineering inference:** allocation failure is a security path. Specify which state is valid at every failure exit, test cleanup after interrupted initialization, and confirm that patch deployment replaces all serving workers. Authentication in application code cannot protect parsing that executes earlier. Suggested detection is correlation of worker crashes/OOM events, request volume and deployment identity; no single log signature proves this exploit.
