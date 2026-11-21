# Expressões de narração — Gemini 3.8 TTS

Conferido em 29/10/2026 para `gemini-3.8-flash-tts`, usado pelo gerador local. Catálogo completo **das recomendações publicadas**, não promessa de todas as expressões possíveis.

Eventos ficam em `<...>`, em inglês, no TXT Gemini. O TXT limpo conserva apenas a fala. A duração das pausas precisa ser ouvida; não representa um número fixo de milissegundos. [Documentação da Gemini API](https://ai.google.dev/gemini-api/docs/speech-generation#vocal-bursts-and-non-speech-sounds).

| Expressões documentadas | Sentido aproximado |
|---|---|
| `<argh>` | Frustração |
| `<breath>`; `<heavy breath>`; `<exhales>` | Respiração; respiração pesada; expiração |
| `<cackle>`; `<cheer>` | Gargalhada estridente; comemoração |
| `<chuckle>` / `<chuckles>` | Risada curta |
| `<cough>`; `<cry>`; `<gasp>` | Tosse; choro; inspiração surpresa |
| `<giggle>`; `<groan>` | Risadinha; resmungo |
| `<growl>`; `<grunt>`; `<grr>`; `<hiss>` | Rosnado; grunhido; irritação; chiado vocal |
| `<laugh>` / `<laughter>` | Risada |
| `<moan>`; `<pant>` | Gemido; respiração ofegante |
| `<pff>` / `<phew>` | Reação vocal de desdém ou alívio, conforme contexto |
| `<scream>`; `<shout>`; `<shriek>` | Grito; exclamação alta; grito agudo |
| `<sigh>` / `<sighs>` | Suspiro |
| `<sneeze>`; `<snicker>`; `<snort>`; `<sob>` | Espirro; riso de deboche; bufada; soluço de choro |
| `<throat-clearing>`; `<tsk>`; `<whimper>` | Pigarro; estalo de reprovação; choramingo |
| `<whispers>` / `<whispering>` | Sussurro |
| `<yawn>` | Bocejo |
| `<short pause>`; `<long pause>` | Pausa curta; pausa longa |

## Aplicação editorial

Tom, sarcasmo, velocidade e volume sustentados pertencem ao campo Style (`speech_metadata.style`). Não usar instruções cênicas entre colchetes como se fossem eventos do 3.8. O estilo-base é curto; a identidade vem da voz configurada. [Guia de prompting do Google](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/text-to-speech/prompting-guide).

- Pausa curta: separar ideias ou deixar uma comparação chegar.
- Respiração: transição com mudança de assunto, sem marcar toda frase.
- Risada curta: cumplicidade ocasional; não comemorar cada piada.
- Suspiro/expiração: frustração ou mudança de ritmo com motivo no texto.
- Pausa longa: somente quando o silêncio tem função; evitada neste lote para não atrasar as entregas.
- Outras expressões: reservar para cenas que realmente as peçam. Não inserir tosse, gritos, gemidos ou choro para demonstrar o catálogo.

Não começar o vídeo com um efeito. Não colocar eventos depois da ponte final dos Shorts. Tags não entram em legendas. Antes de editar: ouvir a fala inteira, conferir palavras e eventos, ajustar excesso e medir duração. Esta revisão valida texto e sintaxe; a atuação ainda depende da geração e escuta.
