# Edição final — Pixel Procurado / Dossiê 01

## Entrega

Arquivo: `../exportacoes/Pixel_Procurado_L01_4K.mp4`

- 3840 × 2160, 16:9, 30 fps, H.264.
- Narração Gemini integral: 427,04 segundos. Nenhuma fala removida ou reordenada.
- Fonte de áudio: `../voz/gemini/narracao_guibson2_normalizada.wav`.
- Áudio de origem medido em −16,01 LUFS, pico verdadeiro −1,50 dBTP, faixa dinâmica de loudness 3,90 LU.
- Áudio original dos vídeos de apoio silenciado; narração é a trilha principal.
- 88 planos escolhidos pelo assunto da narração.
- 201 grupos curtos de legenda sincronizados às marcações por palavra; nomes próprios corrigidos na transcrição.
- Palavras-chave em amarelo sobre legendas brancas com fundo escuro.

## Direção

Abertura com planos de aproximadamente 3 segundos; explicações com planos de 4 a 7 segundos; sequência de destinos acompanha a enumeração dos nomes. Cartelas diferenciam anúncio, interpretação, hipótese e exemplo de raciocínio.

Screenshots recebem zoom lento de aproximadamente 3,5%, panorâmica discreta e tratamento tonal leve. Gráficos têm entrada vertical curta e legendas têm fades discretos. O objetivo é conduzir a leitura sem simular movimentos tridimensionais artificiais em fotografias sem camadas de profundidade.

Identidade: grafite, branco e amarelo, tipografia Arial em peso alto, margem segura, rótulo editorial superior esquerdo e assinatura Pixel Procurado superior direita.

## Arquivos editáveis

- `edicao_final_4k.json`: planos, fontes, pontos de entrada, textos e tempos das legendas.
- `../../../remotion/src/Edicao.tsx`: composição integral editável no Remotion.
- `../../../remotion/src/overlay-index.tsx`: gráficos em 4K usados na exportação.
- `../../../automacao/preparar_edicao_final.py`: preparação da montagem e das legendas.
- `../../../remotion/render-overlays.mjs`: exportação dos gráficos Remotion com transparência.
- `../../../automacao/renderizar_final_4k.py`: composição em 4K, movimentos, legendas e codificação Intel Quick Sync.

## Reprodução da exportação

A partir da raiz do projeto, executar `python automacao/preparar_edicao_final.py`. Na pasta `remotion`, executar `node render-overlays.mjs`. De volta à raiz, executar `python automacao/renderizar_final_4k.py`.

A pasta `render4k` armazena os planos já renderizados, logs e o relatório técnico. A automação reaproveita os planos cuja duração confere; ao alterar a edição de um plano, remova somente o MP4 numerado correspondente antes de renderizar novamente.

## Escopo da revisão

Esta é uma edição do áudio fornecido, não uma nova apuração jornalística. As afirmações e a data de checagem narradas foram preservadas. A composição usa os arquivos locais disponibilizados pelo usuário. O relatório `render4k/validacao.json` registra os parâmetros do arquivo exportado.
