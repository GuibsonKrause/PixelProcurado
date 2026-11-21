from shorts_vertical import *

out=BASE/'_acervo/inspecao';out.mkdir(exist_ok=True)
from shorts_editorial import TV
sources=[(TV,t,f'gtav-{t}') for t in (148,152,155.5,156)]
sheet=Image.new('RGB',(1200,math.ceil(len(sources)/4)*480),'#151c28');draw=ImageDraw.Draw(sheet)
for i,(p,t,name) in enumerate(sources):
    dest=out/f'{name}.jpg';run(['-ss',t,'-i',ROOT/p,'-frames:v',1,dest],out/f'{name}.log')
    im=Image.open(dest);im.thumbnail((300,440));x=i%4*300;y=i//4*480;sheet.paste(im,(x,y));draw.text((x+8,y+445),name,fill='white')
sheet.save(out/'contato.jpg')
