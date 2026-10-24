[CmdletBinding()]
param(
    [string]$ServerPath = 'C:\llama.cpp-cuda12\llama-server.exe',
    [string]$ModelPath = 'C:\Models\Dolphin3.0-Llama3.1-8B-abliterated.Q4_K_M.gguf',
    [ValidatePattern('^[a-fA-F0-9]{64}$')]
    [string]$ExpectedModelSha256 = '73da18db1557e19e8ec2d6c1e8ef08e182c735d72f3bd526f6940f4fec96c1cb',
    [ValidateSet(4096,8192)][int]$ContextSize = 4096,
    [ValidateRange(1024,65535)][int]$Port = 8080,
    [switch]$CheckOnly
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
foreach ($item in @($ServerPath, $ModelPath)) {
    if (-not [IO.Path]::IsPathRooted($item) -or -not (Test-Path -LiteralPath $item -PathType Leaf)) {
        throw "Absolute existing file required: $item"
    }
}
$ServerPath = (Resolve-Path -LiteralPath $ServerPath).ProviderPath
$ModelPath = (Resolve-Path -LiteralPath $ModelPath).ProviderPath
if ([IO.Path]::GetExtension($ServerPath) -ne '.exe' -or [IO.Path]::GetExtension($ModelPath) -ne '.gguf') {
    throw 'Expected an EXE server and GGUF model.'
}
$modelHash = (Get-FileHash -LiteralPath $ModelPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($modelHash -ne $ExpectedModelSha256.ToLowerInvariant()) { throw 'Model SHA-256 mismatch; refusing launch.' }
$serverHash = (Get-FileHash -LiteralPath $ServerPath -Algorithm SHA256).Hash.ToLowerInvariant()
# Remove inherited llama configuration, including built-in tools, remote models and RPC.
# Restore the parent environment after creating the child; no values enter the log.
$savedEnvironment = @{}
Get-ChildItem Env: | Where-Object Name -Like 'LLAMA_*' | ForEach-Object {
    $savedEnvironment[$_.Name] = $_.Value
}
$process = $null
try {
    foreach ($name in $savedEnvironment.Keys) { [Environment]::SetEnvironmentVariable($name, $null, 'Process') }
    # PowerShell 5 treats native stderr as ErrorRecord under Stop. Capture version
    # through Start-Process below rather than relying on native stderr redirection.
    $logRoot = Join-Path $PSScriptRoot '../evidence/runs/llama'
    $runDirectory = Join-Path $logRoot ([Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $runDirectory -Force | Out-Null
    $versionProcess = Start-Process -FilePath $ServerPath -ArgumentList '--version' -PassThru -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runDirectory 'version.stdout.log') -RedirectStandardError (Join-Path $runDirectory 'version.stderr.log')
    if (-not $versionProcess.WaitForExit(15000)) { $versionProcess.Kill(); throw 'Version check timed out.' }
    $version = (Get-Content (Join-Path $runDirectory 'version.stdout.log') -Raw -ErrorAction SilentlyContinue) + (Get-Content (Join-Path $runDirectory 'version.stderr.log') -Raw -ErrorAction SilentlyContinue)
    if ($version -notmatch '8833 \(45cac7ca7\)') { throw 'Unreviewed server build; re-audit flags before use.' }
    $arguments = @('--model', ('"' + $ModelPath + '"'), '--host', '127.0.0.1', '--port', "$Port",
        '--gpu-layers', 'all', '--ctx-size', "$ContextSize", '--flash-attn', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0', '--batch-size', '512',
        '--ubatch-size', '256', '--threads', '6', '--parallel', '1', '--fit', 'off',
        '--n-predict', '128', '--timeout', '60', '--offline', '--no-webui', '--no-webui-mcp-proxy', '--no-slots')
    $identity = [ordered]@{ utc = [DateTime]::UtcNow.ToString('o'); model_sha256 = $modelHash;
        model_bytes = (Get-Item -LiteralPath $ModelPath).Length; server_sha256 = $serverHash;
        version = $version.Trim(); context = $ContextSize; arguments = $arguments; check_only = [bool]$CheckOnly }
    $identity | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runDirectory 'identity.json') -Encoding UTF8
    Write-Output "Model SHA-256: $modelHash; context: $ContextSize; listener: 127.0.0.1:$Port"
    Write-Output "Private logs: $runDirectory"
    if ($CheckOnly) { return }
    # Fail closed if a listener already owns the port. This probes no remote host.
    $probe = New-Object Net.Sockets.TcpListener([Net.IPAddress]::Loopback, $Port)
    $probe.Server.ExclusiveAddressUse = $true
    try { $probe.Start() } finally { $probe.Stop() }
    $process = Start-Process -FilePath $ServerPath -ArgumentList $arguments -PassThru -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runDirectory 'server.stdout.log') -RedirectStandardError (Join-Path $runDirectory 'server.stderr.log')
} finally {
    foreach ($name in $savedEnvironment.Keys) { [Environment]::SetEnvironmentVariable($name, $savedEnvironment[$name], 'Process') }
}
try {
    Write-Output "Owned server PID: $($process.Id). Ctrl+C stops this child. No host tools enabled."
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw "Server exited $($process.ExitCode); inspect private logs." }
} finally {
    if ($null -ne $process -and -not $process.HasExited) { $process.Kill(); $process.WaitForExit() }
}
