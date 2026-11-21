import sys
from pathlib import Path
import math

for p in [Path.cwd() / ".production-tools" / "python", Path.cwd() / ".course-tools"]:
    if p.is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_starlink_logo(output_path: Path):
    # Supersampling 4x
    scale = 4
    w, h = 600 * scale, 160 * scale
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fonts
    # Try Bahnschrift or Arial Bold or Segoe UI
    font_candidates = [
        "C:/Windows/Fonts/bahnschrift.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    font_file = None
    for fc in font_candidates:
        if Path(fc).is_file():
            font_file = fc
            break
    
    font_size = 64 * scale
    font = ImageFont.truetype(font_file, font_size) if font_file else ImageFont.load_default()

    # Starlink wordmark with wide letter spacing
    word = "STARLINK"
    # Kerning / tracking spacing
    # Let's measure each letter
    letter_widths = []
    for char in word:
        bbox = draw.textbbox((0, 0), char, font=font)
        letter_widths.append(bbox[2] - bbox[0])
    
    extra_space = 24 * scale
    total_word_width = sum(letter_widths) + extra_space * (len(word) - 1)
    
    start_x = (w - total_word_width) // 2
    y_text = int(75 * scale)

    # Shadow layer
    shadow_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)

    # Draw shadow for letters
    curr_x = start_x
    for i, char in enumerate(word):
        shadow_draw.text((curr_x + 3 * scale, y_text + 4 * scale), char, font=font, fill=(0, 0, 0, 160))
        curr_x += letter_widths[i] + extra_space

    # Draw Orbital Arc on shadow layer
    # An elegant orbital arc swooping from bottom left (x~10% w, y~90% h)
    # up through middle, peaking at top right (x~90% w, y~20% h)
    arc_points = []
    p0 = (int(0.08 * w), int(0.85 * h))
    p1 = (int(0.35 * w), int(0.20 * h))
    p2 = (int(0.65 * w), int(0.12 * h))
    p3 = (int(0.92 * w), int(0.35 * h))

    # Cubic bezier
    steps = 200
    for s in range(steps + 1):
        t = s / steps
        bx = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
        by = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
        arc_points.append((bx, by))

    # Draw arc shadow
    for i in range(len(arc_points) - 1):
        # taper thickness: starts thin, gets thicker in middle, tapers at end
        progress = i / len(arc_points)
        thickness = int((3 + 7 * math.sin(progress * math.pi)) * scale)
        pt1 = (arc_points[i][0] + 2 * scale, arc_points[i][1] + 4 * scale)
        pt2 = (arc_points[i+1][0] + 2 * scale, arc_points[i+1][1] + 4 * scale)
        shadow_draw.line([pt1, pt2], fill=(0, 0, 0, 140), width=thickness)

    # Blur shadow
    shadow_blurred = shadow_img.filter(ImageFilter.GaussianBlur(radius=3 * scale))
    img.alpha_composite(shadow_blurred)

    # Now draw main text in white #F8FAFC
    curr_x = start_x
    for i, char in enumerate(word):
        # Draw letter
        draw.text((curr_x, y_text), char, font=font, fill="#F8FAFC")
        curr_x += letter_widths[i] + extra_space

    # If char is 'A', in Starlink the A has no crossbar or is stylized. But clean geometric sans is also authentic.
    # Let's add the Starlink orbital arc:
    # We draw the arc with gradient from #F8FAFC to #FFD33D (yellow accent) at the peak/tail
    for i in range(len(arc_points) - 1):
        progress = i / len(arc_points)
        thickness = int((2.5 + 6.5 * math.sin(progress * math.pi)) * scale)
        pt1 = arc_points[i]
        pt2 = arc_points[i+1]
        
        # Color gradient: mostly pure white #F8FAFC, with yellow #FFD33D near the apex/end
        if progress < 0.45:
            color = (248, 250, 252, 255)
        elif progress < 0.85:
            # interpolate white to yellow
            t_col = (progress - 0.45) / 0.4
            r = int(248 + t_col * (255 - 248))
            g = int(250 + t_col * (211 - 250))
            b = int(252 + t_col * (61 - 252))
            color = (r, g, b, 255)
        else:
            color = (255, 211, 61, 255)

        draw.line([pt1, pt2], fill=color, width=thickness)

    # Accent star/satellite dot at the apex of the orbit
    apex_idx = int(0.68 * steps)
    apex_pt = arc_points[apex_idx]
    # Draw glowing yellow dot
    dot_r = int(7 * scale)
    glow_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse(
        (apex_pt[0] - dot_r*2, apex_pt[1] - dot_r*2, apex_pt[0] + dot_r*2, apex_pt[1] + dot_r*2),
        fill=(255, 211, 61, 150)
    )
    glow_draw.ellipse(
        (apex_pt[0] - dot_r, apex_pt[1] - dot_r, apex_pt[0] + dot_r, apex_pt[1] + dot_r),
        fill=(255, 255, 255, 255)
    )
    glow_blurred = glow_img.filter(ImageFilter.GaussianBlur(radius=2 * scale))
    img.alpha_composite(glow_blurred)
    draw.ellipse(
        (apex_pt[0] - int(4*scale), apex_pt[1] - int(4*scale), apex_pt[0] + int(4*scale), apex_pt[1] + int(4*scale)),
        fill="#FFD33D", outline="#FFFFFF", width=int(1.5*scale)
    )

    # Downsample with Lanczos 4x
    final_w, final_h = 600, 160
    logo_final = img.resize((final_w, final_h), Image.Resampling.LANCZOS)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    logo_final.save(output_path, format="PNG")
    print(f"Starlink logo generated: {output_path} ({final_w}x{final_h})")

if __name__ == "__main__":
    out = Path(r"c:\Users\guibson.krause\Documents\ChatGPT\GamePlay\producao\starlink\starlink_logo.png")
    create_starlink_logo(out)
