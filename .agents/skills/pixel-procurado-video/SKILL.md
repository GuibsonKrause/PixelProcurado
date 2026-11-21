---
name: pixel-procurado-video
description: Editar e renderizar vídeos narrados do Pixel Procurado com cenas do acervo, legendas sincronizadas e cards animados breves. Use para montar episódios e Shorts ou revisar a edição no padrão V2 aprovado.
---

# Edição narrada do Pixel Procurado

Entregar um vídeo completo, renderizado e verificável. Usar a narração aprovada como linha principal da montagem, preservando as falas, sua ordem e seu significado. Aplicar o padrão visual aprovado no especial pré-lançamento V2 ao conteúdo e formato de cada episódio. Para escrever ou revisar o texto, usar `pixel-procurado-roteiro`.

## Descoberta do episódio

- Identificar o áudio aprovado, roteiro, transcrição, mídia disponível e formato do projeto. Não confundir amostras de voz ou versões antigas com a narração final.
- Trabalhar no projeto atual. Para o ambiente GamePlay, consultar [references/projeto-local.md](references/projeto-local.md) e conferir a existência dos caminhos antes de usar.
- Reutilizar inventários e índices de cenas existentes. Se faltar catálogo, gerar metadados e folhas de contato; para vídeos, inspecionar quadros com timecode. Nome do arquivo não comprova conteúdo ou procedência.
- Seguir a identidade aprovada: grafite, branco e amarelo #FFD33D, tipografia sem serifa legível, marca discreta e rótulos editoriais. Ajustar quando o usuário fornecer outra direção.
- Na ausência de especificação, usar 3840×2160, 16:9, 30 fps, MP4/H.264, áudio AAC a 48 kHz. Respeitar outro formato já definido.

## Direção guiada pela voz

1. Medir duração, volume, picos e pausas do áudio; aproveitar uma boa normalização existente. Alvo inicial de voz: cerca de −16 LUFS e pico verdadeiro de até −1,5 dBTP, ajustado ao material. Não empilhar normalizadores nem aplicar redução de ruído que destrua a voz.
2. Analisar o que cada trecho diz e seu ritmo usando áudio, roteiro e transcrição. Se a análise for apenas por transcrição/medidas, não afirmar que fez escuta subjetiva integral.
3. Criar uma linha do tempo com início/fim, arquivo, ponto de entrada da fonte, assunto, função editorial, texto e movimento de cada plano.
   Quando houver roteiro alinhado, vincular os cortes a frases identificáveis da narração, convertidas para frames. Validar que cada frase usada como âncora corresponde ao trecho correto; não aceitar silenciosamente a primeira ocorrência de uma frase repetida.
4. Priorizar trechos em vídeo que mostrem a ação, o personagem ou a região citada. Usar imagens estáticas quando forem necessárias para ler um detalhe, comparar, mostrar uma fonte ou cobrir uma fala sem vídeo pertinente. Na enumeração de nomes e lugares, sincronizar as trocas às palavras.
5. Aberturas podem usar planos de 1,5–3,5 s; explicações normalmente pedem 3–7 s. São referências, não cotas: respeitar frases, pausas e leitura. Evitar repetir imagens como preenchimento.
6. Distinguir imagem de jogo, artwork, comparação, hipótese e exemplo. Não transformar ilustração em prova nem usar GTA V como GTA VI. Identificar conteúdo de edição/pacote quando relevante.
7. Usar gráficos para esclarecer uma data, comparação ou raciocínio. O título de capítulo não deve disputar atenção com a legenda e o rosto.
8. Para exemplos imaginados, identificar o caráter ilustrativo da mídia. Usar um gráfico próprio quando ajudar a explicar a hipótese. Quando a fala analisa uma imagem, mantê-la pelo tempo necessário e revelar os destaques na ordem mencionada.

## Movimento e legendas

- Preferir cortes limpos e transições curtas motivadas pelo assunto. Alternar planos de ação com momentos de leitura.
- Em fotos, usar movimentos lentos de zoom e panorâmica com enquadramentos escolhidos. Variar direção/foco em vez de aplicar uma fórmula repetida em toda imagem.
- Para profundidade/parallax real, usar camadas separadas de qualidade e conferir bordas/oclusões. Não inventar um recorte 3D que deforme rostos. Se só houver uma imagem plana, movimento 2D suave e planos gráficos independentes são melhores; relatar o que realmente foi aplicado.
- Usar marcações por palavra quando disponíveis. Revisar nomes próprios e erros de reconhecimento contra roteiro e áudio, sem reescrever o significado.
- Registrar diferenças relevantes entre reconhecimento e roteiro. O áudio aprovado prevalece se a locução divergir do texto; não forçar palavras ausentes nas legendas apenas para obter correspondência com o roteiro.
- Agrupar legendas por sentido, geralmente 4–8 palavras, até duas linhas. Pontuação e pausas têm prioridade sobre contagem fixa.
- Evitar fragmentação em blocos muito curtos por pequenas pausas. Como ponto de partida, testar cerca de 0,85 s de exposição mínima quando a fala e a próxima legenda permitirem; conferir fades e leitura no vídeo real.
- Texto branco de alto contraste, fundo escuro ou contorno bem dimensionado, palavras-chave pontuais em amarelo. Evitar karaokê incessante. Animações curtas, discretas e sem prejudicar o tempo de leitura.
- Respeitar áreas seguras, rostos e textos da fonte. Testar a leitura em tamanho pequeno.
- Posicionar títulos por cena: trocar o lado do painel ou baixá-lo para a região do torso quando cobrir um rosto. Ajustar também o gradiente de contraste. Perguntas e itens de listas podem entrar individualmente no instante da fala.
- Usar cards compactos e pontuais. Ancorar a entrada à fala, dimensionar a permanência pelo texto e animar a saída completa. Deixar cenas e legendas livres até o próximo destaque. Encurtar ou omitir o card quando a janela não comportar leitura.
- Variar a animação pelo conteúdo. Usar revelação lateral por máscara para informação editorial, deslocamento e escala para cápsulas curtas e destaque visual para dados. Escalonar palavras ou elementos quando reforçar a fala. Ajustar texto, posição e escala para cada formato e conferir entrada, leitura, saída e cena livre em amostra real.
- Legenda incorporada no MP4 e SRT separado como entregas. Alinhar os tempos ao áudio integral.
- Silenciar o áudio dos clipes sob a narração, exceto quando editorialmente necessário. Música é opcional, depende de fonte adequada e nunca deve competir com a voz.

## Produção e exportação

Planejar a resolução final a partir das fontes nativas e dos destinos. Usar exportações específicas por rede e formato para atingir a maior qualidade aceita. Quando as fontes e o destino oferecerem suporte a 4K, renderizar o projeto nessa resolução. Identificar os planos que exigem ampliação e preservar o detalhe disponível das fontes de maior resolução.

Para novas animações, preferir o fluxo V2 com Hyperframes para os cards e FFmpeg para composição e exportação. Em projetos existentes, reaproveitar a timeline e a ferramenta já compatível, inclusive Remotion, quando preservarem o padrão visual. Fazer primeiro uma amostra representativa em cada formato solicitado.

Consultar [references/renderizacao-e-validacao.md](references/renderizacao-e-validacao.md) para detalhes do fluxo híbrido e critérios técnicos. O método pode mudar; a qualidade pedida não pode ser reduzida silenciosamente.

Não copiar scripts específicos de L01 ou L02 e executá-los como se fossem um novo episódio. Adaptar fontes, tempos, textos, diretórios e estratégia ao episódio atual. Salvar em pasta própria e preservar versões anteriores. Instalar somente dependências necessárias ao fluxo autorizado; serviços pagos e publicação externa não fazem parte desta skill.

## Pipeline V2 padrão (não criar scripts por episódio)

Para episódios e Shorts no padrão V2, usar os scripts genéricos de `automacao/pipeline/` (detalhes em `automacao/pipeline/README.md`). O trabalho do agente é preencher dados, não reescrever código:

1. Copiar `automacao/pipeline/episodio.modelo.json` para `<pasta do episódio>/episodio.json` e preencher planos/cards, mídias, narração normalizada, alinhamento, correções de legenda e publicação (esquema em `automacao/pipeline/episodio.schema.json`; exemplo completo em `producao/L08/episodio.json`).
2. `py -3.12 automacao/pipeline/produzir_v2.py --episodio <pasta> --dry-run` (confere insumos, não grava nada) e `py -3.12 automacao/pipeline/prevoo_v2.py --episodio <pasta>` (pré-voo; ver abaixo).
3. Amostra: `py -3.12 automacao/pipeline/produzir_v2.py --episodio <pasta> --amostra 0-12`, depois `py -3.12 automacao/pipeline/validar_v2.py --episodio <pasta> --amostra 0-12`.
4. Final: `py -3.12 automacao/pipeline/produzir_v2.py --episodio <pasta> [--formato longo|short|ambos]`, depois `py -3.12 automacao/pipeline/validar_v2.py --episodio <pasta>`.

### Pré-voo obrigatório antes do render integral (lições do Dia 02 da série de aquecimento)

O render 4K integral e os painéis Hyperframes custam dezenas de minutos; cada item abaixo custa segundos e evitou (ou teria evitado) um re-render completo. Rodar `py -3.12 automacao/pipeline/prevoo_v2.py --episodio <pasta>` depois do `--dry-run` e antes de qualquer render: ele automatiza os itens 1, 3 e 4 (sai com código 1 se houver erro) e gera em `montagem/prevoo/` as folhas de contato usadas no item 2. Declarar `"rotulos_obrigatorios": {"GTAV": "GTA V"}` no `episodio.json` quando houver mídia de GTA V. Não renderizar com erro de pré-voo aberto:

1. **Janelas da fonte conferidas por quadro.** Os timecodes do catálogo têm desvio de alguns segundos e as fontes têm telas pretas, avisos de classificação (ESRB) e transições. Para cada plano, extrair um quadro do início, do meio e do fim da janela exata (`inicio` até `inicio + duração do corte`) e olhar a folha de contato ao lado do card e da fala. Rodar `blackdetect` (d=0.15) em cada janela. Não confiar em um único quadro do meio: a cena pode trocar 1 s antes do fim do plano.
2. **Card bate com a imagem.** Um card que afirma um conteúdo ("PRAIA LOTADA", um timecode do gameplay) só entra se o quadro sob ele mostrar isso e se o número for o mesmo que a narração diz naquele instante.
3. **Timeline cobre o áudio.** O fim do último plano deve ser igual à duração da narração normalizada (diferença menor que 0,35 s, tolerância de `validar_v2.py`). Conferir no `--dry-run`.
4. **GTA V sempre rotulado.** Todo plano com imagem de GTA V leva card ou rótulo "GTA V"; decidir isso na direção, porque acrescentar um card depois desloca os painéis e obriga a recortar todos os clipes.
5. **Revisão visual em prévia barata.** Renderizar uma prévia integral em baixa resolução (ou amostras cobrindo todos os cards) e passar pela revisão independente antes do render 4K. Correção apontada depois do master custa um ciclo inteiro.
6. **Entrega no formato final.** Definir o bitrate por destino antes de renderizar (ver limites em `pixel-procurado-publicacao`), para não reencodar um intermediário gigante depois.

Processos longos (render, reencode, QA) rodam em segundo plano com log em arquivo dentro da pasta do episódio e uma linha final de conclusão; esperar pela notificação, sem polling. Encadear com as ferramentas genéricas; não criar `.sh` por episódio.

Para remover caches, usar caminhos literais (nunca `rm` com variável de shell). Ao trocar só a janela de um plano sem card, basta apagar o clipe `montagem/<stem>/<NN>.mp4` (NN = índice do plano começando em 00) e a exportação. Ao mudar o texto, a duração ou a quantidade de cards, apagar também os painéis.

Ao mudar cards ou direção, apagar `montagem/paineis_v2.mov` e os clipes em cache de `montagem/<stem>/` antes de renderizar de novo (o script reaproveita o que existe). Se um episódio precisar de algo que o pipeline não cobre (matriz 4K/redes, TikTok, áudio pré-normalização), estender o script genérico com uma opção configurável no `episodio.json` em vez de copiar um script para o episódio. Scripts antigos por episódio (`automacao/*_l0x.py`, `producao/L08/produzir_l08.py` etc.) são histórico: não copiar.

## Validação e entrega
- Para publicação, fornecer o master aprovado na maior qualidade aceita por destino. Derivar versões somente para atender requisitos confirmados, reduzindo apenas o necessário. Preservar resolução e fps quando compatíveis e conferir as orientações da skill de publicação antes de escolher o bitrate.

- Conferir resolução, proporção, codecs, fps, duração e integridade de todas as fontes.
- Decodificar o MP4 final inteiro para detectar corrupção, além de inspecionar visualmente amostras. Conferir continuidade dos planos em frames, cobertura do texto efetivamente narrado e ausência de sobreposição indesejada nas legendas.
- Verificar também a duração do fluxo de vídeo: a duração do contêiner pode esconder desvio, pois o áudio mais longo domina esse número.
- Revisar começo, fim, cada tipo de gráfico e amostras dos cortes/legendas, incluindo mudanças rápidas e nomes. Não chamar amostragem de revisão integral.
- Confirmar ausência de truncamento ou deslocamento da narração. Comparar áudio original/exportado em vários pontos quando houver ferramentas disponíveis.
- Entregar link absoluto para o MP4 final, SRT e projeto/timeline editável, com duração, resolução e limitações relevantes. Se renderização falhar, corrigir e retomar; não apresentar previsão ou processo em andamento como produto final.
- Não fazer upload ou publicar apenas por concluir a edição. Para título, capa e textos de publicação, usar a skill pixel-procurado-publicacao quando esse pacote for solicitado.
