# Progresso do Dia 05 (publicação 13/11/2026 às 18h SP = 21:00Z)

- Roteiro escrito em 12/11 por subagente Opus (1135 palavras, gancho "Esse botão não troca de personagem."). Correções ao Mapa: HUD é LUCIA [L2] (não L1) em 07:06; "GUYS EVERYWHERE" em 23:48 (mensagem, não rádio); supino com L2/R2, sem medidor de força.
- Datas do roteiro já escritas para sexta 13/11 e "amanhã, sábado 14" -> não precisa cópia de publicação.
- Próximo: voz Gemini TTS (blocos pequenos; houve travas de conexão no Dia 04), normalizar, ASR.

- Voz OK (sonnet): 8 blocos TTS, 370,36 s, -16,7 LUFS, 1135 palavras alinhadas; reel 60,3 s e story 15,3 s em _reel/_story/audio. Pendente escuta humana: "a esfriar a" @206,5 s e "com o fuzil" @302,7 s.
- Próximo: episodio.json (direção V2) -> dry-run -> prevoo.

- Direção V2 (sonnet): longo 109 planos/42 cards, reel 22, story 6; dry-run e pré-voo código 0 (longo rodado de novo com folhas, 0 erros/0 avisos). Folha 01 do longo saiu sem miniaturas (falha de desenho do pré-voo sob carga); verificar na prévia. PENDÊNCIA FACTUAL: fala "derrubar um homem" (24:22) vs imagem (segurança agarra a Lucia, plano 80). Plano 71 começa com flash de transição ~0,3 s.
- Próximo: prévia 960x540 (haiku) + revisão independente (opus) antes do 4K.

- Revisão independente da prévia (opus) reprovou o 4K: REVISAO_PREVIA.md. Correções aplicadas (sonnet): frase "derrubar um homem"->"levar um tombo" (1 TTS pago, splice, voz 370,26 s, backups *.PRE_TOMBO), direção (112 planos), pipeline estendido (selo GTA V por plano inteiro, movimento fixo, legenda_alta, falha com código 1 em clipe ausente). Caches da prévia apagados; prévia antiga em _previa_antiga/.

- Revisão 2 independente (opus, _previa/REVISAO_2.md): montagem aprovada; correções aplicadas no episodio.json (longo/_previa/_vertical): legenda final alta (MarginV 900), plano 108 inicio 1071.6, plano 111 inicio 1076.4 (menu desfocado), card 14:42 "Depois do tiroteio na rua", card JL02 "dois armados". Fala "dois mascarados"->"dois armados" (falso factual): splice TTS em andamento (backups *.PRE_ARMADOS). Pendente: opcional trocar still BENCH do plano 56 por vídeo; depois pré-voo, revalidar 335–342/356–360/365–370 s e 4K.

- 4K + derivados validados; capas A/B, carrossel e textos em publicacao/. Agendado no Postiz (QUEUE, 10 pecas) para 13/11 21:00Z (18h SP), sem --agora; R2 mantido ate PUBLISHED. Estado: publicacao/POSTIZ_ESTADO.json. Pendente: confirmar PUBLISHED e rodar --status --limpar apos 13/11 18h; revisao_final nao executada; audio nao ouvido.
