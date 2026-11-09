# L02 — configuração de voz para o Gemini

## Estilo recomendado

Copiar este texto para o campo de estilo da narração, não para o campo que será falado:

> Brazilian Portuguese documentary-analysis narration with a warm, grounded and subtly cinematic male voice. Curious and intimate, as if sharing a compelling character insight with an intelligent friend. Medium pace, clear articulation, natural conversational rhythm, and controlled emotional variation. Begin with immediate curiosity, grow slightly more tense during the failed-heist and conspiracy section, become observant and atmospheric while describing the official image, then finish thoughtful and inviting. Use restrained dry humor on the police joke. Avoid announcer voice, exaggerated suspense, melodrama, shouting, breathiness, or artificial enthusiasm. Pronounce Jason, Lucia, Leonida and Keys clearly; keep “GTA seis” natural in Brazilian Portuguese.

## Versão curta do estilo

Se a interface aceitar apenas uma instrução breve:

> Warm, grounded Brazilian Portuguese gaming-documentary narration; curious, conversational and subtly cinematic, with medium pace, clear articulation, restrained dry humor and controlled tension. Never sound like a trailer announcer.

## Aplicação

- Usar `03_NARRACAO_GEMINI.txt` como texto falado.
- Manter as tags em inglês e entre `< >`; elas indicam eventos pontuais, não palavras narradas.
- As tags foram limitadas a pausas, respirações e um único riso discreto. Se a voz escolhida exagerar `<chuckle>`, remover somente essa tag.
- Gerar primeiro um teste com a abertura e o quinto parágrafo. Eles revelam rapidamente se a voz está respeitando curiosidade, pausa e humor.
- Não colocar o bloco de estilo dentro da transcrição. Nos modelos Gemini TTS atuais, instruções sustentadas pertencem ao campo de estilo ou aos metadados da fala.

Referência técnica: [Google AI for Developers — Text-to-speech generation](https://ai.google.dev/gemini-api/docs/speech-generation).
