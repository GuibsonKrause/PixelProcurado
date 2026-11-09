# Direção, cenas e identidade

## Voz

Tom: investigador curioso, próximo e seguro, sem imitar apresentador de notícia urgente. Português brasileiro, aproximadamente 140–155 palavras/minuto; pausas após perguntas e mudança de assunto. Grave seis blocos e mantenha alguns segundos limpos entre tomadas. WAV mono, 48 kHz, se disponível; evite ambiente reverberante e distorção de entrada. Grave primeiro 20 segundos e ouça no celular.

Teste de pronúncia antes da gravação: “GTA seis, Jason, Lucia, Leonida, Vice City, Grassrivers, Port Gellhorn e Mount Kalaga”. Escute a pronúncia dos nomes em material oficial; preserve a escolha em todos os episódios. Não confiar na grafia fonética automática sem ouvir.

Prompt para uma ferramenta de voz licenciada: “Narre este texto em português brasileiro, com curiosidade e clareza. Faça pausas naturais, sem tom de propaganda. Preserve números e sentido. Não acrescente frases. Não leia instruções. Não imite pessoas reais. Entregue a fala sem música.” Cole apenas o arquivo `01_NARRACAO.txt`.

Preferência operacional para o primeiro vídeo: voz própria gravada ou uma voz sintética cujo resultado e condições de uso já tenham sido aprovados. VoiceStudio é uma opção futura de teste; o computador detectado tem Intel Iris Xe, sem NVIDIA detectada. Não assumir aceleração CUDA.

## Plano de cenas

Tempos abaixo são **marcos de planejamento**, a ajustar pela voz final. Não são capítulos publicáveis nem entradas de arquivos de mídia. Não foi feita inspeção quadro a quadro dos vídeos oficiais nesta entrega.

| Faixa estimada | Trecho da fala | Visual a preparar | Função e fonte |
|---|---|---|---|
| 0:00–0:15 | Fato versus conclusão | Cartela dividida: CONFIRMADO / INTERPRETAÇÃO / EM ABERTO | Gancho próprio; sem vinheta |
| 0:15–0:35 | Identidade e data de conferência | Nome Pixel Procurado + data pequena; breve página oficial | Explicar o método, S1 |
| 0:35–1:20 | Data e plataformas | Recorte legível da página; destacar data, depois plataformas | Provar apenas o que está escrito, S1 |
| 1:20–1:50 | Limite de uma conclusão | Duas cartelas: “está na fonte” e “precisa de outra prova” | Diagrama próprio, sem inventar rumor |
| 1:50–2:40 | Premissa e confiança | Imagem de Jason e Lucia; depois texto resumido da premissa | Contexto oficial e análise identificada, S1 |
| 2:40–3:20 | Antecedentes | Fotos oficiais identificadas; três palavras por personagem | Contexto, S2 |
| 3:20–4:10 | Lugares | Lista animada dos seis nomes; 2–3 imagens oficiais correspondentes | Não usar mapa especulativo, S2 |
| 4:10–4:55 | O que a paisagem não prova | Perguntas tipográficas: “distância?”, “interiores?”, “atividades?” | Ilustração do método, não alegação de ausência global |
| 4:55–5:40 | Atualidade do material | Página de mídia, títulos e datas verificadas | Evidência da disponibilidade, S1/S3 |
| 5:40–6:25 | Filtro em três passos | Quem publicou? O que mostrou? O que permite concluir? | Gráfico próprio |
| 6:25–fim | Recapitulação e próxima investigação | Três provas resumidas; pergunta final e marca | Fechar promessa, sem link falso para L2 |

Se a voz durar mais, dar espaço aos exemplos; se durar menos, encurtar a timeline. Trocar o visual por motivo narrativo; usar aproximações suaves de imagens, destaques e comparações. Evitar repetir uma imagem por um minuto só para preencher a fala.

## Aquisição de material

Abrir https://www.rockstargames.com/VI/media e selecionar imagens de personagens e locais, ou clipes que sustentem os trechos. Guardar o nome original em `midia/originais/`. Registrar cada arquivo em `registro.json`, incluindo URL, data, trecho usado, tipo (evidência/ilustração) e condição de uso avaliada. A disponibilidade de download não foi tratada como licença irrestrita de monetização.

Capturar a página da data e plataformas com texto legível. Para página dinâmica, a captura manual pelo navegador é mais confiável que presumir conteúdo de um print antigo. Não reutilizar as aulas do curso como B-roll. Música dos trailers não é trilha livre; silenciar o áudio do material de apoio e trabalhar com narração própria.

## Layout

- 1920×1080, 30 fps; texto branco, destaque amarelo `#FFD43B`, fundo `#101218`.
- Títulos curtos, margens de cerca de 80 px; rodapé de fonte visível e legível.
- Etiquetas: CONFIRMADO, ANÁLISE e EM ABERTO, com cores e palavras; não depender só de cor.
- SRT separado para acessibilidade no longo; legendas embutidas opcionais no editor.
- Reutilizar os arquivos de identidade em `../../assets/identidade/`, caminho relativo à pasta deste episódio.

## Thumbnail

Proposta A: “GTA 6” grande, “CONFIRMADO?” em amarelo, pequeno selo “DOSSIÊ 01”. Uma composição tipográfica própria pode ser usada sem imagem do jogo. Proposta B: um recorte oficial dos personagens à direita, à esquerda “O QUE É FATO?”. Registrar a origem e revisar uso da imagem antes de substituir a composição tipográfica.

Exportar 1280×720 e testar a legibilidade a 320×180. Não usar data gigante para não competir com a promessa. Não apresentar arte gerada como screenshot do jogo. A capa tipográfica entregue é uma opção editorial, não uma imagem de GTA VI.

## Áudio e revisão

Primeiro episódio pode funcionar só com voz. Se houver trilha, escolher faixa cuja licença permita o uso pretendido e guardar comprovante; começar baixa e ouvir com a voz. Como referência técnica própria, o script usa normalização em duas passagens para -16 LUFS e pico de -1,5 dBTP; não é um requisito universal do YouTube.

Assistir integralmente em velocidade normal. Conferir começo/fim de cada frase, nomes nas legendas, fontes, tela final e enquadramento vertical. O corte vertical deve preservar a informação; o script usa encaixe integral com barras, não detecção de personagens.
