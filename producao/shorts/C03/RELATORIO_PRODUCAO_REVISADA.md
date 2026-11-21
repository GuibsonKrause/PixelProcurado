# C03 — produção revisada

Produção iniciada em 29/10/2026 e concluída tecnicamente em 30/10/2026. Roteiro canônico preservado: `producao/cortes/C03_NARRACAO.txt`; cópia local idêntica por SHA-256. Gancho: “Esse abraço tem polícia no fundo.” Nenhum upload, agendamento ou acesso ao Postiz foi executado por este executor. `producao.json` pertence ao coordenador e não foi editado.

## Entregas

- MP4: `exportacoes/Pixel_Procurado_C03_Short_1080x1920.mp4`.
- SRT: `exportacoes/C03_legendas.srt`.
- WAV bruto: `voz/bruto/C03_narracao.wav`; cópia normalizada: `voz/narracao.wav`.
- Timeline editável: `projeto/timeline.json`; direção: `projeto/DIRECAO.md`.
- Capa master, JPG, arte-base e prompt: `publicacao/`.
- Título, descrição, comentário, tags, alternativas, tempos de consulta e fontes: `publicacao/00_GUIA_DE_PUBLICACAO.md` e TXT numerados.
- Versão anterior integral: `historico/v1_anterior_2026-10-29/` (voz, projeto, render, publicação e LEIA_ME).

## Narração e sincronismo

Uma chamada faturável autorizada pela integração local PowerShell/Gemini; modelo `gemini-3.8-flash-tts`, voz `voice_iagtq1gnk2br`, Style canônico de Shorts. WAV válido PCM16, 24 kHz mono, 75,760s. Normalização em uma cópia pelo utilitário aprovado: PCM16, 48 kHz mono, mesma duração; alvo −16 LUFS/−1,5 dBTP. Medição observada da cópia: −16,87 LUFS/−1,49 dBTP.

Primeiro sinal acima de aproximadamente −44 dBFS em 0,0126s: dentro do primeiro frame. ASR local small com marcações por palavra; gancho completo em 0,00–1,66s e próximo plano em 2,4667s. Pausas acima de 0,8s: aproximadamente 0,84–1,04s, em divisões da fala. Sem omissão material ou tag falada detectada. Seis ambiguidades pequenas estão registradas em `voz/resumo_validacao.json` e `projeto/revisao_alinhamento.json`; correções contextuais nas legendas não são prova de dicção perfeita. Validação por transcrição e medidas, sem alegação de escuta subjetiva integral.

## Edição

21 planos sincronizados e 40 legendas. 1080×1920/30 fps. Montagem híbrida: gráficos e contornos animados Remotion em sequências transparentes, composição/movimentos 2D/legendas no FFmpeg, H.264 Quick Sync e AAC 48 kHz. Sem música e sem áudio original de trailer.

Imagem local 13 de Jason e Lucia inspecionada diretamente em resolução de fonte 3840×2160: casal, sol entre os rostos, barcos policiais e helicóptero presentes. Uso deliberado da mesma imagem como objeto da análise, alternando recorte e quadro completo. Contornos mantêm câmera fixa. A comparação do guincho usa gráficos identificados como COMPARAÇÃO HIPOTÉTICA. Abertura mostra a evidência e destaca o barco. O último plano conecta “Porque...” ao gancho.

A capa anterior gerada foi inspecionada e reutilizada: permanece coerente com a nova fala e sua frase “OLHE ATRÁS / DO ABRAÇO.” complementa o título. Sem nova chamada de ImageGen. PNG/JPG 1080×1920; JPG abaixo de 2 MB. Montagem editorial identificada no pacote; não apresentada como captura oficial.

## QA técnica e visual

- Vídeo: 2273 frames, 75,766667s; diferença para WAV de apenas 0,006667s, inferior a um frame.
- Decodificação integral do MP4 sem erro. Mux sem avisos temporais pendentes.
- Continuidade exata dos planos em frames; cobertura integral da voz; limites de legenda válidos, sem sobreposição. Exposição mínima de 0,85s.
- AAC final: −16,88 LUFS, −1,38 dBTP, LRA 2,70 LU. A codificação elevou o pico em 0,11dB sobre o WAV normalizado; sem clipping. A leitura relevante é `input_*`, não o valor hipotético `output_*` do medidor loudnorm.
- Comparação com a cópia WAV normalizada em 0,3s, 18,94s, 37,88s, 56,82s e 72,76s: correlações entre 0,999962 e 0,999981.
- Amostras representativas antes do integral: planos 0,1,10,18; abertura e gráfico da piada inspecionados em tamanho nativo.
- Amostras do arquivo final: uma por cada um dos 21 planos, mais sete da QA base. Pranchas `projeto/qa/todos_os_planos.jpg` e `contato.jpg`; frames nativos `plano_00.jpg` a `plano_20.jpg`. Inspeção é amostragem visual, não revisão de todos os frames em movimento.
- Correção localizada após primeira QA: texto gráfico do plano16, em 60,3s, reduzido a “RECORTE: / MAIS AFETO.” para impedir toque no topo da imagem; apenas esse overlay/plano foi refeito, seguido de remux e nova QA integral.

Resultados e hashes finais: `projeto/qa/validacao_final.json` e `checagens_adicionais.json`. A revisão editorial independente final é responsabilidade do coordenador.

## Arquivos de automação

Novo `automacao/produzir_c03_revisado.py`: direção exclusiva do episódio e chamadas aos utilitários existentes; comandos prepare/sample/render/qa. Nenhum script compartilhado foi modificado. Para overlays, executar `node render-shorts-overlays.mjs C03` com diretório corrente `remotion/`.

Scripts específicos dentro de C03: `projeto/publicacao_revisada.py` gera somente o pacote do episódio; `projeto/qa_revisada.py` confere continuidade/legendas, captura todos os planos e calcula hashes. Asserts do renderer e checks específicos executados. Uma tentativa inicial de regenerar o overlay corrigido com diretório corrente errado retornou ENOENT e foi repetida corretamente em `remotion/`; nenhuma alteração da fonte ou mídia ocorreu nessa falha.

Os arquivos de publicação registram páginas oficiais consultadas sobre miniaturas, capítulos, tags, telas finais e IA. Não foi prometido desempenho, licença de imagens ou ausência de reivindicações.

Perfil solicitado para este executor: gpt-6.1-sol/medium; valores efetivos não confirmados pela ferramenta. Nenhuma subdelegação realizada pelo executor.
