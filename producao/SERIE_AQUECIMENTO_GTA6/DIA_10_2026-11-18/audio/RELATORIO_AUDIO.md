# Áudio DIA10 — validado tecnicamente, ressalvas ASR

NÃO OUVIDO POR HUMANO.

Master: narracao_master_aprovado.wav; 385.48s, PCM16/48kHz/mono. Ebur128: -16.3LUFS; -1.6dBTP. Mesma duração e samples do WAV usado nos ASR. Bruto/V1/V2/masteranterior preservados. Encode final diretoRAW: loudnormdynamic+ganho0,8dB+limitador−1,6a192k, saída48k.

Small1036palavras;medium1046. Números/datas críticos batem ambos. Gancho0–1,30s(small)/1,74s(medium). Não houve re-ASR nem regravação. Dúvidas de ASR mantidas em palavras comuns, correções somente nomes documentadas; clips e duas transcrições em revisao/trechos_asr.json.

ReelP04–06:[47.78, 99.86];StoryP01:[0, 12.35]. Cortes sample-exact contíguos do master final, sem voz extra. Âncoras20parágrafos e palavras alinhadas disponíveis.

Histórico inicial de timeout preservado em QA_AUDIO_bloqueio_02h.json. RetomadaB02–B07 uma tentativa por bloco/clientnovo, deadline240s; B01 reaproveitado. RequestsSDK efetivos e custos desconhecidos; causa dos timeouts não comprovada.
