"""Finaliza as 14 thumbnails verticais com arte gerada, logo e tipografia."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.production-tools' / 'python'), str(ROOT / '.course-tools')]

from PIL import Image, ImageDraw, ImageFont, ImageFilter
BASE = ROOT / 'producao' / 'shorts'
FRAME = BASE / '_acervo' / 'gtavi_logo_frame.png'
LOGO = BASE / '_acervo' / 'gtavi_logo_transparente.png'
W, H = 1080, 1920
WHITE = '#F8FAFC'
YELLOW = '#FFD33D'
PINK = '#FF2DAA'
FONT_MAIN = 'C:/Windows/Fonts/impact.ttf'
FONT_LABEL = 'C:/Windows/Fonts/bahnschrift.ttf'

LINES = {
    'C01': ['DATA CERTA.', 'VERSÃO ERRADA?'],
    'C02': ['O MESMO SONHO.', 'OUTRA ESCOLHA.'],
    'C03': ['OLHE ATRÁS', 'DO ABRAÇO.'],
    'C04': ['SAUDADE DO JOGO', 'OU DA ÉPOCA?'],
    'C05': ['TEM GAMEPLAY.', 'MAS ONDE?'],
    'C06': ['OFICIAL.', 'MAS É CAPTURA?'],
    'C07': ['O CARRO', 'NÃO É TUDO.'],
    'C08': ['A DONA', 'DA RUA.'],
    'C09': ['VOCÊ VÊ TUDO.', 'E QUEM VÊ VOCÊ?'],
    'C10': ['SUA PLAYLIST.', 'COM LOCUTOR.'],
    'C11': ['SEM ALUGUEL.', 'COM COBRANÇA.'],
    'C12': ['VOCÊ CONFIARIA', 'NESSE PLANO?'],
    'L01-R02': ['CONFIANÇA', 'NÃO É SPOILER.'],
    'L01-R03': ['ESSA IMAGEM', 'NÃO MEDE O MAPA.'],
}

PROMPTS = {
    'C01': 'Vice City neon, calendário/interface fraturada e tensão entre data e plataforma.',
    'C02': 'Jason e Lucia em caminhos visuais opostos, mesmo sonho e escolhas diferentes.',
    'C03': 'Casal em primeiro plano com polícia, helicóptero e barcos compondo a segunda história.',
    'C04': 'Carro clássico em Vice City, transição entre nostalgia retrô e cidade contemporânea.',
    'C05': 'Jason e Lucia em ação, divisão visual entre cena cinematográfica e perspectiva jogável.',
    'C06': 'Composição rasgada entre artwork ilustrado e imagem cinematográfica realista.',
    'C07': 'Carro azul em destaque, com bairro, murais, motos e pessoas disputando a atenção.',
    'C08': 'Iguana em perspectiva baixa como protagonista da rua nas Leonida Keys.',
    'C09': 'Divisão entre horizonte aberto das Keys e margens fechadas de Grassrivers.',
    'C10': 'Interior de carro, rádio e ondas sonoras atravessando a cidade neon.',
    'C11': 'Brian e Jason numa negociação, chaves da casa e sombra de obrigação.',
    'C12': 'Raul planejando um golpe, rotas crescentes e pressão policial ao fundo.',
    'L01-R02': 'Jason e Lucia sob pressão, reflexos partidos sugerindo dúvida sem confirmar traição.',
    'L01-R03': 'Vice City e ilhas desaparecendo nas bordas e na névoa, sem escala comprovada.',
}

def extract_logo():
    src = Image.open(FRAME).convert('RGB')
    crop = src.crop((900, 330, 2960, 1725))
    marked = crop.copy()
    marker = (1, 2, 3)
    d = ImageDraw.Draw(marked)
    for point in [(0,0),(crop.width-1,0),(0,crop.height-1),(crop.width-1,crop.height-1)]:
        ImageDraw.floodfill(marked, point, marker, thresh=28)
    alpha = Image.new('L', crop.size, 255)
    ap = alpha.load(); mp = marked.load()
    for y in range(crop.height):
        for x in range(crop.width):
            if mp[x,y] == marker: ap[x,y] = 0
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.7))
    crop.putalpha(alpha)
    bbox = alpha.getbbox()
    assert bbox
    crop = crop.crop(bbox)
    crop.save(LOGO)
    return crop

def cover(im):
    scale = max(W/im.width, H/im.height)
    size = (round(im.width*scale), round(im.height*scale))
    im = im.resize(size, Image.Resampling.LANCZOS)
    left = (im.width-W)//2
    top = max(0, (im.height-H)//2)
    return im.crop((left, top, left+W, top+H)).convert('RGBA')

def fit_font(text, max_width, start=145, minimum=82):
    for size in range(start, minimum-1, -2):
        f = ImageFont.truetype(FONT_MAIN, size)
        if f.getbbox(text)[2] <= max_width:
            return f
    return ImageFont.truetype(FONT_MAIN, minimum)

def gradient_overlay(canvas):
    layer = Image.new('RGBA', (W,H), (0,0,0,0))
    px = layer.load()
    for y in range(960):
        a = int(222 * max(0, 1-y/980)**1.25)
        for x in range(W): px[x,y] = (4,8,18,a)
    canvas.alpha_composite(layer)

def make_one(rid, logo):
    pub = BASE / rid / 'publicacao'
    base = cover(Image.open(pub/'thumbnail_base_gerada.png').convert('RGB'))
    gradient_overlay(base)
    draw = ImageDraw.Draw(base)
    label_font = ImageFont.truetype(FONT_LABEL, 28)
    draw.rounded_rectangle((54,64,353,118), radius=12, fill=(5,9,18,210), outline=YELLOW, width=2)
    draw.text((76,76), 'PIXEL / PROCURADO', font=label_font, fill=WHITE)

    if rid == 'C10':
        badge_font = ImageFont.truetype(FONT_MAIN, 74)
        draw.rounded_rectangle((720,54,1024,164), radius=14, fill=(5,9,18,225), outline=PINK, width=4)
        draw.text((754,62), 'GTA V', font=badge_font, fill=WHITE, stroke_width=3, stroke_fill='#130918')
    else:
        lg = logo.copy()
        target_w = 390
        lg.thumbnail((target_w,250), Image.Resampling.LANCZOS)
        base.alpha_composite(lg, (W-lg.width-44, 34))

    y = 300
    draw.rounded_rectangle((52,y-38,1028,y+425), radius=28, fill=(4,8,18,125))
    draw.rectangle((62,y-12,220,y-2), fill=YELLOW)
    for i,line in enumerate(LINES[rid]):
        font = fit_font(line, 930)
        fill = WHITE if i == 0 else YELLOW
        draw.text((62,y+20+i*152), line, font=font, fill=fill,
                  stroke_width=8, stroke_fill='#080A10')

    draw.rounded_rectangle((58,1788,432,1846), radius=12, fill=(5,9,18,190))
    small = ImageFont.truetype(FONT_LABEL, 25)
    draw.text((79,1802), 'DETALHES • HISTÓRIAS • EVIDÊNCIAS', font=small, fill='#DCE3EC')

    master = pub/'capa_master.png'
    ready = pub/'capa_youtube.jpg'
    base.convert('RGB').save(master, optimize=True)
    quality = 92
    while True:
        base.convert('RGB').save(ready, quality=quality, optimize=True, progressive=True)
        if ready.stat().st_size < 2_000_000 or quality <= 80: break
        quality -= 3
    assert Image.open(master).size == (W,H)
    assert Image.open(ready).size == (W,H)
    assert ready.stat().st_size < 2_000_000
    prompt = f'''# Thumbnail {rid}\n\nArte-base gerada com a ferramenta integrada de geração de imagens.\n\nDireção: {PROMPTS[rid]}\n\nAcabamento: composição 9:16, gradiente grafite, frase “{' / '.join(LINES[rid])}”, tipografia Impact branca e amarela, marca Pixel Procurado e {'identificação GTA V' if rid=='C10' else 'logo oficial de GTA VI extraída do Trailer 1 do acervo'}.\n\nA arte-base não contém texto nem logotipo gerado; esses elementos foram aplicados separadamente para preservar grafia e identidade. A composição é uma montagem editorial, não uma captura oficial do jogo.\n'''
    (pub/'PROMPT_THUMBNAIL.txt').write_text(prompt, encoding='utf8')
    return ready

def main():
    logo = extract_logo()
    outputs = [make_one(rid,logo) for rid in LINES]
    thumb_w, thumb_h = 270, 480
    sheet = Image.new('RGB',(thumb_w*4, (thumb_h+40)*4),'#111826')
    draw = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT_LABEL,22)
    for i,(rid,p) in enumerate(zip(LINES,outputs)):
        im=Image.open(p).convert('RGB'); im.thumbnail((thumb_w,thumb_h),Image.Resampling.LANCZOS)
        x=(i%4)*thumb_w; y=(i//4)*(thumb_h+40)
        sheet.paste(im,(x,y)); draw.text((x+10,y+486),rid,font=f,fill='white')
    sheet.save(BASE/'00_THUMBNAILS_REFEITAS.jpg',quality=92,optimize=True)
    print(f'THUMBNAILS: {len(outputs)}; logo={LOGO}')

if __name__ == '__main__':
    main()
