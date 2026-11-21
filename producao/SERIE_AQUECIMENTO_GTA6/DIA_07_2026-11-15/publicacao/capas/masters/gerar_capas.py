"""Capas do Dia 7: quadros nativos 4K do Extended Look (sem IA, R$0). Rodar da raiz com py -3.12."""
import sys, subprocess, shutil
sys.path.insert(0,'.course-tools')
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np
D='producao/SERIE_AQUECIMENTO_GTA6/DIA_07_2026-11-15/'
R=D+'montagem/referencias/'; OUT=D+'publicacao/capas/'; M=OUT+'masters/'
YE=(255,212,59)
def bg_cover(img,W,H,dark,blur):
    s=max(W/img.width,H/img.height); i=img.resize((round(img.width*s),round(img.height*s)))
    l=(i.width-W)//2; t=(i.height-H)//2
    i=i.crop((l,t,l+W,t+H))
    if blur: i=i.filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Brightness(i).enhance(dark).convert('RGB')
def place(img,W,H,scale,x,y,feather=120,dark=0.5,crop=None,blur=50,bg=None):
    if crop: img=img.crop(crop)
    img=img.resize((round(img.width*scale),round(img.height*scale)),Image.LANCZOS)
    base=bg if bg is not None else bg_cover(img,W,H,dark,blur)
    m=np.ones((img.height,img.width),np.float32)
    ramp=lambda n:np.clip(np.arange(n)/feather,0,1)
    if x>0: m*=ramp(img.width)[None,:]
    if x+img.width<W: m*=ramp(img.width)[::-1][None,:]
    if y>0: m*=ramp(img.height)[:,None]
    if y+img.height<H: m*=ramp(img.height)[::-1][:,None]
    base.paste(img.convert('RGB'),(x,y),Image.fromarray((m*255).astype('uint8'))); return base
A=Image.open(R+'EXT_0643.jpg').convert('RGB')
ImageDraw.Draw(A).rounded_rectangle((1140,930,2340,1610),30,outline=YE,width=18)  # tenis + cadarco
B=Image.open(R+'EXT_1857.jpg').convert('RGB')
HUDB=B.crop((3250,1870,3835,2145))
def hud(w):
    h=round(w*HUDB.height/HUDB.width)
    c=HUDB.resize((w,h),Image.LANCZOS); c=ImageEnhance.Brightness(c).enhance(1.25)
    o=Image.new('RGB',(w+16,h+16),YE); o.paste(c,(8,8)); return o
place(A,1920,1080,0.55,300,0,feather=170,crop=(700,100,3840,2060)).save(M+'base_longo_A.png')
place(A,1080,1920,0.5625,0,1000,feather=200,crop=(730,192,2650,1728)).save(M+'base_vertical_A.png')
bgl=bg_cover(B,1920,1080,0.6,6); bgl.paste(hud(1380),(480,330)); bgl.save(M+'base_longo_B.png')
bgv=bg_cover(B.crop((900,0,3000,2160)),1080,1920,0.6,6); bgv.paste(hud(1000),(40,1000)); bgv.save(M+'base_vertical_B.png')
C='py','-3.12','.agents/skills/pixel-procurado-thumbnails/scripts/compose_thumbnail.py'
for k,(l1,l2) in {'A':('PAUSA','AQUI'),'B':('CASAL','BRAVO?')}.items():
    for fmt,nome in (('long','longo'),('short','vertical')):
        od=M+f'out_{nome}_{k}'
        subprocess.run([*C,'--base',M+f'base_{nome}_{k}.png','--output-dir',od,'--line1',l1,'--line2',l2,'--format',fmt],check=True)
        shutil.copy(od+'/capa_youtube.jpg',OUT+f'capa_{nome}_{k}.jpg'); shutil.copy(od+'/capa_master.png',M+f'capa_{nome}_{k}_master.png')
sh=Image.new('RGB',(1340,350),'#222')
for k in 'AB':
    o=0 if k=='A' else 330
    sh.paste(Image.open(OUT+f'capa_longo_{k}.jpg').resize((320,180)),(10+o,10))
    sh.paste(Image.open(OUT+f'capa_vertical_{k}.jpg').resize((180,320)),(670+(0 if k=='A' else 190),10))
sh.save(OUT+'prancha_320.jpg')
