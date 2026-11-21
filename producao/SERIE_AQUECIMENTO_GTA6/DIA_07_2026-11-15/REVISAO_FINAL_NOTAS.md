# Revisão final independente: Dia 7, notas das peças extras

Revisor: Claude Opus 5.5 (subagente revisor independente), 2026-11-13, revalidado em 2026-11-14 após o re-render. Resultado em `REVISAO_FINAL.json`: **aprovado_com_ressalvas**, sem problemas de severidade alta ou média; dos 7 de severidade baixa, 4 foram corrigidos e 3 seguem abertos. Rodei `py -3.12 automacao/validar_revisao.py <D7>` com e sem `--cards montagem/revisao_final/cards_longo.json`, e as duas execuções saíram com código 0.

O áudio **não foi ouvido por humano**. A checagem usou transcrição ASR (faster-whisper small, local) comparada aos textos `01/05/06_*NARRACAO.txt`, mais medição de amostras, silencedetect e os QA de loudness. Os frames foram extraídos do MP4 real e abertos um a um. Estão todos em `montagem/revisao_final/`.

## Atualização 2026-11-14: revalidação após re-render do Longo e do Vertical
Hashes novos (sha256):
- Longo MP4 `512fd3b1db8d18d5e592164bc07593eacbe4d5fc7a78415295d7ec8e1da7b0fe`.
- Longo SRT `dda9494c053fa305a75ed974281b6a0441940582437b1b6ba9417b8e8cec15ba`.
- Vertical MP4 `2f7a98726f26d87bd7eac07a14973b00e882caee312df98fb85cf857ad898d83`.
- Vertical SRT `dda9494c…8cec15ba`, idêntico ao do Longo.

Revalidei só o que mudou, com frames reais dos MP4 novos em `montagem/revisao_final/v2/`:
- **Legendas, problema 1: corrigido.** Agora saem "faltam quatro dias pro lançamento" (70,2 s), "seis e cinquenta" (89–100 s), "pro satélite" (305,9 s), "vinte e seis" (319,8 s) e "minuto seis" (348,7 s), conferidos no Longo e no Vertical. "PS cinco Pro" mantém o "Pro" correto, e "GTA seis" segue o roteiro.
- **Cartelas de 316 a 362 s, problema 2: corrigido.** O rodapé saiu e não há mais texto fantasma sob a legenda; o recorte em resolução cheia `v2/longo_crop_rodape_t343.jpg` confirma. No Vertical as cartelas também estão sem rodapé.
- **Card de data, problema 5: corrigido.** Agora é "DOM 15/11 / faltam 4 dias", em uma linha.
- **PACOTE.md, problema 6: corrigido pelo diretor.**
- **Trecho de 316 a 349 s:** segue sem quadro nítido de contato ou sangue. Os quadros são o desfocado, o piso de concreto e as cartelas.
- **Resto do Longo:** re-extraí os 44 timecodes da revisão anterior a partir do MP4 novo. Fora dos trechos alterados, os quadros são idênticos pixel a pixel (diferença média 0,0).
- **Áudio:** a trilha não mudou. O QA dá -16,9 LUFS e pico -1,3 dBFS, e as amostras zeradas continuam em 1,83–2,90 s.

Continuam abertas, como ressalvas baixas, a 3 (sobreposições pontuais), a 4 (silêncio digital na emenda do gancho) e a 7 (logo das capas verticais na grade do Instagram).

## Hashes da revisão anterior (2026-11-13; Vertical e SRT já substituídos)
- Vertical MP4 `f5343c8f…aceb34`; SRT `0ddb6d80…63bda77`, idêntico ao SRT do Longo.
- Reel MP4 `1f3034da…281767`; SRT `86a53c81…84f2dda`.
- Story MP4 `3efe4601…43907`; SRT `7a89b54e…bc284`.
- Capas: longo_A `e1fdf2ca…`, longo_B `089ab8d0…`, vertical_A `15e05ff3…`, vertical_B `3f7301cb…`.

## Vertical (1080x1920, 383,84 s; QA: 11514/11514 quadros, -16,9 LUFS, pico -1,3, 0 pretos)
Frames: `vertical_t1.0`, `t3.96`, `t44.02`, `t150.0`, `t320.0`, `t324.74`, `t335.0`, `t382.79`.
- O vídeo fica numa faixa central (y≈280–690 em 720 px). O fundo é desfocado da própria cena, sem verde e sem preto chapado. O card fica abaixo do vídeo e a legenda abaixo do card, sem sobreposição em nenhum frame.
- Em 25:26 (t320 e t324.74), o quadro da luta está totalmente desfocado e o recorte mostra só o piso de concreto. Não aparece contato nem sangue.
- Nas cartelas (t335), o rodapé "PIXEL PROCURADO" fica dentro da janela do vídeo, acima da legenda. O texto fantasma do Longo não se repete aqui.
- Mesmos erros de legenda do Longo, porque o mapa de correção é igual: "Pro lançamento", "Pro satélite", "6 e cinquenta", "vinte e 6". Visto em t320.
- O HUD nativo fica pequeno na faixa de vídeo (ex.: "HOLD HANDS" em t1.0). Os cards e destaques repetem a informação, então a ressalva é só estética.

## Reel (1080x1920, 67,35 s; QA: 2020/2020, -16,8 LUFS, pico -1,3, 0 pretos)
Frames: `reel_t1.0`, `t3.96`, `t13.16`, `t44.02`, `t61.74`, `t65.52`, `t66.8`.
- O gancho "Mão dada é no R dois." aparece no 1º segundo, sem card e com o destaque HOLD HANDS R2. O ASR reconhece "Mão dada é no R2" com confiança alta.
- A emenda é a mesma do Longo: silêncio digital de 1,83 a 2,90 s, sem clique. Está em `problemas`.
- O ASR do Reel bate com `05_REEL_NARRACAO.txt` até "Faz todo o sentido." Em ~49 s o ASR do Reel "perdeu" a expressão "fim da lista". Comparei as amostras do Reel e do Longo entre 48,5 e 50,7 s: a correlação é 1,0 e o RMS é idêntico. Foi falha do ASR, não corte de áudio.
- O card final "VÍDEO COMPLETO NO CANAL / 11 detalhes que você só lê pausando" (t65.52 e t66.8) não esconde a legenda. Não há CTA falado, coerente com o roteiro do Reel.

## Story (1080x1920, 16,54 s; QA: 496/496, -17,0 LUFS, pico -1,4, 0 pretos)
Frames: `story_t0.8`, `t2.5`, `t6.0`, `t10.0`, `t15.2`, `t16.3`.
- O card "AMANHÃ • 16/11 / PS5 × PS5 Pro" aparece desde o 1º quadro, sobre perseguição policial com HUD legível. Em t6.0 entra o card "30 OU 60 FPS?" e em t10.0 ele já saiu, deixando a cena livre. Em t15.2 está "SE INSCREVE • ATÉ AMANHÃ" e em t16.3 o card sai, com a legenda "amanhã." no fim.
- O ASR bate com `06_STORY_NARRACAO.txt`. Aqui "Pro" está correto (PS5 Pro).

## Capas
Prévias geradas por mim: `preview_capa_longo_A_320.jpg`, `preview_capa_longo_B_320.jpg`, `preview_capa_vertical_A_270.jpg`, `preview_capa_vertical_B_270.jpg`.
- **Longo A "PAUSA AQUI"**: texto legível a 320 px, tênis com moldura amarela, logo GTA VI inteira e bom contraste. O selo "PIXEL / PROCURADO" fica ilegível em miniatura.
- **Longo B "CASAL BRAVO?"**: legível, com HUD ampliado (R1, retratos, coração, carinhas), logo inteira e nenhum nome de personagem.
- **Vertical A/B**: texto grande legível a 270 px e logo inteira na peça cheia. Ressalva: logo e selo ficam nos 283 px do topo e seriam cortados no recorte de grade do perfil do Instagram. O foco do A (tênis) fica na faixa inferior, que a interface do Reel cobre parcialmente.

## Outras checagens
- Nomes de personagem: nenhum nome aparece nos SRT do Longo, Vertical, Reel e Story, nas descrições ou no PACOTE.
- `publicacao/PACOTE.md` linha 2: o texto diz que os MP4 ainda estão pendentes de render, o que já não vale.

## O que mudar, se forem corrigir (todas as correções são de severidade baixa)
1. `episodio.json` e `_vertical/episodio.json`, campo `correcoes_legenda`: remover as entradas genéricas `"pro": "Pro"` e `"seis": "6"` e usar correção por contexto ("PS5 Pro", "GTA 6"). Depois, re-renderizar o **Longo** e o **Vertical**.
2. Cartelas CARTELA*, COLAGEM11 e CARTELAQUINTA: tirar o rodapé "PIXEL PROCURADO" da faixa de legenda e re-renderizar o **Longo**.
3. Opcional: reenquadrar os recortes CRholdprompt, CRfridgeprompt, CRtorneira e CRretratoscoracao, e encurtar o título "HOJE: 15 DE NOVEMBRO".
4. Opcional, depois de escuta humana: aplicar room tone ou encurtar a pausa de 1,83 a 2,90 s.
5. Atualizar a linha 2 do PACOTE.md. Se a capa vertical também for usada na grade do perfil, gerar uma variante com a logo dentro da área central 1080x1350.

## Não verificado
- Escuta humana do áudio (timbre, naturalidade, cliques inaudíveis ao ASR).
- Decodificação integral e contagem de quadros. Usei os QA existentes; não recontei o 4K.
- Capa pública no YouTube e no Instagram, e o comportamento do Postiz.
- O carrossel (`publicacao/carrossel/`) não foi inspecionado.
