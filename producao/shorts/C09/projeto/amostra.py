import sys
sys.path[:0]=['.production-tools/python','.course-tools']
import av
from PIL import Image,ImageDraw
from pathlib import Path
out=Path('producao/shorts/C09/projeto');ims=[]
for i in [0,2,8]:
 p=out/f'render/{i:03}.mp4'
 with av.open(str(p)) as c:
  c.seek(1000000);f=next(f for f in c.decode(video=0) if float(f.time)>=min(1.0,float(c.duration/1e6)-.05));im=f.to_image();im.thumbnail((360,640));ims.append(im)
sheet=Image.new('RGB',(1080,640))
for i,im in enumerate(ims):sheet.paste(im,(i*360,0))
sheet.save(out/'amostra_previa.jpg')

