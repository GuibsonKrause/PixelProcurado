"""Inventory and consistency checks for the completed delivery."""
import hashlib,json,csv
from shorts_vertical import ROOT,BASE,PLANS,META,Image,ImageDraw,ImageFont,write_json
from shorts_publicacao import make

rows=[];font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',21)
sheet=Image.new('RGB',(4*270,4*525),'#101824');draw=ImageDraw.Draw(sheet)
for i,rid in enumerate(PLANS):
    p=BASE/rid;data=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'))
    qa=json.loads((p/'projeto/qa/validacao_final.json').read_text(encoding='utf8'))
    movie=p/'exportacoes'/f'Pixel_Procurado_{rid}_Short_1080x1920.mp4'
    for file in [movie,p/'exportacoes'/f'{rid}_legendas.srt',p/'publicacao/capa_youtube.jpg',p/'publicacao/capa_master.png',p/'voz/narracao.wav']:
        assert file.is_file() and file.stat().st_size>0,file
    assert qa['video_frames']==data['frames']
    assert abs(qa['video_duration']-data['duration'])<.034
    assert not (p/'projeto/qa/decodificacao_integral.txt').read_text().strip()
    assert float(qa['loudness_aac']['input_tp'])<0
    assert min(c['correlation'] for c in qa['audio_correlations'])>.97
    original=ROOT/'producao/cortes/audio_gemini/normalizados'/f'{rid}_narracao_normalizada.wav'
    assert hashlib.sha256(original.read_bytes()).digest()==hashlib.sha256((p/'voz/narracao.wav').read_bytes()).digest()
    cap=Image.open(p/'publicacao/capa_youtube.jpg');assert cap.size==(1080,1920)
    assert (p/'publicacao/capa_youtube.jpg').stat().st_size<2_000_000
    cap.thumbnail((270,480));x=i%4*270;y=i//4*525;sheet.paste(cap,(x,y));draw.text((x+10,y+490),f'{rid}  /  {data["duration"]:.2f}s',font=font,fill='white')
    row=dict(id=rid,duration=qa['video_duration'],frames=qa['video_frames'],size_mib=round(movie.stat().st_size/1024**2,2),lufs=float(qa['loudness_aac']['input_i']),true_peak=float(qa['loudness_aac']['input_tp']),audio_correlation_min=min(c['correlation'] for c in qa['audio_correlations']),sha256=hashlib.sha256(movie.read_bytes()).hexdigest())
    rows.append(row);make(rid)
    (p/'00_LEIA_ME.md').write_text(f'# {rid} — {META[rid][0]}\n\n[Assistir ao vídeo](exportacoes/{movie.name})\n\n[Abrir o guia e os textos de publicação](publicacao/00_GUIA_DE_PUBLICACAO.md)\n\n[Ver direção e tempos de edição](projeto/DIRECAO.md)\n\n[Consultar a validação técnica](projeto/qa/validacao_final.json)\n',encoding='utf8')
sheet.save(BASE/'00_CAPAS_DOS_SHORTS.jpg',quality=92)
write_json(BASE/'RELATORIO_TECNICO.json',rows)
lines=['# Entrega dos Shorts','',f'{len(rows)} vídeos finais. Duração total dos arquivos: {sum(r["duration"] for r in rows):.2f}s. Volume total dos MP4s: {sum(r["size_mib"] for r in rows):.1f} MiB.','', '## O que foi validado','', '- Todos os MP4s decodificados integralmente sem erro.','- Vídeo H.264 em 1080×1920, 30 fps; áudio AAC em 48 kHz.','- Duração do stream de vídeo alinhada à narração, com diferença inferior a um quadro.','- As 14 cópias WAV são idênticas às narrações normalizadas aprovadas, verificadas por SHA-256.','- Áudio exportado comparado à voz original em cinco posições por vídeo; nenhuma faixa de trailer ou trilha comercial acrescentada.','- Legendas geradas com tempos por palavra, correções contextuais registradas em cada projeto.','- Capas JPG/PNG em 1080×1920; JPGs abaixo de 2 MB.','- Aberturas, regiões intermediárias e finais examinados em pranchas visuais. O acervo usado foi revisado em pranchas de imagens e amostras dos trechos de vídeo.','', 'A verificação de áudio foi técnica e por transcrição; não equivale a uma audição humana integral ou a uma certificação subjetiva de dicção. Os relatórios prévios da geração Gemini continuam em producao/cortes/audio_gemini.','', '| ID | Duração | Quadros | MiB | LUFS integrados | Pico real dBTP | Correlação mínima |','|---|---|---|---|---|---|---|']
for r in rows:lines.append(f"| {r['id']} | {r['duration']:.3f}s | {r['frames']} | {r['size_mib']:.1f} | {r['lufs']:.2f} | {r['true_peak']:.2f} | {r['audio_correlation_min']:.5f} |")
lines+=['','## Reedição','', 'A narração foi mantida integral. A montagem é híbrida: gráficos e entradas animadas do Remotion, composição e legendas em FFmpeg, exportação H.264/AAC. Onde um trecho de vídeo é mais curto que a fala, o último quadro é sustentado; esses casos estão identificados nos créditos. Não se transformou um screenshot em suposto gameplay.','', 'Para mudar as escolhas de imagem, ajuste automacao/shorts_editorial.py. A composição gráfica fica em remotion/src/shorts-overlays.tsx. Os roteiros/tempos particulares estão nas pastas voz e projeto de cada Short. Os arquivos intermediários foram preservados.','', 'Na raiz do projeto, com o ambiente local existente:', '', '```powershell', r'.\.venv-gemini\Scripts\python.exe automacao/shorts_vertical.py prepare C08', r'.\.venv-gemini\Scripts\python.exe automacao/shorts_batch.py C08', r'.\.venv-gemini\Scripts\python.exe automacao/shorts_publicacao.py', '```','', 'Depois de alterações, repetir a inspeção visual e a validação antes de substituir o arquivo destinado ao upload. Não renumerar ou apagar acervo de outros episódios.','', '## Publicação','', 'Os textos prontos, títulos alternativos, crédito de cada mídia e instruções do Studio ficam em publicacao. O registro de postagem está em CONTROLE_DE_PUBLICACAO.csv. Nenhum vídeo foi enviado ao YouTube.','', 'A informação técnica do C05 foi reconfirmada na descrição pública do Trailer 2 no YouTube. O trecho pertinente e o método de consulta ficam em C05/projeto/fonte_descricao_trailer2.txt.']
(BASE/'00_RELATORIO_DE_ENTREGA.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(f'COMPLETE: {len(rows)} verified Shorts, {sum(r["size_mib"] for r in rows):.1f} MiB')
