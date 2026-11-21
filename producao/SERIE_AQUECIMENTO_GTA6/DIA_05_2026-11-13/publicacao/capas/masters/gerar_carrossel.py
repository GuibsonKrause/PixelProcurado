import sys
sys.path.insert(0,'.course-tools')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D='producao/SERIE_AQUECIMENTO_GTA6/DIA_05_2026-11-13/'
R=D+'montagem/referencias/'
IMP=ImageFont.truetype('C:/Windows/Fonts/impact.ttf',92)
LB=ImageFont.truetype('C:/Windows/Fonts/bahnschrift.ttf',38)
TX=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',36)
import textwrap
WH,YE='#F8FAFC','#FFD33D'
slides=[
 ('videosGTAVI/GTAVI_Screenshots/People/Jason and Lucia/Jason_and_Lucia_02.jpg',1.0,'CRIME','A DOIS','Jason e Lucia dividem o plano no GTA 6.',None),
 (R+'hud_0706.jpg',1.6,'L2 NÃO TROCA','DE PERSONAGEM','"Lucia [L2]" aparece no HUD, mas o Jason segue no controle.',None),
 (R+'supino_L2R2.jpg',1.0,'TREINO COM','L2 + R2','Um ícone por mão no supino. Medidor de força: não apareceu.',None),
 (R+'msg_2349.jpg',1.9,'ELA','AVISOU','Mensagem da Lucia: "guys everywhere". Detalhes no vídeo.',None),
]
for n,(src,br,l1,l2,sub,_) in enumerate(slides,1):
    im=Image.open(src).convert('RGB')
    if 'hud_0706' in src: im=im.crop((1920,700,3840,2160))
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
