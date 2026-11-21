# PROGRESSO — Dia 03 (publicação em 11/11/2026)

Retomar sempre por aqui. Checkpoint formal: `producao.json` (`automacao/checkpoint.py`).

## Decisões
- Datas do roteiro ("faltando oito dias", "amanhã, dia doze") continuam válidas em 11/11: sem cópias de publicação; roteiro original usado.
- Pipeline genérico `produzir_v2.py` + `episodio.json`. `rotulos_obrigatorios: {"GTAV": "GTA V"}`. Master 4K 30 fps.
- Ferramenta temporária (scratchpad, não versionada): `voz.py` (normalização loudnorm 2 passes + faster-whisper small + alinhamento difflib). Obs.: faster-whisper 1.2.1 quebra com `av` 19 ao abrir arquivo; contornado decodificando o áudio via ffmpeg para numpy.

## Estado
| Etapa | Estado | Artefato |
|---|---|---|
| Voz Gemini TTS | OK (373,08 s) | `audio/03_NARRACAO_narracao.wav` |
| Normalização -16 LUFS / TP -1,5 | OK | `audio/narracao_normalizada.wav` |
| Alinhamento | OK (958/1125 palavras casadas, 167 interpoladas, sobretudo números) | `audio/palavras_alinhadas.json` |
| Direção / episodio.json | v1 (64 planos) | `episodio.json` |
| Pré-voo | em andamento | `EXEC_PREVOO.log`, `montagem/prevoo/` |
| episodio.json v2 (64 planos, 35 cards) | pré-voo código 0 (folhas olhadas; janelas sem repetição) | `episodio.json`, `montagem/prevoo/` |
| Derivados | `_reel` (72,1 s), `_story` (15,05 s), `_vertical` (integral) com episodio.json próprio (gerados por script temporário a partir do longo) | `_reel/`, `_story/`, `_vertical/` |
| Thumbnails | A (arte Gemini '6 ESTRELAS! VOLTARAM'), B (quadro real EXT 15:45 'SEM ESCAPATÓRIA FÁCIL'), vertical (arte Gemini vertical) | `thumbnail_A/B/vertical` |
| Pacote | títulos A/B, descrição+capítulos, tags, comentário, carrossel (4) | `publicacao/`, `social/` |
- Ajuste genérico: `compose_thumbnail.py` (formato short) desceu o painel de texto (y=335) para não cobrir a logo.
- Pendente: prévia 960x540 + revisão independente; render 4K; derivados; QA; publicação.
- Lição: tempos dos trailers (T1/T2/LT) no INDICE são imprecisos; confirmar pelas folhas do pré-voo.

## Atualização (revisão da prévia)
- Revisor independente (opus) olhou 192 quadros da prévia 540p. Corrigido: P03 (HUD de 6 espaços, EXT@1088,5), cards com número desmentido pelo HUD (4 estrelas acesas, 4 ícones) sem o número, P13 sem tela ESRB (T1@80), P14/P15 trocados, P20/21/40 com policiais do T2, P35 pântano (airboat), P45/46 sem repetir o drone, 'FICHA DO VEÍCULO' etc. Painéis refeitos.
- Não corrigido (aceito): P12/P24 usam T2 (GTA VI) sobre fala de GTA V (acervo GTA V tem só ~28 s de perseguição); P23 repete cena do P04; fotos estáticas longas; legenda sobre overlays de mídia (Weazel/LuchaLibre); planos de pântano/garagem genéricos em P56/P57.
- Render: `EXEC_RENDER.log` (cadeia: master 4K -> _YT 40 Mbps -> reel/story/vertical -> *_final 18 Mbps; vertical ig300 5,6 Mbps). Depois: validar_v2 em todos, distribuir_postiz.
- 22:03 publicação iniciada (EXEC_PUBLICAR.log). NÃO rodar --publicar de novo sem conferir POSTIZ_ESTADO.json.
- 22:39 youtube_longo (1,85 GB via R2) falhou no Postiz ('re-authenticate'; vídeo NÃO está no canal; short publicou). Reencodando YT a 27 Mbps (~1,25 GB, como o Dia 2 que passou) e reenviando só essa peça após apagar o post velho cmwcuok9m0000pna93utgzbn4.
- 23:25 reenviando youtube_longo (post velho apagado, R2 limpo, estado com backup .bak_youtube_longo_falhou). NAO repetir.
- 23:36 2ª tentativa youtube_longo falhou igual (token OAuth expirado a cada ~1h; falha dispara refresh). Reenvio imediato com token fresco.

## Atualização final (12/11)
- 10/10 peças PUBLISHED (ver POSTIZ_ESTADO.json). youtube_longo: https://www.youtube.com/watch?v=KQuZW0clCPw (3ª tentativa; as duas primeiras falharam com 'Please re-authenticate your YouTube account': o token OAuth do YouTube expira ~1 h e a tentativa que o encontra expirado falha e dispara o refresh; reenviar logo em seguida funciona). Posts velhos apagados, R2 limpo.
- Upload YouTube de 1,25 GB via Postiz leva ~35-40 min (~35 MB/min).
- Revisão final formal (REVISAO_FINAL.json) NÃO emitida: áudio nunca ouvido. Revisão visual independente só na prévia 540p (antes das correções); master final só conferido por QA técnico e folha de contato.
- Pendente do usuário: A/B no YouTube Studio (título `publicacao/02_TITULO_B.txt`, capa `thumbnail_B/capa_youtube.jpg`).
- Lições: Docker Desktop precisa estar ligado para o Postiz; faster-whisper 1.2.1 x av 19 (passar áudio como numpy); tempos de trailers no INDICE são imprecisos.
