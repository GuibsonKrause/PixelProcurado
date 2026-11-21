# L03 — Direção da montagem

Estado em 29/10/2026: **direção final concluída e timeline liberada para implementação**. `edicao_l03.json` usa o WAV definitivo de 330,68 s, liberado pela execução de áudio após aprovação auditiva do usuário para o reparo “encenar”. São 61 planos, 146 blocos de legenda e 9.921 frames a 30 fps. Os tempos abaixo vêm do alinhamento real, com sua procedência registrada; não vêm da duração estimada do roteiro.

Formato: 3840×2160, 16:9, 30 fps. Identidade grafite, branco e amarelo #FFD33D. A voz integral é o relógio mestre. Cortes limpos; movimentos lentos de pequena amplitude; sem música comercial nem áudio dos clipes.

## Fontes inspecionadas

Foram lidos primeiro os guias `videosGTAVI/_catalogo/GUIA_IMAGENS.md`, `GUIA_EDITORIAL.md` e `INDICE_VIDEOS.md`. A seleção central foi então aberta individualmente. As imagens VI têm 3840×2160; V1/V2 têm 640×448. Nome de arquivo e guia foram usados para encontrar a fonte, não como substitutos da inspeção.

| ID | Arquivo relativo à raiz | Observação visual e uso |
|---|---|---|
| V1 | `producao/L03/midia/V1_Vice_City_Classico_Screens_1.jpg` | Carro vermelho central; avenida, palmeiras à esquerda e comércio/prédio à direita; logo no canto inferior direito. P2/P4/P5/P17/P18. |
| V2 | `producao/L03/midia/V2_Vice_City_Classico_Screens_2.jpg` | Tommy, camisa azul estampada, palmeiras e prédio; logo superior esquerdo. P2/P6 e memória do clássico. Nunca sinalizar retorno do personagem. |
| RD2 | `videosGTAVI/GTAVI_Screenshots/People/Real Dimez/Real_Dimez_02.jpg` | Duas artistas sobre o carro e público; telefone grande à esquerda com as artistas visíveis na tela. A tela tem desfoque da própria fonte: não fabricar conteúdo nem aplicar reconstrução. P1/P2/P8/P9/P10/P12/P17/P19. |
| VC2 | `videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_02.jpg` | Casal à direita na varanda; piscina na base, vegetação no meio, praia e mar ao fundo. P13/P14/P16/P17. |
| VC5 | `videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_05.jpg` | Casal caminhando no centro-direita, pessoa com detector ao centro-esquerda, pessoa tomando sol na base esquerda, outros banhistas à direita. P15/P16/P18. |
| VC6 | `videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_06.jpg` | Fachadas e neon, palmeiras, pessoas e carro policial. P7 e atmosfera. Não chamar de localização idêntica a V1. |
| RD1 | `videosGTAVI/GTAVI_Screenshots/People/Real Dimez/Real_Dimez_01.jpg` | Artista em estúdio com fones e mesa; apoio literal à carreira musical em P10. |
| RD4 | `videosGTAVI/GTAVI_Screenshots/People/Real Dimez/Real_Dimez_04.jpg` | Duas artistas diante de microfones; música e parceria em P10/P12. |
| VC1 | `videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_01.jpg` | Letreiro VICE CITY, avião e palmeiras ao entardecer. Apoio breve ao reconhecimento da cidade, sem substituir a análise das imagens centrais. |

`Real_Dimez_03.jpg` foi inspecionada e excluída: mostra uma artista e um homem no carro; o resumo do catálogo diz “dupla”, mas não será usado como prova da presença das duas artistas.

As duas folhas detalhadas de Trailer 1 foram consultadas, e foram extraídos quadros próprios de 15 a 40 s, em `inspecoes/Trailer_1_15a40s.jpg`. A avenida noturna foi candidata para “O neon ainda cumpre seu turno”. A inspeção mais fina em `inspecoes/Trailer_1_neon_limites.jpg` mostrou avenida em 32,6/32,8 s e já um clube em 34,3 s; esse insert não foi escolhido para a fala de 1,9 s. VC6 mantém a relação entre fachadas, palmeiras e pessoas. Os panoramas 15–18 s incluem título/fade e não foram escolhidos. A timeline final usa as fotografias analisadas e gráficos próprios, sem clipes genéricos.

## Enquadramentos e coordenadas verificadas

`inspecoes/retangulos_fontes.json` contém os retângulos `[x, y, largura, altura]` em pixels das fontes 3840×2160, com mapas anotados de cada fonte. São coordenadas de inspeção para destaques, não instrução de recorte automático. O telefone e o detector também têm recortes de evidência próprios.

| Fonte / alvo | Retângulo em pixels | Direção |
|---|---|---|
| RD2 / telefone esquerdo | `[420,940,440,700]` | Contorno no aparelho visível; não apontar o telefone da direita como tela da apresentação. |
| RD2 / imagem na tela | `[485,1015,320,345]` | Pequeno contorno interno na frase “uma das telas mostra a apresentação”. Preservar o desfoque original. |
| RD2 / artistas | `[1090,10,1240,1440]` | Contexto central; sem título em cima dos rostos. |
| RD2 / público à direita | `[2320,370,1340,1630]` | Apoio à leitura do conjunto da plateia, sem afirmar que todos filmam. |
| VC2 / casal e varanda | `[2080,340,1720,1780]` | Texto no lado esquerdo quando houver; não cobrir os rostos. |
| VC2 / piscina | `[80,1190,2370,950]` | Mostrar a relação vertical entre varanda e lazer; não identificar propriedade/hotel sem fonte. |
| VC2 / praia | `[0,80,2740,475]` | Contexto distante; não simular continuidade geográfica com VC5. |
| VC5 / casal caminhando | `[1940,235,1270,1660]` | Entrada na fala “um casal caminhando”. |
| VC5 / pessoa e detector | `[660,630,640,955]` | Entrada em “alguém procurando coisas na areia com um detector de metais”; círculo/bobina incluído. |
| VC5 / pessoa tomando sol | `[10,1510,2140,640]` | Entrada em “uma pessoa tomando sol em primeiro plano”; evitar legenda sobre esse alvo. |
| VC5 / outros banhistas | `[3130,770,680,930]` | Entrada em “outras ocupando o espaço ao redor”. |
| VC6 / fachadas e neon | `[10,10,1445,930]` | Paleta/luz e linguagem urbana. |
| VC6 / palmeiras | `[2080,10,1370,790]` | Reconhecimento tropical. |

Durante contornos, usar câmera fixa e imagem inteira (`zoom: [1,1]`). O contorno coincide com a fonte sem tracking. A legenda da praia muda para **caixa superior esquerda**, canvas lógico `{x:96,y:130,width:860,alignment:'top-left'}` (4K: x192, y260, largura1720), porque o alvo do banho de sol ocupa a base. Essa caixa fica antes do casal e acima do detector; uma legenda superior central cobriria as cabeças. A marca fica superior direita, com rótulo editorial pequeno acima da caixa. Não empilhar textos na faixa da legenda.

Para V1/V2, usar `presentation: classic-card`: quadro completo de proporção 10:7, base física sugerida `[480,252,2080,1456]` (viewport lógico `{x:240,y:126,width:1040,height:728}`), fundo grafite, rótulo “Imagem promocional do clássico”, crédito Rockstar Games e painel à direita quando necessário. Preservar os logos dentro da imagem. A imagem pode flutuar no máximo 1,2% como um cartão completo; nunca esticar para 16:9 nem usar recorte cego ou falsa nitidez. Não atribuir plataforma de captura. A composição é 4K, a fonte clássica não é.

## Mapa editorial sem timecodes

| Parágrafo | Direção e entradas vinculadas à fala |
|---|---|
| P1 | Abrir diretamente em RD2, sem vinheta. O aparelho à esquerda recebe o primeiro contorno em “a plateia sobe o celular”. Retirar o destaque para mostrar as artistas em “duas artistas”. Na conclusão, quadro completo: o excesso continua, a época mudou. Sem apresentar o título por cima da recompensa inicial. |
| P2 | V1 para a lembrança tropical, V2 na camisa de Tommy; retornar a RD2 em “Agora coloca” para a multidão. A repetição do quadro inicial acrescenta a leitura da vitrine, não é filler. |
| P3 | Cartela editorial com três itens que entram separadamente: “Identidade”, “Época”, “Além da nostalgia”. Encerrar com V1 em “A primeira pista”. |
| P4 | V1 em cartela, quadro inteiro. Texto lateral “Um lugar reconhecível” deixa a vegetação, a luz e o comércio disponíveis para a leitura da voz, sem antecipar uma lista nem ampliar detalhe insuficiente. O carro permanece reconhecível. |
| P5 | Gráfico próprio “LANÇAMENTO: 2002” entra em “dois mil e dois”; “HISTÓRIA: 1986” entra em “mil novecentos e oitenta e seis”. Em “São duas datas diferentes”, ambos permanecem. Em “atmosfera dos anos oitenta” e “lembrança de ter jogado”, duas ideias editoriais claramente separadas, sem transformar nostalgia em fato externo. |
| P6 | V2 completa em cartela. Texto breve no painel à direita: “Personagem + cidade”. O rosto e as palmeiras permanecem visíveis. Não ilustrar com Tommy em imagens VI. |
| P7 | VC6 inteira para fachadas/palmeiras/rua. Pequeno insert noturno de Trailer 1 somente se os tempos reais comportarem. Na ressalva “não transforma”, gráfico discreto “Ligação de atmosfera”, sem mapas sobrepostos ou antes/depois do mesmo endereço. |
| P8 | RD2 sem título grande; pergunta curta “Quem segura a câmera?” num espaço livre, seguida imediatamente de P9. |
| P9 | RD2 inteira, artistas no primeiro trecho. Contorno no telefone em “Há telefones erguidos”; contorno na tela real em “uma das telas mostra a apresentação”; retornar ao quadro completo em “A festa está acontecendo”. Em “Até a plateia”, deixar o conjunto legível. Análise visual identificada. |
| P10 | RD4/RD1 para apresentação oficial de música e redes sociais, com fonte S4. Em “Minha leitura”, trocar rótulo para “Leitura do canal” e RD2. “Aparecer / Crescer / Ser alguém” pode entrar como texto discreto na ordem da voz, sem painel pesado cobrindo a foto. |
| P11 | Rádio desenhado com formas vetoriais próprias sobre grafite; “RÁDIO / 1986”, “Comerciais fictícios”. Revelar “Consumo”, “Aparência”, “Sucesso” quando ditos. Fonte S3 resumida, sem copiar comerciais ou usar música deles. Voltar a RD2 em “O celular oferece”. |
| P12 | Alternar RD4 e RD2 pelo argumento música/atenção, com rótulo “Leitura do canal”. Pequenas palavras “Dinheiro”, “Prestígio”, “Atenção” podem entrar cada qual na própria fala; não ilustrar com violência/crime aleatórios. |
| P13 | Corte motivado para VC2, preparando a mudança de ponto de vista. Pergunta curta apenas; não estender a pausa. |
| P14 | VC2: quadro inteiro, depois aproximação sutil para o casal e retorno à relação varanda/piscina/praia. Texto à esquerda. Frigobar: manter a imagem, sem inserir objeto inexistente, valor inventado ou efeito de meme. Pequeno rótulo “Humor / imaginação” somente se necessário à clareza. |
| P15 | Corte para VC5 em “Agora desce”. Câmera fixa; quatro destaques individuais em sequência, cada um na fala correspondente e sem antecipar o seguinte. Legenda em cima durante esse trecho. Após o quarto, limpar os contornos para a variedade do quadro. |
| P16 | Comparação editorial VC2 → VC5. “O sonho de alguém” na varanda; “o dia comum de outra pessoa” na praia. Mostrar moradores/visitantes como interpretação, sem atribuir identidade a cada figurante. Retomar plano aberto para histórias ao redor dos protagonistas. |
| P17 | V1 para descrição clássica e VC6 para a nova cultura visual. Em “a varanda, a rua e a tela do telefone”, uma cartela revela os três termos na fala: os intervalos entre palavras são curtos demais para alternar fotografias sem criar um flash de oito frames. Fonte S1 no início; análise do canal no raciocínio. |
| P18 | Três partes, três entradas reais: “A identidade tropical continua reconhecível”; “A cultura exibida nos materiais mudou de época”; “E a memória do jogo antigo”. Gráfico próprio com itens progressivos e miniaturas identificadas, ou etapas consecutivas do mesmo gráfico. Nenhum item antes de ser dito. |
| P19 | VC1/VC6 para reconhecer; RD2 em “A plateia filmando Real Dimez”; voltar ao telefone real sem novo zoom agressivo. Pergunta final com opções “Rádio / Atmosfera das ruas / Conquistar a cidade” nas próprias palavras. Encerrar na última fala, preservando a cauda natural do áudio. Sem vinheta, inscrição ou novo resumo depois dela. |

## Contrato da timeline e orientação de implementação

Reutilizar a estrutura de L02 (`episode`, `title`, `duration`, `frames`, `fps`, `voice`, `shots`, `captions`, `paragraphs`). Todos os caminhos de L03 serão relativos à raiz do projeto, incluindo o prefixo `videosGTAVI/` quando necessário. O renderizador não deve acrescentar esse prefixo automaticamente. `voice` é o WAV normalizado validado, nunca um bloco Gemini bruto.

Cada plano terá `start`, `end`, `fromFrame`, `frames`, `kind`, `file`, `offset`, `anchor`, `label`, `title`, `sub`, `graphic`, `source`, `zoom`, `focus`, `animate` e `animationFrames`, quando aplicável. `anchor` registra a frase original e a ocorrência explicitamente resolvida; não aceitar a primeira correspondência de frase repetida. Os limites absolutos são arredondados a 30 fps; o último plano cobre `ceil(duration * 30)`.

Contrato fechado com a implementação: os overlays usam um **canvas lógico 1920×1080, escalado 2× para o render 4K**. Os retângulos do arquivo de inspeção permanecem em pixels 4K da fonte; a timeline entrega os retângulos divididos por dois e já projetados no canvas lógico. Campos adicionais e semântica:

- `presentation`: `full` para imagem VI no quadro completo; `classic-card` para V1/V2 completas sobre fundo; `graphic` para gráfico editorial próprio.
- `viewport`: objeto `{x,y,width,height}` de destino em pixels lógicos 1920×1080 para a fonte inteira, preservando sua proporção; não é um recorte da fonte. Ausente significa quadro inteiro.
- `layout`: objeto opcional `{side,top,width}` para posicionar texto no canvas lógico. `side` é `left` ou `right`. Não descreve a imagem.
- `focusRects`: objetos `{id,x,y,width,height,cue,label}` já projetados no canvas lógico. `cue` é o frame relativo ao plano. Só usar com câmera fixa; um alvo por plano reduz sequências.
- `items`: lista de strings; `cues`: lista paralela de frames relativos ao plano. Os itens anteriores usam cue negativo para permanecer imóveis; a nova entrada usa zero ou a âncora real dentro do plano. Não usar atraso automático que antecipe a voz.
- `stage`: número de itens atualmente visíveis em uma cartela progressiva. Permite cortar o plano na entrada seguinte e renderizar só a nova animação, mantendo o visual idêntico e os itens anteriores imóveis.
- `captionPosition`: `bottom` por padrão; `top` em P15 durante atividades. `panelSide`: indica lado livre de rosto/detalhe, não substitui inspeção do render.
- `evidence`: `official-image`, `official-description`, `editorial-reading` ou `editorial-graphic`, para manter clara a natureza do que está na tela.
- `editorialPurpose`: função concreta do plano, útil à revisão e ao projeto editável.

Tipos de `graphic`: `headline`, `list`, `dates`, `radio`, `focus`, ou string vazia para identificação fixa. `dates` tem dois cartões (“LANÇAMENTO\n2002” e “HISTÓRIA\n1986”); `radio` tem desenho vetorial simples próprio e a lista editorial; `list` atende P3/P18 e opções finais. Itens progressivos usam `stage` e `cues`, não entram todos no primeiro frame.

No fluxo híbrido, renderizar os gráficos animados no Remotion com `renderFrames`, resolução nativa e alpha. Entradas de cerca de 18–24 frames bastam; manter o último frame via `tpad=stop_mode=clone`. Dividir listas longas em estágios na própria fala evita centenas de PNGs vazios antes da entrada seguinte. Marca/crédito fixos podem usar frame único. Não copiar o acervo inteiro ao bundle. Movimentos da foto ficam no FFmpeg e não continuam por baixo de contornos fixos.

Recursos informados pelo coordenador em 29/10: cerca de **7,3 GiB livres em disco e 1,5 GiB de RAM livre**. Render sequencial, sem fechar aplicativos do usuário. Preferir gerar a curta sequência de um plano, compor/verificar esse plano e liberar somente os PNGs derivados desse plano quando o cache íntegro estiver confirmado. Não deixar todas as sequências 4K na memória ou em disco ao mesmo tempo; não reduzir resolução silenciosamente.

Legendas: baseadas no áudio efetivamente validado, agrupadas por sentido e pontuação, geralmente 4–8 palavras, máximo de duas linhas. Não forçar palavras ausentes para coincidir com o roteiro. Nomes, anos e “Real Dimez” precisam de revisão contra o áudio. Evitar blocos curtos por pausa mínima. Incluir SRT e legenda incorporada na etapa de implementação.

## Passagem de etapa

`edicao_l03.json` está liberado para a implementação. O gerador específico é `automacao/preparar_l03.py`; não altera o roteiro nem arquivos de áudio. Bloqueia entradas com palavras `pending_review`, exige âncoras únicas ou ocorrência explícita e valida limites, caminhos e cobertura. O ano 1986 tem duas ocorrências no áudio: o corte de P5 usa explicitamente a primeira.

A timeline usa o áudio definitivo, hash SHA256 `700311cc62811827581f30cff51b4070a5960b4875b7b0478339757746cd2636`; alinhamento SHA256 `9607eec8d27227b2abe707e4f25b1a95dac6562c8cc658eeb689b51d3fe8dc9e`. “Encenar” está em 163,29–163,75 s com status `human_confirmed` e divergência ASR “ensinar” preservada no alinhamento. Há 841 tokens ASR exatos, 31 com ambiguidade/alocação estimada, 20 expansões numéricas e um token confirmado pelo usuário. Essa procedência impede tratar todos os limites de palavras como medição manual perfeita.

Verificações da direção: 61 planos contíguos e positivos; fontes existentes; 19 parágrafos; câmera imóvel sob contornos; retângulos dentro do canvas; V1/V2 em 10:7; todos os tokens do alinhamento presentes nas legendas na ordem; nenhuma sobreposição entre legendas; UTF-8 sem caractere de substituição. Um “retorno:” de 0,42 s foi unido à pergunta anterior; as opções finais foram agrupadas por sentido. O fluxo visual previsto é 330,70 s, apenas 0,02 s acima do WAV, cobrindo seu último sample dentro de um frame.

São 24 planos com animação e 743 frames de overlay no total, incluindo estados fixos dos demais planos. A sequência mais longa tem 170 frames para a revelação dos itens do rádio; listas de P3/P18 usam estágios curtos e sustentação do último frame. Render e composição devem continuar sequenciais conforme o limite de recursos.

Não houve render ou escuta integral nesta etapa de direção. A validação das fontes foi visual; a sincronização foi conferida estruturalmente contra o alinhamento liberado. A amostra da implementação e a revisão visual/sonora do produto renderizado continuam necessárias antes de liberar o MP4 final.
