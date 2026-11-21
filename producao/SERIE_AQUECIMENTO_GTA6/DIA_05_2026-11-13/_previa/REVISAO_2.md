# Revisão 2 (independente): prévia 960x540 do DIA 05

Revisor independente, somente leitura. Data: 12/11/2026.
Objeto: `_previa/exportacoes/Pixel_Procurado_DIA05_Previa_V2.mp4`. São 370,267 s de vídeo e 11108 quadros; o áudio tem 370,260 s.
Numeração dos planos: **1-based, na ordem atual** de `formatos.longo.planos` (112 planos). Como foi inserido o close HUDZ, o antigo "plano 3 (10–13,5 s)" passou a ser o **plano 4** (`HUD`).
Evidências próprias ficam em `scratchpad\r2\` (sessão do revisor):
- `crops.png` e `fb\boundaries.png`: selo GTA V;
- `fl\A.png` e `fl\B.png`: corte a corte em 236–239 s;
- `p108\P.png` e `end\E.png`: planos 108 e 111;
- `src\SRC.png`: fonte EXT 1066–1078;
- `jl\JL.png`: as 13 imagens oficiais da dupla;
- `ex\exact_*.png`: quadros exatos.

**Veredito: ainda NÃO ir para o 4K.** Nada é grave na montagem. Mas há 1 item da lista reprovado (5, legenda final), um resto da 1ª revisão (menu desfocado, plano 108/111) e 2 cards cujo texto não bate com a imagem. Tudo se corrige no JSON ou na legenda. Depois disso, basta revalidar os trechos afetados, sem nova prévia completa, e o 4K está liberado. Há um ponto de texto falado (JL02, "dois mascarados") que fica para decisão editorial (correção 6).

## Itens 1–9

| # | Resultado | Timecode / evidência | Observação |
|---|---|---|---|
| 1 | **APROVADO** | 0–2,66 s (plano 1, HUDZ). `revisao/quadro_0.5s.png`, `quadro_1.5s.png`, folha 01. freezedetect: imóvel de 0 a 2,66 s (intencional, `movimento: fixo`) | Close fixo. "HURRY ◯" e "LUCIA L2" ficam inteiros dentro do quadro, com a elipse amarela (borda direita em x≈955/960). A fala "Esse botão não troca de personagem" começa no quadro 0 sobre o close, e a legenda não encosta no HUD. De 2,66 a 5,92 s (plano 2, EXT@426), "Olha o canto direito da tela no minuto sete" passa sobre o HUD real "LUCIA L2" no canto (`quadro_3s.png`). |
| 2 | **APROVADO c/ ressalva** | 10,18–13,48 s (plano 4, HUD). `quadro_11s/12s/13s.png` idênticos (fixo, freeze 10,4–12,9 intencional) | Coerente: "apressar, na bolinha, e Lucia, no L dois" sobre o HUD com a elipse, mais o card LUCIA [L2]. O pan sumiu. Ressalva leve: o HUD fica pequeno, com cerca de 70x50 px a 540p, e a elipse é cortada pela borda direita do quadro. Opcional, não bloqueia. |
| 3 | **APROVADO** | (a) 236–246 s: `fl\A.png` e `fl\B.png`, quadro a quadro em 236,5–237,5 e 238,75–239,4; `revisao/quadro_236s/241s/246s.png`. (b) 149,7–207,7 s: folhas 08–11 | (a) Não há flash nem quadro estourado nos cortes de 236,6 e 238,88. Imagem e fala batem: "Tem gente pra todo lado" sobre o segurança e "a Lucia aparece de vestido preto, abaixada…" sobre a Lucia digitando (241 s). Residual BAIXA: de 243,9 a 245,4 s, "abaixada perto de uma mesa iluminada" cai sobre o segurança e o LMSG. (b) O parêntese do pedido (anilha/supino/foto oficial) corresponde a 150–207 s, não a 236–246, e também confere: anilha verde GAINZ a 2:30–2:37, L2/R2 a 2:38–2:45 e foto oficial L01 (saco de pancada) a 3:23–3:27. |
| 4 | **APROVADO** | 265,58–270,74 s (planos 82–83). Folha 14 (4:25–4:30) | "…abrir a porta da escada de incêndio e levar um tombo no minuto 24:22": a Lucia abre a porta (4:28–4:29) e o segurança a agarra (4:30). A imagem não contradiz a fala. A queda em si aparece depois, no plano 93 (4:56–4:57). O card "24:22 / Porta da escada de incêndio" é verdadeiro: a fonte EXT 1461–1462 é 24:21–24:22. O card não afirma nada falso. |
| 5 | **REPROVADO** (leve) | 367,9–370,26 s (plano 112, T1@85, `legenda_alta`). `revisao/quadro_368s.png`, `quadro_370s.png` | Sem preto: blackdetect não acusou nada. O fim não tem corte seco: o logo fica parado até o último quadro, e o áudio decai a −64 dB em 370,1 e a −71 dB em 370,2 (volumedetect), depois do fim da última palavra em 370,02. O vídeo e o áudio terminam com 7 ms de diferença. **Falha:** a legenda subiu e saiu de cima de "NOVEMBER 19, 2026", mas agora fica **sobre a arte do logo**, logo abaixo de "auto" e dentro do "VI". Continua legível, mas está sobreposta. A faixa preta superior (y < 95 px a 540p) está livre. |
| 6 | **APROVADO** (sincronia medida em ±1 quadro) | 21 quadros GTA V (`gv_*.png`, `crops.png`) e as 10 fronteiras quadro a quadro (`fb\boundaries.png`) | O selo "GTA V" aparece em todos os planos GTAV (18–26, 60, 61, 84, 89, 97) e não aparece em GTA VI. Diferença de 1 quadro (33 ms, imperceptível): o selo entra 1 quadro atrasado em 52,56 e 270,74. Em 273,04 e 315,74, fica 1 quadro sobre a imagem GTA VI seguinte (`fb\b5_3.png`). Personagens corretos: Trevor de cueca em 66,5–70,5 s, Trevor com o Ron em 70,5–72,7 s, e picape Bodhi do Trevor com 5 estrelas em 312,9–315,7 s (`gv_313.5.png`). O Franklin não aparece mais sob "Trevor". Para informação: os cards "GTA V" (linha de detalhe) não são mais desenhados; aparece só o selo. |
| 7 | **APROVADO c/ observações** | Varredura de sobreposição de janelas no `episodio.json`, mais folhas | As 3 janelas aceitas conferem. Há sobreposição exata de fonte apenas em stills. **BENCH** (still do supino) aparece 3 vezes: planos 52 (153–157,6), 56 (170,9–175,3) e 63 (194,3–197,5). Somado ao vídeo do mesmo enquadramento nos planos 51 e 55, o plano de cima do supino ocupa cerca de 23 s. O nº 9 da 1ª revisão foi aplicado só em parte: o plano 56 continua still. MÉDIA-BAIXA. **MSG** se repete nos planos 17 (49 s) e 100 (321 s). Funciona como retomada (callback). BAIXA, aceitável. **Menu desfocado** de EXT ≈1070,2–1071,5 nos planos 108 e 111: ver item 9. Não há outras repetições relevantes. As vizinhanças com folga menor que 0,25 s são continuações, não repetições. |
| 8 | **APROVADO c/ 2 correções de texto** | Folhas 01–19, `quadro_12s.png`, `quadro_246s.png` | Todos os cards entram na âncora ou pouco antes, ficam no canto inferior esquerdo e saem por completo. Nenhum fica preso. Os números conferem com a fala: 14:42, 15:20, 15:30, 17:20, 24:10, 24:22, 19/11, 13/11, 6 dias, 3 cenas, 2 palavras e 18. Nenhum card cobre a ação. O 17:20 cobre parte da anilha esquerda em 2:30–2:32, mas a direita fica visível. Não bloqueia. **Erros de texto:** (a) Card **14:42**, plano 30, EXT@878 (fonte 14:38): o detalhe diz "Lucia ao volante", mas a imagem é a rua com viaturas. A Lucia só aparece no plano 32 (93,9 s). (b) Card **IMAGEM OFICIAL** (plano 104, JL02, 335,8–341,6 s): diz "dois mascarados", mas na imagem **só o Jason está mascarado**, com balaclava de caveira. O rosto da Lucia está descoberto. A fala diz o mesmo ("dos dois mascarados"). Conferi as 13 imagens JL (`jl\JL.png`): nenhuma mostra os dois mascarados com cofre e dinheiro. |
| 9 | **APROVADO c/ 1 correção** | freezedetect e blackdetect no arquivo inteiro; 19 folhas abertas; quadros exatos | Nenhum trecho preto (blackdetect d=0,1, pix_th=0,08). Todos os congelamentos são intencionais: HUDZ (0–2,66), HUD fixo (10,4–12,9), slate "NOVEMBER 19" da fonte (199,9–202,2) e logo final (367,9–370,27). Fala e legenda alinhadas nas amostras: 0,5, 3, 12, 236, 241, 246, 368 e 370 s, e nas folhas. **Correção:** o **menu desfocado do jogo** (UI do porta-malas) continua aparecendo **duas vezes**. A 1ª vez é em 356,32–356,8 s, no início do plano 108 (EXT@1071.0, `p108\P.png`). A 2ª é em 367,1–367,9 s, no fim do plano 111 (EXT@1069.0), imediatamente antes do logo (`end\E.png`). É o nº 15 da 1ª revisão, ainda sem correção. Na fonte, o desfoque vai de cerca de 1070,2 a 1071,5 (`src\SRC.png`). Residuais opcionais, já conhecidos: porta de elevador escura (5:24, cerca de 0,6 s), trechos muito escuros (3:43–3:51), 3 cortes do T1 sob "Casal normal…" (2:13–2:15) e cerca de 0,9 s de BMX antes do Trevor sob "Às vezes você chegava no Trevor" (1:05–1:06). |

### Observação do operador: planos 77 e 108 e os 3 quadros

- **Não há divergência real.** Os arquivos de clipe são numerados a partir de 0 (`00.mp4` = plano 1). Contagem com ffprobe:
  - `76.mp4` = plano 77: **109** quadros (3,62 s), igual ao log;
  - `107.mp4` = plano 108: **86** quadros (2,88 s), igual ao log;
  - o operador comparou `77.mp4`, que é o plano 78 (71 quadros = 2,36 s), e `108.mp4`, que é o plano 109 (154 quadros = 5,14 s). As duas contagens também estão corretas.
- **Nos planos 77 (252,22–255,84) e 108 (356,32–359,2):** nenhum congelamento (freezedetect), corte curto ou sobra. Plano 77: close da Lucia por cerca de 0,5 s e depois o segurança com o walkie-talkie (`ex\exact_252.3.png`). Plano 108: o único defeito é o menu desfocado no início (item 9).
- **11108 vs 11111 quadros:** a 1ª prévia tinha 370,37 s. A atual tem 370,267 s, para um áudio de 370,260 s. A diferença de 3 quadros é o fim alinhado ao áudio. Não há dessincronia: a legenda "até amanhã." aparece em 369,68–370,02, como no alinhamento.

## Correções objetivas (antes do 4K)

1. **Plano 112 (367,9–370,26), legenda final:** subir a legenda para a faixa preta superior, acima do logo, com y entre 30 e 80 px a 540p (\an8 ou MarginV equivalente em 4K). Nada mais muda. Revalidar só esses 2,4 s.
2. **Plano 108 (356,32), EXT@1071.0 → `inicio` 1071.6** (ou 1071.7, por folga), para eliminar o menu desfocado do início. Verificado: em 1071,6 a imagem já está limpa (carro vermelho na oficina).
3. **Plano 111 (365,9–367,9), EXT@1069.0 → `inicio` 1076.4:** Lucia de amarelo andando em frente à "WE DO REPAIRS". Verificado limpo em 1076,4, 1077,0, 1077,5, 1078,0 e 1078,4. Alternativa: manter 1069.0 e terminar o plano antes de 1070,2 da fonte.
4. **Plano 30, card 14:42:** trocar o detalhe "Lucia ao volante" por "Depois do tiroteio na rua". A outra opção é mover o card para o plano 32 (EXT@882, Lucia ao volante).
5. **Plano 104, card IMAGEM OFICIAL:** trocar o detalhe "Cofre, dinheiro voando, dois mascarados" por "Cofre, dinheiro voando, dois armados", ou por "Cofre e dinheiro voando".
6. **Fala do parágrafo 35 (decisão editorial, cerca de 339–341 s):** "dos dois mascarados com dinheiro voando" é falso para a JL02. Sugestão de menor custo: "dos dois **armados** com dinheiro voando", uma sílaba a menos. Exige regerar só essa frase e realinhar do ponto em diante. Se não houver TTS agora, aplicar ao menos a correção 5 e registrar a imprecisão.
7. (Opcional) **Plano 56 (170,86–175,26), BENCH:** trocar por vídeo para reduzir a repetição do plano de cima do supino. Exemplo: continuação do supino da praia (T2) ou outro trecho da academia. Esta janela **não foi verificada**.

Depois de 1–5 (e de 6, se aplicado): rodar `prevoo_v2.py` e conferir só 335–342 s, 356–360 s e 365–370,27 s. O 4K fica liberado.

## O que NÃO pude verificar

- **Áudio audível:** não ouvi nada. Medi só o nível no fim (volumedetect) e a duração. Timbre, cortes de respiração, clipping fora do fim e loudness integrado (ebur128) não foram verificados.
- Nitidez e legibilidade em 4K: o HUD do plano 4 em celular e o texto miúdo dos cards.
- A janela alternativa do plano 56 (correção 7).
- O trecho de EXT entre 1071,6 e 1074,5 da correção 2 foi visto só até 1073,9. O restante é continuação da mesma tomada; conferir no pré-voo.
- Reel, Story e vertical: fora do escopo desta revisão.
