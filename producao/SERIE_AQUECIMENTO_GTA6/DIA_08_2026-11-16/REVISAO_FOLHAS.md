# Revisão independente das folhas do pré-voo — Dia 08 (16/11/2026)

Revisor: subagente Opus 5.5. Não alterei nenhum arquivo do episódio. Só criei este relatório.

Material visto: 6 folhas do longo (`montagem/prevoo`), 6 do vertical (`_vertical/montagem/prevoo`), 1 do Reel e 1 do Story. Conferi as cartelas em 4K (`montagem/referencias/C*.jpg`, recortes ampliados), `01_NARRACAO.txt`, os 4 `episodio.json` e `FONTES.md`. Para casar fala e imagem, usei `audio/palavras_alinhadas.json`, `_reel/audio/palavras.json` e `_story/audio/palavras.json`. As folhas não imprimem a fala, então cruzei o corte de cada plano com o alinhamento.

## Veredito

**Nenhum bloqueio grave de imagem.** Nenhum quadro faz comparação base x Pro, mostra split-screen ou traz número de fps, resolução ou PSSR sobre o gameplay. Os 20 planos de gameplay do longo têm o card `ILUSTRAÇÃO | não mostra fps`. Também não há conselho de compra, rumor apresentado como fato nem personagem identificado por figurino. Não encontrei erro de português nas cartelas.

Encontrei **1 bloqueio de texto, de correção trivial** (C06) e vários ajustes. O vertical **não pôde ser verificado visualmente** (ver seção 3).

## 1. Longo (404,09 s) — achados

| # | Plano / tempo | Achado | Severidade | Correção sugerida |
|---|---|---|---|---|
| 1 | P09 · 66,0–79,5 s · `C06_PSSR` | A legenda pequena diz "mais detalhe e estabilidade (descrição da Sony)". `FONTES.md` (F5/F6) só traz "analyzes game images pixel by pixel and uses AI to upscale them" e "AI-driven upscaling". "Estabilidade" e "mais detalhe" não estão nas fontes. O texto também encosta na margem direita (cerca de 96% da largura). | **bloqueia** | Refazer `C06_PSSR.jpg` com "aumenta a resolução com IA (descrição da Sony)", fiel ao F5 e à fala. Puxar o bloco de texto para dentro da área segura. |
| 2 | P29 · 237,3–259,0 s · `C14_XBOX` | A citação "MOST AFFORDABLE WAY TO PLAY NATIVELY" corta "GTA VI" de dentro das aspas sem reticências. A fonte diz "the most affordable way to play GTA VI natively". | ajuste | Usar "MOST AFFORDABLE WAY TO PLAY GTA VI NATIVELY" ou "…TO PLAY […] NATIVELY". |
| 3 | P02→P03 · 18,7–21,7 s | P03 (`EXT@760`, 1,1 s) entra exatamente em "Nem pro Pro." Um flash de gameplay na palavra "Pro" pode ser lido como "imagem do Pro", e o card de ilustração não dá tempo de leitura em 1,1 s. A `C02_SEM60` já diz "nem pro PS5 Pro". | ajuste | Remover P03 e estender `C02_SEM60` até 21,68. |
| 4 | P32→P33 · 282,3–299,2 s | A fala "E o Remote Play… suporte total, no PlayStation e no Xbox" cai em P32 (`S1213`). A cartela `C16_REMOTE` só entra em 290,1 s, quando a fala já passou para "É isso que o texto oficial diz…". A cartela chega atrasada. | ajuste | Trocar a ordem: `C16_REMOTE` em 282,30–290,09 e `S1213` (com card) em 290,09–299,20. Outra saída é começar C16 em 282,30 e reduzir S1213. |
| 5 | P01 · 0–18,7 s · `C01_META` | São 18,7 s de cartela parada. O gancho dos 3 s funciona, mas a partir de "Ontem eu prometi…" (cerca de 3,4 s) não há variação visual por 15 s. | ajuste | Cortar C01 em cerca de 3,4 s. Pôr gameplay com card (por exemplo `EXT@1215` ou `VC10`) em "Ontem eu prometi… sem torcida". Voltar a `C01_META` em "Resposta curta: no dia dez de novembro…" (cerca de 11–12 s pelo alinhamento). |
| 6 | P50 · 383,5–399,1 s · `C21_AMANHA` | 15,5 s de cartela parada no fecho. | ajuste | Dividir: cartela por cerca de 5 s, depois `VC08` (noite) com card até 399,08, e manter P51/P52. |
| 7 | Repetição — trecho diurno do BMW na via expressa (`EXT` 760–790) | O mesmo trecho aparece em P03 (760), P06 (772–779), P10 (`S780`), P16 (780–788), P18 (`S788`), P20 (`S763`), P48 (`S770`) e P49 (`S788`). São 8 planos. `S788` repete em P18 e P49, e os stills `S780` e `S788` são o mesmo plano de P16. | ajuste | Trocar ao menos P18 e P49 por mídia diferente do acervo. Trocar também P10 ou P20. Sugestões: `VC10` (já usada só uma vez), `EXT` 980–990 (diurno de van) ou outro trecho diurno do catálogo. Manter cada um com o card ILUSTRAÇÃO. |
| 8 | Repetição — noite/pista molhada (`EXT` 1200–1217) | P12 (1200), P14 (1207–1210), P31 (`S1210`, 13,5 s parado) e P32 (`S1213`). P31 mostra o mesmo quadro visto em P14. | ajuste | Em P31, usar o vídeo `EXT` a partir de 1213 ou outra cena noturna, em vez do still de 13,5 s. |
| 9 | Repetição — `VC11` (P05 e P27, 13,0 s) e `VC08` (P22 e P51) | P27 repete o still do helicóptero por 13 s. | ajuste | Em P27, usar outra mídia (de preferência vídeo). O `VC08` duplo é aceitável. |
| 10 | P10 · 79,5–86,7 s · `S780` | O sol estourado com flare entra durante "aplicativo que melhora foto antiga". Com o card, não sugere PSSR. | ok | — |
| 11 | P16 · 122,6–130,8 s | "a imagem que tá passando aqui é ilustração… Olhar Estendido" sobre `EXT`: coerente. | ok | — |
| 12 | Demais cartelas (C01–C05, C07–C13B, C15, C17_0–6, C18, C18B, C19_0–3, C22) | Batem com a fala no instante e com F1–F9 e R1/R1b. Os destaques progressivos de C17 e C19 acompanham cada item falado. | ok | — |
| 13 | Legibilidade (longo) | Títulos e linhas principais estão legíveis. As linhas cinza pequenas (por exemplo "texto original do comunicado" e "(blog PlayStation: também não)") têm cerca de 60–70 px em 4K. Legíveis na TV, mas no limite. | ok | — |

Personagens: P12 e P14 mostram pessoas na noite. Não há rótulo ou nome sobre elas, e a fala não as identifica. **ok.**

## 2. Reel (65,34 s; palavras 1–176, termina em "repetiu a dupla.")

| Plano | Achado | Severidade | Correção |
|---|---|---|---|
| P01 · 0–18,7 s | O mesmo plano parado de 18,7 s do longo (achado 5). Em Reel isso pesa mais: a retenção cai depois do gancho. | ajuste | Aplicar a mesma divisão do achado 5. |
| P03 · 20,6–21,7 s | Mesmo flash de 1,1 s em "Nem pro Pro" (achado 3). | ajuste | Mesma correção. |
| Início | A voz começa em 0,0 s ("Meta oficial: trinta quadros por segundo.") sobre a cartela-evidência. Início limpo. | ok | — |
| Fim | A última palavra termina em 64,94 s e o arquivo, em 65,34 s (cauda de 0,4 s, limpa). Do ponto de vista editorial, o Reel termina numa informação de apoio ("o blog da PlayStation repetiu a dupla"), sem fecho nem chamada para o longo. | ajuste (editorial) | Opcional: um card final de 1–2 s ("Vídeo completo no canal") ou fechar o corte em "Esse só no Pro é palavra deles, não minha." (cerca de 62,2 s), que é a frase mais forte. A estrutura de palavras 0–175 foi pedida pela coordenação, então a decisão fica com o coordenador. |
| P04–P08 | Coerentes com a fala, card ILUSTRAÇÃO presente nos gameplays e sem imagem de comparação. | ok | — |

## 3. Vertical (longo completo em 1080x1920) — NÃO VERIFICÁVEL PELAS FOLHAS

- As 6 folhas de `_vertical/montagem/prevoo` são **byte a byte idênticas** às do longo (md5 conferido nas 6). O pré-voo desenha só os quadros-fonte em 16:9. Por isso **não mostra o enquadramento 9:16, o fundo desfocado, o card a 780 px nem possível verde**. Os itens (6) do pedido não puderam ser verificados visualmente.
- Pelo código (`automacao/pipeline/produzir_v2.py`, linhas 191–242): miolo 16:9 de 1080x608 em y=425 sobre fundo desfocado. Card de 780 px em (150, 1060), abaixo do miolo, então não cobre a imagem. O `format=yuv420p` contra o verde do d3d11va está presente, mas isso é inferência pelo código, não verificação.
- **Risco objetivo de legibilidade (ajuste):** as cartelas 3840x2160 entram inteiras no miolo de 1080 px, em escala de cerca de 0,28. As linhas cinza pequenas caem para cerca de 18–20 px de altura num quadro de 1920 px. Os itens apagados de C17/C19 e o subtítulo de C14 também ficam pequenos. No celular, isso fica no limite da leitura. Texto cortado não há, porque a cartela é escalada inteira, sem recorte.
  - Correção sugerida: estender a ferramenta com uma variante de cartela 9:16 (ou `enquadramento: "conter"` com uma versão vertical da cartela e fonte maior). Pelo menos C06, C07, C14, C15, C16, C17_* e C19_* devem ganhar versão vertical. Depois, rodar `produzir_v2.py --amostra` no vertical e extrair quadros de 2–3 planos de gameplay e 2 de cartela para conferir o fundo desfocado e a ausência de verde.

## 4. Story (20,55 s)

| Plano | Achado | Severidade | Correção |
|---|---|---|---|
| Início | A primeira palavra ("Amanhã") começa em 0,70 s, ou seja, 0,7 s de silêncio no começo. | ajuste | Aparar o áudio e a timeline em cerca de 0,6 s para a voz entrar no primeiro quadro. |
| P01 · 0–15,5 s · `C21_AMANHA` | Cartela parada em 75% do Story. | ajuste | Dividir como no achado 6 (cartela por cerca de 5 s, depois `VC08` ou outra cena noturna com card). |
| Conteúdo | O Story divulga o episódio de amanhã (vida noturna, 17/11), não o de hoje. É coerente consigo mesmo, mas não leva o público ao vídeo publicado hoje. | ajuste (editorial) | Confirmar com a coordenação se a intenção é essa. Se o Story deve puxar para o Dia 8, trocar o texto por um gancho do Dia 8. |
| Fim | "faltam só três dias." termina em 19,74 s. O arquivo vai até 20,55 s, com `C22_QUINTA` ("QUINTA, 19/11 · FALTAM 3 DIAS", correto para 16/11). Fim limpo. | ok | — |

## 5. Não verificado

- O enquadramento vertical real, o fundo desfocado e o verde (seção 3): as folhas não renderizam o 9:16.
- A animação de entrada e saída dos cards e o tempo de leitura em cena: as folhas mostram só os quadros-fonte, não a camada de cards.
- Legendas `.ass`/`.srt` sobre a imagem: não aparecem nas folhas.
- Conteúdo da cartela `C21_AMANHA` (pauta de 17/11: "boates, ID check e infiltração de luxo"): é pauta do próximo episódio e não está no `FONTES.md` do Dia 8. Não avaliei a veracidade.

## Lista de correções (ordem sugerida)

1. **[bloqueia]** C06_PSSR: trocar "mais detalhe e estabilidade" por texto fiel ao F5 ("aumenta a resolução com IA") e afastar da margem direita.
2. [ajuste] C14_XBOX: corrigir a citação ("…PLAY GTA VI NATIVELY").
3. [ajuste] Longo e Reel: remover P03 (flash em "Nem pro Pro") e estender C02 até 21,68.
4. [ajuste] Longo: pôr C16_REMOTE em 282,30 (na fala do Remote Play) e o gameplay depois.
5. [ajuste] Longo e Reel: dividir o P01 de 18,7 s com gameplay ilustrativo no meio.
6. [ajuste] Longo e Story: dividir C21_AMANHA (15,5 s); no Story, aparar 0,7 s de silêncio inicial.
7. [ajuste] Longo: reduzir repetição do trecho EXT 760–790 (P18/P49 `S788`, P10 ou P20), de P31 (`S1210` repete P14) e de P27 (`VC11` repetido, 13 s parado).
8. [ajuste] Vertical: cartelas em versão 9:16 ou com fonte maior, e conferência por `--amostra` com extração de quadros (fundo desfocado e verde).
9. [ajuste editorial, decisão do coordenador] Fecho do Reel e propósito do Story (divulga o Dia 9, não o Dia 8).
