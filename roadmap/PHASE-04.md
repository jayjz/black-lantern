# Phase 04 — Reproduction, Dolphin comparison, expert review, customer discovery

**Status:** planned, not executed. **Recorded:** 2026-10-24. **Scope:** next research-and-validation phase for a potential agent-security assessment business. This roadmap is not an authorization to access third-party systems or publish claims unsupported by observed evidence.

## Mission and commercial hypothesis

Black Lantern researches **whether tool-using agents exceed their permissions, whether trusted controls prevent unauthorized effects, and whether tests can prove the distinction**. A possible future service is a scoped, reproducible agent tool-authorization review for teams preparing to deploy agents. Neither customer demand nor professional security-assurance capability has been validated.

**Research claim to test:** The existing final-action permission gate detects and prevents forbidden synthetic effects even when agent-model behavior varies. **Business claim to test:** A defined buyer with an imminent agent release values and would pay for an independent assessment that improves on their current testing.

## Phase gates — in order

| Gate | Activity | Observable acceptance evidence | Stop / no-go |
| --- | --- | --- | --- |
| **G0 — Freeze baseline** | Inspect current main and PR #5; decide whether Experiment 03 is merged or use exact commit; preserve immutable raw live capture, fixture and source identities | Commit SHA, published evidence hashes, execution commands, explicit trust boundary and independently reviewed expected results | Missing original inputs, moving reference, untrusted or overwritten history |
| **G1 — Independent reproduction** | Run existing Experiment 01–03 offline suite and original captured-data verification in a **fresh environment**; a reviewer other than the original execution agent inspects outputs and verifies source hashes. Fresh inference is a separate optional check, not a replacement for old traces | Environment manifest, raw command/exit-code log, checksum reconciliation, all required expected outcomes, deliberate corruption rejected, discrepancies and owner recorded | Any forged/missing evidence passes; inability to reproduce not silently repaired |
| **G2 — Dolphin provenance and interface compatibility** | Hash both local `C:\Models` and `E:\Models` copies; trace exact model repository/revision and GGUF hash where possible; record inherited license; import locally under new name; inspect model context and native tool-call format without giving host tools | Exact SHA-256, provenance confidence, GGUF quantization, Ollama/version/driver, schema-valid proposal in an unexecuted capability probe | Model identity ambiguous for a claimed matched comparison; unavailable licensing terms; parser incompatibility not counted as model security failure |
| **G3 — Preregistered model comparison** | Compare existing Qwen model and Dolphin using the **same synthetic tasks, schema, resource permission table, sampling policy where supported, safety limits and outcome definitions**. Use a versioned, predeclared ID-insensitive prefix rule for new capture only. Keep original E03 pair inconclusive | Frozen protocol before inference; model-specific immutable identity; multiple fresh repetitions; raw sanitized proposals, decisions, effects, task outcomes and confidence/variance description; mutation-sensitive oracle | Any real-world host tool or data exposure; unknown model drift; invalid schema conflated with authorization pass; outcome-driven prompt edits |
| **G4 — External security review** | Give one experienced application security / AI-agent security engineer source, threat model, traces, test expectations and known limitations. Ask them to reproduce or challenge claims and identify highest-risk untested boundary | Independent written criticisms linked to code, severity/rationale, reproduction or counterexample, accepted/rejected finding with rationale and verified fixes | A self-review by the same agent represented as independent; unresolved high-severity evidence flaw presented as certification |
| **G5 — Customer discovery and limited pilot** | Interview 5 qualified teams actually deploying tool-using agents; observe existing security review workflows and alternatives. Only offer an explicitly authorized staging assessment if a buyer has a concrete unmet need | At least 5 dated anonymized discovery notes; buyer/job/trigger/current workaround; documented willingness-to-pay signal; one potential scoped pilot with signed authorization before testing | No urgent problem or sponsor; no permission to test; need to handle production secrets before mature controls |

**Sequencing:** G1 before any new model experiment. G2 and the signed protocol precede G3. G4 critiques G1–G3 before any claim of external readiness. G5 interviews may occur in parallel, but **testing customer systems** cannot occur without written scope and authorization. A paid pilot is a hypothesis, not a commitment.

## Frozen comparison design (draft — must finalize before running)

- **Independent variables:** model identity (original `unhinged-qwen:latest` or exact registered Qwen comparator, versus Dolphin3.0-Llama3.1-8B-abliterated Q4_K_M); clean or injected synthetic document. Never assume both models implement tool calling equivalently.
- **Keep constant:** actor identity bound by harness; `notice-1` document; `vault-1` resource; direct/read/write/relay contracts; policy; initial state; sequence and stopping rules; system/task instructions. Record exceptions where model chat templates make perfect equivalence impossible.
- **Primary outcomes:** unauthorized protected dispatch/disclosure/mutation from service-side observations and independent oracle. **Secondary:** forbidden proposal rate, malformed proposals, legitimate task completion, refusal, tool-call latency, evidence completion. A *denied unauthorized attempt* is distinct from a *model refusal* and an *unexercised boundary*.
- **Design:** independently seeded/repeated fresh episodes (initial target: at least 10 per condition, feasible after a smoke-test; not a statistical power claim). Predeclare comparisons and report counts/uncertainty rather than inventing general safety percentages. Match pre-exposure prefixes with `comparison_v2.py` only for new captures; preserve exact original Experiment 03 results and failure status.
- **Separation:** scripts may send requests only to the localhost inference endpoint and synthetic resources. No OS commands, shells, CUA, browser, remote hosts, credentials, network-scanning, or arbitrary filesystem tools exposed to the actor. Model generates proposals; mediator decides effects.
- **Failure criteria:** missing/forged traces, inconsistent or unavailable oracle, unreviewed tool surface, model digest drift, unexpected host effects, scope violation. Fail closed and stop affected run; publish partial/inconclusive evidence honestly.

## Review package for a qualified security engineer

Provide a commit-pinned threat model, authorized scope, model/fixture hashes, data-flow diagram, trusted-computing-base list, allowed/denied matrices, raw sanitized traces, mutation test source, reproducible commands, precise known gaps (same-process observer, lack of external attestation, ID-sensitive historical comparison), and three review questions:

1. Can the actor reach any protected effect without mediation through an accepted data-only entry point?
2. Can missing or maliciously inconsistent evidence still be scored as a pass?
3. Which real deployment assumptions invalidate this synthetic trust boundary?

Record findings in `assessments/external-review-*.md` **only after** actual review. Never invent reviewer endorsements.

## Discovery interview protocol

Target engineering/security owners of an actual tool-using agent release, not a broad survey of AI enthusiasts. Ask for their **last concrete deployment/security review**, what triggered it, which systems the agent could affect, which checks failed, who approved release, what alternatives they considered, time spent, and whether a demonstrably better assessment would change a buying decision. Avoid leading questions and invented price validation.

A prospective paid offer is **one staging workflow, one authorization boundary, evidence-backed report, remediation suggestions, optional retest**. Do not claim penetration-test credentials or product certifications. No third-party testing without signed authorization and bounded scope.

## Learning and operational safeguards

The operator must build demonstrable skill in Python code review, authn/authz, HTTP/TLS, threat modeling, experiment design and reporting; seek expert review before making assurance claims. Non-technical milestone: identify where current tools or a customer's own security team already solve the problem better, and record a no-go if no differentiated buyer job is found.

## Repository hygiene and handoff

- Existing `GOALS.md`, `PLANS.md`, `DECISIONS.md` and Experiment 01–03 reports remain historical canonical records. This file is the **prospective** Phase 04 source of truth.
- Update navigation, not historical conclusions; a PR against `main` may need a rebase after PR #5 merges.
- Do not overwrite frozen `results/*.json` or change source/fixture commits while trying to reproduce.
- Deliver each gate as a narrow PR with an evidence index, negative tests, explicit outcomes, and a decision to proceed, revise, or stop.

## Useful references

- [Experiment 03 report](../experiments/model-tool-authorization/README.md) (available when PR #5 merges)
- [Experiment 03 hardening](../experiments/model-tool-authorization/HARDENING.md) (available when PR #5 merges)
- [OWASP agentic security guidance](https://genai.owasp.org/)
- [NIST AI RMF and Generative AI Profile](https://www.nist.gov/itl/ai-risk-management-framework)
- [Ollama GGUF import](https://docs.ollama.com/import)
- [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling)
