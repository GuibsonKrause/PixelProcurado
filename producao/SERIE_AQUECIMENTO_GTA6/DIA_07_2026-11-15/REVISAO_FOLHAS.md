# Revisão independente das folhas do pré-voo: DIA 07 (11 detalhes pausando)

Revisor independente, somente leitura (não participei da direção). Data: 13/11/2026. Nada renderizado.
Objeto: 11 folhas de `montagem/prevoo/`, 2 de `_reel/montagem/prevoo/` e 1 de `_story/montagem/prevoo/`. Também li `episodio.json`, `00_ROTEIRO_COMPLETO.md`, `montagem/referencias/EVIDENCIAS.md`, `audio/palavras_alinhadas.json` (fala por plano cruzada com script), `PROGRESSO.md` e o modelo do Dia 06.
Numeração: planos **1-based** na ordem de `formatos.longo.planos` (100 planos), igual às folhas. Tempos = timeline; `EXT@s` = segundo-fonte do Extended Look.
Evidência própria: tiras de quadros extraídas do `GTAVI_An_Extended_Look.mp4` com ffmpeg (scratchpad da sessão): TV 445,0–453,5 a cada 0,5 s e 446,5–447,7 a cada 0,1 s; joalheria 1079,5–1084,5 e 1082,6–1083,4 a 0,1 s; 544,0–547,0; 1141,4–1144,2; 1146–1151,5; 465,3–467,9; 395,0–396,4; 601,8–605,3.

**Veredito: APROVADO COM AJUSTES** (1 bloqueante simples, de troca de imagem; nenhum erro de fato na fala, de botão ou de número em card).

## BLOQUEANTE

| # | Plano / tempo | Problema | Evidência | Correção (episodio.json) |
|---|---|---|---|---|
| B1 | **40** (148,81–151,21) "Logo depois aparece uma **nuvem de chuva em cima dele**" + **42** (`MINIATURAS_TV`, miniatura "NUVEM") | A imagem não mostra o que a fala diz. O plano 40 (EXT 450,15–452,5) é céu de pôr do sol com a **pílula azul** e o braço azul, ou seja, antecipa o plano 41 (07:32). A nuvem de chuva sobre o cérebro existe só em **EXT 447,2–447,3** (relâmpago/nuvem cinza sobre o cérebro no banco, ~0,2 s), dentro do plano 38, sob outra fala. A miniatura "NUVEM" da cartela é o mesmo céu ensolarado com a pílula, não nuvem de chuva. | Folha 04, plano 40 (3 quadros); folha 05, plano 42; tira 446,5–447,7 (nuvem só em 447,2 e 447,3). | Extrair still nativo 3840 de **EXT 447,25** (`CR_nuvem_chuva.jpg`, recorte na TV) e usar no plano 40 `[148,81, 151,21]` com `movimento: fixo` (opcional: zoom lento). Refazer `MINIATURAS_TV.jpg` com esse quadro na miniatura do meio ("NUVEM DE CHUVA"). O plano 41 (`EXT0732`, joinha confirmado no nativo) fica. Não afeta reel/story; afeta `_vertical` (mesmos planos). |

## AJUSTES

| # | Plano / tempo | Problema | Evidência | Correção |
|---|---|---|---|---|
| A1 | **02 → 04** (2,96–24,33) | Repetição: o still do plano 02 (`EXT0950` = EXT 590,0) é exatamente o 1º quadro do vídeo do plano 04 (EXT@590,0). Depois da geladeira (plano 03), o plano 04 "recomeça" do mesmo quadro congelado. | Folha 01, planos 02 e 04 (1º quadro idêntico). | Plano 04 `inicio` **591,0** (fim 603,17); plano 06 `inicio` **603,2** (fim 606,0; terraço contínuo até 606,6, conferido na tira 601,8–605,3). Prompt `HOLD HANDS R2` segue visível. Afeta **reel** (planos 02–06 iguais). |
| A2 | **03** e **09** (6,58–12,16 e 34,18–38,06) | Mesmo still `EXT0716` duas vezes em 28 s (5,6 s + 3,9 s), com o plano 07 (`EXT0715`) e o vídeo 08 entre eles: a geladeira "fechada" parece congelada no mesmo quadro. | Folha 01, planos 03 e 09. | Plano 03 → `EXT_0718.jpg` (já existe, 3840; porta cheia de coisas coladas) recortado/zoom fixo na metade superior da porta (fotos, post-its, FLEECA, panfleto), **sem** o menu, para não antecipar o plano 12. Plano 09 fica com `EXT0716` ("um homem de camisa preta parado na frente"). Afeta **reel**. |
| A3 | **56–58** (221,65–230,72) | Plano 56 (`CRzoomprompt`, 3,55 s) é ~90% preto (vinheta do binóculo) sob "o direcional é a fofoca"; o plano 57 leva o card "17:27 • BINÓCULO" em só **1,8 s**; o close do prompt ZOOM não cai sob "zoom no direcional" (228,5). | Folha 06, planos 56–58. | Trocar as mídias de 56 e 58: plano 56 = `EXT1727` (janela visível), plano 58 = `CRzoomprompt` (agora sob "e no canto, zoom no direcional"). Mover o card `17:27 • BINÓCULO / zoom no direcional` do plano 57 para o plano 58 (3,7 s); plano 57 vira `sem_card`. |
| A4 | **68** (262,24–265,18), EXT@1080,35 | O plano cruza um corte: o vídeo corta da joalheria para a rua (homem de camisa verde nº 68 saindo pela porta `FLEECA`) em ~**1083,25**; o fim do plano (1083,29) pega 1 quadro da cena seguinte. | Tira 1082,6–1083,4 a 0,1 s (último quadro já é a rua). | `inicio` **1080,2** (fim 1083,14; 1080,17 já é o interior da joalheria). Ver também O1 sobre o conteúdo. |
| A5 | **19** (68,54–74,0), EXT@390,0 → plano **25** EXT@396,0 | O plano 19 cruza um corte em ~**395,2** (novo ângulo: Lucia deitada de celular) por ~0,3 s, e o plano 25 começa 0,8 s depois nesse mesmo ângulo: a cama aparece "duas vezes". | Tira 395,0–396,4; folha 02 (plano 19, 3º quadro) e folha 03 (plano 25). | Encurtar o plano 19 para terminar em EXT 395,1: `inicio` **389,64** (conferir no pré-voo que 389,6–390,0 é a mesma tomada; se não for, aceitar o resíduo de 0,3 s, que vira O). |
| A6 | **71–81** (268,9–316,68) | Ritmo: ~45 s quase só do **mesmo HUD de 18:57**. `EXT1857` aparece 3× (22, 72, 79), `CRretratos` 2× com o **mesmo recorte** (73 e 77), `CRcarinhas` 2× (74 e 81). Só 75–76 têm vídeo (5,4 s). Os planos 73 (6,8 s) e 81 (6,9 s) são stills longos sem variação. | Folhas 08 e 09. | (a) Plano 77 ("FATO: 2 RETRATOS"): novo recorte de `EXT_1857.jpg` a partir do nativo 3840, **só retratos + coração** (como o roteiro previa); o `CR_1857_troca.jpg` existente tem 900×400 e ficaria mole em 4K. (b) Plano 79: `movimento` com push lento sobre `EXT1857`, ou a 1ª metade com vídeo EXT **[1141,6–1143,4]** (satélite limpo, ainda sem uso) e o resto no still. (c) Plano 81: push lento no `CRcarinhas`. Não usar EXT >1147,3 (corte para o aeroporto). |
| A7 | **62** (238,95–243,92), `DIVIDIDA_BINOCULO_HEADSET` | O título da cartela "CADA UM ACHA QUE O ESQUISITO É O OUTRO" entrega a piada ~1 s antes da fala (243,9, plano 63). Durante "Pensa na cena: você, de binóculo…", a tela já mostra o punchline. | Folha 07, plano 62. | Refazer a cartela com o título **"VOCÊ × ELE"** (rótulos "VOCÊ, DE BINÓCULO" e "ELE, DE VR" ficam). Se quiser a frase escrita, colocá-la como card no plano 63. |
| A8 | **35** (129,84–131,5), EXT@443,5 | Logo depois do card "DRINK • R1 / DROP", o HUD do vídeo já mostra `DRINK / **PUT DOWN**` (a 2ª linha muda em ~443,5). Em 4K dá para ler, e o espectador pode achar que o card errou. O roteiro pedia máscara no canto. | Folha 04, plano 35 (quadros 1–2, canto inferior direito). | Desfocar ou mascarar o canto inferior direito (~10% × 8% do quadro) durante o plano 35. Ou iniciar o `CRbarra` (36) em 129,84 e cortar o vídeo 35, se a máscara não for prática no pipeline. |
| A9 | Global: stills `CR_*`, cartelas, colagens, `CR_hold_casal` | Todas as referências usadas como mídia têm **1920×1080** numa saída **3840×2160**: upscale de 2×. Cartelas com texto pequeno ("ícones redesenhados • a cena é sensível", rótulos das 11 miniaturas, "PIXEL PROCURADO") e o `CR_hold_casal` (quadro inteiro reduzido e ampliado de novo) vão ficar moles em 4K. | ffprobe das referências. | Regerar cartelas, colagens e `CR_hold_casal` em 3840×2160. Para os recortes, exportar a região nativa sem reduzir. Prioridade: plano 01 (gancho), 42, 49, 55, 62, 82–91, 93–94. |
| A10 | **13** (`CRmenuverde`) | "BLITZ GREEN SMOOTHIE" esmaecido está legível, mas é a linha menos visível do quadro, e o card diz "APAGADO" sem indicar onde. O roteiro previa seta/contorno. | `CR_menu_verde.jpg`. | Contorno amarelo `#FFD43B` ou seta na linha esmaecida (como em `CRtorneira`/`CRdrink`). |

## OBSERVAÇÕES (não bloqueiam)

- **O1, joalheria (plano 68, 262–265 s): aceitável, com o corte do A4.** O conteúdo é uma mulher (roupa cinza e calça vinho, sem nome) em luta corporal com um homem de camisa branca, que cai e fica estirado no chão; há pistola na mão dela. Não aparece sangue nem tiro, e é o mesmo uso do Dia 06. Serve à piada "deixa você assaltar joalheria". Se quiser suavizar: `corte` mais curto terminando antes do homem no chão (fonte ≤1081,5). Fala só 1,2 s, então o restante iria para o plano 69 (`EXT1734`). Não é necessário.
- **O2, cena sensível §15 (planos 82–90): OK.** `DESFOQUE_2527` em resolução total é um borrão marrom: sem contato, rosto, sangue ou ícone legível. `CRchaoconcreto` mostra só o chão e linhas (mangueira). Do 85 ao 90 são cartelas grafite com ícones redesenhados e o aviso "ícones redesenhados • a cena é sensível". Nenhum quadro nítido da luta.
- **O3, ritmo do bloco final:** 316,7–348,7 s (32 s) só tem cartela, desfoque e chão. É justificável pela sensibilidade, mas o bloco fica parado. Sugestão: zoom lento (`movimento` não fixo) nas cartelas 85–90 e entrada animada dos ícones no Hyperframes.
- **O4, planos curtos:** 85 (1,44 s), 86 (1,18 s), 95 (1,20 s), 96 (1,15 s) e 22 (1,64 s), todos sem card. As cartelas 85/86 têm 2–4 palavras, legíveis. 95–97 são a lista rápida "geladeira, mão dada, vizinho". OK.
- **O5, repetições intencionais (callbacks):** `CRdrink` 3× (33, 44 e dentro de 49/55); `EXT0643` (27 e 92, "o tênis do minuto seis"); `EXT1220` (23 e 54); `EXT1734` (24 e 69); `EXT1727` 4× (21, 58/56, 63, 97). Aceitáveis. Se der, no 63 usar `CRvrmaos` com outro enquadramento, ou o vídeo EXT [1047,0–1048,8] restante.
- **O6, plano 52** (EXT 672,0, 11:12, um acende o cigarro do outro): a fala diz "outro de camisa preta, **de costas** pra câmera", mas nesse plano ele aparece de perfil. Quem está de costas é o do plano 51. Diferença pequena. Opcional: começar o plano 52 em 205,1 ("de costas" ficaria no 51, estendido).
- **O7, plano 67** (`CRseguranca`): muito escuro, e o segurança mal se vê no celular. Subir a exposição ou gama do recorte (+0,5 EV).
- **O8, plano 57:** cruza a fala "visão" (226,9) com o plano 58. Sem problema.
- **O9, plano 99/100:** a janela EXT 456–467,6 tem um corte interno (TV para tela cheia), o que é ilustração válida. O plano 100 termina em 467,63, e o corte para o cervo é em ~467,8: margem de 0,17 s. Não alongar.
- **O10, plano 76:** o 1º quadro (1144,0) ainda está no fade quente e estourado da transição. Natural, e casa com "a cena seguinte já é outra".
- **O11, plano 47:** sem corte em 544,15–546,35 (a barra rosa no topo é HUD). OK.
- **O12, folha 11 desatualizada:** `Pixel_Procurado_DIA07_Longo_V2_11.jpg` (13:23) mostra um "PLANO 101" que não existe no `episodio.json` atual (100 planos). É sobra de uma execução anterior. O `episodio.json` (13:32) é posterior às folhas (13:26); segundo o PROGRESSO, a única mudança foi tirar a correção de legenda twenty/one. Ao rodar o pré-voo de novo, limpar `montagem/prevoo/` antes.
- **O13, alinhamento:** as entradas de `palavras_alinhadas.json` vêm com `"estimado": true, "probability": 0.0`. Os cortes batem com a fala nas folhas, mas as emendas de card e plano devem ser conferidas na amostra.
- **O14, critério 3:** nenhum card nomeia personagem (retratos sem nome; "homem de camisa preta"). Fleeca, Lombank, Logger, Lavazas e Blitz aparecem só na fala, na legenda ou no próprio HUD, nunca como prova em card. Nome de loja (`…MARKET FOOD BY THE POUND`, `M Fashions`) e de clube (`J&H`) só no cenário. OK.
- **O15, critério 5:** hipóteses marcadas: 42 "(PARECE)", 55 "HIPÓTESE • fato: 3 prompts R1", 78 "HIPÓTESE • MENU DE TROCA / leitura minha", 80 "HIPÓTESE • LEMBRA O GTA V", 89 "HIPÓTESE / leitura minha, não confirmada". OK.

## Conferido e OK

Também conferem:
- **Gancho:** 6 palavras, voz em 0,17 s, `CR_hold_casal` com contorno amarelo em `HOLD HANDS R2`.
- **Planos 04–06:** casal de mãos dadas no terraço, prompt R2.
- **Plano 05:** `CRholdprompt` com R2 legível; o card "R3 → R2" bate com "tava R três. Errado".
- **Plano 10:** `△ ⋮ FRIDGE`, card 07:16.
- **Planos 12–18:** menu Logger/Lavazas/Blitz Berry/Green esmaecido; porta com FLEECA, LOMBANK, foto do cachorro na grama, panfleto "Frugality is for Fools."; duas cervejas `LOGGER`.
- **Planos 26–30:** vestidos em cabide sem banheira; tênis de sola caramelo e mão no cadarço; torneira com contorno e sem água.
- **Plano 33:** `DRINK R1 / DROP`, quadro ≤07:23,4, sem `PUT DOWN`.
- **Planos 37–39 e 41:** caixa de suco na TV; cérebro no banco com os dentes; pílula azul e joinha (confirmado no nativo `EXT_0732`).
- **Planos 45–50:** salgadinho vermelho e `EAT R1 / DROP`; 4 pessoas e 2 máquinas.
- **Planos 51–53:** havaiana, óculos verdes, `SMOKE R1`.
- **Planos 59–61:** VR, parede verde, mãos.
- **Planos 64–66:** `OVER 21 ONLY`, `ID Check`, "STATE LAW PROHIBITS THE SALE OF ALCOHOL TO MINORS".
- **Planos 73–74:** dois retratos, coração rosa, R1, diabinhos.
- **Plano 80:** vista de satélite.
- **Planos 91/94:** colagem com 11 miniaturas numeradas e "11/11".
- **Plano 93:** "QUINTA, 19/11 • FALTAM 4 DIAS".
- **Planos 98–100:** AMANHÃ 16/11, PS5 × PS5 Pro.
- **Cards:** os timecodes de todos os cards batem com o quadro mostrado.
- **Pretos e duração:** não há quadro preto real nem glitch fora das transições de origem (75). Nenhum plano com card tem menos de 1,5 s, exceto o 57 (A3).

## Reel e Story

- **Reel** (18 planos, 0–67,3 s): os planos 01–17 são idênticos aos do longo. Herdam **A1** (02 → 04) e **A2** (03/09) e A9 (resolução). O plano 18 (`CRcervejas`, card "VÍDEO COMPLETO NO CANAL") está OK. Não herda o B1.
- **Story** (3 planos): é o mesmo §18 do longo (planos 98–100), com o plano 01 em EXT@847,75. Perseguição com tiro, sem sangue; OK. Nada a corrigir.
- **_vertical:** espelha o longo e herda B1 e A1–A10. As folhas de `_vertical/montagem/prevoo/` não foram pedidas e não foram revistas. Conferir na amostra se o miolo 16:9 mantém legíveis o HUD do gancho e os closes.

## Para conferir em vídeo (etapa `--amostra`)

1. **Gancho, 0–3 s:** voz no 1º quadro, contorno do R2 legível no celular e na versão vertical.
2. **Emendas de vídeo:** 01 → 02 → 03 (still → still → still); 04 com `inicio` novo; 19 → 20 (corte em 395,2); 68 terminando antes de 1083,25; 75 → 76 (transição de satélite com flash branco, sem salto).
3. **Plano 35:** máscara do `PUT DOWN`.
4. **Entrada e saída dos cards** nos planos com 3–4 s (05, 10, 13, 37, 48, 53, 58 após A3, 65, 66) e o tempo de leitura do card do 77/78.
5. **Legendas:** grafia `OVER 21 ONLY` (sem espaço duplo), `R1/R2/R3`, `DRINK/DROP/EAT/SMOKE/ZOOM`, `Frugality is for Fools`, `PS5 Pro`. `legenda_alta` no último plano, se houver prompt no canto.
6. **Movimento dos stills:** blocos 71–81 e 82–90 (A6/O3), para ver se o ritmo deixa de parecer congelado.
7. **Nitidez em 4K** das cartelas e recortes depois do A9.
8. **Bloco sensível (319–344 s):** confirmar no vídeo final que nenhum quadro nítido da 25:26 entra por transição ou crossfade.
9. **SFX previstos** (pausa no 1º quadro, porta de geladeira, garrafas, gota, saco de salgadinho, zoom, whoosh) e o volume da trilha sob a TV.
