# PROGRESSO — Dia 02 (publicação em 11/11/2026)

Retomar sempre por aqui. Checkpoint formal: `producao.json` (`automacao/checkpoint.py`).

## Decisões
- Roteiro era de 10/11; hoje é 11/11. Cópias `*_PUBLICACAO_2026-11-11.txt` corrigem 2 referências temporais (ver `AJUSTES_EDITORIAIS_PUBLICACAO_2026-11-11.md`). Originais preservados.
- Pipeline genérico `automacao/pipeline/produzir_v2.py` + `episodio.json` (sem script por episódio). Extensão genérica adicionada: plano com `"sem_card": true` (sem card) e pan suave em imagens.
- Master 4K 3840x2160 30 fps (fontes são 4K30). Vertical 1080x1920 para Instagram. Prioridade: vídeo do acervo; imagens só quando necessário; sem repetir janelas de vídeo.
- Ferramentas temporárias (scratchpad, não versionadas): `voz.py` (normalização + ASR + alinhamento).

## Estado das etapas
| Etapa | Estado | Artefato |
|---|---|---|
| Voz Gemini TTS | OK | `audio/03_NARRACAO_PUBLICACAO_2026-11-11_narracao.wav` (24 kHz, bruto) |
| Normalização -16 LUFS / TP -1.5 | OK | `audio/narracao_normalizada.wav` (416.89 s, LRA 3.2) |
| Alinhamento palavra a palavra | OK (1242 palavras; 147 trechos numéricos estimados, ok) | `audio/palavras_alinhadas.json` |
| Direção / episodio.json | OK (113 planos, ~38 cards, janelas de vídeo sem repetição; só COVER repete) | `episodio.json` |
| Render master 4K | em andamento (`EXEC_RENDER_MASTER.log`; clipes em `montagem/DIA02_Master_4K/NN.mp4` são reaproveitados) | `exportacoes/DIA02_Master_4K.mp4` |
| Derivados verticais (integral 1080x1920, reel 68s, story 15s) | pendente; `_vertical/`, `_reel/`, `_story/` cada um com `episodio.json` próprio | `_*/exportacoes/` |
| QA técnico + revisão independente | pendente | `qa/` |
| Thumbnails A/B | OK (A '212 GIGAS?!' arte Gemini; B 'ZERO TELA PRETA' quadros reais) | `thumbnail_A/`, `thumbnail_B/`, `comparacao_capas_AB.jpg` |
| Pacote SEO (títulos A/B, descrição, capítulos, tags, comentário) | OK | `publicacao/01..05` |
| Postiz | pendente | `publicacao/POSTIZ_ESTADO.json` |

## Como retomar
1. `py -3.12 automacao/pipeline/produzir_v2.py --episodio producao/SERIE_AQUECIMENTO_GTA6/DIA_02_2026-11-10 --dry-run`
2. Clipes por plano ficam em `montagem/<stem>/NN.mp4` e são reaproveitados; apagar a pasta se mudar a direção.
3. Nunca repetir TTS (cobrado) nem ASR se `audio/palavras_alinhadas.json` existe.

## Notas técnicas
- Corrigido bug em `automacao/gerar_arte_thumbnail.py` (cliente Gemini fechado pelo GC).
- Hyperframes (painéis) levam ~5 min por formato; já em `montagem/paineis_long.mov`.
- Master intermediário é crf17 ultrafast (~50 Mbps); reencodar para ~40 Mbps antes do envio.
- Capítulos da descrição vêm do alinhamento (início dos parágrafos 1,4,5,10,11/12,17,20,23,25,29).

## Atualização (render)
- Master 4K intermediário pronto (`exportacoes/DIA02_Master_4K.mp4`, 2.9 GB). `montagem/encadeado.sh` (log `EXEC_ENCADEADO.log`) faz: reencode `DIA02_Master_4K_YT.mp4` (~40 Mbps) e renderiza `_reel`, `_story`, `_vertical`.
- Depois: reencodar derivados verticais para `*_final.mp4` (18 Mbps, max 20), QA (`validar_v2.py`), revisão independente, `distribuir_postiz.py --episodio <pasta> --publicar --agora`, depois `--status --limpar`.
- `episodio.json` já contém a seção `publicacao` (10 peças; capas A e vertical; carrossel em `social/`).

## Atualização (QA 1)
- QA achou quadros pretos na fonte: GTAV@~121,3 s (plano 51) e LT@~66,7 s (planos 94 do longo/vertical e 1 do reel). Corrigido em `episodio.json` (51→GTAV@122; 94 e reel 1→LT@67,3), clipes em cache apagados.
- `montagem/refazer.sh` (log `EXEC_REFAZER.log`) re-renderiza master, reencoda `_YT`, regera `*_final.mp4` e roda QA. Story já passou no QA. Depois: revisão independente e publicação.

## Atualização (revisão independente)
- Subagente (opus) revisou frames. Corrigido: plano 12 (tela ESRB → GTAV@8), 75 (card "praia lotada" com imagem de estande → EXT@1109, 3 s), 76 (EXT@639,8), 51/52 (GTA V deserto: @190 e @12), card do plano 82 ("06:30 → 08:50"). Painéis Hyperframes e clipes afetados apagados; `montagem/refazer.sh` rodando de novo (log `EXEC_REFAZER.log`).
- Não corrigido (baixa/média, aceito): cenas GTA V sem rótulo em 01:49–02:00 e 03:09–03:19; quadro de transição em 03:59; card +25-30 GB sobre o logo; carrossel 2/3; capa vertical corta o console.
- Áudio nunca ouvido por pessoa/agente: REVISAO_FINAL.json formal não emitido.
- Publicação iniciada (log EXEC_PUBLICAR.log; estado em publicacao/POSTIZ_ESTADO.json). Retomar com --publicar (pula peças com post_id) e depois --status --limpar.

## Atualização (publicação, 11/11)
- 9 de 10 peças PUBLISHED com link (ver `publicacao/POSTIZ_ESTADO.json`); R2 dessas já limpo com `--status --limpar`.
- `instagram_integral`: 1ª tentativa (832 MB) ERROR por limite de 300 MB; reenviado `_vertical/exportacoes/DIA02_Instagram_Integral_ig300.mp4` (post `cmwclk8v9000rpnalt3ra3z1v`, estava em QUEUE). Conferir: `py -3.12 automacao/pipeline/distribuir_postiz.py --episodio <pasta> --status --limpar`.
- `distribuir_postiz.py` grava `post_id` vazio (bug aberto): IDs foram recuperados à mão. NÃO rodar `--publicar` de novo sem conferir.
- Pendente do usuário: A/B no YouTube Studio (título `publicacao/02_TITULO_B.txt`, capa `thumbnail_B/capa_youtube.jpg`).
- Skills atualizadas com as lições (pré-voo, limites, IDs) e sincronizadas.
- 11/11 fim: instagram_integral PUBLISHED (https://www.instagram.com/reel/DfnY7oGBlR8/), R2 limpo. 10/10 peças publicadas. Ferramentas novas: prevoo_v2.py; distribuir_postiz.py com captura de ID, limites e --reenviar.
