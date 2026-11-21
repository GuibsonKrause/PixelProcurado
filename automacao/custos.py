"""Registro de custo das chamadas pagas (Gemini texto/quadros, TTS, imagem) em producao/live/custos.jsonl.

Cada chamada grava uma linha com tokens reais (usageMetadata) e o custo em USD pelos precos abaixo.
Resumo:  py -3.12 automacao/custos.py [--cambio 5.50] [--por clipe]
So biblioteca padrao (importavel tambem pelo .venv-gemini).

Precos: pagina oficial https://aistudio.google.com/docs/pricing (nivel pago, Standard, USD por 1M tokens), lida em
2026-11-18. Os valores de 2027 entram sozinhos a partir de 01/01/2027 — confira a pagina se o preco mudar.
"""
import argparse, json, sys
from collections import defaultdict
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "producao" / "live" / "custos.jsonl"
VIRADA = date(2027, 1, 1)

# USD por 1M tokens: (ate 2026, a partir de 2027). saida_img = tokens de IMAGEM gerada; saida_audio = tokens de audio.
PRECOS = {
    "gemini-3.8-flash": {"entrada": (0.75, 1.50), "saida": (3.75, 7.50)},  # saida inclui tokens de raciocinio
    "gemini-3.8-flash-tts": {"entrada": (0.50, 1.00), "saida_audio": (9.00, 18.00)},
    "gemini-3-pro-image": {"entrada": (2.00, 2.00), "saida": (12.00, 12.00), "saida_img": (120.00, 120.00)},
    "gemini-3.1-flash-image": {"entrada": (0.50, 0.50), "saida": (3.00, 3.00), "saida_img": (60.00, 60.00)},
}
TOKENS_AUDIO_POR_S = 25  # TTS: 25 tokens por segundo de audio gerado


def preco(modelo, campo, quando=None):
    tabela = PRECOS.get(modelo) or PRECOS.get(modelo.split("/")[-1])
    if not tabela or campo not in tabela:
        return None
    a, b = tabela[campo]
    return b if (quando or date.today()) >= VIRADA else a


def custo_usage(modelo, um):
    """um = usageMetadata (dict da API REST). Retorna (custo_usd, detalhe) ou (None, detalhe) se o modelo nao tem preco."""
    ent = um.get("promptTokenCount", 0)
    cand = um.get("candidatesTokenCount", 0)
    pens = um.get("thoughtsTokenCount", 0)
    img = sum(d.get("tokenCount", 0) for d in um.get("candidatesTokensDetails", []) if d.get("modality") == "IMAGE")
    texto_saida = max(0, cand - img) + pens
    detalhe = {"tok_entrada": ent, "tok_saida": texto_saida, "tok_saida_img": img, "tok_pensamento": pens}
    p_in, p_out = preco(modelo, "entrada"), preco(modelo, "saida")
    if p_in is None or p_out is None:
        return None, detalhe
    total = ent * p_in / 1e6 + texto_saida * p_out / 1e6 + img * (preco(modelo, "saida_img") or 0) / 1e6
    return total, detalhe


def custo_tts(modelo, segundos, caracteres):
    tok_out = round(segundos * TOKENS_AUDIO_POR_S)
    tok_in = round(caracteres / 3.5)  # estimativa: a API de TTS nao devolve a contagem de entrada
    p_in, p_out = preco(modelo, "entrada"), preco(modelo, "saida_audio")
    if p_in is None or p_out is None:
        return None, {"tok_entrada": tok_in, "tok_saida_audio": tok_out}
    return tok_in * p_in / 1e6 + tok_out * p_out / 1e6, {"tok_entrada": tok_in, "tok_saida_audio": tok_out,
                                                         "estimado": True}


def registrar(tipo, modelo, custo, ctx="", **extra):
    """Nunca levanta excecao: registrar custo nao pode derrubar a producao."""
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        linha = {"ts": datetime.now().isoformat(timespec="seconds"), "tipo": tipo, "modelo": modelo,
                 "ctx": ctx, "usd": round(custo, 6) if custo is not None else None, **extra}
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    except Exception:
        pass


def registrar_usage(tipo, modelo, um, ctx=""):
    c, det = custo_usage(modelo, um or {})
    registrar(tipo, modelo, c, ctx, **det)


def ler():
    out = []
    try:
        for l in LOG.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(l))
            except Exception:
                pass
    except OSError:
        pass
    return out


def resumo():
    """{'total': usd, 'chamadas': n, 'por_tipo': {tipo: (n, usd)}, 'por_ctx': {ctx: usd}, 'sem_preco': n}"""
    r = {"total": 0.0, "chamadas": 0, "por_tipo": defaultdict(lambda: [0, 0.0]), "por_ctx": defaultdict(float),
         "sem_preco": 0}
    for e in ler():
        r["chamadas"] += 1
        t = r["por_tipo"][e["tipo"]]
        t[0] += 1
        if e.get("usd") is None:
            r["sem_preco"] += 1
            continue
        t[1] += e["usd"]
        r["total"] += e["usd"]
        r["por_ctx"][(e.get("ctx") or "-").rsplit("_", 1)[0] if e["tipo"] == "avaliacao" else e.get("ctx") or "-"] += e["usd"]
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cambio", type=float, help="cotacao USD->BRL para mostrar tambem em reais")
    ap.add_argument("--por", choices=("tipo", "clipe"), default="tipo")
    a = ap.parse_args()
    r = resumo()
    brl = (lambda v: f" (R$ {v * a.cambio:.2f})") if a.cambio else (lambda v: "")
    print(f"{r['chamadas']} chamadas registradas | total US$ {r['total']:.4f}{brl(r['total'])}")
    for t, (n, usd) in sorted(r["por_tipo"].items()):
        print(f"  {t:22s} {n:4d} chamadas  US$ {usd:.4f}{brl(usd)}")
    if a.por == "clipe":
        for c, usd in sorted(r["por_ctx"].items()):
            print(f"  {c:40s} US$ {usd:.4f}{brl(usd)}")
    if r["sem_preco"]:
        print(f"  ({r['sem_preco']} chamadas sem preco conhecido para o modelo)")


if __name__ == "__main__":
    main()
