"""Monta o video longo "melhores momentos" a partir dos clipes aprovados do acervo de lives.

  py -3.12 automacao/live_longo.py --id LONGO_01 [--min-clipes 5] [--max-min 12] [--imagem auto|prompt|nenhum]

Saida: videosGTAVI/_live/_longos/<id>/ com compilacao.mp4 (1920x1080 60 fps, cartela de 2 s por clipe com titulo e
credito), capitulos.txt, descricao.md, thumbnail (mesmos modos de live_thumb.py) e episodio.json (plano do Postiz).
So gera plano; publicar exige `--publicar` E o arquivo APROVADO na pasta. Usa a versao narrada do clipe quando existe.
Clipes duplicados, retidos, com risco ou sem GTA VI visivel ficam de fora.
"""
import argparse, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import captura_live as cl
import live_publicar as lp
import live_thumb
from live_aviso import avisar

ROOT, ACERVO = cl.ROOT, cl.ACERVO
FONTE = "C\\:/Windows/Fonts/arialbd.ttf"
NORM = ("scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x14161c,"
        "fps=60,format=yuv420p,setsar=1")
ENC = ["-c:v", "libx264", "-crf", "17", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]


def selecionar(min_nota, max_s):
    todos = []
    for mp in cl.metas_acervo():
        m = cl.ljs(mp)
        if not m.get("id"):
            continue
        arq = mp.parent / ("clip_narrado.mp4" if m.get("narrado") and (mp.parent / "clip_narrado.mp4").exists() else "clip.mp4")
        if m.get("status") in ("empacotado", "aguardando_aprovacao", "publicado") and arq.exists() \
                and not lp.passa_filtro(m, min_nota):
            todos.append((m, arq))
    todos.sort(key=lambda x: -x[0]["nota"])
    if not todos:
        return []
    escolhidos, total = [], 0.0
    for m, arq in todos:
        if total + m["duracao_s"] - FADE > max_s:
            continue
        escolhidos.append((m, arq))
        total += m["duracao_s"] - FADE
    abertura, resto = escolhidos[0], sorted(escolhidos[1:], key=lambda x: x[0].get("gravado_em", ""))
    return [abertura] + resto


def cartela(tmp, i, titulo, canal):
    import textwrap
    (tmp / f"t{i}.txt").write_text("\n".join(textwrap.wrap(titulo, 30)[:2]), encoding="utf-8")
    (tmp / f"c{i}.txt").write_text(f"Live: {canal}", encoding="utf-8")
    vf = (f"drawtext=fontfile='{FONTE}':textfile=t{i}.txt:fontcolor=white:fontsize=72:line_spacing=12:"
          f"x=(w-text_w)/2:y=(h/2)-150,"
          f"drawtext=fontfile='{FONTE}':textfile=c{i}.txt:fontcolor=0xFFD400:fontsize=44:x=(w-text_w)/2:y=(h/2)+90")
    out = f"card{i}.mp4"
    subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x14161c:s=1920x1080:r=60:d=2",
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "2", "-vf", vf + ",format=yuv420p"] + ENC + [out],
                   cwd=tmp, check=True)
    return out


FADE = 0.5     # crossfade de video e audio entre momentos
FIM_S = 4.0    # fechamento curto (<= 5 s)


def _txt(tmp, nome, texto):
    import textwrap
    (tmp / nome).write_text(chr(10).join(textwrap.wrap(texto, 34)[:2]), encoding="utf-8")


def segmento(tmp, i, n, titulo, arq):
    """Um momento: 1080p60, zoom lento (push-in), titulo animado, contador 'MOMENTO X/N', audio a -14 LUFS."""
    _txt(tmp, f"t{i}.txt", titulo)
    (tmp / f"n{i}.txt").write_text(f"MOMENTO {i + 1}/{n}", encoding="utf-8")
    al = "if(lt(t,0.3),t/0.3,if(lt(t,3.6),1,max(0,(4.1-t)/0.5)))"
    vf = (f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x14161c,"
          f"scale=w='1920*(1+0.07*min(t/6,1))':h=-2:eval=frame,crop=1920:1080,fps=60,setsar=1,"
          f"drawtext=fontfile='{FONTE}':textfile=t{i}.txt:fontcolor=white:fontsize=64:line_spacing=10:box=1:"
          f"boxcolor=black@0.6:boxborderw=24:x=70:y=h-250:alpha='{al}',"
          f"drawtext=fontfile='{FONTE}':textfile=n{i}.txt:fontcolor=0x14161c:fontsize=38:box=1:boxcolor=0xFFD400:"
          f"boxborderw=14:x=w-text_w-60:y=50,format=yuv420p")
    out = f"seg{i}.mp4"
    subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-i", str(arq), "-vf", vf,
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000"] + ENC + [out], cwd=tmp, check=True)
    return out


def montar(sel, tmp, pasta):
    n = len(sel)
    segs, durs, caps = [], [], []
    for i, (m, arq) in enumerate(sel):  # trava por etapa (expira em 30 min; nao segurar o encode inteiro)
        titulo = lp.limpar(m.get("titulo"), 60) or "Momento da live"
        with cl.trava_pesada():
            segs.append(segmento(tmp, i, n, titulo, arq))
        durs.append(cl.ffprobe_dur(tmp / segs[-1]))
        caps.append((0.0, titulo, m.get("canal"), m["id"]))
    # fechamento curto
    with cl.trava_pesada():
        _txt(tmp, "fim.txt", "Inscreva-se no Pixel Procurado")
        subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=0x2a2f3a:s=1920x1080:r=60:d={FIM_S}",
                        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(FIM_S), "-vf",
                        f"drawtext=fontfile='{FONTE}':textfile=fim.txt:fontcolor=0xFFD400:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2,format=yuv420p"]
                       + ENC + ["fim.mp4"], cwd=tmp, check=True)
    segs.append("fim.mp4")
    durs.append(FIM_S)
    # crossfade encadeado (video xfade + audio acrossfade)
    ent = []
    for s_ in segs:
        ent += ["-i", s_]
    fc, vl, al_, acc = [], "[0:v]", "[0:a]", durs[0]
    inicio = [0.0]
    for k in range(1, len(segs)):
        off = acc - FADE
        fc.append(f"{vl}[{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{k}]")
        fc.append(f"{al_}[{k}:a]acrossfade=d={FADE}[a{k}]")
        vl, al_ = f"[v{k}]", f"[a{k}]"
        inicio.append(off)
        acc = off + durs[k]
    with cl.trava_pesada():
        subprocess.run([cl.ffbin(), "-y", "-loglevel", "error"] + ent + ["-filter_complex", ";".join(fc), "-map", vl, "-map", al_]
                       + ENC + ["-movflags", "+faststart", "bruto.mp4"], cwd=tmp, check=True)
    with cl.trava_pesada():  # mistura final a -14 LUFS (video copiado)
        subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-i", "bruto.mp4", "-c:v", "copy", "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", "../compilacao.mp4"], cwd=tmp, check=True)
    qa(pasta / "compilacao.mp4", pasta)
    caps = [(inicio[k], c[1], c[2], c[3]) for k, c in enumerate(caps)]
    return caps, acc


def qa(arq, pasta):
    """silencedetect, blackdetect e ebur128: grava qa.json e avisa se algo estiver fora."""
    import re
    r = subprocess.run([cl.ffbin(), "-hide_banner", "-nostats", "-i", str(arq), "-vf", "blackdetect=d=0.5:pix_th=0.10",
                        "-af", "silencedetect=n=-50dB:d=2,ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    log = r.stderr
    pretos = re.findall(r"black_start:([\d.]+).*?black_duration:([\d.]+)", log)
    sil = re.findall(r"silence_start: ([\d.]+)", log)
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    res = {"pretos": pretos, "silencios_inicio": sil, "lufs_integrado": float(lufs[-1]) if lufs else None}
    res["ok"] = not pretos and not sil and res["lufs_integrado"] is not None and abs(res["lufs_integrado"] + 14) <= 1.5
    cl.sj(pasta / "qa.json", res)
    if not res["ok"]:
        avisar("QA do longo falhou", f"{pasta.name}: pretos={len(pretos)} silencios={len(sil)} LUFS={res['lufs_integrado']} (veja qa.json)", "acao")


def gerar_instagram(pasta):
    """Versao leve do longo para o Instagram (limite 300 MB): 1080p 30 fps, bitrate calculado pela duracao."""
    src, out = pasta / "compilacao.mp4", pasta / "compilacao_instagram.mp4"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                               capture_output=True, text=True).stdout)
    vbr = int((270e6 * 8 / dur) - 128_000)  # alvo ~270 MB com audio de 128 kbps
    subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-i", str(src), "-vf", "fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-b:v", str(vbr), "-maxrate", str(int(vbr * 1.3)),
                    "-bufsize", str(vbr * 2), "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)], check=True)
    return out


def so_instagram(a):
    """Complementa um longo ja montado com a peca do Instagram (autorizado pelo usuario) e publica so ela."""
    pasta = ACERVO / "_longos" / a.id
    ep = json.loads((pasta / "episodio.json").read_text(encoding="utf-8"))
    out = gerar_instagram(pasta)
    pub = ep["publicacao"]
    desc = pub["textos"]["longo"]
    pub["textos"]["instagram_longo"] = desc[:2100] + ("..." if len(desc) > 2100 else "")
    pub["pecas"] = [p for p in pub["pecas"] if p["chave"] != "instagram_long"]
    capa = next((p["capa"] for p in pub["pecas"] if p.get("capa")), None)
    pub["pecas"].append({"chave": "instagram_long", "rede": "instagram", "tipo": "post",
                         "midia": out.relative_to(ROOT).as_posix(), "texto": "instagram_longo",
                         **({"capa": capa} if capa else {})})
    (pasta / "episodio.json").write_text(json.dumps(ep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"instagram: {out} ({out.stat().st_size / 1e6:.0f} MB)")
    if a.publicar and (pasta / "APROVADO").exists():
        cod = lp.distribuir(pasta, "--publicar", "--agora")
        avisar("Longo (Instagram) publicado" if cod == 0 else "Erro ao publicar longo no Instagram", a.id,
               "info" if cod == 0 else "erro")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--so-instagram", action="store_true", help="so gera a versao leve e publica a peca do Instagram")
    ap.add_argument("--id", required=True)
    ap.add_argument("--min-clipes", type=int, default=5)
    ap.add_argument("--max-min", type=int, default=12)
    ap.add_argument("--min-nota", type=int, default=70)
    ap.add_argument("--imagem", choices=("auto", "prompt", "nenhum"), default=os.environ.get("LIVE_IMAGEM_MODO", "prompt"))
    ap.add_argument("--publicar", action="store_true")
    ap.add_argument("--aprovar", action="store_true", help="grava APROVADO (so com autorizacao do usuario no chat)")
    a = ap.parse_args()
    if a.aprovar:
        (ACERVO / "_longos" / a.id).mkdir(parents=True, exist_ok=True)
        (ACERVO / "_longos" / a.id / "APROVADO").write_text("autorizado pelo usuario no chat em 2026-11-20\n", encoding="utf-8")
    if a.so_instagram:
        return so_instagram(a)
    sel = selecionar(a.min_nota, a.max_min * 60 - FIM_S)
    if len(sel) < a.min_clipes:
        sys.exit(f"so {len(sel)} clipes elegiveis (minimo {a.min_clipes}); aguarde mais lives")
    pasta = ACERVO / "_longos" / a.id
    tmp = pasta / "_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    caps, t = montar(sel, tmp, pasta)
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    hh = lambda s: f"{int(s // 60):02d}:{int(s % 60):02d}"
    (pasta / "capitulos.txt").write_text("\n".join(f"{hh(s)} {tit}" for s, tit, _, _ in caps), encoding="utf-8")
    creditos = "\n".join(f"- {tit}: live de {c}" for _, tit, c, _ in caps)
    titulo = f"As melhores jogadas das lives de GTA VI ({len(sel)} momentos)"
    desc = (f"{titulo}\n\n{(pasta / 'capitulos.txt').read_text(encoding='utf-8')}\n\nCréditos (trechos de lives de terceiros, "
            f"com comentário/edição do Pixel Procurado):\n{creditos}\n\n#GTA6 #GTAVI #PixelProcurado")
    (pasta / "descricao.md").write_text(desc, encoding="utf-8")
    meta = {"id": a.id, "titulo": "Melhores Momentos", "motivo": "compilacao dos melhores momentos de lives de GTA VI",
            "clipes": [c[3] for c in caps], "duracao_s": round(t, 1), "status": "montado"}
    try:
        res = live_thumb.preparar(pasta, meta, a.imagem, "long")
        if res == "prompt":
            avisar("Imagem pendente (longo)", f"prompt em {pasta / 'thumb_prompt.md'}", "acao")
    except Exception as e:
        meta["thumb_falhou"] = repr(e)[:200]
    rel = lambda p: p.relative_to(ROOT).as_posix()
    ep = {"id": a.id, "publicacao": {
        "canais": lp.CANAIS, "data_padrao": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "estado": rel(pasta / "POSTIZ_ESTADO.json"), "pasta_envio": rel(pasta / "envio"),
        "tags_youtube": ["GTA 6", "GTA VI", "Pixel Procurado"], "youtube_visibilidade": "public",
        "textos": {"longo": desc},
        "pecas": [{"chave": "youtube_long", "rede": "youtube", "tipo": "post", "midia": rel(pasta / "compilacao.mp4"),
                   "texto": "longo", "titulo": titulo, **({"capa": meta["capa"]} if meta.get("capa") else {})},
                  {"chave": "facebook_video", "rede": "facebook", "tipo": "post", "midia": rel(pasta / "compilacao.mp4"),
                   "texto": "longo", "titulo": titulo}]}}
    (pasta / "episodio.json").write_text(json.dumps(ep, indent=2, ensure_ascii=False), encoding="utf-8")
    cl.sj(pasta / "meta.json", meta)
    lp.distribuir(pasta)
    print(f"compilacao: {pasta / 'compilacao.mp4'} ({hh(t)}, {len(sel)} clipes)\nplano: {pasta / 'publicacao.log'}")
    if a.publicar:
        if not (pasta / "APROVADO").exists():
            print(f"retido: crie {pasta / 'APROVADO'} apos revisar a compilacao")
        else:
            cod = lp.distribuir(pasta, "--publicar", "--agora")
            avisar("Longo publicado" if cod == 0 else "Erro ao publicar longo", a.id, "info" if cod == 0 else "erro")
            try:
                so_instagram(a)  # versao leve (<300 MB) no Instagram
            except Exception as e:
                avisar("Erro no longo do Instagram", repr(e)[:150], "erro")


if __name__ == "__main__":
    main()
