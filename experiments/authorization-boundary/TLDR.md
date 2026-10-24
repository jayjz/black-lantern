# Experiment 01 TLDR

The modeled boundary held for the tested requests: an unauthorized synthetic actor could not read or change the in-memory vault directly or through the relay. Legitimate reads and writes remained usable.

- Correct control: **96/96 expected episode outcomes**, including three observer-fault episodes explicitly marked incomplete, never a security pass. The 93 complete episodes passed.
- Broken control: bypassing final authorization for relay requests caused actual synthetic disclosure and mutation. The runner exited **1**, failing **18/96 episodes**.
- Correct source remained unchanged and passed again. Six evidence-corruption controls were detected. Three fresh repetitions produced identical observations.

This establishes sensitivity to one broken authorization check and a narrow result for a data-only Python model. It proves nothing about real agents, operating-system isolation, networks, MCP, compromised trusted code or arbitrary Python execution.

[Reproduction commands and boundary](README.md) · [Engineering report and all findings](REPORT.md) · [Full evidence](results/correct-after.json) · [Counterexample](results/broken-relay.json)
