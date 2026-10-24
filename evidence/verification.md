# Research 01 verification record

Session date: 2026-10-23 America/New_York; retrieval crossed into 2026-10-24 UTC. This records actual observations and separates them from proposed experiment tests.

## Workspace inspection

Executed `Get-Location`, `Get-ChildItem -Force`, `git status -sb`, `git remote -v`, and `git log -5 --oneline` before writing files. Observed `C:\Dev\black-lantern`, only `.git`, unborn branch `main`, and fetch/push origin `https://github.com/jayjz/black-lantern.git`. Git log reported that the branch had no commits; this was the expected absence of history, not a lost-history event. No branch, remote or Git configuration was changed.

## Source and claim checks actually performed

- Opened primary advisory/incident pages and inspected their relevant passages; retrieved the three named PHP/Reasonix CNA records through the GitHub connector. Exact dates, URLs and retrieval limitations are in the [source index](../research/sources/index.md).
- Compared PHP's announcement, OOM advisory and CNA metadata; separated successful research exploitation from F5 traffic observations and from hypothetical impact.
- Compared Reasonix researcher, maintainer and CNA statements; preserved date, severity and CVE-field inconsistencies.
- Compared OpenAI's initial/later disclosures with Hugging Face's original/technical accounts and METR's bounded independent investigation. No conclusion claims METR verified all affected-party data scope or remediation.
- Checked the latest in-window PHP and OpenAI updates. Excluded the current October 24 Vercel Node.js body from cutoff findings and used the October 21 Node.js original for that lead.
- Read and manually reviewed the three report narratives against the ledger. Confirmed exactly three focused cases. No exploit chain was invented to fill an evidence gap.

No raw page archive, publisher-signature validation or complete patch review was performed. URLs identify live evidence, not immutable copies. No unavailable source was treated as verified.

## Local evidence identities

Read-only sample; no source copied into this repository. SHA-256 identifies the observed file bytes, not authorship, correctness or proficiency.

| Local path | Scope read | SHA-256 |
| --- | --- | --- |
| `C:\Dev\automated_social\archive_intelligence\evidence_policy.py` | First 165 lines requested (returned module) | `D19BA174D4EC798A6024FC87DA93C80910E4191EA5CAA138FC79E3DDC5D7C646` |
| `C:\Dev\automated_social\tests\test_evidence_policy.py` | First 180 lines requested | `4ECD5E5348755910BEA3838A0020337B251C0B80728B5BEAD7EBB469AE1BF818` |
| `C:\Dev\automated_social\AGENTS.md` | First 130 lines requested | `A438474534AA46164B0E06A71075493970645D498480367DA28F9F33B970DD5D` |
| `C:\Dev\hvac-invoice-gatekeeper\AGENTS.md` | First 100 lines requested | `997CE3BD5937DF93F89C215DE8A8B34B5355F18AD207A5B5F427403AC5517E1C` |
| `C:\Dev\hvac-invoice-gatekeeper\README.md` | First 100 lines requested | `8A144BF572BB87D08EEBD7DD92C4A32FB15EEA54F76782195401A814C106B00C` |

Executed file inventory and `Get-FileHash -Algorithm SHA256`. Attempts to run `git -C <project> rev-parse HEAD` and `git -C <project> status --short` on these two projects failed with dubious-ownership protection. No global or per-command safe-directory override was applied. Thus file observations are working-copy evidence without verified commit provenance. `leadgen` received filename inventory only; no capability conclusion relies on it.

## Repository checks

Final results are recorded below after execution. The checks are read-only and require no dependency installation.

- Enumerate candidate files with `rg --files --hidden -g '!.git'`.
- Resolve every Markdown relative link against its containing directory. Check fragment IDs against explicit HTML anchors and normalized Markdown headings. Ignore HTTP(S) links in the local-link check; source access is recorded separately.
- Check required directories and top-level files, exactly three focused reports, and external citation URL membership in the source index.
- Inspect files for credential-like token patterns, private-key headers, private IP addresses, NUL bytes, trailing whitespace and final newlines. This is a limited pattern/manual review, not a comprehensive secret scanner.
- Execute `git diff --check` and `git -c core.autocrlf=false diff --no-index --check -- NUL <file>` for every untracked file. The latter matters because ordinary `git diff` omits untracked content. The command-local line-ending override suppresses conversion warnings; it does not write Git configuration. Exit 1 without diagnostics means files differ under no-index, not a whitespace failure; inspect diagnostics and reject errors above exit 1.
- Confirm `git status -sb` and `git diff --cached --name-only`: no commits, no staged files, only the intended foundation/research files untracked.

## Safety and experiment review

Manual review confirms a design-only, deterministic simulation with synthetic identifiers, no real endpoint, no exploit payload, no exposed shell or networking tool, an outer disconnected VM requirement, independent effect checks and explicit stop conditions. The proposal separates logical authorization tests from unproven OS/network isolation. These are design checks, not execution results.

No dependencies installed; no tests in other projects run; no networks scanned; no exploit code run; no VM launched; no third-party system tested; no credentials used; no unrelated files or security settings modified; no repository created; no commit, staging or push performed. Public-source retrieval used read-only web/GitHub requests.

## Final check outcome

Passed: required structure; 16 candidate files (14 Markdown documents, `.gitignore`, and the market-directory placeholder); exactly three focused reports; 68 local links and fragments resolved; all 27 unique external citation URLs represented in the source index. A read-only PowerShell/.NET regex check found no NUL bytes, trailing whitespace or missing final newlines.

The limited sensitive-content check found no private-key headers, GitHub token formats, AWS access-key IDs, JWT-shaped tokens or private IPv4 addresses. Manual review found no copied credentials, personal datasets or runnable exploit payloads. This is not a guarantee against every secret format.

`git diff --check` produced no diagnostics. Per-file no-index checks covered all 16 candidate files and produced no whitespace diagnostics. An initial wrapper incorrectly treated no-index exit 1 as failure and displayed LF-to-CRLF warnings; the corrected diagnostic-aware check passed without changing files or persistent configuration. `git check-ignore --no-index` confirmed coverage for `.env`, raw/private evidence, PEM files and virtual-environment files.

Final Git state: unborn `main`; expected origin unchanged; all 16 intended files untracked; index empty. No test suite or experiment was executed. The substantive checks above are document/source validation, not vulnerability validation. Remaining limitations are source-version uncertainty, untested patches, bounded forensic corroboration and unverified operator capability.
