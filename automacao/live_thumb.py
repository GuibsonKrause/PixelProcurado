"""Thumbnail dos clipes de live (e da compilacao longa).

Dois modos (a escolha do modo e do ambiente que roda o fluxo):
  auto    Codex / Antigravity: gera a arte-base sem texto via automacao/gerar_arte_thumbnail.ps1 (Gemini, faturavel)
          e compoe texto+logo deterministicamente com compose_thumbnail.py.
  prompt  Claude: NAO chama API de imagem. Grava <pasta>/thumb_prompt.md com o prompt completo; voce gera a imagem em
          outro lugar, salva como <pasta>/thumbnail_base_gerada.png e o proximo ciclo (ou `compor`) faz o resto.
  nenhum  Sem thumbnail.

  py -3.12 automacao/live_thumb.py --pasta videosGTAVI/_live/<live>/<id> [--modo auto|prompt|nenhum] [--formato short|long]
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import captura_live as cl
from gerar_arte_thumbnail import montar_prompt

ROOT = cl.ROOT
COMPOSE = ROOT / ".agents/skills/pixel-procurado-thumbnails/scripts/compose_thumbnail.py"
BASE = "thumbnail_base_gerada.png"


def linhas_titulo(titulo):
    pal = re.sub(r"[^\w\sÀ-ÿ'-]", "", titulo or "").split() or ["MOMENTO", "GTA VI"]
    if len(pal) <= 2:
        return pal[0], " ".join(pal[1:]) or "GTA VI"
    meio = (len(pal) + 1) // 2
    return " ".join(pal[:meio][:3]), " ".join(pal[meio:][:3])


def prompt_base(meta, formato):
    cena = (meta.get("motivo") or meta.get("titulo") or "momento de gameplay").strip()
    tipo = "vertical 9:16 (capa de Short)" if formato == "short" else "horizontal 16:9 (capa de video longo)"
    return (f"Arte editorial {tipo} para um video do canal Pixel Procurado sobre GTA VI: {cena}. "
            f"Cenario urbano tropical estilo Vice City ao entardecer, atmosfera de tensao e humor, "
            f"um unico assunto principal grande e facil de reconhecer, sem personagens reais identificaveis.")


def compor(pasta, meta, formato="short"):
    base = pasta / BASE
    if not base.exists():
        return False
    l1, l2 = linhas_titulo(meta.get("titulo"))
    r = subprocess.run([sys.executable, str(COMPOSE), "--base", str(base), "--output-dir", str(pasta / "capa"),
                        "--line1", l1, "--line2", l2, "--format", formato], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-300:])
    meta["capa"] = (pasta / "capa" / "capa_youtube.jpg").relative_to(ROOT).as_posix()
    return True


def preparar(pasta, meta, modo, formato="short"):
    """Devolve 'composta' | 'gerada' | 'prompt' | 'nenhum'."""
    if modo == "nenhum":
        return "nenhum"
    pronta = next((p for p in (pasta / "capa_pronta.png", pasta / "capa_pronta.jpg") if p.exists()), None)
    if pronta:  # imagem ja com texto e logo (feita pelo usuario): so converte, nao compoe de novo
        from PIL import Image
        (pasta / "capa").mkdir(exist_ok=True)
        dest = pasta / "capa" / "capa_youtube.jpg"
        Image.open(pronta).convert("RGB").resize((1280, 720), Image.LANCZOS).save(dest, quality=92)
        meta["capa"] = dest.relative_to(ROOT).as_posix()
        return "composta"
    if (pasta / BASE).exists():
        if (pasta / "capa" / "capa_youtube.jpg").exists():
            meta["capa"] = (pasta / "capa" / "capa_youtube.jpg").relative_to(ROOT).as_posix()
        else:
            compor(pasta, meta, formato)
        return "composta"
    base_txt = prompt_base(meta, formato)
    (pasta / "thumb_prompt.txt").write_text(base_txt, encoding="utf-8")
    fmt = "short" if formato == "short" else "longo"
    if modo == "auto":
        r = subprocess.run(["powershell", "-NoProfile", "-File", str(ROOT / "automacao/gerar_arte_thumbnail.ps1"),
                            "--prompt-file", str(pasta / "thumb_prompt.txt"), "--formato", fmt,
                            "--saida", str(pasta / BASE)], cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError("arte-base falhou: " + (r.stderr or r.stdout)[-300:])
        compor(pasta, meta, formato)
        return "composta"
    final = montar_prompt(base_txt, fmt)
    ref = pasta / "story.png"
    (pasta / "thumb_prompt.md").write_text(
        f"# Prompt de imagem - {meta.get('id')}\n\n"
        f"Gere UMA imagem {'9:16 (1080x1920)' if formato == 'short' else '16:9 (1920x1080)'} em qualquer gerador "
        f"(ChatGPT, Gemini app, Midjourney etc.) com o prompt abaixo.\n\n"
        f"## Prompt\n\n```\n{final}```\n\n"
        f"## Referencia opcional\n\nQuadro do clipe (so para o clima, nao copie a interface): `{ref}`\n\n"
        f"## Depois de gerar\n\n1. Salve a imagem exatamente em: `{pasta / BASE}`\n"
        f"2. O proximo ciclo do fluxo compoe sozinho texto + logo (ou rode "
        f"`py -3.12 automacao/live_thumb.py --pasta \"{pasta}\" --modo prompt`).\n"
        f"3. Linhas da capa: **{linhas_titulo(meta.get('titulo'))[0].upper()}** / "
        f"**{linhas_titulo(meta.get('titulo'))[1].upper()}**\n", encoding="utf-8")
    return "prompt"


def listar_pendentes(raiz_live):
    """Atualiza <live>/PENDENTE_IMAGEM.md com os prompts ainda sem imagem."""
    linhas = ["# Imagens pendentes (gere fora e salve no caminho indicado)\n"]
    n = 0
    for pm in sorted(raiz_live.glob("*/thumb_prompt.md")):
        if not (pm.parent / BASE).exists():
            n += 1
            linhas.append(f"- [{pm.parent.name}]({pm.as_posix()}) -> salvar em `{pm.parent / BASE}`")
    (raiz_live / "PENDENTE_IMAGEM.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pasta", required=True)
    ap.add_argument("--modo", choices=("auto", "prompt", "nenhum"), default="prompt")
    ap.add_argument("--formato", choices=("short", "long"), default="short")
    a = ap.parse_args()
    pasta = Path(a.pasta).resolve()
    mp = pasta / "meta.json"
    meta = cl.lj(mp, {"id": pasta.name, "titulo": pasta.name})
    print(preparar(pasta, meta, a.modo, a.formato))
    if mp.exists():
        cl.sj(mp, meta)


if __name__ == "__main__":
    main()
