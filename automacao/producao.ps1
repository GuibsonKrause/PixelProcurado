param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Argumentos)
$ErrorActionPreference = 'Stop'
$runtime = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
if (-not (Test-Path -LiteralPath $runtime)) { throw 'Python 3.12 do runtime não encontrado. Configure o caminho em automacao/producao.ps1.' }
& $runtime (Join-Path $PSScriptRoot 'producao.py') @Argumentos
exit $LASTEXITCODE
