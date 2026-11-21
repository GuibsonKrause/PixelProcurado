# Progresso — Only in Dade

## Pronto para distribuição

- As quatro exportações passaram no QA técnico sem intervalos pretos. Master 4K de 254,6 MB, vertical integral de 128,1 MB, Reel de 263,4 MB e Story de 51,4 MB.
- Revisão final independente conferiu os quatro formatos, as capas e o carrossel. O validador formal acusou apenas a falta de escuta real. O usuário autorizou a publicação com essa pendência. Evidências em `REVISAO_FINAL.md`.
- Plano Postiz validado e envio único executado para 11 peças em YouTube, Facebook, Instagram e TikTok, após checagem de duplicatas. As 11 receberam IDs e terminaram em `ERROR`, sem `releaseURL`. Facebook integral e corte retornaram `fetch failed`; as demais não expuseram detalhe. `posts:missing` retornou vazio para os 11 IDs. O Docker não respondeu às consultas de logs. IDs e mídias no R2 preservados para diagnóstico. Estado em `publicacao/POSTIZ_ESTADO.json`.

- Baixados os dois Reels no melhor formato oferecido ao extrator, 720×1280 a 30 fps. Terceiro clipe público e galeria da campanha inventariados em `videosGTAVI/ONLY_IN_DADE_2026-11/`.
- Roteiro de 544 palavras e versões de locução entregues. O vídeo do Gameplayrj foi consultado pela transcrição automática em português. O TudoCelular devolveu HTTP 402. As duas fontes principais foram conferidas por quadro. A pauta é a comparação com Miami e a forma de filmar, sem tratar a perspectiva de celular como confirmação de mecânica jogável.
- O Gemini gerou os cinco blocos. WAV normalizado em `audio/narracao_normalizada.wav`, com 193,760 s. Conferência da fala pelo ASR em andamento.
- Locução definitiva em `audio/narracao_normalizada_editada.wav` (196,980 s, −16,9 LUFS e −1,5 dBTP). O ASR confirmou a frase reparada. Alinhamento de 545 palavras e 11 âncoras. Reel de 66,350 s e Story de 16,480 s com WAV e marcas próprias.
- Capas horizontal e vertical e carrossel de três peças prontos em `publicacao/`, inspecionados em prancha reduzida. A direção está montando a timeline com suporte genérico de enquadramento 9:16 sem distorção. Pré-voo, revisão independente, amostras, renders, QA e publicação pendentes.
- Dry-run e pré-voo aprovados para os formatos finais. Revisão independente inspecionou 86 planos nas folhas e sete amostras. Corrigimos os planos 50 e 51 para manter a perseguição e o HUD ao longo da fala e removemos dois tokens espúrios da legenda em cópia do alinhamento. Relatório em `REVISAO_PREVIA.md`. A escuta real continua pendente.
- Após falta de espaço, os caches regeneráveis do Dia 04 foram limpos e a configuração restaurada por escrita atômica com as 11 peças, incluindo TikTok. Renders finais encaminhados ao executor após a checagem da legenda corrigida, em sequência. Nenhum envio iniciado.
