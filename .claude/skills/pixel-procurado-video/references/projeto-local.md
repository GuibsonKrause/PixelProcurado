# Referência local: padrão aprovado

Raiz original: C:/Users/guibson.krause/Documents/ChatGPT/GamePlay
Este caminho é referência de descoberta, não destino obrigatório. Não reusar fatos, datas ou arquivos antigos sem verificar o episódio atual.

## Arquivos úteis

### L02 — referência preferencial para animações e direção contextual
- producao/L02/projeto/EDICAO_L02.md — decisões e verificação da segunda edição aprovada.
- producao/L02/projeto/edicao_l02.json — timeline com âncoras de fala, fontes, cortes, legendas e entradas dos gráficos.
- producao/L02/voz/palavras_alinhadas.json e producao/L02/projeto/revisao_asr.json — alinhamento e diferenças entre reconhecimento e roteiro; revisar divergências contra o áudio, não copiar correções automaticamente.
- remotion/src/l02-overlays.tsx — gráficos animados, listas progressivas, comparações e contornos de destaque; posição dos textos ajustada às cenas.
- remotion/render-l02-overlays.mjs — sequências transparentes com renderFrames; renderStill apenas para camadas fixas.
- automacao/preparar_l02.py — escolhas editoriais específicas de L02 e cortes ancorados em frases.
- automacao/renderizar_l02.py — composição de sequências, câmera, legendas, assinatura de cache e junção.
- automacao/verificar_l02.py — amostragem visual, decodificação integral e comparação de áudio.
- producao/L02/projeto/render4k/qa/validacao_final.json — resultado técnico verificado.

L02 teve 309,76 s de narração, 76 planos, 136 legendas e 26 planos animados; esses números não são metas para os próximos episódios. A melhora reutilizável é o vínculo entre fala, imagem e gráfico. Hipóteses receberam gráficos próprios; a análise de uma fotografia manteve a fonte na tela com destaques sequenciais.

### L01 e acervo compartilhado
- producao/L01/projeto/EDICAO_FINAL_4K.md — decisões e configuração da edição aprovada.
- producao/L01/projeto/edicao_final_4k.json — exemplo de timeline (88 planos e 201 blocos de legenda; contagens específicas de L01).
- producao/L01/voz/gemini/narracao_guibson2_normalizada.wav — narração usada em L01, não áudio padrão de novos episódios.
- producao/L01/voz/gemini/narracao_guibson2_palavras.json — exemplo de alinhamento por palavra.
- videosGTAVI/_catalogo/inventario_midia.json — caminhos e metadados do acervo.
- videosGTAVI/_catalogo/INDICE_VIDEOS.md e GUIA_IMAGENS.md — índices editoriais a conferir visualmente ao selecionar planos.
- remotion/src/Edicao.tsx — exemplo de composição integral.
- remotion/src/overlay-index.tsx e remotion/render-overlays.mjs — exportação de gráficos transparentes em resolução nativa.
- automacao/preparar_edicao_final.py — preparação específica de L01; seleção e textos estão codificados no arquivo.
- automacao/renderizar_final_4k.py — composição por planos e junção.
- automacao/verificar_final_4k.py — amostragem visual e comparação técnica de áudio.
- assets/identidade/ — artes existentes do canal.

## Adaptação
Inspecionar os scripts antes de executar. Eles usam caminhos e textos de seus episódios; copiá-los sem adaptação pode sobrescrever entregas ou usar a narração errada. Criar uma pasta de episódio/versionamento e tornar as entradas necessárias explícitas, sem construir uma plataforma genérica desnecessária. Os scripts L02 são exemplos locais, não um editor genérico pronto para qualquer narração.

A normalização original de L01 mediu −16,01 LUFS e −1,50 dBTP. Isso é histórico, não uma medição de qualquer arquivo novo.

## Ambiente observado
Windows/PowerShell; Node.js; Remotion local; FFmpeg empacotado em .production-tools/python/imageio_ffmpeg/binaries. Havia Python 3.12 e 3.14, mas o Pillow em .course-tools era compatível com 3.12. Verificar compatibilidade dos binários antes de alterar instalações.

Intel Quick Sync H.264 funcionou no i7-1355U/Iris Xe. Detectar e testar novamente no computador atual; usar codificação por CPU se necessário.

Não copiar bancos inteiros de dezenas de GB para cada bundle Remotion quando só gráficos precisam ser renderizados. O exportador de overlays usa publicDir vazio. Para vídeos, preparar apenas a mídia necessária ou uma estratégia de acesso local compatível.
