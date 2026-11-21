# Revisão independente das folhas do pré-voo: DIA 06 (porta-malas)

Revisor independente, somente leitura. Data: 13/11/2026. Nada foi renderizado.
Objeto: as 8 folhas de `montagem/prevoo/`, as 2 de `_reel/montagem/prevoo/` e a de `_story/montagem/prevoo/`. Também li `episodio.json`, `_reel/episodio.json`, `_story/episodio.json`, `audio/palavras_alinhadas.json`, os `palavras.json` do reel e do story, `00_ROTEIRO_COMPLETO.md`, `PROGRESSO.md` e as referências em `montagem/referencias/`.
Numeração: planos **1-based**, na ordem de `formatos.longo.planos` (78 planos), igual às folhas. Os tempos são da timeline; `EXT@s` é o segundo da fonte.
Evidência própria: quadros extraídos da fonte com ffmpeg (`c1.jpg` e `c2.jpg` no scratchpad da sessão) e níveis RMS do áudio a cada 20 ms nos pontos de emenda.

**Veredito: REPROVADO para render.** Não há erro de fato na fala. O problema é que 4 pontos centrais não são sustentados pelo que aparece na tela, ou entram em choque com ela:
- o pico do episódio ("o ícone do carro some") não fica legível;
- o "letra por letra" da placa não dá para ler;
- 2 cards mostram um minuto que conflita com o que a fala diz.

Todos se corrigem no `episodio.json` e com recortes (dois deles já existem em `referencias/`), sem mexer na voz. Depois disso: rodar o pré-voo de novo, conferir só os trechos alterados e seguir para a `--amostra`.

## BLOQUEANTES

| # | Plano / tempo | Problema | Correção |
|---|---|---|---|
| B1 | **22** (98,3–102,6), e também 19 (84,0–89,6) e 27 (117,9–126,1) | **O pico do episódio não aparece.** A fala diz "nesse instante o ícone do carro some. Sobram três", e o card diz "15:57 • ÍCONE DO CARRO: sumiu". Só que o plano começa em EXT@959,0, quando o ícone já sumiu. O sumiço acontece entre 15:56 e 15:57,5, no fim do plano 21, sob "A Lucia desce". Além disso, os ícones ficam no canto superior direito, com cerca de 25 px a 1920 e cerca de 10 px no celular: ilegíveis em todas as folhas. O "realce no canto" previsto no roteiro não foi feito. O mesmo vale para "quatro estrelas, quatro bolinhas" (plano 19) e "4 ESTRELAS • 3 ÍCONES" (plano 27). | Fazer 2 recortes fixos do HUD no mesmo enquadramento de `CR_estrelas_15_30.jpg`: **15:56,0** (4 ícones, com o carro) e **15:57,5** (3 ícones). Plano 22: still ANTES/DEPOIS (ou os dois em sequência, cerca de 2 s cada) com `movimento: fixo` e o card atual, e depois volta ao vídeo. Plano 19: os primeiros cerca de 2,5 s em vídeo e o resto (de "quatro estrelas" em diante) no close `EST1530`. O plano 37 ("O mesmo cabide das estrelas") passa a usar `EST1827` como callback, o que é aceitável. No plano 27, opcional: um close de 16:24 (3 ícones vermelhos). |
| B2 | **43–44** (206,4–213,8) "a placa… é a mesma… Letra por letra"; **42** (200,0) "Sentinel escrito na traseira"; **25** (111,9) "Declasse Burrito" | Placa, emblema `SENTINEL` e emblema `DECLASSE BURRITO` ilegíveis nos quadros: pequenos, e a placa de 18:41 aparece à noite. O roteiro já condicionava o "letra por letra" à placa legível nos dois planos. O card SENTINEL só entra em 206,4, 6 s depois da palavra (200,28). | O recorte pronto `referencias/CROP_0828_SENTINEL_1612_BURRITO_1841_placa.jpg` tem os 3 trechos nítidos: placa de dia com SENTINEL, BURRITO, placa de noite. Fatiar em 3 stills (`CR_placa_0828`, `CR_burrito_1612`, `CR_placa_1841`). Inserir `CR_placa_0828` em cerca de 206,4–208,6 ("E a placa desse minuto oito") e `CR_placa_1841` em cerca de 212,0–213,8 ("Letra por letra"), as duas com `movimento: fixo`. O vídeo 18:40 fica em 210,5–212,0. `CR_burrito_1612` entra no plano 25, em cerca de 112,5–114,5. Mover o card SENTINEL para entrar em cerca de 200,2. |
| B3 | **33** (161,5–165,58), card "CAMARIM \| 13:10 • Jason e Lucia no carro" | Número na tela contra número dito. A fala "Minuto dezessete e cinquenta" (163,86–165,24) cai dentro do plano 33, com o card "13:10" ainda visível. Só em 165,58 entra o card 17:50. A fala nunca cita 13:10. | Cortar o plano 33 em **163,80** e começar o plano 34 (F1750, card 17:50) em 163,80. Ou tirar "13:10" do detalhe, por exemplo "Jason e Lucia no carro". |
| B4 | **58** (268,34–272,0), card "RACHA ILEGAL? \| 20:07 • sem polícia, aposta ou estrela" | O card põe o minuto 20:07 na afirmação. Só que "nessa corrida de rua… não mostra polícia, aposta nem estrela" foi checado na corrida de **20:21,5–20:25,9**. Em 20:07 o que aparece é um SUV na pista do aeroporto, que não é corrida. O card faz o SUV passar pela corrida. | Detalhe "20:21 • sem polícia, aposta ou estrela", ou o texto do roteiro, sem minuto: "Corrida de rua: sem polícia nem aposta na tela". A imagem pode ficar (ilustração). |

## AJUSTES

| # | Plano / tempo | Problema | Correção |
|---|---|---|---|
| A1 | **20** (89,64), EXT@949,0 | Entrada suja. Em 949,0–949,5 a tela mostra **outra cena** (rua com perua e um casal de scooter), por cerca de 1 s, sob "No minuto quinze e cinquenta". O sedã só aparece em 950,0. | Plano 20 `inicio` **950,0** com `corte` [90,64, 93,7], o que dá 950,0–953,06 e mantém o plano 21 intacto. Estender o plano 19 (EXT@930) até 90,64. Ele termina em 936,64 e não encosta no plano 29 (937). Verificar no pré-voo se 935,6–936,6 está limpo. **Não** empurrar o plano 21: de 957,9 a 959,0 aparece a roda de armas, com transição desfocada. |
| A2 | **54** (256,34), T1@70,0 | Entrada suja. O quadro 70,0 é o assalto à loja (Lucia e Jason de bandana) sob "Um é circuito". O carro derrapando só entra em cerca de 70,4. | `inicio` **70,4**. |
| A3 | **55–56** (258,5–266,22) | (a) O plano 55 (EXT 1115,0–1119,4) termina com cerca de 0,25 s da **fuga noturna do conversível**: em 1119,2 já é noite. Esse trecho se repete nos planos 44 e 71. (b) "minuto dezoito e trinta e cinco" (262,76–263,98) cai sobre o **T2** (plano 56), e não sobre a moto. | A moto limpa vai de 1114,9 a 1119,1 (1114,7 ainda é o estande de tiro). Novo arranjo: plano 54 T1@70,4 `corte` [256,34, 259,9] (verificar T1 até 73,96); plano 55 EXT@**1114,9** `corte` [259,9, 264,1] (termina em 1119,1), com o card entrando em "moto"; plano 56 T2@153 `corte` [264,1, 266,22]. |
| A4 | **50** (236,82–241,36), T1@25 | Em T1@29,0 o vídeo corta para a **boate/strip club**: cerca de 0,6 s no fim, sob "a tela entrega a diferença". O trecho limpo (mulher no carro e rua de rebaixados) vai até cerca de 28,9. T1@24,x são lanchas, então não dá para recuar o início. | Terminar o plano 50 em **240,72** (T1 25,0–28,9) e cobrir 240,72–241,36 com o plano 51 começando antes. Antes, conferir se o EXT 17:46,9–17:47,6 continua no autódromo, porque 17:41 é boate. Se não estiver, usar 0,64 s de `DUPLO` antecipado ou aceitar o T1 terminando em 28,9 com um corte para o 51 em 240,72 e `inicio` 1061,36 só se 17:41,4 já for pista. |
| A5 | **09** (34,2–36,3), LT@47,0 | Três tomadas em 2,1 s: carro verde, viatura (cerca de 47,9–48,85) e ciclista no viaduto ao pôr do sol (48,9). A "viatura do lado" que a fala descreve é a do gameplay, em 18:24, e não a do trailer. | Trocar por um still de `EXT_1824.jpg` (viatura `POLICE` à direita, 2 estrelas, `LIVE 51k`; recorte da metade direita, `movimento: fixo`). É a prova real e libera o selo. Se o trailer ficar, usar `LT@47,9` por no máximo 0,95 s e completar com o close. |
| A6 | **03–04** (10,72–15,9) | O plano 03 dura **1,08 s** e carrega o card "18:12 • Porta-malas do Buffalo", que não tem tempo de leitura. Em seguida o plano 04 volta ao still de 18:12,0, um salto para trás no tempo: a Lucia já tinha se virado no fim do plano 03. | Fundir: still `F1812` de 10,72 a 15,9 com o card 18:12. Ou o vídeo 18:12 até 15,9 (EXT 1092,0–1097,18) e começar o plano 07 em 1097,2 (verificar se ele ainda está de pé e filmando até 1104). |
| A7 | **47–48** (224,4–232,3) | "a tela dá duas opções **no minuto seis**" é dito sobre o T2 (Jason ao volante). O prompt `SLIM JIM / SMASH WINDOW` só aparece no início do plano 48 (06:05,2) e some antes do fim. O roteiro colocava o T2 na piada "A outra faz você parecer o dono". | Inverter: EXT@365,2 em 224,4–228,5 (o prompt aparece sob "duas opções"), close `SLIMJIM` em 228,5–233,0 ("triângulo… bolinha"), T2@28 em 233,0–236,82 ("Uma faz barulho. A outra faz você parecer o dono"). |
| A8 | **67** (315,5–320,7), LT@6 | Mostra **oficina em vídeo** (Brian's Marina, polimento e casco de barco no galpão) logo depois de "uma oficina que só existe em foto" e "não achei nenhuma oficina por dentro". Mesmo com o selo, convida o "olha a oficina aí". | Usar as janelas do roteiro (T2 02:24–02:25,9 e T1 00:52–00:53,9, conferindo os cortes) ou um trecho de rua do EXT. Se o LT ficar, a fala precisaria ressalvar "oficina de carro". |
| A9 | **Story** (0–15,83) | (a) Abre com "E me conta aí: no dia dezenove, você larga o carro **marcado**…": começa com "E" e cita "carro marcado" sem contexto, com um gancho fraco para Story. (b) O áudio começa em 355,12, com cerca de 40 ms do rabo de "cara." (−38 dB no primeiro quadro), e depois 0,64 s de silêncio. (c) Plano 1 com 1,28 s. A emenda 369,30→375,15 está **limpa** ("…sem pausar, \| Já se inscreve…", silêncio nos dois lados) e lê bem. | Story = trecho contínuo **360,70–377,72** (cerca de 17 s, sem emenda). Planos: 20:35 (card AMANHÃ 15/11) → 07:20,2 (geladeira) em "incluindo o que tá colado" (369,28) → 10:00 (HOLD HANDS) em "mão dada" (372,84). Se o operador preferir manter a pergunta, cortar o início em ≥355,20. |
| A10 | **Reel** (0–60,82) | (a) Emenda em 49,95: corta o decaimento de "influenciador." ainda a cerca de −31 dB, que só chega a −66 dB em 50,04. O risco é um estalo. A emenda lê bem: "Leonida leva influenciador. \| E se abrir um porta-malas…". (b) "você larga o carro **marcado**" fica órfão: o reel nunca apresenta o ícone. (c) O fim em 359,95 corta "fim?" ainda a −31 dB. | (a) Terminar o 1º trecho em **50,06**, que é silêncio digital. (b) Terminar o reel em "…já viram a sua cara." (cortar em cerca de 355,2; 56 s), com o CTA só no card. Outra opção é manter a pergunta e trocar o card por "Larga o carro ou foge com ele? Comenta". (c) Se a pergunta ficar, cortar o fim em 360,0. |

## OBSERVAÇÕES (não bloqueiam)

- **Plano 01 (gancho):** o close `TRUNK` mostra mais as costas da Lucia que o streamer. Pernas e topete aparecem, mas pequenos, à direita. Está dentro da regra (voz no quadro 0 e uma evidência). Um recorte mais fechado no interior, como no roteiro, deixaria o gancho mais claro.
- **Plano 05 (BUFFALO):** o letreiro na tampa é escuro e pequeno no recorte. Vale um contorno ou um recorte mais fechado.
- **Planos 16–17:** dois stills quase idênticos do HUD (18:26 e 18:27) seguidos, com cerca de 10 s de imagem parada. Pode ser um único still com o card na âncora "Um cabide".
- **Repetição visual:** o plano 61 (13:18, interior do carro com o outdoor "OVER A NEW LEAF") repete o enquadramento do plano 33 (13:10). O plano 70 (08:15, Jason entrando no conversível com a mulher de rosa) repete o fim do plano 41. Os segundos da fonte são diferentes, mas a tomada parece a mesma. O primeiro quadro do plano 38 (17:52) é igual ao still `F1750` do plano 34.
- **Plano 12:** 3 tomadas do T1 em 3 s (câmera de loja, bodycam, posto). Ilustração da piada, com selo. Aceitável.
- **Plano 23 (`F1558`):** ordem 16:03 → roda (15:58) → 16:03,3. O pulo é pequeno, aceitável. O card diz "ROLETA", a fala diz "roda": tanto faz.
- **Plano 56:** o último quadro do T2 (cerca de 155,5) é bem escuro. Se o A3 for aplicado, ele sai.
- **Plano 74 e Reel plano 14:** "se abrir um porta-malas e tiver um streamer lá dentro" passa sobre o conversível. No longo isso é intencional (não repetir o trecho). No reel, um callback visual do porta-malas (EXT 18:22–18:24, ainda não usado) seria mais forte.
- **Plano 77:** quem aparece na geladeira é o Jason. "Geladeira da Lucia" segue a identificação do roteiro (casa/cozinha); está ok.
- **Último plano (78):** sem logo nem data, então não há conflito. `legenda_alta` deixa livre o prompt `HOLD HANDS` no canto inferior direito.
- **Alinhamento:** "E me conta aí" hoje está em 355,77–356,32 em `palavras_alinhadas.json`, sem a compressão citada no PROGRESSO. Também está assim no reel e no story.
- **Selos:** as folhas não desenham selo, card nem legenda. O pré-voo informa selo persistente nos planos de T1, T2, LT e Ultimate Edition (9, 12, 13, 47, 50, 54, 56, 59, 62–68). Conferir isso na `--amostra`.
- **Vertical (reel e story):** o 16:9 vira o miolo de 1080 px sobre o fundo desfocado. Os HUDs do vídeo ficam ainda menores, o que reforça B1 e B2. Os closes resolvem.

## Conferido e OK

O gancho tem 5 palavras e a voz começa no quadro 0. Também conferem:
- Plano 07: de pé, óculos, moletom, filmando em 18:15; "três segundos" bate.
- Plano 08: deitado no porta-malas, carro andando, live.
- Planos 10–11: `LIVE 51k`, 2 estrelas acesas, "KING OF TRUNK!!".
- Plano 13: influenciadora em cima do carro.
- Plano 14: card SÁBADO 14/11 e faltam 5 dias.
- Planos 21 e 24–25: garagem coberta, Lucia de bandana, molotov e fogo, van vinho.
- Planos 34–36: conversível na Zekes Gadgets; roda WEAPONS → ITEMS com FACE WRAP ON, óculos e boné OFF, cabide.
- Planos 39–40: WE DO REPAIRS e cartaz de celulares.
- Planos 41–42: Jason entra no conversível; a capota recolhe em 08:27.
- Plano 46: viaturas atrás do conversível em 18:43.
- Planos 51–53: LAP 1/2, x/16, PROGRESS %, x/6, luz azul; o duplo está legível.
- Planos 62–66 e 68: as imagens da Ultimate Edition batem com cada frase.
- Planos 76–78: AMANHÃ 15/11, geladeira, HOLD HANDS R2.
- Nenhum plano tem menos de 1,2 s, exceto o 03 (A6). O plano 13 tem 1,46 s e o plano 1 do story 1,28 s, os dois legíveis.

## Não verificado

- Áudio ouvido: só medi o RMS nas emendas. A escuta humana pendente no PROGRESSO continua pendente.
- Algumas janelas alternativas, marcadas com "verificar": T1 72,2–74,0; EXT 935,6–936,6; EXT 17:46,9–17:47,6; T2 02:24 e T1 00:52.
- Cards, legendas e selos renderizados (as folhas não os desenham).
