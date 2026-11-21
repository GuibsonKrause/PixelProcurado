---
name: pixel-procurado-producao-completa
description: Produzir um video completo do Pixel Procurado a partir de um roteiro ja existente indicado pelo usuario, encadeando narracao Gemini, alinhamento, selecao de midia, edicao, animacoes, legendas, thumbnail e pacote para YouTube. Use quando o usuario disser qual roteiro ou video quer produzir ou retomar; nao use para escrever ou reescrever o roteiro.
---

# Pixel Procurado - producao completa

Transforme o roteiro indicado em um pacote pronto para o usuario publicar. O comando que invoca esta skill autoriza a execucao continua das etapas necessarias, inclusive a chamada faturavel do Gemini TTS e a geracao da arte da thumbnail. Nao autoriza upload, publicacao, comentario ou alteracao da conta do YouTube.

## Entrada

Aceite um ID, caminho, titulo ou descricao distintiva, por exemplo:

- `$pixel-procurado-producao-completa L03`
- `$pixel-procurado-producao-completa faca o video do roteiro sobre Vice City`
- `$pixel-procurado-producao-completa retome C07`

O roteiro ja existe. Nao crie, resuma, expanda nem melhore seu texto. Correcoes indispensaveis de erro factual ou pronuncia devem ser propostas separadamente e nunca aplicadas silenciosamente ao roteiro original.

## Modelos, esforco e delegacao (Economia estrita de Usage)

Priorize qualidade maxima com consumo minimo de cota (usage).
- **No Antigravity (`invoke_subagent`)**: NUNCA use `Model="inherit"` para tarefas operacionais quando o chat principal estiver em um modelo caro (`pro`). Defina explicitamente `Model="flash_lite"` para execucao de scripts/validacoes deterministicas, `Model="flash"` para trabalho criativo/tecnico padrao (tags TTS, timeline padrao V2, implementacao da edicao, composicao de thumbnail e textos de publicacao) e reserve **`Model="pro"` exclusivamente** para:
  1. **Direcao de montagem inedita/complexa** (somente quando o episodio nao tiver direcao previa e exigir decisoes visuais dificeis — para episodios e Shorts que seguem o padrao V2 e o catalogo, use `Model="flash"`).
  2. **Revisao final independente** (inspecao visual real das folhas de contato, frames, legendas, capa e audio).
- **No Codex (`collaboration.spawn_agent`)**: Use `gpt-6.1-sol` (`low` ou `medium`) na rotina e reserve `gpt-6-astra` com esforco `high` apenas para decisoes visuais dificeis ineditas e para a revisao editorial final.
- **No Claude Code (ferramenta `Agent`)**: equivalencia da tabela abaixo — `flash_lite` → `model: "haiku"`; `flash` → `model: "sonnet"`; `pro` → `model: "opus"` (somente direcao inedita/complexa e revisao final independente). Se o Opus estiver indisponivel ou sem cota, use `model: "fable"` como reserva apenas nessas mesmas etapas (custa ~2x o Opus; nunca em tarefas operacionais). Sempre informe `model` explicitamente em subagentes operacionais. A thumbnail nao tem gerador de imagem no Claude: veja `pixel-procurado-thumbnails`.

| Etapa | Antigravity (`Model`) | Codex (`model` / `reasoning_effort`) | Entrega e responsabilidade |
|---|---|---|---|
| Coordenacao | Chat principal (leve) | `gpt-6.1-sol` / `medium` | Passagem entre etapas e escrita unica em `producao.json` |
| Descoberta e organizacao | `flash_lite` | `gpt-6.1-sol` / `low` | Roteiro correto, inventario de entradas e artefatos reaproveitaveis |
| Direcao da narracao | `flash` | `gpt-6.1-sol` / `medium` | Versao Gemini e direcao de pausas, enfase e ritmo |
| Execucao e validacao do audio | `flash_lite` | `gpt-6.1-sol` / `low` | WAV, normalizacao, transcricao ASR e medicoes |
| Direcao da montagem (padrao V2 / Shorts) | `flash` | `gpt-6.1-sol` / `medium` | Selecao contextual pelo catalogo e cards V2 em estrutura validada |
| Direcao da montagem (apenas inedita/dificil) | `pro` | `gpt-6-astra` / `high` | Somente decisoes novas e dificeis sem direcao previa |
| Implementacao da edicao | `flash` | `gpt-6.1-sol` / `medium` | Composicao, animacoes Hyperframes/Remotion, legendas e amostra |
| Render e verificacao tecnica | `flash_lite` | `gpt-6.1-sol` / `low` | MP4, SRT, decodificacao e verificacoes executadas por scripts |
| Direcao e composicao da thumbnail | `image-generator` + `flash` | `imagegen` + `gpt-6.1-sol` / `medium` | Arte-base via gerador de imagem e composicao via `compose_thumbnail.py` |
| Textos de publicacao | `flash` | `gpt-6.1-sol` / `medium` | Titulo, descricao, capitulos, tags, comentario e guia |
| Envio Postiz + Cloudflare R2 (se autorizado) | `flash_lite` | `gpt-6.1-sol` / `low` | Stage no R2, upload/agendamento Postiz e manifesto JSON |
| Revisao final independente | `pro` | `gpt-6-astra` / `high` | Uma unica revisao independente do pacote pronto, com evidencias e lista objetiva de correcoes |

### Como aplicar os perfis

- A skill nao altera o modelo ou esforco do chat principal. Use o principal para coordenar e executar rotinas compativeis, sem criar outro coordenador apenas para reproduzir a tabela ou por nao conhecer seu esforco efetivo. Se ele estiver em modelo mais caro, registre essa limitacao e delegue o trabalho substancial ao Sol, mantendo o principal somente na entrega e nas decisoes necessarias. Nao afirme que houve troca do modelo do chat.
- Crie subagentes apenas para trabalho concreto que justifique contexto separado:
  - No **Antigravity**: use `invoke_subagent` com `TypeName="self"` (para execução, montagem, render ou revisão independente), `TypeName="research"` (para pesquisa/inventário read-only) ou `TypeName="image-generator"` (para gerar `thumbnail_base_gerada.png`).
  - No **Codex**: use `collaboration.spawn_agent`, valores da tabela e `fork_turns="none"`. Prefira `default` ou `worker`.
  Agrupe tarefas compativeis no mesmo executor; nao crie um agente para cada etapa, para aguardar arquivos ou apenas comunicar andamento. Nenhum executor cria outro coordenador.
- Reutilize um agente para novas etapas do mesmo perfil quando o contexto for adequado. Se modelo ou esforco mudar, crie outro agente: enviar uma mensagem a um agente existente nao muda esses parametros. Mantenha a revisao final em um agente separado de quem planejou ou implementou o video.
- O coordenador e o unico escritor de `producao.json`. Informe a cada executor que compartilha o projeto com outros agentes, quais arquivos pode alterar, quais sao somente leitura e que deve preservar o trabalho alheio. Os executores devolvem caminhos, medicoes, problemas e evidencias ao coordenador.
- Como `fork_turns="none"` nao herda a conversa, forneca a cada agente a raiz absoluta do projeto, ID/formato, roteiro selecionado, caminhos das skills aplicaveis, entradas validadas, decisoes anteriores, destino dos arquivos e criterios de conclusao. Encaminhe o escopo autorizado de geracao e seus limites; somente o executor designado pode disparar cada chamada faturavel.
- Leia cada skill e referencia necessaria uma vez por contexto e quando a etapa chegar. Encaminhe os caminhos ao executor responsavel; nao cole manuais, roteiros e logs inteiros em todas as mensagens. Cada agente deve carregar as instrucoes aplicaveis ao trabalho que executa e cumprir as exigencias de leitura do ambiente.
- Respeite as dependencias: audio validado antes da timeline; timeline antes da implementacao; amostra revisada antes do render integral; tempos finais antes dos capitulos. Paralelize somente tarefas independentes com arquivos separados, dentro dos slots disponiveis.
- A revisao final inspeciona os artefatos reais e registra trechos/timecodes e frames examinados. Resultado de ASR ou resumo de outro agente nao comprova escuta ou revisao visual. O revisor parte do modelo `py -3.12 automacao/validar_revisao.py <pasta> --modelo <video.mp4> [--cards cards.json]`, salva `<pasta>/REVISAO_FINAL.json` com as evidencias (trechos de audio, frames salvos em imagem, amostras de legenda, previa reduzida da capa, problemas) e o coordenador so marca `revisao_final` como validado quando `py -3.12 automacao/validar_revisao.py <pasta>` sair com codigo 0. Uma aprovacao sem esse relatorio, ou com sha256 diferente do artefato atual, nao vale. Encaminhe correcoes ao executor responsavel e revalide os trechos alterados antes de concluir.
- Se o ambiente rejeitar um modelo, esforco ou delegacao (ou se o usage da cota Gemini for atingido):
  - Está **autorizado o fallback para a família Claude**: use **Claude Sonnet 5.5** como substituto direto para manter a produção rodando sem interrupção (com consumo moderado de usage).
  - Use **Claude Opus 5.5** exclusivamente como última alternativa ou para etapas de alta complexidade/revisão profunda.
  - Registre no checkpoint `producao.json` a alternância de modelo e informe o motivo. Continue a produção sem bloquear o fluxo.

### Economia durante a execucao e a retomada

- Use no maximo dois executores ativos alem do principal, e menos quando as etapas forem sequenciais. Nao mantenha especialistas caros ativos enquanto Gemini, ASR ou render trabalham. Aguarde processos com as ferramentas de espera e intervalos de 30-60 s, sem rodadas de raciocinio para descobrir repetidamente que nada mudou.
- O Astra recebe uma tarefa delimitada e os artefatos relevantes: decidir a direcao visual quando ela ainda nao existe ou revisar uma versao final. Encerre a tarefa apos a entrega e execute correcoes objetivas com Sol. Uma retomada ou ajuste de timecode nao exige chamar novamente o diretor Astra. Em episodios simples com direcao reutilizavel, Sol medium pode preencher a timeline, reservando Astra high para a revisao final.
- Preserve independencia na revisao: se Astra planejou a montagem, use outro contexto Astra high para a revisao final. Agrupe video, legendas e capa em uma unica revisao, com amostras representativas, metadados e relatorios. Reinspecione apenas os trechos corrigidos, salvo mudanca estrutural. Nao confunda amostragem com revisao integral.
- Executar FFmpeg, medir audio, transcrever, testar continuidade e conferir hashes sao tarefas de ferramentas/scripts. Use seus resultados; nao substitua checks deterministas por deliberacao longa ou delegacao cara. Nao repetir ASR, inspecoes ou validacoes ja suficientes sem evidencia nova.
- Na retomada, leia primeiro o checkpoint e os relatorios curtos. Compare entradas/assinaturas apenas onde necessario. Um perfil novo nao invalida audio, thumbnail, timeline ou render ja validado. Registre a mudanca de perfil nas proximas etapas, preservando o historico real das anteriores.
- Agentes antigos nao mudam de modelo/esforco por mensagem. Se um agente anterior tem perfil mais caro que o novo, nao o reative: use o principal ou um executor no novo perfil com um resumo curto do estado salvo. Reutilize agentes existentes somente quando o perfil continuar adequado.
- Saidas e mensagens entre agentes devem conter caminhos, resultado, evidencias essenciais e proxima acao; nao recapitular toda a producao. Informe ao usuario marcos concretos e bloqueios, evitando narracoes repetidas de status.

Os perfis controlam o raciocinio do Codex. A sintese da voz continua no Gemini configurado, a arte na ferramenta de imagens e a renderizacao segue a skill `pixel-procurado-video`. O teto desta skill e `gpt-6-astra` com `high`: nao use `xhigh`, `max` ou `ultra` sem nova instrucao explicita do usuario. Esta politica reduz trabalho desnecessario, mas nao garante uma porcentagem de economia nem altera limites compartilhados da conta.

## Descoberta segura

1. Localize a raiz do projeto pelo arquivo `automacao/gemini_tts.py` e trabalhe nela.
2. Resolva primeiro um caminho fornecido pelo usuario. Sem caminho, procure com `rg` e priorize:
   - `producao/<ID>/01_NARRACAO.txt` para episodios longos;
   - `producao/cortes/<ID>_NARRACAO.txt` para cortes e Shorts ainda nao produzidos;
   - `producao/shorts/<ID>/voz/NARRACAO.txt` apenas para retomar uma producao ou quando a fonte anterior nao existir.
3. Ignore por padrao pastas `historico`, transcricoes ASR e copias de publicacao. Mostre opcoes somente se duas fontes continuarem materialmente ambiguas.
4. Infira Short vertical para IDs `Cxx`, reservas de corte e roteiros em `producao/cortes`; infira video longo 16:9 para IDs `Lxx`. Uma instrucao explicita do usuario prevalece.

## Pasta e checkpoint

Use a estrutura existente do projeto:

- Short: `producao/shorts/<ID>/`
- Longo: `producao/<ID>/`

Crie e atualize `<pasta>/producao.json` somente com `automacao/checkpoint.py` (formato fixo `automacao/schemas/producao.schema.json`, etapas na ordem `narracao`, `alinhamento`, `montagem`, `render`, `thumbnail`, `publicacao_pacote`, `distribuicao`, `revisao_final`, estados `pendente|em_andamento|validado|bloqueado`):

- Novo: `py -3.12 automacao/checkpoint.py novo <pasta> --id <ID> --formato longo|short|longo_e_short --roteiro <caminho>`
- Apos cada etapa: `py -3.12 automacao/checkpoint.py etapa <pasta> <etapa> --status validado [--sub longo|short] --campo artefatos.<nome>=<caminho> --campo medicoes.<nome>=<valor> --campo executor.model_solicitado=<modelo>`
- Antes de retomar e antes de concluir: `py -3.12 automacao/checkpoint.py validar <pasta>` (precisa sair com codigo 0).
- Checkpoint antigo: `py -3.12 automacao/checkpoint.py migrar <pasta>` mostra a conversao; grave com `--aplicar` apenas ao retomar aquele episodio.

Nao edite `producao.json` a mao. Use caminhos relativos a raiz quando possivel.

Em cada etapa delegada, registre tambem `model_solicitado`, `reasoning_effort_solicitado`, `agent_id` e os valores efetivos somente quando confirmados pelo ambiente. Se nao houver confirmacao, registre-os como desconhecidos; nao trate o perfil solicitado como prova de execucao. Guarde a referencia ao relatorio do executor e a decisao do coordenador sobre a validacao.

Antes de executar uma etapa, inspecione o checkpoint e os artefatos. Reaproveite somente arquivos que existam e passem pela validacao da skill responsavel. Nunca considere um arquivo valido apenas pelo nome, duracao ou existencia. Preserve versoes anteriores; nao sobrescreva uma entrega aprovada.

## Fluxo continuo

Antes de renderizar, conferir a resolucao nativa do acervo e os destinos previstos. Produzir exportacoes especificas por rede e formato para atingir a maior qualidade aceita. Quando houver suporte confirmado a 4K no destino e detalhe nativo nas fontes, renderizar o projeto em 4K. O master 1080p existente nao define o teto de qualidade. Registrar a matriz de exportacoes e conferir a qualidade publica apos o processamento.

Execute as etapas abaixo seguindo os perfis e dependencias definidos acima e prossiga sem pedir aprovacoes rotineiras. Envie atualizacoes curtas durante trabalhos longos.

### Passo zero: armazenamento e disco (SEMPRE, antes de qualquer outra etapa)

A midia pesada mora no Google Drive (montagem `P:` via rclone; no projeto ficam links simbolicos com os mesmos caminhos). O usuario autorizou de forma permanente arquivar no Drive e aplicar as cotas da ferramenta.

1. `py -3.12 automacao/armazenamento.py status`: a montagem precisa estar OK (senao `.utomacao\montar_drive.ps1`). Registre o espaco livre no `PROGRESSO.md`.
2. Atualize o estado de cada episodio anterior ainda nao confirmado: `py -3.12 automacao/pipeline/distribuir_postiz.py --episodio <pasta> --status` (sem `--limpar` se for so conferir; o `--limpar` tambem remove do R2 as midias ja PUBLISHED).
3. Simule: `py -3.12 automacao/armazenamento.py automatico --excluir <pasta do episodio em producao>` e confira a lista.
4. Aplique: repita com `--executar`. Arquiva no Drive (md5 conferido antes de trocar por link) lives de dias anteriores e episodios sem midia alterada ha 48 h; remove intermediarios de publicados ha 7 dias; aplica as cotas do Drive (lives 400 GB, publicados 500 GB) apagando o menor valor/GB primeiro. Nunca toca no episodio em `--excluir`, em pecas nao `PUBLISHED` nem em clipes pendentes de aprovacao.
5. Se ainda faltarem 15 GB livres no disco local, pare e avise o usuario; nao apague nada alem do que a ferramenta lista.
6. Midia do episodio que sera muito lida (ex.: clipes do acervo usados em varios renders) pode ser trazida com `armazenamento.py trazer <pasta> --executar`; ao terminar, o `automatico` devolve ao Drive.

### 0. Checagem factual visual (antes de gastar com voz)

Regravar uma frase depois da montagem custa TTS, emenda, realinhamento e novo ciclo de render e revisao. Antes da narracao:

- Liste toda afirmacao do roteiro que a imagem pode desmentir: quem aparece, o que a pessoa faz, roupa/mascara/arma, texto na tela, botao do HUD, minuto citado do video-fonte.
- Extraia o quadro correspondente do acervo (um `ffmpeg -ss` por afirmacao, reduzido) e confira cada uma olhando a imagem; nome de arquivo e catalogo nao provam conteudo. Um executor `flash`/`sonnet` basta; salve os quadros em `<pasta>/montagem/referencias/` para a direcao reaproveitar.
- Divergencia: proponha a correcao da frase e aplique nas copias de narracao ANTES do TTS (sem tocar no original aprovado sem registrar). So siga para a voz com a lista zerada ou com as excecoes anotadas no `PROGRESSO.md`.

### 1. Narracao

Leia e aplique integralmente a skill `pixel-procurado-gemini-tts`.

- Preserve o roteiro original e crie uma versao Gemini separada.
- Use a integracao local e `automacao/gerar_narracao_gemini.ps1`; nao automatize o site do Gemini quando a API local estiver disponivel.
- O PowerShell ja seleciona `.venv-gemini`; nunca use o Python global para contornar esse fluxo.
- Valide WAV, duracao, codec, picos, silencios e transcricao. Se houver omissao provavel, tag falada ou erro material, corrija somente a versao Gemini e tente novamente no trecho afetado, no maximo duas vezes antes de bloquear.
- Quando a validacao automatica nao encontrar divergencia material, normalize a copia aprovada e continue. Registre qualquer pronuncia que ainda mereca escuta humana sem interromper a producao por incerteza pequena.

### 2. Alinhamento, midia e edicao

Leia e aplique integralmente a skill `pixel-procurado-video`, inclusive as referencias que ela indicar para o projeto e o formato atual.

- Trate a narracao validada como relogio mestre.
- Gere ou revise o alinhamento por palavra/frase e monte uma timeline que cubra todo o audio.
- A timeline e os cards vao em `<pasta>/episodio.json` e a montagem roda com `automacao/pipeline/produzir_v2.py` e `validar_v2.py` (ver "Pipeline V2 padrao" em `pixel-procurado-video`). Nao escreva `produzir_<id>.py`, `renderizar_<id>.py` ou `validar_<id>.py`.
- Consulte primeiro `videosGTAVI/_catalogo/` e o acervo local. Inspecione visualmente a midia; nome de arquivo nao prova conteudo.
- Cada plano deve corresponder ao que esta sendo dito naquele instante. Use graficos editoriais identificados quando nao houver imagem literal adequada; nao preencha com clipes genericos repetidos.
- Siga a ferramenta e o fluxo V2 definidos em `pixel-procurado-video`. Para Python audiovisual, verifique a versao compativel antes de executar: neste projeto os pacotes de `.course-tools` foram preparados para Python 3.12, e o Python 3.14 global pode falhar com extensoes binarias.
- Antes do render integral, rode `py -3.12 automacao/pipeline/prevoo_v2.py --episodio <pasta>` (precisa sair com codigo 0) e olhe as folhas de `montagem/prevoo/`; isso cumpre o "Pre-voo obrigatorio" de `pixel-procurado-video`: janelas conferidas por quadro (inicio, meio e fim) e por `blackdetect`, card coerente com a imagem e com o numero dito na narracao, timeline cobrindo toda a narracao, GTA V rotulado, e bitrate de entrega definido por destino.
- Faca uma amostra representativa antes do render completo, corrija problemas objetivos e siga sem exigir aprovacao quando a amostra estiver coerente com o roteiro e a identidade do canal.
- A primeira revisao visual independente acontece sobre as folhas do pre-voo (`montagem/prevoo/`: 3 quadros por plano ao lado do card e da fala), que custam minutos e nao exigem render. Ela cobre imagem x fala, card x imagem x numero, personagem certo, rotulos e repeticoes. Corrija e rode o pre-voo de novo ate aprovar.
- Movimento, legenda, entrada/saida de card e emendas de audio so aparecem em video: depois das folhas aprovadas, renderize amostras de baixa resolucao com `--amostra INICIO-FIM` cobrindo abertura, encerramento, um trecho por tipo de card e os pontos apontados na revisao. Previa integral so se o episodio tiver direcao inedita.
- Segunda rodada de revisao: renderize e mostre SOMENTE os trechos alterados (`--amostra`), nunca a previa inteira de novo. Depois do master, a revisao final so confirma.
- Um processo pesado por vez (render, pre-voo com folhas, reencode, ASR): em notebook, dois renders simultaneos demoram mais que em fila e derrubam comandos por timeout. Capas, textos e pacote de publicacao podem rodar em paralelo ao render, porque quase nao usam CPU.
- Peca com limite de tamanho no destino (video do Instagram: 300 MB): declare `"limite_mb"` no formato do `episodio.json` daquela peca; o render ja sai no tamanho certo em um unico encode. Nao gere o arquivo grande para recomprimir depois.
- Renders, reencodes, QA e uploads rodam em segundo plano com log na pasta do episodio; delegue-os ao perfil mais barato (`flash_lite` / `haiku`) e nao gaste o modelo principal acompanhando.
- Entregue MP4, SRT e timeline/projeto editavel. Decodifique o MP4 inteiro e faca a QA visual e temporal exigida pela skill de video.

### 3. Thumbnail

Leia e aplique integralmente a skill `pixel-procurado-thumbnails`. A arte raster nova sai de `automacao/gerar_arte_thumbnail.ps1` (Gemini), igual em qualquer IA; `imagegen`/`image-generator` so como alternativa se o script falhar.

Prepare uma capa por video final. Quando o episodio incluir longo e Short, entregue capas proprias para as duas pecas e adapte as proporcoes aos destinos solicitados.

- Use o roteiro e o video final para definir uma unica tensao visual.
- Gere a arte-base sem texto/logo e componha texto e identidade de forma deterministica.
- Entregue master, arquivo para upload, arte-base e prompt na pasta de publicacao do episodio.
- Se a primeira composicao falhar na leitura reduzida, corrija-a; nao gere variantes sem necessidade.

### 4. Pacote de publicacao

Leia e aplique integralmente a skill `pixel-procurado-publicacao` usando os tempos do MP4 final e a thumbnail ja validada. Nao regenere a capa salvo incompatibilidade real.

Entregue titulo recomendado e alternativas, descricao, capitulos quando aplicaveis, comentario fixado, tags, creditos/fontes e guia do YouTube Studio. Consulte fontes oficiais atuais quando regras da plataforma ou informacoes volateis influenciarem o pacote.

### 5. Publicacao e agendamento via Postiz + Cloudflare R2 (somente quando autorizado pelo usuario)

Se o comando do usuario pedir explicitamente para publicar ou agendar no Postiz:

1. Valide a conexao com `py -3.12 automacao/postiz_shorts.py check`.
2. Para **YouTube** (`cmvsctfgl0001jncj932ovibv`), envie o MP4 e a thumbnail (`capa_youtube.jpg` para 16:9) via `PostizClient` (`automacao/postiz_shorts.py`).
3. Para **Instagram** (`cmvzyw7vj0003pddwkgtivv8i`) e **Facebook** (`cmvzyur290001pddwolrt33em`), faca stage temporario do MP4 e da capa no Cloudflare R2 (`automacao/r2_media.py`), crie o post no Postiz apontando para a URL assinada do Worker, aguarde `PUBLISHED` + `releaseURL` (ou confirmacao de agendamento `QUEUE`) e limpe o objeto do R2 apos publicacao imediata, salvando o manifesto JSON auditavel em `publicacao/`. Use `py -3.12 automacao/pipeline/distribuir_postiz.py --episodio <pasta>` (plano) e `--publicar` (envio real, somente com autorizacao); nao crie script de distribuicao por episodio. `automacao/distribuir_l06_postiz.py` fica como referencia para a limpeza do R2 apos `PUBLISHED`.

4. Antes de `--publicar`, confira cada arquivo contra os limites observados em `pixel-procurado-publicacao` (upload local do Postiz ate ~1 GB; video do Instagram ate 300 MB). Derive a versao menor antes do envio, nao depois do erro.
5. Depois do envio, confirme que cada peca ficou com `post_id` real em `POSTIZ_ESTADO.json`. O script agora descobre o ID pela resposta ou pelo post novo na integracao, e para com erro se nao conseguir; nesse caso NAO use `--reenviar` sem antes conferir no Postiz se o post existe (publicaria em duplicata): grave o ID no estado. So entao rode `--status --limpar` e relate o estado real (`PUBLISHED` com `releaseURL`, ou o erro) de cada peca.
6. O Postiz aceita um titulo e uma capa por video do YouTube. Teste A/B de titulo e miniatura e feito pelo usuario no YouTube Studio: entregue titulo B e capa B e diga isso no relatorio.

## Retomada e limites

`retome <ID>` deve abrir o checkpoint, revalidar a ultima entrega e continuar da primeira etapa incompleta. Invalide somente os artefatos afetados por uma mudanca; nunca regenere audio pago ou render completo sem necessidade.

Pare apenas quando houver ambiguidade real de roteiro, credencial ausente, fonte essencial inacessivel, falha repetida de geracao/validacao ou decisao editorial que mude materialmente o sentido. Registre o bloqueio no checkpoint e diga exatamente o que falta.

Concluir significa entregar links absolutos para o MP4, SRT, thumbnail pronta, pasta de publicacao e checkpoint, com o que foi validado e qualquer limitacao relevante. Declare explicitamente que nao houve upload.
