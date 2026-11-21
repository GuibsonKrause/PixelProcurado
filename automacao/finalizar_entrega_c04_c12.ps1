$ErrorActionPreference = 'Stop'
$rootPath = Split-Path -Parent $PSScriptRoot
$basePath = Join-Path $rootPath 'producao/shorts'
$reviewPath = Join-Path $basePath 'REVISAO_INDEPENDENTE_C04_C12.md'
if (-not (Test-Path -LiteralPath $reviewPath)) { throw 'Revisão independente ainda não foi entregue.' }
$rows = @()
foreach ($n in 4..12) {
    $id = 'C{0:00}' -f $n
    $folder = Join-Path $basePath $id
    $videoRelative = "exportacoes/Pixel_Procurado_${id}_Short_1080x1920.mp4"
    $required = @($videoRelative,"exportacoes/${id}_legendas.srt",'publicacao/capa_youtube.jpg','publicacao/capa_master.png','publicacao/01_TITULO.txt','publicacao/02_DESCRICAO.txt','publicacao/04_TAGS.txt','projeto/timeline.json','projeto/qa/validacao_final.json')
    foreach ($relative in $required) {
        $file = Get-Item -LiteralPath (Join-Path $folder $relative)
        if ($file.Length -eq 0) { throw "Arquivo vazio: $id/$relative" }
    }
    $qa = Get-Content -LiteralPath (Join-Path $folder 'projeto/qa/validacao_final.json') -Raw | ConvertFrom-Json
    if ($qa.width -ne 1080 -or $qa.height -ne 1920 -or $qa.fps -ne 30) { throw "Formato incorreto: $id" }
    $hash = (Get-FileHash -LiteralPath (Join-Path $folder $videoRelative) -Algorithm SHA256).Hash.ToLower()
    $title = (Get-Content -LiteralPath (Join-Path $folder 'publicacao/01_TITULO.txt') -Raw).Trim()
    $checkpoint = Get-Content -LiteralPath (Join-Path $folder 'producao.json') -Raw | ConvertFrom-Json
    $checkpoint.estado = 'validado_pronto_para_publicacao_manual'
    $checkpoint.etapa_atual = 'concluido'
    $checkpoint | Add-Member -NotePropertyName artefatos -NotePropertyValue @{
        mp4="producao/shorts/$id/$videoRelative";srt="producao/shorts/$id/exportacoes/${id}_legendas.srt";
        thumbnail="producao/shorts/$id/publicacao/capa_youtube.jpg";descricao="producao/shorts/$id/publicacao/02_DESCRICAO.txt";
        timeline="producao/shorts/$id/projeto/timeline.json";qa="producao/shorts/$id/projeto/qa/validacao_final.json"
    } -Force
    $checkpoint | Add-Member -NotePropertyName validacao_final -NotePropertyValue @{
        duracao=$qa.video_duration;frames=$qa.video_frames;sha256=$hash;revisao_independente='PASS por amostragem';
        relatorio='producao/shorts/REVISAO_INDEPENDENTE_C04_C12.md';upload_realizado=$false;agendamento_realizado=$false
    } -Force
    $checkpoint | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath (Join-Path $folder 'producao.json') -Encoding utf8
    $duration = [math]::Round($qa.video_duration,2)
    $rows += "| $id | $title | $duration s | [Vídeo]($id/$videoRelative) | [Capa]($id/publicacao/capa_youtube.jpg) | [Descrição]($id/publicacao/02_DESCRICAO.txt) | [SRT]($id/exportacoes/${id}_legendas.srt) |"
}
$content = @'
# Shorts C04–C12 — prontos para publicação manual

Nove produções com os roteiros revisados, narração nova, vídeo vertical 1080×1920 a 30 fps, legendas, thumbnail e textos de publicação. Cada linha abre os arquivos da pasta individual. Não houve upload nem agendamento deste lote.

| ID | Título | Duração | MP4 | Thumbnail | Descrição | Legendas |
|---|---|---:|---|---|---|---|
'@
$content += "`n" + ($rows -join "`n")
$content += "`n`n[Revisão independente do lote](REVISAO_INDEPENDENTE_C04_C12.md). Cada pasta contém também título, tags, comentário sugerido, fontes, áudio, timeline e checkpoint de produção.`n`nForam priorizados clipes correspondentes à fala. Nas análises de fotografias específicas, elas permanecem na tela com movimento e destaques. As capas anteriores coerentes foram inspecionadas e reaproveitadas. Versões antigas estão preservadas em históricos individuais.`n`nValidação: decodificação integral, metadados, sincronismo e comparação de áudio; revisão visual independente por amostragem. Não equivale a escuta subjetiva integral. As limitações de pronúncia reconhecida estão nos relatórios individuais e na revisão do lote.`n"
$content | Set-Content -LiteralPath (Join-Path $basePath 'ENTREGA_C04_C12.md') -Encoding utf8
Write-Output '9 produções verificadas; checkpoints e índice final atualizados.'
