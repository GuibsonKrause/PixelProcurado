"""Montagem V2 genérica: cards Hyperframes + legendas ASS/SRT + cortes FFmpeg, guiada por episodio.json.

Uso: py -3.12 automacao/pipeline/produzir_v2.py --episodio producao/L08 [--formato longo|short|ambos]
     [--amostra INICIO-FIM] [--saida DIR] [--dry-run]
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from comum import (FF, GSAP_PADRAO, SLUG, caminho, carregar, erro, escala, formatos,
                   nome_saida, pastas, parse_amostra, planos, selecionar, vertical)

SLOT = 0.8   # janela de cada card no .mov de painéis
ANIM = 0.8   # duração do trecho de painel usado por plano


def run(args):
    return subprocess.run([str(FF), "-hide_banner", "-nostdin", "-loglevel", "error", "-y",
                           *map(str, args)], check=True)


def panel_art(kind):
    if kind == "data":
        return '<rect x="17" y="23" width="120" height="86" rx="8"/><path d="M17 44h120M48 128h58m-29-19v19M34 76h80m-80 11h47"/>'
    if kind == "tag":
        return '<path d="M15 93V74l16-16 15-28h61l16 28 16 16v19H15zm16-35h92M23 95v18h20V95m69 0v18h20V95M29 77h16m66 0h16"/>'
    return '<circle cx="77" cy="76" r="49"/><circle cx="77" cy="76" r="30"/><path d="M77 8v25m0 86v25M8 76h25m87 0h26"/>'


def prepare_hyperframes(direction, out_html, kicker, gsap_src):
    out_html.parent.mkdir(parents=True, exist_ok=True)
    slides = []
    for i, p in enumerate(q for q in direction if not q.get("sem_card")):
        title, detail, kind = p["titulo"], p["detalhe"], p["tipo"]
        words = "".join(f'<span>{html.escape(word)} </span>' for word in title.split())
        compact = " compact" if len(title) > 21 else ""
        slides.append(f'''<section class="clip {kind}{compact}" id="p{i}" data-start="{i*SLOT:.2f}" data-duration="{SLOT}" data-track-index="1">
        <div class="card"><div class="accent"></div><div class="content">
        <div class="kicker">{kicker}</div>
        <div class="headline">{words}</div>
        <div class="detail">{html.escape(detail)}</div>
        </div><div class="sweep"></div><svg viewBox="0 0 154 152" aria-hidden="true">{panel_art(kind)}</svg></div></section>''')
    page = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Pixel Procurado · Motion</title>
<script src="gsap.min.js"></script>
<style>
*{{box-sizing:border-box}}html,body{{margin:0;background:transparent;font-family:Arial,sans-serif}}
#motion,.clip{{position:absolute;inset:0;width:900px;height:250px;overflow:hidden}}
.card{{position:absolute;inset:20px 16px;background:linear-gradient(115deg,#101218f0,#1a1c23eb);
border:1px solid #ffffff30;border-radius:13px;box-shadow:0 7px 18px #0008;color:#fff;overflow:hidden}}
.content{{position:absolute;left:30px;top:27px;width:668px}}.accent{{position:absolute;left:0;top:0;bottom:0;width:4px;background:#ffd33d;box-shadow:0 0 22px #ffd33d77}}
.kicker{{font:700 19px Consolas,monospace;color:#ffd33d;letter-spacing:3px}}.kicker b{{color:#858585}}
.headline{{font-size:43px;font-weight:900;letter-spacing:-1.4px;margin-top:15px;line-height:1.08}}
.headline span{{display:inline-block;white-space:pre;opacity:0}}
.editorial.compact .headline{{font-size:37px;letter-spacing:-1px;white-space:nowrap}}
.detail{{font-size:22px;color:#d3d6de;margin-top:12px;line-height:1.15;max-width:650px;opacity:0}}
svg{{position:absolute;right:24px;top:38px;width:117px;height:128px;fill:none;stroke:#ffd33d;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;opacity:0}}
.sweep{{position:absolute;left:30px;bottom:19px;width:270px;height:2px;background:linear-gradient(90deg,#ffd33d,transparent);transform-origin:left}}
.tag .card{{inset:48px 16px;border-radius:60px;background:#11141af2;border-color:#ffd33d66}}
.tag .content{{top:22px;left:42px;width:780px}}
.tag .headline{{margin-top:13px;font-size:46px}}
.tag .detail,.tag svg,.tag .sweep{{display:none}}
.tag .accent{{width:9px}}
.data .card{{background:linear-gradient(100deg,#302a12f5,#13161bf5)}}
.data .headline{{color:#ffd33d;font-size:51px;margin-top:11px}}
.data svg{{stroke:#fff}}
</style><body><div id="motion" data-composition-id="motion" data-start="0" data-width="900" data-height="250" data-duration="{len(slides)*SLOT:.2f}">
{''.join(slides)}
</div><script>
const tl=gsap.timeline({{paused:true}});
document.querySelectorAll(".clip").forEach((s,i)=>{{
 const t=i*{SLOT};
 const card=s.querySelector(".card");
 const tag=s.classList.contains("tag"), data=s.classList.contains("data");
 tl.fromTo(card,{{x:tag||data?0:-38,y:tag?20:data?26:0,scale:tag?.94:1,rotationY:tag||data?0:12,opacity:0,clipPath:tag?"inset(0 0% 0 0 round 60px)":"inset(0 96% 0 0 round 13px)"}},{{x:0,y:0,scale:1,rotationY:0,opacity:1,clipPath:"inset(0 0% 0 0 round 13px)",duration:.23,ease:tag?"back.out(1.5)":"expo.out",immediateRender:false}},t);
 tl.fromTo(s.querySelectorAll(".headline span"),{{y:20,opacity:0,rotationX:-35}},{{y:0,opacity:1,rotationX:0,duration:.18,stagger:.018,ease:"power3.out",immediateRender:false}},t+.06);
 tl.fromTo(s.querySelector("svg"),{{scale:.65,rotation:16,opacity:0}},{{scale:1,rotation:0,opacity:1,duration:.25,ease:"back.out(1.8)",immediateRender:false}},t+.09);
 tl.fromTo(s.querySelector(".detail"),{{y:8,opacity:0}},{{y:0,opacity:1,duration:.15,ease:"power2.out",immediateRender:false}},t+.20);
 tl.fromTo(s.querySelector(".sweep"),{{scaleX:0}},{{scaleX:1,duration:.25,ease:"expo.out",immediateRender:false}},t+.08);
 tl.to(s.querySelectorAll(".headline span"),{{y:-8,opacity:0,stagger:.012,duration:.12,ease:"power2.in"}},t+.46);
 tl.to(card,{{x:32,opacity:0,clipPath:"inset(0 0 0 100% round 13px)",duration:.24,ease:"power3.inOut"}},t+.53);
}});
window.__timelines={{motion:tl}};
</script></body></html>'''
    out_html.write_text(page, encoding="utf-8")
    ref = caminho(gsap_src)
    if ref.is_file() and not (out_html.parent / "gsap.min.js").is_file():
        (out_html.parent / "gsap.min.js").write_bytes(ref.read_bytes())


def card_duration(p, frames, fps):
    tag = p["tipo"] == "tag"
    words = len((p["titulo"] if tag else p["titulo"] + " " + p["detalhe"]).split())
    reading = min(5.4, max(2.5, 0.85 + words / 3.4))
    return min(frames / fps - 0.1, reading)


def card_position(p, fmt):
    position = p.get("card_posicao", (150, 1060) if vertical(fmt) else (58, 730))
    if (not isinstance(position, (list, tuple)) or len(position) != 2
            or any(isinstance(v, bool) or not isinstance(v, (int, float))
                   or not math.isfinite(v) or v < 0 for v in position)):
        raise ValueError("card_posicao deve ser [x, y] com números finitos e não negativos")
    k = escala(fmt)
    x, y = (round(v * k) for v in position)
    if "card_posicao" in p:
        width = round((780 if vertical(fmt) else 720) * k)
        height = 2 * round(width * 250 / 900 / 2)
        if x + width > fmt["resolucao"][0] or y + height > fmt["resolucao"][1]:
            raise ValueError("card_posicao deve manter o painel inteiro dentro da resolução de saída")
    return x, y


def fix_word(word, fixes):
    return re.sub(r"[\wÀ-ÿ]+", lambda m: fixes.get(m[0].casefold(), m[0]), word)


def stamp(seconds, scale, sep):
    units = round(max(0, seconds) * scale)
    return f"{units//(3600*scale):02}:{units//(60*scale)%60:02}:{units//scale%60:02}{sep}{units%scale:0{len(str(scale))-1}}"


def legenda_margem(a, b, altas, fmt):
    """MarginV (px) para a legenda [a,b] se ela cair majoritariamente num plano com `legenda_alta`; senão None."""
    k, vert = escala(fmt), vertical(fmt)
    for pa, pb, valor in altas:
        if min(b, pb) - max(a, pa) >= (b - a) / 2:
            base = (350 if vert else 300) if valor is True else float(valor)
            return round(base * k)
    return None


def write_subs(stem, entries, fmt, build, out_dir, source_labels, altas=()):
    w, h = fmt["resolucao"]
    k = escala(fmt)
    vert = vertical(fmt)
    font = round((64 if vert else 54) * k)
    margin = round((350 if vert else 80) * k)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pixel,Arial,{font},&H00FFFFFF,&H000000FF,&H00131317,&H80000000,-1,0,0,0,100,100,0,0,1,{round(5*k)},{round(2*k)},2,{round(110*k)},{round(110*k)},{margin},1
Style: Origem,Arial,{round(44*k)},&H003DD3FF,&H000000FF,&H60131317,&H00131317,-1,0,0,0,100,100,0,0,3,{round(9*k)},0,7,{round(58*k)},{round(58*k)},{round((465 if vert else 55)*k)},1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_path = build / f"{stem}.ass"
    with ass_path.open("w", encoding="utf-8-sig") as stream:
        stream.write(header)
        for a, b, t in entries:
            safe = t.replace("{", "(").replace("}", ")").replace("\\", "/")
            mv = legenda_margem(a, b, altas, fmt) or 0
            stream.write(f"Dialogue: 0,{stamp(a,100,'.')},{stamp(b,100,'.')},Pixel,,0,0,{mv},,{safe}\n")
    label_files = {}
    for index, (media, label) in enumerate(source_labels.items()):
        name = f"{stem}_origem_{index}.ass"
        safe = label.replace("{", "(").replace("}", ")").replace("\\", "/")
        (build / name).write_text(
            header + f"Dialogue: 1,0:00:00.00,9:59:59.99,Origem,,0,0,0,,{safe}\n",
            encoding="utf-8-sig",
        )
        label_files[media] = name
    with (out_dir / f"{stem}.srt").open("w", encoding="utf-8") as stream:
        for i, (a, b, t) in enumerate(entries, 1):
            stream.write(f"{i}\n{stamp(a,1000,',')} --> {stamp(b,1000,',')}\n{t}\n\n")
    return label_files


def build_captions(words, total_duration, fixes):
    entries, batch = [], []
    for w in words:
        batch.append(w)
        if len(batch) >= 6 or (len(batch) >= 3 and w["word"].endswith((".", "?", "!"))):
            entries.append((batch[0]["start"], batch[-1]["end"], " ".join(fix_word(x["word"], fixes) for x in batch)))
            batch = []
    if batch:
        entries.append((batch[0]["start"], min(total_duration, batch[-1]["end"]), " ".join(fix_word(x["word"], fixes) for x in batch)))
    res = []
    for i, (a, b, text) in enumerate(entries):
        next_a = entries[i+1][0] if i+1 < len(entries) else total_duration
        end_time = min(max(b, a + 0.65), next_a)
        if end_time > a:
            res.append((a, end_time, text))
    return res


def _sha(path):
    path = Path(path)
    return hashlib.sha1(path.read_bytes()).hexdigest() if path.is_file() else ""


def assinatura(p, ctx):
    """Hash de tudo que define o clipe de um plano; muda -> o clipe é refeito em vez de reaproveitado."""
    build = ctx["build"]
    label = ctx["label_files"].get(p["midia"])
    dado = {"plano": {k: v for k, v in p.items()}, "res": ctx["fmt"]["resolucao"], "fps": ctx["fps"],
            "kbps": ctx.get("kbps"), "midia": ctx["midias"].get(p["midia"], p["midia"]),
            "ass": _sha(build / f"{ctx['stem']}.ass"), "selo": _sha(build / label) if label else "",
            "paineis": ctx.get("paineis_sig", "") if p.get("card_i") is not None else ""}
    return hashlib.sha1(json.dumps(dado, sort_keys=True, default=str, ensure_ascii=False).encode()).hexdigest()


def cut_shot(job):
    p, ctx = job
    build, fmt, fps = ctx["build"], ctx["fmt"], ctx["fps"]
    out = build / ctx["stem"] / f"{p['i']:02d}.mp4"
    # reaproveita o clipe só se nada que entra nele mudou (plano, formato, legenda/selo queimados, painel do card)
    sig_file = out.with_suffix(".sig")
    sig = assinatura(p, ctx)
    if out.exists() and out.stat().st_size > 1024 and sig_file.is_file() and sig_file.read_text() == sig:
        return out
    count = p["n"]
    k, vert = escala(fmt), vertical(fmt)
    even = lambda v: 2 * round(v / 2)
    conter = p.get("enquadramento") == "conter"
    # O layout vertical padrão usa um miolo 16:9 sobre o fundo desfocado.
    bw, bh = (even(1920 * k), even(1080 * k)) if vert and not conter else fmt["resolucao"]
    source_path = ctx["fontes"] / ctx["midias"].get(p["midia"], p["midia"])
    is_image = source_path.suffix.lower() in (".jpg", ".jpeg", ".png")
    if is_image:
        inputs = ["-loop", "1"]
        hw = []
    else:
        inputs = ["-ss", str(p["inicio"])]
        hw = ["-hwaccel", ctx["hwaccel"]] if ctx.get("hwaccel") else []
    inputs += ["-t", f"{count/fps+0.05:.6f}", "-threads", "2", "-i", str(source_path)]
    # "recorte": [x, y, w, h] em pixels da fonte — tira facecam/chat/HUD de capturas de terceiros antes de escalar
    rc = p.get("recorte")
    pre = f"crop={rc[2]}:{rc[3]}:{rc[0]}:{rc[1]}," if rc else ""
    # "mascaras": [[x, y, w, h], ...] em pixels da fonte — apaga (delogo) facecam/alertas quando o quadro inteiro
    # precisa ficar (ex.: estrelas no topo direito) e o recorte não serve
    pre = "".join(f"delogo=x={x}:y={y}:w={w}:h={h}," for x, y, w, h in p.get("mascaras") or []) + pre
    flags = "lanczos" if rc else "fast_bilinear"
    if conter:
        filters = [
            f"[0:v]{pre}scale={bw}:{bh}:force_original_aspect_ratio=decrease:force_divisible_by=2,"
            f"setsar=1,format=yuv420p,pad={bw}:{bh}:(ow-iw)/2:(oh-ih)/2:color=0x242424,"
            f"fps={fps},trim=end_frame={count},setpts=PTS-STARTPTS[base]"
        ]
    elif is_image:
        dur = count / fps
        zw, zh = even(bw * 1.12), even(bh * 1.12)
        px, py = ("(in_w-out_w)*t/%.3f" % dur, "(in_h-out_h)*t/%.3f" % dur) if p["i"] % 2 else ("(in_w-out_w)*(1-t/%.3f)" % dur, "(in_h-out_h)*(1-t/%.3f)" % dur)
        if p.get("movimento") == "fixo":   # sem zoom/pan: a imagem só preenche o quadro, parada
            filters = [f"[0:v]scale={bw}:{bh}:force_original_aspect_ratio=increase,fps={fps},crop={bw}:{bh},trim=end_frame={count},setpts=PTS-STARTPTS[base]"]
        else:
            filters = [f"[0:v]scale={zw}:{zh}:force_original_aspect_ratio=increase,fps={fps},crop={bw}:{bh}:'{px}':'{py}',trim=end_frame={count},setpts=PTS-STARTPTS[base]"]
    else:
        # no vertical, o ramo do fundo desfocado (split -> boxblur) saía com metade verde chapada quando o quadro vinha do
        # d3d11va: forçar yuv420p logo depois do scale evita o defeito (conferido por quadro; o horizontal não muda)
        fmt_px = ",format=yuv420p" if vert else ""
        filters = [f"[0:v]{pre}scale={bw}:{bh}:flags={flags},setsar=1{fmt_px},fps={fps},trim=end_frame={count},setpts=PTS-STARTPTS[base]"]
    tem_card = p.get("card_i") is not None
    if tem_card:
        visible = card_duration(p, count, fps)
        hold = max(0, round((visible - ANIM) * fps))
        panel_width = round((780 if vert else 720) * k)
        inputs += ["-ss", f"{p['card_i']*SLOT:.2f}", "-t", str(ANIM), "-i", str(ctx["panels"])]
        filters.append(f"[1:v]fps={fps},format=rgba,scale={panel_width}:-2,"
                       f"setpts='PTS-STARTPTS+gte(N,{round(0.4*fps)})*{hold}/{fps}/TB',fps={fps}[panel]")
    if vert and not conter:
        w, h = fmt["resolucao"]
        sw, sh = round(270 * k), round(480 * k)
        filters += [
            "[base]split[raw][blur]",
            f"[blur]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},boxblur=10:1,scale={w}:{h},eq=brightness=-0.29[bg]",
            f"[raw]scale={w}:{even(w*9/16)}[fg]",
            f"[bg][fg]overlay=0:{round(425*k)}[canvas]",
        ]
    canvas = "canvas" if vert and not conter else "base"
    if tem_card:
        x, y = card_position(p, fmt)
        filters.append(f"[{canvas}][panel]overlay={x}:{y}:"
                       f"eof_action=pass:enable='lt(t,{visible:.6f})'[vcard]")
    else:
        filters.append(f"[{canvas}]null[vcard]")
    label_file = ctx["label_files"].get(p["midia"]) if p.get("selo", True) is not False else None
    label_filter = f"ass=filename={label_file}," if label_file else ""
    filters.append(f"[vcard]{label_filter}setpts=PTS+{p['offset']/fps:.8f}/TB,ass=filename={ctx['stem']}.ass,setpts=PTS-STARTPTS[v]")
    temp = out.with_suffix(".part.mp4")
    # sem limite: intermediário quase sem perda (ultrafast crf 17). Com `limite_mb`: um único encode já no teto
    # de bitrate do destino (preset medium + VBV), em vez de gerar o arquivo grande e recomprimir depois.
    kbps = ctx.get("kbps")
    codec = (["-preset", "medium", "-crf", "20", "-maxrate", f"{kbps}k", "-bufsize", f"{2*kbps}k", "-profile:v", "high"]
             if kbps else ["-preset", "ultrafast", "-crf", "17"])
    args = ["-filter_complex_threads", "3", "-filter_complex", ";".join(filters), "-map", "[v]",
            "-frames:v", str(count), "-an", "-c:v", "libx264", *codec,
            "-pix_fmt", "yuv420p", "-r", str(fps), "-video_track_timescale", str(fps * 1000), str(temp)]
    try:
        run([*hw, *inputs, *args])
    except subprocess.CalledProcessError:
        if not hw:
            raise
        # decodificação por GPU indisponível/instável nesta fonte: repete na CPU (mesmos quadros, só mais lento)
        print(f"Plano {p['i']+1:02d}: hwaccel {ctx['hwaccel']} falhou, repetindo na CPU", flush=True)
        run([*inputs, *args])
    temp.replace(out)
    got = contar_quadros(out)
    if got != count:
        out.unlink(missing_ok=True)
        raise RuntimeError(f"plano {p['i']+1}: clipe com {got} quadros, esperado {count}")
    sig_file.write_text(sig)
    print(f"Plano {p['i']+1:02d} concluído ({count} frames)", flush=True)
    return out


def contar_quadros(path):
    """Quadros de vídeo do arquivo (conta pacotes; rápido, sem decodificar). None se não der para ler."""
    ffprobe = shutil.which("ffprobe") or "ffprobe"
    res = subprocess.run([ffprobe, "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_packets", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return int(res.stdout.strip().split(",")[0])
    except ValueError:
        return None


def insumos_ausentes(ep, fmt, selecionados):
    fontes = caminho(ep.get("pasta_fontes", "videosGTAVI"))
    midias = ep.get("midias", {})
    falta = [f"mídia do plano {p['i']+1}: {fontes / midias.get(p['midia'], p['midia'])}"
             for p in selecionados if not (fontes / midias.get(p["midia"], p["midia"])).is_file()]
    falta += [f"{c}: {caminho(fmt[c])}" for c in ("voz", "alinhamento") if not caminho(fmt[c]).is_file()]
    return falta


def render_movie(ep, nome, fmt, amostra, build, out_dir, dry, hwaccel=None):
    fps = fmt.get("fps", 60)
    slug, stem = SLUG[nome], fmt["stem"]
    source_labels = ep.get("rotulos_obrigatorios", {})
    if source_labels:
        fmt = {**fmt, "planos": [
            {**p, "sem_card": True}
            if p.get("titulo") == source_labels.get(p["midia"]) else p
            for p in fmt["planos"]
        ]}
    todos = planos(fmt)
    sel = selecionar(todos, amostra)
    for p in sel:
        if p.get("card_i") is not None:
            card_position(p, fmt)
    falta = insumos_ausentes(ep, fmt, sel)
    total = todos[-1]["fim_s"]
    print(f"[{nome}] {fmt['resolucao'][0]}x{fmt['resolucao'][1]} @{fps}fps, {len(todos)} planos "
          f"({total:.2f}s); renderizar {len(sel)}: planos {sel[0]['i']+1}..{sel[-1]['i']+1}")
    if dry:
        for p in sel:
            print(f"   {p['i']+1:02d} {p['inicio_s']:7.2f}-{p['fim_s']:7.2f}s {p['n']:5d}q {p['tipo']:9s} {p['titulo']} <- {p['midia']}@{p['inicio']}")
        print(f"   saída: {out_dir / (nome_saida(fmt, amostra) + '.mp4')}")
        print("   insumos: " + ("OK" if not falta else "FALTAM " + "; ".join(falta)))
        return None
    if falta:
        erro("insumos ausentes: " + "; ".join(falta))
    out_dir.mkdir(parents=True, exist_ok=True)
    (build / stem).mkdir(parents=True, exist_ok=True)

    hf_html = build / f"hyperframes_{slug}" / "index.html"
    panels = build / f"paineis_{slug}.mov"
    prepare_hyperframes(fmt["planos"], hf_html, ep.get("kicker", "PIXEL PROCURADO <b> / </b> GTA VI"),
                        ep.get("gsap", GSAP_PADRAO))
    # o .mov de painéis vale enquanto o index.html (textos/ordem dos cards) for o mesmo que o gerou
    paineis_sig = _sha(hf_html)
    panels_sig_file = panels.with_suffix(".sig")
    panels_ok = (panels.is_file() and panels.stat().st_size >= 1000 and panels_sig_file.is_file()
                 and panels_sig_file.read_text() == paineis_sig)
    if any(p["card_i"] is not None for p in sel) and not panels_ok:
        print(f"Renderizando painéis Hyperframes para {stem}...", flush=True)
        res = subprocess.run(["hyperframes.cmd", "render", str(hf_html.parent), "--format", "mov", "-f", str(fps), "-o", str(panels)],
                             cwd=str(build), capture_output=True, text=True)
        if res.returncode != 0:
            print("Hyperframes stderr:", res.stderr)
            raise RuntimeError(f"Falha no render Hyperframes: {res.stderr}")
        panels_sig_file.write_text(paineis_sig)

    words = json.loads(caminho(fmt["alinhamento"]).read_text(encoding="utf-8"))
    altas = [(p["inicio_s"], p["fim_s"], p["legenda_alta"]) for p in todos if p.get("legenda_alta")]
    label_files = write_subs(stem, build_captions(words, total, ep.get("correcoes_legenda", {})),
                             fmt, build, out_dir, source_labels, altas)

    limite_mb = fmt.get("limite_mb")
    kbps = None
    if limite_mb:   # orçamento: 92% do limite (margem de contêiner/VBV) menos o áudio de 192 kbps
        kbps = int(limite_mb * 0.92 * 8192 / total - 192)
        if kbps < 1500:
            erro(f"limite_mb={limite_mb} dá só {kbps} kbps de vídeo para {total:.0f}s; reduza a resolução ou aumente o limite")
        print(f"limite_mb={limite_mb}: vídeo com teto de {kbps} kbps (encode único, preset medium)", flush=True)
    ctx = {"build": build, "fmt": fmt, "fps": fps, "stem": stem, "panels": panels, "hwaccel": hwaccel, "kbps": kbps,
           "paineis_sig": paineis_sig,
           "midias": ep.get("midias", {}), "fontes": caminho(ep.get("pasta_fontes", "videosGTAVI")),
           "label_files": label_files}
    print(f"Iniciando renderização de {len(sel)} planos ({sum(p['n'] for p in sel)} frames)...", flush=True)
    with ThreadPoolExecutor(max_workers=2) as executor:
        clips = list(executor.map(cut_shot, [(p, ctx) for p in sel]))
    ruins = [p["i"] + 1 for clip, p in zip(clips, sel) if not clip.is_file() or clip.stat().st_size < 1024]
    if ruins:
        erro(f"clipes ausentes/vazios para os planos {ruins}; nada foi concatenado")

    final = nome_saida(fmt, amostra)
    concat_file = build / f"{final}.ffconcat"
    with concat_file.open("w", encoding="utf-8") as f:
        f.write("ffconcat version 1.0\n")
        for clip, p in zip(clips, sel):
            f.write(f"file '{clip.relative_to(build).as_posix()}'\nduration {p['n']/fps:.9f}\n")
    final_mp4, temp_mp4 = out_dir / f"{final}.mp4", out_dir / f"{final}.part.mp4"
    audio_in = ["-ss", f"{sel[0]['inicio_s']:.3f}", "-t", f"{sum(p['n'] for p in sel)/fps:.6f}"] if amostra else []
    run(["-f", "concat", "-safe", "0", "-i", str(concat_file), *audio_in, "-i", str(caminho(fmt["voz"])),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(temp_mp4)])
    esperado, obtido = sum(p["n"] for p in sel), contar_quadros(temp_mp4)
    if obtido != esperado:
        temp_mp4.unlink(missing_ok=True)
        erro(f"MP4 final com {obtido} quadros, esperado {esperado} (truncado?); {final_mp4.name} NÃO foi gerado")
    mb = temp_mp4.stat().st_size / 1048576
    if limite_mb and not amostra and mb > limite_mb:
        erro(f"MP4 final com {mb:.0f} MB, acima de limite_mb={limite_mb}; {temp_mp4.name} mantido para diagnóstico")
    temp_mp4.replace(final_mp4)
    print(f"Render concluído: {final_mp4} ({mb:.0f} MB)", flush=True)
    return final_mp4


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episodio", required=True, help="pasta do episódio com episodio.json")
    ap.add_argument("--formato", choices=("longo", "short", "ambos"), default="ambos")
    ap.add_argument("--amostra", help="INICIO-FIM em segundos: renderiza só os planos que cobrem o intervalo")
    ap.add_argument("--saida", help="pasta base de saída (montagem/ e exportacoes/); com --amostra o padrão é <episodio>/amostra")
    ap.add_argument("--dry-run", action="store_true", help="só valida insumos e imprime o plano, sem gravar nada")
    ap.add_argument("--hwaccel", default="d3d11va",
                    help="decodificação das fontes por GPU (padrão d3d11va; quadros idênticos aos da CPU, com "
                         "repetição automática na CPU se falhar); 'nenhum' desliga")
    a = ap.parse_args()
    ep = carregar(a.episodio)
    amostra = parse_amostra(a.amostra)
    build, out_dir = pastas(ep, a.saida, amostra)
    if not a.dry_run:
        build.mkdir(parents=True, exist_ok=True)
        os.chdir(build)  # o filtro `ass` usa caminho relativo
    for nome in formatos(ep, a.formato):
        try:
            render_movie(ep, nome, ep["formatos"][nome], amostra, build, out_dir, a.dry_run,
                         None if a.hwaccel.lower() in ("nenhum", "none", "cpu") else a.hwaccel)
        except subprocess.CalledProcessError as e:
            sys.exit(f"ERRO: FFmpeg falhou (código {e.returncode}) no formato {nome}")
        except RuntimeError as e:
            sys.exit(f"ERRO: {e}")


if __name__ == "__main__":
    main()
