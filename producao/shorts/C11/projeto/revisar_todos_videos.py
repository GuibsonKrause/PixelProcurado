import sys,json
from pathlib import Path
sys.path[:0]=['.production-tools/python','.course-tools']
import av
from PIL import Image,ImageDraw
for rid in ['C11']:
 p=Path('producao/shorts')/rid;data=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'));movie=p/f'exportacoes/Pixel_Procurado_{rid}_Short_1080x1920.mp4';shots=[s for s in data['shots'] if s['file'].endswith('.mp4')];items=[]
 for s in shots:
  for t in [s['start']+.3,min(s['end']-.1,s['start']+min(s.get('motion',999),s['frames']/30)-.1)]:
   with av.open(str(movie)) as c:
    c.seek(int(t*1e6));f=next(f for f in c.decode(video=0) if float(f.time)>=t);im=f.to_image();im.thumbnail((216,384));items.append((im,f"{s['index']} / {t:.2f}s"))
 sheet=Image.new('RGB',(216*6,410*((len(items)+5)//6)),'#111119');d=ImageDraw.Draw(sheet)
 for i,(im,label) in enumerate(items):x=i%6*216;y=i//6*410;sheet.paste(im,(x,y));d.text((x+4,y+386),label,fill='white')
 sheet.save(p/'projeto/qa/todos_planos_video.jpg')

