# QA da thumbnail L03

Revisão: 28/10/2026. Capa real concluída; vídeo ainda em produção. A conferência de aderência ao MP4 final poderá complementar esta revisão.

## Conteúdo e direção

Frase principal: **A MESMA / SENSAÇÃO?** Complemento: **VICE CITY: CLÁSSICA × NOVA**. O conjunto acompanha a comparação de memória, atmosfera e cultura do celular de `01_NARRACAO.txt`, lido integralmente com `02_DIRECAO_E_FONTES.md`.

A base é uma ilustração/montagem editorial gerada, explicitamente identificada na própria capa. As duas figuras no telefone são anônimas: não constituem retrato de Real Dimez, nova imagem oficial, gameplay ou prova de mecânica. Carro antigo, palmeiras e neon evocam nostalgia; o telefone concentra o espetáculo contemporâneo. Não há afirmação de retorno de Tommy nem comparação do mesmo endereço.

## Produção e resolução

- Uma única chamada à ferramenta integrada `image_gen.imagegen`; sem API/CLI alternativa ou segunda geração.
- Arquivo nativo: **1672 × 941**, RGB, preservado sem texto/logo em `thumbnail_base_gerada.png`.
- Origem: `C:/Users/guibson.krause/.codex/generated_images/01a184df-6e20-74e1-86b5-96bcfbeae280/exec-3f408435-aceb-43fd-ab8e-e1bb7769346e.png`.
- Master: **1920 × 1080**, PNG RGB, 16:9 exato. A base foi ajustada proporcionalmente com recorte mínimo e ampliada para o canvas; a arte não possui detalhe nativo 1920 nem 4K. Texto e logo foram compostos diretamente no canvas de 1920.
- Upload: **1280 × 720**, JPEG RGB, 16:9 exato, **433.785 bytes**, progressivo, qualidade 94 e subamostragem 0; abaixo de 2 MB.
- Composição determinística: `compose_thumbnail_l03.py`, Python 3.12 com Pillow local de `.course-tools`; fontes Impact e Bahnschrift.
- Logo oficial GTA VI: asset aprovado `C:/Users/guibson.krause/.codex/skills/pixel-procurado-thumbnails/assets/gta-vi-logo.png`, nativo 2060 × 1395. Removido apenas preto externo conectado à borda, recortadas margens externas e preservada a proporção do conteúdo (241 × 180 na composição). Nenhum desenho de letras/logotipo foi gerado por IA.
- Nenhuma capa anterior L03 existia para preservar. Não houve upload.

## Inspeção visual realizada

Inspecionados: referência aprovada L01, imagem clássica V2, imagem oficial Real Dimez 02, logo da skill, arte gerada, master em 100%, redução de 25% (**480 × 270**) e miniatura de celular (**320 × 180**).

- Frase principal legível nas duas reduções; til, cedilha e interrogação corretos.
- Celular e duas figuras continuam reconhecíveis a 320 × 180. O telefone tem silhueta íntegra e permanece dominante.
- Nenhum texto principal cortado; caixas medidas permanecem dentro do canvas. Olhos/rostos das figuras não são cobertos pela tipografia ou logo.
- Branco/amarelo contrastam com a região grafite; o texto não depende de pequeno detalhe do fundo.
- Logo sem deformação; esquina inferior direita reservada para interface/duração, contendo somente parte da mão/fundo.
- Selo e nota editorial são auxiliares e naturalmente pequenos em tamanho de celular. A promessa principal não depende deles.
- O rótulo comparativo torna explícitos clássico e novo; o texto principal não repete o título do roteiro.

## Regras atuais do YouTube

Fonte oficial consultada em 28/10/2026: [Adicionar miniaturas personalizadas](https://support.google.com/youtube/answer/72431?hl=pt-BR).

A página atualmente recomenda 3840 × 2160 para vídeos, largura mínima de 640 pixels, JPG/PNG e 16:9; limita uploads a 2 MB em dispositivos móveis e 50 MB em computador. Os arquivos solicitados de 1920 × 1080 e 1280 × 720 respeitam o mínimo e a proporção. A exportação JPEG atende também ao limite móvel. Não foi criada uma ampliação 4K apenas para corresponder à recomendação.

## Arquivos finais

- `capa_master.png`
- `capa_youtube.jpg`
- `thumbnail_base_gerada.png`
- `PROMPT_THUMBNAIL.txt`
- `compose_thumbnail_l03.py`
- `QA_THUMBNAIL.md`

Os demais arquivos de produção e publicação não foram alterados nesta tarefa.
