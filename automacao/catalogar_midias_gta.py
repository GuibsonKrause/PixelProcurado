"""Cataloga o banco local de mídia oficial de GTA VI e gera folhas de contato."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA_ROOT = ROOT / "videosGTAVI"
OUTPUT = MEDIA_ROOT / "_catalogo"
sys.path[:0] = [str(ROOT / ".course-tools"), str(ROOT / ".production-tools" / "python")]

import av  # noqa: E402
from PIL import Image, ImageDraw, ImageFont, ImageOps  # noqa: E402

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}


def natural_key(value: str) -> list[object]:
    return [int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", value)]


def humanize(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("_", " ").strip()).title()


def orientation(width: int, height: int) -> str:
    ratio = width / height
    if ratio > 1.15:
        return "paisagem"
    if ratio < 0.87:
        return "vertical"
    return "quadrado"


def classify(path: Path) -> tuple[str, str, str, str]:
    relative = path.relative_to(MEDIA_ROOT)
    parts = relative.parts
    stem = path.stem
    lower_parts = [part.casefold() for part in parts]

    if path.suffix.casefold() in VIDEO_EXTENSIONS:
        category = "video"
        if stem.startswith("GTA-B02"):
            return category, "GTA V — visão geral", "gameplay de apoio", (
                "Usar apenas como imagem de apoio identificada como GTA V; nunca como prova de GTA VI."
            )
        if "An_Extended_Look" in stem:
            subject = "GTA VI — An Extended Look"
            use = "Fonte ampla para mundo, personagens, veículos e cenas oficiais; selecionar pelo índice de timestamps."
        elif "Launch_Trailer" in stem:
            subject = "GTA VI — Launch Trailer"
            use = "Abertura, estado mais recente da campanha e cenas diretamente ligadas à premissa oficial."
        elif "Trailer_1" in stem:
            subject = "GTA VI — Trailer 1"
            use = "Contexto histórico do primeiro anúncio, Lucia e apresentação inicial de Vice City/Leonida."
        elif "Trailer_2" in stem:
            subject = "GTA VI — Trailer 2"
            use = "Jason e Lucia, relação da dupla, ação e expansão visual de Leonida."
        elif "Official_Cover_Art" in stem:
            subject = "Arte oficial animada"
            use = "Abertura, separador de capítulo, recapitulação e encerramento; não usar como prova de mecânica."
        else:
            subject = humanize(stem.replace("_Video_Clip", ""))
            use = f"Perfil e apresentação oficial de {subject}; usar quando a narração citar esse personagem ou grupo."
        return category, subject, "vídeo oficial", use

    if "gtavi_screenshots" in lower_parts:
        section = parts[1] if len(parts) > 1 else ""
        subject = parts[-2] if len(parts) > 2 else humanize(stem)
        if section.casefold() == "people":
            return "screenshot — personagem", subject, "frame oficial", (
                f"Usar como evidência visual ou apoio ao apresentar {subject}; não inferir mecânicas ou destino narrativo."
            )
        return "screenshot — lugar", subject, "frame oficial", (
            f"Usar ao nomear ou descrever visualmente {subject}; não converter a imagem em medida de mapa, acesso ou escala."
        )

    if "gtavi_artwork_wallpapers" in lower_parts:
        subject = parts[-2] if len(parts) > 2 else humanize(stem)
        variant_match = re.search(r"_(landscape|phone(?:_[ab])?|portrait|square|tablet|ultrawide)$", stem, re.I)
        variant = variant_match.group(1).lower() if variant_match else "arte"
        if "postcards" in lower_parts:
            return "arte — postal de lugar", subject, variant, (
                f"Cartela de capítulo ou apresentação de {subject}; preferir landscape em vídeo longo e phone/portrait em Shorts."
            )
        if "with_logo" in stem.casefold() or "with_logos" in stem.casefold() or "with_logo" in str(relative).casefold() or "with_logos" in str(relative).casefold():
            use = "Thumbnail, abertura ou encerramento em que a marca GTA VI precisa aparecer integrada à arte."
        elif "official_cover_art" in stem.casefold():
            use = "Capa, abertura, encerramento e divulgação geral do jogo; não representa uma cena literal do gameplay."
        else:
            use = "Fundo de cartela, thumbnail, transição ou apoio editorial; distinguir artwork de screenshot do jogo."
        return "artwork / wallpaper", humanize(subject), variant, use

    if "gtavi_ultimate_edition_benefits" in lower_parts:
        subject = re.sub(r"_\d+$", "", stem.replace("ULTIMATE_EDITION_", ""))
        if subject.isdigit() or not subject:
            subject = "Visão geral da Ultimate Edition"
        else:
            subject = humanize(subject)
        return "benefício — Ultimate Edition", subject, "imagem oficial", (
            f"Usar somente em conteúdo sobre a Ultimate Edition ou o benefício “{subject}”; não atribuir ao jogo-base."
        )

    if "gtavi_vintage_vice_city_pack" in lower_parts:
        subject = re.sub(r"_\d+$", "", stem.replace("VINTAGE_VICE_CITY_PACK_", ""))
        subject = "Visão geral do pacote" if subject.isdigit() or not subject else humanize(subject)
        return "benefício — Vintage Vice City Pack", subject, "imagem oficial", (
            f"Usar somente em conteúdo sobre o Vintage Vice City Pack ou “{subject}”; não atribuir ao jogo-base."
        )

    return "imagem", humanize(stem), "imagem", "Revisar visualmente antes de atribuir uma função editorial."


def image_metadata(path: Path) -> dict[str, object]:
    with Image.open(path) as image:
        width, height = image.size
        return {
            "width": width,
            "height": height,
            "orientation": orientation(width, height),
            "duration_seconds": None,
            "fps": None,
            "video_codec": None,
            "audio_codec": None,
        }


def video_metadata(path: Path) -> dict[str, object]:
    with av.open(str(path)) as container:
        video = next((stream for stream in container.streams if stream.type == "video"), None)
        audio = next((stream for stream in container.streams if stream.type == "audio"), None)
        duration = container.duration / av.time_base if container.duration else None
        width = video.codec_context.width if video else 0
        height = video.codec_context.height if video else 0
        fps = float(video.average_rate) if video and video.average_rate else None
        return {
            "width": width,
            "height": height,
            "orientation": orientation(width, height) if width and height else None,
            "duration_seconds": round(duration, 3) if duration else None,
            "fps": round(fps, 3) if fps else None,
            "video_codec": video.codec_context.name if video else None,
            "audio_codec": audio.codec_context.name if audio else None,
        }


def short_hash(path: Path) -> str:
    digest = hashlib.sha256()
    size = path.stat().st_size
    with path.open("rb") as handle:
        digest.update(handle.read(1024 * 1024))
        if size > 2 * 1024 * 1024:
            handle.seek(max(0, size - 1024 * 1024))
            digest.update(handle.read(1024 * 1024))
    digest.update(str(size).encode("ascii"))
    return digest.hexdigest()[:16]


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidate = Path("C:/Windows/Fonts/arial.ttf")
    return ImageFont.truetype(str(candidate), size) if candidate.is_file() else ImageFont.load_default()


def fit_thumb(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, "#11131a")
    fitted = ImageOps.contain(image.convert("RGB"), size, Image.Resampling.LANCZOS)
    canvas.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return canvas


def contact_sheet(items: list[tuple[Image.Image, str]], destination: Path, columns: int = 3) -> None:
    thumb_size = (480, 270)
    label_height = 58
    rows = (len(items) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_size[0], rows * (thumb_size[1] + label_height)), "#090a0f")
    draw = ImageDraw.Draw(sheet)
    label_font = font(18)
    for index, (image, label) in enumerate(items):
        x = (index % columns) * thumb_size[0]
        y = (index // columns) * (thumb_size[1] + label_height)
        sheet.paste(fit_thumb(image, thumb_size), (x, y))
        clipped = label if len(label) <= 52 else label[:49] + "..."
        draw.text((x + 10, y + thumb_size[1] + 8), clipped, fill="#ffffff", font=label_font)
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, quality=90)


def make_image_sheets(image_paths: list[Path]) -> None:
    groups: dict[Path, list[Path]] = defaultdict(list)
    for path in image_paths:
        groups[path.parent].append(path)
    for folder, paths in groups.items():
        items: list[tuple[Image.Image, str]] = []
        for path in sorted(paths, key=lambda item: natural_key(item.name)):
            with Image.open(path) as image:
                items.append((image.copy(), path.name))
        safe_name = "__".join(folder.relative_to(MEDIA_ROOT).parts)
        contact_sheet(items, OUTPUT / "folhas_imagens" / f"{safe_name}.jpg")


def video_frames(path: Path, count: int) -> list[tuple[Image.Image, str]]:
    frames: list[tuple[Image.Image, str]] = []
    with av.open(str(path)) as container:
        stream = next(stream for stream in container.streams if stream.type == "video")
        duration = container.duration / av.time_base if container.duration else 0
        for index in range(count):
            second = duration * (index + 0.5) / count
            container.seek(int(second * av.time_base), any_frame=False, backward=True)
            frame = next(container.decode(stream), None)
            if frame is None:
                continue
            frames.append((frame.to_image(), f"{second:07.2f}s"))
    return frames


def make_video_sheets(video_paths: list[Path]) -> None:
    for path in video_paths:
        count = 15 if "Extended_Look" in path.name else 12 if "Trailer" in path.name else 6
        frames = video_frames(path, count)
        contact_sheet(frames, OUTPUT / "folhas_videos" / f"{path.stem}.jpg")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = sorted(
        (path for path in MEDIA_ROOT.rglob("*") if path.is_file() and OUTPUT not in path.parents),
        key=lambda item: natural_key(str(item.relative_to(MEDIA_ROOT))),
    )
    rows: list[dict[str, object]] = []
    image_paths: list[Path] = []
    video_paths: list[Path] = []
    for index, path in enumerate(files, 1):
        suffix = path.suffix.casefold()
        if suffix in IMAGE_EXTENSIONS:
            metadata = image_metadata(path)
            media_type = "image"
            image_paths.append(path)
        elif suffix in VIDEO_EXTENSIONS:
            metadata = video_metadata(path)
            media_type = "video"
            video_paths.append(path)
        else:
            continue
        category, subject, variant, recommended_use = classify(path)
        rows.append({
            "id": f"GTA6-{index:03d}",
            "relative_path": path.relative_to(MEDIA_ROOT).as_posix(),
            "file_name": path.name,
            "media_type": media_type,
            "category": category,
            "subject": subject,
            "variant": variant,
            "width": metadata["width"],
            "height": metadata["height"],
            "orientation": metadata["orientation"],
            "duration_seconds": metadata["duration_seconds"],
            "fps": metadata["fps"],
            "video_codec": metadata["video_codec"],
            "audio_codec": metadata["audio_codec"],
            "size_bytes": path.stat().st_size,
            "fingerprint": short_hash(path),
            "recommended_use": recommended_use,
        })

    fieldnames = list(rows[0])
    with (OUTPUT / "inventario_midia.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    (OUTPUT / "inventario_midia.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    make_image_sheets(image_paths)
    make_video_sheets(video_paths)
    print(json.dumps({"files": len(rows), "images": len(image_paths), "videos": len(video_paths)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
