# Teste local de clonagem — Guibson

Fonte recebida em 22/10/2026: `C:/Users/guibson.krause/Downloads/modeloVozGuibson.wav`. WAV PCM 16-bit, 44,1 kHz, estéreo, 29,242 segundos. Pico -7,73 dBFS, sem amostras saturadas. A fala começa em aproximadamente 3,34s.

Referência preparada: `referencia_18s.wav`, 18,6 segundos, mono, 48 kHz, filtro passa-altas de 70 Hz e nivelamento. O original não foi modificado. Perfil local do VoiceStudio: `097c5b55`, nome “Guibson - Pixel Procurado”. O perfil não recebeu a marca formal de consentimento do aplicativo porque a gravação contém o texto do canal, não uma declaração de consentimento; isso não impede síntese local.

O OmniVoice comum foi descartado neste computador: uma frase de nove palavras, com 16 etapas, ultrapassou o limite de 600 segundos de cálculo em CPU. O MOSS-TTS-Nano foi instalado como alternativa: 100 milhões de parâmetros, clonagem, português, 48 kHz, licença Apache 2.0. Os pesos foram fixados na revisão `44502f80dbf9743528fa921cc544d662c685ebec`; o tokenizer foi baixado em cópia local porque o cache por links simbólicos estava ilegível neste Windows.

## Amostras

- `amostra_MOSS_Nano_normalizada.wav`: 13,04s. O Whisper base reconheceu quase todo o texto, mas registrou “Oi” no lugar de “Hoje” e “Roxa” no lugar de “Rockstar”.
- `amostra_MOSS_Nano_ajustada_normalizada.wav`: 14,80s. A tentativa de facilitar “Rockstar Games” apresentou mais alterações na transcrição e não deve ser assumida como melhor.

A transcrição serve para detectar possíveis problemas; ela também pode errar. A escolha deve ser feita ouvindo as amostras. Ainda não há base para usar o perfil no roteiro completo. Para repetir um teste, abrir o VoiceStudio com `automacao/abrir_voicestudio.ps1` e executar `automacao/testar_clone_guibson.ps1 -Texto '...' -Saida 'caminho.wav'`.
