# Uso: .\automacao\gerar_arte_thumbnail.ps1 --prompt-file p.txt --formato longo --saida producao\L09\thumbnail_base_gerada.png [--dry-run]
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv-gemini\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw "Ambiente Python nao encontrado: $python" }
if (-not $env:GEMINI_API_KEY) {
    $env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable('GEMINI_API_KEY', 'User')
}
& $python (Join-Path $PSScriptRoot 'gerar_arte_thumbnail.py') @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
