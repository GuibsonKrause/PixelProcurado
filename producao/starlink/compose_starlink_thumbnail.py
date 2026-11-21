import sys
from pathlib import Path
import shutil

for p in [Path.cwd() / ".production-tools" / "python", Path.cwd() / ".course-tools"]:
    if p.is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(path_list, size):
    for p in path_list:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

MAIN_FONTS = ["C:/Windows/Fonts/impact.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"]
LABEL_FONTS = ["C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]

WHITE = "#F8FAFC"
YELLOW = "#FFD33D"
GRAPHITE = (4, 8, 18)

def fit_font(text: str, max_width: int, start: int, minimum: int) -> ImageFont.FreeTypeFont:
    for size in range(start, minimum - 1, -2):
        font = get_font(MAIN_FONTS, size)
        bbox = font.getbbox(text)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
    return get_font(MAIN_FONTS, minimum)

def fit_label_font(text: str, max_width: int, start: int, minimum: int) -> ImageFont.FreeTypeFont:
    for size in range(start, minimum - 1, -1):
        font = get_font(LABEL_FONTS, size)
        bbox = font.getbbox(text)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
    return get_font(LABEL_FONTS, minimum)

def draw_vector_arrow(draw: ImageDraw.ImageDraw, center_x: int, center_y: int, length: int = 40):
    """Desenha uma flecha direcional estilizada de alta visibilidade em amarelo."""
    half_len = length // 2
    x1 = center_x - half_len
    x2 = center_x + half_len
    
    stem_h = 7
    arrow_head_w = 16
    arrow_head_h = 14
    
    # Stem
    draw.rectangle(
        [(x1, center_y - stem_h // 2), (x2 - arrow_head_w + 3, center_y + stem_h // 2)],
        fill=YELLOW
    )
    # Head triangle
    draw.polygon(
        [
            (x2 - arrow_head_w, center_y - arrow_head_h),
            (x2 + 4, center_y),
            (x2 - arrow_head_w, center_y + arrow_head_h)
        ],
        fill=YELLOW
    )

def draw_lightning_bolt(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 24):
    """Desenha um raio dourado como ícone vetorial."""
    pts = [
        (x + int(size * 0.55), y),
        (x + int(size * 0.15), y + int(size * 0.52)),
        (x + int(size * 0.50), y + int(size * 0.52)),
        (x + int(size * 0.35), y + size),
        (x + int(size * 0.90), y + int(size * 0.40)),
        (x + int(size * 0.55), y + int(size * 0.40)),
    ]
    draw.polygon(pts, fill=YELLOW)

def compose():
    base_path = Path(r"c:\Users\guibson.krause\Documents\ChatGPT\GamePlay\producao\starlink\thumbnail_base_gerada.png")
    logo_path = Path(r"c:\Users\guibson.krause\Documents\ChatGPT\GamePlay\producao\starlink\starlink_logo.png")
    output_dir = Path(r"c:\Users\guibson.krause\Documents\ChatGPT\GamePlay\producao\starlink")

    base = Image.open(base_path).convert("RGBA")
    
    # Target 1080x1920
    target_w, target_h = 1080, 1920
    scale = max(target_w / base.width, target_h / base.height)
    new_w = round(base.width * scale)
    new_h = round(base.height * scale)
    base_resized = base.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Crop to exact 1080x1920, anchoring to top so sky is preserved and dish is well positioned
    crop_x = (new_w - target_w) // 2
    crop_y = 0 # keep top anchor
    canvas = base_resized.crop((crop_x, crop_y, crop_x + target_w, crop_y + target_h)).convert("RGBA")

    # 1. Top dark graphite gradient over the first 950px
    grad_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(grad_layer)
    grad_height = 950
    for y in range(grad_height):
        factor = (1.0 - (y / grad_height)) ** 1.3
        alpha = int(220 * factor)
        grad_draw.line([(0, y), (target_w, y)], fill=(4, 8, 18, alpha))
    canvas.alpha_composite(grad_layer)

    # 2. Top-left Badge: OFERTA BRASIL • 30% OFF
    # Position: x=54, y=64
    badge_y1 = 64
    badge_h = 60
    badge_font = get_font(LABEL_FONTS, 26)
    
    part1 = "OFERTA BRASIL "
    part2 = "• "
    part3 = "30% OFF"
    
    b1 = badge_font.getbbox(part1)
    b2 = badge_font.getbbox(part2)
    b3 = badge_font.getbbox(part3)
    
    w1 = b1[2] - b1[0]
    w2 = b2[2] - b2[0]
    w3 = b3[2] - b3[0]
    total_badge_text_w = w1 + w2 + w3
    
    pad_x = 22
    badge_w = total_badge_text_w + pad_x * 2
    badge_x1 = 54
    badge_x2 = badge_x1 + badge_w
    badge_y2 = badge_y1 + badge_h

    # Badge background with drop shadow
    badge_shadow = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    bshadow_draw = ImageDraw.Draw(badge_shadow)
    bshadow_draw.rounded_rectangle(
        (badge_x1 + 3, badge_y1 + 4, badge_x2 + 3, badge_y2 + 4),
        radius=14, fill=(0, 0, 0, 160)
    )
    badge_shadow = badge_shadow.filter(ImageFilter.GaussianBlur(radius=4))
    canvas.alpha_composite(badge_shadow)
    
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (badge_x1, badge_y1, badge_x2, badge_y2),
        radius=14, fill=(6, 12, 24, 235), outline=YELLOW, width=2
    )
    
    tx = badge_x1 + pad_x
    ty = badge_y1 + 15
    draw.text((tx, ty), part1, font=badge_font, fill=WHITE)
    draw.text((tx + w1, ty), part2, font=badge_font, fill=YELLOW)
    draw.text((tx + w1 + w2, ty), part3, font=badge_font, fill=YELLOW)

    # 3. Top-right Logo: STARLINK
    if logo_path.is_file():
        logo_img = Image.open(logo_path).convert("RGBA")
        logo_target_w = 340
        logo_target_h = int(logo_img.height * (logo_target_w / logo_img.width))
        logo_resized = logo_img.resize((logo_target_w, logo_target_h), Image.Resampling.LANCZOS)
        logo_x = target_w - logo_target_w - 54
        logo_y = 52
        canvas.alpha_composite(logo_resized, (logo_x, logo_y))

    # 4. Main Text Panel (between y=220 and y=760)
    panel_x1 = 52
    panel_x2 = target_w - 52  # 1028 (width 976)
    panel_y1 = 220
    panel_y2 = 750
    panel_radius = 28

    # Translucent panel shadow
    panel_shadow = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    pshad_draw = ImageDraw.Draw(panel_shadow)
    pshad_draw.rounded_rectangle(
        (panel_x1 + 4, panel_y1 + 8, panel_x2 + 4, panel_y2 + 8),
        radius=panel_radius, fill=(0, 0, 0, 180)
    )
    panel_shadow = panel_shadow.filter(ImageFilter.GaussianBlur(radius=8))
    canvas.alpha_composite(panel_shadow)

    # Draw panel background
    panel_bg = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    pbg_draw = ImageDraw.Draw(panel_bg)
    pbg_draw.rounded_rectangle(
        (panel_x1, panel_y1, panel_x2, panel_y2),
        radius=panel_radius, fill=(4, 8, 18, 195), outline=(255, 211, 61, 90), width=2
    )
    # Accent top bar on the panel
    pbg_draw.rectangle(
        (panel_x1 + 36, panel_y1 + 14, panel_x1 + 220, panel_y1 + 22),
        fill=YELLOW
    )
    canvas.alpha_composite(panel_bg)

    draw = ImageDraw.Draw(canvas)

    # Line 1: MENSALIDADE CAIU 30%
    line1_text = "MENSALIDADE CAIU 30%"
    font1 = fit_font(line1_text, max_width=900, start=112, minimum=75)
    bbox1 = font1.getbbox(line1_text)
    w_l1 = bbox1[2] - bbox1[0]
    line1_x = panel_x1 + (panel_x2 - panel_x1 - w_l1) // 2
    line1_y = panel_y1 + 42

    draw.text(
        (line1_x, line1_y), line1_text, font=font1,
        fill=WHITE, stroke_width=8, stroke_fill="#080A10"
    )

    # Line 2: ANTENA POR R$ 49?
    line2_text = "ANTENA POR R$ 49?"
    font2 = fit_font(line2_text, max_width=900, start=118, minimum=80)
    bbox2 = font2.getbbox(line2_text)
    w_l2 = bbox2[2] - bbox2[0]
    line2_x = panel_x1 + (panel_x2 - panel_x1 - w_l2) // 2
    line2_y = line1_y + 130

    draw.text(
        (line2_x, line2_y), line2_text, font=font2,
        fill=YELLOW, stroke_width=8, stroke_fill="#080A10"
    )

    # Sub-barra comparativa:
    # Pill vermelha com preço antigo riscado DE R$ 249  ➔  Pill verde/amarela POR R$ 132 A R$ 174/MÊS
    comp_y1 = line2_y + 142
    comp_h = 64
    comp_y2 = comp_y1 + comp_h
    
    font_pill = get_font(LABEL_FONTS, 27)
    
    # Left pill: DE R$ 249
    txt_old = "DE R$ 249"
    bbox_old = font_pill.getbbox(txt_old)
    w_old = bbox_old[2] - bbox_old[0]
    pad_pill = 22
    pill_old_w = w_old + pad_pill * 2
    
    # Center arrow width
    arrow_w = 46
    
    # Right pill: POR R$ 132 A R$ 174/MÊS
    txt_new = "POR R$ 132 A R$ 174/MÊS"
    bbox_new = font_pill.getbbox(txt_new)
    w_new = bbox_new[2] - bbox_new[0]
    pill_new_w = w_new + pad_pill * 2
    
    gap = 20
    total_comp_w = pill_old_w + gap + arrow_w + gap + pill_new_w
    comp_start_x = panel_x1 + (panel_x2 - panel_x1 - total_comp_w) // 2
    
    # Draw Left Pill (Red)
    old_x1 = comp_start_x
    old_x2 = old_x1 + pill_old_w
    draw.rounded_rectangle(
        (old_x1, comp_y1, old_x2, comp_y2),
        radius=14, fill=(185, 28, 28, 230), outline=(239, 68, 68, 255), width=2
    )
    txt_old_x = old_x1 + pad_pill
    txt_old_y = comp_y1 + (comp_h - (bbox_old[3] - bbox_old[1])) // 2 - 2
    draw.text((txt_old_x, txt_old_y), txt_old, font=font_pill, fill="#FEE2E2", stroke_width=2, stroke_fill="#450A0A")
    # Strikethrough line (prominent white/silver line across the old price)
    line_y = comp_y1 + comp_h // 2 + 2
    draw.line([(txt_old_x - 4, line_y), (txt_old_x + w_old + 4, line_y)], fill="#FFFFFF", width=4)

    # Draw Vector Arrow
    arr_center_x = old_x2 + gap + arrow_w // 2
    arr_center_y = comp_y1 + comp_h // 2
    draw_vector_arrow(draw, arr_center_x, arr_center_y, length=arrow_w)

    # Draw Right Pill (Emerald Green with Yellow outline)
    new_x1 = old_x2 + gap + arrow_w + gap
    new_x2 = new_x1 + pill_new_w
    draw.rounded_rectangle(
        (new_x1, comp_y1, new_x2, comp_y2),
        radius=14, fill=(16, 95, 45, 235), outline=YELLOW, width=2
    )
    txt_new_x = new_x1 + pad_pill
    txt_new_y = comp_y1 + (comp_h - (bbox_new[3] - bbox_new[1])) // 2 - 2
    draw.text((txt_new_x, txt_new_y), txt_new, font=font_pill, fill="#FFD33D", stroke_width=2, stroke_fill="#052E16")

    # Selo inferior de gatilho de clique:
    # + BÔNUS DE R$ 200 NA CONTA (com ícone de raio relâmpago)
    bonus_y1 = comp_y2 + 18
    bonus_h = 52
    bonus_y2 = bonus_y1 + bonus_h
    font_bonus = fit_label_font("+ BÔNUS DE R$ 200 NA CONTA", max_width=600, start=28, minimum=20)
    txt_bonus = "+ BÔNUS DE R$ 200 NA CONTA"
    bbox_bon = font_bonus.getbbox(txt_bonus)
    w_bon = bbox_bon[2] - bbox_bon[0]
    
    bolt_size = 22
    bolt_gap = 12
    bonus_pad = 24
    bonus_w = bolt_size + bolt_gap + w_bon + bonus_pad * 2
    bonus_x1 = panel_x1 + (panel_x2 - panel_x1 - bonus_w) // 2
    bonus_x2 = bonus_x1 + bonus_w
    
    draw.rounded_rectangle(
        (bonus_x1, bonus_y1, bonus_x2, bonus_y2),
        radius=12, fill=(10, 18, 32, 235), outline=(255, 211, 61, 180), width=2
    )
    # Draw lightning bolt icon
    bolt_x = bonus_x1 + bonus_pad
    bolt_y = bonus_y1 + (bonus_h - bolt_size) // 2
    draw_lightning_bolt(draw, bolt_x, bolt_y, size=bolt_size)
    
    txt_bon_x = bolt_x + bolt_size + bolt_gap
    txt_bon_y = bonus_y1 + (bonus_h - (bbox_bon[3] - bbox_bon[1])) // 2 - 2
    draw.text((txt_bon_x, txt_bon_y), txt_bonus, font=font_bonus, fill=YELLOW, stroke_width=2, stroke_fill="#080A10")

    # Save outputs
    master_path = output_dir / "capa_master.png"
    upload_path = output_dir / "capa_youtube.jpg"
    brain_copy_path = Path(r"C:\Users\guibson.krause\.gemini\antigravity\brain\8cac68d3-885f-41ee-bda7-638dc58b4594\capa_starlink_final.jpg")

    # Save master lossless PNG
    canvas.convert("RGB").save(master_path, format="PNG", optimize=True)
    print(f"Master PNG salvo: {master_path} ({master_path.stat().st_size} bytes)")

    # Save JPG optimized < 2 MB
    quality = 92
    while True:
        canvas.convert("RGB").save(upload_path, format="JPEG", quality=quality, optimize=True, progressive=True)
        size = upload_path.stat().st_size
        print(f"Tentativa JPG qualidade {quality}: {size} bytes")
        if size < 2_000_000 or quality <= 80:
            break
        quality -= 3
    print(f"Capa YouTube JPG salva: {upload_path} ({upload_path.stat().st_size} bytes)")

    # Copy to brain
    shutil.copy2(upload_path, brain_copy_path)
    print(f"Cópia salva no brain do agente pai: {brain_copy_path}")

    # Write PROMPT_THUMBNAIL.txt
    prompt_txt_path = output_dir / "PROMPT_THUMBNAIL.txt"
    prompt_content = """# PROMPT E ESTRATÉGIA DA THUMBNAIL - STARLINK BRASIL 2026

## 1. Prompt Utilizado na Arte-Base (sem texto/logo)
"A cinematic, high-contrast, editorial vertical 9:16 composition showcasing the Starlink satellite internet experience in rural Brazil. In the foreground, an authentic Starlink rectangular dish terminal mounted on an off-grid pole, subtly illuminated with cyan and warm amber rim lighting. In the background, a cozy off-grid modern home with warm interior lights, and an overland 4x4 expedition pickup truck parked on the hill under a breathtaking dark starry night sky with a faint satellite orbital streak across the upper atmosphere. Clean upper third with deep negative space in dark blue/graphite night sky designed specifically for text overlay. 8k, photorealistic, cinematic lighting, Unreal Engine 5 render style, no text, no watermark, no logos."

## 2. Frase da Capa e Hierarquia de Mensagem
- **Linha 1 (Branco)**: MENSALIDADE CAIU 30%
- **Linha 2 (Amarelo)**: ANTENA POR R$ 49?
- **Sub-barra Comparativa**: Pill Vermelha [DE R$ 249] (riscado) ➔ Pill Verde [POR R$ 132 A R$ 174/MÊS]
- **Selo de Gatilho**: [+ BÔNUS DE R$ 200 NA CONTA]
- **Selo Topo**: OFERTA BRASIL • 30% OFF
- **Logo Topo**: STARLINK oficial com vetor orbital e satélite em amarelo

## 3. Estratégia de SEO, CTR e Retenção
- **Tensão Imediata**: Contraste brutal de valor (antena barata de R$ 49 e mensalidade caindo 30%), ativando o gatilho de curiosidade e oportunidade sem promessa falsa.
- **Leitura em Dispositivos Móveis**: Tipografia Impact pesada com stroke preto duplo e painel grafite translúcido que garante legibilidade instantânea em miniaturas de 150px na timeline do YouTube Shorts/Reels/TikTok.
- **Zona Segura (Safe Area)**: Todo o bloco textual e logos está concentrado nos primeiros 750 pixels verticais. A antena iluminada, a casa e o veículo 4x4 ficam 100% desobstruídos no centro e base, totalmente protegidos dos botões de like/comentário e da legenda inferior dos Shorts.
- **Natureza da Peça**: Montagem editorial cinematográfica para fins jornalísticos e de análise de custo-benefício da promoção Starlink Brasil.
"""
    with open(prompt_txt_path, "w", encoding="utf-8") as f:
        f.write(prompt_content)
    print(f"Documento de prompt e estratégia salvo: {prompt_txt_path}")

if __name__ == "__main__":
    compose()
