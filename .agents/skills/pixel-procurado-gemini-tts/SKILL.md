---
name: pixel-procurado-gemini-tts
description: Gerar, revisar e preparar narrações do Pixel Procurado com a voz personalizada do Gemini TTS. Use para narrar Shorts ou vídeos longos, testar interpretação, validar WAVs e preparar áudio aprovado para a edição; não use para montagem visual ou pacote de publicação.
---

# Pixel Procurado — Gemini TTS

Use a integração local do projeto para manter a mesma voz e os mesmos controles expressivos entre episódios.

## Configuração aprovada

- Modelo: `gemini-3.8-flash-tts`.
- Voz: `voice_iagtq1gnk2br`.
- Idioma de desempenho: português do Brasil, orientado pelo texto, pela voz e pelo campo Style.
- Estilo dos Shorts: `producao/cortes/00_ESTILO_GEMINI_SHORTS.txt`.
- Gerador: `automacao/gemini_tts.py`.
- Atalho PowerShell: `automacao/gerar_narracao_gemini.ps1`.
- Saída padrão: `producao/cortes/audio_gemini/`.

Localize a raiz do projeto pelo arquivo `automacao/gemini_tts.py`. Se a integração não existir no projeto atual, informe a ausência em vez de reconstruir ou instalar dependências sem necessidade.

## Roteiros e expressões

Preserve o roteiro limpo para legendas e revisão editorial. Grave comandos do Gemini em uma versão separada com sufixo `_GEMINI.txt`.

- Direção persistente pertence ao campo Style.
- Eventos locais podem usar tags como `<short pause>`, `<long pause>`, `<breath>` ou `<chuckle>`.
- Prefira pausas e expressão contida. Use vocalizações somente quando combinarem com o sentido da frase.
- Não copie as tags para as legendas.
- Gere cada peça separadamente quando uma correção isolada puder evitar repetir custos e revisão.

## Interpretação para a edição V2

- Para criar ou revisar o texto antes da locução, use `pixel-procurado-roteiro`. Para uma revisão somente visual, reutilize a narração aprovada.
- Use uma conversa próxima e curiosa, com energia variada, clareza nos fatos e entrega seca no fim da piada. Um sorriso discreto nas comparações e pausas por sentido ajudam a marcar as viradas. Reserve respirações e risadas para pontos justificados.
- Comece pela fala do gancho, sem respiração, risada ou silêncio anterior. Meça a abertura na locução real. Se o gancho não couber naturalmente em cerca de três segundos, sinalize o trecho para ajuste editorial.
- Dê nitidez à palavra ou frase que dispara a troca de cena e mantenha a cadência natural. A edição sincroniza o B-roll e calcula a permanência dos cards. Use pausas quando a fala pedir.
- Quando preparar áudio para montagem, entregue a narração limpa, o WAV aprovado e, quando disponível, o alinhamento por palavras com timestamps. Marque dúvidas de nomes e pronúncia para revisão antes de sincronizar as legendas.

## Autenticação

A integração lê `GEMINI_API_KEY` da variável de usuário do Windows. Nunca exiba, registre ou grave a chave em arquivos. Não peça que o usuário cole a chave no chat.

Se a variável estiver ausente, oriente o usuário a executar, na raiz do projeto:

```powershell
.\automacao\configurar_chave_gemini.ps1
```

O `voice_id` precisa estar acessível ao projeto associado à chave. Um erro de voz não encontrada pode indicar projeto incorreto, mesmo com autenticação válida.

## Geração

Para um roteiro específico:

```powershell
.\automacao\gerar_narracao_gemini.ps1 -Roteiros 'producao/cortes/C02_GEMINI.txt'
```

Para C02 e C03, o atalho sem argumentos usa ambos. Use `-Todos` somente quando o usuário pedir todas as narrações. A geração é uma chamada faturável; um pedido explícito para gerar o áudio já autoriza a chamada necessária.

## Validação obrigatória

Antes de declarar sucesso:

1. Confirme que o processo terminou sem erro e que o arquivo começa como WAV válido.
2. Meça duração, codec, taxa de amostragem e canais. A resposta atual costuma ser PCM 16-bit, 24 kHz, mono, mas registre o formato observado.
3. Confira picos, silêncios anormais e pausas produzidas pelas tags.
4. Transcreva localmente para detectar palavras omitidas, tags faladas ou pronúncias ambíguas. Trate divergências do ASR como sinais para escuta, não como prova automática de erro da voz.
5. Entregue o WAV por link local e, quando útil, incorpore o áudio na resposta para audição.

O arquivo bruto da API é o teste de interpretação. Quando o áudio for aprovado para entrar no vídeo, normalize uma cópia com `automacao/producao.py normalize`, preservando o original. Use o padrão do projeto de `-16 LUFS` e pico verdadeiro de `-1,5 dB`.

## Relato

Informe o roteiro, modelo, voz, duração e formato realmente obtidos. Aponte trechos que merecem escuta quando a conferência automática detectar ambiguidade. Não afirme que a pronúncia ficou correta apenas porque a API retornou um arquivo.
