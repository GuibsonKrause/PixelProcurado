"""Pré-voo da montagem V2: confere a direção do episodio.json ANTES do render (segundos por plano, não horas).

Uso: py -3.12 automacao/pipeline/prevoo_v2.py --episodio producao/L08 [--formato longo|short|ambos] [--sem-folhas]

Verifica, por formato:
- ERRO  timeline x narração: fim do último plano difere da duração da voz além da tolerância do QA (0,35 s);
- ERRO  quadros pretos dentro da janela exata de cada plano de vídeo (blackdetect d=0.15, igual ao QA);
- ERRO  janela que passa do fim da fonte;
- ERRO  rótulo obrigatório ausente: `"rotulos_obrigatorios": {"GTAV": "GTA V"}` no episodio.json exige que todo plano
        dessa mídia tenha o selo persistente (padrão; `"selo": false` desliga) ou card cujo título contenha o texto;
        os planos cobertos pelo selo saem como INFO;
- AVISO janelas sobrepostas da mesma fonte (repetição de trecho).
Gera folhas de contato em <episodio>/montagem/prevoo/<stem>_NN.jpg com 3 quadros por plano (início, meio, fim da
janela) ao lado do número do plano, tempo no vídeo, fonte e card — para conferir se a imagem mostra o que o card e a
fala afirmam (trocas de cena dentro da janela aparecem aqui). Sai com código 1 se houver ERRO.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from comum import FF, ROOT, caminho, carregar, formatos, planos

sys.path[:0] = [str(ROOT / ".production-tools/python"), str(ROOT / ".course-tools")]
TOL_AV = 0.35
IMAGEM = (".jpg", ".jpeg", ".png")
FFPROBE = shutil.which("ffprobe") or "ffprobe"


def duracao(path):
    out = subprocess.check_output([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(out.decode().strip())


def analisar(job):
    """Uma passada por plano: blackdetect na janela exata e 3 quadros (início, meio, fim) para a folha de contato."""
    p, tmp, fps = job
    red = "scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2"
    saida = str(tmp / f"{p['i']:03d}_%d.jpg")
    if p["imagem"]:
        subprocess.run([str(FF), "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(p["src"]),
                        "-frames:v", "1", "-vf", red, "-start_number", "0", saida], capture_output=True)
        return p, []
    n = max(1, round(p["dur"] * fps))
    sel = f"eq(n,0)+eq(n,{n // 2})+eq(n,{max(0, n - 3)})"
    grafo = (f"[0:v]fps={fps},trim=end_frame={n},scale=320:-2,blackdetect=d=0.15:pic_th=0.98:pix_th=0.10,split[a][b];"
             f"[a]nullsink;[b]select='{sel}',{red}[q]")
    res = subprocess.run([str(FF), "-hide_banner", "-nostats", "-nostdin", "-y", "-ss", str(p["inicio"]),
                          "-t", f"{p['dur'] + 0.2:.3f}", "-i", str(p["src"]), "-an", "-filter_complex", grafo,
                          "-map", "[q]", "-fps_mode", "passthrough", "-start_number", "0", saida],
                         capture_output=True, text=True, errors="replace")
    return p, re.findall(r"black_start:([\d.]+)\s+black_end:([\d.]+)", res.stderr)


def folhas(stem, lista, pasta):
    """Monta as folhas a partir dos quadros já extraídos por analisar() em <pasta>/_q."""
    from PIL import Image, ImageDraw, ImageFont
    try:
        fonte = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    except OSError:
        fonte = ImageFont.load_default()
    tmp = pasta / "_q"
    por_folha, saidas = 10, []
    for n in range(0, len(lista), por_folha):
        bloco = lista[n:n + por_folha]
        folha = Image.new("RGB", (330 + 3 * 322, len(bloco) * 182), (20, 22, 28))
        d = ImageDraw.Draw(folha)
        for r, p in enumerate(bloco):
            y = r * 182
            card = "(sem card)" if p.get("sem_card") else f"{p.get('titulo', '')} | {p.get('detalhe', '')}"
            linhas = [f"PLANO {p['i']+1:02d}   {p['inicio_s']:.1f}-{p['fim_s']:.1f}s ({p['dur']:.1f}s)",
                      f"{p['midia']} @ {p['inicio']} -> {p['inicio'] + p['dur']:.1f}", card[:44], card[44:88]]
            for k, linha in enumerate(linhas):
                d.text((8, y + 10 + 22 * k), linha, font=fonte, fill=(255, 211, 61) if k == 0 else (230, 230, 230))
            if p.get("_erro"):
                d.text((8, y + 110), ("ERRO: " + p["_erro"])[:44], font=fonte, fill=(255, 90, 90))
            for j in range(3):
                arq = tmp / f"{p['i']:03d}_{j}.jpg"
                if arq.is_file():
                    folha.paste(Image.open(arq).convert("RGB"), (330 + j * 322, y + 1))
        saida = pasta / f"{stem}_{n // por_folha + 1:02d}.jpg"
        folha.save(saida, quality=85)
        saidas.append(saida)
    shutil.rmtree(tmp, ignore_errors=True)
    return saidas


def conferir(ep, nome, fmt, fazer_folhas):
    fontes, midias = caminho(ep.get("pasta_fontes", "videosGTAVI")), ep.get("midias", {})
    erros, avisos, lista, dur_fonte = [], [], [], {}
    for p in planos(fmt):
        src = fontes / midias.get(p["midia"], p["midia"])
        p.update(src=src, dur=p["fim_s"] - p["inicio_s"], imagem=src.suffix.lower() in IMAGEM)
        if not src.is_file():
            erros.append(f"plano {p['i']+1}: mídia ausente {src}")
            continue
        lista.append(p)

    voz = caminho(fmt["voz"])
    if voz.is_file() and lista:
        dv, fim = duracao(voz), planos(fmt)[-1]["fim_s"]
        if abs(dv - fim) >= TOL_AV:
            erros.append(f"timeline termina em {fim:.2f}s mas a narração tem {dv:.2f}s (ajuste o fim do último plano)")
    else:
        erros.append(f"voz ausente: {voz}")

    videos = [p for p in lista if not p["imagem"]]
    for p in videos:
        if p["src"] not in dur_fonte:
            dur_fonte[p["src"]] = duracao(p["src"])
        if p["inicio"] + p["dur"] > dur_fonte[p["src"]] + 0.05:
            p["_erro"] = "janela passa do fim da fonte"
            erros.append(f"plano {p['i']+1}: janela {p['midia']}@{p['inicio']}+{p['dur']:.1f}s passa do fim da fonte ({dur_fonte[p['src']]:.1f}s)")
    tmp = ep["_pasta"] / "montagem" / "prevoo" / "_q"
    tmp.mkdir(parents=True, exist_ok=True)
    fps = fmt.get("fps", 60)
    with ThreadPoolExecutor(max_workers=3) as ex:
        for p, achados in ex.map(analisar, [(p, tmp, fps) for p in lista]):
            if achados:
                onde = ", ".join(f"{p['inicio'] + float(a):.2f}-{p['inicio'] + float(b):.2f}s" for a, b in achados)
                p["_erro"] = f"preto na fonte em {onde}"
                erros.append(f"plano {p['i']+1} ({p['inicio_s']:.1f}s do vídeo): quadros pretos em {p['midia']} {onde}")

    cobertos = []
    for midia, texto in ep.get("rotulos_obrigatorios", {}).items():
        for p in lista:
            if p["midia"] != midia:
                continue
            if p.get("selo", True) is not False:   # produzir_v2.py desenha o selo durante o plano inteiro
                cobertos.append(p["i"] + 1)
            elif p.get("sem_card") or texto.lower() not in str(p.get("titulo", "")).lower():
                p.setdefault("_erro", f"sem rótulo '{texto}'")
                erros.append(f"plano {p['i']+1}: mídia {midia} com `selo: false` e sem card com '{texto}' no título")
    if cobertos:
        avisos.append(f"INFO selo persistente cobre {len(cobertos)} plano(s) de rótulo obrigatório: {cobertos}")

    por_fonte = {}
    for p in videos:
        por_fonte.setdefault(p["midia"], []).append(p)
    for midia, ps in por_fonte.items():
        ps = sorted(ps, key=lambda p: p["inicio"])
        for a, b in zip(ps, ps[1:]):
            if b["inicio"] < a["inicio"] + a["dur"] - 0.05:
                avisos.append(f"planos {a['i']+1} e {b['i']+1} repetem trecho de {midia} ({b['inicio']}–{a['inicio'] + a['dur']:.1f}s)")

    print(f"[{nome}] {len(lista)} planos conferidos ({len(videos)} de vídeo): {len(erros)} erro(s), {len(avisos)} aviso(s)")
    for e in erros:
        print("  ERRO  " + e)
    for a in avisos:
        print("  AVISO " + a)
    if not fazer_folhas:
        shutil.rmtree(tmp, ignore_errors=True)
    if fazer_folhas and lista:
        saidas = folhas(fmt["stem"], lista, ep["_pasta"] / "montagem" / "prevoo")
        print(f"  folhas de contato ({len(saidas)}): {saidas[0].parent}  <- olhar antes do render: imagem x card x fala")
    return erros


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episodio", required=True)
    ap.add_argument("--formato", choices=("longo", "short", "ambos"), default="ambos")
    ap.add_argument("--sem-folhas", action="store_true", help="só as verificações automáticas, sem folhas de contato")
    a = ap.parse_args()
    ep = carregar(a.episodio)
    erros = []
    for nome in formatos(ep, a.formato):
        erros += conferir(ep, nome, ep["formatos"][nome], not a.sem_folhas)
    if erros:
        sys.exit(1)
    print("Pré-voo sem erros. Confira as folhas de contato e siga para a amostra/render.")


if __name__ == "__main__":
    main()
