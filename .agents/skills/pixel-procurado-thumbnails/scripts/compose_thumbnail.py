"""Aplica o sistema visual Pixel Procurado sobre uma arte-base sem texto."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError:
    for candidate in (Path.cwd() / ".production-tools" / "python", Path.cwd() / ".course-tools"):
        if candidate.is_dir():
            sys.path.insert(0, str(candidate))
    from PIL import Image, ImageDraw, ImageFont

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_LOGO = SKILL_DIR / "assets" / "gta-vi-logo.png"
WHITE = "#F8FAFC"
YELLOW = "#FFD33D"


def font_path(candidates: list[str]) -> str:
    for candidate in candidates:
        if Path(candidate).is_file():
            return candidate
    raise FileNotFoundError("Instale Impact/Bahnschrift ou adapte as fontes no script.")


MAIN_FONT = font_path(["C:/Windows/Fonts/impact.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"])
LABEL_FONT = font_path(["C:/Windows/Fonts/bahnschrift.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"])


def cover(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = max(width / image.width, height / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (image.width - width) // 2)
    top = max(0, (image.height - height) // 2)
    return image.crop((left, top, left + width, top + height)).convert("RGBA")


def fit_font(text: str, max_width: int, start: int, minimum: int) -> ImageFont.FreeTypeFont:
    for size in range(start, minimum - 1, -2):
        font = ImageFont.truetype(MAIN_FONT, size)
        if font.getbbox(text)[2] <= max_width:
            return font
    return ImageFont.truetype(MAIN_FONT, minimum)


def top_gradient(canvas: Image.Image, height: int, alpha: int = 225) -> None:
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    pixels = layer.load()
    for y in range(height):
        value = int(alpha * max(0, 1 - y / max(1, height)) ** 1.2)
        for x in range(canvas.width):
            pixels[x, y] = (4, 8, 18, value)
    canvas.alpha_composite(layer)


def add_logo(canvas: Image.Image, logo_path: Path, max_size: tuple[int, int], right: int, top: int) -> None:
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail(max_size, Image.Resampling.LANCZOS)
    canvas.alpha_composite(logo, (canvas.width - logo.width - right, top))


def compose_short(base: Image.Image, line1: str, line2: str, logo: Path | None) -> Image.Image:
    canvas = cover(base, 1080, 1920)
    top_gradient(canvas, 980)
    draw = ImageDraw.Draw(canvas)
    label = ImageFont.truetype(LABEL_FONT, 28)
    draw.rounded_rectangle((54, 64, 353, 118), 12, fill=(5, 9, 18, 215), outline=YELLOW, width=2)
    draw.text((76, 76), "PIXEL / PROCURADO", font=label, fill=WHITE)
    if logo:
        add_logo(canvas, logo, (390, 250), 44, 34)
    y = 335
    draw.rounded_rectangle((52, y - 38, 1028, y + 425), 28, fill=(4, 8, 18, 160))
    draw.rectangle((62, y - 12, 220, y - 2), fill=YELLOW)
    for index, text in enumerate((line1, line2)):
        font = fit_font(text, 930, 145, 82)
        draw.text((62, y + 20 + index * 152), text, font=font, fill=WHITE if index == 0 else YELLOW,
                  stroke_width=8, stroke_fill="#080A10")
    return canvas


def compose_long(base: Image.Image, line1: str, line2: str, logo: Path | None) -> Image.Image:
    canvas = cover(base, 1280, 720)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for x in range(760):
        alpha = int(225 * max(0, 1 - x / 800) ** 1.15)
        overlay_draw.line((x, 0, x, 720), fill=(4, 8, 18, alpha))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)
    label = ImageFont.truetype(LABEL_FONT, 22)
    draw.rounded_rectangle((42, 36, 284, 82), 10, fill=(5, 9, 18, 220), outline=YELLOW, width=2)
    draw.text((61, 47), "PIXEL / PROCURADO", font=label, fill=WHITE)
    if logo:
        add_logo(canvas, logo, (260, 150), 38, 26)
    draw.rectangle((50, 170, 190, 180), fill=YELLOW)
    for index, text in enumerate((line1, line2)):
        font = fit_font(text, 650, 104, 62)
        draw.text((48, 205 + index * 120), text, font=font, fill=WHITE if index == 0 else YELLOW,
                  stroke_width=7, stroke_fill="#080A10")
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--line1", required=True)
    parser.add_argument("--line2", required=True)
    parser.add_argument("--format", choices=("short", "long"), required=True)
    parser.add_argument("--logo", type=Path, default=DEFAULT_LOGO)
    parser.add_argument("--no-logo", action="store_true")
    args = parser.parse_args()

    base = Image.open(args.base).convert("RGB")
    logo = None if args.no_logo else args.logo
    if logo and not logo.is_file():
        raise FileNotFoundError(logo)
    canvas = compose_short(base, args.line1.upper(), args.line2.upper(), logo) if args.format == "short" else compose_long(base, args.line1.upper(), args.line2.upper(), logo)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    master = args.output_dir / "capa_master.png"
    upload = args.output_dir / "capa_youtube.jpg"
    canvas.convert("RGB").save(master, optimize=True)
    quality = 92
    while True:
        canvas.convert("RGB").save(upload, quality=quality, optimize=True, progressive=True)
        if upload.stat().st_size < 2_000_000 or quality <= 80:
            break
        quality -= 3
    print(f"Criados: {master} e {upload}")


if __name__ == "__main__":
    main()
