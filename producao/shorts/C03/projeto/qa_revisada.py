"""Additional shot-level coverage, hashes and subtitle invariants for C03."""
import sys,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'automacao'))
from shorts_vertical import Image,ImageDraw,ImageFont,run,write_json
p=Path(__file__).resolve().parents[1]
t=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'))
movie=p/'exportacoes/Pixel_Procurado_C03_Short_1080x1920.mp4'
q=p/'projeto/qa'
assert sum(s['frames'] for s in t['shots'])==t['frames']
assert all(a['from']+a['frames']==b['from'] for a,b in zip(t['shots'],t['shots'][1:]))
assert all(0<=c['start']<c['end']<=t['duration'] for c in t['captions'])
assert all(a['end']<=b['start'] for a,b in zip(t['captions'],t['captions'][1:]))
times=[min(s['end']-.1,s['start']+.8) for s in t['shots']]
sheet=Image.new('RGB',(1080,math.ceil(len(times)/4)*520),'#151c28')
draw=ImageDraw.Draw(sheet)
for i,time in enumerate(times):
    frame=q/f'plano_{i:02}.jpg'
    run(['-ss',time,'-i',movie,'-frames:v','1','-q:v','2',frame],q/f'plano_{i:02}.log')
    im=Image.open(frame);im.thumbnail((270,480));x=i%4*270;y=i//4*520
    sheet.paste(im,(x,y));draw.text((x+10,y+490),f'{i:02} / {time:.2f}s',fill='white')
sheet.save(q/'todos_os_planos.jpg',quality=94)
hashes={str(path.relative_to(p)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [movie,p/'exportacoes/C03_legendas.srt',p/'voz/narracao.wav',p/'publicacao/capa_youtube.jpg']}
write_json(q/'checagens_adicionais.json',dict(continuous_frames=True,subtitle_bounds=True,subtitle_nonoverlap=True,min_caption_seconds=min(c['end']-c['start'] for c in t['captions']),sampled_times=times,sha256=hashes))
print('C03 additional QA passed; all 21 shots sampled',flush=True)
