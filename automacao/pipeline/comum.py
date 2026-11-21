"""Utilidades compartilhadas do pipeline V2 (carregamento de episodio.json, caminhos, amostra)."""
import json
from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
FF = next((ROOT / ".production-tools/python/imageio_ffmpeg/binaries").glob("*.exe"))
SLUG = {"longo": "long", "short": "short"}
GSAP_PADRAO = "producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06/montagem/hyperframes_v2/gsap.min.js"


def erro(msg):
    sys.exit(f"ERRO: {msg}")


def carregar(pasta):
    pasta = Path(pasta)
    pasta = pasta if pasta.is_absolute() else ROOT / pasta
    arq = pasta / "episodio.json"
    if not arq.is_file():
        erro(f"{arq} não existe (copie automacao/pipeline/episodio.modelo.json)")
    ep = json.loads(arq.read_text(encoding="utf-8"))
    ep["_pasta"] = pasta.resolve()
    return ep


def caminho(rel):
    p = Path(rel)
    return p if p.is_absolute() else ROOT / p


def formatos(ep, escolha):
    nomes = [n for n in ("longo", "short") if n in ep["formatos"]]
    if escolha != "ambos":
        if escolha not in nomes:
            erro(f"formato '{escolha}' ausente em episodio.json")
        nomes = [escolha]
    return nomes


def vertical(fmt):
    w, h = fmt["resolucao"]
    return h > w


def escala(fmt):
    """Fator de escala em relação à geometria-base (1920 de largura no horizontal, 1080 no vertical)."""
    w, _ = fmt["resolucao"]
    return w / (1080 if vertical(fmt) else 1920)


def parse_amostra(texto):
    if not texto:
        return None
    try:
        a, b = (float(x) for x in texto.split("-"))
    except ValueError:
        erro("--amostra deve ser INICIO-FIM em segundos, ex.: 0-12")
    if b <= a:
        erro("--amostra: FIM deve ser maior que INICIO")
    return a, b


def pastas(ep, saida, amostra=None):
    """(BUILD, OUT). Amostra nunca grava sobre os arquivos aprovados do episódio."""
    base = Path(saida).resolve() if saida else (ep["_pasta"] / "amostra" if amostra else ep["_pasta"])
    return base / "montagem", base / "exportacoes"


def planos(fmt):
    """Lista de planos com contagem de quadros e offset global (acumulado em quadros)."""
    fps, off, res, card = fmt.get("fps", 60), 0, [], 0
    for i, p in enumerate(fmt["planos"]):
        a, b = p["corte"]
        n = round((b - a) * fps)
        ci = None if p.get("sem_card") else card
        card += 0 if p.get("sem_card") else 1
        res.append({**p, "i": i, "inicio_s": a, "fim_s": b, "n": n, "offset": off, "card_i": ci})
        off += n
    return res


def selecionar(todos, amostra):
    if not amostra:
        return todos
    sel = [p for p in todos if p["fim_s"] > amostra[0] and p["inicio_s"] < amostra[1]]
    if not sel:
        erro("a amostra não cobre nenhum plano")
    return sel


def nome_saida(fmt, amostra):
    return fmt["stem"] + ("_amostra" if amostra else "")
