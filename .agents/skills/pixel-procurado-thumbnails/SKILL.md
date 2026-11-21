---
name: pixel-procurado-thumbnails
description: Criar ou refazer thumbnails do Pixel Procurado para Shorts verticais e vídeos longos horizontais, com arte temática de alto impacto, frases curtas, identidade grafite/branco/amarelo e logos corretas. Use quando o pedido envolver capa, thumbnail, CTR ou pacote visual de vídeo; não use para editar o vídeo, gerar narração ou publicar no YouTube.
---

# Thumbnails do Pixel Procurado

Crie capas que prometam com precisão o conflito do vídeo e continuem legíveis no tamanho de miniatura. Preserve o conteúdo: apelo visual não autoriza spoiler falso, personagem inexistente, captura inventada ou logo de outro jogo.

## Antes de compor

1. Leia o roteiro, título, descrição ou transcrição. Identifique uma única tensão central.
2. Confirme o formato: Short vertical ou vídeo longo horizontal.
3. Inspecione as imagens, logos e capas existentes. Preserve a versão anterior antes de substituí-la.
4. Leia [references/sistema-visual.md](references/sistema-visual.md). Para dimensões e layout, leia [references/formatos.md](references/formatos.md).
5. Identifique a intenção de busca e a promessa de cada peça. Use o título para nomear o assunto e a capa para abrir uma dúvida específica que o vídeo responde. Dê ao Short uma proposta própria e proteja assunto, texto e logo dos recortes de grade e das áreas da interface.

## Método

- Gere apenas a arte-base: cena temática, contraste alto, assunto reconhecível e espaço negativo planejado. Não peça texto nem logotipo dentro da imagem gerada.
  - **Padrão em qualquer IA (Claude, Codex, Antigravity)**: escreva o prompt em `<pasta>/publicacao/thumbnail_base_prompt.txt` e rode `.\automacao\gerar_arte_thumbnail.ps1 --prompt-file <pasta>\publicacao\thumbnail_base_prompt.txt --formato longo|short --saida <pasta>\publicacao\thumbnail_base_gerada.png` (Gemini `gemini-3-pro-image`; `--modelo gemini-3.1-flash-image` é mais barato; `--referencia <img>` para condicionar em quadros do acervo; `--dry-run` para conferir sem custo). O script acrescenta as regras fixas de arte e salva o prompt usado em `<saida>.prompt.txt`. Cada imagem é cobrada: gere uma por peça e só refaça se a leitura em miniatura falhar.
  - Alternativas apenas se o script falhar: `image-generator` no Antigravity ou `imagegen` no Codex, com o mesmo prompt.
- Aplique texto, marca do canal e logo oficial numa segunda etapa determinística. Use `py -3.12 .agents/skills/pixel-procurado-thumbnails/scripts/compose_thumbnail.py` quando o layout padrão atender ao pedido.
- Use a logo GTA VI de `assets/gta-vi-logo.png` somente quando o conteúdo for realmente sobre GTA VI. Para GTA V, identifique GTA V; não use GTA VI só para aumentar o clique.
- Confirme que o painel de texto deixa toda a logo visível, especialmente na vertical. Teste a leitura em miniatura antes de anexar a capa.
- Prefira uma frase de 2 a 7 palavras, em no máximo duas linhas. Ela deve complementar o título, não repeti-lo.
- Mostre uma ideia dominante: rosto/objeto/cena principal, frase e identificação. Remova qualquer elemento que dispute atenção sem reforçar a promessa.
- Para um lote, varie cenas e conflitos, mas mantenha grade, tipografia, cores e assinatura consistentes.

## Entrega

Salve na pasta do vídeo:

- `capa_master.png`: master sem perdas no formato correto.
- `capa_youtube.jpg`: arquivo otimizado para envio, abaixo de 2 MB.
- `thumbnail_base_gerada.png`: arte-base sem texto e sem logo.
- `PROMPT_THUMBNAIL.txt`: prompt, frase, direção e indicação de que é montagem editorial.
- `capa_anterior.*`: backup da capa substituída, quando existir.

Em lotes, gere também uma prancha de contato para comparação. Inspecione-a em tamanho reduzido e corrija texto cortado, logo deformada, rostos cobertos, contraste fraco e capas excessivamente parecidas.

Não prometa desempenho ou viralização. Descreva a capa como orientada a clareza, curiosidade e potencial de clique.
