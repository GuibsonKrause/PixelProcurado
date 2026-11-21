import sys
sys.path.insert(0,'.course-tools')
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
D='producao/SERIE_AQUECIMENTO_GTA6/DIA_05_2026-11-13/'
OUT=D+'publicacao/capas/masters/'
ART='videosGTAVI/GTAVI_Artwork_Wallpapers/Jason_and_Lucia_02/Jason_and_Lucia_02_'
def bg_cover(img,W,H,dark=0.55):
    s=max(W/img.width,H/img.height); i=img.resize((round(img.width*s),round(img.height*s)))
    l=(i.width-W)//2; t=(i.height-H)//2
    i=i.crop((l,t,l+W,t+H)).filter(ImageFilter.GaussianBlur(50))
    return ImageEnhance.Brightness(i).enhance(dark)
def place(img,W,H,scale,x,y,feather=90,dark=0.55,crop=None):
    if crop: img=img.crop(crop)
    img=img.resize((round(img.width*scale),round(img.height*scale)),Image.LANCZOS)
    bg=bg_cover(img,W,H,dark).convert('RGB')
    m=np.ones((img.height,img.width),np.float32)
    ramp=lambda n:np.clip(np.arange(n)/feather,0,1)
    if x>0: m*=ramp(img.width)[None,:]
    if x+img.width<W: m*=ramp(img.width)[::-1][None,:]
    if y>0: m*=ramp(img.height)[:,None]
    if y+img.height<H: m*=ramp(img.height)[::-1][:,None]
    mask=Image.fromarray((m*255).astype('uint8'))
    bg.paste(img.convert('RGB'),(x,y),mask); return bg
A=Image.open('videosGTAVI/GTAVI_Screenshots/People/Jason and Lucia/Jason_and_Lucia_02.jpg').convert('RGB')
P=Image.open(ART+'portrait.jpg').convert('RGB')
B=Image.open(D+'montagem/referencias/msg_2349.jpg').convert('RGB')
B=ImageEnhance.Contrast(ImageEnhance.Brightness(B).enhance(1.9)).enhance(1.1)
# A longo: arte oficial deslocada p/ direita
place(A,1920,1080,1920/A.width,300,0,feather=200,dark=0.8).save(OUT+'base_longo_A.png')
# A vertical: retrato oficial descido 330px
place(A,1080,1920,1080/2112,0,800,feather=220,dark=0.8,crop=(768,0,2880,2160)).save(OUT+'base_vertical_A.png')
# B longo
place(B,1920,1080,1632/B.width,290,62,feather=160,dark=0.8).save(OUT+'base_longo_B.png')
# B vertical
place(B,1080,1920,1080/2480,0,760,feather=200,dark=0.8,crop=(1120,0,3600,2160)).save(OUT+'base_vertical_B.png')
