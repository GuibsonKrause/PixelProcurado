"""Empacota os clipes de live do acervo (vertical + horizontal + story + capa), narra os melhores, aplica o filtro de
risco e publica via distribuir_postiz.py (Postiz + R2). Chamado por `captura_live.py auto --empacotar|--publicar`.

  py -3.12 automacao/live_publicar.py --saida producao/live/<nome> [--publicar] [--narrar] [--imagem auto|prompt|nenhum]

Sem --publicar so empacota e gera o plano (dry-run do Postiz). Com --publicar, publica apenas clipes que passam no
filtro (nota >= 70, risco nenhum, gameplay/reacao, GTA VI visivel nos quadros, nao duplicado) e so depois que existir
<acervo>/<AAAA-MM-DD>/<canal>/APROVADO (a primeira publicacao de cada live fica retida para o usuario aprovar).
"""
import argparse, json, re, subprocess, sys, textwrap, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import captura_live as cl
import live_narrar, live_thumb
from live_aviso import avisar

ROOT, ACERVO = cl.ROOT, cl.ACERVO
CANAIS = {"youtube": "cmvsctfgl0001jncj932ovibv", "facebook": "cmvzyur290001pddwolrt33em",
          "instagram": "cmvzyw7vj0003pddwkgtivv8i", "tiktok": "cmwa9e6ie0001pna8wkbk1x2e"}


LOUDNORM = "loudnorm=I=-14:TP=-1.5:LRA=11"  # clipe sem narracao: som do jogo/streamer em volume de plataforma


def limpar(txt, maximo):
    txt = re.sub(r"https?://\S+|www\.\S+", "", txt or "")
    txt = re.sub(r"[@#]\S+", "", txt)
    txt = re.sub(r"[\x00-\x1f\x7f]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip(" -–—:,.")
    return txt[:maximo].strip()


def titulo_seo(meta, maximo=95):
    """Titulo otimizado para busca: 'GTA VI' no inicio, gancho no meio, 'GTA 6' no fim (limite do YouTube = 100)."""
    base = limpar(meta.get("titulo"), 80) or "Momento da live"
    if not re.search(r"gta\s*(vi|6)", base, re.I):
        base = f"GTA VI: {base}"
    for sufixo in (" | GTA 6 Gameplay", " | GTA 6"):
        if not re.search(r"gta\s*6", base, re.I) and len(base) + len(sufixo) <= maximo:
            return base + sufixo
    return base[:maximo].strip()


def srt_tempo(s):
    return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(s % 1 * 1000):03d}"


def empacotar(pasta, meta):
    clip = pasta / "clip.mp4"
    raw = pasta / "_a.f32"
    subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-i", str(clip), "-vn", "-ac", "1", "-ar", "16000",
                    "-f", "f32le", str(raw)], check=True)
    segs = cl.transcrever(raw)
    raw.unlink(missing_ok=True)
    meta["legenda_segmentos"] = segs
    blocos = []
    for i, s in enumerate(segs, 1):
        linhas = textwrap.wrap(s["text"], 28)[:3]
        blocos.append(f"{i}\n{srt_tempo(s['s'])} --> {srt_tempo(s['e'])}\n" + "\n".join(linhas) + "\n")
    (pasta / "legenda.srt").write_text("\n".join(blocos), encoding="utf-8")
    (pasta / "credito.txt").write_text(f"Live: {meta.get('canal')}", encoding="utf-8")
    # fundo desfocado calculado em baixa resolucao (muito mais rapido) e ampliado
    filtro = ("[0:v]split=2[a][b];[a]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,"
              "boxblur=8:2,scale=1080:1920[bg];[b]scale=1080:-2,format=yuv420p[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    if segs:
        filtro += (",subtitles=legenda.srt:force_style='FontName=Arial,FontSize=7,Bold=1,Outline=3,Shadow=0,"
                   "Alignment=2,MarginV=55'")
    filtro += (",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':textfile=credito.txt:fontcolor=0xFFD400:"
               "fontsize=40:box=1:boxcolor=0x000000@0.55:boxborderw=14:x=40:y=70,format=yuv420p")
    # split-screen (webcam em cima, gameplay embaixo, legenda na divisoria) aprovado em 2026-11-20; sem webcam => layout antigo
    try:
        import split_vertical
        dividido = split_vertical.split_para_clipe(pasta, meta.get("canal"))
    except Exception as e:
        print("split-screen falhou, usando layout antigo:", repr(e)[:200], flush=True)
        dividido = False
    meta["layout_vertical"] = "split" if dividido else "blur"
    if not dividido:
        subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-i", "clip.mp4", "-filter_complex", filtro,
                        "-af", LOUDNORM, "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", "vertical.mp4"], cwd=pasta, check=True)
    # horizontal sem narracao: video copiado, so o audio e normalizado (clip.mp4 segue intacto no acervo)
    subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-i", "clip.mp4", "-map", "0:v", "-map", "0:a?", "-c:v", "copy",
                    "-af", LOUDNORM, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "horizontal.mp4"],
                   cwd=pasta, check=True)
    subprocess.run([cl.ffbin(), "-y", "-loglevel", "error", "-ss", str(meta["duracao_s"] * 0.4), "-i", "vertical.mp4",
                    "-frames:v", "1", "story.png"], cwd=pasta, check=True)
    meta["tamanhos_mb"] = {"vertical": round((pasta / "vertical.mp4").stat().st_size / 1e6, 1),
                           "horizontal": round(clip.stat().st_size / 1e6, 1)}
    meta["status"] = "empacotado"


def gerar_episodio(pasta, meta):
    rel = lambda n: (pasta / n).relative_to(ROOT).as_posix()
    narrado = meta.get("narrado") and (pasta / "vertical_narrado.mp4").exists()
    vert = rel("vertical_narrado.mp4" if narrado else "vertical.mp4")
    horiz = rel("clip_narrado.mp4" if narrado else ("horizontal.mp4" if (pasta / "horizontal.mp4").exists() else "clip.mp4"))
    titulo = titulo_seo(meta)
    canal = limpar(meta.get("canal"), 40)
    quem = "Narração, corte e legendas: Pixel Procurado (voz sintética)." if narrado else "Corte e legendas: Pixel Procurado."
    desc = (f"{titulo}\n\nTrecho da live de {canal} ({meta.get('url_live')}). {quem} "
            f"Conteúdo de GTA VI, créditos ao streamer.\n\n#GTA6 #GTAVI #PixelProcurado")
    capa = meta.get("capa") if meta.get("capa") and (ROOT / meta["capa"]).exists() else None
    yt = {"chave": "youtube_short", "rede": "youtube", "tipo": "post", "midia": vert, "texto": "short", "titulo": titulo}
    if capa:
        yt["capa"] = capa
    ep = {"id": meta["id"], "publicacao": {
        "canais": CANAIS, "data_padrao": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "estado": rel("POSTIZ_ESTADO.json"), "pasta_envio": rel("envio"),
        "tags_youtube": ["GTA 6", "GTA VI", "GTA 6 gameplay", "GTA VI gameplay", "GTA 6 live", "Pixel Procurado"]
        + ([canal] if canal else []), "youtube_visibilidade": "public",
        "textos": {"short": desc, "longo": desc, "story": f"{titulo} #GTA6", "tiktok_short": desc},
        "pecas": [
            yt,
            {"chave": "instagram_reel", "rede": "instagram", "tipo": "post", "midia": vert, "texto": "short"},
            {"chave": "instagram_story", "rede": "instagram", "tipo": "story", "midia": rel("story.png"), "texto": "story"},
            {"chave": "facebook_reel", "rede": "facebook", "tipo": "post", "midia": vert, "texto": "short", "titulo": titulo},
            {"chave": "facebook_story", "rede": "facebook", "tipo": "story", "midia": rel("story.png"), "texto": "story"},
            {"chave": "tiktok_short", "rede": "tiktok", "tipo": "video", "midia": vert, "texto": "tiktok_short",
             "titulo": titulo, "tiktok": {"comment": True, "video_made_with_ai": bool(narrado)}},
        ]}}
    (pasta / "episodio.json").write_text(json.dumps(ep, indent=2, ensure_ascii=False), encoding="utf-8")


def passa_filtro(meta, nota_min=70):
    motivos = []
    if meta.get("nota", 0) < nota_min:
        motivos.append("nota baixa")
    # vazamento, spoiler e cinematica nao bloqueiam: jogo ja lancado na Nova Zelandia (decisao do usuario, 2026-11-18)
    if meta.get("risco") not in ("nenhum", "vazamento", "spoiler", "cinematica_isolada"):
        motivos.append(f"risco={meta.get('risco')}")
    if meta.get("tipo") not in ("gameplay", "reacao", "cinematica"):
        motivos.append(f"tipo={meta.get('tipo')}")
    return motivos  # GTA VI nos quadros nao e mais exigido: a live e toda de GTA VI (decisao do usuario)


def distribuir(pasta, *args):
    r = subprocess.run([sys.executable, str(ROOT / "automacao/pipeline/distribuir_postiz.py"), "--episodio",
                        str(pasta), *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    with open(pasta / "publicacao.log", "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.now().isoformat(timespec='seconds')} {' '.join(args)} (cod {r.returncode})\n{r.stdout}{r.stderr}")
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--publicar", action="store_true")
    ap.add_argument("--narrar", action="store_true")
    ap.add_argument("--narrar-min-nota", type=int, default=75)
    ap.add_argument("--max-narracoes", type=int, default=12)
    ap.add_argument("--imagem", choices=("auto", "prompt", "nenhum"), default="prompt")
    ap.add_argument("--max-imagens", type=int, default=12, help="teto de imagens via API por live (modo auto)")
    ap.add_argument("--intervalo-min", type=int, default=10)
    ap.add_argument("--nota-publicar", type=int, default=70)
    a = ap.parse_args()
    nome = Path(a.saida).name
    base = cl.pasta_acervo(nome)
    est_f = ACERVO / "_estado_publicacao.json"
    est = cl.lj(est_f, {})
    metas = [(mp, cl.ljs(mp)) for mp in sorted(base.glob("*/meta.json"))]
    metas = [(mp, m) for mp, m in metas if m.get("id")]  # ignora meta ilegivel (nao a sobrescreve)
    narradas = sum(1 for _, m in metas if m.get("narrado"))
    imagens = sum(1 for _, m in metas if m.get("thumb_modo") == "auto")
    for mp, meta in metas:
        pasta = mp.parent
        if meta.get("status") == "duplicata":
            continue
        try:
            mudou = False
            if meta["status"] == "extraido":
                with cl.trava_pesada():
                    empacotar(pasta, meta)
                mudou = True
                print("empacotado:", meta["id"], flush=True)
            if meta["status"] in ("empacotado", "aguardando_aprovacao", "retido"):
                # 1) narracao propria (faturavel) so para os melhores
                if (a.narrar and not meta.get("narrado") and not meta.get("narracao_falhou")
                        and meta.get("nota", 0) >= a.narrar_min_nota and not passa_filtro(meta, a.nota_publicar)
                        and narradas < a.max_narracoes):
                    try:
                        with cl.trava_pesada():
                            live_narrar.narrar(pasta, meta)
                        narradas += 1
                        mudou = True
                        print("narrado:", meta["id"], flush=True)
                    except Exception as e:
                        meta["narracao_falhou"] = repr(e)[:200]
                        mudou = True
                        avisar("Narracao falhou", f"{meta['id']}: {meta['narracao_falhou']}", "erro")
                # 2) thumbnail (auto = API; prompt = so o prompt)
                modo_img = a.imagem
                if modo_img == "auto" and imagens >= a.max_imagens and not (pasta / live_thumb.BASE).exists():
                    modo_img = "prompt"  # teto de gasto com imagem atingido: cai para so o prompt
                if modo_img != "nenhum" and meta.get("capa") is None and not meta.get("thumb_falhou") and not passa_filtro(meta, a.nota_publicar):
                    try:
                        antes = (pasta / "thumb_prompt.md").exists()
                        existia = (pasta / live_thumb.BASE).exists()
                        res = live_thumb.preparar(pasta, meta, modo_img, "short")
                        if modo_img == "auto" and not existia and res == "composta":
                            meta["thumb_modo"] = "auto"
                            imagens += 1
                        mudou = mudou or res != "prompt" or not antes
                        if res == "prompt" and not antes:
                            n = live_thumb.listar_pendentes(base)
                            avisar("Imagem pendente", f"{n} prompt(s) em {base / 'PENDENTE_IMAGEM.md'}", "acao")
                    except Exception as e:
                        meta["thumb_falhou"] = repr(e)[:200]
                        mudou = True
                        avisar("Thumbnail falhou", f"{meta['id']}: {meta['thumb_falhou']}", "erro")
                if mudou or not (pasta / "episodio.json").exists():
                    gerar_episodio(pasta, meta)
                    distribuir(pasta)  # plano (dry-run)
            # falha de envio (ex.: R2/SSL) volta para a fila ate 4 tentativas; pecas ja enviadas (post_id) nao sao reenviadas
            if meta["status"] == "erro_publicacao" and meta.get("tentativas_pub", 0) < 4 and a.publicar:
                meta["status"] = "empacotado"
            if meta["status"] in ("empacotado", "aguardando_aprovacao", "retido") and a.publicar:
                bloqueios = passa_filtro(meta, a.nota_publicar)
                if bloqueios:
                    if meta["status"] != "retido":
                        avisar("Clipe retido", f"{meta['id']}: {', '.join(bloqueios)}", "acao")
                    meta["status"], meta["retido_por"] = "retido", bloqueios
                elif not (base / "APROVADO").exists():
                    if meta["status"] != "aguardando_aprovacao":
                        avisar("Aprovar publicacao", f"{meta['id']} (nota {meta['nota']}): revise e crie {base / 'APROVADO'}", "acao")
                    meta["status"] = "aguardando_aprovacao"
                elif time.time() - est.get(nome, 0) < a.intervalo_min * 60:
                    print("intervalo minimo entre publicacoes: aguardando", meta["id"])
                else:
                    meta["status"] = "empacotado"
                    cod = distribuir(pasta, "--publicar", "--agora")
                    meta["status"] = "publicado" if cod == 0 else "erro_publicacao"
                    if cod != 0:
                        meta["tentativas_pub"] = meta.get("tentativas_pub", 0) + 1
                    if cod == 0:
                        est[nome] = time.time()
                    avisar("Publicado" if cod == 0 else "Erro ao publicar", meta["id"], "info" if cod == 0 else "erro")
            elif meta["status"] == "publicado":
                distribuir(pasta, "--status", "--limpar")
        except Exception as e:
            meta["erro"] = repr(e)[:300]
            print("erro em", meta.get("id"), meta["erro"])
        cl.sj(mp, meta)
    cl.sj(est_f, est)
    cl.atualizar_indice_acervo()


if __name__ == "__main__":
    main()
