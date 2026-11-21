import argparse
from concurrent.futures import ThreadPoolExecutor
import html
import json
import math
import os
from pathlib import Path
import re
import subprocess
import wave
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BUILD = HERE / "montagem"
OUT = HERE / "exportacoes"
HF = BUILD / "hyperframes_v2"
FF = next((ROOT / ".production-tools/python/imageio_ffmpeg/binaries").glob("*.exe"))
FPS = 60
SLOT = 0.8
ANIM = 0.8
PANELS = BUILD / "paineis_v2.mov"
VOICE_LONG = HERE / "voz/narracao_normalizada.wav"
VOICE_SHORT = ROOT / "producao/shorts/L08/voz/narracao_normalizada.wav"

EXT = "GTAVI_An_Extended_Look.mp4"
LAUNCH = "GTAVI_Launch_Trailer.mp4"
T1 = "GTAVI_Trailer_1.mp4"
T2 = "GTAVI_Trailer_2.mp4"

BRIAN = "GTAVI_Screenshots/People/Brian Heder/Brian_Heder_04.jpg"
CAL = "GTAVI_Screenshots/People/Cal Hampton/Cal_Hampton_04.jpg"
RAUL = "GTAVI_Screenshots/People/Raul Bautista/Raul_Bautista_02.jpg"
BOOBIE = "GTAVI_Screenshots/People/Boobie Ike/Boobie_Ike_02.jpg"
DREQUAN = "GTAVI_Screenshots/People/DreQuan Priest/DreQuan_Priest_04.jpg"

DIRECTION_LONG = [
    ("O ALUGUEL GRÁTIS", "Jason mora sem pagar aluguel na propriedade de Brian", BRIAN, 0, "tag"),
    ("APRESENTAÇÃO OFICIAL", "O que cada um oferece e espera receber no elenco", LAUNCH, 47, "editorial"),
    ("O VALOR DA MORADIA", "A ajuda que resolve o problema imediato de Jason", EXT, 31, "tag"),
    ("A CAMINHONETE", "Brian Heder e Jason juntos na apresentação", BRIAN, 0, "editorial"),
    ("GENTILEZA OU DÍVIDA?", "Onde termina o favor e começa a cobrança", T2, 15, "editorial"),
    ("A CHAVE DA CASA", "Como recusar o pedido de quem resolve sua moradia?", EXT, 406, "tag"),
    ("A FATURA DO FAVOR", "O aluguel grátis chega em outro formato", T1, 45, "editorial"),
    ("CAL HAMPTON", "Amigo de Jason e associado a Brian", CAL, 0, "tag"),
    ("AMIZADE E NEGÓCIO", "Confiança que torna pedidos difíceis de recusar", EXT, 542, "editorial"),
    ("CONVITE PRA CERVEJA", "O ambiente em que favores se acumulam", T2, 35, "tag"),
    ("EXAMINE O PEDIDO", "Em GTA, misturar dinheiro e amizade custa caro", T1, 50, "editorial"),
    ("RAUL BAUTISTA", "Assaltante experiente com disposição para o risco", RAUL, 0, "tag"),
    ("EXPERIÊNCIA X PRUDÊNCIA", "Confiança demais após várias tentativas certas", EXT, 245, "data"),
    ("O PLANO PERIGOSO", "A calma de quem escolhe onde almoçar", EXT, 691, "editorial"),
    ("DINHEIRO E ARMA", "O universo de risco sem missões inventadas", RAUL, 0, "editorial"),
    ("QUEM PAGA PELO ERRO?", "A assimetria entre propor e sofrer o plano", EXT, 857, "data"),
    ("ONLY RAW RECORDS", "Boobie Ike e Dre'Quan Priest no comando", BOOBIE, 0, "tag"),
    ("JACK OF HEARTS", "Parceria na gravadora e contratação da Real Dimez", DREQUAN, 0, "editorial"),
    ("ENCONTRO DE AMBIÇÕES", "O próximo passo versus proteger o patrimônio", EXT, 1040, "editorial"),
    ("O QUE ARRISCAR?", "Negócios que rendem mais que dinheiro rodando", T2, 42, "tag"),
    ("DIVIDIR O PREJUÍZO", "Na hora da perda, a cadeira afasta da mesa", T1, 62, "data"),
    ("SEM CONSPIRAÇÃO FÁCIL", "Conhecer algumas relações não entrega o desfecho", EXT, 775, "editorial"),
    ("JASON E LUCIA", "A premissa do casal diante da pressão externa", LAUNCH, 12, "tag"),
    ("AS TRÊS PERGUNTAS", "O que oferece, o que pede e quem paga o risco", EXT, 1569, "data"),
    ("LEIA O COMBINADO", "Pixel Procurado • A pista com a fonte oficial", BRIAN, 0, "editorial"),
]

SLICES_LONG = [
    (0.00, 14.50),
    (14.50, 27.50),
    (27.50, 40.00),
    (40.00, 52.00),
    (52.00, 64.00),
    (64.00, 75.00),
    (75.00, 87.50),
    (87.50, 101.00),
    (101.00, 114.00),
    (114.00, 126.00),
    (126.00, 139.00),
    (139.00, 153.00),
    (153.00, 166.00),
    (166.00, 179.00),
    (179.00, 190.00),
    (190.00, 204.00),
    (204.00, 218.00),
    (218.00, 230.00),
    (230.00, 243.00),
    (243.00, 256.00),
    (256.00, 270.00),
    (270.00, 285.00),
    (285.00, 300.00),
    (300.00, 315.00),
    (315.00, 335.80),
]

DIRECTION_SHORT = [
    ("O ALUGUEL GRÁTIS", "Jason mora sem pagar aluguel com Brian", BRIAN, 0, "tag"),
    ("DESCRIÇÃO OFICIAL", "Apresentação dos personagens de GTA VI", EXT, 406, "editorial"),
    ("FAVOR OU PRENDEDOR?", "Um favor desses aproxima ou prende?", T1, 45, "data"),
]

SLICES_SHORT = [
    (0.00, 15.00),
    (15.00, 30.00),
    (30.00, 46.30),
]

def run(args, capture=False):
    return subprocess.run([str(FF), "-hide_banner", "-nostdin", "-loglevel", "error", "-y",
                           *map(str, args)], check=True, capture_output=capture)

def panel_art(kind):
    if kind == "data":
        return '<rect x="17" y="23" width="120" height="86" rx="8"/><path d="M17 44h120M48 128h58m-29-19v19M34 76h80m-80 11h47"/>'
    if kind == "tag":
        return '<path d="M15 93V74l16-16 15-28h61l16 28 16 16v19H15zm16-35h92M23 95v18h20V95m69 0v18h20V95M29 77h16m66 0h16"/>'
    return '<circle cx="77" cy="76" r="49"/><circle cx="77" cy="76" r="30"/><path d="M77 8v25m0 86v25M8 76h25m87 0h26"/>'

def prepare_hyperframes(direction, out_html):
    out_html.parent.mkdir(parents=True, exist_ok=True)
    slides = []
    for i, (title, detail, _, _, kind) in enumerate(direction):
        words = "".join(f'<span>{html.escape(word)} </span>' for word in title.split())
        compact = " compact" if len(title) > 21 else ""
        slides.append(f'''<section class="clip {kind}{compact}" id="p{i}" data-start="{i*SLOT:.2f}" data-duration="{SLOT}" data-track-index="1">
        <div class="card"><div class="accent"></div><div class="content">
        <div class="kicker">PIXEL PROCURADO <b> / </b> GTA VI</div>
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
    ref_gsap = ROOT / "producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06/montagem/hyperframes_v2/gsap.min.js"
    if ref_gsap.is_file() and not (out_html.parent / "gsap.min.js").is_file():
        (out_html.parent / "gsap.min.js").write_bytes(ref_gsap.read_bytes())

def card_duration(index, frames, direction):
    title, detail, _, _, kind = direction[index]
    tag = kind == "tag"
    words = len((title if tag else title + " " + detail).split())
    reading = min(5.4, max(2.5, 0.85 + words / 3.4))
    return min(frames / FPS - 0.1, reading)

def fix_word(word):
    fixes = {"leonardo": "Leonida", "leonida": "Leonida", "gratis": "grátis", "pragar": "pagar",
             "dracone": "Dre'Quan", "drequan": "Dre'Quan", "bobbiq": "Boobie Ike", "bobbi": "Boobie"}
    return re.sub(r"[\wÀ-ÿ]+", lambda m: fixes.get(m[0].casefold(), m[0]), word)

def stamp(seconds, scale, sep):
    units = round(max(0, seconds) * scale)
    return f"{units//(3600*scale):02}:{units//(60*scale)%60:02}:{units//scale%60:02}{sep}{units%scale:0{len(str(scale))-1}}"

def write_subs(stem, entries, vertical, out_dir):
    w, h = (1080, 1920) if vertical else (1920, 1080)
    font = 64 if vertical else 54
    margin = 350 if vertical else 80
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pixel,Arial,{font},&H00FFFFFF,&H000000FF,&H00131317,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,110,110,{margin},1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_path = BUILD / f"{stem}.ass"
    srt_path = out_dir / f"{stem}.srt"
    with ass_path.open("w", encoding="utf-8-sig") as stream:
        stream.write(header)
        for a, b, t in entries:
            safe = t.replace("{","(").replace("}",")").replace("\\","/")
            stream.write(f"Dialogue: 0,{stamp(a,100,'.')},{stamp(b,100,'.')},Pixel,,0,0,0,,{safe}\n")
    with srt_path.open("w", encoding="utf-8") as stream:
        for i, (a, b, t) in enumerate(entries, 1):
            stream.write(f"{i}\n{stamp(a,1000,',')} --> {stamp(b,1000,',')}\n{t}\n\n")
    return ass_path

def build_captions(words, total_duration):
    entries = []
    batch = []
    for w in words:
        batch.append(w)
        if len(batch) >= 6 or (len(batch) >= 3 and w["word"].endswith((".", "?", "!"))):
            entries.append((batch[0]["start"], batch[-1]["end"], " ".join(fix_word(x["word"]) for x in batch)))
            batch = []
    if batch:
        entries.append((batch[0]["start"], min(total_duration, batch[-1]["end"]), " ".join(fix_word(x["word"]) for x in batch)))
    res = []
    for i, (a, b, text) in enumerate(entries):
        next_a = entries[i+1][0] if i+1 < len(entries) else total_duration
        end_time = min(max(b, a + 0.65), next_a)
        if end_time > a:
            res.append((a, end_time, text))
    return res

def cut_shot(job):
    index, count, stem, vertical, offset, ass_name, direction, panels_mov = job
    out = BUILD / stem / f"{index:02d}.mp4"
    if out.exists() and out.stat().st_size > 1024:
        return out
    
    title, detail, source, start_sec, kind = direction[index]
    inputs = []
    filters = []
    
    source_path = ROOT / "videosGTAVI" / source
    is_image = source_path.suffix.lower() in (".jpg", ".jpeg", ".png")
    
    if is_image:
        inputs += ["-loop", "1", "-t", f"{count/FPS+0.05:.6f}", "-threads", "2", "-i", str(source_path)]
        filters.append(f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=60,trim=end_frame={count},setpts=PTS-STARTPTS[base]")
    else:
        inputs += ["-ss", str(start_sec), "-t", f"{count/FPS+0.05:.6f}", "-threads", "2", "-i", str(source_path)]
        filters.append(f"[0:v]scale=1920:1080:flags=fast_bilinear,setsar=1,fps=60,trim=end_frame={count},setpts=PTS-STARTPTS[base]")
    
    visible = card_duration(index, count, direction)
    hold = max(0, round((visible - ANIM) * FPS))
    panel_width = 780 if vertical else 720
    
    inputs += ["-ss", f"{index*SLOT:.2f}", "-t", str(ANIM), "-i", str(panels_mov)]
    filters += [
        f"[1:v]fps=60,format=rgba,scale={panel_width}:-2,"
        f"setpts='PTS-STARTPTS+gte(N,24)*{hold}/60/TB',fps=60[panel]"
    ]
    
    if vertical:
        filters += [
            "[base]split[raw][blur]",
            "[blur]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=10:1,scale=1080:1920,eq=brightness=-0.29[bg]",
            "[raw]scale=1080:608[fg]",
            "[bg][fg]overlay=0:425[canvas]",
            f"[canvas][panel]overlay=150:1060:eof_action=pass:enable='lt(t,{visible:.6f})'[vcard]"
        ]
    else:
        filters.append(f"[base][panel]overlay=58:730:eof_action=pass:enable='lt(t,{visible:.6f})'[vcard]")
        
    filters.append(f"[vcard]setpts=PTS+{offset/FPS:.8f}/TB,ass=filename={ass_name},setpts=PTS-STARTPTS[v]")
    
    temp = out.with_suffix(".part.mp4")
    run([*inputs, "-filter_complex_threads", "3", "-filter_complex", ";".join(filters), "-map", "[v]",
         "-frames:v", str(count), "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "17",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-video_track_timescale", "60000", str(temp)])
    temp.replace(out)
    print(f"Plano {index+1:02d} concluído ({count} frames)", flush=True)
    return out

def render_movie(mode):
    vertical = mode == "short"
    direction = DIRECTION_SHORT if vertical else DIRECTION_LONG
    slices = SLICES_SHORT if vertical else SLICES_LONG
    voice_file = VOICE_SHORT if vertical else VOICE_LONG
    words_file = ROOT / ("producao/shorts/L08/voz/alinhamento_palavras.json" if vertical else "producao/L08/voz/alinhamento_palavras.json")
    
    stem = "Pixel_Procurado_L08_Short_V2" if vertical else "Pixel_Procurado_L08_Longo_V2"
    out_dir = OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    (BUILD / stem).mkdir(parents=True, exist_ok=True)
    
    # 1. Hyperframes
    hf_html = BUILD / ("hyperframes_short" if vertical else "hyperframes_long") / "index.html"
    panels_mov = BUILD / ("paineis_short.mov" if vertical else "paineis_long.mov")
    prepare_hyperframes(direction, hf_html)
    
    if not panels_mov.is_file() or panels_mov.stat().st_size < 1000:
        print(f"Renderizando painéis Hyperframes para {stem}...", flush=True)
        res = subprocess.run(["hyperframes.cmd", "render", str(hf_html.parent), "--format", "mov", "-f", "60", "-o", str(panels_mov)],
                             cwd=str(BUILD), capture_output=True, text=True)
        if res.returncode != 0:
            print("Hyperframes stderr:", res.stderr)
            raise RuntimeError(f"Falha no render Hyperframes: {res.stderr}")
            
    # 2. Legendas
    with open(words_file, encoding="utf-8") as f:
        words = json.load(f)
    captions = build_captions(words, slices[-1][1])
    write_subs(stem, captions, vertical, out_dir)
    
    # 3. Cortes
    jobs = []
    offset = 0
    for idx, (s_start, s_end) in enumerate(slices):
        count = round((s_end - s_start) * FPS)
        jobs.append((idx, count, stem, vertical, offset, f"{stem}.ass", direction, panels_mov))
        offset += count
        
    print(f"Iniciando renderização de {len(jobs)} planos ({offset} frames)...", flush=True)
    with ThreadPoolExecutor(max_workers=2) as executor:
        clips = list(executor.map(cut_shot, jobs))
        
    # 4. Concat
    concat_file = BUILD / f"{stem}.ffconcat"
    with concat_file.open("w", encoding="utf-8") as f:
        f.write("ffconcat version 1.0\n")
        for clip, job in zip(clips, jobs):
            f.write(f"file '{clip.relative_to(BUILD).as_posix()}'\nduration {job[1]/FPS:.9f}\n")
            
    final_mp4 = out_dir / f"{stem}.mp4"
    temp_mp4 = out_dir / f"{stem}.part.mp4"
    
    run(["-f", "concat", "-safe", "0", "-i", str(concat_file), "-i", str(voice_file),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(temp_mp4)])
    temp_mp4.replace(final_mp4)
    print(f"Render concluído: {final_mp4}", flush=True)
    return final_mp4

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("long", "short", "all"))
    args = parser.parse_args()
    
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    
    os.chdir(BUILD)
    if args.mode in ("short", "all"):
        render_movie("short")
    if args.mode in ("long", "all"):
        render_movie("long")
