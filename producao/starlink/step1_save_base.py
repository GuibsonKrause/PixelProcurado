import sys
from pathlib import Path

# Setup paths for PIL
for p in [Path.cwd() / ".production-tools" / "python", Path.cwd() / ".course-tools"]:
    if p.is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from PIL import Image

src = Path(r"C:\Users\guibson.krause\.gemini\antigravity\brain\8cac68d3-885f-41ee-bda7-638dc58b4594\starlink_thumbnail_base_1794075032807.jpg")
dest_dir = Path(r"c:\Users\guibson.krause\Documents\ChatGPT\GamePlay\producao\starlink")
dest_png = dest_dir / "thumbnail_base_gerada.png"

img = Image.open(src)
print(f"Loaded image: size={img.size}, mode={img.mode}, format={img.format}")

# Save as PNG
dest_dir.mkdir(parents=True, exist_ok=True)
img.save(dest_png, format="PNG")
print(f"Saved PNG to {dest_png}, size={dest_png.stat().st_size} bytes")
