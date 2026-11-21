"""Reedita um video longo de melhores momentos (LONGO_xx) em compilacao_v2.mp4, sem cartela preta.

  py -3.12 automacao/live_longo_v2.py --id LONGO_01 [--trim 0.5] [--xf 0.4]

Por clipe: corta o preparo inicial (ate o limite da folga de 0,8 s antes da voz), normaliza (loudnorm -14), aplica titulo
animado (720 px, 0,2-3,0 s, canto superior esquerdo, longe do facecam) e marcador "MOMENTO n/N | LIVE: canal" discreto.
Entre clipes: xfade de video + acrossfade de audio, tipos alternados (nunca repete em sequencia). Ultimo clipe leva
chamada para inscricao nos ultimos 4,5 s. Loudness final por loudnorm em duas passadas (-14 LUFS, TP -1.5).
Nao publica nada. Saida: compilacao_v2.mp4, capitulos_v2.txt, RESUMO_V2.md ao lado do original.
"""
import argparse, json, re, subprocess, sys, textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import captura_live as cl

FONTE = "C\\:/Windows/Fonts/arialbd.ttf"
ENC = ["-c:v", "libx264", "-crf", "17", "-preset", "medium", "-r", "60", "-pix_fmt", "yuv420p"]
TIPOS = ["fade", "slideleft", "circleopen", "fade", "slideright", "wipeleft", "slideleft"]


def run(args, **kw):
    subprocess.run([cl.ffbin(), "-y", "-hide_banner", "-loglevel", "error"] + args, check=True, **kw)


def painel_x(t0, t1):
    """x do painel: entra em 0,35 s (desacelera), segura, sai em 0,35 s."""
    a, b, c = t0 + 0.35, t1 - 0.35, t1
    return (f"if(lt(t,{t0}),-760,if(lt(t,{a}),-760+800*(1-pow(1-(t-{t0})/0.35,3)),"
            f"if(lt(t,{b}),40,40-800*pow((t-{b})/0.35,2))))")


def bloco(tmp, nome, linhas, t0, t1, alt, cor_linha2):
    """Filtros de um painel de 720 px com ate 2 linhas de titulo + 1 de credito. Retorna (input_lavfi, partes de filtro)."""
    x = painel_x(t0, t1)
    return x


def montar_clipe(tmp, i, n, arq, m, trim, titulo, canal, fim_cta):
    # o audio de alguns clipes termina antes do video (clip.mp4 original ja removido): cortar onde o audio acaba
    adur = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration",
                                 "-of", "csv=p=0", str(arq)], capture_output=True, text=True, check=True).stdout.strip())
    dur = min(cl.ffprobe_dur(arq), adur)
    d_out = dur - trim
    linhas = textwrap.wrap(titulo, 28)[:2]
    (tmp / f"t{i}.txt").write_text("\n".join(linhas), encoding="utf-8", newline="\n")
    (tmp / f"c{i}.txt").write_text(f"LIVE: {canal.upper()}", encoding="utf-8", newline="\n")
    (tmp / f"m{i}.txt").write_text(f"MOMENTO {i + 1}/{n}  |  LIVE: {canal.upper()}", encoding="utf-8", newline="\n")
    alt = 70 + 56 * len(linhas) + 50
    x = painel_x(0.2, 3.0)
    f = [f"[0:v]trim=start={trim}:end={dur},setpts=PTS-STARTPTS,scale=1920:1080,fps=60,format=yuv420p[v0]",
         f"color=c=0x14161c@0.88:s=720x{alt}:r=60,format=rgba[bx]",
         f"[v0][bx]overlay=shortest=1:x='{x}':y=40:enable='between(t,0.2,3.0)'[v1]",
         f"[v1]drawtext=fontfile='{FONTE}':textfile=t{i}.txt:fontcolor=white:fontsize=46:line_spacing=10:"
         f"x='{x}+28':y=40+22:enable='between(t,0.2,3.0)',"
         f"drawtext=fontfile='{FONTE}':textfile=c{i}.txt:fontcolor=0xFFD33D:fontsize=30:"
         f"x='{x}+28':y=40+{alt}-48:enable='between(t,0.2,3.0)',"
         f"drawtext=fontfile='{FONTE}':textfile=m{i}.txt:fontcolor=white:fontsize=26:box=1:boxcolor=0x14161c@0.75:"
         f"boxborderw=10:x=40:y=40:alpha='if(lt(t,3.1),0,min(1,(t-3.1)/0.3))'[v2]"]
    saida = "v2"
    if fim_cta:
        (tmp / "cta.txt").write_text("GOSTOU? INSCREVA-SE NO\nPIXEL PROCURADO", encoding="utf-8", newline="\n")
        t0 = d_out - 4.8
        t1 = d_out - 0.1
        xc = painel_x(t0, t1)
        f += [f"color=c=0xFFD33D@0.95:s=720x190:r=60,format=rgba[bc]",
              f"[v2][bc]overlay=shortest=1:x='{xc}':y=40:enable='between(t,{t0},{t1})'[v3]",
              f"[v3]drawtext=fontfile='{FONTE}':textfile=cta.txt:fontcolor=0x14161c:fontsize=44:line_spacing=12:"
              f"x='{xc}+28':y=40+40:enable='between(t,{t0},{t1})'[v4]"]
        saida = "v4"
    f.append(f"[0:a]atrim=start={trim}:end={dur},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,"
             f"aformat=sample_fmts=fltp:channel_layouts=stereo,afade=t=out:st={d_out-0.1:.3f}:d=0.1[a0]")
    (tmp / f"g{i}.txt").write_text(";\n".join(f), encoding="utf-8")
    out = f"c{i}.mp4"
    with cl.trava_pesada():
        run(["-i", str(arq), "-/filter_complex", f"g{i}.txt", "-map", f"[{saida}]", "-map", "[a0]"] + ENC +
            ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", out], cwd=tmp)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True)
    ap.add_argument("--trim", type=float, default=0.5)
    ap.add_argument("--xf", type=float, default=0.4)
    a = ap.parse_args()
    pasta = cl.ACERVO / "_longos" / a.id
    meta = cl.lj(pasta / "meta.json", {})
    tmp = pasta / "_v2"
    tmp.mkdir(exist_ok=True)
    clipes = []
    for cid in meta["clipes"]:
        mp = next(m for m in cl.metas_acervo() if m.parent.name == cid)
        m = cl.ljs(mp)
        arq = mp.parent / ("clip_narrado.mp4" if (mp.parent / "clip_narrado.mp4").exists() else "clip.mp4")
        clipes.append((m, arq))
    n = len(clipes)
    caps = re.findall(r"^\d\d:\d\d (.+)$", (pasta / "capitulos.txt").read_text(encoding="utf-8"), re.M)
    partes = []
    for i, (m, arq) in enumerate(clipes):
        partes.append(montar_clipe(tmp, i, n, arq, m, a.trim, caps[i] if i < len(caps) else m.get("titulo", ""),
                                   m.get("canal", "canal"), i == n - 1))
    durs = [cl.ffprobe_dur(tmp / p) for p in partes]
    xf = a.xf
    starts, L = [0.0], durs[0]
    af, acc_a = [], "[0:a]"
    for k in range(1, n):
        starts.append(L - xf)
        af.append(f"{acc_a}[{k}:a]acrossfade=d={xf}:c1=tri:c2=tri[xa{k}]")
        acc_a = f"[xa{k}]"
        L = L - xf + durs[k]
    ins = sum([["-i", p] for p in partes], [])
    (tmp / "xa.txt").write_text(";\n".join(af), encoding="utf-8")
    with cl.trava_pesada():
        run(ins + ["-/filter_complex", "xa.txt", "-map", acc_a, "-c:a", "pcm_s16le", "-ar", "48000", "audio_x.wav"], cwd=tmp)
    # video por segmentos (transicoes de 0,4 s + corpos), concatenados por copia: evita estouro de memoria de 8 xfade
    seg = []
    for i in range(n):
        ini = xf if i > 0 else 0.0
        fim = durs[i] - xf if i < n - 1 else durs[i]
        nome = f"s{i:02d}b.mp4"
        with cl.trava_pesada():
            run(["-i", partes[i], "-vf", f"trim=start={ini}:end={fim},setpts=PTS-STARTPTS,fps=60", "-an"] + ENC + [nome], cwd=tmp)
        seg.append(nome)
        if i < n - 1:
            tipo = TIPOS[i % len(TIPOS)]
            nome = f"s{i:02d}t.mp4"
            g = (f"[0:v]trim=start={durs[i] - xf},setpts=PTS-STARTPTS,fps=60[a];[1:v]trim=end={xf},setpts=PTS-STARTPTS,fps=60[b];"
                 f"[a][b]xfade=transition={tipo}:duration={xf}:offset=0[v]")
            with cl.trava_pesada():
                run(["-i", partes[i], "-i", partes[i + 1], "-filter_complex", g, "-map", "[v]", "-an"] + ENC + [nome], cwd=tmp)
            seg.append(nome)
    (tmp / "lista.txt").write_text("".join(f"file '{s}'\n" for s in seg), encoding="utf-8")
    with cl.trava_pesada():
        run(["-f", "concat", "-safe", "0", "-i", "lista.txt", "-i", "audio_x.wav", "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "pre.mp4"], cwd=tmp)
    pre = tmp / "pre.mp4"
    # loudnorm em duas passadas sobre o audio da montagem
    p1 = subprocess.run([cl.ffbin(), "-hide_banner", "-i", str(pre), "-af",
                         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-vn", "-f", "null", "-"],
                        capture_output=True, text=True, check=True).stderr
    j = json.loads(p1[p1.rfind("{"):p1.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    out = pasta / "compilacao_v2.mp4"
    with cl.trava_pesada():
        run(["-i", str(pre), "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", ln + ",aresample=48000",
             "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(out)])
    hh = lambda s: f"{int(s // 60):02d}:{int(s % 60):02d}"
    (pasta / "capitulos_v2.txt").write_text(
        "\n".join(f"{hh(s)} {caps[i]}" for i, s in enumerate(starts)), encoding="utf-8")
    json.dump({"starts": starts, "durs": durs, "total": L, "tipos": TIPOS[:n - 1]}, open(tmp / "v2.json", "w"))
    print(f"ok {out} total={L:.1f}s ({hh(L)})")


if __name__ == "__main__":
    main()
