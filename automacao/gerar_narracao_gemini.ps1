param(
    [string[]]$Roteiros = @(
        'producao/cortes/C02_GEMINI.txt',
        'producao/cortes/C03_GEMINI.txt'
    ),
    [switch]$Todos,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv-gemini\Scripts\python.exe'
$generator = Join-Path $PSScriptRoot 'gemini_tts.py'

if (-not (Test-Path -LiteralPath $python)) {
    throw "Ambiente Python nao encontrado: $python"
}

if (-not $env:GEMINI_API_KEY) {
    $env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable('GEMINI_API_KEY', 'User')
}

$arguments = @($generator)
if ($Todos) {
    $arguments += '--all-shorts'
}
else {
    $arguments += $Roteiros
}
if ($DryRun) {
    $arguments += '--dry-run'
}

Push-Location $root
try {
    & $python @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "A geracao falhou com codigo $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
