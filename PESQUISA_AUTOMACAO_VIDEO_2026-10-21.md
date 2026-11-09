# Automação de edição para o canal dark

Pesquisa em 21/10/2026. Complemento à base do curso; recomendações técnicas nossas, não ensinamentos atribuídos ao professor. Foram consultadas documentações dos próprios projetos. Não houve instalação, teste de compatibilidade com editores, envio de arquivos a serviços externos ou produção de vídeo nesta pesquisa.

## Recomendação

**Atualização após os exemplos indicados pelo usuário:** testar Concat como primeira opção de editor automatizável; avaliar VoiceStudio se adotarmos narração sintética; usar Remotion quando o padrão visual estiver definido; acrescentar SupoClip para derivados de vídeos narrados. Essa prioridade amplia a pesquisa inicial, que se concentrou em componentes e adaptadores para editores existentes. A análise detalhada está na seção final. A seleção continua provisória até um teste real.

Construir primeiro um fluxo local de preparação e montagem: transcrição → seleção editorial → cortes → legendas → prévia para revisão. Guardar as decisões em um plano de edição independente do editor. Acrescentar exportação de projeto CapCut se essa for a interface escolhida pelo usuário.

Essa proposta aproveita o faster-whisper e os modelos já utilizados neste projeto para analisar o curso. Os scripts existentes fazem transcrição e amostragem visual; ainda não são uma ferramenta completa de edição.

## O que existe e o que cada abordagem resolve

“Engenharia reversa” não descreve todas as soluções: algumas escrevem formatos de projetos não oficiais; outras usam APIs de fabricantes; outras executam a edição diretamente com ferramentas abertas. Um MCP é uma interface de ferramentas para o agente chamar. Não fornece sozinho inteligência editorial nem garante que o programa consiga exportar o resultado.

| Projeto e fonte primária | Capacidade documentada | Avaliação para este canal |
|---|---|---|
| [pyCapCut](https://github.com/GuanYixuan/pyCapCut) | Geração/edição de rascunhos, trilhas, texto, áudio, efeitos e importação SRT. A documentação orienta abrir e exportar manualmente no CapCut para Windows. Templates precisam estar em JSON legível. | Bom candidato para entregar uma timeline ajustável. Testar na versão instalada; não presumir exportação automática. |
| [CapCutAPI — ashreo](https://github.com/ashreo/CapCutAPI) | Interface comunitária HTTP/MCP para criar rascunhos e acrescentar vídeos, áudio, textos e legendas. | Alternativa de integração, não API oficial do fabricante. O README aponta também para outro proprietário no comando de clone: verificar origem e versão antes de escolher o fork. |
| [DaVinci Resolve MCP — samuelgursky](https://github.com/samuelgursky/davinci-resolve-mcp) | Controle por scripting de edição, mídia e configuração de render. O mantenedor diferencia Studio de uma ponte interna para versões gratuitas anteriores e informa mudança no Resolve 21.1. | Candidato se o editor escolhido for Resolve. Não assumir que qualquer versão gratuita oferece as mesmas capacidades de automação. |
| [Descript MCP oficial](https://github.com/descriptinc/descript-mcp) | Importação, edição por instrução com Underlord, legendas, remoção de vícios de fala e exportação de timeline. Serviço remoto com autenticação OAuth. | Alternativa para reduzir desenvolvimento local, condicionada a conta, plano e teste com português. |
| [OpenCut-app/OpenCut](https://github.com/opencut-app/opencut) | O README informa uma reescrita; API, MCP e renderização sem interface aparecem como recursos futuros. Recomenda a edição classic para uso atual. | Acompanhar; não planejar a operação com base em recursos ainda anunciados. Há projetos diferentes usando o mesmo nome. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) e [WhisperX](https://github.com/m-bain/whisperX) | Reconhecimento de fala; WhisperX inclui alinhamento de palavras e diarização. | Reutilizar nossa transcrição local. Avaliar alinhamento mais preciso quando houver legenda destacando palavras; revisar nomes e números. |
| [Auto-Editor](https://github.com/WyattBlue/auto-editor) | Primeiro corte por áudio/movimento e exportação para editores, incluindo Resolve, Premiere, Shotcut e Kdenlive. | Útil em narração com pausas. Critérios acústicos não determinam interesse de uma cena de gameplay. |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Detecta mudanças de cena e permite dividir o vídeo. | Ajuda a indexar arquivos longos. Mudança de cena não equivale a acontecimento interessante. |
| [FFmpeg](https://ffmpeg.org/ffmpeg-filters.html) | Filtros de corte, composição, escala, texto/legendas e processamento de áudio. | Motor proposto para executar o plano e gerar MP4 de revisão sem depender da interface de um editor. |

## Dois fluxos diferentes

### Material bruto com fala

Entrada: gravação narrada, entrevista ou explicação que temos autorização para editar.

1. Extrair e transcrever áudio com tempos.
2. A IA propor trechos que tenham começo, contexto e conclusão. Entregar justificativa e intervalos, não apenas uma nota abstrata de “viralidade”.
3. Marcar silêncios longos e repetições; preservar respirações e pausas úteis.
4. Definir a montagem e recalcular os tempos das legendas para a nova sequência. Uma legenda do bruto perde sincronismo se reutilizada sem ajuste após cortes.
5. Gerar SRT e, quando necessário, ASS com estilos/destaques. Revisar transcrição antes de gravar texto na imagem.
6. Produzir prévia e uma versão revisável do plano; exportar o resultado aprovado.

### Gameplay ou banco de imagens sem fala relevante

Entrada: cenas de GTA com origem registrada, roteiro e narração própria ou sintética revisada.

1. Separar cenas ou janelas de tempo e produzir miniaturas com timestamps.
2. Identificar o conteúdo visual com inspeção humana ou modelo com visão. Essa etapa precisa de um motor de visão escolhido e validado; transcrição não a substitui.
3. Criar um índice por personagem, local, ação e adequação à pauta. Registrar jogo e origem de cada recurso.
4. Associar trechos do roteiro a imagens pertinentes. Para uma afirmação factual, distinguir evidência de imagem meramente ilustrativa.
5. Usar a narração final como referência de duração, acrescentar cenas, cartelas e trilha ajustada.
6. Gerar legendas a partir da voz final e revisar ritmo e correspondência entre imagem e fala.

Para o nosso canal, o segundo fluxo é especialmente importante: o banco apresentado na aula 11 fornece material visual, mas uma captura sem fala não informa ao Whisper quem aparece ou por que uma cena vale entrar no vídeo. Tiros, música e movimento intenso também não são critérios suficientes de qualidade editorial.

## Arquitetura proposta

```text
Brutos + roteiro + narração + registro das fontes
                    ↓
Transcrição / análise de cenas / índice do acervo
                    ↓
IA propõe um plano com arquivos, intervalos e justificativas
                    ↓
Validação dos intervalos, legendas e duração
                    ↓
FFmpeg → MP4 de revisão + SRT
        ou
Adaptador pyCapCut → projeto editável → exportação no CapCut
                    ↓
Revisão humana de narrativa, fatos, áudio e enquadramento
```

O plano deve guardar caminho do arquivo, entrada/saída no bruto, posição na timeline, texto, recurso de origem, proporção e transformações. Manter esse registro permite trocar de editor e regenerar versões sem depender de instruções vagas ou de cliques na tela. Projetos derivados e saídas recebem nomes próprios; os originais ficam preservados.

## Piloto recomendado

Proposta de teste, ainda não executada: usar 5–10 minutos de material autorizado e uma narração curta para montar uma explicação de 60–90 segundos. Entregas: prévia horizontal, SRT, plano de edição e relatório curto de problemas. Depois testar um derivado vertical que funcione sozinho.

Critérios de sucesso:

- Nenhuma palavra cortada no meio; legendas sincronizadas após a montagem.
- Personagens, mapas ou detalhes importantes permanecem visíveis no enquadramento.
- Música não encobre a narração; nenhum trecho entra somente por ser barulhento.
- Fontes registradas e imagens de GTA V identificadas quando usadas em contexto de GTA VI.
- A seleção tem uma explicação editorial coerente com o papel do canal.
- Tempo de revisão e processamento medidos no computador real, sem promessa antecipada de ganho percentual.

Verticalização precisa ser uma escolha de composição: recorte acompanhado, imagem inteira com fundo, ou layout específico. Um corte central fixo pode esconder a ação; o acerto depende de testar as cenas usadas.

## Custos e dependências

A combinação local evita que cada tarefa de transcrição e corte exija um serviço de edição em nuvem. Ainda há custo de processamento, armazenamento, implantação e manutenção. Modelos externos de linguagem/visão/voz podem gerar cobrança e transmissão de dados conforme a opção escolhida. Não foram estimados desempenho ou custo por vídeo sem conhecer hardware e duração média.

O [Descript oferece API e MCP](https://www.descript.com/api); requisitos comerciais e limites devem ser conferidos antes de contratar. DaVinci Studio ou recursos pagos do CapCut, quando necessários ao fluxo escolhido, não passam a ser gratuitos por existir um adaptador comunitário.

## Ordem sugerida de implementação

1. Reaproveitar o componente local de transcrição e construir saída de legendas com revisão.
2. Criar um plano de cortes e renderização de prévia com FFmpeg.
3. Indexar o banco visual e associar cenas ao roteiro.
4. Testar um projeto mínimo no CapCut antes de desenvolver o adaptador completo; fixar as versões aprovadas no teste.
5. Acrescentar derivados verticais e padrões visuais após o fluxo principal funcionar.

Essa ordem é uma recomendação de engenharia para nossa situação. As capacidades dos repositórios acima são declarações documentadas de seus mantenedores, não resultados de testes realizados nesta máquina. A publicação no canal não faz parte do piloto proposto.

## Ampliação: SupoClip, Concat, VoiceStudio, Remotion e ViceScale

Consulta em 21/10/2026. Os produtos abaixo resolvem etapas diferentes. A arquitetura proposta não exige instalar todos; escolher uma ferramenta por necessidade evita duplicar processamento e manutenção.

### Concat: primeiro candidato para edição assistida

O [Concat de jub0t](https://github.com/jub0t/Concat) é um editor independente, local, multiplataforma, em beta. Documenta timeline com várias faixas, legendas locais, geração de voz e exportação. Não é apenas um gerador de projetos para o CapCut.

Sua [documentação MCP](https://github.com/jub0t/Concat/blob/main/docs/MCP.md) descreve importação, cortes, títulos, legendas, leitura de quadros e exportação, inclusive sem janela aberta. Há uma limitação importante: o agente trabalha em projetos próprios; editar ao vivo o projeto que o usuário está manipulando na janela ainda aparece como recurso planejado.

**Avaliação nossa:** merece o primeiro piloto pela possibilidade de reunir edição revisável e automação no mesmo programa. Validar importação, salvamento, reabertura, exportação, fontes e áudio no Windows antes de migrar uma produção inteira. A indicação é de candidato para teste, não de estabilidade já comprovada.

### VoiceStudio: componente de narração

O [VoiceStudio indicado pelo usuário](https://github.com/debpalash/VoiceStudio) oferece voz sintética, clonagem, dublagem, processamento em lote e API/MCP local. Documenta Windows, aceleração CUDA e execução em CPU mais lenta. As condições dos modelos e vozes são separadas da licença do aplicativo.

**Avaliação nossa:** testar a mesma passagem em português brasileiro, com nomes de personagens e pausas, antes de escolher a voz do canal. Medir naturalidade e tempo por minuto de áudio. Usar voz própria, projetada ou autorizada. Como Concat também oferece voz, só acrescentar VoiceStudio se melhorar qualidade ou controle. Não foi realizado teste de geração nesta pesquisa.

### Remotion: identidade visual reproduzível

O [Remotion](https://www.remotion.dev/) cria vídeos e animações com React e permite parametrização e renderização em lote. A [página de licença](https://www.remotion.dev/docs/license/pricing) informa gratuidade para indivíduos e empresas de até três pessoas, sujeita aos termos; organizações maiores têm licença paga. Infraestrutura de renderização e serviços de IA são custos separados.

**Aplicação proposta:** construir modelos nossos de explicação, comparação e curiosidade, recebendo roteiro, narração, fontes, cenas e tempos. Reutilizar tipografia, posições de legenda, cartões de evidência e animações. A seleção do conteúdo entra como dado ou decisão anterior: Remotion não escolhe sozinho o que merece virar vídeo. Exige desenvolvimento inicial, mas é um bom candidato para repetir o formato editorial com consistência.

### SupoClip: derivados de conteúdo narrado

O [SupoClip de FujiwaraChoki](https://github.com/FujiwaraChoki/supoclip) seleciona trechos pela transcrição, gera vídeos verticais, legendas sincronizadas e enquadramento centrado em rostos. Documenta Docker, API/MCP e alternativas de provedores; o caminho local com Whisper/Ollama é diferente do início rápido com serviços externos. Não confundir com forks, como o de cspenn, que tem requisitos próprios.

**Avaliação nossa:** útil depois de termos vídeos narrados próprios para extrair Shorts. Em gameplay, revisar o enquadramento: seguir um rosto pode esconder mapa, personagem ou ação. A pontuação de viralidade é uma estimativa da ferramenta, não prova de resultado. Começar pelo arquivo narrado e verificar se cada corte responde a uma pergunta completa.

### ViceScale: opção comercial de produção e distribuição

Identificado como [ViceScale](https://www.vicescale.com/). A página anuncia templates, variações de vídeos, editor simplificado, agendamento e integração Claude MCP. Na consulta, apresenta Pro por R$ 97,90/mês e Escala por R$ 197,90/mês. Há uma oferta histórica indexada como vitalícia; não presumir que ela corresponda à contratação atual. A página não foi suficiente para validar o protocolo de integração ou a qualidade das saídas.

**Avaliação nossa:** comparar uma demonstração com nosso próprio piloto antes de contratar. Testar especialmente português, exportação, liberdade de layout, limites efetivos e economia de revisão. A promessa de multiplicar publicações não substitui a entrega de explicação e investigação definida para o canal. Recursos de repostagem não são centrais à nossa proposta.

### Escolha por objetivo

| Objetivo | Primeiro candidato a testar | Evidência necessária no piloto |
|---|---|---|
| Pedir cortes e receber um projeto editável | Concat | Projeto abre, salva e exporta corretamente no Windows |
| Gerar narração consistente | VoiceStudio, comparado à voz do Concat | Português natural e pronúncia revisável |
| Repetir identidade visual a partir de roteiro e dados | Remotion | Um modelo produz dois episódios diferentes sem refazer a montagem |
| Extrair Shorts de explicações longas | SupoClip | Cortes completos e enquadramento adequado a games |
| Usar serviço pronto de variações e distribuição | ViceScale | Demonstração funcional, custo e acesso à integração confirmados |

### Piloto revisado para este canal

Produzir uma peça de 60–90 segundos sobre uma curiosidade de GTA com roteiro nosso, imagens autorizadas e voz revisada. Primeiro testar a edição no Concat. Se a narração sintética for necessária e insuficiente ali, avaliar VoiceStudio. Quando aprovados ritmo e apresentação, transformar esse padrão em um modelo Remotion. SupoClip passa a fazer sentido ao existir um catálogo longo para derivar; não precisa entrar no primeiro teste.

Manter uma única montagem responsável por cada saída. Concat e Remotion podem ser caminhos alternativos, ou Remotion gerar elementos visuais incorporados à edição. Não é necessário renderizar todo vídeo em ambos. Essa decisão deve seguir o resultado do piloto, preservando a base local de mídia, transcrições e planos de edição já proposta.
