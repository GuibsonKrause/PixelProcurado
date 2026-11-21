# L03 — Inventário de entradas

Descoberta executada em 28/10/2026. Raiz: `C:/Users/guibson.krause/Documents/ChatGPT/GamePlay`. Formato definido: longo, 3840×2160, 16:9, 30 fps. Somente descoberta e download de fontes oficiais; nenhuma voz/imagem paga gerada. Checkpoint pertence ao coordenador.

## Roteiro e direção

- `producao/L03/01_NARRACAO.txt`: 19 parágrafos, 894 palavras, preservado.
- `producao/L03/02_DIRECAO_E_FONTES.md`: direção contextual e fontes S1–S5; preservar a distinção lançamento 2002 / história 1986. Tempo final depende da voz validada.

## Mídia clássica incorporada

| ID | Arquivo | Dimensões / bytes | Inspeção visual |
|---|---|---|---|
| V1 | `producao/L03/midia/V1_Vice_City_Classico_Screens_1.jpg` | 640×448 / 84854 | Carro vermelho em avenida, palmeiras à esquerda, lojas e prédio à direita; logo no canto inferior direito. Confirma descrição P4. |
| V2 | `producao/L03/midia/V2_Vice_City_Classico_Screens_2.jpg` | 640×448 / 89202 | Tommy com camisa azul estampada e arma, palmeiras e prédio; logo no canto superior esquerdo. Confirma descrição P6. |

Ambas foram baixadas diretamente dos URLs identificados na direção e abertas individualmente com `view_image`. Integridade JPEG validada com Pillow. São fontes de baixa resolução, proporção 10:7: preservar o quadro em composição editorial 4K com fundo/painel e movimento moderado; não prometer detalhe nativo 4K. Rotular “imagem promocional do clássico”, sem atribuir plataforma. Crédito: Rockstar Games, Grand Theft Auto: Vice City.

- Página de origem: https://www.rockstargames.com/games/vicecity
- V1: https://media-rockstargames-com.akamaized.net/mfe-r19/prod/__common/img/7c3466bd07d09ec14c9555505ea4e6af.jpg
- V2: https://media-rockstargames-com.akamaized.net/mfe-r19/prod/__common/img/b0353d1406b5264dc18326a811bc5bb5.jpg
- SHA256 V1: `091f4a5f281c057979bcc79eddb16b95f02a2c532939faf5536835ae37bf404e`
- SHA256 V2: `0499d24aaadc0004ab2bf9f3e229c5c7e82610929e2c20e3e196001e0234c4de`

## Acervo VI necessário

Todas as quatro entradas abaixo existem e passaram por abertura/verificação JPEG; são 3840×2160. A inspeção editorial anterior está registrada na direção. Esta descoberta não substitui a inspeção visual detalhada e coordenadas dos destaques na etapa de montagem.

- `videosGTAVI/GTAVI_Screenshots/People/Real Dimez/Real_Dimez_02.jpg` — 632862 bytes; abertura/P9, telefones e plateia.
- `videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_02.jpg` — 528149 bytes; varanda/piscina/praia.
- `videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_05.jpg` — 561227 bytes; praia e atividades.
- `videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_06.jpg` — 649067 bytes; hotéis/palmeiras/rua; não tratar como o endereço de V1.

Catálogo existente: `videosGTAVI/_catalogo/inventario_midia.json`, `GUIA_IMAGENS.md`, `GUIA_EDITORIAL.md`, `INDICE_VIDEOS.md`, `folhas_imagens/`, `folhas_videos/`, `indices_detalhados/`, `GALERIA.html`. Usar índices existentes antes de varrer todo o banco. Não copiar todo o banco ao bundle Remotion.

## Ferramentas confirmadas

- Python audiovisual: `C:/Users/guibson.krause/AppData/Local/Programs/Python/Python312/python.exe`, versão 3.12.10. Imports testados com `sys.path[:0]=['.course-tools','.production-tools/python']`: Pillow 12.3.0, PyAV 19.0.1, numpy 2.5.3, imageio_ffmpeg.
- FFmpeg: `.production-tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe`. Usar caminho absoluto ou `imageio_ffmpeg.get_ffmpeg_exe()` após preparar sys.path; não depender de PATH.
- Node: `C:/Program Files/nodejs/node.exe`, versão v24.13.0.
- Remotion instalado em `remotion/node_modules`; package.json fixa Remotion e @remotion/cli 4.0.538, React 19.3.1. Verificada presença, sem disparar render nesta etapa.
- ASR local: `.course-tools/models/models--Systran--faster-whisper-small` e `...base` existem; o exemplo `automacao/shorts_asr.py` usa small CPU/int8, 4 threads, português e word_timestamps. Adaptar para L03; não executar o batch de Shorts.
- Voz: usar exclusivamente o fluxo `automacao/gerar_narracao_gemini.ps1` / `.venv-gemini` pela etapa responsável. Não usar Python audiovisual para contornar esse fluxo.

## Reuso permitido mediante adaptação

- `automacao/preparar_l02.py`: âncoras de fala e timeline; `automacao/renderizar_l02.py`: composição por plano e assinatura de cache; `automacao/verificar_l02.py`: decodificação, amostras e comparação de áudio. São específicos de L02: não executar sem trocar caminhos/textos/entradas para L03.
- `remotion/src/l02-overlays.tsx` e `remotion/render-l02-overlays.mjs`: animação transparente com renderFrames, 3840×2160/30 fps, publicDir vazio, cache por assinatura. Adaptar nomes e caminhos L03. O exportador aceita índices de planos como argumento separado por vírgulas.
- `producao/L02/projeto/edicao_l02.json` e `EDICAO_L02.md`: contrato e referência editorial; contagens não são metas.
- `automacao/renderizar_final_4k.py`, `verificar_final_4k.py`, `preparar_edicao_final.py`: alternativa histórica L01, também específica do episódio.
- `assets/identidade/pixel-procurado-marca-dagua-v1.png`, avatar e banner existentes. Identidade grafite/branco/amarelo #FFD33D.

## Limites e passagem de etapa

Nenhum bloqueio para descoberta. Baixa resolução de V1/V2 é uma limitação real de fonte e deve orientar o layout. Áudio validado, alinhamento e timeline ainda dependem dos respectivos executores; não inferir duração pelo texto. QSV deve ser testado no renderizador antes de adotá-lo. Não declarar Remotion/render/QSV/ASR operacional só pela presença de dependências. Entregar MP4/SRT/timeline após amostra e QA; nenhuma publicação foi feita.

Medições adicionais: catálogo com 309 entradas (14 vídeos, 295 imagens). FFmpeg respondeu versão 7.1 essentials. Disco C: com 26.103.140.352 bytes livres (~24,3 GiB) no momento da descoberta; planejar overlays transparentes/cache com atenção ao espaço.
