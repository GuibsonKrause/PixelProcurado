"""Cartões sociais do L06 a partir do acervo oficial do episódio."""
import sys
from pathlib import Path

from distribuir_l06_postiz import ROOT, SOCIAL, CARDS, STORY, digest, write

sys.path.insert(0, str(ROOT / '.course-tools'))
from PIL import Image, ImageDraw, ImageFont, ImageOps

INK = '#111318'
LIGHT = '#F6F5EF'
YELLOW = '#FFD33D'
MUTED = '#C0C3C6'
FONT = Path('C:/Windows/Fonts')
MEDIA = ROOT / 'videosGTAVI'
KEYS = 'Leonida_Keys_01.jpg'
GRASS = 'Grassrivers_03.jpg'
VICE = 'Vice_City_06.jpg'
PORT = 'Port_Gellhorn_01.jpg'
AMBROSIA = 'Ambrosia_02.jpg'
KALAGA = 'Mount_Kalaga_National_Park_04.jpg'
KEYS_COVER = 'Leonida_Keys_05.jpg'
GRASS_COVER = 'Grassrivers_02.jpg'


def source(name):
    paths = list(MEDIA.rglob(name))
    if len(paths) != 1:
        raise ValueError(f'Acervo para {name}: {len(paths)} correspondências')
    return paths[0]


def render(output, size, number, headline, panels, footer):
    width, height = size
    image = Image.new('RGB', size, INK)
    draw = ImageDraw.Draw(image)
    margin = 72

    def text(x, y, copy, size, color=LIGHT, bold=False):
        font = ImageFont.truetype(str(FONT / ('arialbd.ttf' if bold else 'arial.ttf')), size)
        if draw.multiline_textbbox((x, y), copy, font=font, spacing=5)[2] > width - margin:
            raise ValueError('Texto fora da margem: ' + copy)
        draw.multiline_text((x, y), copy, font=font, fill=color, spacing=5)

    is_story = height == 1920
    top = 226 if is_story else 58
    text(margin, top, 'PIXEL PROCURADO  /  GTA VI', 28, YELLOW, True)
    text(margin, top + 57, headline, 70 if is_story else 61, LIGHT, True)
    photo_y = top + 237
    panel_height = 390 if is_story else 305
    for number_in_card, (path, label) in enumerate(panels):
        x = margin
        y = photo_y + number_in_card * (panel_height + 70)
        inner = (width - 2 * margin, panel_height)
        with Image.open(path) as original:
            resized = ImageOps.contain(ImageOps.exif_transpose(original).convert('RGB'), inner,
                                       method=Image.Resampling.LANCZOS)
            image.paste(resized, (x + (inner[0] - resized.width) // 2,
                                  y + (panel_height - resized.height) // 2))
        text(x, y + panel_height + 9, label, 32, YELLOW, True)
    footer_y = 1518 if is_story else 1155
    text(margin, footer_y, footer, 31, LIGHT, True)
    text(margin, footer_y + (96 if is_story else 81),
         f'IMAGENS OFICIAIS • ROCKSTAR GAMES{number}', 23, MUTED)
    image.save(output, quality=92, subsampling=0, optimize=True)
    with Image.open(output) as check:
        check.load()
        if check.size != size or output.stat().st_size > 4_000_000:
            raise ValueError(f'Cartão inválido: {output.name}')


def main():
    SOCIAL.mkdir(parents=True, exist_ok=True)
    paths = {name: source(name) for name in (KEYS, GRASS, VICE, PORT, AMBROSIA, KALAGA, KEYS_COVER, GRASS_COVER)}
    water = [(paths[KEYS], 'LEONIDA KEYS  /  HORIZONTE ABERTO'),
             (paths[GRASS], 'GRASSRIVERS  /  MARGENS FECHADAS')]
    city = [(paths[VICE], 'VICE CITY  /  NEON À BEIRA DA RUA'),
            (paths[PORT], 'PORT GELLHORN  /  O BRILHO DO MOTEL')]
    scale = [(paths[AMBROSIA], 'AMBROSIA  /  LINHAS INDUSTRIAIS'),
             (paths[KALAGA], 'MOUNT KALAGA  /  PAREDÕES E ESTRADA')]
    cover = [(paths[KEYS_COVER], 'LEONIDA KEYS'), (paths[GRASS_COVER], 'GRASSRIVERS')]
    specs = (
        ('Leonida além\nde Vice City', cover, 'Deslize para ver três contrastes no mesmo estado.'),
        ('A mesma água.\nOutra sensação.', water, 'O horizonte das Keys dá lugar às margens fechadas.'),
        ('Duas cidades.\nDois tipos de brilho.', city, 'A iluminação muda o jeito de olhar para a rua.'),
        ('Da indústria\nà montanha', scale, 'Qual desses lugares seria sua primeira parada?'),
    )
    for index, (headline, panels, footer) in enumerate(specs, 1):
        render(CARDS[index - 1], (1080, 1350), f'   /   {index:02d} DE 04', headline, panels, footer)
    render(STORY, (1080, 1920), '', 'A mesma água.\nOutro clima.',
           water, 'Seis lugares de Leonida.\nVeja o vídeo no Pixel Procurado.')
    write(SOCIAL / 'CARTOES_QA.json',
          {'sources': {name: {'file': str(path.relative_to(ROOT)), 'sha256': digest(path)}
                       for name, path in paths.items()},
           'assets': {path.name: digest(path) for path in (*CARDS, STORY)}})


if __name__ == '__main__':
    main()
