import sys
sys.path[:0] = ['.course-tools', '.production-tools/python']
import av
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
p=Path('producao/SERIE_AQUECIMENTO_GTA6/DIA_01_2026-11-09')
c=av.open(str(p/'exportacoes/DIA01_Amostra_4K.mp4'))
st=c.streams.video[0]
times=[0,.15,.6,1.3,2.5,5,10,12,18,22,28,31,35,39]
page=Image.new('RGB',(1920,1260),'#080A10')
draw=ImageDraw.Draw(page)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
for i,t in enumerate(times):
 c.seek(int(t*1000000),backward=True)
 frame=next(f for f in c.decode(st) if f.time>=t-.001)
 im=frame.to_image()
 if t in [1.3,18,35]:im.save(p/f'montagem/amostra_frame_{t}.png')
 im.thumbnail((480,270))
 x=(i%4)*480;y=(i//4)*315
 page.paste(im,(x,y))
 draw.text((x+12,y+275),f'{frame.time:.3f}s',font=font,fill='white')
page.save(p/'montagem/amostra_inspecao.jpg',quality=94)
print('14 quadros extraídos da amostra com PTS exato')
