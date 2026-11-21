# Espelha as skills pixel-procurado-* de <raiz>\.agents\skills (fonte canonica) para
#   %USERPROFILE%\.codex\skills  e  %USERPROFILE%\.gemini\config\skills
# e garante as junctions <raiz>\.claude\skills\<skill> -> .agents\skills\<skill>.
# Nunca toca em outras skills dos destinos (impeccable, ponytail, .system...). Arquivos alterados/removidos
# nos destinos vao antes para %LOCALAPPDATA%\PixelProcurado\backup_skills\<timestamp>\.
#
#   .\automacao\sincronizar_skills.ps1             # sincroniza
#   .\automacao\sincronizar_skills.ps1 -Verificar  # so reporta; exit 1 se houver diferenca (-WhatIf idem)

param([switch]$Verificar, [switch]$WhatIf)

$ErrorActionPreference = 'Stop'
$somenteVerificar = $Verificar -or $WhatIf
$root = Split-Path -Parent $PSScriptRoot
$origem = Join-Path $root '.agents\skills'
$destinos = @{
    codex  = Join-Path $env:USERPROFILE '.codex\skills'
    gemini = Join-Path $env:USERPROFILE '.gemini\config\skills'
}
$junctions = Join-Path $root '.claude\skills'
$backup = Join-Path $env:LOCALAPPDATA ('PixelProcurado\backup_skills\' + (Get-Date -Format 'yyyyMMdd_HHmmss'))

$skills = Get-ChildItem -LiteralPath $origem -Directory | Where-Object { $_.Name -like 'pixel-procurado-*' }
if (-not $skills) { throw "Nenhuma skill pixel-procurado-* em $origem" }

function Get-Arquivos($pasta) {
    # mapa caminho-relativo -> hash; ignora __pycache__
    $mapa = @{}
    if (-not (Test-Path -LiteralPath $pasta)) { return $mapa }
    Push-Location -LiteralPath $pasta   # caminhos relativos via Resolve-Path -Relative (imune a nomes 8.3/longos)
    try {
        Get-ChildItem -LiteralPath . -Recurse -File -Force |
            Where-Object { $_.FullName -notmatch '[\\/]__pycache__[\\/]' } |
            ForEach-Object { $mapa[(Resolve-Path -LiteralPath $_.FullName -Relative).Substring(2)] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
    }
    finally { Pop-Location }
    return $mapa
}

$diferencas = 0
foreach ($nomeDestino in $destinos.Keys) {
    foreach ($skill in $skills) {
        $dst = Join-Path $destinos[$nomeDestino] $skill.Name
        $a = Get-Arquivos $skill.FullName
        $b = Get-Arquivos $dst
        $copiar = @($a.Keys | Where-Object { $b[$_] -ne $a[$_] })
        $remover = @($b.Keys | Where-Object { -not $a.ContainsKey($_) })
        if (-not $copiar -and -not $remover) { continue }
        $diferencas += $copiar.Count + $remover.Count
        foreach ($f in $copiar) { Write-Host ("[{0}] {1}: {2} {3}" -f $nomeDestino, $skill.Name, $(if ($b.ContainsKey($f)) { 'alterado' } else { 'novo' }), $f) }
        foreach ($f in $remover) { Write-Host ("[{0}] {1}: sobrando no destino {2}" -f $nomeDestino, $skill.Name, $f) }
        if ($somenteVerificar) { continue }
        foreach ($f in @($copiar | Where-Object { $b.ContainsKey($_) }) + $remover) {
            $bk = Join-Path $backup (Join-Path $nomeDestino (Join-Path $skill.Name $f))
            New-Item -ItemType Directory -Force -Path (Split-Path $bk) | Out-Null
            Copy-Item -LiteralPath (Join-Path $dst $f) -Destination $bk
        }
        foreach ($f in $copiar) {
            $alvo = Join-Path $dst $f
            New-Item -ItemType Directory -Force -Path (Split-Path $alvo) | Out-Null
            Copy-Item -LiteralPath (Join-Path $skill.FullName $f) -Destination $alvo -Force
        }
        foreach ($f in $remover) { Remove-Item -LiteralPath (Join-Path $dst $f) -Force }
    }
}

# Junctions do Claude Code
New-Item -ItemType Directory -Force -Path $junctions | Out-Null
foreach ($skill in $skills) {
    $j = Join-Path $junctions $skill.Name
    $item = Get-Item -LiteralPath $j -Force -ErrorAction SilentlyContinue
    if ($item -and $item.LinkType -eq 'Junction' -and ($item.Target -replace '\\$', '') -eq $skill.FullName) { continue }
    $diferencas++
    if ($item) { Write-Host "[claude] $($skill.Name): existe mas nao e a junction esperada (resolver manualmente): $j"; continue }
    Write-Host "[claude] $($skill.Name): junction ausente"
    if (-not $somenteVerificar) { New-Item -ItemType Junction -Path $j -Target $skill.FullName | Out-Null }
}

if ($diferencas -eq 0) { Write-Host "Nada a fazer: $($skills.Count) skills identicas em codex, gemini e junctions do claude."; exit 0 }
if ($somenteVerificar) { Write-Host "$diferencas diferenca(s). Rode sem -Verificar para sincronizar."; exit 1 }
Write-Host "$diferencas item(ns) sincronizado(s). Backup dos arquivos substituidos: $backup"
exit 0
