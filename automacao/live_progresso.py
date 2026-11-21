"""Painel de progresso das lives: gera producao/live/PROGRESSO.html (auto-atualiza a cada 15 s).

Uso (a partir da raiz, py -3.12):
  automacao/live_progresso.py            # gera uma vez
  automacao/live_progresso.py --loop     # regenera a cada 15 s (deixe em segundo plano)
Somente leitura: nao altera clipes, estado nem publicacao.
"""
import argparse, html, json, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "producao" / "live"
ACERVO = ROOT / "videosGTAVI" / "_live"
sys.path.insert(0, str(ROOT / "automacao"))
from captura_live import pasta_acervo  # noqa: E402
OUT = LIVE / "PROGRESSO.html"

ETAPAS = ["Cortado", "Empacotado", "Narrado", "Capa", "Plano", "Publicado"]


def lj(p, d=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return d


def tail(p, n=1):
    try:
        return Path(p).read_text(encoding="utf-8", errors="replace").strip().splitlines()[-n:]
    except Exception:
        return []


def etapas(pasta, m):
    st = m.get("status")
    feitas = {"Cortado": True,
              "Empacotado": (pasta / "vertical.mp4").exists() or st in ("empacotado", "publicado"),
              "Narrado": bool(m.get("narrado")),
              "Capa": bool(m.get("capa")) or (pasta / "thumbnail_base_gerada.png").exists(),
              "Plano": (pasta / "episodio.json").exists(),
              "Publicado": st == "publicado"}
    if st == "duplicata":
        return feitas, "duplicata (descartado)"
    if st == "publicado":
        return feitas, "PUBLICADO"
    if st == "erro_publicacao":
        return feitas, "ERRO ao publicar (veja publicacao.log)"
    if st == "retido":
        return feitas, "retido: " + ", ".join(m.get("retido_por") or [])
    if st == "aguardando_aprovacao":
        return feitas, "aguardando seu APROVADO"
    if st == "extraido":
        return feitas, "na fila para empacotar"
    if m.get("nota", 0) < 70:
        return feitas, "guardado no acervo (nota baixa, nao publica)"
    if (pasta / "episodio.json").exists():
        return feitas, "pronto; publica no proximo ciclo (intervalo de 30 min entre posts)"
    return feitas, "em producao"


def render():
    status = subprocess.run([sys.executable, str(ROOT / "automacao/live_multi.py"), "status"], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    livre = shutil.disk_usage(ROOT).free / 1e9
    secs = []
    for d in sorted(p for p in LIVE.glob("*") if (p / "estado.json").exists()):
        est = lj(d / "estado.json", {})
        logs = sorted(d.glob("auto*.log"), key=lambda p: p.stat().st_mtime)  # o reinicio do ciclo grava em auto<N>.log
        linhas = tail(logs[-1], 3) if logs else []
        rows = []
        for mp in sorted(pasta_acervo(d.name).glob("*/meta.json")):
            m = lj(mp, {})
            if not m.get("id"):
                continue
            feitas, texto = etapas(mp.parent, m)
            chips = "".join(f'<span class="c {"ok" if feitas[e] else ""}">{e}</span>' for e in ETAPAS)
            rows.append(f'<tr><td>{html.escape(m.get("hms", ["?"])[0])}</td><td><b>{html.escape(m.get("titulo", ""))}</b>'
                        f'<br><small>{html.escape(m["id"])}</small></td><td>{m.get("nota", "")}</td>'
                        f'<td>{chips}<br><small>{html.escape(texto)}</small></td></tr>')
        secs.append(f'<h2>{html.escape(d.name)}</h2><p>{len(est.get("processados", []))} picos avaliados, '
                    f'{len(est.get("clips", []))} clipes guardados, {len(est.get("rejeitados", []))} descartados</p>'
                    f'<table><tr><th>Hora</th><th>Clipe</th><th>Nota</th><th>Etapas</th></tr>{"".join(rows) or "<tr><td colspan=4>nenhum clipe ainda</td></tr>"}</table>'
                    f'<pre>{html.escape(chr(10).join(linhas))}</pre>')
    avisos = "\n".join(tail(LIVE / "AVISOS.md", 8))
    try:
        sys.path.insert(0, str(ROOT / "automacao"))
        import custos
        r = custos.resumo()
        livre_txt = " · ".join(f"{t}: {n}× US$ {u:.3f}" for t, (n, u) in sorted(r["por_tipo"].items()))
        status += f"\ncusto API: US$ {r['total']:.3f} ({r['chamadas']} chamadas) | {livre_txt}"
    except Exception:
        pass
    pagina = f"""<!doctype html><html lang="pt-br"><head><meta charset="utf-8"><meta http-equiv="refresh" content="15">
<title>Progresso das lives</title><style>
body{{font:14px system-ui;background:#111;color:#eee;margin:20px;max-width:1000px}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #333;padding:6px;text-align:left;vertical-align:top}}
.c{{display:inline-block;padding:1px 7px;margin:1px;border-radius:9px;background:#333;color:#888;font-size:12px}}
.c.ok{{background:#1f6f3a;color:#fff}}pre{{background:#1a1a1a;padding:8px;overflow:auto;white-space:pre-wrap}}small{{color:#999}}
</style></head><body><h1>Progresso das lives</h1>
<p>Atualizado {datetime.now():%H:%M:%S} · disco livre {livre:.0f} GB</p><pre>{html.escape(status)}</pre>
{"".join(secs) or "<p>Nenhuma live ativa.</p>"}<h2>Avisos recentes</h2><pre>{html.escape(avisos)}</pre></body></html>"""
    OUT.write_text(pagina, encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--loop", action="store_true")
    a = ap.parse_args()
    while True:
        render()
        if not a.loop:
            break
        time.sleep(15)
