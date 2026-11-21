# Rotina diaria (Agendador de Tarefas "PixelProcurado\Armazenamento diario", 05:00):
# garante a montagem do Drive e roda armazenamento.py automatico --executar (arquiva + cotas).
$raiz = Split-Path $PSScriptRoot -Parent
Set-Location $raiz
$log = Join-Path $env:LOCALAPPDATA 'PixelProcurado\armazenamento_diario.log'
"`n===== $(Get-Date -Format s)" | Out-File $log -Append -Encoding utf8
& (Join-Path $PSScriptRoot 'montar_drive.ps1') *>> $log
py -3.12 automacao/armazenamento.py automatico --executar *>> $log
