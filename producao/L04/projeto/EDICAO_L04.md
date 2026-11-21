# Edição L04

Roteiro preservado: 25 parágrafos atuais de `01_NARRACAO.txt`; versão expressiva original em `03_NARRACAO_GEMINI.txt`. Quatro blocos foram gerados pelo atalho local Gemini, com gemini-3.8-flash-tts e voice_iagtq1gnk2br. Brutos preservados em `../voz/gemini/bruto_v1/`. Não houve reutilização de locução antiga.

Áudio integral 260,36 s, PCM16 mono 24kHz bruto; cópia normalizada mono 48kHz. Medição da cópia: −16,81 LUFS, −1,49 dBTP, zero amostras clipadas. ASR integral small/int8/beam1 e segunda conferência base/int8 em quatro divergências. Nenhuma omissão extensa ou tag falada detectada. A inspeção automatizada não comprova pronúncia perfeita nem equivale a escuta integral.

A comparação de dois ASRs aponta “Vamos ao Trailer dois” em torno de 36s; as legendas usam essa contração, preservando roteiro e alinhamento de referência para auditoria. Conferir no áudio 146–149s (“dado ao PlayStation”) e 172–178s (“cor escolhida”, “pôster”), que têm divergências fonéticas no ASR. A segunda conferência recuperou a pergunta final completa em 248–253s.

Timeline editável: `edicao_l04.json`; 44 planos, 109 blocos de legenda. Imagens oficiais 4K examinadas e Trailer 2 nativo 3840×2160/30fps. São 16 planos em movimento do Trailer 2 e oito planos de observação de artwork/screenshot. As analogias, hipóteses e distinções técnicas usam gráficos próprios identificados, sem inventar filmagens de evidência.

Direção: resposta imediata na abertura; câmera atrás do personagem tratada como pista, sem classificação individual de gameplay. O exemplo de entrar no carro é gráfico e tem rótulo de hipótese. Captura PS5 e plataformas PS5/Xbox são perguntas diferentes. Artwork do casal no carro e screenshot do casal diante da cidade são exatamente os dois arquivos descritos; cada categoria permanece identificada na tela.

Remotion gera gráficos transparentes em resolução 3840×2160 e animações por quadro. As listas entram nas palavras alinhadas; o exportador específico rasteriza todos os frames em movimento e usa hardlinks de frames idênticos nos intervalos imóveis. FFmpeg compõe mídia, câmera 2D suave nas imagens e legendas ASS em cada plano. Não foi criado parallax 3D. QSV H.264 nos segmentos; narração inteira muxada uma única vez em AAC/48kHz; áudio dos trechos oficiais silenciado. Durações explícitas no concat impedem acúmulo de desvio.

Caches incluem assinatura da timeline por plano, arquivos de origem, código de composição e legendas. PNGs derivados dos overlays só são removidos após contagem de frames do segmento validada; brutos, mídia original e versões editoriais anteriores são preservados.

O pacote final exige `render4k/qa/validacao_final.json` com decodificação integral, metadados, correlação do áudio em vários pontos e loudness após AAC. A revisão visual é por amostragem de entradas, estados finais e imagens; não é chamada de revisão integral. Revisão independente editorial será feita pelo coordenador.

Comandos de reprodução, a partir da raiz: `py -3.12 automacao/preparar_l04.py`; `node remotion/render-l04-overlays.mjs <índices>`; `py -3.12 automacao/renderizar_l04.py`; `py -3.12 automacao/verificar_l04.py --validate-only`. Não regenerar áudio faturável sem necessidade.

Não houve upload nem agendamento por este executor. A autorização de programação pública 01/11/2026 às 12h Brasília será executada pelo coordenador após revisão independente.


## Fechamento verificado — correção P03, 01/11/2026

P03 (17,833–24,767s) usa o trecho oficial do píer/água, fonte 82–85,4s retimada a 0,5× e identificada na tela. Frames reais do candidato em 20/21/22/23s confirmam luz e reflexos durante a fala; a cauda de oficina após a frase é uma transição da própria fonte aceita pela revisão independente. Não houve nova geração de áudio, imagem ou render integral nesta retomada. A revisão foi pontual; as demais cenas e todos os pacotes AAC foram comparados pelo revisor e permanecem idênticos ao render anterior.

Candidato integralmente decodificado sem erros e estável durante QA; promoção feita após PASS editorial independente, preservando o MP4 anterior em `../exportacoes/Pixel_Procurado_L04_4K_antes_correcao_P03.mp4`. Final: 277.055.211 bytes, SHA-256 `a2f40e2ece43fb1fe7679d959b9746f1e3709d24b5bcfa9a3dc158af4fe9fcef`. A cópia promovida tem hash idêntico ao candidato validado; não se repetiu a decodificação desses mesmos bytes.

QA final: H.264, 3840×2160, 30fps, 7811 frames; vídeo 260,366667s, áudio AAC 48kHz 260,36s. 44 planos contíguos e 109 legendas com limites válidos. SRT final e candidato são idênticos. Correlação com a narração normalizada em sete pontos: mínimo 0,999961. AAC medido em −16,82 LUFS, −1,24 dBTP e LRA 3,10; o true peak excede em 0,26dB o alvo inicial de −1,5dBTP, sem indicação de clipping. O filtro loudnorm foi usado para medir, não para reaplicar processamento.

Evidências: `render4k/qa/validacao_final.json`, `render4k/qa/promocao_P03.json`, `render4k/qa_revisao_P03/assinatura_candidato.json` e frames `render4k/qa_revisao_P03/P03_*.jpg`. A QA anterior foi preservada em `render4k/qa/validacao_antes_correcao_P03.json`. Limites de escuta/ASR continuam registrados acima. Não houve upload nem agendamento por este executor.
