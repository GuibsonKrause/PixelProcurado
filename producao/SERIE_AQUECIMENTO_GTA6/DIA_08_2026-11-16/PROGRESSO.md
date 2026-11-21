# Progresso do Dia 08 (publicacao 16/11/2026 18h SP = 21:00Z)

- 00:52 inicio (relogio da maquina, 16/11): skill, Mapa, Dia 7 lidos; disco C: 74 GB livres (ok).
- ~01:20 Etapa 0 pesquisa: Newswire da Rockstar (10/11) lido no navegador embutido (WebFetch nao renderiza JS): confirma 'targeting 30 frames per second' + PSSR/ray-traced shadows so no Pro; nada de modo 60 fps. Promessa central NAO derrubada (a resposta honesta e: meta oficial 30, 60 nao confirmado). FONTES.md gravado. Quadros do acervo extraidos (EXT 12:40-13:10 = direcao diurna em autopista; 20:00-20:20 = SUV em pista molhada, aeroporto a noite; Vice_City_08/10/11 conferidas).
- 01:35 roteiro Opus concluido: 21 paragrafos, 1096 palavras; Reel = par. 1-4, Story = par. 21 (ver 00_ROTEIRO_COMPLETO.md 'Cortes'). Revisado: fatos batem com FONTES.md.
- 01:33 TTS Gemini iniciado em 7 blocos de 3 paragrafos (audio/tts_blocos, log audio/gemini.log), fila unica em background.
- 01:45 TTS: blocos 1 e 2 deram TIMEOUT (330 s) no Gemini; chamada minima de teste tambem travou >100 s (API/rede ok: models=200). Glue parado; investigando (teste com timeout 240 s em background). Cartelas 3840x2160 (C*.jpg em montagem/referencias) geradas; stills 4K extraidos.
- 01:55 teste minimo respondeu em 6 s (travada anterior transitoria); fila TTS reiniciada (blocos 1-7).
- 02:20 fila 1: blocos 1,3,5 ok; 2,4,6,7 TIMEOUT (travadas intermitentes do Gemini, chamadas boas levam ~25-40 s). Rodando nova fila com timeout de 100 s e 3 passadas sobre os faltantes. Bloco 1 saiu com 114 s (esperado ~60 s): checar por ASR.
- 02:56 blocos 4,6,7 falharam em 5 rodadas paralelas (hang deterministico). Mudanca: gerar esses 9 paragrafos (10-12,16-18,19-21) um a um em paralelo (tts_blocos/par) e emendar em blocos; registrar como desvio do padrao de 3 paragrafos.
- 03:09 so PAR_12 saiu; Gemini travando quase sempre. Fila sequencial 'paciente' (75 s/tentativa, ate 12 rodadas) nos 8 paragrafos faltantes.
- 03:25 capas A/B (16:9 e 9:16) compostas com compose_thumbnail.py sobre quadros nativos (A = EXT 20:10 pista molhada, 'META: 30 FPS / E O PRO?'; B = Vice_City_11, 'SEM FILTRO / SO O CONFIRMADO'); sem IA, R$0; sem comparacao lado a lado.
- 03:28 CAUSA dos travamentos: Gemini TTS responde HTTP 429 Too Many Requests com Retry-After 5606 s (~93 min); o SDK ficava esperando. Blocos 1,2,3,5 (e PAR_12) ja gerados. Retomada agendada em background para ~05:05 (sleep 5800 s e depois fila sequencial dos 8 paragrafos restantes). Publicacao so 18h; folga ok. Nada de fallback de voz (o TTS e Gemini; fallback Claude nao gera voz).
- 03:46 pronto sem voz: FONTES.md, roteiro (Opus), cartelas 3840x2160, capas A/B, carrossel 4 slides, gerador do episodio.json ancorado nas palavras. Bloco 1 do TTS teve cauda alucinada (a partir de 46,2 s: ~60 s de texto improvisado); sera truncado em 46,3 s. Aguardando janela de cota do Gemini (~05:05) para os 8 paragrafos restantes (10,11,16-21).
[05:25] TTS completo; ASR dos paragrafos ok. Montando blocos + loudnorm.
[05:36] Audio normalizado (404.09 s, -16.8 LUFS, TP -1.5); alinhamento ok (107 estimadas = numerais por extenso). Gerando episodio.json x5.
[05:42] prevoo 0 erros nas 4 pecas; revisao Opus das folhas disparada.
[05:45] Pacote de texto (titulos A/B, descricao com capitulos, tags 14/231, comentario) e secao publicacao no episodio.json prontos; aguardando revisao Opus das folhas.
[05:52] Revisao Opus: 1 bloqueio (texto C06 PSSR) + ajustes; aplicando em todas as pecas.
[06:12] Correcoes aplicadas (C06/C14 texto, P03, Remote Play, repeticoes, reel cortado em 62.9 s, story -0.6 s); gsap ausente no padrao -> 'gsap' em episodio.json (L08). Amostra vertical ok (sem verde). Amostras previa 0-25 e 280-300.
[06:42] 2a revisao Opus: longo/story ok; reel corrigido (corte 62.30, sem C05). Fila de render 4K iniciada (longo, reel, story, vertical).
[07:13] Renders 4K concluidos 06:42-07:11 (longo 341MB, reel 46MB, story 16MB, vertical 49MB). Rodando validar_v2.
[07:23] validar_v2 ok nas 4 pecas (vertical: pix_th 0.04 por cenas noturnas escuras; opcao black_pix_th adicionada ao validar_v2). Preparando revisao final.
[08:03] Revisao final Opus APROVADA (validar_revisao exit 0). Proximo: dry-run distribuir_postiz.
[08:04] dry-run distribuir ok; iniciando --publicar --data 2026-11-16T21:00:00.000Z
[08:08] 10 pecas aceitas no Postiz (agendadas 21:00Z). Conferindo --status.
