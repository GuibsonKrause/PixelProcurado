"""Gera páginas de contato em intervalos curtos para os vídeos longos de GTA VI."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA_ROOT = ROOT / "videosGTAVI"
OUTPUT = MEDIA_ROOT / "_catalogo" / "indices_detalhados"
sys.path[:0] = [str(ROOT / ".course-tools")]

import av  # noqa: E402
from PIL import Image, ImageDraw, ImageFont, ImageOps  # noqa: E402

VIDEOS = {
    "GTAVI_An_Extended_Look.mp4": 10,
    "GTAVI_Launch_Trailer.mp4": 5,
    "GTAVI_Trailer_1.mp4": 5,
    "GTAVI_Trailer_2.mp4": 5,
}


def stamp(seconds: float) -> str:
    total = int(round(seconds))
    return f"{total // 60:02d}:{total % 60:02d}"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidate = Path("C:/Windows/Fonts/arial.ttf")
    return ImageFont.truetype(str(candidate), size) if candidate.is_file() else ImageFont.load_default()


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, "#11131a")
    fitted = ImageOps.contain(image.convert("RGB"), size, Image.Resampling.LANCZOS)
    canvas.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return canvas


def save_page(items: list[tuple[Image.Image, str]], destination: Path) -> None:
    columns, rows = 3, 4
    cell = (480, 270)
    label_height = 44
    sheet = Image.new("RGB", (columns * cell[0], rows * (cell[1] + label_height)), "#090a0f")
    draw = ImageDraw.Draw(sheet)
    label_font = font(24)
    for index, (image, label) in enumerate(items):
        x = index % columns * cell[0]
        y = index // columns * (cell[1] + label_height)
        sheet.paste(fit(image, cell), (x, y))
        draw.text((x + 12, y + cell[1] + 7), label, fill="#ffffff", font=label_font)
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, quality=92)


def frame_at(container: av.container.InputContainer, stream: av.video.stream.VideoStream, second: float) -> Image.Image | None:
    container.seek(int(second * av.time_base), any_frame=False, backward=True)
    frame = next(container.decode(stream), None)
    return frame.to_image() if frame else None


def index_video(path: Path, interval: int) -> int:
    with av.open(str(path)) as container:
        stream = next(stream for stream in container.streams if stream.type == "video")
        duration = container.duration / av.time_base if container.duration else 0
        seconds = list(range(0, max(1, math.ceil(duration)), interval))
        if seconds[-1] < duration - 1:
            seconds.append(max(0, int(duration - 1)))
        items: list[tuple[Image.Image, str]] = []
        for second in seconds:
            image = frame_at(container, stream, float(second))
            if image is not None:
                items.append((image, stamp(float(second))))
        for page_index in range(0, len(items), 12):
            page = items[page_index:page_index + 12]
            save_page(page, OUTPUT / path.stem / f"pagina_{page_index // 12 + 1:02d}.jpg")
        return len(items)


def main() -> None:
    for name, interval in VIDEOS.items():
        count = index_video(MEDIA_ROOT / name, interval)
        print(f"{name}: {count} quadros")


if __name__ == "__main__":
    main()
