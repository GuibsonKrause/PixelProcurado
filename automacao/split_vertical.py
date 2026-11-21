"""Vertical 9:16 em split-screen para clipes de live: webcam em cima (32%), gameplay central embaixo (68%), legenda na divisoria.

  py -3.12 automacao/split_vertical.py <clip.mp4> <legenda.srt> <saida.mp4> [--credito twitch.tv/canal] [--cam '{"x":..,"y":..,"w":..,"h":..}']

A webcam e detectada so com FFmpeg + numpy (bordas retas persistentes entre ~40 quadros; sem OpenCV). A posicao fica em
cache por live (webcam.json na pasta da live no acervo). Sem webcam detectada devolve False e o chamador usa o layout antigo.
Aprovado pelo usuario em 2026-11-20 (teste de 10 s no clipe alanzoka_20261119_001450).
"""
import json, re, subprocess, sys
from pathlib import Path

import numpy as np

TOPO, BASE, W = 620, 1300, 1080  # 32% / 68%


def _ffbin():
    try:
        import captura_live as cl
        return cl.ffbin()
    except Exception:
        return "ffmpeg"


def detectar_webcam(arq):
    """Retorna {"x","y","w","h","conf"} em pixels da fonte, ou None."""
    ff = _ffbin()
    w, h = 960, 540
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                               capture_output=True, text=True).stdout)
    sw = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of",
                             "csv=p=0", str(arq)], capture_output=True, text=True).stdout.strip().split(",")[0])
    n = 40
    raw = subprocess.run([ff, "-loglevel", "error", "-i", str(arq), "-vf", f"fps={n / dur},scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)[: (len(raw) // (w * h)) * w * h].reshape(-1, h, w).astype(np.float32)
    if len(fr) < 8:
        return None
    mx = (np.abs(np.diff(fr, axis=2))[:, :-1, :] > 18).mean(0) > 0.5
    my = (np.abs(np.diff(fr, axis=1))[:, :, :-1] > 18).mean(0) > 0.5
    cols = [c for c in range(w - 1) if mx[:, c].sum() > 0.12 * h]
    rows = [r for r in range(h - 1) if my[r, :].sum() > 0.12 * w]
    cand = []
    for x0 in cols:
        for x1 in cols:
            if x1 - x0 < 80:
                continue
            for y0 in rows:
                for y1 in rows:
                    if y1 - y0 < 50:
                        continue
                    e = (mx[y0:y1, x0].mean() + mx[y0:y1, x1].mean() + my[y0, x0:x1].mean() + my[y1, x0:x1].mean()) / 4
                    ar = (x1 - x0) / (y1 - y0)
                    if e > 0.5 and 0.7 < ar < 2.4 and (x1 - x0) * (y1 - y0) < 0.3 * w * h:
                        cand.append((e, (x1 - x0) * (y1 - y0), x0, y0, x1, y1))
    if not cand:
        return None
    cand.sort(key=lambda c: (round(c[0], 1), c[1]), reverse=True)
    e, _, x0, y0, x1, y1 = cand[0]
    k = sw / w
    return {"x": round(x0 * k), "y": round(y0 * k), "w": round((x1 - x0) * k), "h": round((y1 - y0) * k), "conf": round(e, 2)}


def _t(s):
    h, m, r = s.split(":")
    sec, ms = r.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def _ass_t(x):
    x = max(0, x)
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


def renderizar(clip, srt, out, cam, credito=None, ini=0.0, dur=None, loudnorm="loudnorm=I=-14:TP=-1.5:LRA=11", crf=17):
    clip, out = Path(clip), Path(out)
    ins = 4
    cw = cam["w"] - 2 * ins
    ch = round(cw * TOPO / W / 2) * 2
    cx, cy = cam["x"] + ins, cam["y"] + ins
    gw = round(1080 * W / BASE / 2) * 2
    gx = (1920 - gw) // 2
    ev = []
    if Path(srt).exists():
        for b in re.split(r"\n\s*\n", Path(srt).read_text(encoding="utf-8").strip()):
            ln = b.strip().splitlines()
            if len(ln) < 3:
                continue
            a, z = [_t(p.strip()) for p in ln[1].split("-->")]
            a, z = a - ini, z - ini
            if z <= 0 or (dur and a >= dur):
                continue
            txt = " ".join(ln[2:]).upper().replace("{", "").replace("}", "")
            ev.append(f"Dialogue: 0,{_ass_t(a)},{_ass_t(min(z, dur) if dur else z)},Div,,0,0,0,,"
                      f"{{\\an5\\pos(540,{TOPO})\\fad(60,60)}}{txt}")
    ass = out.with_suffix(".ass")
    ass.write_text("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\n"
                   "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
                   "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
                   "MarginR, MarginV, Encoding\n"
                   "Style: Div,Arial Black,66,&H00FFFFFF,&H000000FF,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,7,4,5,110,110,0,1\n\n"
                   "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
                   + "\n".join(ev) + "\n", encoding="utf-8")
    fc = (f"[0:v]split=2[a][b];[a]crop={cw}:{ch}:{cx}:{cy},scale={W}:{TOPO}:flags=lanczos,setsar=1[cam];"
          f"[b]crop={gw}:1080:{gx}:0,scale={W}:{BASE}:flags=lanczos,setsar=1[gp];[cam][gp]vstack=inputs=2")
    if credito:
        (out.parent / (out.stem + "_cred.txt")).write_text(credito, encoding="utf-8")
        fc += (f",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':textfile={out.stem}_cred.txt:fontcolor=white@0.85:"
               f"fontsize=30:box=1:boxcolor=black@0.45:boxborderw=10:x=60:y={TOPO + 70}")
    fc += f",ass={ass.name},fps=60,format=yuv420p[v]"
    cmd = [_ffbin(), "-y", "-loglevel", "error"]
    if ini:
        cmd += ["-ss", str(ini)]
    if dur:
        cmd += ["-t", str(dur)]
    cmd += ["-i", str(clip.resolve()), "-filter_complex", fc, "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", str(crf),
            "-preset", "fast", "-c:a", "aac", "-b:a", "192k", "-af", loudnorm, "-movflags", "+faststart", out.name]
    subprocess.run(cmd, cwd=out.parent, check=True)
    ass.unlink(missing_ok=True)
    return True


def split_para_clipe(pasta, canal=None):
    """Usado pelo empacotamento: gera vertical.mp4 em split. False => sem webcam (usar layout antigo)."""
    pasta = Path(pasta)
    cache = pasta.parent / "webcam.json"
    cam = None
    if cache.exists():
        try:
            cam = json.loads(cache.read_text(encoding="utf-8"))
        except Exception:
            cam = None
    if not cam:
        cam = detectar_webcam(pasta / "clip.mp4")
        if not cam:
            return False
        cache.write_text(json.dumps(cam), encoding="utf-8")
        try:  # quadro com a caixa detectada, para conferir (corrija editando webcam.json: x,y,w,h em pixels da fonte)
            subprocess.run([_ffbin(), "-y", "-loglevel", "error", "-ss", "3", "-i", str(pasta / "clip.mp4"), "-frames:v", "1",
                            "-vf", f"drawbox=x={cam['x']}:y={cam['y']}:w={cam['w']}:h={cam['h']}:color=red@0.9:t=6",
                            str(cache.parent / "webcam_preview.png")], check=False)
            from live_aviso import avisar
            avisar("Webcam detectada", f"confira {cache.parent / 'webcam_preview.png'}; se errada, edite webcam.json", "info")
        except Exception:
            pass
    cred = f"twitch.tv/{canal}" if canal else None
    renderizar(pasta / "clip.mp4", pasta / "legenda.srt", pasta / "vertical.mp4", cam, cred)
    return True


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("srt"); ap.add_argument("saida")
    ap.add_argument("--credito"); ap.add_argument("--cam")
    ap.add_argument("--ini", type=float, default=0.0); ap.add_argument("--dur", type=float)
    a = ap.parse_args()
    cam = json.loads(a.cam) if a.cam else detectar_webcam(a.clip)
    if not cam:
        sys.exit("webcam nao detectada")
    renderizar(a.clip, a.srt, a.saida, cam, a.credito, a.ini, a.dur)
    print("ok", a.saida, cam)
