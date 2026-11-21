import sys
from pathlib import Path
sys.path[:0]=['.production-tools/python','.course-tools','automacao']
import av
from PIL import Image,ImageDraw
from shorts_editorial import T2,T1,TV,K,G,R,B
root=Path('.');out=root/'producao/shorts/C09/projeto';out.mkdir(exist_ok=True)
items=[]
for src,times in [(T2,[10,13,16,19,22,25,90,94,98,100,108,112,126,130,136,140,142,144]),(T1,[20,22,23,34,35,36,37]),(TV,[25,28,32,95,100,105,108,110,130,135,140,145,150])]:
 for t in times:
  with av.open(src) as c:
   c.seek(int(t*1e6));f=next(c.decode(video=0));im=f.to_image();im.thumbnail((320,180));items.append((im,Path(src).stem[:8]+' '+str(t)))
for src in [K(1),G(3),R(1),R(2),R(3),R(4),B(4)]:
 im=Image.open(src);im.thumbnail((320,180));items.append((im,Path(src).stem))
canvas=Image.new('RGB',(320*5,210*((len(items)+4)//5)),'#101018');d=ImageDraw.Draw(canvas)
for i,(im,label) in enumerate(items):x=i%5*320;y=i//5*210;canvas.paste(im,(x,y));d.text((x+4,y+182),label,fill='white')
canvas.save(out/'fontes_inspecao.jpg')
canvas=Image.new('RGB',(270*4,480),'#101018')
for i,rid in enumerate(['C09','C10','C11','C12']):
 im=Image.open(root/f'producao/shorts/{rid}/historico/antes_revisao_20261031/publicacao/capa_master.png');im.thumbnail((270,480));canvas.paste(im,(i*270,0))
canvas.save(out/'capas_anteriores_contato.jpg')
