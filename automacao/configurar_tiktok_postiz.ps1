# Script para configurar TikTok Client Key e Secret no Postiz
$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Configurador TikTok OAuth - Postiz" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

$postizDir = "C:\Users\guibson.krause\Documents\ChatGPT\Postiz"
$composeFile = Join-Path $postizDir "docker-compose.yaml"

if (-not (Test-Path $composeFile)) {
    Write-Error "Arquivo docker-compose.yaml nao encontrado em $postizDir"
    exit 1
}

$clientKey = Read-Host "Cole o Client key do TikTok"
$clientSecret = Read-Host "Cole o Client secret do TikTok"

$clientKey = $clientKey.Trim()
$clientSecret = $clientSecret.Trim()

if ([string]::IsNullOrWhiteSpace($clientKey) -or [string]::IsNullOrWhiteSpace($clientSecret)) {
    Write-Warning "Client Key ou Client Secret nao podem ser vazios!"
    exit 1
}

Write-Host "`nAtualizando docker-compose.yaml..." -ForegroundColor Cyan

$content = [System.IO.File]::ReadAllText($composeFile, [System.Text.Encoding]::UTF8)

$content = [System.Text.RegularExpressions.Regex]::Replace(
    $content,
    "(?m)^\s*TIKTOK_CLIENT_ID:\s*.*$",
    "      TIKTOK_CLIENT_ID: '$clientKey'"
)

$content = [System.Text.RegularExpressions.Regex]::Replace(
    $content,
    "(?m)^\s*TIKTOK_CLIENT_SECRET:\s*.*$",
    "      TIKTOK_CLIENT_SECRET: '$clientSecret'"
)

[System.IO.File]::WriteAllText($composeFile, $content, [System.Text.Encoding]::UTF8)

Write-Host "docker-compose.yaml atualizado com sucesso!" -ForegroundColor Green
Write-Host "Reiniciando o conteiner do Postiz..." -ForegroundColor Cyan

Push-Location $postizDir
try {
    docker compose up -d postiz
    Write-Host "`n[SUCESSO] Postiz atualizado e reiniciado com o TikTok configurado!" -ForegroundColor Green
    Write-Host "Acesse http://localhost:4007 e conecte sua conta do TikTok." -ForegroundColor Yellow
} finally {
    Pop-Location
}
