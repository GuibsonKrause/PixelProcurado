import sys
sys.path[:0]=['.production-tools/python','.course-tools','automacao']
import av
from PIL import Image,ImageDraw
from shorts_editorial import T2
sheet=Image.new('RGB',(1600,420),'#111119');d=ImageDraw.Draw(sheet)
for i,t in enumerate([137,137.5,138,138.5,139,139.5,140,140.5,141,141.5]):
 with av.open(T2) as c:
  c.seek(int(t*1e6));f=next(f for f in c.decode(video=0) if float(f.time)>=t);im=f.to_image();im.thumbnail((320,180));x=i%5*320;y=i//5*210;sheet.paste(im,(x,y));d.text((x+5,y+182),str(t),fill='white')
sheet.save('producao/shorts/C09/projeto/agua_precisa.jpg')
