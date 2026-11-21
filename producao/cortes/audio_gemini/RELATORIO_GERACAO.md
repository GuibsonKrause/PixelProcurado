# Narrações dos Shorts — geração e validação

Geração concluída em 26/10/2026 com o modelo `gemini-3.8-flash-tts` e a voz personalizada `voice_iagtq1gnk2br`.

## Arquivos para edição

As cópias prontas para entrar na timeline estão em `normalizados/`. São WAV PCM 16-bit, mono, 48 kHz, normalizados com alvo de -16 LUFS e pico verdadeiro de -1,5 dBTP. Os arquivos originais retornados pela API permanecem na raiz desta pasta, em WAV PCM 16-bit, mono, 24 kHz.

| Roteiro | Duração | Loudness medido | Pico verdadeiro |
|---|---:|---:|---:|
| C01 | 1min19,92s | -17,00 LUFS | -1,49 dBTP |
| C02 | 1min18,08s | -16,65 LUFS | -1,49 dBTP |
| C03 | 1min20,64s | -16,85 LUFS | -1,49 dBTP |
| C04 | 1min16,92s | -16,90 LUFS | -1,49 dBTP |
| C05 | 1min23,96s | -16,74 LUFS | -1,49 dBTP |
| C06 | 1min19,96s | -16,40 LUFS | -1,49 dBTP |
| C07 | 1min20,44s | -16,81 LUFS | -1,48 dBTP |
| C08 | 1min18,24s | -16,86 LUFS | -1,49 dBTP |
| C09 | 1min19,64s | -16,72 LUFS | -1,49 dBTP |
| C10 | 1min30,08s | -16,68 LUFS | -1,46 dBTP |
| C11 | 1min23,76s | -16,85 LUFS | -1,49 dBTP |
| C12 | 1min23,24s | -16,84 LUFS | -1,45 dBTP |
| L01-R02 | 1min19,64s | -16,75 LUFS | -1,49 dBTP |
| L01-R03 | 1min30,72s | -16,95 LUFS | -1,49 dBTP |

Duração total: 19min05,24s.

## Validação realizada

- Os 14 arquivos têm cabeçalho WAV válido e um único canal de áudio.
- Nos brutos, os picos ficaram entre -1,00 e -1,68 dBFS; o maior silêncio contínuo abaixo de -45 dBFS ficou entre 1,20 e 1,95 segundo.
- Todos foram transcritos localmente com Whisper `base`. Dez casos com maior ambiguidade foram repetidos com `small`.
- Nenhuma tag `<short pause>`, `<breath>` ou `<chuckle>` apareceu como fala nas transcrições.
- A segunda passagem descartou a possível omissão detectada inicialmente em L01-R02. Não restou indício de frase inteira ausente.

## Pontos de escuta antes de travar a edição

O reconhecimento automático não comprova pronúncia. Ouvir especialmente:

- C06: a palavra “screenshots”.
- C08: conferir se o `chuckle` depois de “É uma iguana” ficou natural.
- C09: “Keys” e “Grassrivers”.
- C11: o trecho “onde Jason mora”.

As transcrições de controle estão em `asr/` e `asr_small/`. As métricas completas estão em `validacao_brutos.json` e `normalizados/validacao_normalizados.json`.

Para editar, usar os arquivos de `normalizados/`. Preservar os brutos para uma eventual comparação ou correção pontual.
