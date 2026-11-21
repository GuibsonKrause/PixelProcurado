# Automação de produção — operação local

## Fluxo escolhido

Pesquisa e decisão editorial → roteiro → voz revisada → normalização → imagens selecionadas → montagem → legendas a partir do master final → revisão → upload manual → derivados → avaliação.

O maior ganho agora vem de repetir preparação, exportação e identidade. Selecionar uma cena que sustente uma afirmação e julgar se uma teoria foi apresentada corretamente continuam exigindo revisão editorial.

## Ferramentas e estado real

| Ferramenta | Papel | Estado nesta entrega |
|---|---|---|
| FFmpeg via imageio-ffmpeg 0.6.0 | Tratar áudio, montar MP4, converter vertical e cortar intervalos | Instalado localmente em `.production-tools/python`; montagem e cortes testados |
| Python 3.12 do runtime existente | Executar scripts | Reutilizado; o Python 3.14 padrão não é compatível com as bibliotecas do curso |
| faster-whisper / base | Gerar SRT em português | Ambiente e modelo do curso reaproveitados; teste descrito em `06_VALIDACAO.md` |
| Concat 0.2.8 | Editor com projeto revisável e controle MCP | Cópia local extraída do MSI oficial; handshake, criação, importação, timeline, salvamento e exportação curta testados |
| Voz Windows Maria | Testar entrada de áudio em PT-BR | Amostra técnica gerada; não escolhida como voz editorial do canal |
| VoiceStudio 0.5.6 | Voz local com Supertonic-3 | Instalado e API testada em CPU; voz masculina escolhida: M5, português, velocidade 1,0 |
| Remotion 4.0.538 | Animações e templates em React | Instalado em `remotion/`; composição 1920×1080/30 fps reconhecida e render de cinco segundos concluído |
| SupoClip | Sugerir cortes e gerar versões verticais | Não instalado. Para três cortes planejados, o script local evita montar agora serviços, contas e dependências extras |
| ViceScale | Alternativa comercial de produção/distribuição | Não contratado nem testado; não é dependência deste episódio |

Referências atuais: [Concat](https://github.com/jub0t/Concat), [MCP](https://github.com/jub0t/Concat/blob/main/docs/MCP.md), [VoiceStudio](https://github.com/debpalash/VoiceStudio), [Remotion](https://www.remotion.dev/docs/), [SupoClip](https://github.com/FujiwaraChoki/supoclip). Capacidades anunciadas não equivalem a integração validada neste computador.

## Comandos prontos

### VoiceStudio e narração

Abrir pelo comando `./automacao/abrir_voicestudio.ps1`. O lançador contorna o tempo limite da checagem inicial da versão 0.5.6 neste computador. Aguarde alguns minutos na primeira abertura. O motor TTS selecionado é Supertonic-3; escolha o preset **M5**, idioma português e velocidade **1,0**.

Para repetir a síntese pelo aplicativo: `./automacao/narrar.ps1 full --voice M5 --speed 1.0`. É necessário que o VoiceStudio esteja aberto. Alternativa independente do tempo de abertura da interface: acrescentar `--sdk`, que usa diretamente o mesmo motor local. Os blocos ficam em `voz/voicestudio/blocos_M5_1.0/`, com parâmetros registrados em JSON.

Os comandos reutilizam blocos existentes: para outro roteiro, use uma pasta de produção nova e ajuste os caminhos do script; não reutilize a pasta L01 com texto alterado. A concatenação rejeita saída existente para preservar o áudio anterior.

O script `automacao/finalizar_narracao.py`, executado com o Python 3.12 indicado abaixo, normaliza a locução, exporta MP3 e gera transcrição Whisper small. As saídas são `voz/narracao_normalizada.wav`, `voz/narracao_M5.mp3` e `voz/narracao_M5_transcricao.srt`. O relatório `voz/VOICESTUDIO_PRODUCAO.md` registra escolha e limites da avaliação.

No PowerShell, a partir da pasta `GamePlay`, usar o lançador abaixo: ele escolhe o Python 3.12 compatível. Não usar simplesmente `python` neste computador para as funções que dependem do ambiente do curso.

```powershell
# Inspecionar duração e trilhas
./automacao/producao.ps1 probe producao/L01/voz/narracao.wav

# Normalização em duas passagens (gera WAV; não substitui o original)
./automacao/producao.ps1 normalize producao/L01/voz/narracao.wav producao/L01/voz/narracao_normalizada.wav

# Após finalizar os cortes: SRT do master realmente publicado
./automacao/producao.ps1 transcribe producao/L01/exportacoes/L01_master.mp4 producao/L01/exportacoes/L01_legendas.srt

# Montagem simples por manifesto preenchido
./automacao/producao.ps1 assemble producao/L01/projeto/montagem.json producao/L01/exportacoes/L01_master.mp4

# Exemplo de intervalo: SUBSTITUIR 35 e 75 pelos tempos reais escolhidos
./automacao/producao.ps1 clip producao/L01/exportacoes/L01_master.mp4 producao/L01/exportacoes/C01_vertical.mp4 --start 35 --end 75 --vertical

# Gerar SRT de cada corte, com timestamps começando no próprio corte
./automacao/producao.ps1 transcribe producao/L01/exportacoes/C01_vertical.mp4 producao/L01/exportacoes/C01_vertical.srt
```

Esses comandos de produção dependem dos arquivos reais ainda não gravados/selecionados. As amostras de teste estão em `testes/` e `voz/TESTE_voz_windows.*`. O SRT é uma base para revisão: corrigir principalmente nomes próprios, pontuação e divisões longas. Não há destaque automático palavra por palavra.

## Como preencher o manifesto

Copiar `projeto/montagem.exemplo.json` para `projeto/montagem.json`. Caminhos são relativos à pasta do manifesto. `voice` aponta para a voz final. Cada item de `clips` contém:

- `file`: mídia existente; `kind`: `image` ou `video`.
- `start`: entrada no vídeo bruto em segundos; imagens não precisam desse campo.
- `duration`: duração da cena na timeline. A soma deve cobrir a narração, tolerância de 0,25s.
- `source`: origem concreta; `use_reviewed`: marcar `true` somente depois da avaliação do recurso.

O montador cria cenas em 1920×1080/30 fps, encaixa a imagem inteira, remove o som dos clipes de apoio e usa a voz como áudio. Ainda não adiciona música, zoom, setas, títulos ou legendas embutidas. Para esses ajustes, abrir o resultado no Concat e acrescentar as camadas; o manifesto é independente, não um projeto nativo do Concat.

O script rejeita saída existente, duração inválida, cenas além do bruto, falta de arquivo e mídia sem origem/revisão. Não seleciona cenas sozinho, não determina licenças e não publica. Se uma execução falhar no meio, pode sobrar uma saída parcial: conferir e usar outro nome para nova exportação.

## Abrir Concat

Executável local: `GamePlay/.production-tools/concat-portable/PFiles64/Concat/concat.exe`.

A instalação MSI em `Program Files` falhou por falta de permissão (erro 1303/1603). A extração local funcionou e seu motor foi testado. Não alteramos políticas de segurança, não registramos um MCP global e não comprovamos o comportamento de todas as funções da interface gráfica.

O protocolo pode ser acessado por `concat.exe --mcp headless`. O script `automacao/testar_concat.py` demonstra o handshake e grava os schemas em `testes/concat-schemas.json`. A opção `--export` cria um projeto novo com cartela e exporta cinco segundos. O arquivo `testes/concat-export-result.json` registra o resultado da execução.

Para automação futura da edição: criar projeto → importar mídia → inserir na timeline → ajustar cenas e títulos → salvar → exportar → esperar conclusão → inspecionar MP4. Usar os schemas retornados pela versão instalada. O teste de cinco segundos não comprova ainda o desempenho de um episódio com dezenas de camadas.

## Prompts reutilizáveis

**Apuração:** “Use apenas as fontes abaixo. Monte afirmação, evidência, URL, data e limite. Separe fato, interpretação e hipótese. Aponte contradições e anúncios novos. Não transforme ausência nesta seleção em ausência em toda a internet.”

**Roteiro:** “Escreva para o Pixel Procurado, investigador de GTA. Uma pergunta central; primeira entrega nos 15 segundos iniciais; três a cinco blocos de evidência, explicação e consequência; uma conclusão e uma pergunta final. Não acrescente fatos fora da tabela validada. Marque a fonte fora do texto de locução.”

**Montagem:** “Use a voz final como referência. Para cada bloco, indique o arquivo de mídia, entrada, duração, origem e função: prova ou ilustração. Preserve nomes e números. Não preencha falta de material com cenas desconexas. Gere proposta revisável antes de renderizar.”

**Cortes:** “Proponha três trechos autônomos da transcrição final, com pergunta, contexto e resposta. Informe início/fim reais, duração e necessidade de reenquadramento. Não invente nota de viralidade nem timestamp. Se nenhum intervalo funcionar, proponha uma regravação curta.”

**Revisão:** “Compare título, thumbnail, roteiro, fontes e legendas. Liste só divergências concretas, com correção proposta. Verifique se uma hipótese aparece como fato quando isolada em um corte.”

## Próxima camada de automação

Depois de dois vídeos: medir tempo por etapa; automatizar o gargalo observado. A voz já dispõe de síntese local por blocos com Supertonic-3. O Remotion está instalado e tem uma composição-base validada em `remotion/src/Root.tsx`; ela pode evoluir para cartelas, títulos e legendas reutilizáveis. Se seleção de cortes for o gargalo, piloto SupoClip com transcrição local. Para distribuição, começar com os agendadores das próprias plataformas; integração externa só quando contas e destino estiverem definidos.

Não foi criada tarefa agendada, monitor nem automação de publicação. O backend do VoiceStudio funciona localmente enquanto o aplicativo está aberto. Nenhuma assinatura ou crédito pago foi adquirido. Os scripts processam mídia local.
