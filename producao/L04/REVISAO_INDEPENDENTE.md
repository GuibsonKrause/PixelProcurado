# Revisão independente — L04

**Resultado atual: PASS editorial — correção pontual P03 revalidada em 01/11/2026.** Candidato aprovado para promoção após conclusão da QA técnica integral pelo executor. Este parecer não executa envio/agendamento. Revisão iniciada em 01/11/2026, com quatro skills Pixel Procurado e referências de vídeo, thumbnail e publicação lidas. Revisor independente da montagem; edição restrita a este relatório.

## Artefato examinado e escopo

MP4 examinado diretamente após sinal de arquivo fechado: `exportacoes/Pixel_Procurado_L04_4K.mp4`.

SHA-256 da primeira versão examinada: `3603A5CAA6130A50E5A3659980A40805EB36C10DB3DC7F83347F1CA03AA21597`.
SRT: `C6D56360F773E6A7050A1DB9C242DA575BE25F1D0867992B660B58225691086C`.

Inspeção visual **por amostragem**, não reprodução/escuta integral. Quadros decodificados diretamente do MP4 em memória, sem modificar mídias ou criar provas derivadas em disco. Um quadro intermediário de cada um dos 44 planos, abertura, progressão de listas e encerramento; também folhas de contato existentes e amostra 4K fechada. A amostra não substituiu a inspeção do arquivo final.

## Correção obrigatória identificada

P03, 17,833–24,767s: o plano começa com água/cais em 18–19s, mas corta para oficina às 20s. Durante a legenda “GTA mostra uma luz bonita na água e”, em 21,000s/f630, 21,300s/f639 e 22,000s/f660, aparecem escada/oficina e rua. O rótulo superior continua “EMPOLGAÇÃO / LUZ NA ÁGUA”. Manter água visível durante essa frase (~20,34–23,62s), preservando voz, duração e demais planos. Falha histórica da primeira versão; resolvida no candidato identificado na revalidação abaixo.

Os demais 43 planos amostrados não apresentaram erro visual bloqueante. Não há solicitação de reedição estrutural.

## Evidência visual registrada

Frames numerados a partir de zero. Tempos representam o quadro decodificado, arredondado a milissegundos.

| Plano | Segundo | Frame |
|---:|---:|---:|
| 00 | 2,933 | 88 |
| 01 | 8,567 | 257 |
| 02 | 14,533 | 436 |
| 03 | 21,300 | 639 |
| 04 | 30,233 | 907 |
| 05 | 38,367 | 1151 |
| 06 | 42,467 | 1274 |
| 07 | 45,633 | 1369 |
| 08 | 49,333 | 1480 |
| 09 | 54,000 | 1620 |
| 10 | 59,967 | 1799 |
| 11 | 66,067 | 1982 |
| 12 | 71,467 | 2144 |
| 13 | 77,467 | 2324 |
| 14 | 84,833 | 2545 |
| 15 | 93,433 | 2803 |
| 16 | 99,833 | 2995 |
| 17 | 103,333 | 3100 |
| 18 | 109,033 | 3271 |
| 19 | 116,133 | 3484 |
| 20 | 123,533 | 3706 |
| 21 | 131,933 | 3958 |
| 22 | 138,867 | 4166 |
| 23 | 143,900 | 4317 |
| 24 | 150,767 | 4523 |
| 25 | 157,867 | 4736 |
| 26 | 163,833 | 4915 |
| 27 | 169,700 | 5091 |
| 28 | 174,300 | 5229 |
| 29 | 178,067 | 5342 |
| 30 | 183,233 | 5497 |
| 31 | 188,767 | 5663 |
| 32 | 193,567 | 5807 |
| 33 | 198,033 | 5941 |
| 34 | 203,333 | 6100 |
| 35 | 208,800 | 6264 |
| 36 | 213,033 | 6391 |
| 37 | 217,467 | 6524 |
| 38 | 222,100 | 6663 |
| 39 | 227,833 | 6835 |
| 40 | 239,833 | 7195 |
| 41 | 251,533 | 7546 |
| 42 | 255,933 | 7678 |
| 43 | 258,967 | 7769 |

Verificações adicionais no MP4: 0s/f0 e 3s/f90 (abertura); 25/29/31/33s, f750/870/930/990 (lista P04); 128/132s, f3840/3960 (lista P21); 231,6/237/242,2/248,5s, f6948/7110/7266/7455 (lista P40); 257,6/259,5/260,333s, f7728/7785/7810 (fim). Amostra estável também examinada em 0/0,3/1/2,1/2,9/3,2/5/6,2/10,9s. O gancho/pergunta termina por volta de 2,12s; a resposta factual vem na frase seguinte (~3–5s), não aos 2,12s.

As listas revelam os itens progressivamente e mantêm espaço para legendas. Tipos headline/list cobertos. Hipóteses do carro identificadas como exemplo, sem atribuição de mecânica a uma cena oficial. Artwork (167,233–179,667s e 196,367–199,700s) e screenshot (179,667–196,367s e 210,667–215,367s) exibem as peças exatas descritas, categorias permanentes, rostos preservados e movimento 2D moderado. Não há alegação de parallax.

Os vídeos usados são do Trailer 2; a timeline identifica arquivo e entrada, e a folha de entradas da fonte foi inspecionada. O final passa pela transição da cidade para logo VI; último quadro não exibe data de lançamento nem informação conflitante. Não foi identificado quadro preto inesperado como falha; há fade da própria fonte.

## Temporal, legenda e áudio

Conferência independente da timeline: 44 planos contíguos, 7811 frames, 109 legendas, nenhuma sobreposição ou duração inválida; menor exposição 0,85s. Legendas preservam acentos e nomes próprios visualmente nas amostras; não cobrem os rostos examinados. Algumas atravessam cortes de planos sem deslocamento indevido.

QA técnica da primeira versão, lida em `projeto/render4k/qa/validacao_final.json`: 3840×2160, 30fps, H.264/AAC 48kHz; vídeo 260,366667s, áudio 260,36s; 282892300 bytes. Decodificação integral sem erros realizada pelo executor. Correlação com `voz/narracao_normalizada.wav` em 1/26/65/130/195/234/256s, mínimo 0,999961. Loudness AAC: −16,82 LUFS, true peak −1,24 dBTP, LRA 3,10. O pico AAC ultrapassa em 0,26dB o alvo inicial de −1,5dBTP, sem indicação de clipping; registrar a medição real, sem alegar −1,5dBTP no exportado.

ASR e alinhamento foram lidos. Não houve escuta subjetiva integral, nem se afirma pronúncia perfeita. Permanecem as ambiguidades documentadas em ~36s (“Vamos usar o”/“Vamos ao”), ~146–149s (“dado ao PlayStation”) e ~173–178s (“cor escolhida”, “pôster”). As duas transcrições não indicam omissão extensa; a segunda recupera a pergunta final. Essas incertezas pequenas, já registradas, não são tratadas como erro material comprovado.

## Publicação, capa e fontes

Título “GTA 6: tem gameplay no Trailer 2? Três dúvidas resolvidas” corresponde ao conteúdo. Capa “TEM GAMEPLAY?” examinada em 1280×720 e 320×180: leitura imediata, contraste, rostos e logo íntegros, 223010 bytes. A imagem é montagem editorial gerada, explicitada no prompt e descrição, sem promessa de captura inédita. Não foi solicitada variante.

Descrição, comentário e tags são pertinentes, sem promessa inventada. Capítulos 00:00, 00:41, 01:52, 02:40, 03:30, 03:50 seguem a locução, começam em zero, são crescentes e todos superam 10s. O guia deve trocar “duração planejada” por duração validada após a QA da versão corrigida. O guia distingue público infantil/restrição, explica duplicação possível das legendas e não afirma clonagem da própria voz. A declaração de uso de IA recomendada é compatível com a transparência adotada.

Revalidação independente online: [plataformas oficiais](https://www.rockstargames.com/VI) lista PS5 e Xbox Series X|S; [biblioteca oficial](https://www.rockstargames.com/VI/media) separa Screenshots de Artwork & Wallpapers. A [VGC, 07/05/2025](https://www.videogameschronicle.com/news/rockstar-reiterates-that-the-latest-gta-6-trailer-was-captured-on-ps5/) reproduz o comunicado histórico sobre captura em PS5 e partes iguais de gameplay/cutscenes. Não se afirma novo acesso direto à postagem X; o limite está explicitado no pacote.

[Capítulos](https://support.google.com/youtube/answer/9884579?hl=pt-BR), [thumbnail](https://support.google.com/youtube/answer/72431?hl=pt-BR) e [transparência de IA](https://support.google.com/youtube/answer/14328491?hl=pt-BR) conferidos na revisão. A recomendação atual de thumbnail 3840×2160 não torna inválida a capa 1280×720, acima do mínimo de 640px e dentro dos limites de arquivo.

## Melhorias opcionais e limites

A frequência de cartelas textuais poderia variar mais em episódios futuros; aqui as cartelas são legíveis, contextualizadas e não exigem remontagem. Não foi feita avaliação de desempenho de clique, retenção ou processamento YouTube. Não houve upload, agendamento, publicação, comentário ou alteração de conta por este revisor. O novo hash e a revalidação de P03 constam abaixo.


## Revalidação pontual final — 01/11/2026

**PASS editorial.** Candidato examinado diretamente: `producao/L04/exportacoes/Pixel_Procurado_L04_4K_revisao_P03.mp4`. Tamanho e data de modificação permaneceram estáveis antes/depois da inspeção: 277055211 bytes. SHA-256 independente: `a2f40e2ece43fb1fe7679d959b9746f1e3709d24b5bcfa9a3dc158af4fe9fcef`.

Frames decodificados do candidato e inspecionados em memória: 18/19/20/21/22/23/24s (f540/570/600/630/660/690/720); transições e limites em 17,800/17,833/20,333/23,633/24,733/24,767s (aproximadamente f534/535/610/709/742/743). Água e reflexos estão visíveis durante a frase crítica (~20,34–23,62s); o cais próximo dá lugar ao plano aberto do pôr do sol sobre a água. A legenda permanece legível e o crédito informa velocidade 0,5× de edição. A oficina reaparece somente na cauda após a frase, sem legenda no quadro 24,733s, antes da cartela de três checagens em 24,767s. Esse curto corte de transição não repete a falha narrativa que bloqueava P03 e não exige correção adicional.

Metadados independentes do candidato: 3840×2160, H.264, 30fps, 7811 frames, vídeo 260,366667s; AAC 48kHz, áudio 260,36s. Valores idênticos aos da primeira versão. Comparação de todos os pacotes comprimidos entre a primeira versão e o candidato: mesmas chaves de stream/PTS; nenhum pacote AAC alterado; somente 208 pacotes de vídeo alterados, todos dentro de P03 (PTS 17,833333–24,733333s). Todos os pacotes de vídeo fora desse intervalo são idênticos por SHA-256. Isso confirma preservação da narração, duração, timestamps e mídia restante, permitindo aproveitar a revisão anterior dos demais 43 planos.

A revalidação visual continua sendo **amostragem**, sem alegação de escuta subjetiva integral. Permanecem os limites de ASR, fontes e medições já registrados. A decodificação integral do candidato e a promoção do arquivo cabem ao executor técnico, que recebeu o sinal de PASS editorial; nenhuma publicação, agendamento ou alteração de conta foi realizada por este revisor.
