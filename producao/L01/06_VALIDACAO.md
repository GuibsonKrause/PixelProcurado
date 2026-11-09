# Validação local — atualizada em 22/10/2026

## Resultado

O pacote de pré-produção está pronto. Há um fluxo local executável de preparação, montagem simples e legendagem, e um teste real do motor Concat. **O vídeo L01 completo ainda não foi produzido.** A voz escolhida é M5 do Supertonic-3; os recursos visuais ainda precisam ser selecionados.

## Testes executados

| Componente | Evidência | Resultado / limite |
|---|---|---|
| FFmpeg | `testes/20261021-231455/resultado.json` | Normalização em duas passagens, imagem + áudio em MP4 H.264/AAC, derivado vertical; durações 3s e 2s verificadas |
| Validação de entrada | Mesmo relatório | Intervalo além da mídia, sobrescrita, mídia sem revisão e cobertura incorreta da voz rejeitados |
| Concat | `testes/concat-mcp.json` | Versão 0.2.8, MCP headless conectado, 42 ferramentas descobertas |
| Edição no Concat | `testes/concat-teste-231624/concat.json` | Projeto criado, cartela importada, inserida na timeline e projeto salvo |
| Exportação Concat | `testes/concat-teste-231624.mp4` e `concat-export-result.json` | Exportação de 5s, 1920×1080, estado `done`; MP4 decodificado e frame extraído |
| Voz de teste | `voz/TESTE_voz_windows.wav` | 110,49s dos quatro primeiros parágrafos usando Microsoft Maria; ritmo lento, apenas teste técnico |
| Transcrição | `voz/TESTE_voz_windows.srt` | Whisper base local produziu 15 segmentos; errou nomes, ano e algumas palavras |
| Correção textual | `voz/TESTE_voz_windows_corrigido.srt` | Corrigidos Rockstar, 2026 e erros evidentes contra o texto-fonte. Sincronização fina e quebra de linhas ainda precisam de revisão audiovisual |
| Capa | `arte/thumbnail_tipografica.png` | 1280×720, composição própria; inspecionada visualmente, sem corte de texto |
| Roteiro | `01_NARRACAO.txt` | 967 palavras: aproximadamente 6,2–6,9 min a 140–155 palavras/min, mais pausas. Não é duração medida da locução final |

## Instalação e compatibilidade

- `imageio-ffmpeg==0.6.0` instalado em `.production-tools/python`, sem modificar o Python global.
- Concat obtido do release oficial `v0.2.8`. SHA-256 do MSI conferido com o SHA256SUMS publicado: `dc24b7588ec7fe430223ccb06cb7fa54027382e4b8867557bc5515710fa3af98`.
- Instalação convencional falhou com erro de permissão em `C:/Program Files/Concat`; extração local concluída com código 0. O aplicativo não foi registrado como instalação global.
- Bibliotecas do curso têm extensões Python 3.12; o executável padrão é 3.14. O lançador usa o runtime 3.12 existente.
- Encontrada incompatibilidade entre a chamada de decodificação do faster-whisper e o PyAV local. Resolvida no script decodificando para PCM float32 com FFmpeg antes da transcrição; não foi necessário reinstalar o ambiente do curso.
- GPU detectada: Intel Iris Xe. Os testes de transcrição foram feitos em CPU, int8.

## Ainda não validado

- Episódio completo de 6–8 min com mídia oficial, várias camadas, música e voz final.
- Piloto editorial de 60–90s com cenas oficiais: os testes atuais são técnicos, com cartela e sinal/voz de referência.
- Interface gráfica completa do Concat, edição ao vivo por MCP ou integração persistente no aplicativo de chat.
- Modelos Remotion, instalação SupoClip ou serviço ViceScale.
- Direitos de cada imagem, clipe e trilha a selecionar; nenhuma autorização foi presumida por existir crédito.
- Upload, agendamento, monitoramento e desempenho do canal.

Não há cobrança contratada. Os processos de teste do Concat foram encerrados depois da execução. O VoiceStudio mantém um backend local enquanto o aplicativo está aberto.

## VoiceStudio — instalação validada em 22/10

VoiceStudio Electron 0.5.6 instalado no perfil do usuário, instalador oficial com SHA-256 conferido: `3d7ac1d6b54e7854ca7fff4dda838e402d1c5d31acc9656b1838432e29a97624`. Runtime Python 3.11.16 e motor Supertonic-3 instalados; endpoint de instalação retornou `succeeded` e `installed: true`. `/health` retornou versão 0.5.6 e CPU. `/engines/select` confirmou `active: supertonic3`.

Teste real de `/v1/audio/speech` com `voice: M5`, idioma `pt`: `voz/voicestudio/teste_api_M5.wav`, 5,503 segundos, 44.100 Hz, WAV decodificado. A narração longa usa diretamente o mesmo SDK Supertonic 1.3.1 para evitar depender do tempo de inicialização da interface. Detalhes da seleção em `voz/VOICESTUDIO_PRODUCAO.md`.

Narração revisada entregue em WAV PCM 16-bit/48 kHz mono e MP3 192 kbps: **484,601 segundos (8min05s)**. Medição final: -16,01 LUFS e -1,49 dBTP. As 19 partes e a primeira versão foram preservadas; duas partes receberam adaptações de pronúncia. Comparação por ASR feita com Whisper small e base; legenda automática continua sujeita à revisão de nomes próprios e sincronização. Não houve avaliação auditiva subjetiva pelo assistente. Relatório: `voz/validacao_audio.json`; tempos: `voz/tempos_por_bloco.csv`.
