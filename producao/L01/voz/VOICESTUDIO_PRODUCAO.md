# Narração do Pixel Procurado — VoiceStudio

Execução iniciada em 22/10/2026. Objetivo: voz masculina em português, clara e adequada a um canal de investigação e explicação de GTA.

## Configuração utilizada

- Aplicativo: VoiceStudio Electron 0.5.6, instalado para o usuário atual.
- Motor: Supertonic-3, síntese ONNX em CPU. Presets masculinos comparados: M1/M3/M4/M5; escolhido M5.
- Escolha editorial: comparar clareza, ritmo, pronúncia e estabilidade no mesmo texto. A preferência é relativa às amostras testadas, não uma afirmação de “melhor voz” entre todos os serviços.
- Texto: `../01_NARRACAO.txt` relativo à pasta deste documento; o arquivo original permanece preservado. A menção a 21/10 é a data da apuração descrita no roteiro, não a data de geração do áudio.
- Produção por parágrafos para permitir corrigir um trecho sem refazer todo o áudio.
- Não clonar pessoa real, contratar API de voz ou enviar o roteiro para síntese em nuvem.

## Licença e identificação

SDK Supertonic: MIT. Pesos: OpenRAIL-M, revisão fixada pelo VoiceStudio `724fb5abbf5502583fb520898d45929e62f02c0b`. Fonte: https://huggingface.co/Supertone/supertonic-3/blob/main/LICENSE.

A licença inclui restrições de uso e identificação de conteúdo gerado por máquina. Incluir na descrição do vídeo: **“Narração gerada por inteligência artificial, com roteiro e revisão editorial do Pixel Procurado.”** Não apresentar a voz como gravação de uma pessoa real.

## Validação antes da entrega

- Arquivos WAV decodificáveis, sem respostas de erro salvas como áudio.
- Mesmo preset e velocidade nos blocos.
- Correspondência entre texto-fonte e transcrição, com atenção a números, nomes e omissões.
- Duração real, pausas entre blocos, normalização e versão MP3 para escuta.
- Registrar escolha final, caminhos e limites da revisão ao concluir.

## Arquivos produzidos em 22/10/2026

- `narracao_normalizada.wav`: versão revisada com 484,601 segundos (8min05s), PCM 16-bit, mono, 48 kHz. Medições finais em `validacao_audio.json`.
- `narracao_M5.mp3`: versão para escuta, 192 kbps, duração conferida pelo decodificador.
- `voicestudio/narracao_M5_bruta.wav`: síntese original concatenada, preservada. `voicestudio/narracao_M5_revisada.wav`: versão com correções nos blocos 11 e 14.
- `voicestudio/blocos_M5_1.0/`: 19 parágrafos separados e seus parâmetros de geração. Semente 42, dez passos, velocidade 1,0, idioma pt, pausas de 0,32s entre parágrafos.
- `tempos_por_bloco.csv` e `voicestudio/timeline_narracao_revisada.json`: referência de tempos para edição da versão entregue.
- `validacao_audio.json`: medição de duração e volume; `checksums.json`: integridade das entregas.

O VoiceStudio também gerou uma amostra pela API, `voicestudio/teste_api_M5.wav` (5,503s). A narração longa foi produzida diretamente pelo mesmo SDK e pesos locais. A checagem de imports da versão 0.5.6 excedeu seu limite de 30s; abrir o aplicativo pelo lançador `automacao/abrir_voicestudio.ps1`, que usa o override documentado para o backend supervisionado. Não foi necessário alterar o instalador.

## Escolha: M5 — critério de seleção

Comparação feita com o mesmo texto em português, velocidade 1,0 e dez passos de síntese no SDK Supertonic 1.3.1, o mesmo motor integrado ao aplicativo. M1: 18,53s; M3: 15,46s; M4: 17,55s; M5: 18,53s. Estimativa de frequência fundamental mediana por autocorrelação: M1 137,8 Hz; M3 99,1 Hz; M4 119,2 Hz; M5 90,9 Hz. É uma medição aproximada de altura vocal, não uma nota de naturalidade.

M5 foi escolhida pela voz grave, ritmo moderado e preservação do texto na transcrição de conferência. M3 foi mais rápida; M4 produziu uma possível repetição em “informação oficial” na transcrição. A avaliação automática não substitui uma escuta humana de preferência e sotaque. As quatro amostras permanecem disponíveis para comparação.


## Revisão textual e limites

A primeira transcrição com Whisper small apresentou divergências. Uma segunda passagem com Whisper base nos blocos 3, 6, 9, 11, 14, 15, 16 e 18 recuperou corretamente a data, Xbox Series X e S, a conspiração criminosa em Leonida e frases que haviam sido omitidas ou alteradas pelo primeiro reconhecedor. Divergência de ASR não prova defeito na fala.

Foram regenerados os blocos 11 e 14: grafia fonética para Grassrivers e Port Gellhorn e tradução explícita do título An Extended Look para “Um Olhar Estendido, em tradução livre”. O texto original permanece intacto; as adaptações estão em voicestudio/revisao/adaptacoes.json. Na tela e na descrição, manter os nomes oficiais.

O SRT é transcrição automática para conferência, não legenda editorial aprovada. Nomes próprios e palavras estrangeiras ainda exigem escuta humana. Não foi realizada avaliação auditiva subjetiva pelo assistente; não se afirma sotaque brasileiro perfeito ou ausência absoluta de artefatos. A primeira versão dos arquivos está preservada em primeira_versao/.
