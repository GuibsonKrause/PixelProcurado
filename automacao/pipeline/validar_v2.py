"""QA técnico das exportações V2: blackdetect, loudness (ebur128), decodificação integral,
folha de contato e conferência de dimensões/fps/quadros/duração. Grava <stem>.qa.json em montagem/.

Uso: py -3.12 automacao/pipeline/validar_v2.py --episodio producao/L08 [--formato longo|short|ambos]
     [--amostra INICIO-FIM] [--saida DIR]
"""
import argparse
import json
import re
import shutil
import subprocess

from comum import FF, SLUG, carregar, erro, formatos, nome_saida, pastas, parse_amostra, planos, selecionar

TOL_AV = 0.35  # diferença máxima aceita entre duração de vídeo e de áudio (s)


def validar(ep, nome, fmt, amostra, build, out_dir):
    fps = fmt.get("fps", 60)
    width, height = fmt["resolucao"]
    stem = nome_saida(fmt, amostra)
    slug = SLUG[nome]
    sel = selecionar(planos(fmt), amostra)
    frames = sum(p["n"] for p in sel)
    path = out_dir / f"{stem}.mp4"
    if not path.is_file():
        erro(f"{path} não existe")
    print(f"Validando {nome}: {path.name}...")

    probe = json.loads(subprocess.check_output(
        [shutil.which("ffprobe") or "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]))
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    assert (video["width"], video["height"]) == (width, height), f"Dimensões incorretas: {video['width']}x{video['height']}"
    assert video["codec_name"] == "h264" and audio["codec_name"] == "aac", "Codecs inválidos"
    num, den = map(int, video["avg_frame_rate"].split("/"))
    assert abs(num / den - fps) < .01, f"FPS não é {fps}: {num/den}"

    # decodifica tudo (-xerror aborta em qualquer erro) enquanto mede pretos e loudness
    log = build / f"{stem}.qa.log"
    with log.open("w", encoding="utf-8") as stream:
        subprocess.run([str(FF), "-hide_banner", "-nostats", "-xerror", "-threads", "2",
                        "-i", str(path), "-vf", "blackdetect=d=0.15:pic_th=0.98:pix_th=" + str(fmt.get("black_pix_th", 0.10)),
                        "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "NUL"],
                       check=True, stdout=subprocess.DEVNULL, stderr=stream)
    report = log.read_text(encoding="utf-8")
    black = re.findall(r"black_start:([^\n]+)", report)
    assert not black, f"Detectados intervalos pretos indesejados: {black}"
    levels = re.findall(r"I:\s+(-?[\d.]+) LUFS", report)
    peaks = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", report)

    nb = int(video.get("nb_frames") or 0)
    video_s, audio_s = float(video["duration"]), float(audio["duration"])
    assert abs(nb - frames) <= 1, f"Quadros: {nb}, esperado {frames}"
    assert abs(video_s - frames / fps) < 0.05, f"Duração de vídeo {video_s}s, esperado {frames/fps:.2f}s"
    assert abs(video_s - audio_s) < TOL_AV, f"Áudio ({audio_s}s) e vídeo ({video_s}s) divergem"

    amostras = fmt.get("amostras_contato") if not amostra else None
    if not amostras:
        amostras = [round(video_s * (i + .5) / 8, 2) for i in range(8)]
    captures = build / f"qa_{slug}_v2{'_amostra' if amostra else ''}"
    captures.mkdir(exist_ok=True)
    thumb_w = 270 if height > width else 480
    for i, t in enumerate(amostras):
        subprocess.run([str(FF), "-hide_banner", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(path),
                        "-vf", f"scale={thumb_w}:-2", "-frames:v", "1", str(captures / f"{i:02d}.jpg")], check=True)
    contact = build / f"{slug}_v2_qa{'_amostra' if amostra else ''}.jpg"
    subprocess.run([str(FF), "-hide_banner", "-loglevel", "error", "-y", "-framerate", "1",
                    "-i", str(captures / "%02d.jpg"), "-vf", "tile=4x2", "-frames:v", "1", str(contact)], check=True)

    result = {"arquivo": str(path), "dimensoes": f"{width}x{height}", "fps": num / den,
              "quadros": nb, "quadros_esperados": frames, "video_s": video_s, "audio_s": audio_s,
              "lufs": float(levels[-1]) if levels else None, "peak_dbfs": float(peaks[-1]) if peaks else None,
              "intervalos_pretos": len(black), "folha_contato": str(contact)}
    (build / f"{stem}.qa.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episodio", required=True)
    ap.add_argument("--formato", choices=("longo", "short", "ambos"), default="ambos")
    ap.add_argument("--amostra", help="valida <stem>_amostra.mp4 gerado com o mesmo INICIO-FIM")
    ap.add_argument("--saida", help="mesma pasta base usada em produzir_v2.py")
    a = ap.parse_args()
    ep = carregar(a.episodio)
    amostra = parse_amostra(a.amostra)
    build, out_dir = pastas(ep, a.saida, amostra)
    for nome in formatos(ep, a.formato):
        validar(ep, nome, ep["formatos"][nome], amostra, build, out_dir)
    print("Validação concluída com sucesso.")


if __name__ == "__main__":
    main()
