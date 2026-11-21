"""Reproduz a composição editorial L03 sobre a base imagegen preservada."""
from pathlib import Path
import sys
import tempfile
import json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '.course-tools'))
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

OUT = Path(__file__).resolve().parent
BASE = OUT / 'thumbnail_base_gerada.png'
LOGO = Path('C:/Users/guibson.krause/.codex/skills/pixel-procurado-thumbnails/assets/gta-vi-logo.png')
WHITE, YELLOW, GRAPHITE = '#F8FAFC', '#FFD33D', '#080A10'
main_font = 'C:/Windows/Fonts/impact.ttf'
label_font = 'C:/Windows/Fonts/bahnschrift.ttf'

def font(size, main=False):
    return ImageFont.truetype(main_font if main else label_font, size)

base = Image.open(BASE).convert('RGB')
canvas = ImageOps.fit(base, (1920, 1080), Image.Resampling.LANCZOS).convert('RGBA')
draw = ImageDraw.Draw(canvas)

# Logo oficial: remover somente o preto externo conectado às bordas.
logo = Image.open(LOGO).convert('RGBA')
for xy in [(0, 0), (logo.width-1, 0), (0, logo.height-1), (logo.width-1, logo.height-1)]:
    ImageDraw.floodfill(logo, xy, (0, 0, 0, 0), thresh=12)
logo = logo.crop(logo.getbbox())
logo.thumbnail((250, 180), Image.Resampling.LANCZOS)
logo_xy = (1844-logo.width, 45)
shadow = Image.new('RGBA', canvas.size)
shadow.paste((4, 8, 18, 230), (logo_xy[0]-8, logo_xy[1]-8), logo.getchannel('A'))
canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(13)))
canvas.alpha_composite(logo, logo_xy)
draw = ImageDraw.Draw(canvas)

draw.rounded_rectangle((76, 63, 390, 124), radius=9, fill=(5,9,18,230), outline=YELLOW, width=2)
draw.text((95, 77), 'PIXEL / PROCURADO', font=font(28), fill=WHITE)
draw.text((82, 274), 'VICE CITY: CLÁSSICA × NOVA', font=font(35), fill=WHITE, stroke_width=2, stroke_fill=GRAPHITE)
draw.rectangle((82, 337, 224, 345), fill=YELLOW)

text_bounds = []
for text, top, fill, max_size in [('A MESMA', 383, WHITE, 190), ('SENSAÇÃO?', 607, YELLOW, 190)]:
    size = max_size
    while font(size, True).getlength(text) > 950:
        size -= 1
    f = font(size, True)
    box = draw.textbbox((82, top), text, font=f, anchor='lt', stroke_width=9)
    draw.text((82, top), text, font=f, anchor='lt', fill=fill, stroke_width=9, stroke_fill=GRAPHITE)
    text_bounds.append({'text': text, 'font_px': size, 'bbox': box})

draw.text((82, 989), 'MONTAGEM EDITORIAL', font=font(22), fill='#B8C0CB', stroke_width=1, stroke_fill=GRAPHITE)
master = canvas.convert('RGB')
master.save(OUT / 'capa_master.png', optimize=True)
upload = master.resize((1280, 720), Image.Resampling.LANCZOS)
upload.save(OUT / 'capa_youtube.jpg', quality=94, subsampling=0, optimize=True, progressive=True)
assert (OUT / 'capa_youtube.jpg').stat().st_size < 2_000_000

# Provas visuais temporárias, fora dos arquivos finais do episódio.
qa = Path(tempfile.gettempdir()) / 'pixel_l03_thumbnail_qa'
qa.mkdir(exist_ok=True)
master.resize((480, 270), Image.Resampling.LANCZOS).save(qa / '25_percent.png')
master.resize((320, 180), Image.Resampling.LANCZOS).save(qa / 'mobile_320.png')
print(json.dumps({'base_native': base.size, 'master': master.size, 'upload': upload.size,
    'upload_bytes': (OUT / 'capa_youtube.jpg').stat().st_size, 'logo_composed': logo.size,
    'text_bounds': text_bounds, 'qa_preview_dir': str(qa)}, ensure_ascii=False, indent=2))
