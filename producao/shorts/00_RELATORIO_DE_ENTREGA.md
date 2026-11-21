# Entrega dos Shorts

14 vídeos finais. Duração total dos arquivos: 1145.50s. Volume total dos MP4s: 187.6 MiB.

## O que foi validado

- Todos os MP4s decodificados integralmente sem erro.
- Vídeo H.264 em 1080×1920, 30 fps; áudio AAC em 48 kHz.
- Duração do stream de vídeo alinhada à narração, com diferença inferior a um quadro.
- As 14 cópias WAV são idênticas às narrações normalizadas aprovadas, verificadas por SHA-256.
- Áudio exportado comparado à voz original em cinco posições por vídeo; nenhuma faixa de trailer ou trilha comercial acrescentada.
- Legendas geradas com tempos por palavra, correções contextuais registradas em cada projeto.
- Capas JPG/PNG em 1080×1920; JPGs abaixo de 2 MB.
- Aberturas, regiões intermediárias e finais examinados em pranchas visuais. O acervo usado foi revisado em pranchas de imagens e amostras dos trechos de vídeo.

A verificação de áudio foi técnica e por transcrição; não equivale a uma audição humana integral ou a uma certificação subjetiva de dicção. Os relatórios prévios da geração Gemini continuam em producao/cortes/audio_gemini.

| ID | Duração | Quadros | MiB | LUFS integrados | Pico real dBTP | Correlação mínima |
|---|---|---|---|---|---|---|
| C01 | 79.933s | 2398 | 9.3 | -17.01 | -1.41 | 0.99996 |
| C02 | 78.100s | 2343 | 8.6 | -16.66 | -1.38 | 0.99995 |
| C03 | 80.667s | 2420 | 10.7 | -16.86 | -1.37 | 0.99997 |
| C04 | 76.933s | 2308 | 15.2 | -16.91 | -1.40 | 0.99996 |
| C05 | 83.967s | 2519 | 20.4 | -16.75 | -1.39 | 0.99997 |
| C06 | 79.967s | 2399 | 15.3 | -16.41 | -1.37 | 0.99997 |
| C07 | 80.467s | 2414 | 16.8 | -16.82 | -1.39 | 0.99996 |
| C08 | 78.267s | 2348 | 17.2 | -16.87 | -1.39 | 0.99996 |
| C09 | 79.667s | 2390 | 15.0 | -16.74 | -1.40 | 0.99996 |
| C10 | 90.100s | 2703 | 11.1 | -16.70 | -1.34 | 0.99997 |
| C11 | 83.767s | 2513 | 10.3 | -16.86 | -1.40 | 0.99997 |
| C12 | 83.267s | 2498 | 9.3 | -16.85 | -1.16 | 0.99994 |
| L01-R02 | 79.667s | 2390 | 11.9 | -16.77 | -1.38 | 0.99995 |
| L01-R03 | 90.733s | 2722 | 16.3 | -16.95 | -1.34 | 0.99994 |

## Reedição

A narração foi mantida integral. A montagem é híbrida: gráficos e entradas animadas do Remotion, composição e legendas em FFmpeg, exportação H.264/AAC. Onde um trecho de vídeo é mais curto que a fala, o último quadro é sustentado; esses casos estão identificados nos créditos. Não se transformou um screenshot em suposto gameplay.

Para mudar as escolhas de imagem, ajuste automacao/shorts_editorial.py. A composição gráfica fica em remotion/src/shorts-overlays.tsx. Os roteiros/tempos particulares estão nas pastas voz e projeto de cada Short. Os arquivos intermediários foram preservados.

Na raiz do projeto, com o ambiente local existente:

```powershell
.\.venv-gemini\Scripts\python.exe automacao/shorts_vertical.py prepare C08
.\.venv-gemini\Scripts\python.exe automacao/shorts_batch.py C08
.\.venv-gemini\Scripts\python.exe automacao/shorts_publicacao.py
```

Depois de alterações, repetir a inspeção visual e a validação antes de substituir o arquivo destinado ao upload. Não renumerar ou apagar acervo de outros episódios.

## Publicação

Os textos prontos, títulos alternativos, crédito de cada mídia e instruções do Studio ficam em publicacao. O registro de postagem está em CONTROLE_DE_PUBLICACAO.csv. Nenhum vídeo foi enviado ao YouTube.

A informação técnica do C05 foi reconfirmada na descrição pública do Trailer 2 no YouTube. O trecho pertinente e o método de consulta ficam em C05/projeto/fonte_descricao_trailer2.txt.
