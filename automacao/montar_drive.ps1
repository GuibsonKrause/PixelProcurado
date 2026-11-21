# Monta o Google Drive (gdrive:GamePlay) na unidade P: com cache local limitado (rclone + WinFsp).
# Os arquivos de midia arquivados no projeto sao links simbolicos para P:\...; sem a montagem eles ficam inacessiveis.
# Uso: .\automacao\montar_drive.ps1            (monta se ainda nao estiver montado; roda oculto)
#      .\automacao\montar_drive.ps1 -Parar     (desmonta)
param([switch]$Parar)

$cfg = Get-Content (Join-Path $PSScriptRoot 'armazenamento.json') -Raw | ConvertFrom-Json
$letra = $cfg.montagem.TrimEnd('\').TrimEnd(':') + ':'
$rclone = (Get-Command rclone -ErrorAction SilentlyContinue).Source
if (-not $rclone) { $rclone = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Links\rclone.exe' }

$proc = Get-CimInstance Win32_Process -Filter "Name='rclone.exe'" | Where-Object { $_.CommandLine -match ' mount ' }
if ($Parar) { $proc | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }; "desmontado"; return }
if ($proc -and (Test-Path "$letra\")) { "ja montado em $letra"; return }

$logDir = Join-Path $env:LOCALAPPDATA 'PixelProcurado'
New-Item -ItemType Directory -Force $logDir | Out-Null
$args = @('mount', $cfg.remoto, $letra,
  '--vfs-cache-mode', 'full',
  '--vfs-cache-max-size', "$($cfg.cache_local_gb)G",
  '--vfs-cache-min-free-space', "$($cfg.disco_livre_min_gb)G",
  '--vfs-cache-max-age', '336h',
  '--vfs-write-back', '10s',
  '--dir-cache-time', '30s',
  '--poll-interval', '30s',
  '--drive-chunk-size', '64M',
  '--volname', 'PixelProcurado',
  '--log-level', 'NOTICE', '--log-file', (Join-Path $logDir 'rclone_mount.log'),
  '--no-console')
Start-Process -FilePath $rclone -ArgumentList $args -WindowStyle Hidden
for ($i = 0; $i -lt 30 -and -not (Test-Path "$letra\"); $i++) { Start-Sleep -Milliseconds 500 }
if (Test-Path "$letra\") { "montado em $letra" } else { "falhou: veja $logDir\rclone_mount.log"; exit 1 }
