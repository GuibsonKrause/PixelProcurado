"""Capas do Dia 6: montagem editorial de quadros nativos do Extended Look (sem IA). Rodar da raiz com py -3.12."""
import sys, subprocess, shutil
sys.path.insert(0,'.course-tools')
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np
D='producao/SERIE_AQUECIMENTO_GTA6/DIA_06_2026-11-14/'
R=D+'montagem/referencias/'
OUT=D+'publicacao/capas/'
M=OUT+'masters/'
def bg_cover(img,W,H,dark):
    s=max(W/img.width,H/img.height); i=img.resize((round(img.width*s),round(img.height*s)))
    l=(i.width-W)//2; t=(i.height-H)//2
    return ImageEnhance.Brightness(i.crop((l,t,l+W,t+H)).filter(ImageFilter.GaussianBlur(50))).enhance(dark)
def place(img,W,H,scale,x,y,feather=120,dark=0.5,crop=None):
    if crop: img=img.crop(crop)
    img=img.resize((round(img.width*scale),round(img.height*scale)),Image.LANCZOS)
    bg=bg_cover(img,W,H,dark).convert('RGB')
    m=np.ones((img.height,img.width),np.float32)
    ramp=lambda n:np.clip(np.arange(n)/feather,0,1)
    if x>0: m*=ramp(img.width)[None,:]
    if x+img.width<W: m*=ramp(img.width)[::-1][None,:]
    if y>0: m*=ramp(img.height)[:,None]
    if y+img.height<H: m*=ramp(img.height)[::-1][:,None]
    bg.paste(img.convert('RGB'),(x,y),Image.fromarray((m*255).astype('uint8'))); return bg
YE=(255,211,61)
A=Image.open(R+'EXT_1824.jpg').convert('RGB')
B=Image.open(R+'EXT_1604.jpg').convert('RGB')
HUD=(1660,24,1910,104)
def lupa(img):
    c=img.crop(HUD).resize((500,160),Image.LANCZOS)
    c=ImageEnhance.Brightness(c).enhance(1.15)
    out=Image.new('RGB',(512,172),YE); out.paste(c,(6,6)); return out
Bring=B.copy(); ImageDraw.Draw(Bring).rounded_rectangle((1776,56,1906,104),14,outline=YE,width=7)
# A longo / vertical
place(A,1920,1080,0.85,288,180,feather=160).save(M+'base_longo_A.png')
place(A,1080,1920,0.9,0,900,feather=200,crop=(700,0,1900,1080)).save(M+'base_vertical_A.png')
# B longo (aro nos icones) / vertical (lupa nos icones)
lb=place(B,1920,1080,0.85,288,160,feather=160,dark=0.6)
lb.paste(lupa(B).resize((420,134),Image.LANCZOS),(1450,300)); lb.save(M+'base_longo_B.png')
v=place(B,1080,1920,1080/1290,0,1010,feather=200,crop=(330,0,1620,1080))
v.paste(lupa(B),(530,790)); v.save(M+'base_vertical_B.png')
C='py','-3.12','.agents/skills/pixel-procurado-thumbnails/scripts/compose_thumbnail.py'
for k,(l1,l2) in {'A':('TEM UM','STREAMER'),'B':('O ÍCONE','SUMIU')}.items():
    for fmt,nome in (('long','longo'),('short','vertical')):
        od=M+f'out_{nome}_{k}'
        subprocess.run([*C,'--base',M+f'base_{nome}_{k}.png','--output-dir',od,'--line1',l1,'--line2',l2,'--format',fmt],check=True)
        shutil.copy(od+'/capa_youtube.jpg',OUT+f'capa_{nome}_{k}.jpg')
        shutil.copy(od+'/capa_master.png',M+f'capa_{nome}_{k}_master.png')
# prancha 320
sh=Image.new('RGB',(1340,600),'#222'); x=10
for k in 'AB':
    sh.paste(Image.open(OUT+f'capa_longo_{k}.jpg').resize((320,180)),(10+(0 if k=='A' else 330),10))
    sh.paste(Image.open(OUT+f'capa_vertical_{k}.jpg').resize((320,569)).crop((0,0,320,400)) if False else Image.open(OUT+f'capa_vertical_{k}.jpg').resize((180,320)),(670+(0 if k=='A' else 190),10))
sh.save(OUT+'prancha_320.jpg')
