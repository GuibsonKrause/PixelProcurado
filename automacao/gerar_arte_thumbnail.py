"""Gera a arte-base (sem texto/logo) da thumbnail via Gemini Image API.

Rode com .venv-gemini (use gerar_arte_thumbnail.ps1). Saida pronta para
.agents/skills/pixel-procurado-thumbnails/scripts/compose_thumbnail.py (que faz cover 1280x720 / 1080x1920).
"""
import argparse
import io
import os
import sys
from pathlib import Path

MODELO_PADRAO = 'gemini-3-pro-image'  # "Nano Banana Pro", GA; alternativa barata: gemini-3.1-flash-image
FORMATOS = {  # aspect_ratio da API, tamanho final (master; compose reduz para 1280x720 no longo)
    'longo': ('16:9', (1920, 1080)),
    'short': ('9:16', (1080, 1920)),
}
RESTRICOES = (
    "REGRAS FIXAS DA ARTE (obrigatorias): nao escreva nenhum texto, letra, numero, legenda, marca d'agua, "
    "logotipo ou interface de jogo dentro da imagem; contraste alto, assunto principal grande e reconhecivel, "
    "iluminacao cinematografica, paleta grafite profundo com acentos neon (amarelo/rosa) quando fizer sentido; "
    "mantenha um espaco negativo limpo e escuro para o texto e o logo serem aplicados depois "
    "({espaco}); nao crie rostos de pessoas reais; e uma montagem editorial, nao uma captura de gameplay."
)
ESPACO = {
    'longo': 'cerca de 45% da largura num dos lados, e margens livres no alto',
    'short': 'os 35% superiores da altura, assunto principal no centro e na metade inferior',
}


def montar_prompt(base, formato):
    return f"{base.strip()}\n\n{RESTRICOES.format(espaco=ESPACO[formato])}\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--prompt-file', type=Path)
    g.add_argument('--prompt')
    ap.add_argument('--formato', choices=FORMATOS, required=True)
    ap.add_argument('--saida', type=Path, default=Path('thumbnail_base_gerada.png'))
    ap.add_argument('--referencia', type=Path, action='append', default=[])
    ap.add_argument('--modelo', default=MODELO_PADRAO)
    ap.add_argument('--sobrescrever', action='store_true')
    ap.add_argument('--dry-run', action='store_true', help='valida e mostra o plano, sem chamar a API paga')
    a = ap.parse_args()

    base = a.prompt_file.read_text(encoding='utf-8') if a.prompt_file else a.prompt
    if not base.strip():
        sys.exit('Erro: prompt vazio.')
    for r in a.referencia:
        if not r.is_file():
            sys.exit(f'Erro: referencia nao encontrada: {r}')
    saida = a.saida.resolve()
    if saida.exists() and not a.sobrescrever:
        sys.exit(f'Erro: {saida} ja existe. Use --sobrescrever ou outro --saida.')
    aspecto, tamanho = FORMATOS[a.formato]
    prompt = montar_prompt(base, a.formato)
    prompt_path = saida.with_name(saida.name + '.prompt.txt')

    print(f'Modelo: {a.modelo} | formato: {a.formato} ({aspecto}) -> {tamanho[0]}x{tamanho[1]}')
    print(f'Saida: {saida}\nPrompt usado: {prompt_path}\nReferencias: {[str(r) for r in a.referencia] or "nenhuma"}')
    print(f'Prompt final ({len(prompt)} caracteres):\n---\n{prompt}---')
    if a.dry_run:
        print('DRY-RUN: nenhuma chamada paga feita.')
        return

    sys.path[:0] = [str(Path(__file__).resolve().parent.parent / '.production-tools/python'),
                    str(Path(__file__).resolve().parent.parent / '.course-tools')]
    from google import genai
    from google.genai import types
    from PIL import Image

    if not os.environ.get('GEMINI_API_KEY'):
        sys.exit('Erro: GEMINI_API_KEY ausente (use o .ps1, que a le do ambiente do usuario).')
    partes = [prompt]
    for r in a.referencia:
        partes.append(Image.open(r))
    cfg = types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio=aspecto))
    cliente = genai.Client()
    resp = cliente.models.generate_content(model=a.modelo, contents=partes, config=cfg)
    try:  # registro de custo (nunca derruba a geracao)
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import custos
        um = resp.usage_metadata
        det = [{'modality': str(getattr(d.modality, 'name', d.modality)), 'tokenCount': d.token_count}
               for d in (getattr(um, 'candidates_tokens_details', None) or [])]
        custos.registrar_usage('imagem', a.modelo, {
            'promptTokenCount': um.prompt_token_count or 0, 'candidatesTokenCount': um.candidates_token_count or 0,
            'thoughtsTokenCount': getattr(um, 'thoughts_token_count', 0) or 0, 'candidatesTokensDetails': det},
            os.environ.get('CUSTO_CTX', ''))
    except Exception:
        pass
    dados = next((p.inline_data.data for c in (resp.candidates or []) for p in (c.content.parts or [])
                  if getattr(p, 'inline_data', None) and p.inline_data.data), None)
    if not dados:
        sys.exit(f'Erro: a API nao devolveu imagem (possivel bloqueio de seguranca). Resposta: {str(resp)[:500]}')
    img = Image.open(io.BytesIO(dados)).convert('RGB')
    # cover + crop central no tamanho exato
    esc = max(tamanho[0] / img.width, tamanho[1] / img.height)
    img = img.resize((round(img.width * esc), round(img.height * esc)), Image.Resampling.LANCZOS)
    l, t = (img.width - tamanho[0]) // 2, (img.height - tamanho[1]) // 2
    img = img.crop((l, t, l + tamanho[0], t + tamanho[1]))
    saida.parent.mkdir(parents=True, exist_ok=True)
    img.save(saida, 'PNG')
    prompt_path.write_text(prompt, encoding='utf-8')
    print(f'OK: {saida} ({tamanho[0]}x{tamanho[1]})')


if __name__ == '__main__':
    main()
