# Progresso — Truque da Nova Zelândia (15/11/2026)

- Voz: Gemini TTS (gemini-3.8-flash-tts, voice_iagtq1gnk2br), longo em 10 partes (`audio/tts_blocos/`) e Short em 1 bloco (`audio/short_tts/`). Nenhuma regeneração. Normalizadas em -16,7 LUFS (longo, 389,28 s) e -17,1 LUFS (Short, 75,16 s), pico -1,5 dBTP.
- Gancho "GTA 6 às oito da manhã." começa em 0,00 s e termina em 2,34 s nos dois formatos.
- Alinhamento: faster-whisper small + difflib contra o texto limpo (`audio/palavras_alinhadas.json`, `audio/short_alinhadas.json`). Divergências em `audio/revisao_asr.json` e `audio/short_revisao_asr.json`.
- Direção: só acervo videosGTAVI (Extended Look, Trailer 1, Launch Trailer). Janelas conferidas por quadro no pré-voo (`montagem/prevoo/`, 0 erros). Cards de menu Xbox identificados como ILUSTRAÇÃO.
- Qualidade: fontes nativas 3840x2160 a 30 fps. Longo 3840x2160/30. Peças verticais 1080x1920/30 (padrão do episódio anterior; o miolo 16:9 sai de fonte 4K reduzida). Sem interpolação de fps.
- Capas: `publicacao/thumbnail_A/` (16:9, "8H DA MANHÃ?") e `publicacao/thumbnail_vertical/` (9:16, "16 HORAS ANTES").
- Estado dos renders e QA: ver `producao.json`, `RENDER_*_LOG.txt` e `QA_*_LOG.txt`.
