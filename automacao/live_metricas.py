"""Metricas dos clipes publicados (Postiz) e calibragem do filtro.

  py -3.12 automacao/live_metricas.py coletar [--dias 30]    le `postiz analytics:post` dos posts publicados -> meta.json
  py -3.12 automacao/live_metricas.py calibrar               com >= 8 clipes medidos, grava producao/live/calibragem.json

`captura_live.py auto` le calibragem.json (nota_min, limiar) quando as flags nao sao passadas. Sem dados suficientes
nao muda nada. O formato exato do analytics do Postiz varia por rede: o parser soma series cujo rotulo contem
views/impressions/plays, likes, comments e shares; confira os numeros na primeira coleta real.
"""
import argparse, json, math, re, statistics, subprocess, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import captura_live as cl

ROOT, ACERVO = cl.ROOT, cl.ACERVO
CAL = ROOT / "producao" / "live" / "calibragem.json"
CHAVES = {"views": ("view", "impression", "play", "reach"), "likes": ("like",), "comments": ("comment",),
          "shares": ("share",)}


def analytics(post_id, dias):
    r = subprocess.run(["postiz.cmd", "analytics:post", post_id, "-d", str(dias)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", shell=True)
    m = re.search(r"(\[.*\]|\{.*\})", r.stdout, re.S)
    if not m:
        return {}
    try:
        dados = json.loads(m.group(1))
    except ValueError:
        return {}
    out = {k: 0 for k in CHAVES}
    for item in dados if isinstance(dados, list) else [dados]:
        rot = str(item.get("label", "")).lower()
        total = 0.0
        for p in item.get("data", []) if isinstance(item.get("data"), list) else []:
            try:
                total += float(p.get("total", 0) or 0)
            except (TypeError, ValueError):
                pass
        for k, termos in CHAVES.items():
            if any(t in rot for t in termos):
                out[k] += total
    return out


def coletar(a):
    n = 0
    for mp in sorted(cl.metas_acervo()):
        meta = cl.ljs(mp)
        if meta.get("status") != "publicado":
            continue
        est = cl.lj(mp.parent / "POSTIZ_ESTADO.json", {}).get("items", {})
        soma = {k: 0 for k in CHAVES}
        for rec in est.values():
            if rec.get("post_id") and rec.get("remote", {}).get("state") == "PUBLISHED":
                for k, v in analytics(rec["post_id"], a.dias).items():
                    soma[k] += v
        meta["metricas"] = {**soma, "coletado_em": datetime.now().isoformat(timespec="seconds")}
        cl.sj(mp, meta)
        n += 1
        print(meta["id"], meta["metricas"])
    print(f"{n} clipes medidos")


def pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else 0.0


def calibrar(a):
    pts = []
    for mp in cl.metas_acervo():
        m = cl.ljs(mp)
        if m.get("metricas", {}).get("views") and m.get("nota") is not None:
            pts.append(m)
    if len(pts) < a.minimo:
        print(f"{len(pts)} clipes com views; preciso de {a.minimo}. Calibragem inalterada.")
        return
    views = [math.log1p(m["metricas"]["views"]) for m in pts]
    r_nota = pearson([m["nota"] for m in pts], views)
    mediana = statistics.median(views)
    top = [m for m, v in zip(pts, views) if v >= mediana]
    cal = cl.lj(CAL, {})
    if r_nota > 0.3:
        cal["nota_min"] = int(max(65, min(80, statistics.quantiles([m["nota"] for m in top], n=4)[0])))
        # so clipes da versao atual do score (v1 e v2 tem escalas diferentes) e de origem automatica
        sc = [m["score"] for m in top if isinstance(m.get("score"), (int, float)) and m.get("origem") == "auto"
              and m.get("score_versao") == cl.SCORE_VERSAO]
        if len(sc) >= 4:
            cal["limiar"] = round(max(1.0, min(2.5, statistics.quantiles(sc, n=4)[0])), 2)
            cal["score_versao"] = cl.SCORE_VERSAO
    # quanto cada subnota da rubrica acompanha as views (para ajustar PESOS_RUBRICA no futuro)
    com_sub = [(m, v) for m, v in zip(pts, views) if m.get("sub")]
    if len(com_sub) >= a.minimo:
        cal["r_sub_views"] = {k: round(pearson([m["sub"].get(k, 0) for m, _ in com_sub], [v for _, v in com_sub]), 2)
                              for k in cl.PESOS_RUBRICA}
        cal["r_rubrica_views"] = round(pearson([m.get("nota_rubrica") or 0 for m, _ in com_sub],
                                               [v for _, v in com_sub]), 2)
    cal.update({"n": len(pts), "r_nota_views": round(r_nota, 2), "atualizado": datetime.now().isoformat(timespec="seconds")})
    cl.sj(CAL, cal)
    print("calibragem:", cal)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("coletar"); c.add_argument("--dias", type=int, default=30)
    k = sp.add_parser("calibrar"); k.add_argument("--minimo", type=int, default=8)
    a = ap.parse_args()
    {"coletar": coletar, "calibrar": calibrar}[a.cmd](a)


if __name__ == "__main__":
    main()
