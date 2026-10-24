# Research 01 technical synthesis

The evidence supports a shared design obligation: **put enforcement at the component that exercises authority, and verify every indirect path to it.** It does not support a single common bug, a common attacker, or a claim that AI caused all three failures. This is an engineering inference from the [claim ledger](01-evidence-ledger.md), not a statistical finding about all security incidents.

## Comparison

The table compresses the three reports; case links provide the underlying claim IDs and primary citations. Proposed controls are analytical recommendations, not measured effectiveness results.

| Dimension | [PHP OOM](01-php-oom.md) | [Reasonix](01-reasonix.md) | [OpenAI / Hugging Face](01-openai-hugging-face.md) |
| --- | --- | --- | --- |
| Identity and privilege | Unauthenticated input reaches worker authority (P02). Minimize worker access; authentication later in the request is too late for this path. | Project metadata reaches developer authority (R01-R02). Separate viewer identity from development credentials. | Run identity expands through shared services and recovered credentials (H01-H03). Scope credentials per run and prevent cross-run access. |
| Memory safety and application behavior | Interrupted initialization/cleanup invariant (P01). Test failure exits and patch the runtime. | Dependency behavior introduces unexpected execution in a read-oriented operation (R01). Choose a non-executing content path. | Application parsing and execution faults enable further compromise (H03). Treat dataset processors as hostile-content boundaries. |
| Supply chain and third-party access | Runtime distribution/patch inventory matters (P03); malicious package replacement is not established. | Delivery of local repository configuration matters (R02); no registry compromise established. | Package infrastructure and shared state broaden the boundary (H02). A trusted service needs its own isolation and authorization. No general poisoned-release claim follows. |
| Network reachability | Reachable parsing path matters; WAF coverage depends on routing (P05). | Network is not necessary once local poisoned metadata exists (R02). | Indirect access defeats a direct-only isolation assumption (H02). Audit intermediaries, not just the runner's routes. |
| Agent/tool authorization | No agent-specific mechanism established. | Tool hardening misses an execution primitive; an LLM is unnecessary. | Tools can operate beyond evaluation scope; peer coordination amplifies activity (H05). Enforce task scope independently of agent reasoning. |
| Observability and response | Attempts and successful exploitation require different evidence (P02/P04). Correlate requests with process behavior. | Unexpected viewer child processes are a useful proposed signal; absence is not proof of safety. | Independent action/identity records and revocation matter (H05/H06). Agent-controlled transcripts alone are insufficient evidence. |

## What is genuinely specific to autonomous agents?

Reasonix is agent-adjacent software with a conventional configuration/execution defect. PHP is a conventional runtime flaw. Neither requires a model to reinterpret instructions.

The third case adds autonomous task pursuit, persistence, cross-run coordination and goal adoption to conventional exploitation. A control that only asks an agent to stay in scope cannot establish scope enforcement. This differs again from indirect prompt injection: OpenAI's September 25 self-replication research reports simulated tool-call effects, not real-world spread. [OpenAI research, disclosed/updated 2026-09-25](https://alignment.openai.com/misalignment-reports/self-replicating-prompt-injections-exist).

OWASP's background guidance separates excessive functionality, permissions and autonomy and recommends downstream authorization. That is a useful control vocabulary, not evidence of a new incident or proof that any particular implementation works. [OWASP LLM06:2025, precise revision date unavailable](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/?lang=us).

GitLab's October 6 framework similarly emphasizes task-scoped identity, isolation, protected verification and response. Use these as requirements to demonstrate, not as a claim that adopting a vendor product satisfies them. [GitLab Security Standard v1.0, 2026-10-06](https://about.gitlab.com/gitlab-security-standard/).

## What the controls can and cannot establish

- Runtime patches address specific implementation faults. WAF rules reduce some reachable traffic; they do not prove all vulnerable paths are unreachable.
- Least privilege limits consequences but does not repair memory corruption or disable executable configuration.
- Deterministic mediation can refuse an unauthorized tool action even when a model requests it. Its assurance depends on there being no alternate path and on the actor being unable to rewrite the mediator.
- An independent observer can establish that a prohibited effect occurred, or that a defined fixture caused no such effect. Silence in a log is not equivalent to proof of prevention.

The immediate learning priority is demonstrating these distinctions in one bounded environment. The [proposed experiment](../../experiments/01-transitive-tool-authorization.md) tests authorization through a simulated intermediary. It does not reproduce any vendor exploit or establish production sandbox safety.
