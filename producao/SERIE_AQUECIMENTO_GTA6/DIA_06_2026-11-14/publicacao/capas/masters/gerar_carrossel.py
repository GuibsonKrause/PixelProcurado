import sys
sys.path.insert(0,'.course-tools')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D='producao/SERIE_AQUECIMENTO_GTA6/DIA_06_2026-11-14/'
R=D+'montagem/referencias/'
IMP=ImageFont.truetype('C:/Windows/Fonts/impact.ttf',92)
LB=ImageFont.truetype('C:/Windows/Fonts/bahnschrift.ttf',38)
TX=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',36)
import textwrap
WH,YE='#F8FAFC','#FFD33D'
slides=[
 (R+'EXT_1824.jpg',1.0,'TEM UM','STREAMER','Porta-malas do minuto 18: sem malote, sem fuzil. Tem um streamer, com live de 51 mil.',None),
 (R+'EXT_1604.jpg',1.6,'O ÍCONE','SUMIU','15:57: a Lucia larga o sedã e o ícone do carro some. O que cada ícone significa é hipótese.',None),
 (R+'EXT_2024.jpg',1.0,'2 TIPOS','DE RACHA','17:42: circuito com volta. 20:21: rua com progresso em %. Polícia e aposta: não aparecem.',None),
 ('videosGTAVI/GTAVI_Ultimate_Edition_Benefits/ULTIMATE_EDITION_RIDEOUT_CUSTOMS_03.jpg',1.0,'OFICINA','SÓ EM FOTO','Nas cenas de carro não achei oficina por dentro. É imagem da Ultimate Edition.',None),
]
for n,(src,br,l1,l2,sub,_) in enumerate(slides,1):
    im=Image.open(src).convert('RGB')
    if br!=1: im=ImageEnhance.Brightness(im).enhance(br)
    c=Image.new('RGB',(1080,1350),'#080A10'); d=ImageDraw.Draw(c)
    h=825; w=1080; s=max(w/im.width,h/im.height)
    bg=im.resize((round(im.width*s),round(im.height*s))); l=(bg.width-w)//2; t=(bg.height-h)//2
    bg=bg.crop((l,t,l+w,t+h)).filter(ImageFilter.GaussianBlur(30)); bg=ImageEnhance.Brightness(bg).enhance(.6)
    c.paste(bg,(0,130))
    fh=round(im.height*w/im.width); fi=im.resize((w,fh),Image.LANCZOS)
    if fh>h: fi=fi.crop((0,(fh-h)//2,w,(fh-h)//2+h)); fh=h
    c.paste(fi,(0,130+(h-fh)//2))
    d.text((60,52),'PIXEL / PROCURADO',font=LB,fill=YE); d.text((1020,52),f'{n}/4',font=LB,fill=WH,anchor='ra')
    d.rectangle((60,978,193,988),fill=YE)
    d.text((60,1000),l1,font=IMP,fill=WH); d.text((60,1092),l2,font=IMP,fill=YE)
    d.multiline_text((60,1205),textwrap.fill(sub,46),font=TX,fill=WH,spacing=6)
    c.save(D+f'publicacao/carrossel/0{n}.jpg',quality=92)
sh=Image.new('RGB',(1320,420),'#222')
for n in range(4): sh.paste(Image.open(D+f'publicacao/carrossel/0{n+1}.jpg').resize((320,400)),(10+n*330,10))
sh.save(D+'publicacao/carrossel/prancha.jpg')
