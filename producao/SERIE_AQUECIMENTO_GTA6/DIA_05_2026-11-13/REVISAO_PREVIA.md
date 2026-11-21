# Revisão independente: prévia 960x540 do DIA 05 (Lucia e Jason)

Revisor independente (não participou da direção). Data: 12/11/2026.
Objeto: `_previa/exportacoes/Pixel_Procurado_DIA05_Previa_V2.mp4` (370,37 s), `episodio.json`, `audio/palavras_alinhadas.json`, `01_NARRACAO.txt`, folhas do reel e do story.
Numeração dos planos: **1-based**, na ordem de `formatos.longo.planos` (plano 80 = `EXT@1460.9`, como na pendência).

**Veredito: NÃO renderizar o 4K ainda.** Há 1 erro factual (plano 80), 1 erro de personagem do GTA V (plano 94), a evidência da abertura cortada pelo movimento (plano 3) e o rótulo "GTA V" ausente em boa parte dos planos de GTA V. Todos se corrigem com mudança de corte ou de ferramenta, exceto o plano 80, que exige trocar 3 palavras da fala.

## 0. Aviso sobre as folhas de revisão fornecidas

As folhas `_previa/revisao/folha_NN_*.png` **não cobrem o vídeo**. O nome da folha não bate com o conteúdo:
- folha_01 começa em 13,3 s, então 0–13,3 s não aparece;
- falta 38,3–53,3 s, e também 2:18–2:33 e 2:51–3:31;
- folha_09 e folha_10 são idênticas.

Ao reproduzir o problema, vi a causa: `fps → tile → image2` sem `-fps_mode passthrough` faz o muxer duplicar ou descartar quadros de saída. Use `-fps_mode passthrough` (ou `-vsync 0`) no script que gera essas folhas. Por isso montei folhas próprias, com 1 quadro por segundo e o vídeo inteiro, mais quadros a 10 fps nas transições suspeitas e nos trechos de origem. A pendência (c) era sintoma desse bug: os planos 1–10 foram conferidos nas folhas novas.

## 1. Problemas (do mais grave ao menos grave)

| # | Sev. | Plano / TC | Evidência | Problema | Correção objetiva |
|---|---|---|---|---|---|
| 1 | **ALTA** | 80 (267,9–270,84), fala "derrubar um homem" em 267,66–268,4 | quadros da fonte EXT 1455–1476,5 a 0,5 s | **A fala é factualmente oposta ao vídeo.** Lucia abre a porta da escada (1461–1462,5). Em 1463, um segurança de branco **a agarra**, joga contra a parede (1464) e **a arremessa escada abaixo** (1465–1466). Ela fica caída no chão (1469,5–1472) enquanto ele desce. Nenhuma janela da fonte mostra Lucia derrubando alguém. Trocar o corte não resolve, porque a afirmação continua falsa. | Mudar o texto (último recurso, mas aqui é inevitável). Trocar só 3 palavras: "e **derrubar um homem**" → "e **levar um tombo**" (mesmo número de sílabas, cerca de 0,7 s). Gerar só essa frase ("…até abrir a porta da escada de incêndio e levar um tombo no minuto vinte e quatro e vinte e dois.") e encaixar no lugar de 265,58–270,84. Se a duração mudar menos de 0,15 s, nada se desloca de forma perceptível. Se o encaixe ficar audível, regerar o parágrafo 27 inteiro e realinhar só daí em diante. Imagem para o plano 80: manter EXT@1460.9 (1460,9–1463,84), que já mostra a porta e o início da agressão e passa a casar com "levar um tombo". Fallback sem regerar voz: EXT@1458.6 (só Lucia andando até a porta, sem a briga). Isso esconde a contradição, mas a fala continua falsa; não recomendo. |
| 2 | **ALTA** | 94 (313,0–315,84) "O Trevor era o caos que você visitava" | quadro GTAV@192 (`gv_192.0.png`) | Quem aparece é o **Franklin** (camisa azul sobre manga branca). A roda de troca no canto mostra os retratos de Michael e Trevor, ou seja, o personagem ativo é o Franklin. | Trocar para `GTAV@148.0` (148,0–150,84): a picape Bodhi do Trevor fugindo da polícia com 5 estrelas na terra de Sandy Shores. Verificado: sem preto, ação contínua. Alternativa com o Trevor visível: `GTAV@183.0` (veja o nº 4). |
| 3 | **ALTA** | 3 (10,18–13,48) HUD, e abertura 0–3 s | `card_003_…LUCIA_L2.png`, quadros 10,1–11,3 s | O still `hud_0706.jpg` passa pelo Ken Burns de 12% em `produzir_v2.py` (índice par = pan saindo do canto inferior direito). **O anel amarelo e o "LUCIA L2" saem do quadro** em cerca de 0,5 s: o card fala do botão e o botão não está na tela. Na abertura (plano 1, EXT@426), o "LUCIA L2" ocupa cerca de 30x15 px no canto inferior direito, num quadro escuro. A fala "Esse botão não troca de personagem" começa no quadro 0, mas a evidência não é legível no celular nos 3 primeiros segundos. | (a) Estender a ferramenta: opção por plano, por exemplo `"movimento": "fixo"` ou `"foco": [x, y]`, para stills que não podem sofrer pan. Também serve para BENCHZ, MSG e LMSG. (b) Na abertura, plano 1 de 0–2,66 s (até "Olha") com um recorte do HUD em close (`hud_0706` recortado em volta de x≈3400–3840 e y≈1850–2160 da 4K, com folga), sem movimento. Depois volta EXT@426 a partir de 2,66 s ("Olha o canto direito da tela…"), com o restante do corte. |
| 4 | **ALTA** | Todos os planos GTAV (17–25, 57–58, 81, 86, 94) | folhas 1 fps em 52,5; 70,5–72,7; 75,5–76,5; 78,5; 82,5; 186–187; 315,7 | **O rótulo "GTA V" só existe dentro do card, e o card sai.** Cerca de 40–50% do tempo de tela com GTA V fica sem rótulo. Exemplos: 72,5 (carro laranja), 75,5–76,5 (golpe de macacão vermelho), 78,5 (família), 82,5 (dinheiro), 186–187 (tênis e mergulho), 315,7. `prevoo_v2.py` só confere se o título contém "GTA V", não se o rótulo está visível em todo o plano. | Estender `produzir_v2.py`: `rotulos_obrigatorios` gera um selo pequeno e persistente "GTA V" (canto superior esquerdo) durante todo o plano dessa mídia, independente do card. Fazer `prevoo_v2.py` validar isso. Alternativa sem mexer na ferramenta: card com duração igual à do plano para mídia GTAV. |
| 5 | MÉDIA | 22 (70,5–72,74) "Trevor no meio do nada" | 70,5–72,5; GTAV 266–268 | Mostra uma Ferrari vermelha em rodovia e depois um carro laranja em primeira pessoa. Não é o Trevor nem o "meio do mato". | `GTAV@183.0` (183,0–185,24): Trevor (camiseta clara) com o Ron no trailer em Sandy Shores, deserto ao fundo. Verificado (`gv_183.5.png`), sem preto; a troca para o close do Ron acontece em cerca de 185,2. |
| 6 | MÉDIA | 72 (238,88–245,42) "…a câmera desce pra festa, e a Lucia aparece de vestido preto, abaixada perto de uma mesa iluminada" | 4:00,5–4:03,5 | Nesse trecho aparece o **segurança careca armado**. A Lucia abaixada na mesa já tinha aparecido em 3:57 (plano 71, "Tem gente pra todo lado") e só volta em 4:04,5. | Inverter: plano 71 = `EXT@1436.2` (2,28 s, os seguranças = "gente pra todo lado"). Plano 72 = `EXT@1433.6` (1433,6–1440,14: Lucia abaixada digitando, já sem o flash do nº 7, seguida dos seguranças). Ou, no mínimo, aplicar só o nº 7. |
| 7 | MÉDIA | 71 (236,6) | quadros 236,4–237,2 a 10 fps | Corte duro para um quadro estourado (branco/azul) da transição do jogo, por cerca de 0,4 s (236,6–237,0). | `inicio` 1433.0 → **1433.6** (estável a partir de 237,2 da prévia = 1433,6 da fonte). Para não repetir no plano 72: 1435.3 → 1435.9, e no plano 74: 1441.9 → 1442.5. Se adotar o nº 6, ele já resolve isso. **O mesmo flash está no REEL plano 16 (EXT@1433.0)**: veja a seção de reel. |
| 8 | MÉDIA | 90 (295,6–297,34) "…e entra no combate" | 4:55,9–4:56,9 | Mostra o **Jason** no escritório, não a Lucia. | `EXT@1463.0` (1463,0–1464,74): Lucia entra na briga com o segurança. Verificado em 1463,0, 1463,5, 1464,0 e 1464,5, sem preto. Fica coerente com a nova fala do nº 1. |
| 9 | MÉDIA | 50, 51, 53, 60, 64 (supino) | 2:33–2:55; 3:15–3:17; 3:28–3:31 | O still do supino (BENCH ×3, BENCHZ ×2) soma cerca de 25 s, com 7,2 s seguidos no plano 53. É repetição e uso de estático onde existe vídeo (EXT 1038,8–1042 é o mesmo supino em movimento). | Plano 53 (168,06–175,26): trocar o BENCH por vídeo. Sugestão: `T2@38.5` estendido (homem no supino da praia) para "minijogo de coordenação" e EXT@1038.8 para "mais cansado que a Lucia". Plano 64: trocar BENCHZ por `EXT@1039.0`. Plano 60 ("CONFIRMADO: só o supino") pode ficar. *Janelas não verificadas além do que já aparece na prévia.* |
| 10 | MÉDIA | 26 (85,88–88,4) "…dividem o apartamento, o carro…" | 1:24,5–1:25,5 | Depois da cozinha com Jason e Lucia (1:23,5), entram um homem de boné amarelo e um bar com outras pessoas. | Encurtar o plano 25 para mostrar só a cozinha. No plano 26, usar um plano dos dois no carro (por exemplo LT@27, já usado no plano 11, que mostra os dois no conversível em 41,5). *Não verifiquei outra janela de T2.* |
| 11 | MÉDIA | Fim (368,0–370,36), T1@85 | `end.png` | A legenda "Já se inscreve nessa porra e até amanhã" fica **em cima** da linha "NOVEMBER 19, 2026" do logo. Ilegível. | Subir a legenda só nesse plano (MarginV maior) ou usar `T1@84.0` se o logo estiver sem a data. Também dá para manter e encurtar a legenda para cima do logo. |
| 12 | BAIXA | 14 (46,5–47,9) "uma na academia" | quadros 46,4–47,9 | Um quadro (46,5) do biplano rosa antes da academia: flash de 1 quadro. | `LT@57.0` → `LT@57.15`. |
| 13 | BAIXA | 89 (292,92–294,5) "Ela dirige a fuga" | 4:52,9 | No primeiro 1 s aparece o contato de óculos no banco de trás. A Lucia só entra em 4:53,9. | `EXT@898.0` → `EXT@899.0` (Lucia ao volante, como em 4:53,9). |
| 14 | BAIXA | 43 (132,6–135,66) "Casal normal briga porque alguém pegou a saída errada" | 2:13,5–2:15,5 | Três cortes do T1 em 3 s: noticiário de engavetamento, foto de fichado do "Florida Joker" e motos. Não há casal. | Manter só o noticiário (T1@63.0 por cerca de 1,2 s) e completar com uma viatura da perseguição. Ou aceitar como piada. |
| 15 | BAIXA | 108 (366,0–368,0) EXT@1069 | 6:07,7 vs 5:56,7 | O menu desfocado do porta-malas aparece duas vezes em 11 s (planos 105 e 108). | Plano 108: usar `EXT@1076.4` (Lucia andando até o carro). |
| 16 | BAIXA | 30/40/45 (EXT 884–892) e 31/32/89 (contato) | 1:35–1:40; 2:04–2:05; 2:18–2:20; 4:52 | Lucia dirigindo no escuro e o contato de óculos voltam 3 vezes. Não são os mesmos segundos da fonte, mas parecem repetidos. | Aceitável; se mexer no nº 13, uma das repetições já cai. |
| 17 | BAIXA | 84 (277,8–279,3) | quadros 4:38,2 e 4:39,2 | Tingimento vermelho e amarelo de cerca de 0,2 s. É efeito de dano/tiro do próprio jogo, não transição. | Aceitar. |
| 18 | BAIXA | 69 (226–231,7) e 99–100 (328–335,9) | 3:43–3:51; 5:29–5:35 | Trechos muito escuros (blackdetect pix_th=0,08 não acusou nada; não é preto). Em 3:46–3:49 o Jason está de pé, não "agachado". | Opcional: clarear (eq) nesses planos no 4K. |
| 19 | BAIXA | 98 (323,48) | 5:23,9–5:24,5 | Cerca de 0,6 s de porta de elevador escura antes do corpo caído, sob "lê. Dez caras, armas automáticas…". | Opcional: `EXT@1445.6` → `EXT@1443.5` (seguranças armados). |

### Pendências que você pediu para julgar

- **(a) plano 80**: veja o nº 1. É erro de fato, não só de corte. A Lucia é quem cai.
- **(b) plano 71**: confirmado, cerca de 0,4 s de quadro estourado. Veja o nº 7.
- **(c) planos 1–10**: o defeito era da folha (seção 0). Na prévia: planos 1–2 OK sem preto, plano 3 com o HUD cortado (nº 3), planos 4–10 coerentes. O beijo do LT (39,5–40,5) sob "jogar com dois protagonistas" é aceitável. O pântano em 42,5 sob "ao mesmo tempo?" é um desvio leve.
- **(d)** Plano 22 é o nº 5. "Rádio" mostrando seguranças (plano 67, 218,9–222,96): aceito. Os seguranças da festa são de fato quem usa rádio (em 4:13 um deles fala num walkie-talkie). O "alerta pelo rádio" sobre eles não contradiz nada; prioridade baixa. **Card "15:30"**: na prévia **está certo**. O card está visível em 113,53, e "quinze e trinta" é dito em 113,66–114,30. Pendência resolvida.

## 2. Cards (cr. 3 e 6)

Conferi a entrada de todos os cards contra a palavra-âncora:

| Card | Entrada | Âncora | Situação |
|---|---|---|---|
| 14:42 | 88,4 | 89,12 | ok |
| 15:20 | 106,4 | 106,5 | ok |
| 15:30 | 113,2 | 113,66 | ok |
| 17:20 | 149,7 | 149,94 | ok |
| 24:10 | 260,56 | 261,28 | ok |
| 24:22 | 267,9 | 268,84 | ok |
| JOALHERIA | 300,26 | 300,42 | ok |
| 3 CENAS | 43,18 | 44,70 | ok |
| 2 PALAVRAS | 49,28 | 50,16 | ok |

Nenhum card entra atrasado. Três entram cerca de 2 s **antes** da palavra: SEXTA-FEIRA 13 (32,6 vs 34,8), 19 DE NOVEMBRO (199,8 vs 201,28) e MINUTO 18 (359,3 vs 361,36). Aceitável, porque o card antecipa e não contradiz. Se quiser exatidão, atrase a entrada do card para a âncora menos 0,3 s.

Todos os cards ficam no canto inferior esquerdo, legíveis a 960 px e com saída completa: em nenhum quadro o card ficou "preso". Não cobrem o assunto, salvo o "LUCIA [L2]" sobre um quadro sem assunto (nº 3). Conteúdo bate com o fato: SALA SEGURA corresponde à mensagem "After Czr, he's in saferoom, 10+ guys, auto weps, explosives, sound military"; GUYS EVERYWHERE à mensagem na tela; JOALHERIA à imagem oficial (Jason vira com o fuzil, Lucia aponta a pistola).

## 3. Legendas (cr. 7)

Sincronizadas com a narração em todos os quadros conferidos (texto da legenda = palavras alinhadas no instante). Legíveis em branco com sombra. Única falha: a sobreposição no logo final (nº 11). No slate "NOVEMBER 19" (200–202,6 e 319–321) a legenda cai sobre o texto legal miúdo; fica aceitável.

## 4. Fatos sobre o GTA V na fala

- "segurava o direcional, escolhia Michael, Franklin ou Trevor, câmera sobe ao satélite e desce": correto.
- "Trevor de cueca no meio do mato": correto como fenômeno do jogo. A imagem é o Trevor de cueca no estúdio de tatuagem; o card "Trevor de cueca" está certo, só o "mato" não aparece.
- "cada personagem tinha barra de força, fôlego e direção": correto (Strength, Stamina/Lung Capacity, Driving).
- "como acontecia em alguns golpes do GTA cinco": correto.
- "Os três viviam vidas separadas e só se juntavam pra fazer golpe": exagero. Michael e Franklin fazem várias missões juntos fora dos golpes, e o Trevor chega a morar com o Michael. Fica como hipérbole humorística; prioridade baixa, sem mexer.
- Datas: sexta 13/11/2026 → 19/11 = 6 dias; "sábado, 14 de novembro" = correto. San Andreas = 2004 (card) correto.
- Erro de imagem, não de fala: plano 94 mostra o Franklin como "Trevor" (nº 2).

## 5. Abertura de 3 s

A fala tem 6 palavras ("Esse botão não troca de personagem."), começa em 0,0 s e não há vinheta antes: está dentro da regra. Falta a evidência visual: o botão está minúsculo num quadro escuro. Correção no nº 3(b).

## 6. Reel (`_reel/episodio.json`, folhas `_reel/montagem/prevoo/*_01..03.jpg`)

- **MÉDIA: gancho órfão.** "Esse botão não troca de personagem" (plano 1) e o reel nunca mostra nem explica o botão (vai direto para o carro). Usar o mesmo close do HUD do nº 3(b) em 0–1,79 s, ou trocar a fala do gancho do reel.
- **MÉDIA: plano 16 `EXT@1433.0`** tem o mesmo quadro estourado (visível na folha 02). → `inicio 1433.6`; plano 18 `1435.9 → 1436.5`; plano 19 `1438.1 → 1438.7`.
- **MÉDIA: plano 22 (57,75–60,29) `EXT@1444.0`** termina na porta de elevador escura, que é o último quadro do reel. Trocar por `JL01` (imagem oficial da dupla, "cooperação de verdade") ou `EXT@1443.4` (aceitando cerca de 0,6 s de sobreposição com o plano 21).
- BAIXA: plano 17 "a câmera desce pra festa" usa EXT@1263 (outra festa, em outro momento do gameplay). Plano 19 "abaixada perto de uma mesa iluminada" mostra o segurança. Mesmo ajuste do nº 6.
- Cards 14:42, 15:30 e GUYS EVERYWHERE coerentes. Não há GTA V no reel.

## 7. Story (`_story`, folha `_story/montagem/prevoo/*_01.jpg`)

- **MÉDIA: o gancho não combina com o conteúdo.** "Esse botão não troca de personagem" abre um teaser sobre carros e o porta-malas de amanhã. Sugiro abrir com o plano 2 (AMANHÃ 14/11) ou com outra frase. Se for manter a frase, mostrar o HUD.
- Planos 2–6 coerentes (porta-malas no minuto 18, rachas, logo). Plano 4 é a continuação de 1074,4 e não repete.

## 8. Não consegui verificar

- Áudio: não rodei `ebur128` nem conferi clipping. Só checagem visual e `blackdetect` (nenhum trecho preto ≥ 0,1 s com pix_th=0,08).
- Legendas e cards renderizados de reel e story: as folhas de pré-voo não têm legenda nem card desenhados, e não há MP4 de prévia deles.
- Os 42 `card_*.png` fornecidos: abri 2. Todos os cards foram conferidos nas minhas folhas de 1 fps, no contexto.
- Janelas alternativas nos nº 9, 10 e 14: não verifiquei quadro a quadro, estão marcadas no texto. Os nº 1, 2, 5, 7, 8, 12 e 13 foram verificados na fonte ou na prévia.
- Identidade do Trevor em GTAV@148 (só a picape aparece, sem o rosto). Para mostrar o Trevor visível, use GTAV@183.
- Qualidade final em 4K (nitidez, legibilidade do HUD em close).

Evidências em: `C:\Users\GUIBSO~1.KRA\AppData\Local\Temp\claude\f357ef5e624d4979\83131ebc-e156-445d-a2d8-38940e9e0439\scratchpad\` (`tiles\t_01..t_20.png` = prévia a 1 fps; `text80\` = EXT 1455–1476,5; `tp71`, `tp14`, `tp83`, `tp98`, `tp03` = transições a 10 fps; `tgv\` = fonte GTA V a 1 fps; `gv_cmp.png`, `open.png`, `end.png`).
