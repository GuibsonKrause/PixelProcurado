"""Prepara a timeline determinística de L07 a partir do áudio e do mapa de planos."""
import json
import math
import re
import unicodedata
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'producao/L07'
W = P / 'projeto'
W.mkdir(exist_ok=True)

words = json.loads((P / 'voz/palavras_alinhadas.json').read_text(encoding='utf8'))
paragraphs = json.loads((P / 'voz/paragrafos_alinhados.json').read_text(encoding='utf8'))

videos = dict(L='Launch_Trailer', T='Trailer_1', D='Trailer_2', E='An_Extended_Look')

with wave.open(str(P / 'voz/narracao_normalizada.wav')) as voice:
    duration = voice.getnframes() / voice.getframerate()
total_frames = math.ceil(duration * 30)

def norm(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()))

shots = []
for line in (W / 'mapa_de_planos.txt').read_text(encoding='utf8').splitlines():
    if not line or line.startswith('#'):
        continue
    parts = line.split('|')
    par = int(parts[0])
    anchor = parts[1]
    asset = parts[2]
    title = parts[3] if len(parts) > 3 else ''
    
    seq = [norm(s) for s in anchor.split()]
    # Localizar âncora nas palavras do parágrafo
    found = [i for i, w in enumerate(words) if w['paragraph'] == par
             and [norm(x['word']) for x in words[i:i + len(seq)]] == seq]
    if not found:
        # Tentar correspondência aproximada se pontuação diferir
        found = [i for i, w in enumerate(words) if w['paragraph'] == par
                 and norm(w['word']) == seq[0]]
    assert len(found) >= 1, f"Âncora não encontrada: {par} | {anchor}"
    i = found[0]

    label = 'VICE CITY / RÁDIO EDITORIAL'
    credit = 'Pixel Procurado • rádio e memória'
    media, speed, offset = '', 1.0, 0.0

    if '@' in asset:
        key, offset_str, speed_str = asset.split('@')
        media = f'videosGTAVI/GTAVI_{videos[key]}.mp4'
        kind = 'video'
        graphic = 'headline' if title else ''
        layout = 'full'
        credit = f'Rockstar Games • {videos[key].replace("_", " ")} • trecho oficial'
        label = 'GTA VI / VÍDEO OFICIAL'
        offset, speed = float(offset_str), float(speed_str)
    elif asset.startswith('videosGTAVI/'):
        media = asset
        kind = 'image'
        graphic = 'headline' if title else ''
        layout = 'full'
        label = 'VICE CITY / LEONIDA'
        credit = 'Rockstar Games • captura oficial'
    else:
        kind = 'graphic'
        graphic = 'headline'
        layout = 'graphic'

    if media:
        assert (ROOT / media).is_file(), f"Mídia inexistente: {media}"

    reverse = len(shots) % 3 == 0
    shot = dict(
        anchor=anchor,
        anchorWordIndex=i,
        paragraph=par,
        fromFrame=round(words[i]['start'] * 30) if shots else 0,
        kind=kind,
        file=media,
        offset=offset,
        speed=speed,
        graphic=graphic,
        presentation=layout,
        title=title.replace('~', '\n'),
        sub='',
        label=label,
        source=credit,
        zoom=[1.035, 1.0] if reverse else [1.0, 1.045],
        focus=[0.35 if reverse else 0.65, 0.45 + 0.10 * (len(shots) % 2)],
        layout=dict(side='left', top=235, width=1600),
        editorialPurpose=title or anchor,
        animate=bool(graphic)
    )
    shots.append(shot)

# Ajustar duração de cada plano
for i, shot in enumerate(shots):
    start = shot['fromFrame']
    end = shots[i + 1]['fromFrame'] if i + 1 < len(shots) else total_frames
    assert end > start, (i, shot)
    shot.update(
        frames=end - start,
        start=start / 30.0,
        end=end / 30.0,
        animationFrames=min(20, end - start) if shot['animate'] else 1
    )

# Gerar legendas sincronizadas (frases curtas de 4 a 8 palavras para leitura limpa)
captions = []
chunk = []
for w in words:
    chunk.append(w)
    # Quebrar por pontuação ou limite de 6 palavras
    if len(chunk) >= 6 or w['word'].endswith(('.', '!', '?', ':', ';', ',')):
        text = ' '.join(x['word'] for x in chunk)
        captions.append(dict(
            start=chunk[0]['start'],
            end=chunk[-1]['end'],
            text=text
        ))
        chunk = []

if chunk:
    captions.append(dict(
        start=chunk[0]['start'],
        end=chunk[-1]['end'],
        text=' '.join(x['word'] for x in chunk)
    ))

timeline = dict(
    id='L07',
    status='final-direction',
    contractVersion='L06-1920-logical-v1',
    width=3840,
    height=2160,
    fps=30,
    duration=duration,
    frames=total_frames,
    voice='producao/L07/voz/narracao_normalizada.wav',
    shots=shots,
    captions=captions
)

(W / 'edicao_l07.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding='utf8')
print(f"Timeline montada com sucesso: {len(shots)} planos, {len(captions)} blocos de legenda, {total_frames} frames ({duration:.2f}s).")
