param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Argumentos)
$ErrorActionPreference = 'Stop'
$runtime = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $runtime (Join-Path $PSScriptRoot 'narrar_voicestudio.py') @Argumentos
exit $LASTEXITCODE
