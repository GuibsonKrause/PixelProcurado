import os
import sys

sys.path.extend([
    os.path.abspath(".course-tools"),
    os.path.abspath(".production-tools/python")
])

from PIL import Image, ImageDraw, ImageFont

os.makedirs("producao/starlink/cards", exist_ok=True)

# Colors
BG_DARK = (18, 22, 28, 235)       # Graphite dark glass
BORDER_COLOR = (255, 211, 61, 200) # Starlink / Pixel yellow accent
TEXT_WHITE = (255, 255, 255, 255)
TEXT_YELLOW = (255, 211, 61, 255)
TEXT_MUTED = (160, 170, 185, 255)
TEXT_RED = (248, 81, 73, 255)
BADGE_BG = (255, 211, 61, 255)
BADGE_TEXT = (15, 18, 22, 255)
CARD_WIDTH = 920
CARD_HEIGHT = 440
CARD_X = (1080 - CARD_WIDTH) // 2
CARD_Y = 180  # Placed in the upper area above presenter's chest/face

# Load fonts
def get_font(size, bold=True):
    font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
    try:
        return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", font_name), size)
    except Exception:
        return ImageFont.load_default()

font_title = get_font(38, bold=True)
font_badge = get_font(24, bold=True)
font_label = get_font(28, bold=False)
font_price_old = get_font(32, bold=True)
font_price_promo = get_font(46, bold=True)
font_hw_title = get_font(28, bold=True)
font_hw_val = get_font(32, bold=True)
font_small = get_font(24, bold=False)

def create_card_base(badge_text, title_text):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer Card Background with Rounded Corners
    draw.rounded_rectangle(
        [CARD_X, CARD_Y, CARD_X + CARD_WIDTH, CARD_Y + CARD_HEIGHT],
        radius=28,
        fill=BG_DARK,
        outline=BORDER_COLOR,
        width=3
    )
    
    # Header Badge Pill
    badge_w = draw.textlength(badge_text, font=font_badge) + 36
    draw.rounded_rectangle(
        [CARD_X + 36, CARD_Y + 28, CARD_X + 36 + badge_w, CARD_Y + 68],
        radius=14,
        fill=BADGE_BG
    )
    draw.text((CARD_X + 54, CARD_Y + 34), badge_text, font=font_badge, fill=BADGE_TEXT)
    
    # Title
    draw.text((CARD_X + 40, CARD_Y + 84), title_text, font=font_title, fill=TEXT_WHITE)
    
    # Subtle separator line
    draw.line([CARD_X + 36, CARD_Y + 140, CARD_X + CARD_WIDTH - 36, CARD_Y + 140], fill=(60, 70, 85, 200), width=2)
    
    return img, draw

# Card 1: Hook
def make_card_hook():
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = 940, 360
    x = (1080 - w) // 2
    y = 200
    draw.rounded_rectangle([x, y, x + w, y + h], radius=32, fill=(15, 20, 26, 240), outline=BORDER_COLOR, width=4)
    # Badge
    draw.rounded_rectangle([x + 36, y + 32, x + 380, y + 76], radius=16, fill=BADGE_BG)
    draw.text((x + 50, y + 40), "PROMOÇÃO STARLINK BRASIL", font=font_badge, fill=BADGE_TEXT)
    
    draw.text((x + 36, y + 96), "MENSALIDADE DESPENCOU!", font=get_font(44, bold=True), fill=TEXT_YELLOW)
    draw.text((x + 36, y + 160), "30% DE DESCONTO EM TODOS OS PLANOS", font=get_font(32, bold=True), fill=TEXT_WHITE)
    draw.text((x + 36, y + 220), "Reduções históricas para novas assinaturas residenciais e viagem.", font=font_small, fill=TEXT_MUTED)
    draw.text((x + 36, y + 270), "Confira os preços comparados abaixo:", font=get_font(26, bold=True), fill=TEXT_WHITE)
    return img

# Card 2: Plano Residencial Max
def make_card_max():
    img, draw = create_card_base("RESIDENCIAL - CASA", "PLANO RESIDENCIAL MAX")
    # Mensalidade
    draw.text((CARD_X + 40, CARD_Y + 155), "Mensalidade:", font=font_label, fill=TEXT_MUTED)
    # De: R$ 249/mês
    de_text = "De: R$ 249,00"
    draw.text((CARD_X + 40, CARD_Y + 195), de_text, font=font_price_old, fill=TEXT_RED)
    de_w = draw.textlength(de_text, font=font_price_old)
    # Strike-through line
    draw.line([CARD_X + 38, CARD_Y + 215, CARD_X + 40 + de_w + 4, CARD_Y + 215], fill=TEXT_RED, width=3)
    
    # Por: R$ 174,00/mês
    draw.text((CARD_X + 280, CARD_Y + 185), "➔", font=font_price_old, fill=TEXT_YELLOW)
    draw.text((CARD_X + 330, CARD_Y + 180), "R$ 174,00/mês", font=font_price_promo, fill=TEXT_YELLOW)
    
    # Tag 30% OFF
    draw.rounded_rectangle([CARD_X + 680, CARD_Y + 184, CARD_X + 860, CARD_Y + 228], radius=12, fill=(46, 160, 67, 240))
    draw.text((CARD_X + 700, CARD_Y + 192), "30% OFF", font=get_font(24, bold=True), fill=TEXT_WHITE)
    
    # Separator
    draw.line([CARD_X + 36, CARD_Y + 255, CARD_X + CARD_WIDTH - 36, CARD_Y + 255], fill=(50, 60, 75, 180), width=1)
    
    # Hardware
    draw.text((CARD_X + 40, CARD_Y + 275), "Equipamento Starlink Mini:", font=font_hw_title, fill=TEXT_WHITE)
    draw.text((CARD_X + 40, CARD_Y + 315), "Antena Mini por apenas R$ 49,00", font=font_hw_val, fill=TEXT_YELLOW)
    draw.text((CARD_X + 40, CARD_Y + 365), "+ Roteador Wi-Fi extra incluso no pacote", font=font_small, fill=TEXT_MUTED)
    return img

# Card 3: Plano Residencial 100 Mega
def make_card_100mega():
    img, draw = create_card_base("RESIDENCIAL - CASA", "PLANO RESIDENCIAL 100 MEGA")
    draw.text((CARD_X + 40, CARD_Y + 155), "Mensalidade:", font=font_label, fill=TEXT_MUTED)
    de_text = "De: R$ 189,00"
    draw.text((CARD_X + 40, CARD_Y + 195), de_text, font=font_price_old, fill=TEXT_RED)
    de_w = draw.textlength(de_text, font=font_price_old)
    draw.line([CARD_X + 38, CARD_Y + 215, CARD_X + 40 + de_w + 4, CARD_Y + 215], fill=TEXT_RED, width=3)
    
    draw.text((CARD_X + 280, CARD_Y + 185), "➔", font=font_price_old, fill=TEXT_YELLOW)
    draw.text((CARD_X + 330, CARD_Y + 180), "R$ 132,00/mês", font=font_price_promo, fill=TEXT_YELLOW)
    
    draw.rounded_rectangle([CARD_X + 680, CARD_Y + 184, CARD_X + 860, CARD_Y + 228], radius=12, fill=(46, 160, 67, 240))
    draw.text((CARD_X + 700, CARD_Y + 192), "30% OFF", font=get_font(24, bold=True), fill=TEXT_WHITE)
    
    draw.line([CARD_X + 36, CARD_Y + 255, CARD_X + CARD_WIDTH - 36, CARD_Y + 255], fill=(50, 60, 75, 180), width=1)
    
    draw.text((CARD_X + 40, CARD_Y + 275), "Equipamento / Kit Antena:", font=font_hw_title, fill=TEXT_WHITE)
    draw.text((CARD_X + 40, CARD_Y + 315), "Kit Completo por R$ 249,00", font=font_hw_val, fill=TEXT_YELLOW)
    draw.text((CARD_X + 40, CARD_Y + 365), "Velocidade estável de 100 Mbps com tráfego ilimitado", font=font_small, fill=TEXT_MUTED)
    return img

# Card 4: Plano Viagem 100 GB
def make_card_viagem100():
    img, draw = create_card_base("PLANO VIAGEM / MÓVEL", "PLANO VIAGEM 100 GB")
    draw.text((CARD_X + 40, CARD_Y + 155), "Mensalidade:", font=font_label, fill=TEXT_MUTED)
    de_text = "De: R$ 339,00"
    draw.text((CARD_X + 40, CARD_Y + 195), de_text, font=font_price_old, fill=TEXT_RED)
    de_w = draw.textlength(de_text, font=font_price_old)
    draw.line([CARD_X + 38, CARD_Y + 215, CARD_X + 40 + de_w + 4, CARD_Y + 215], fill=TEXT_RED, width=3)
    
    draw.text((CARD_X + 280, CARD_Y + 185), "➔", font=font_price_old, fill=TEXT_YELLOW)
    draw.text((CARD_X + 330, CARD_Y + 180), "R$ 237,30/mês", font=font_price_promo, fill=TEXT_YELLOW)
    
    draw.rounded_rectangle([CARD_X + 680, CARD_Y + 184, CARD_X + 860, CARD_Y + 228], radius=12, fill=(46, 160, 67, 240))
    draw.text((CARD_X + 700, CARD_Y + 192), "30% OFF", font=get_font(24, bold=True), fill=TEXT_WHITE)
    
    draw.line([CARD_X + 36, CARD_Y + 255, CARD_X + CARD_WIDTH - 36, CARD_Y + 255], fill=(50, 60, 75, 180), width=1)
    
    draw.text((CARD_X + 40, CARD_Y + 275), "Equipamento Móvel / Carro:", font=font_hw_title, fill=TEXT_WHITE)
    draw.text((CARD_X + 40, CARD_Y + 315), "Antena por R$ 249,00", font=font_hw_val, fill=TEXT_YELLOW)
    draw.text((CARD_X + 40, CARD_Y + 365), "Ideal para veículos, motorhomes e trabalho em movimento", font=font_small, fill=TEXT_MUTED)
    return img

# Card 5: Plano Viagem Ilimitado
def make_card_viagem_ilim():
    img, draw = create_card_base("PLANO VIAGEM / MÓVEL", "PLANO VIAGEM ILIMITADO")
    draw.text((CARD_X + 40, CARD_Y + 155), "Mensalidade:", font=font_label, fill=TEXT_MUTED)
    de_text = "De: R$ 619,00"
    draw.text((CARD_X + 40, CARD_Y + 195), de_text, font=font_price_old, fill=TEXT_RED)
    de_w = draw.textlength(de_text, font=font_price_old)
    draw.line([CARD_X + 38, CARD_Y + 215, CARD_X + 40 + de_w + 4, CARD_Y + 215], fill=TEXT_RED, width=3)
    
    draw.text((CARD_X + 280, CARD_Y + 185), "➔", font=font_price_old, fill=TEXT_YELLOW)
    draw.text((CARD_X + 330, CARD_Y + 180), "R$ 433,30/mês", font=font_price_promo, fill=TEXT_YELLOW)
    
    draw.rounded_rectangle([CARD_X + 680, CARD_Y + 184, CARD_X + 860, CARD_Y + 228], radius=12, fill=(46, 160, 67, 240))
    draw.text((CARD_X + 700, CARD_Y + 192), "30% OFF", font=get_font(24, bold=True), fill=TEXT_WHITE)
    
    draw.line([CARD_X + 36, CARD_Y + 255, CARD_X + CARD_WIDTH - 36, CARD_Y + 255], fill=(50, 60, 75, 180), width=1)
    
    draw.text((CARD_X + 40, CARD_Y + 275), "Equipamento Ilimitado:", font=font_hw_title, fill=TEXT_WHITE)
    draw.text((CARD_X + 40, CARD_Y + 315), "Antena sai a R$ 249,00", font=font_hw_val, fill=TEXT_YELLOW)
    draw.text((CARD_X + 40, CARD_Y + 365), "Uso móvel sem limites de dados em qualquer lugar do Brasil", font=font_small, fill=TEXT_MUTED)
    return img

# Card 6: Regras da Promoção
def make_card_regras():
    img, draw = create_card_base("CONDIÇÕES DA OFERTA", "REGRAS DA PROMOÇÃO")
    draw.text((CARD_X + 40, CARD_Y + 160), "• Válida até 30 de Novembro", font=get_font(34, bold=True), fill=TEXT_YELLOW)
    draw.text((CARD_X + 40, CARD_Y + 220), "• Apenas para Novas Contratações (novos clientes)", font=get_font(28, bold=True), fill=TEXT_WHITE)
    draw.text((CARD_X + 40, CARD_Y + 275), "• Não se aplica a assinaturas antigas ativas", font=font_small, fill=TEXT_MUTED)
    draw.text((CARD_X + 40, CARD_Y + 325), "• Suporte e Instalação Garantida ao fechar contato", font=get_font(30, bold=True), fill=TEXT_YELLOW)
    return img

# Card 7: Bônus R$ 200 de Crédito
def make_card_bonus():
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = 920, 420
    x = (1080 - w) // 2
    y = 180
    draw.rounded_rectangle([x, y, x + w, y + h], radius=30, fill=(22, 28, 36, 245), outline=BORDER_COLOR, width=4)
    # Badge
    draw.rounded_rectangle([x + 36, y + 28, x + 350, y + 72], radius=14, fill=BADGE_BG)
    draw.text((x + 50, y + 36), "VANTAGEM EXCLUSIVA", font=font_badge, fill=BADGE_TEXT)
    
    draw.text((x + 40, y + 90), "GANHE R$ 200,00 DE CRÉDITO!", font=get_font(42, bold=True), fill=TEXT_YELLOW)
    draw.text((x + 40, y + 160), "Desconto direto para abater na sua mensalidade", font=get_font(28, bold=True), fill=TEXT_WHITE)
    draw.line([x + 36, y + 215, x + w - 36, y + 215], fill=(60, 70, 85, 200), width=2)
    
    draw.text((x + 40, y + 240), "• Válido comprando diretamente pelo contato", font=get_font(28, bold=False), fill=TEXT_WHITE)
    draw.text((x + 40, y + 295), "• Instalação e ativação 100% garantida", font=get_font(28, bold=False), fill=TEXT_WHITE)
    draw.text((x + 40, y + 350), "• Economia máxima logo na primeira fatura!", font=get_font(28, bold=True), fill=TEXT_YELLOW)
    return img

# Card 8: CTA Final
def make_card_cta():
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = 920, 320
    x = (1080 - w) // 2
    y = 220
    draw.rounded_rectangle([x, y, x + w, y + h], radius=30, fill=(20, 26, 34, 245), outline=BORDER_COLOR, width=4)
    draw.rounded_rectangle([x + 36, y + 28, x + 320, y + 72], radius=14, fill=(46, 160, 67, 240))
    draw.text((x + 50, y + 36), "APROVEITE AGORA", font=font_badge, fill=TEXT_WHITE)
    
    draw.text((x + 40, y + 95), "ENTRE EM CONTATO AGORA!", font=get_font(44, bold=True), fill=TEXT_YELLOW)
    draw.text((x + 40, y + 165), "Garanta seu kit promocional e o crédito de R$ 200.", font=get_font(28, bold=False), fill=TEXT_WHITE)
    draw.text((x + 40, y + 225), "Chame no direct / mensagem agora mesmo! ➔", font=get_font(30, bold=True), fill=TEXT_WHITE)
    return img

cards = [
    ("card_01_hook.png", make_card_hook()),
    ("card_02_max.png", make_card_max()),
    ("card_03_100mega.png", make_card_100mega()),
    ("card_04_viagem100.png", make_card_viagem100()),
    ("card_05_viagem_ilim.png", make_card_viagem_ilim()),
    ("card_06_regras.png", make_card_regras()),
    ("card_07_bonus.png", make_card_bonus()),
    ("card_08_cta.png", make_card_cta()),
]

for name, card_img in cards:
    p = os.path.join("producao/starlink/cards", name)
    card_img.save(p, "PNG")
    print(f"Saved {p}", flush=True)

print("All 8 cards generated successfully!", flush=True)
