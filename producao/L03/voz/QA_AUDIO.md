# L03 — QA do áudio definitivo

Estado: liberado para montagem após validação técnica/ASR e aprovação auditiva humana do reparo 2. Data: 29/10/2026. O executor não fez escuta: tentativa de retornar áudio nativo recebeu `audio content omitted because you do not support audio input`. A confirmação de **encenar** vem exclusivamente do usuário, que ouviu especificamente o WAV de `reparo_v2` e respondeu: **“Ouço encenar; aprove esse trecho.”**

## Referência definitiva

- `narracao_normalizada.wav`: **330,680000 s / 5:30,680**, PCM signed 16-bit little-endian, **48.000 Hz, mono**, 15.872.640 amostras.
- SHA256: `700311CC62811827581F30CFF51B4070A5960B4875B7B0478339757746CD2636`.
- `palavras_alinhadas.json`, SHA256: `9607EEC8D27227B2ABE707E4F25B1A95DAC6562C8CC658EEB689B51D3FE8DC9E`.
- Medição autoritativa: `medicoes_integral_normalizado_definitivo.json`. Arquivos com `provisoria`, `provisorias`, `passagem1`, `reprocessada_nao_usada` ou outras medições anteriores não são a referência para montagem.

## Medições reais

| Medida | Integral útil bruta | WAV definitivo normalizado |
|---|---:|---:|
| Duração | 330,68 s | 330,68 s |
| Formato | PCM16 / 24 kHz / mono | PCM16 / 48 kHz / mono |
| Loudness integrado | -20,86 LUFS | **-16,84 LUFS** |
| Pico verdadeiro FFmpeg | -0,53 dBTP | **-1,48 dBTP** |
| LRA | 4,30 LU | 3,20 LU |
| Pico de amostra | consultar JSON bruto | -1,48767 dBFS |
| Amostras clipadas | 0 | **0** |

Normalização aplicada uma vez ao bruto definitivo por `automacao/producao.py normalize`, alvo -16 LUFS / -1,5 dBTP, com medição e aplicação internas em duas passagens. O resultado observado é cerca de -16 LUFS; não se afirma -16,00 exato. Pico verdadeiro medido arredondado 0,02 dB acima do alvo nominal, sem clipping. Houve teste adicional de renormalização; seu resultado está preservado em `narracao_reprocessada_nao_usada.wav` e não é usado.

FFmpeg decodificou o WAV completo durante loudness/silencedetect. Cabeçalhos WAV e contagens PCM foram verificados com `wave`; duração preservada na normalização. Detectados 68 intervalos abaixo de -40 dB por pelo menos 500 ms; maior 1,645 s. Não há cauda silenciosa longa. Pausas curtas abaixo de 500 ms não entram nessa contagem; duração da tag não é garantida por esse teste.

## Geração e preservação

Modelo efetivamente solicitado: `gemini-3.8-flash-tts`; voz: `voice_iagtq1gnk2br`; integração `automacao/gerar_narracao_gemini.ps1` com `.venv-gemini/Scripts/python.exe`. O wrapper recebeu apenas parâmetros opcionais StyleFile/OutputDir, mantendo os defaults existentes. Todos os dry runs confirmaram modelo, voz, estilo e lista explícita de entradas.

**Sete respostas WAV retornadas:** B01–B04 v1, B05 v2, reparos 1 e 2. O batch v1 foi interrompido após os quatro retornos; pode ter havido uma chamada B05 v1 em voo abortada, cujo custo não é confirmável. Não houve nova geração após o limite de duas tentativas de reparo. B01/B02 não foram regenerados. Todos os brutos, reparos rejeitados e cópias provisórias foram preservados.

Estilo v1 enviava direção extensa, separada do texto em `speech_metadata.style`. B01/B02 apresentaram continuação inventada após o texto solicitado. Não se atribui causalidade comprovada ao estilo; v2 curto suprimiu conteúdo futuro e encerrou B05 corretamente em “cidade?”.

## Aparo e emenda

| Bloco final | Offset integral | Duração útil | Tratamento |
|---|---:|---:|---|
| B01 / P1–3 | 0,00 s | 45,90 s | Última palavra pedida termina 45,46; corte em silêncio 45,526–46,265. Cauda inventada a partir de 46,12 descartada somente da cópia útil. |
| B02 / P4–7 | 45,90 s | 74,85 s | Última palavra termina 74,42; corte em silêncio 74,424–75,254. Cauda inventada a partir de 75,18 descartada somente da cópia útil. |
| B03 / P8–12 | 120,75 s | 87,81 s | Frase original 38,10–47,45 substituída pelo reparo 2 aprovado, 9,68 s; aumento 0,33 s. |
| B04 / P13–16 | 208,56 s | 61,52 s | Bruto preservado integralmente. |
| B05 / P17–19 | 270,08 s | 60,60 s | v2 preservado integralmente; sem continuação adicional no ASR. |

Emenda B03 com fades de 10 ms somente nas margens silenciosas; nenhuma sobreposição de fala. Frase completa, mesmas 23 palavras do roteiro. Reparo 1 e reparo 2 foram reconhecidos como “ensinar” pelo ASR. O usuário confirmou auditivamente **encenar no reparo 2**, que foi inserido. `reparo_B03.json` conserva aprovação, arquivo exato, fronteiras e delta. Verbo aprovado no integral: **163,29–163,75 s**, `human_confirmed`, evidência humana explícita e reconhecimento “ensinar” preservado em `asr_span`.

## Transcrição e alinhamento

ASR local `faster-whisper small`, CPU/int8, português, word timestamps, sem roteiro como prompt. Segunda leitura `base` de trechos direcionados, também sem roteiro. Duas tentativas iniciais concorrentes falharam por `mkl_malloc`; as revisões seguintes foram sequenciais e concluíram. Não se instalou modelo/dependência nem se usou ASR remoto.

- `palavras_asr.json`: 879 tokens ASR úteis, offsets reais e fonte de tempo, incluindo reconhecimento original do reparo aprovado.
- `palavras_alinhadas.json`: 893 palavras para legendas/âncoras; 841 correspondências exatas, 31 ambiguidades com estimativa explícita, 20 expansões numéricas e 1 confirmação humana.
- Seis palavras com duração zero no ASR receberam janela estimada de 30 ms com `timing_estimated_for_caption=true`; não representam alinhamento fonético forçado nem prova de fala.
- `paragrafos_alinhados.json`: 19 parágrafos com início/fim; `offsets_blocos_finais.json`: cinco offsets definitivos.
- `revisao_alinhamento.json` e ASRs de diagnóstico preservam divergências, em vez de ocultá-las no texto canônico.

O roteiro original continua com 894 palavras intactas. Para a legenda derivada, não se forçou o conectivo “E” antes de “isso muda”, ausente nas duas leituras ASR; “uma linguagem” foi ajustado a “a linguagem”, reconhecido pelos dois modelos. A pequena ambiguidade a/uma não justificou geração. A grafia canônica dos nomes e os anos por extenso têm procedência/estimativa marcada; os dois anos foram reconhecidos como 2002 e 1986. Dimez/Dimes, Vercetti, varanda/baranda, detector/detentor e guardar/acordar/engordar foram tratados como ambiguidades fonéticas do ASR, sem afirmar pronúncia confirmada pelo executor. Não há indício ASR de tags faladas, omissão de frase completa ou acréscimo restante após os aparos.

## Limites e integridade

A aprovação auditiva humana cobre a frase de reparo 2. A qualidade interpretativa, continuidade de timbre/volume nas junções e demais nomes não foram escutados pelo executor; foram avaliados tecnicamente e via ASR. Não se afirma escuta integral.

Fonte e direção editorial mantêm os hashes originais: `01_NARRACAO.txt` SHA256 `47AD0A356C31DB478580D3B25A74A298AC23E0789EC8514EB5C12F92ED5407AF`; `02_DIRECAO_E_FONTES.md` SHA256 `96AC4D63DB310C2F21F765CD06605963EFE05AD2F30B049D8DD32BCB03CCF875`. Nenhuma alteração em `producao.json`, roteiro ou direção editorial; nenhum upload/publicação.
