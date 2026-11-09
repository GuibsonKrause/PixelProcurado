# Primeiro vídeo longo — Pixel Procurado

Pacote preparado em **21/10/2026**, horário de Brasília. Base: plano do canal, pesquisa de automação e fontes oficiais consultadas nesta sessão.

## Decisão editorial

**Título principal:** GTA 6: o que está confirmado a um mês do lançamento

**Promessa:** em aproximadamente 6–8 minutos, organizar data, plataformas, história e mundo, mostrando a diferença entre anúncio, interpretação e pergunta aberta. A duração será confirmada depois da gravação; não acelerar a voz nem repetir ideias para cumprir uma faixa.

**Formato:** explicação em português brasileiro, sem rosto, com narração original, imagens oficiais contextualizadas, cartelas próprias e fontes visíveis. Público adulto interessado em GTA. Não precisamos possuir o jogo.

**Tese do episódio:** a informação mais útil não é a quantidade de detalhes de um trailer; é saber exatamente o que cada evidência permite concluir.

**Publicação planejada:** 22/10/2026 às 19h, se pronto e revisado. Alternativa já prevista: 25/10 às 19h. Revalidar a data do jogo antes de gravar e novamente antes de publicar.

## Material entregue

1. `01_NARRACAO.txt`: texto contínuo para gravar ou enviar a uma ferramenta de voz. Não inclui instruções de edição.
2. `02_DIRECAO_E_CENAS.md`: guia de gravação, plano de imagens, áudio e thumbnail.
3. `03_FONTES_E_CHECAGEM.md`: fontes, limites e itens que precisam ser revalidados.
4. `04_PUBLICACAO_E_CORTES.md`: títulos, descrição, comentário fixado e três roteiros verticais.
5. `05_AUTOMACAO.md`: operação, comandos, ferramentas e limites da automação.
6. `midia/registro.json`: modelo de inventário; preencher para cada recurso selecionado.
7. `projeto/montagem.exemplo.json`: contrato de montagem automatizada; depende dos arquivos reais.
8. `../../automacao/producao.py`: normalização, transcrição, montagem e derivados.
9. `arte/thumbnail_tipografica.png`: capa própria 1280×720, mais três cartelas de classificação.
10. `06_VALIDACAO.md`: testes executados e limites reais do ambiente preparado.

## Ordem de execução do primeiro vídeo

| Etapa | Ação concreta | Tempo inicial para reservar |
|---|---|---:|
| Apuração | Abrir as fontes, revalidar data/plataformas e selecionar as evidências | 45–60 min |
| Voz | Ler uma vez, gravar por blocos, corrigir nomes e pausas | 30–45 min |
| Material | Capturar páginas e selecionar 12–18 imagens/clipes pertinentes | 45–60 min |
| Montagem | Colocar voz primeiro; ajustar imagens à explicação | 90–120 min |
| Acabamento | Revisar SRT, preparar capa, ouvir e assistir ao master | 45–60 min |
| Publicação | Colar metadados, conferir verificações e agendar | 15–20 min |

Estimativa de planejamento: **4h30–6h05**, além da implantação técnica inicial. Medir o realizado. Na primeira semana, um longo bem finalizado cabe melhor na disponibilidade de 10–15h se a montagem demorar.

## O que ainda precisa existir para exportar o episódio

- Narração M5 gerada e revisada em 22/10: `voz/narracao_normalizada.wav` para edição e `voz/narracao_M5.mp3` para escuta. Duração medida: 8min05s. Fazer a escuta editorial antes da montagem final; a voz Windows é apenas um teste antigo.
- Imagens e trechos reais selecionados, com origem e condição de uso registradas. As videoaulas existentes são material de estudo, não nosso banco publicável.
- Entradas/saídas das cenas, ajustadas à voz. Os tempos reais por parágrafo estão em `voz/voicestudio/timeline_narracao_revisada.json`; o plano de cenas original contém estimativas.
- Revisão completa do vídeo e dos fatos no dia da publicação.

O pacote é de **pré-produção e automação**. Não confundir um teste técnico, uma capa tipográfica ou um JSON de exemplo com o vídeo final pronto.

## Critério de aprovação

- A primeira frase entrega a promessa da capa; não há vinheta longa.
- Cada fato tem uma fonte que realmente o sustenta; interpretações são identificadas.
- Tela e voz falam da mesma coisa. Imagem ilustrativa não é apresentada como prova.
- Voz inteligível no celular; nomes corretos; nenhuma palavra cortada.
- Legendas sincronizadas com o master final, depois dos cortes.
- Imagens próprias ou com uso avaliado e registrado; música com licença apropriada.
- Duração útil, exportação sem quadros pretos e sem placeholders.
- Descrição, capa e título correspondem ao vídeo; end screen não aponta para episódio inexistente.

Após publicar, registrar em 48h e sete dias: impressões, CTR por origem, retenção inicial, duração média, inscritos ganhos e horas de produção. Esses registros são manuais; nenhum monitor ou agendamento automático foi criado.
