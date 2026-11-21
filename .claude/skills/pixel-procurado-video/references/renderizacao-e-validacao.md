# Renderização híbrida e validação

## Fluxo comprovado
1. Construir timeline específica do episódio com todos os intervalos de narração cobertos.
2. Renderizar gráficos com transparência no Hyperframes ou na ferramenta compatível com o projeto, como Remotion.
3. Compor cada plano no FFmpeg com a mídia de origem, movimento, correção tonal leve, overlay e legenda.
4. Codificar os planos com configuração compatível: resolução, fps, formato de pixel, codec e base temporal coerentes.
5. Juntar os planos e muxar a narração inteira uma única vez. MP4 com faststart, H.264 e AAC.
6. Validar o arquivo unido, não apenas os segmentos.

Essa alternativa não é obrigatória: preferir o método que preserve efeitos e qualidade com custo local razoável. Não afirmar que animações Remotion foram preservadas se só PNGs estáticos foram exportados; nesse caso, animar as camadas na composição e descrever o método corretamente.

## Cards temporários: referência V2

- No GamePlay, consultar `producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06/REVISAO_V2.md` e, se necessário, `montagem/hyperframes_v2/index.html` e `produzir_especial.py` dentro do episódio. Os arquivos mostram a composição e a montagem aprovadas.
- Compor a entrada, a pausa de leitura e a saída como momentos distintos. Na V2, o ponto de partida foi aproximadamente 0,85 s mais uma palavra a cada 0,29 s, com piso nominal de 2,5 s e limite ajustado ao plano. São referências de leitura, não cotas. Reduzir o texto quando o tempo for curto e evitar reaproveitar a pausa do primeiro card em todos os seguintes.
- No fluxo V2, exportar a camada com alpha. Para estender a pausa no FFmpeg, criar uma lacuna de PTS no quadro estável antes da saída e restaurar o fps para duplicar esse quadro. O arranjo split/trim/tpad/concat testado nesse fluxo encurtou a pausa. Verificar no MP4 o quadro em leitura, a saída e a transparência depois dela.
- Inspecionar o vídeo que fica exposto após a saída. Se o card escondia uma passagem quase preta da fonte, ajustar o ponto de entrada do recorte e manter a duração. Investigar os intervalos apontados por blackdetect antes de substituir fades intencionais.

## Gráficos em projetos existentes com Remotion

- Usar `renderFrames` com fundo transparente e resolução final para os trechos animados. Em L02, títulos e contornos entravam em cerca de 25 frames a 30 fps; isso é referência de suavidade, não duração obrigatória.
- Listas e destaques precisam de tempos próprios: calcular cada entrada a partir da palavra ou frase correspondente, relativa ao início do plano. Renderizar até a última entrada terminar, não somente os primeiros 25 frames.
- Quando o gráfico fica imóvel depois da entrada, renderizar apenas a sequência necessária e sustentar seu último frame na composição, por exemplo com `tpad=stop_mode=clone`. Se houver movimento contínuo, renderizar toda a duração correspondente.
- Separar câmera da imagem e gráficos explicativos. Um contorno que identifica um objeto precisa acompanhar sua posição; manter o enquadramento fixo durante o destaque é uma solução simples, usada em L02.
- Conferir amostras de entrada, estado final e leitura junto às legendas. Inspecionar perguntas progressivas, títulos longos, rostos e detalhes indicados, não só a abertura.

## Invariantes temporais
- Converter limites absolutos para frames de forma consistente: from = round(start * fps); count = round(end * fps) - from.
- Escolher duração total arredondada com cobertura do último sample de áudio; tolerância de no máximo um frame para o fluxo visual.
- No demuxer concat, registrar explicitamente a duração pretendida de cada segmento: frames / fps.
- No caso observado, alguns clipes codificados tinham duração declarada um frame menor. Concatenar somente por duração do contêiner acumulou cerca de 0,67 s de desvio. Durações explícitas corrigiram o problema.
- Examinar avisos Non-monotonic DTS, duração real do stream de vídeo, média de fps, PTS e cortes. Não simplesmente ignorar avisos porque o arquivo abre.
- Gravar os tempos das legendas em relação ao início de cada segmento ao incorporá-las separadamente; não deslocar o áudio para compensar cortes errados.

## Retomada sem resultados antigos
Reaproveitar planos renderizados somente se entradas, intervalo, movimentos, gráficos, legenda e opções de exportação não mudaram. Duração igual não prova validade do cache. Para uma revisão pontual, invalidar apenas planos afetados; não apagar fontes ou entregas aprovadas. Confirmar caminhos antes de qualquer remoção.

Usar uma assinatura das entradas e da configuração para validar o reaproveitamento. Só sinalizar um overlay como pronto após todos os seus frames serem gravados e conferidos. A renderização seguinte deve exigir a versão esperada; a simples existência de um marcador antigo não comprova que a atualização terminou. Não revisar um MP4 ainda sendo escrito. Evitar regenerar todos os gráficos por uma mudança de posição localizada quando for possível identificar os planos realmente afetados.

## Qualidade
- 4K nativo na composição não significa que todas as fontes são 4K. Registrar limitações quando a fonte exigir ampliação.
- Fotos: zoompan de pequena amplitude e renderização sem saltos. Adaptar enquadramento às pessoas/objetos; evitar recorte cego.
- Vídeos: selecionar pontos de entrada precisos, evitar cartelas ou quadros pretos inesperados da fonte.
- Correção de cor deve ser julgada por cena; não aplicar valores fortes de contraste/saturação em todo o material.
- Transições devem preservar o tempo total e a sincronização. Sobreposições não podem encurtar a linha do tempo inadvertidamente.
- Testar legendas, acentos e fonte no render real, não só no preview.

## QA mínima significativa
- Conferência de metadados (resolução e proporção pretendidas, H.264, fps, áudio, duração).
- Decodificação integral do MP4 entregue, com captura de erros. Isso verifica integridade técnica, não substitui revisão estética ou escuta.
- Inspeção visual de cenas de abertura, corpo, encerramento, títulos longos, nomes e sequências rápidas.
- Legendas com limites válidos e sem sobreposição indesejada.
- Áudio: loudness/picos e comparação de sinais em começo, meio e fim, se tecnicamente viável. Correlação alta demonstra alinhamento/preservação do sinal, não qualidade artística nem ausência de erro factual.
- Medir também o áudio final após AAC, pois a codificação pode alterar os picos. Ao comparar a saída com a narração normalizada, identificar essa referência; não apresentar a medição como comparação direta com o WAV original sem tratamento.
- Logs de mux sem avisos temporais pendentes.
- Registrar o que foi verificado e o que não foi. Não substituir escuta humana por alegação de que uma transcrição comprova pronúncia perfeita.
