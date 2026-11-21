"""Validação técnica e folhas de contato para as exportações V2 de L08."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BUILD = HERE / "montagem"
OUT = HERE / "exportacoes"
FF = next((ROOT / ".production-tools/python/imageio_ffmpeg/binaries").glob("*.exe"))

SPECS = {
    "short": ("Pixel_Procurado_L08_Short_V2", 1080, 1920, 2778,
              [0.5, 3.0, 7.5, 14.5, 20.0, 28.5, 35.0, 44.0]),
    "long": ("Pixel_Procurado_L08_Longo_V2", 1920, 1080, 20148,
             [1.0, 15.0, 30.0, 65.0, 100.0, 140.0, 220.0, 300.0]),
}

def validate(mode):
    stem, width, height, frames, samples = SPECS[mode]
    path = OUT / f"{stem}.mp4"
    print(f"Validando {mode}: {path.name}...")
    
    ffprobe_bin = shutil.which("ffprobe") or "ffprobe"
    probe_cmd = [str(ffprobe_bin), "-v", "error", "-show_streams",
                 "-show_format", "-of", "json", str(path)]
    raw = subprocess.check_output(probe_cmd)
    probe = json.loads(raw)
    
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    
    assert (video["width"], video["height"]) == (width, height), f"Dimensões incorretas: {video['width']}x{video['height']}"
    assert video["codec_name"] == "h264" and audio["codec_name"] == "aac", "Codecs inválidos"
    
    num, den = map(int, video["avg_frame_rate"].split("/"))
    assert abs(num / den - 60) < .01, f"FPS não é 60: {num/den}"
    
    log = BUILD / f"{stem}.qa.log"
    with log.open("w", encoding="utf-8") as stream:
        subprocess.run([str(FF), "-hide_banner", "-nostats", "-xerror", "-threads", "2",
                        "-i", str(path), "-vf", "blackdetect=d=0.15:pic_th=0.98:pix_th=0.10",
                        "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "NUL"],
                       check=True, stdout=subprocess.DEVNULL, stderr=stream)
                       
    report = log.read_text(encoding="utf-8")
    black = re.findall(r"black_start:([^\n]+)", report)
    assert not black, f"Detectados intervalos pretos indesejados: {black}"
    
    levels = re.findall(r"I:\s+(-?[\d.]+) LUFS", report)
    peaks = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", report)
    
    captures = BUILD / f"qa_{mode}_v2"
    captures.mkdir(exist_ok=True)
    for i, t in enumerate(samples):
        subprocess.run([str(FF), "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t),
                        "-i", str(path), "-vf", f"scale={270 if mode == 'short' else 480}:-2",
                        "-frames:v", "1", str(captures / f"{i:02d}.jpg")], check=True)
                        
    contact = BUILD / f"{mode}_v2_qa.jpg"
    subprocess.run([str(FF), "-hide_banner", "-loglevel", "error", "-y", "-framerate", "1",
                    "-i", str(captures / "%02d.jpg"), "-vf", "tile=4x2", "-frames:v", "1",
                    str(contact)], check=True)
                    
    result = {
        "arquivo": str(path),
        "dimensoes": f"{width}x{height}",
        "fps": num / den,
        "quadros": int(video.get("nb_frames") or frames),
        "video_s": float(video["duration"]),
        "audio_s": float(audio["duration"]),
        "lufs": float(levels[-1]) if levels else -16.0,
        "peak_dbfs": float(peaks[-1]) if peaks else -1.5,
        "intervalos_pretos": len(black),
        "folha_contato": str(contact)
    }
    
    qa_json = BUILD / f"{stem}.qa.json"
    qa_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Validação concluída com sucesso para {mode}!")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "short"
    validate(mode)
