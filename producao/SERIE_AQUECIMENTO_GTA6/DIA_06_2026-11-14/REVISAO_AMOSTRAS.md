# Segunda revisão independente: amostras do DIA 06 (porta-malas)

Revisor independente, somente leitura. Data: 13/11/2026. Não ouvi áudio; só medi RMS a cada 20 ms nas emendas.

**Material conferido:**
- As 6 amostras do longo (`_previa`, 960x540), a do reel (0–14) e a do story (0–17), com quadros extraídos a cada 0,5 s e a cada 0,1 s nas entradas e saídas de card.
- As folhas do pré-voo: longo 01 a 09, reel 01 e 02, story 01.
- `EXEC_AMOSTRAS.log`, os `*.qa.json`, os `episodio.json` do longo, do reel e do story, `audio/palavras_alinhadas.json` e os `palavras.json` do reel e do story.

Os quadros de evidência estão em `montagem/_rev2/`.

Numeração: planos 1-based da timeline atual (83 planos no longo, 13 no reel, 3 no story). Os tempos são da timeline; `EXT@s` é o segundo da fonte.

## Veredito por peça

| Peça | Veredito |
|---|---|
| **Reel, Story e `_vertical`** | **REPROVADO**. B1: o fundo desfocado sai verde em todos os planos de vídeo. |
| **Longo 16:9** | **Aprovado para 4K com condições.** Antes de renderizar, aplicar A1 a A4. Depois, fazer uma reamostra de 98 a 116 s (planos 22–27), que nunca foi vista em movimento. |

As correções B1–B4 e A1–A10 da primeira revisão estão aplicadas e funcionam no que foi renderizado. Há duas exceções: o A10(b) foi aplicado pela metade, porque o reel ficou sem CTA (A5 abaixo), e o "ícone some" (plano 23) não foi renderizado.

## BLOQUEANTE

| # | Peça / plano / tempo | Problema | Correção |
|---|---|---|---|
| B1 | **Reel** (planos 2, 6, 7, 11–13), **Story** (planos 1–3) e, pelo mesmo código, **`_vertical` inteiro** | **Metade direita do fundo desfocado em verde chapado** em todo plano de **vídeo**. Os planos de still (TRUNK, F1812 etc.) saem certos. Aparece na própria folha oficial `_story/amostra/exportacoes/folha_0-17.jpg` e nos quadros `montagem/_rev2/s_reel.jpg` e `s_story.jpg`. O QA saiu com rc=0 e 0 pretos, ou seja, o `validar_v2.py` **não detecta** esse defeito. **Causa reproduzida:** o mesmo filtro do `produzir_v2.py` (linhas 220–224: split → scale 270x480 → boxblur) com `-hwaccel d3d11va` (o padrão) gera o verde. Sem hwaccel, gera o fundo correto. Evidência: `montagem/_rev2/test2_d3d11va_s.jpg` e `test2_none_s.jpg`, fonte EXT@1095. | Renderizar reel, story e `_vertical` com **`--hwaccel nenhum`** (já suportado pelo CLI). A alternativa é forçar `format=yuv420p` no ramo `[blur]`. **Atenção ao cache:** `cut_shot` reaproveita o clipe por plano que já existe (`<build>/<stem>/NN.mp4`). Antes de renderizar de novo, o operador precisa apagar os clipes de vídeo verdes, por exemplo em `_reel/amostra/montagem/Pixel_Procurado_DIA06_Reel_V2/` e `_story/amostra/montagem/Pixel_Procurado_DIA06_Story_V2/`, e qualquer build de `_vertical`. Se não apagar, o defeito volta. Depois, conferir um quadro de cada plano de vídeo. O longo horizontal não passa por esse ramo e está limpo. |

## AJUSTES

| # | Peça / plano / tempo | Problema | Correção |
|---|---|---|---|
| A1 | Longo **63** (268,34–272,0), EXT@1209,12, card "RACHA ILEGAL? \| 20:21 • sem polícia, aposta ou estrela" | O B4 corrigiu o texto do card, mas a imagem continua sendo o SUV na pista do aeroporto, em 20:09. A fala diz "nessa corrida de rua" e o card carimba "20:21" sobre um quadro de 20:09. Para um canal que vende minuto exato, o minuto fica atribuído à imagem errada. A primeira revisão aceitou a imagem como ilustração, por isso fica como AJUSTE. | Trocar o plano 63 por um still `referencias/EXT_2024.jpg` (20:24: corrida de rua, PROGRESS 8 %, 3/6, sem estrela nem viatura), com `movimento` leve e o card atual. O plano 62 pode ficar. |
| A2 | Longo **83** (372,84–377,72), `legenda_alta` | A legenda alta ("de mão dada no minuto dez." / "Já se inscreve…") **encosta na borda superior direita do próprio card** HOLD HANDS. As duas se sobrepõem em cerca de x 318–380 e y ~372 (a 960x540), no tempo 373,3–375,5. Veja `montagem/_rev2/fim_373_4.png`. O último plano não tem logo nem data. O único elemento a proteger é o prompt `HOLD HANDS (R2)` no canto inferior direito (x ≥ 855), e a legenda centralizada na posição normal não chega lá. | Tirar `legenda_alta` do plano 83, ou subir a legenda alta acima de y ≈ 330 (a 540). Conferir no 4K que o prompt R2 continua livre. |
| A3 | Longo **59** (258,74–259,9), T1@66,5 | Mostra cerca de 0,15 s de motos empinando e depois cerca de 1 s do boletim **WEAZEL NEWS "DIRT-BIKE DIRT-BAGS / COPS FAIL TO STOP THUGS ON MOTORBIKES"**, com viaturas, sob "ponto a ponto. E tem um terceiro". Dois problemas: (a) a legenda fica sobre o letreiro do boletim e os dois textos disputam leitura; (b) imagem de polícia perseguindo moto aparece 8 s antes de "o vídeo não mostra polícia". | `inicio` **65,70**. A tomada limpa das motos vai de cerca de 65,65 a 66,65. Isso deixa cerca de 0,15 s de boletim no fim, o que é aceitável. Ou encurtar o plano 59 e estender o 58. |
| A4 | **Reel 12** (48,46–50,06), T1@44,0 → 45,6 | O T1 corta em cerca de 45,47 para uma **aérea noturna com explosão**. Com isso, cerca de 4 quadros piscam logo antes da emenda de 50,06. No longo, o plano 12 termina em 45,46 e está limpo. | No reel, `inicio` **43,86**. A tomada da caçamba vai de cerca de 43,85 a 45,46, então 43,86 + 1,60 = 45,46. |
| A5 | **Reel 13** (50,06–56,23), sem card | A10(b) previa "o CTA só no card". O reel agora termina em "…já viram a sua cara." **sem nenhum CTA nem pergunta**, e o vídeo acaba 0,1 s depois da última sílaba (56,12). | Card no plano 13, entrando em cerca de 53,4 ("Cinquenta mil…"): por exemplo "LARGA OU FOGE? \| Comenta • episódio completo no canal". Opcional: 0,3–0,5 s de cauda, se o formato permitir. |

## OBSERVAÇÕES (não bloqueiam)

- **Plano 22→23 (pico):** o corte para "sem carro" acontece em 100,6. A fala diz "ícone" em 100,84 e "some" em 101,34, então o ícone some cerca de 0,7 s antes do verbo. Lê como sincronia em "o ícone", o que é aceitável. Na folha do pré-voo, os dois stills estão legíveis: 4 ícones com o carro à direita, depois 3 ícones. Os ícones são alinhados à direita, então o grupo "anda" um ícone para a direita, mas a falta do carro fica clara. O fundo muda (escuro → faixa de sebe), o que é aceitável.
- **Plano 47** (210,5–212,0, EXT@1120): os últimos cerca de 0,4 s (fonte 1121,1–1121,5) são a transição desfocada de troca de personagem, com retratos no canto. Sai por corte em 212,0. Se quiser, terminar em cerca de 211,6 e entrar com o `PLACA1841` antes.
- **Plano 57 (DUPLO):** o card "PONTO A PONTO?" e a legenda ficam sobre os cronômetros (00:21.32 / 00:07.88). LAP 1/2, PROGRESS 9 %, 8/16 e 3/6, que são o que importa, ficam livres.
- **Plano 8** (F1824 de corpo inteiro, 34,2–36,3) vem depois do vídeo 18:24–18:28,2 do plano 7: é um pequeno salto para trás. A viatura `POLICE` está à direita e legível. `CR_viatura_1824.jpg` existe e não foi usado.
- **Plano 36** (F1750): still totalmente parado por 8,3 s (163,8–172,1). Vale considerar um `movimento` leve.
- **Plano 39** repete o close `EST1530` do plano 19, e não `EST1827`, como a primeira revisão sugeria. Aceitável.
- **Plano 62:** os primeiros ≤ 0,3 s ainda mostram o interior de outro carro (fonte 1207,0) antes do SUV.
- **Plano 64** (T2@149,5, 272,0–274,8): mostra uma garagem/oficina com faíscas (trailer, com selo) logo antes de "não achei nenhuma oficina por dentro". O efeito é menor que o do antigo A8; fica a critério.
- **Plano 3:** o card 18:12 cobre a lanterna esquerda e parte da tampa. O conteúdo do porta-malas aparece à direita. A entrada tem um zoom de cerca de 0,3 s, que é a transição padrão.
- **Legendas:** "camarim. Minuto dezessete e cinquenta: um" junta o fim de uma frase com o início da seguinte (163,0–165,5). É aceitável.

## Conferido e OK (em movimento, nas amostras)

- **Gancho (0–2,4):** a voz e a legenda "Tem um streamer nesse porta-malas." estão no quadro 0, sem vinheta.
- **A6 (plano 3):** still 18:12 de 10,72 a 15,9. O card entra em 10,9 e sai por completo em cerca de 13,3, sem salto para trás.
- **B1:**
  - Plano 18: o card "15:30 • 4 ESTRELAS" entra em 84,5 e sai por completo em 86,2, antes do corte de 86,5.
  - Plano 19: close `EST1530` com 4 estrelas e 4 ícones nítidos, sob "quatro estrelas, quatro bolinhas".
  - Plano 20 (A1): começa limpo no sedã, sem perua nem scooter.
  - Plano 21: a Lucia de bandana aparece em 97,5–98,0.
  - Plano 22: `ICO1556` com 4 ícones grandes e o carro legível. O card "15:56 • COM O CARRO" entra em 98,5 e sai por completo em 100,5.
- **B3 (planos 35–36):** o card CAMARIM não tem minuto e sai em 163,6. O card 17:50 entra em 164,0, junto com "dezessete e cinquenta" (163,86), e sai em cerca de 167,3.
- **B2:**
  - Card SENTINEL em 200,3.
  - `PLACA0828` com "HRP RB9" legível e o card entre 206,8 e 208,4.
  - `PLACA1841` com a placa iluminada "HRP RB9" legível à noite. O card entra em 212,2 e sai em 213,6, antes do corte de 213,8.
  - O card do plano 49 entra limpo.
- **A3:**
  - Plano 58 em T1@70,4, sem assalto.
  - Plano 60 com as motos limpas em EXT@1114,9–1119,1. O card "18:35 • LAP 1/2" fica de 260,0 a cerca de 263,2, e o HUD LAP/11/12 continua livre no canto inferior direito.
  - Plano 61: o T2 termina claro, sem o quadro escuro.
- **Selos** "TRAILER 1" e "TRAILER 2" visíveis no canto superior esquerdo dos planos 58, 59 e 61.
- **Fechamento (81–83):**
  - Card AMANHÃ entre 361,3 e 363,8.
  - Geladeira com bilhetes visível sob "geladeira da Lucia".
  - HOLD HANDS R2 visível.
  - Sem logo nem data no último plano.
- **Story** (corrigido, sem considerar B1): trecho contínuo de 360,70 a 377,70. O áudio começa a −55 dB, com voz em 0,16 s, e termina a −64 dB. Os cards entram e saem por completo. A legenda fica abaixo do miolo e não cobre o HUD.
- **Emendas de áudio do reel (RMS):**
  - Em 50,06: −65 dB → −52 dB (piso do 2º trecho), sem estalo, e "Então" (onset em cerca de 50,3 na fonte) ficou fora.
  - Fim em 56,23: −56 a −59 dB nos últimos 0,1 s.
- **QA das amostras:** 0 intervalos pretos em todas.
  - LUFS do longo: −16,8 / −16,7 / −17,2 / −15,9 / −17,0 / −17,6.
  - Reel: −16,8. Story: −17,6.
  - Picos entre −1,4 e −1,5 dBFS.
  - Quadros esperados = quadros obtidos.

## Não verificado em movimento (só pela folha do pré-voo)

- **Longo planos 23–27:** "o ícone do carro some" (`ICO1557`) com o card de 2,0 s, a roda de armas, o Burrito (`CR_burrito_1612`, emblema legível no still) e o card dele. A amostra 86–100 termina em 100,6. **Condição para o 4K:** reamostrar 98–116.
- **Longo planos 51–56:** a ordem SLIM JIM do A7, o T1 25–28,9 do A4, 17:42 e 20:21.
- **Longo planos 67–73:** os selos ULTIMATE EDITION e o plano 72 (EXT 13:26, interior do carro, sem oficina), que é o A8.
- **Reel:** a emenda visual de 50,06, o plano 12 e o fechamento sem CTA. Só existe amostra de 0–14. Reamostrar 44–56,23 depois de B1, A4 e A5.
- **`_vertical`:** nenhuma amostra. Ver B1.
- **Escuta:** não ouço áudio. A escuta humana pendente listada no PROGRESSO continua pendente ("racha ilegal" 267,4, Sentinel, Burrito etc.).

## Ordem sugerida

1. Corrigir B1: `--hwaccel nenhum` e apagar os clipes de vídeo em cache das peças verticais.
2. Aplicar A1–A5 nos `episodio.json` (longo, `_previa`, `_vertical` e reel).
3. Pré-voo dos planos alterados.
4. Reamostrar: longo 98–116 e 266–272; reel 0–14 e 44–56,23; story 0–17. Conferir um quadro de cada plano de vídeo vertical.
5. Segunda olhada só nesses trechos. Depois, 4K.
