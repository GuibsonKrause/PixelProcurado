# Narração automática com Gemini TTS

Configuração fixa do projeto:

- Modelo: `gemini-3.8-flash-tts`
- Voz: `voice_iagtq1gnk2br`
- Idioma de desempenho: português do Brasil, orientado pelo texto, pelo estilo e pela voz criada
- SDK: `google-genai` em `.venv-gemini`
- Saída: WAV, normalmente PCM de 24 kHz e um canal

## Primeira configuração

Crie uma chave no Google AI Studio usando a mesma conta/projeto em que a voz foi criada. A assinatura de consumidor Gemini Pro não funciona como crédito automático da API; preços, cotas e eventual faturamento pertencem ao projeto da API.

No PowerShell, dentro da pasta do projeto:

```powershell
.\automacao\configurar_chave_gemini.ps1
```

O comando pede a chave com entrada oculta e a grava na variável de usuário `GEMINI_API_KEY`. A chave não é colocada nos arquivos do projeto.

## Gerar C02 e C03

```powershell
.\automacao\gerar_narracao_gemini.ps1
```

## Gerar todos os Shorts

```powershell
.\automacao\gerar_narracao_gemini.ps1 -Todos
```

## Validar sem gastar API

```powershell
.\automacao\gerar_narracao_gemini.ps1 -DryRun
```

Os WAVs são salvos em `producao/cortes/audio_gemini`. Cada geração é feita separadamente para facilitar a revisão e a regeneração de somente um corte.

O `voice_id` pertence ao projeto/conta que o criou. Uma chave de outro projeto pode retornar erro de voz não encontrada ou de permissão.
