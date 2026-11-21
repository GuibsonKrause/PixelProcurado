param(
    [Parameter(Mandatory=$true)][string]$Texto,
    [string]$Saida = 'producao/L01/voz/clone_guibson/novo_teste.wav'
)
$ErrorActionPreference = 'Stop'
$destino = [IO.Path]::GetFullPath((Join-Path (Join-Path $PSScriptRoot '..') $Saida))
if (Test-Path -LiteralPath $destino) { throw "A saída já existe: $destino" }
$health = Invoke-RestMethod 'http://127.0.0.1:3900/health' -TimeoutSec 10
if ($health.status -ne 'ok') { throw 'O VoiceStudio não está pronto.' }
$body = @{
    model = 'moss-tts-nano'
    voice = '097c5b55'
    input = $Texto
    language = 'pt'
    response_format = 'wav'
    denoise = $true
    preprocess_prompt = $true
} | ConvertTo-Json
Invoke-WebRequest 'http://127.0.0.1:3900/v1/audio/speech' -Method Post `
    -ContentType 'application/json; charset=utf-8' `
    -Body ([Text.Encoding]::UTF8.GetBytes($body)) -OutFile $destino -TimeoutSec 1800
Write-Output "Gerado: $destino"
