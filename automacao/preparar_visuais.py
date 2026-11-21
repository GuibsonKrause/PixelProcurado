"""Gera arte tipográfica original, sem imagens de GTA, e fixtures de teste."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / '.course-tools'))
from PIL import Image, ImageDraw, ImageFont

OUT = ROOT / 'producao/L01/arte'
OUT.mkdir(parents=True, exist_ok=True)
def font(size):
    return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', size)

im = Image.new('RGB', (1280,720), '#101218')
d = ImageDraw.Draw(im)
for x in range(30,1280,80):
    for y in range(30,720,80):
        d.rectangle((x,y,x+6,y+6), fill='#242834')
d.rounded_rectangle((66,57,383,105),radius=9,fill='#FFD43B')
d.text((84,66),'PIXEL PROCURADO',font=font(25),fill='#101218')
d.text((62,154),'GTA 6',font=font(155),fill='white')
d.text((69,353),'CONFIRMADO?',font=font(103),fill='#FFD43B')
d.line((72,510,1200,510),fill='#FFD43B',width=4)
d.text((75,549),'FATOS. FONTES. PERGUNTAS.',font=font(37),fill='white')
d.text((76,632),'DOSSIÊ 01',font=font(23),fill='#A6ADB9')
im.save(OUT/'thumbnail_tipografica.png')
im.resize((320,180)).save(OUT/'thumbnail_celular.png')

for name, title, subtitle in [
    ('confirmado','CONFIRMADO','O que a fonte realmente informa'),
    ('analise','ANÁLISE','Nossa interpretação da evidência'),
    ('em_aberto','EM ABERTO','Uma pergunta que exige outra prova')]:
    card=Image.new('RGB',(1920,1080),'#101218')
    p=ImageDraw.Draw(card)
    p.rectangle((100,160,115,900),fill='#FFD43B')
    p.text((160,205),'PIXEL PROCURADO / DOSSIÊ 01',font=font(35),fill='#A6ADB9')
    p.text((160,420),title,font=font(120),fill='#FFD43B')
    p.text((168,610),subtitle,font=font(52),fill='white')
    card.save(OUT/f'cartela_{name}.png')
print(OUT)
