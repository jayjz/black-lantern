# Local llama.cpp audit — 2026-10-24

**Observed:** the existing 4096-context loopback server completed one warmup and three measured synthetic requests. Median prompt processing: **2191.06 tokens/s**; generation: **42.53 tokens/s**. New-launch loading and 8192 tests were **skipped**: the user explicitly chose to preserve the running process and avoid competing loads. These numbers describe a 1466-token prompt in a 4096-capacity context, not a filled 4096-token prompt, security evaluation, or sustained throughput guarantee.

Canonical scope, limits and acceptance were recorded before inference in [PLANS.md](../PLANS.md#version-control-and-local-runtime-audit-acceptance-gate). [Launcher](../scripts/Start-LocalLlama.ps1), [metadata/benchmark helper](../scripts/audit_local_llama.py), [reviewed machine-readable observations](../evidence/llama-baseline-2026-10-24.json).

## Local identity and environment

Inspected 2026-10-24 UTC. Hardware supplied by user: Windows 11, i5-13400F, 32 GB RAM, RTX 4060 8 GB. GPU independently detected by NVIDIA-SMI and llama.cpp: RTX 4060, compute capability 8.9, 8188 MiB reported by NVIDIA-SMI (8187 MiB by llama.cpp), WDDM, driver 610.88. NVIDIA-SMI's CUDA UMD 13.3 is driver capability, not a claim that this binary was compiled with CUDA 13.3. CUDA12 directory contains cudart64_12.dll/cublas64_12.dll; binary loads ggml-cuda.dll and ggml-cpu-alderlake.dll, plus an available RPC backend. Backend availability is not RPC authorization or a remote connection.

- Server: `C:\llama.cpp-cuda12\llama-server.exe`; version `8833 (45cac7ca7)`, Clang 19.1.5, Windows x86_64. EXE SHA-256: `8f535089d8ce1996a2fd784a40a8207fc620122e2b584176b65e77f824c16a13`. Hash/version self-report do not attest the supply chain or associated DLLs.
- Model: `C:\Models\Dolphin3.0-Llama3.1-8B-abliterated.Q4_K_M.gguf`; 4,920,745,984 bytes. SHA-256: `73da18db1557e19e8ec2d6c1e8ef08e182c735d72f3bd526f6940f4fec96c1cb`. File last-write UTC observed as 2026-10-24 18:40:10; filesystem timestamps are not publication provenance (and this timestamp is ahead of the observation clock).
- Parsed locally: GGUF v3, 292 tensors; architecture llama; 32 blocks; 4096 embedding; 32 attention heads / 8 KV heads; K/V head dimension 128; declared training context 131072; RoPE base 500000; quantization version 2 / general.file_type 15. Filename labels Q4_K_M; no independent tensor-type census performed.
- Embedded metadata names `Unsloth_Gguf_X01U6R2L`, quantized_by Unsloth, generic repository URL `https://huggingface.co/unsloth`; these untrusted fields do not establish an exact upstream model, revision, inherited license, checksum or abliteration lineage. Those remain unknown; this task did not resolve them or compare another local copy. No model downloads/imports occurred.
- Embedded chat template is ChatML style, using `<|im_start|>`/`<|im_end|>`. `/props` reports support for tools/tool calls **false**. Benchmark uses raw `/completion`, does not claim native tool compatibility and never executes output.

## Existing server, not a new launch

Read-only process inspection found one matching process and listener **127.0.0.1:8080 only**. Command line:

```text
llama-server.exe -m C:\Models\Dolphin3.0-Llama3.1-8B-abliterated.Q4_K_M.gguf -ngl all -c 4096 -fa on --cache-type-k q8_0 --cache-type-v q8_0 -b 512 -ub 256 -t 6 -np 1 --fit on --host 127.0.0.1 --port 8080
```

`GET /health` and `GET /props` each returned HTTP 200; props confirmed model path/alias, build b8833-45cac7ca7, effective context 4096 and one slot. The command requests full GPU offload, FA and Q8 cache. Startup allocation logs were not captured, so an exact effective offloaded-layer count/cache allocation is not independently verified. The existing process uses `--fit on` and enables its Web UI; the reviewed launcher uses `--fit off` and disables Web UI/MCP proxy. The benchmark therefore does not validate every launcher setting. No tools were supplied in requests; the process command contains no `--tools`; inherited environment of the preexisting process was not inspected. No host-control tools were granted by this audit.

Initial NVIDIA-SMI readings were approximately 6192 MiB used. During benchmark, whole-GPU snapshots were 6211–6252 MiB used and 1705–1746 MiB free; other desktop/GPU activity is included. The driver's used/free/total figures are reported as returned and need not add exactly under WDDM. `--list-devices` reported 6388 MiB free at a nearby observation, inconsistent with NVIDIA-SMI's ~1.7 GiB free; this estimate was not used to justify another load. No other process was stopped or reconfigured.

## Official flag verification

Primary sources: [server documentation at installed commit](https://github.com/ggml-org/llama.cpp/blob/45cac7ca703fb9085eae62b9121fca01d20177f6/tools/server/README.md) and [argument parser at installed commit](https://github.com/ggml-org/llama.cpp/blob/45cac7ca703fb9085eae62b9121fca01d20177f6/common/arg.cpp). Official commit metadata: revision date **2026-04-17T16:17:11Z**, [commit](https://github.com/ggml-org/llama.cpp/commit/45cac7ca703fb9085eae62b9121fca01d20177f6); retrieval 2026-10-24. No separate page publication date is supplied. Both were downloaded directly from official raw GitHub into ignored scratch and checked against the installed `--help` output. These claim mappings cover every launcher flag; no flags were inferred from another runtime/version.

| Launcher flag | Value / verified meaning |
| --- | --- |
| `--version` | Identity-only preflight; build output |
| `--model` | Explicit existing local GGUF path |
| `--host`, `--port` | Fixed 127.0.0.1; integer 1024–65535 |
| `--gpu-layers` | `all`, full-offload request |
| `--ctx-size` | 4096 default; explicit 8192 opt-in |
| `--flash-attn` | `on`, explicit enabled request |
| `--cache-type-k`, `--cache-type-v` | `q8_0` accepted for each |
| `--batch-size`, `--ubatch-size` | 512 logical / 256 physical, below build defaults 2048/512 |
| `--threads` | 6 generation CPU threads, initial conservative setting; not CPU tuned |
| `--parallel` | 1 server slot |
| `--fit` | `off`; do not silently adjust unset allocation settings |
| `--n-predict` | 128 default generation limit; not an unoverrideable per-request quota |
| `--timeout` | 60 seconds server read/write timeout; not a hard compute deadline |
| `--offline` | Prevent model downloading through runtime download paths |
| `--no-webui`, `--no-webui-mcp-proxy`, `--no-slots` | Disable Web UI, MCP CORS proxy and slot monitoring |

Official parser's `--tools` entry documents built-in shell/file tools, disabled by default. Launcher never sets this flag and removes all inherited `LLAMA_*` variables before creating either child, restoring the parent's values afterward without logging them. This also prevents inherited RPC, remote model and host overrides. No arbitrary extra-argument parameter is accepted. Explicit flags remain visible in the private identity log. Loopback binding and absent tools reduce exposure; they are not an OS sandbox against local users/processes.

## Measurements

Protocol: same synthetic lantern prompt, no personal data, temperature 0, seed 1234, `cache_prompt=false`, `stream=false`, `ignore_eos=true`, 64 generated tokens. One warmup plus three measured requests, serial, four total. Every response: 1466 prompt tokens, 64 generated tokens, zero cached tokens. Text was discarded, never interpreted as instructions. Native `/completion` timing fields come from this server and are local observations, not an independent timing implementation. Python wall time includes small HTTP/serialization overhead; it excludes each pre-request GPU snapshot.

| Request | Prompt tokens/s | Generation tokens/s | Wall seconds | GPU after MiB used |
| --- | ---: | ---: | ---: | ---: |
| Warmup | 1645.19 | 43.37 | 2.375 | 6221 |
| 1 | 2230.04 | 43.22 | 2.141 | 6223 |
| 2 | 2179.73 | 42.01 | 2.218 | 6226 |
| 3 | 2191.06 | 42.53 | 2.172 | 6252 |

Measured medians: prompt 2191.06 tokens/s (2179.73–2230.04), generation 42.53 tokens/s (42.01–43.22), wall 2.172 s. Short sample, shared desktop, no continuous peak/per-process VRAM attribution, no thermal soak or power/CPU sweep. No 4096-token occupancy or long-context speed claim. The Q8 KV footprint inferred from architecture is about 272 MiB at 4096 and 544 MiB at 8192 (32 layers × 8 heads × 128 dimensions × two caches × 34/32 bytes per element); this is an estimate excluding weights, alignment, graphs, buffers and driver overhead, not proof 8192 fits.

8192 and fresh loading were skipped by the user's explicit keep-running choice. A concurrent load with only ~1.7 GiB free was not justified. Future 8192 validation requires a separately agreed single-model window, actual allocation/offload checks and the same prompt protocol before comparing speeds. No quality/security comparison is authorized by such a performance test.

## Reproduce

From repository root in PowerShell, use the installed standard-library CPython used here:

```powershell
$auditPython = Join-Path $env:APPDATA 'uv/python/cpython-3.11.15-windows-x86_64-none/python.exe'
& $auditPython -I -S scripts/audit_local_llama.py --metadata 'C:\Models\Dolphin3.0-Llama3.1-8B-abliterated.Q4_K_M.gguf' --output evidence/runs/fresh-model.json
& $auditPython -I -S scripts/audit_local_llama.py --benchmark --output evidence/runs/fresh-4096.json
& ./scripts/Start-LocalLlama.ps1 -CheckOnly
```

Actual benchmark/metadata output paths were `evidence/runs/launch-audit/benchmark.json` and `metadata.json`; both commands exited 0. No dependencies installed. `/health` and `/props` were also inspected with .NET HttpClient, proxy and redirects disabled. The helper uses fixed loopback HTTPConnection, no proxies/redirects, 60-second socket timeout, 2 MiB response bound and 10-second NVIDIA-SMI subprocess timeout. It refuses an existing output path; capture failures stop with nonzero exit. The measured completion requests totaled 256 generated tokens.

Launcher `-CheckOnly` exited 0 after exact SHA/path/build validation and wrote an ignored identity log. PowerShell AST parser and Python `ast.parse` passed. Explicit missing EXE, all-zero expected hash and context 16384 were rejected; normal launch at the occupied 8080 port was rejected before creating a model-loading child. Test harness exited 0 after verifying each expected exception. This tested a live occupied listener but never killed it. The version check uses a hidden process with a 15-second deadline. CheckOnly logs configuration without binding; it does not prove available memory, port availability, loading, shutdown, full GPU placement or inference through the new launcher.

To launch later when the port/GPU are available:

```powershell
& ./scripts/Start-LocalLlama.ps1
# Only after reviewing memory and arranging a single-model window:
& ./scripts/Start-LocalLlama.ps1 -ContextSize 8192
```

These two launch commands were **not executed successfully** in this task. Launcher blocks while its hidden child runs and attempts to stop only that owned child in `finally`; Ctrl+C cleanup is not verified here and cannot protect against forcibly terminating the shell. It creates unique ignored log directories and logs model/binary hashes and arguments. Changed build 8833 requires flag re-audit; a changed model requires explicit reviewed expected hash. The GGUF is never loaded into a host-control agent.

Validation also reconciled all four token/cache/warmup records and independently recomputed the medians from the reviewed JSON. All 20 launcher flag names exist in both pinned official parser and server README. All 68 relative link targets in changed/root/added documentation resolved. `git diff --check` passed; `git diff --exit-code origin/main -- experiments` exited 0, and PR #5's local branch still resolves to its original SHA. The experiment regression suites were not rerun because their source/evidence was unchanged; no Experiment 03 capture was regenerated.

Initial sandbox process/listener inspection was denied; approved read-only rerun succeeded. Official raw-document downloads and remote Git reads required approved network reruns. Public web fetch of the server README failed, so direct pinned raw-source download was used. `gh`/system Python were unavailable; GitHub connector and the already installed uv-managed CPython were used. No shell policy, installation, inference process or host configuration was changed.
