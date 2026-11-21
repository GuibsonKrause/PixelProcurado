# Revisao final independente — Only in Dade

Parecer visual: aprovado com ressalva baixa. Parecer formal: PENDENTE / REPROVADO pelo validador porque nao houve escuta real. Nenhum trecho foi falsamente declarado ouvido. A autorizacao de publicacao nao substitui uma evidencia auditiva inexistente.

Foram efetivamente inspecionados os 66 quadros individuais extraidos dos quatro MP4s finais (27 master 4K, 27 integral vertical, 7 Reel, 5 Story), em dez folhas qa/revisao_final/*_folha_*.jpg. Cobertura: todos os cards, ao menos um quadro por janela de30s, inicio e final. Tambem vistas as quatro folhas gerais finais (32 amostras adicionais), a prancha de capas/carrossel e a evidencia composta da legenda saneada. Nao houve reproducao integral, escuta ou observacao continua das animacoes finais.

Confirmacoes: originais e replicas distinguiveis; selos GTA VI/CAPTURA e REPLICA REAL nos quadros relevantes; cards e legendas sem corte; enquadramento vertical preservado. Perseguicao/HUD corrigidos em162-166s. Legenda corrigida em158.84-160.94s, conferida no SRT e nos frames finais. FUNCAO A CONFIRMAR conserva a incerteza sobre captura pelo celular. Capas horizontal/vertical e carrossel01-03 legiveis e coerentes com janela/esquina e replica real.

Ressalva baixa: master135s, legenda PT cruza parte do nome de perfil original do Trailer1. O portugues permanece legivel; nao considero bloqueio visual. Evidencia: qa/revisao_final/Longo_15.jpg. A versao vertical separa esses textos.

QA tecnico lido: 4/4 com contagens esperadas de quadros e zero intervalo preto. Master3840x2160 e integral1080x1920:197.166633s; Reel1080x1920:66.4s; Story1080x1920:16.466667s. LUFS entre -16.9 e -16.7, picos -1.4 a -1.3dBFS. Isso nao comprova qualidade de interpretacao/pronuncia ou ausencia de defeito audivel.

Escuta humana minima pendente: master e integral vertical0-10s,125-140s,187.2-197.2s; Reel0-10s e56.4-66.4s; Story0-16.5s. Recomendo tambem159-166s dos longos para conferir a fala junto da legenda saneada. Registrar no JSON somente apos escuta efetiva.

REVISAO_FINAL.json identifica com SHA256 os quatro MP4s, quatro SRTs, duas capas e tres paginas do carrossel. O campo audio_trechos_ouvidos esta vazio deliberadamente. O validador foi executado com --cards qa/revisao_final/cards.json e retornou exit1; detalhe em qa/revisao_final/validador_final.txt. Como o schema rejeita lista vazia de escuta antes dos demais testes, o resultado nao certifica automaticamente toda a cobertura visual: ela e descrita acima e documentada nas imagens e no JSON.
