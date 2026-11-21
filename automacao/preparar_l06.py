"""Edição de L06 ancorada na fala e nas fontes oficiais de cada região."""
import json
import math
import re
import unicodedata
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'producao/L06'
W = P / 'projeto'
W.mkdir(exist_ok=True)
words = json.loads((P / 'voz/palavras_alinhadas.json').read_text(encoding='utf8'))
paragraphs = json.loads((P / 'voz/paragrafos_alinhados.json').read_text(encoding='utf8'))
regions = dict(K='Leonida Keys', G='Grassrivers', V='Vice City', P='Port Gellhorn',
               A='Ambrosia', M='Mount Kalaga National Park')
videos = dict(L='Launch_Trailer', T='Trailer_1', D='Trailer_2', E='An_Extended_Look')
with wave.open(str(P / 'voz/narracao_normalizada.wav')) as voice:
    duration = voice.getnframes() / voice.getframerate()
total = math.ceil(duration * 30)


def norm(s):
    return re.sub('[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()))


shots = []
for line in (W / 'mapa_de_planos.txt').read_text(encoding='utf8').splitlines():
    if not line or line.startswith('#'):
        continue
    par, anchor, asset, title = line.split('|')
    par = int(par)
    seq = [norm(s) for s in anchor.split()]
    found = [i for i, w in enumerate(words) if w['paragraph'] == par
             and [norm(x['word']) for x in words[i:i+len(seq)]] == seq]
    assert len(found) == 1, (par, anchor, found)
    i = found[0]
    label = 'LEONIDA / LEITURA EDITORIAL'
    credit = 'Pixel Procurado • interpretação das imagens'
    media, speed, offset = '', 1, 0
    if asset == '-':
        kind, graphic, layout = 'graphic', 'headline', 'graphic'
    elif '@' in asset:
        key, offset, speed = asset.split('@')
        media = f'videosGTAVI/GTAVI_{videos[key]}.mp4'
        kind, graphic, layout = 'video', 'headline' if title else '', 'full'
        credit = f'Rockstar Games • {videos[key].replace("_", " ")} • trecho oficial'
        label = 'GTA VI / VÍDEO OFICIAL'
        offset, speed = float(offset), float(speed)
    else:
        key, number = asset[0], int(asset[1:])
        region = regions[key]
        media = f'videosGTAVI/GTAVI_Screenshots/Places/{region}/{region.replace(" ", "_")}_{number:02}.jpg'
        kind, graphic, layout = 'image', 'headline' if title else '', 'full'
        label = region.upper()
        credit = f'Rockstar Games • {region} {number:02} • captura oficial'
    if media:
        assert (ROOT / media).is_file(), media
    reverse = len(shots) % 3 == 0
    shot = dict(anchor=anchor, anchorWordIndex=i, paragraph=par,
                fromFrame=round(words[i]['start']*30) if shots else 0,
                kind=kind, file=media, offset=offset, speed=speed, graphic=graphic,
                presentation=layout, title=title.replace('~','\n'), sub='',
                label=label, source=credit, zoom=[1.035, 1] if reverse else [1, 1.045],
                focus=[.35 if reverse else .65, .45 + .10*(len(shots)%2)],
                layout=dict(side='left', top=235, width=1600),
                editorialPurpose=title or anchor, animate=bool(graphic))
    if kind == 'image' and asset in {'K2','G2','V6','P1','M6'}:
        shot.update(zoom=[1,1.018], focus=[.50,.50])
    shots.append(shot)

for i, shot in enumerate(shots):
    start = shot['fromFrame']
    end = shots[i+1]['fromFrame'] if i+1 < len(shots) else total
    assert end > start, (i, shot)
    shot.update(frames=end-start, start=start/30, end=end/30,
                animationFrames=min(20, end-start) if shot['animate'] else 1)

caps, batch = [], []
for i, w in enumerate(words):
    batch.append(w)
    spoken = ' '.join(x['word'] for x in batch)
    last = i+1 == len(words)
    if last or len(batch) >= 8 or len(spoken) >= 46 or (
        len(batch) >= 3 and w['word'].endswith(('.', '?', '!', ';', ':'))
    ):
        caps.append(dict(start=batch[0]['start'], end=min(duration,w['end']+.12), text=spoken))
        batch = []
if len(caps[-1]['text'].split()) < 3:
    tail = caps.pop()
    caps[-1]['text'] += ' ' + tail['text']
    caps[-1]['end'] = tail['end']
for a, b in zip(caps, caps[1:]):
    a['end'] = min(max(a['end'], a['start']+.85), b['start'])
data = dict(episode='L06', title='GTA 6 além de Vice City: seis lugares, seis climas',
            duration=duration, frames=total, fps=30, width=3840, height=2160,
            voice='producao/L06/voz/narracao_normalizada.wav', paragraphs=paragraphs,
            contractVersion='L06-1920-logical-v1', status='final-direction',
            shots=shots, captions=caps)
(W / 'edicao_l06.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
print(f'{len(shots)} planos, {len(caps)} legendas, {duration:.3f} s')
