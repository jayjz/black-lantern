# Engineering verification report: Experiment 01

Execution date: 2026-10-23. Evidence class: **local synthetic observations**. No external vulnerability reproduction, confirmed compromise or independent engineering review is asserted. [TLDR](TLDR.md), [audit, boundary and reproduction](README.md).

## Property and implementation

Tested property: for these harness-bound callers and requests, unauthorized direct or delegated resource actions produce zero dispatches, protected disclosures and mutations; authorized actions retain their exact expected effects. I1-I5 and the independent acceptance rule were defined before execution in [PLANS.md](../../PLANS.md#experiment-01-execution-gate-subsequent-task) and [cases.json](cases.json).

The final check lives in `Resource.perform` in [model.py](model.py). Both direct and relay routes converge there with the harness principal. Only canonical `vault-1` reaches that site; the allowlisted alias is canonicalized first, while other spellings are rejected. Exact request schemas reject forged identity/role/capability claims. Request replay state is principal-scoped, with no response cache. The single resource contains only `SYNTHETIC-DATA-001`, initially version 0; the only accepted write value is `SYNTHETIC-WRITE-001`.

[oracle.py](oracle.py) builds expected service records from the static matrix, never the policy implementation. It compares the response, independent service record, mediator record and resource snapshot separately. A denied read cannot be justified by an unchanged snapshot alone. The runner checks evidence after each operation and halts a divergent scenario before its next call. Subsequent scenarios have fresh state and are diagnostic only; a failure remains a failed run.

## Actual test results

| Run | Expected vs observed | Process outcome |
| --- | --- | --- |
| Correct before mutation | 32 cases x 3 repetitions; 96/96 expected episode outcomes; 93 complete episodes pass; three observer-fault episodes rejected as incomplete | Runner 0 |
| Disposable broken relay | Same matrix and oracle; unauthorized relay read disclosed marker; write changed value/version; 18/96 episodes fail, 78 accepted; no full-run pass | Child runner 1; mutation driver 0 because defect detected |
| Original correct source rerun | 96/96 expected episode outcomes; same source hashes and normalized observations as first run | Runner 0 |

Each correct run contains 123 request observations and 33 service dispatch records, all authorized. The observer-fault scenarios contribute no dispatches. All three repetitions agree for each variant. Repeatability establishes deterministic behavior for these fixtures, not statistical confidence about unseen attacks.

| Matrix group | Cases | Correct observation |
| --- | --- | --- |
| Authorized direct, relay, aliases | 4 | Exact reads; exact writes and single version increments; subsequent reads see written bytes |
| Unauthorized direct/relay read/write, canonical/alias | 8 | Denied response, zero dispatches, unchanged exact bytes/version |
| Forged principal/role/capability, unknown operations/routes/resources, alias spelling and malformed/missing fields | 15 | Invalid; no disclosure, dispatch or mutation |
| Authorized write replay, unauthorized replay, cross-principal replay | 3 | No duplicate mutation or borrowed authorized response; unauthorized effects absent |
| Authorized schema-error recovery | 1 | Invalid claim does not prevent next legitimate read |
| Observer unavailable, then restored | 1 | Write blocked; dispatch remains frozen on next read; oracle refuses security pass |

Six additional evidence sensitivity controls delete an event, alter a decision to a false denial, change an event principal, alter a snapshot version, omit a response or remove a step. All six are rejected in every run. They are tests of the oracle, not successful security episodes. The observer-fault fixture is counted as an expected diagnostic outcome only when it has exactly the anticipated incomplete-evidence verdict; it is never converted into a security pass.

## Failed-control counterexample

[prove_regression.py](prove_regression.py) copies the five test inputs to a temporary directory and changes exactly one guard:

```python
# Correct final resource check:
if principal != "operator-1" or target != "vault-1":
# Disposable defect: omit this check for delegated actions:
if route != "relay" and (principal != "operator-1" or target != "vault-1"):
```

Concrete observation: `forbidden-relay-read-vault-1`, repetition 1, expected a denied response, zero events, initial value/version. Observed `ok` with `SYNTHETIC-DATA-001` and one service read event attributed to `intruder-1`. The corresponding write case observed `SYNTHETIC-WRITE-001`, version **1**, and an unauthorized write event. API responses, service events and snapshots all support the local counterexample.

The four canonical/alias forbidden relay cases plus unauthorized replay and cross-principal replay fail in each repetition: 6 x 3 = 18 failed episodes. The replay scenario halts after its first unexpected disclosure; its remaining request is missing from the failed trace rather than silently run. Direct negative controls remain denied. This local regression demonstrates that the tested relay property depends on the final check and that the tests detect an actual forbidden effect.

Original model SHA-256: `cf7cf8989d08e829ceb1c71dd76a858851e690427b92696384837e9ba06a4b0d`. Mutant SHA-256: `23a7fdffb9a525fff8d9036a9aec8cc3bb67d2fb33d7a4ea85340aff5a3a8cee`. The driver verified original bytes unchanged, discarded the temporary copy and recorded the child exit 1. The third command retested the correct original. No vulnerable mode is enabled in the default implementation.

## Evidence and environment

- [Correct baseline](results/correct-before.json): expected-versus-observed records, verdicts, environment and source hashes.
- [Broken-control evidence](results/broken-relay.json): full failed traces, guard replacement, original/mutant hashes, subprocess command template and child exit.
- [Correct rerun](results/correct-after.json): full final observations and matching source hashes.
- [Frozen matrix](cases.json), [runner](run.py), [oracle](oracle.py), [model](model.py), [mutation driver](prove_regression.py).

Base commit: `106e621` on `experiment/agent-intrusion-containment`. Dedicated output branch: `feature/experiment-01-authorization-boundary`. Tested interpreter: CPython **3.11.15**, MSC v.1944, AMD64; platform reported `Windows-10-10.0.26300-SP0`. All runner invocations use `-I -S` (isolated Python mode and no site initialization). These flags are not OS isolation. No dependencies were installed, host settings changed, models called or target services contacted. Git publication is outside the offline simulation; the actor has no network interface.

Exact successful PowerShell test sequence from repository root (environment variable avoids committing a private user path):

```powershell
$python = Join-Path $env:APPDATA 'uv/python/cpython-3.11.15-windows-x86_64-none/python.exe'
& $python -I -S experiments/authorization-boundary/run.py --output experiments/authorization-boundary/results/correct-before.json
& $python -I -S experiments/authorization-boundary/prove_regression.py --output experiments/authorization-boundary/results/broken-relay.json
& $python -I -S experiments/authorization-boundary/run.py --output experiments/authorization-boundary/results/correct-after.json
```

Use a different existing interpreter path on another machine; no install is required by the experiment. Preserve committed evidence by choosing scratch outputs. `source_sha256` identifies all five executable/fixture inputs. OS/interpreter strings may differ; compare expected observations and hashes, not an environment-dependent report hash. No raw capture, real identifier, credential or live payload is present in test records.

Inspection also ran `git status --short --branch`, `git remote -v`, `git log -3 --oneline`, `rg --files`, document reads, interpreter discovery and `git diff --check`. `python --version` was unavailable, `py -3 --version` found no launcher-managed install, and `uv python list --only-installed` could not acquire its cache lock. An already installed interpreter was subsequently located by read-only directory listing and successfully invoked directly; no installation or permissions change followed. An initial optional one-line summary query failed because PowerShell stripped native-command string quoting; a PowerShell JSON query then confirmed the 93/123/33 counts. None of these discovery/query failures were security-test outcomes.

Final read-only PowerShell checks used `ConvertFrom-Json`, `Get-FileHash`, `Test-Path` and relative Markdown-link enumeration. Outcomes: all five tested source/fixture hashes match current bytes; before/after correct reports are byte-identical; expected child failure and mutation detection present; zero unauthorized service events in correct evidence; 50 relative document links resolve. `rg` review of the new package found no private user path or real credentials. `git diff --check` reported no whitespace errors (only existing root-document LF/CRLF notices). Commit and push identities are recorded by Git history, not embedded in self-referential source hashes.

The final three-command sequence was repeated after compacting report serialization to one episode per JSON line; outcomes and model hashes remained the same. A final hash/report-identity check passed. Initial staging was blocked by sandbox denial of `.git/index.lock`; staging succeeded through explicit command escalation without changing filesystem permissions. `git diff --cached --check` passed.

## Findings and residual risks

1. **Observed:** final-action checking prevented forbidden effects across the enumerated direct, alias and relay paths. Legitimate functionality passed. **Inference limited to the model:** carrying authoritative identity through delegation and checking it at the effect site addresses this modeled confused-deputy path.
2. **Observed deliberately introduced defect:** skipping the relay check allows both confidentiality and integrity violations. The independent expectation/effect comparison detects it; no actual deployment vulnerability was discovered or claimed.
3. **Design inconsistency resolved explicitly:** the previous proposals require a disconnected VM, multi-run fixtures and broader containment/repair acceptance. This task implements a smaller host-process authorization model. Those earlier criteria remain unproven, not passed. [D07](../../DECISIONS.md#2026-10-23---d07-narrow-execution-to-a-modeled-authorization-boundary) records the scope change.
4. **Trust limitation:** harness binding, resource method, observer snapshots and fixture/oracle are trusted. Same-process code and a single author do not provide tamper resistance or independent human review. An actor allowed to execute arbitrary Python could inspect closures/state; this experiment grants only data submission. A compromised authorized principal is still authorized in this model.
5. **Untested:** OS/VM escape, filesystem permissions, network egress, MCP, Hermes, Ollama, autonomous-agent behavior, real authentication, credential theft, concurrent/distributed races, caches, transactional durability, observer failure during an already executing operation, revocation/expiry, dynamic policy, multiple resources/tenants, arbitrary values, nested relay graphs, arbitrary deserialization and denial-of-service limits. Observation availability is checked synchronously before effects; crash atomicity is not established.
6. **Evidence limits:** hashes establish byte identity only. The fixture was authored before execution, but not externally sealed or reviewed by a second engineer. Finite regression coverage and mutation sensitivity do not prove universal security. No real-world vulnerability, demonstration against a vendor, attempted exploitation of a live asset or confirmed compromise is reported.

The deliverable stops at this authorization experiment. Independent reproduction consists of running the three commands, checking the child failure and exact forbidden effect, then reconciling the final run with the static matrix and service/state records.
