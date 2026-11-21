"""Cobre varias lives ao mesmo tempo (uma gravacao + um ciclo `auto` por live; processos pesados em fila por trava).

  py -3.12 automacao/live_multi.py iniciar <url1> <url2> ... [--publicar|--empacotar] [--narrar] [--imagem auto|prompt|nenhum]
  py -3.12 automacao/live_multi.py status
  py -3.12 automacao/live_multi.py parar [--nome <pasta>]

Cada live vira producao/live/<canal>_<AAAAMMDD>. Limite padrao de 3 lives (CPU/disco); ~3 GB/h por live em 1080p60.
"""
import argparse, os, re, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import captura_live as cl
from live_aviso import avisar

ROOT = cl.ROOT
LIVE = ROOT / "producao" / "live"
ATIVAS = LIVE / "_ativas.json"
CAPT = str(ROOT / "automacao" / "captura_live.py")


def nome_de(url):
    c = cl.canal_twitch(url) or re.sub(r"[^A-Za-z0-9_]", "", url.rstrip("/").split("/")[-1]) or "live"
    return f"{c}_{datetime.now():%Y%m%d}"


def bg(cmd, log):
    f = open(log, "a", encoding="utf-8")
    return subprocess.Popen(cmd, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT,
                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW)


def iniciar(a):
    LIVE.mkdir(parents=True, exist_ok=True)
    ativas = cl.lj(ATIVAS, {})
    vivas = [n for n in ativas if cl.gravando(LIVE / n)]
    if len(vivas) + len(a.urls) > a.max_lives:
        sys.exit(f"limite de {a.max_lives} lives simultaneas (ativas: {vivas})")
    livre = shutil.disk_usage(LIVE).free / 1e9
    if livre < 15 * (len(vivas) + len(a.urls)):
        sys.exit(f"disco insuficiente: {livre:.0f} GB livres (minimo ~15 GB por live)")
    for url in a.urls:
        nome = nome_de(url)
        saida = LIVE / nome
        if cl.gravando(saida):
            print(f"ja esta gravando: {nome} (ignorada)")
            continue
        saida.mkdir(parents=True, exist_ok=True)
        py = [sys.executable, CAPT]
        bg(py + ["gravar", url, "--saida", str(saida), "--espera"], saida / "gravar.log")
        auto = py + ["auto", "--saida", str(saida), "--loop", str(a.loop), "--imagem", a.imagem]
        if a.publicar:
            auto.append("--publicar")
        elif a.empacotar:
            auto.append("--empacotar")
        if a.narrar:
            auto.append("--narrar")
        bg(auto, saida / "auto.log")
        ativas[nome] = {"url": url, "inicio": datetime.now().isoformat(timespec="seconds")}
        print(f"iniciada: {nome}  (logs em {saida}\\gravar.log e auto.log)")
    # painel PROGRESSO.html: um unico processo de fundo (pidfile), religado a cada `iniciar` se tiver morrido
    pidf = LIVE / ".progresso.pid"
    try:
        vivo = cl.vivo(int(pidf.read_text().strip()))
    except Exception:
        vivo = False
    if not vivo:
        pr = bg([sys.executable, str(ROOT / "automacao" / "live_progresso.py"), "--loop"], LIVE / "progresso.log")
        pidf.write_text(str(pr.pid))
    cl.sj(ATIVAS, ativas)
    avisar("Lives iniciadas", ", ".join(ativas), "info")


def status(a):
    ativas = cl.lj(ATIVAS, {})
    if not ativas:
        print("nenhuma live registrada")
    for nome, d in ativas.items():
        saida = LIVE / nome
        if not saida.is_dir():
            continue
        est = cl.lj(saida / "estado.json", {})
        idx = cl.lj(saida / "indice.json", {"segs": []})
        segs = idx["segs"]
        print(f"{nome}: gravando={cl.gravando(saida)} indexado={cl.hms(sum(s['dur'] for s in segs))} "
              f"picos={len(est.get('processados', []))} clipes={len(est.get('clips', []))} "
              f"segmentos_em_disco={sum(1 for s in segs if not s['apagado'])}")
    print(f"disco livre: {shutil.disk_usage(LIVE).free / 1e9:.0f} GB")


def parar(a):
    ativas = cl.lj(ATIVAS, {})
    for nome in ([a.nome] if a.nome else list(ativas)):
        if not (LIVE / nome).is_dir():
            print(nome, "... pasta inexistente (entrada antiga), ignorada")
            continue
        ns = argparse.Namespace(saida=str(LIVE / nome))
        print(nome, "...", end=" ", flush=True)
        cl.parar(ns)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    i = sp.add_parser("iniciar")
    i.add_argument("urls", nargs="+")
    i.add_argument("--publicar", action="store_true"); i.add_argument("--empacotar", action="store_true")
    i.add_argument("--narrar", action="store_true")
    i.add_argument("--imagem", choices=("auto", "prompt", "nenhum"), default=os.environ.get("LIVE_IMAGEM_MODO", "prompt"))
    i.add_argument("--loop", type=int, default=90); i.add_argument("--max-lives", type=int, default=3)
    sp.add_parser("status")
    p = sp.add_parser("parar"); p.add_argument("--nome")
    a = ap.parse_args()
    {"iniciar": iniciar, "status": status, "parar": parar}[a.cmd](a)


if __name__ == "__main__":
    main()
