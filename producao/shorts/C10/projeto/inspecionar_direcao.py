import sys
sys.path[:0]=['.production-tools/python','.course-tools','automacao']
from pathlib import Path
import av
from PIL import Image,ImageDraw
from shorts_editorial import TV,T2
items=[]
for src,times in [(TV,[36,40,44,48,52,56,60,64,68,144,146,148,150,152,154,156,158,160,162,164,166,168]),(T2,[106,107,108,109,110])]:
 for t in times:
  with av.open(src) as c:
   c.seek(int(t*1e6));f=next(c.decode(video=0));im=f.to_image();im.thumbnail((320,180));items.append((im,str(t)+(' T2' if src==T2 else ' V')))
sheet=Image.new('RGB',(1600,210*((len(items)+4)//5)),'#111119');d=ImageDraw.Draw(sheet)
for i,(im,t) in enumerate(items):x=i%5*320;y=i//5*210;sheet.paste(im,(x,y));d.text((x+5,y+182),t,fill='white')
sheet.save('producao/shorts/C10/projeto/fontes_direcao.jpg')
