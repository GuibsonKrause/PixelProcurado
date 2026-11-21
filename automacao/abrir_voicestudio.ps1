$ErrorActionPreference = 'Stop'
$app = Join-Path $env:LOCALAPPDATA 'Programs/VoiceStudio/VoiceStudio.exe'
$runtimePython = Join-Path $env:APPDATA 'VoiceStudio/runtime/project/.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $runtimePython)) { throw 'Runtime do VoiceStudio não encontrado.' }
# A checagem de imports da versão 0.5.6 expira em 30s neste computador.
# Usar o override documentado mantém o backend supervisionado pelo Electron.
$env:OMNIVOICE_BACKEND_CMD = ConvertTo-Json -Compress -InputObject @($runtimePython, '-m', 'uvicorn', 'main:app', '--app-dir', 'backend', '--host', '127.0.0.1', '--port', '3900')
$env:OMNIVOICE_STARTUP_BUDGET_S = '600'
$env:SUPERTONIC_INTRA_OP_THREADS = '4'
$env:SUPERTONIC_INTER_OP_THREADS = '1'
$env:OMNIVOICE_SUPERTONIC3_RECV_TIMEOUT_S = '900'
$env:OMNIVOICE_MOSS_TTS_MODEL = Join-Path $PSScriptRoot '../.production-tools/models/MOSS-TTS-Nano'
$env:OMNIVOICE_MOSS_TTS_TOKENIZER = Join-Path $PSScriptRoot '../.production-tools/models/MOSS-Audio-Tokenizer-Nano'
$logDir = Join-Path $PSScriptRoot '../.production-tools/voice-bootstrap'
Start-Process -FilePath $app -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDir 'app-out.log') -RedirectStandardError (Join-Path $logDir 'app-err.log')
