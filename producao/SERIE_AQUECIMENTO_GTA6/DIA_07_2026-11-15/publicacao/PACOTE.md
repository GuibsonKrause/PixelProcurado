# Pacote de publicação - Dia 7 (domingo 15/11/2026, 18h SP = 21:00Z)
Longo 383,84 s (narração). Nada foi enviado/publicado. Capas em `capas/`, carrossel em `carrossel/`. Os MP4 já foram renderizados em 4K e validados; a revisão final foi aprovada com ressalvas (REVISAO_FINAL.json / REVISAO_FINAL_NOTAS.md). Os MP4 de longo e vertical estão sendo re-renderizados com correções de legenda, cartelas e card (ver PROGRESSO.md); caminhos em `publicacao_secao.json` / `episodio.json`.

## Títulos (YouTube; teste A/B aplicado manualmente no Studio)
- **A (recomendado, capa A "PAUSA AQUI")**: GTA 6: 11 Detalhes do Gameplay Que Você Só Lê Pausando
- **B (capa B "CASAL BRAVO?")**: O Botão de Mão Dada no GTA 6 é R2 (e Mais 10 Detalhes)  (verdadeiro: 11 itens no total; mão dada + 10)
- Short/Reel: GTA 6: Mão Dada É no R2 #shorts
- Não usados: "detalhes doentios", "a Rockstar perdeu a linha" (o vídeo mostra detalhes pequenos e legíveis); "Pausei o Gameplay do GTA 6 Quadro a Quadro: Geladeira, Binóculo e Mão Dada" fica como reserva.

## Capas
`capas/capa_longo_A.jpg`, `capa_longo_B.jpg` (1280x720); `capa_vertical_A.jpg`, `capa_vertical_B.jpg` (1080x1920); masters e scripts em `capas/masters/` (`gerar_capas.py`, `gerar_carrossel.py`); prévia 320 px em `capas/prancha_320.jpg`.
Montagem editorial sobre quadros nativos 4K do Extended Look, sem IA (Gemini R$0): A = `EXT_0643` (06:42,7, tênis na borda da banheira, contorno amarelo no tênis); B = `EXT_1857` (18:57, HUD de troca ampliado sobre o paraquedas desfocado). Texto, selo e logo GTA VI pelo `compose_thumbnail.py`. A alternativa B2 ("TEM CERVEJA", `EXT_0719`) não foi necessária: B ficou legível. Os retratos do B são personagens do jogo, sem nome.

## Descrição, tags e comentário
Descrição pronta para colar: `03_DESCRICAO.txt`. Tags (30): `04_TAGS.txt`. Comentário fixado: `05_COMENTARIO_FIXADO.txt`.

## Capítulos (de `audio/ancoras_paragrafos.json`, áudio 383,84 s)
00:00 Hold hands é R2, não R3
00:30 Geladeira: cardápio e a porta com panfleto
01:08 A regra do dia: 11 detalhes com minuto e segundo
01:26 Tênis na banheira: a torneira estava fechada
01:53 Garrafa na mão e barra de pole dance
02:14 TV ligada: cérebro, nuvem e pílula azul
02:49 DRINK, EAT e SMOKE: o R1 dos vícios
03:41 Binóculo e o vizinho de óculos de realidade virtual
04:06 Porta de clube: OVER 21 ONLY e ID Check
04:27 HUD de troca: dois retratos e um coração (hipótese marcada)
05:16 O último detalhe: dois ícones sem texto
05:44 Balanço dos 11 e a pergunta do dia
06:07 Dia 8: PS5 contra PS5 Pro

## Facebook / Instagram (integral)
Mão dada no GTA 6 é R2, não R3. Pausei o gameplay quadro a quadro e li 11 detalhes com minuto e segundo: a geladeira com menu e panfleto, o tênis na borda da banheira, DRINK, EAT e SMOKE no mesmo botão, o binóculo, a porta de clube e o HUD de troca. Hipótese vem marcada. Domingo 15/11, faltam 4 dias para 19/11. Qual você procura primeiro? Amanhã: PS5 contra PS5 Pro. #GTA6 #GTAVI #PixelProcurado

## Reel / Short (`_reel`, §1 a §3)
Mão dada é no R2. No GTA 6, o botão de andar de mãos dadas aparece no minuto 9:50 do gameplay, e a geladeira da cozinha rosa tem menu de bebidas, ímã de banco e um panfleto que diz Frugality is for Fools. Vídeo completo no canal: 11 detalhes que só se leem pausando. #GTA6 #GTAVI #PixelProcurado

## Story (`_story`, §18)
Dia 7 no ar: 11 detalhes do GTA 6 que só se leem pausando. Amanhã, segunda 16/11: PS5 contra PS5 Pro, 30 ou 60 quadros. Faltam 4 dias para 19/11.

## Carrossel Instagram/Facebook (4 slides 1080x1350, `carrossel/01-04.jpg`)
Legenda: Pausei o GTA 6 quadro a quadro: tênis na borda da banheira, mão dada no R2, menu da geladeira e um HUD de troca que é hipótese. Deslize. Vídeo completo no canal: 11 detalhes com minuto e segundo. Faltam 4 dias para 19/11. #GTA6 #GTAVI #PixelProcurado
1. PAUSA / AQUI - `EXT_0643` (06:42).
2. MÃO DADA / É R2 - `CR_1000_HOLD_HANDS` (10:00).
3. TEM / CERVEJA - `EXT_0719` (07:19, menu da geladeira).
4. CASAL / BRAVO? - `EXT_1857` (18:57), hipótese declarada no texto.

## Cópia vertical (Instagram integral)
`_vertical/exportacoes/Pixel_Procurado_DIA07_Vertical_V2.mp4`; `limite_mb` 300 está no formato `_vertical` do `episodio.json` (como no D6); capa `capa_vertical_A.jpg`.

## Guia do YouTube Studio (teste A/B manual)
1. Envie com título A + capa longo A. Categoria: Jogos; jogo: Grand Theft Auto VI se listado; idioma português (Brasil); "Não é conteúdo para crianças". Campo de IA conforme a política vigente e o uso da voz sintética (decisão do dono do canal).
2. Descrição (capítulos com 00:00 e >=10 s cada), tags e comentário fixado (fixar depois de publicado; o Postiz não fixa).
3. Teste A/B: capa A vs capa B com o título A; depois, com amostra, título A vs B. Interpretar CTR por origem de tráfego e tempo de exibição, sem diagnóstico com poucas impressões.
4. Tela final nos últimos 5-20 s sem cobrir legendas; sugerir o vídeo do Dia 6 e inscrição; não linkar o Dia 8 antes de existir. Anexar `Pixel_Procurado_DIA07_Longo_V2.srt` como faixa de acessibilidade.
5. Playlist: "Aquecimento GTA 6".

## Verificação de fatos (contra o roteiro e `montagem/referencias/EVIDENCIAS.md`)
- Observado em quadro: HOLD HANDS R2 (09:50-10:02); FRIDGE no triângulo (07:16,5) e menu com duas BEER e smoothie esmaecido (07:18,3); tênis na borda com torneira fechada (06:42,7); DRINK R1 (07:23); EAT R1 (09:04); SMOKE R1 (12:15); ZOOM no binóculo (17:27); OVER 21 ONLY e ID Check (17:32); HUD de 18:57; luta com dois ícones e sem texto (25:26).
- Hipóteses (marcadas no vídeo e na descrição): R1 como botão dos vícios; HUD de 18:57 como troca de personagem com humor; ícone da luta como botão contextual; TV como comercial de remédio.
- Correções ao Dia 2/Mapa: torneira não estava ligada; R3 virou R2 (HOLD HANDS) e R1 (SMOKE).
- Datas: domingo 15/11, faltam 4 dias para quinta 19/11; amanhã (segunda 16/11) Dia 8: PS5 contra PS5 Pro.

## Legibilidade
Prancha 320 px: frases de 2 linhas legíveis nas quatro capas. A: o gancho depende do texto "PAUSA AQUI" (cena sem HUD, contorno amarelo no tênis). B: HUD ocupa a metade direita; as carinhas são pequenas no vertical e mais legíveis no 16:9.
