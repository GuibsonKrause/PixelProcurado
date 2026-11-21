"""Libera disco apagando os videos pesados de episodios JA PUBLICADOS.

Uso (a partir da raiz, py -3.12):
  py -3.12 automacao/limpar_publicados.py [--excluir PASTA ...]           # simulacao (padrao)
  py -3.12 automacao/limpar_publicados.py [--excluir PASTA ...] --apagar  # apaga de verdade

Regras de seguranca:
- So considera pastas com publicacao/POSTIZ_ESTADO.json em que TODAS as pecas tem remote.state == PUBLISHED e
  remote.releaseURL (rode antes `distribuir_postiz.py --episodio <pasta> --status` para atualizar o estado).
- Pecas agendadas (QUEUE), com erro ou sem estado: o episodio inteiro e PULADO.
- Nunca toca em --excluir (episodio em producao) nem fora de producao/.
- Apaga apenas videos regeneraveis: exportacoes/*.mp4 e *.mov, pastas amostra*/ e qa*/amostras, e
  montagem/**/*.mp4|*.mov (blocos e paineis). Preserva roteiro, audio, legendas, json, capas, carrossel e fontes.
- Grava LIMPEZA_<data>.json na pasta do episodio com a lista [(caminho relativo, bytes)].
"""
import argparse, json, sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROD = RAIZ / "producao"
EXT = {".mp4", ".mov"}


def publicado(estado_path):
    try:
        est = json.loads(estado_path.read_text(encoding="utf-8"))
        itens = est.get("items") or {}
    except Exception as e:
        return False, f"estado ilegivel ({e})"
    if not itens:
        return False, "sem pecas no estado"
    for chave, rec in itens.items():
        rm = rec.get("remote") or {}
        if rm.get("state") != "PUBLISHED" or not rm.get("releaseURL"):
            return False, f"{chave}: {rm.get('state') or 'sem estado'}"
    return True, "todas PUBLISHED"


def alvos(pasta):
    vistos, out = set(), []
    for p in pasta.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in EXT:
            continue
        partes = [x.lower() for x in p.relative_to(pasta).parts]
        if "referencias" in partes or "publicacao" in partes:
            continue
        # videos de entrega, amostras e blocos/paineis de montagem
        if "exportacoes" in partes or "montagem" in partes or any(x.startswith(("amostra", "qa")) for x in partes):
            if p not in vistos:
                vistos.add(p)
                out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--excluir", nargs="*", default=[], help="pastas em producao (nome ou caminho) a preservar")
    ap.add_argument("--apagar", action="store_true", help="apaga de verdade (padrao: simulacao)")
    a = ap.parse_args()
    excl = {Path(x).resolve() if Path(x).exists() else (RAIZ / x).resolve() for x in a.excluir}
    total = 0
    for estado in sorted(PROD.rglob("publicacao/POSTIZ_ESTADO.json")):
        pasta = estado.parent.parent
        if pasta.resolve() in excl or any(e in pasta.resolve().parents or e == pasta.resolve() for e in excl):
            print(f"[preservado] {pasta.relative_to(RAIZ)}")
            continue
        ok, motivo = publicado(estado)
        if not ok:
            print(f"[pulado] {pasta.relative_to(RAIZ)}: {motivo}")
            continue
        lista = [(str(p.relative_to(pasta)).replace("\\", "/"), p.stat().st_size) for p in alvos(pasta)]
        mb = sum(b for _, b in lista) / 1e6
        print(f"[{'APAGA' if a.apagar else 'simula'}] {pasta.relative_to(RAIZ)}: {len(lista)} arquivos, {mb:,.0f} MB")
        if a.apagar and lista:
            for rel, _ in lista:
                (pasta / rel).unlink(missing_ok=True)
            (pasta / f"LIMPEZA_{date.today().isoformat()}.json").write_text(
                json.dumps(lista, ensure_ascii=False, indent=1), encoding="utf-8")
        total += mb
    print(f"\nTotal {'liberado' if a.apagar else 'liberavel'}: {total/1000:,.2f} GB")


if __name__ == "__main__":
    sys.exit(main())
