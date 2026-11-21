"""Armazenamento do projeto no Google Drive (rclone) com cache local e cotas por valor/GB.

Midia pesada (video/audio) mora no Drive em gdrive:GamePlay/<mesmo caminho relativo>. No projeto fica um link
simbolico para P:\\<caminho> (montagem rclone com cache limitado, ver montar_drive.ps1): scripts e agentes continuam
abrindo os mesmos caminhos; o arquivo baixa ao abrir e sai do cache local sozinho quando o cache enche.
Textos (roteiros, json, legendas, capas) ficam sempre locais.

Uso (raiz do projeto, py -3.12). Tudo SIMULA por padrao; --executar aplica.
  armazenamento.py status                         uso local, cache e Drive por categoria x cota
  armazenamento.py arquivar <pasta|arquivo>...    envia a midia ao Drive, confere md5 e troca por link
  armazenamento.py trazer <pasta|arquivo>...      traz de volta como arquivo local real (edicao pesada)
  armazenamento.py automatico [--excluir PASTA]   rotina diaria / inicio de producao:
      1) arquiva lives de dias anteriores e episodios sem alteracao ha `inativo_horas` (exceto --excluir)
      2) remove intermediarios de episodios publicados ha `intermediarios_apos_dias`
      3) aplica as cotas (lives / publicados): acima de 100% apaga ate `alvo_pct`, menor valor por GB primeiro

Heuristica das cotas (configuracao em armazenamento.json):
  valor = base x 0,5^(idade / meia_vida)
    lives: base = nota/100; +0,3 publicado; +ate 0,4 por views; +0,2 usado em compilacao; x0,3 descartado/duplicata
    publicados: base = 1
  Protegidos (nunca apagados): clipes extraido/empacotado/aguardando_aprovacao, APROVADO ainda nao publicado,
  clipes de compilacao nao publicada, episodios com qualquer peca nao PUBLISHED e pastas em --excluir.
  Antes de apagar, degrada: lives perdem primeiro os derivados (horizontal/vertical/narrado, regeneraveis a partir
  de clip.mp4); episodios perdem primeiro os intermediarios. Custo de cada passo = valor perdido / GB liberado.
  Apagar no Drive manda para a lixeira (30 dias, conta na cota do Drive). Registro em _armazenamento/registro.jsonl.
"""
import argparse, json, math, os, shutil, subprocess, sys, tempfile, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "automacao"))
from limpar_publicados import publicado, alvos as intermediarios  # noqa: E402

CFG = json.loads((ROOT / "automacao" / "armazenamento.json").read_text(encoding="utf-8"))
REMOTO, MONT = CFG["remoto"], Path(CFG["montagem"].rstrip("\\/") + "\\")
MIDIA = set(CFG["extensoes_midia"])
REG = ROOT / "_armazenamento" / "registro.jsonl"
LIVE = ROOT / "videosGTAVI" / "_live"
PROD = ROOT / "producao"
GB = 1024 ** 3


# ------------------------------------------------------------------ base
def rclone_bin():
    return shutil.which("rclone") or str(Path(os.environ["LOCALAPPDATA"]) / "Microsoft/WinGet/Links/rclone.exe")


def rclone(*args, check=True):
    r = subprocess.run([rclone_bin(), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"rclone {' '.join(args[:2])}: {r.stderr.strip()[-600:]}")
    return r


def rel(p):
    return Path(os.path.abspath(p)).relative_to(ROOT).as_posix()


def registrar(acao, **k):
    REG.parent.mkdir(exist_ok=True)
    with REG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"quando": datetime.now().isoformat(timespec="seconds"), "acao": acao, **k},
                           ensure_ascii=False) + "\n")


def montado():
    return MONT.exists()


def eh_midia(p):
    try:
        return p.suffix.lower() in MIDIA or p.stat().st_size >= CFG["arquivar_acima_mb"] * 1e6
    except OSError:
        return False


def arquivos(alvos_):
    for a in alvos_:
        a = Path(a) if Path(a).is_absolute() else ROOT / a
        it = [a] if a.is_file() or a.is_symlink() else a.rglob("*")
        for p in it:
            yield p


def remoto_lista(prefixo):
    """{caminho relativo ao projeto: bytes} de tudo que esta no Drive sob o prefixo."""
    r = rclone("lsjson", "-R", "--files-only", "--no-mimetype", "--no-modtime", f"{REMOTO}/{prefixo}", check=False)
    if r.returncode:
        return {}
    return {f"{prefixo}/{x['Path']}": x["Size"] for x in json.loads(r.stdout or "[]")}


# ------------------------------------------------------------------ arquivar / trazer
def arquivar(alvos_, executar, rotulo="arquivar"):
    lista = [p for p in arquivos(alvos_) if p.is_file() and not p.is_symlink() and eh_midia(p)]
    tot = sum(p.stat().st_size for p in lista)
    print(f"[{'arquiva' if executar else 'simula'}] {len(lista)} arquivos, {tot / GB:.2f} GB")
    if not executar or not lista:
        return tot
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
        f.write("\n".join(rel(p) for p in lista))
        fl = f.name
    try:
        rclone("copy", str(ROOT), REMOTO, "--files-from", fl, "--checksum", "--transfers", "4",
               "--drive-chunk-size", "64M", "--retries", "5")
        chk = rclone("check", str(ROOT), REMOTO, "--files-from", fl, "--one-way", "--checksum", check=False)
        if chk.returncode:
            raise RuntimeError("conferencia md5 falhou; nada foi apagado localmente:\n" + chk.stderr[-800:])
        for p in lista:
            r_ = rel(p)
            p.unlink()
            os.symlink(MONT / Path(r_), p)
        registrar(rotulo, arquivos=len(lista), gb=round(tot / GB, 3), itens=[rel(p) for p in lista])
        print(f"  ok: {tot / GB:.2f} GB agora no Drive (links em {MONT})")
    finally:
        os.unlink(fl)
    return tot


def trazer(alvos_, executar):
    lista = [p for p in arquivos(alvos_) if p.is_symlink()]
    print(f"[{'traz' if executar else 'simula'}] {len(lista)} arquivos")
    for p in lista if executar else []:
        tmp = p.with_name(p.name + ".baixando")
        rclone("copyto", f"{REMOTO}/{rel(p)}", str(tmp))
        p.unlink()
        tmp.rename(p)
    if executar and lista:
        registrar("trazer", itens=[rel(p) for p in lista])


def apagar(rels, executar, motivo):
    """Apaga do Drive (lixeira) e o link/arquivo local. rels: caminhos relativos ao projeto."""
    if not executar or not rels:
        return
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
        f.write("\n".join(rels))
        fl = f.name
    try:
        rclone("delete", REMOTO, "--files-from", fl, check=False)
    finally:
        os.unlink(fl)
    for r_ in rels:
        p = ROOT / r_
        if p.is_symlink() or p.exists():
            p.unlink()
    registrar("apagar", motivo=motivo, itens=rels)


# ------------------------------------------------------------------ itens e valor
def idade_dias(iso_ou_ts):
    try:
        t = datetime.fromisoformat(iso_ou_ts).timestamp() if isinstance(iso_ou_ts, str) else float(iso_ou_ts)
    except Exception:
        return 0
    return max(0, (time.time() - t) / 86400)


def itens_lives(remoto):
    """Um item por clipe e por compilacao (_longos), com o que ocupa no Drive."""
    longos = {}
    for mp in (LIVE / "_longos").glob("*/meta.json"):
        m = json.loads(mp.read_text(encoding="utf-8"))
        pub = m.get("status") == "publicado" or (mp.parent / "POSTIZ_ESTADO.json").exists() and \
            publicado(mp.parent / "POSTIZ_ESTADO.json")[0]
        for c in m.get("clipes", []):
            longos[c] = longos.get(c) or pub
    out = []
    for mp in LIVE.glob("*/*/*/meta.json"):
        d = mp.parent
        if d.relative_to(LIVE).parts[0].startswith("_"):
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        r_ = rel(d) + "/"
        arqs = {k: v for k, v in remoto.items() if k.startswith(r_)}
        if not arqs:
            continue
        st = m.get("status")
        prot = (st in ("extraido", "empacotado", "aguardando_aprovacao")
                or ((d / "APROVADO").exists() and st != "publicado") or longos.get(m.get("id")) is False)
        base = (m.get("nota") or 50) / 100
        if st == "publicado":
            base += 0.3 + min(0.4, math.log10((m.get("metricas", {}).get("views") or 0) + 1) / 15)
        if m.get("id") in longos:
            base += 0.2
        if st in ("descartado", "duplicata", "rejeitado"):
            base *= 0.3
        valor = base * 0.5 ** (idade_dias(m.get("gravado_em") or mp.stat().st_mtime) / CFG["meia_vida_dias"]["lives"])
        deriv = [k for k in arqs if Path(k).name in CFG["derivados_live"]]
        out.append({"cat": "lives", "id": rel(d), "valor": valor, "protegido": prot,
                    "fases": [(0.2, deriv), (0.8, [k for k in arqs if k not in deriv])], "arqs": arqs})
    # compilacoes (_longos/<id>): protegidas ate publicar; depois valem 0,6 com a mesma meia-vida
    for d in (LIVE / "_longos").glob("*"):
        r_ = rel(d) + "/"
        arqs = {k: v for k, v in remoto.items() if k.startswith(r_)}
        if not d.is_dir() or not arqs:
            continue
        est = d / "POSTIZ_ESTADO.json"
        m = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else {}
        pub = m.get("status") == "publicado" or (est.exists() and publicado(est)[0])
        valor = 0.6 * 0.5 ** (idade_dias(d.stat().st_mtime) / CFG["meia_vida_dias"]["lives"])
        deriv = [k for k in arqs if Path(k).name in CFG["derivados_live"] or "/_v2/" in k]
        out.append({"cat": "lives", "id": rel(d), "valor": valor, "protegido": not pub,
                    "fases": [(0.2, deriv), (0.8, [k for k in arqs if k not in deriv])], "arqs": arqs})
    return out


def itens_publicados(remoto):
    out = []
    for est in PROD.rglob("publicacao/POSTIZ_ESTADO.json"):
        d = est.parent.parent
        r_ = rel(d) + "/"
        arqs = {k: v for k, v in remoto.items() if k.startswith(r_)}
        if not arqs:
            continue
        ok, _ = publicado(est)
        valor = 0.5 ** (idade_dias(est.stat().st_mtime) / CFG["meia_vida_dias"]["publicados"])
        inter = {rel(p) for p in intermediarios(d, incluir_links=True)} & set(arqs)
        final = [k for k in arqs if k not in inter and "/publicacao/" not in k]
        out.append({"cat": "publicados", "id": rel(d), "valor": valor, "protegido": not ok,
                    "fases": [(0.1, sorted(inter)), (0.9, final)], "arqs": arqs, "estado": est})
    return out


def aplicar_cotas(itens, executar, excl):
    for cat, cota in CFG["cotas_gb"].items():
        its = [i for i in itens if i["cat"] == cat]
        uso = sum(sum(i["arqs"].values()) for i in its) / GB
        alvo = cota * CFG["alvo_pct"] / 100
        print(f"[cota] {cat}: {uso:.1f} / {cota} GB" + ("" if uso <= cota else f" -> reduzir ate {alvo:.0f} GB"))
        if uso <= cota:
            continue
        passos = []
        for i in its:
            if i["protegido"] or any(e in i["id"] for e in excl):
                continue
            acum = []
            for peso, ks in i["fases"]:
                acum = acum + ks
                gb = sum(i["arqs"][k] for k in acum) / GB
                if gb > 0:
                    passos.append(((i["valor"] * peso) / gb, i, list(acum)))
        feito = {}
        for custo, i, ks in sorted(passos, key=lambda x: x[0]):
            if uso <= alvo:
                break
            novos = [k for k in ks if k not in feito.get(i["id"], set())]
            if not novos:
                continue
            gb = sum(i["arqs"][k] for k in novos) / GB
            print(f"  {'APAGA' if executar else 'simula'} {gb:5.2f} GB  custo={custo:.3f}  {i['id']} ({len(novos)} arq)")
            apagar(novos, executar, f"cota {cat}")
            feito.setdefault(i["id"], set()).update(novos)
            uso -= gb


# ------------------------------------------------------------------ comandos
def cmd_status(_a):
    livre = shutil.disk_usage(ROOT).free / GB
    cache = Path(os.environ["LOCALAPPDATA"]) / "rclone" / "vfs"
    cgb = sum(f.stat().st_size for f in cache.rglob("*") if f.is_file()) / GB if cache.exists() else 0
    print(f"disco local livre: {livre:.0f} GB | cache rclone: {cgb:.1f} / {CFG['cache_local_gb']} GB | "
          f"montagem {MONT}: {'OK' if montado() else 'NAO MONTADO (rode automacao/montar_drive.ps1)'}")
    for nome, pref in (("lives", "videosGTAVI/_live"), ("producao", "producao"), ("curso", "_curso")):
        gb = sum(remoto_lista(pref).values()) / GB
        cota = CFG["cotas_gb"].get(nome if nome != "producao" else "publicados")
        print(f"Drive {nome:9}: {gb:7.1f} GB" + (f" / cota {cota} GB" if cota else ""))
    quebrados = [p for pref in CFG["pastas"] for p in (ROOT / pref).rglob("*") if p.is_symlink() and not p.exists()]
    if quebrados and montado():
        print(f"ATENCAO: {len(quebrados)} links sem arquivo no Drive, ex.: {rel(quebrados[0])}")


def cmd_automatico(a):
    if not montado():
        sys.exit(f"montagem {MONT} ausente: rode .\\automacao\\montar_drive.ps1 antes")
    excl = [rel(ROOT / e) if (ROOT / e).exists() else e for e in a.excluir]
    hoje = datetime.now().strftime("%Y-%m-%d")
    lim = time.time() - CFG["inativo_horas"] * 3600
    # 1) arquivar
    sys.path.insert(0, str(ROOT / "automacao"))
    import captura_live as cl
    vivas = {cl.pasta_acervo(d.name) for d in (PROD / "live").glob("*") if d.is_dir() and cl.gravando(d)}
    candidatos = [d for d in LIVE.glob("*/*") if d.parent.name < hoje and d not in vivas
                  and not d.parent.name.startswith("_")]
    candidatos += [d for d in (LIVE / "_longos").glob("*") if d.is_dir()]
    eps = []
    for d in sorted(PROD.iterdir()):
        if not d.is_dir() or d.name == "live":
            continue
        subs = [s for s in d.iterdir() if s.is_dir()]
        serie = subs and not any((d / n).exists() for n in ("episodio.json", "producao.json", "publicacao"))
        eps += subs if serie and all((s / "episodio.json").exists() or (s / "producao.json").exists()
                                     or (s / "publicacao").exists() for s in subs) else [d]
    for d in eps:
        if any(rel(d).startswith(e) or e in d.name for e in excl):
            continue
        # so a midia conta como "em uso": editar roteiro/json nao impede arquivar os videos
        recentes = [p for p in d.rglob("*") if p.is_file() and not p.is_symlink() and eh_midia(p)
                    and p.stat().st_mtime > lim]
        if not recentes:
            candidatos.append(d)
    for d in candidatos:
        pend = [p for p in arquivos([d]) if p.is_file() and not p.is_symlink() and eh_midia(p)]
        if pend:
            print(f"- {rel(d)}")
            arquivar([d], a.executar, "automatico")
    # 2) intermediarios de publicados antigos  3) cotas
    remoto = {**remoto_lista("videosGTAVI/_live"), **remoto_lista("producao")}
    itens = itens_lives(remoto) + itens_publicados(remoto)
    for i in itens:
        if i["cat"] == "publicados" and not i["protegido"] and \
                idade_dias(i["estado"].stat().st_mtime) >= CFG["intermediarios_apos_dias"] and i["fases"][0][1]:
            print(f"[intermediarios] {i['id']}: {sum(i['arqs'][k] for k in i['fases'][0][1]) / GB:.2f} GB")
            apagar(i["fases"][0][1], a.executar, "intermediarios de publicado")
            for k in i["fases"][0][1]:
                i["arqs"].pop(k, None)
            i["fases"][0] = (i["fases"][0][0], [])
    aplicar_cotas(itens, a.executar, excl)
    if not a.executar:
        print("\n(simulacao; use --executar para aplicar)")


def outra_execucao():
    """True se outro processo python roda armazenamento.py com --executar (duas copias criariam duplicatas no Drive)."""
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='py.exe'\" | "
          f"Where-Object {{ $_.ProcessId -ne {os.getpid()} -and $_.ProcessId -ne {os.getppid()} -and "
          "$_.CommandLine -match 'armazenamento\\.py' -and $_.CommandLine -match '--executar' } | "
          "Select-Object -ExpandProperty ProcessId")
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True)
    outros = [int(x) for x in r.stdout.split() if x.isdigit()]
    # o py.exe lancador e o python.exe filho aparecem juntos; ignora o par desta execucao
    return any(pid not in (os.getpid(), os.getppid()) for pid in outros)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("status")
    for n in ("arquivar", "trazer"):
        x = sp.add_parser(n)
        x.add_argument("alvos", nargs="+")
        x.add_argument("--executar", action="store_true")
    x = sp.add_parser("automatico")
    x.add_argument("--excluir", nargs="*", default=[])
    x.add_argument("--executar", action="store_true")
    a = ap.parse_args()
    if a.cmd != "status" and getattr(a, "executar", False) and outra_execucao():
        sys.exit("outra execucao de armazenamento.py esta rodando; tente mais tarde (evita envio duplicado no Drive)")
    if a.cmd == "status":
        cmd_status(a)
    elif a.cmd == "arquivar":
        if a.executar and not montado():
            sys.exit(f"montagem {MONT} ausente: rode .\\automacao\\montar_drive.ps1 antes")
        arquivar(a.alvos, a.executar)
    elif a.cmd == "trazer":
        trazer(a.alvos, a.executar)
    else:
        cmd_automatico(a)


if __name__ == "__main__":
    sys.exit(main())
