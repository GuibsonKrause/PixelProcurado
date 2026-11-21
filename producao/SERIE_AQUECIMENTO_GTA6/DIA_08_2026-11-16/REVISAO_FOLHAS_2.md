# Segunda revisão independente — Dia 08 (16/11/2026), só trechos alterados

Revisor: subagente Opus 5.5. Não alterei nenhum arquivo do episódio. Só criei este relatório. Os quadros extraídos ficaram fora da pasta, no diretório temporário do revisor.

Material visto:
- Cartelas `montagem/referencias/C06_PSSR.jpg` e `C14_XBOX.jpg`.
- Amostras `_previa/amostra_0-25`, `amostra_282-300` e `amostra_385-404`, com 1 quadro a cada 2 s. As amostras começam no início do primeiro plano, não no segundo exato da janela: 0–34,9 s, 268,83–302,5 s e 383,54–404,09 s.
- Folhas regeneradas `montagem/prevoo/*_01`, `_02`, `_03` e `_06`, além das folhas do Reel e do Story.
- Fonte `videosGTAVI/GTAVI_An_Extended_Look.mp4` entre 1218 e 1225,2 s (1 quadro por segundo e `blackdetect`).
- Stills `EXT_1203_4k`, `EXT_763_4k`, `EXT_1210_4k` e `EXT_1213_4k`.
- `episodio.json` (longo, Reel e Story), `audio/palavras_alinhadas.json`, `_reel/audio/palavras.json`, `_story/audio/palavras.json` e o nível de áudio de `_reel/audio/narracao.wav` entre 60,8 e 62,86 s.

## Veredito

**Longo: aprovado** nos itens 1 a 5. Há só observações menores e opcionais.
**Reel: 1 correção obrigatória.** A voz é cortada no meio da frase seguinte, "No mesmo…".
**Story: aprovado.**

## Itens pedidos

| # | Trecho | Resultado | Evidência |
|---|---|---|---|
| 1a | `C06_PSSR` | **ok** | O texto agora diz "pixel por pixel / aumenta a resolução com IA / (descrição da Sony)", fiel ao F5. A linha mais longa termina em cerca de 92% da largura, dentro da área segura. |
| 1b | `C14_XBOX` | **ok** | A citação agora é "MOST AFFORDABLE WAY TO PLAY GTA VI NATIVELY" e termina em cerca de 93% da largura. |
| 2 | Abertura 0–21,7 s | **ok** | `C01_META` vai de 0 a 3,08. `VC10` com card ILUSTRAÇÃO vai de 3,08 a 9,64: "Ontem" começa em 3,4 e "lado." em 8,9. `C01_META` volta de 9,64 a 18,66, e "Resposta" começa em 10,0. `C02_SEM60` vai de 18,66 a 21,68 e cobre "Sessenta… Nem pro Pro." (20,8–21,1). O flash de gameplay saiu. Nas amostras, o card aparece a 4 s e não há quadro preto. |
| 3 | 282–300 s | **ok** | `C16_REMOTE` vai de 282,30 a 290,09 e cobre a fala inteira, de "E o Remote Play" (282,3) até "Xbox." (289,2). `S1213` com card entra em 290,09, em "É isso que o texto oficial diz". |
| 4 | 383,5–404 s | **ok** | P52 `C21` vai de 383,54 a 389,95. P53 `VC08` com card vai de 389,95 a 395,13, sobre "entra na balada: vida noturna, boates…" (encaixe bom). P54 `C21` vai de 395,13 a 399,08. P55 `S1203` com card vai de 399,08 a 402,10, sobre "Se inscreve no canal". P56 `C22` vai até o fim. Nenhum trecho de cartela passa de 6,4 s. |
| 5a | P29 `EXT@1218` (221,88–229,01) | **ok, com observação** | A amostragem a 1 quadro por segundo e o `blackdetect` não acharam preto. São cerca de 3 s de festa na piscina, sem rótulo nem nome, e depois uma corrida de rua noturna. A corrida mostra o HUD oficial no canto inferior direito ("PROGRESS 5–10%", posição "6/6" e um cronômetro "00:04.79"). Não é um contador de fps nem comparação. A fala no trecho é "upscaler de brinde… torcida nunca renderizou um pixel". Opcional: começar em cerca de 1218 e cortar antes de 1221 para evitar números na tela num episódio sobre fps. Não bloqueia. |
| 5b | `S1203` (P17 122,57–130,85; P55 399,08–402,10; Story P04) | **ok, com observação** | O quadro é válido: escuro, mas legível. Mostra dois homens dentro de um carro, sem nome ou rótulo na tela. Observação: P55 entra cerca de 3 s depois de a fala citar "Boobie Ike" (395,6). O risco de o público achar que um dos homens é ele é baixo, porque a `C21` fica entre os dois. Repetição: é a mesma cena do 3º quadro de P13 e do 1º quadro de P15 (EXT 1200–1207). |
| 5c | `S763` (P21 151,23–156,97; P51 372,15–383,54) | **ok, com observação** | Quadro diurno válido. O minimapa oficial do jogo aparece no canto inferior esquerdo, sob o card. Não há fps nem comparação. Observação: P51 é um still de 11,4 s e o mesmo quadro já aparece em P21. Trocar P51 por vídeo (por exemplo `EXT` 980–990 a partir de outro ponto) melhoraria o ritmo do fecho. É opcional. |

Notas laterais, não bloqueiam:
- `S1210` e `S1213` (268,83–299,2): depois da saída do card, aparece no canto inferior esquerdo um pedaço do minimapa oficial (ponto rosa e seta). Esse pedaço é do material-fonte e não é artefato da montagem.
- `VC11` ainda aparece em P06 e em P28, agora com 5,9 s. O achado 9 da 1ª revisão foi atenuado e não precisa de mais nada.

## Reel (`_reel`) — 1 correção obrigatória

| Plano / tempo | Achado | Severidade | Correção |
|---|---|---|---|
| Fim · 62,18–62,86 s · P09 `C05_BLOG` (0,7 s) | O corte do áudio é `[0.0, 62.86]`. Pelo alinhamento, depois de "não minha." (61,92) vêm **"No" (62,44–62,70) e "mesmo" (62,70–62,86)**. Isso foi confirmado no WAV: o nível cai para cerca de −60 dB em 62,1–62,3 e volta para −25 e −14 dB em 62,5–62,8. O Reel termina, portanto, com o começo audível de "No mesmo…", cortado no meio. Além disso, `C05_BLOG` pisca por 0,7 s, curto demais para leitura. | **bloqueia** | Em `audio/cortes_pecas.json`, mudar `reel` para `[0.0, 62.30]` (vale entre 62,15 e 62,35, que está em silêncio). Regenerar `_reel/audio/narracao.wav` e `palavras.json`. Remover o P09 `C05_BLOG` e estender `C04_PRO` até o fim. Depois, conferir que a última palavra do `palavras.json` é "minha." |
| P01–P08 | Mesma abertura corrigida do longo (C01 → VC10 → C01 → C02 → C03). | ok | — |

## Story (`_story`) — aprovado

| Plano | Resultado |
|---|---|
| Início | O corte é `[384.14, 404.09]`. "Amanhã" começa em 0,10 s, então a voz entra praticamente no primeiro quadro. |
| P01 `C21` 0–5,8 s · P02 `VC08` 5,8–11,0 s · P03 `C21` 11,0–14,9 s · P04 `S1203` 14,9–18,0 s · P05 `C22` 18,0–19,95 s | A cartela foi dividida e nenhum plano passa de 5,8 s. "dias." termina em 19,14 s, com 0,8 s de cauda sobre `C22`. Ok. |

## Não verifiquei

- Os vídeos renderizados do Reel e do Story, porque não existem exportações nas pastas. Para eles, verifiquei só as folhas, o `episodio.json`, o alinhamento e o WAV.
- No longo, verifiquei em vídeo apenas as três janelas de amostra. Os demais planos, inclusive P29 `EXT@1218` e P17 `S1203`, conferi só pelas folhas, pelos stills e pela fonte.
- Legendas `.ass` e `.srt` sobre a imagem: só as vi queimadas nas amostras, onde estavam legíveis e sem corte. Não fiz uma revisão completa.
- Animação de entrada e saída dos cards além do que aparece nos quadros a cada 2 s.
- O vertical (`_vertical`), que ficou fora do escopo pedido.
- Itens que não mudaram em relação à 1ª revisão, como a repetição do trecho diurno EXT 760–790.
