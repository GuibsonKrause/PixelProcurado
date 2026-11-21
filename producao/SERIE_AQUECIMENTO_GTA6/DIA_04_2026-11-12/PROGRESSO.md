# Progresso do Dia 04

Publicação prevista para 12/11/2026 às 18h em São Paulo (21h UTC).

## Locução e alinhamento

- Consultados o README Codex, o mapa mestre e o progresso do Dia 02. As referências ao lançamento em 19/11 e ao próximo episódio em 13/11 correspondem ao dia da publicação. Roteiros originais preservados.
- Geração, normalização e alinhamento delegados ao executor `audio` (`gpt-6.1-sol`, esforço solicitado `low`).
- A primeira execução do Gemini ficou sem WAV, com log vazio e conexão em `CloseWait`. O executor encerrou os processos dessa tentativa e não observou início da tentativa de recuperação com o texto original.

## Conferência editorial do acervo

- Extended Look, `02:00`: o HUD mostra `STUDY [R1]`. A fala diz R2. Em `01:00`, o HUD mostra um alvo associado a L2 e não comprova que o botão selecione o tom da conversa.
- Extended Look, `07:10`: o HUD mostra `LUCIA [L2]`. A direção original indicava L1.
- Extended Look, `07:50`: o cervo aparece em uma sequência exibida na TV do jogo. `Mount_Kalaga_National_Park_05.jpg` mostra os cervos junto à água.
- Extended Look, `09:38–09:50`: a mulher usa óculos escuros e Jason já está na cabine no primeiro quadro observado. O plano permite comentar postura e movimento da cabeça. Ele não demonstra leitura dos olhos, distância ou reações sistêmicas da IA.
- `Grassrivers_06.jpg` mostra um homem com uma arma no ombro e um réptil pendurado ao fundo. A tomada do airboat em `GTAVI_Trailer_1.mp4` por volta de `00:20` e `Grassrivers_01.jpg` oferecem imagens de pântano e jacaré.
- O usuário autorizou as correções nas cópias. `01_NARRACAO_PUBLICACAO_2026-11-12.txt` e `03_NARRACAO_PUBLICACAO_2026-11-12_GEMINI.txt` têm 27 parágrafos com as mesmas 931 palavras, descontadas as marcações vocais. A abertura tem seis palavras. A fala passa a propor testes para as hipóteses de comportamento da IA, corrige os comandos, troca a cena da cobra pela evidência de jacarés e mantém as datas originais. O executor foi acionado para retomar o Gemini com a versão de publicação.

## Bloqueio da locução

- Na segunda execução, com o texto de publicação dividido em três partes, o Gemini iniciou a parte 1 e a conexão TLS entrou em `CloseWait`. O wrapper ficou pendente e não retornou áudio, código HTTP ou erro de API antes de ser encerrado. Zero WAVs gerados. Evidência em `audio/gemini_publicacao.log`.
- Uma consulta `models.list` com a mesma credencial retornou HTTP 200. O teste confirma acesso básico à API. A requisição de geração de áudio segue sem resposta utilizável.
- Locução, normalização e alinhamento pendentes. A próxima etapa começa somente após validar o WAV da cópia de publicação. Pré-voo, prévia independente, render, QA, pacote A/B e agendamento ainda pendentes. Nenhuma peça foi enviada ao Postiz.

## Retomada

- Em 12/11, uma chamada curta com a voz oficial gerou WAV mono de 2,12 s a 24 kHz. A locução corrigida foi retomada em blocos menores, com log `audio/gemini_publicacao_2026-11-12.log`.
- O Gemini entregou os oito blocos. Bruto concatenado em `audio/03_NARRACAO_PUBLICACAO_2026-11-12_narracao.wav`. Normalizado em `audio/narracao_normalizada.wav` (337,160 s, 48 kHz mono, −16,8 LUFS e pico de −1,5 dBTP). ASR em andamento.
- A transcrição detectou um parágrafo extra de locução. O trecho de 79,350 a 101,050 s foi removido entre pausas, preservando os brutos. Master de voz `audio/narracao_normalizada.wav` com 315,460 s e 934 marcas em `audio/palavras_alinhadas.json`. Âncoras em `audio/ancoras_paragrafos.json` e relatório em `audio/revisao_asr.json`.
- Direção e configurações de edição delegadas ao executor `acervo` (`gpt-6.1-sol`, esforço solicitado `medium`). Pré-voo, prévia, renders e QA atribuídos ao executor `render` (`gpt-6.1-sol`, esforço solicitado `low`).
- Master de voz e alinhamento final decodificados/validados. Reel de 47,950 s e Story de 15,350 s em `_reel/audio/` e `_story/audio/`, com alinhamentos de 146 e 48 marcas. A escuta das pronúncias apontadas pelo ASR segue pendente.
- `episodio.json` principal (90 planos, 3840×2160 a 30 fps) e os configs `_previa`, `_vertical`, `_reel` e `_story` passaram no dry-run, código 0. Pré-voo com folhas delegado; nenhum render antes da inspeção das folhas aprovadas.
- Pré-voo do principal aprovado com código 0, sem avisos. Inspecionadas as nove folhas; corrigidos preto no plano 57, sobreposições de fonte e janelas da abertura, luta, cervo, Effluvia, corredor e treino. Reel e Story também com pré-voo código 0. Prévia de 960×540 liberada; render 4K aguardará revisão independente.
- Prévia em `_previa/exportacoes/Pixel_Procurado_DIA04_Previa_V2.mp4` passou `validar_v2.py` (960×540, 30 fps, 9465 quadros, 315,46 s, −16,8 LUFS e sem pretos). O primeiro concat truncou por falta de `48.mp4`, regenerado antes da aprovação técnica. Revisão visual independente da prévia atribuída a `/root/revisao` (`gpt-6-astra`, esforço solicitado `high`).
- Revisão independente inspecionou 104 quadros dos 26 cards e reteve o 4K por cinco pontos: persistência do rótulo GTA V, duração do card da luta, âncora de 19 de novembro, fonte do HUD de R1 e legenda cobrindo o perfil PlanetLeonidaMan. O pipeline genérico recebeu rótulos de origem persistentes via ASS, com SRT preservado. A direção está corrigindo os quatro demais pontos antes da segunda prévia. A revisão se baseou nas imagens e nos tempos da transcrição, sem escuta subjetiva.
- Quatro ajustes editoriais aprovados pelo revisor na segunda prévia (`_previa_revisada/`, QA 0). Restou um quadro sem rótulo GTA V a 191,133 s. O rótulo passou a ser aplicado desde o primeiro quadro local de cada clipe, sem depender de timestamps globais. A amostra `qa/teste_rotulo_p52/` mostra o rótulo nos quadros 0 e 202. Revalidação independente dessa amostra solicitada.
- Revisão independente liberou o 4K depois de conferir os dois quadros da amostra. Evidências e hashes em `REVISAO_PREVIA.md`. Renders finais iniciados em segundo plano (logs `RENDER_MASTER.log`, `_vertical/RENDER_VERTICAL.log`, `_reel/RENDER_FINAL.log`, `_story/RENDER_FINAL.log`). QA e derivação de bitrate previstos após cada render.
- As cinco exportações passaram no QA técnico. Pacote A/B, metadados e carrossel prontos em `publicacao/`. O plano do Postiz passou para dez peças, com integral do Instagram de 282,3 MB e sem duplicata encontrada na consulta remota. O usuário autorizou publicação imediata assim que validado.
- Revisão visual final aprovada por amostragem de 170 quadros e inspeção das capas e do carrossel. O validador formal rejeitou `REVISAO_FINAL.json` por `$.audio_trechos_ouvidos: minimo de 1 itens (tem 0)`. A escuta real não foi possível neste ambiente. Nenhuma peça enviada.

- Conferir `producao.json` e os logs do episódio antes de disparar outra chamada de TTS.
- Após validar a narração, preparar `episodio.json` com `"rotulos_obrigatorios": {"GTAV": "GTA V"}` e rodar o dry-run e o pré-voo. Inspecionar as folhas e obter a revisão independente da prévia antes do 4K.
- Conferir tamanho de cada mídia. O código trata `--agora` como publicação imediata e ignora a data informada nesse modo. Para agendar, usar `--publicar --data 2026-11-12T21:00:00Z`, sem `--agora`. Verificar cada `post_id` antes de qualquer reenvio.
- Publicação imediata autorizada com escuta pendente. Postiz confirmou 10/10 `PUBLISHED` com `releaseURL`, e `--status --limpar` saiu com código 0. Nenhum reenvio. URLs e IDs em `publicacao/POSTIZ_ESTADO.json`, consulta em `publicacao/STATUS_POSTIZ.log`.
