$ErrorActionPreference='Continue'
$root='C:\Users\guibson.krause\Documents\ChatGPT\GamePlay'
$D="$root\producao\SERIE_AQUECIMENTO_GTA6\DIA_07_2026-11-15"
$out="$D\audio\tts_blocos"
$log="$D\audio\gemini.log"
$env:GEMINI_API_KEY=[Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User')
$py="$root\.venv-gemini\Scripts\python.exe"
foreach($i in 1..6){
  $n='{0:D2}' -f $i
  $wav="$out\BLOCO_${n}_narracao.wav"
  if(Test-Path $wav){ "[$n] ja existe, pulando" | Add-Content $log; continue }
  "[$n] inicio $(Get-Date -Format o)" | Add-Content $log
  $p=Start-Process -FilePath $py -ArgumentList @("$root\automacao\gemini_tts.py","$out\BLOCO_${n}_GEMINI.txt","--style-file","$D\04_ESTILO_GEMINI.txt","--output-dir",$out) -NoNewWindow -PassThru -RedirectStandardOutput "$out\out_$n.txt" -RedirectStandardError "$out\err_$n.txt"
  if(-not $p.WaitForExit(330000)){ Stop-Process -Id $p.Id -Force; "[$n] TIMEOUT" | Add-Content $log; continue }
  "[$n] fim codigo $($p.ExitCode) $(Get-Date -Format o)" | Add-Content $log
  Get-Content "$out\err_$n.txt" -ErrorAction SilentlyContinue | Add-Content $log
}
"CONCLUIDO" | Add-Content $log
