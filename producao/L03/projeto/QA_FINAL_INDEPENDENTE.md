# L03 — revisão final independente

**Parecer: APROVADO no escopo da revisão visual por amostragem.**

Data: 29/10/2026. Não foram encontrados problemas materiais de sentido, escolha de imagem, alvos dos contornos, sobreposição de textos ou cobertura visual que exijam correção do render. Não há nova renderização solicitada por este parecer.

## Objeto e método

Arquivo revisado: `../exportacoes/Pixel_Procurado_L03_4K.mp4`, 207.556.151 bytes, 3840×2160, 30 fps, 9.921 frames e 330,700 s. Roteiro, direção original, `DIRECAO_MONTAGEM.md` e `edicao_l03.json` foram usados para comparar a intenção com o resultado real. Aplicadas a skill pixel-procurado-video e suas referências de projeto local e validação, além do escopo econômico da skill maestra.

Foi feita uma única passagem delimitada: inspeção da folha existente `render4k/qa/contato_amostra.jpg`, da capa de upload e de **45 quadros extraídos diretamente do MP4 final unido**. A extração verificou o índice do frame pelo PTS a 30 fps, com busca localizada; não houve re-render. Os quadros foram vistos em seis folhas legíveis de 1280 px de largura, com cada miniatura em 640×360. Os JPGs individuais de 1280×720 permanecem como derivados temporários em `C:/Users/GUIBSO~1.KRA/AppData/Local/Temp/L03_QA_final_kef596sa/`, denominados `fNNNNN.jpg`; as folhas são `contato_1.jpg` a `contato_6.jpg`. Esse cache temporário pode expirar: a evidência reproduzível é o MP4 mais os índices abaixo.

Índices zero-based de todos os frames diretamente inspecionados; tempo exato = índice / 30 segundos:

```text
0, 60, 610, 980, 1050, 1110, 1160, 1650, 1975, 2055,
3120, 3650, 3800, 3831, 3995, 4058, 4133, 4140, 5089,
5180, 5250, 6256, 6275, 6405, 6418, 6470, 6590, 6840,
7115, 7167, 7275, 7330, 8550, 8650, 8868, 8950, 9034,
9666, 9680, 9748, 9770, 9828, 9865, 9900, 9920
```

## Evidências e conclusão visual

| Ponto | Tempo e frame do MP4 | Resultado |
|---|---|---|
| Abertura e celular | 00:00,000 f0; 00:02,000 f60 | Abre na imagem da apresentação. O destaque aponta o telefone esquerdo; artistas e tela ficam livres da legenda. |
| Tommy e imagem clássica | 00:20,333 f610; 00:55,000 f1650 | Nome identificado como clássico; rosto, camisa, palmeiras e logos da fonte preservados. Cartões mantêm a proporção 10:7 e a aparência da fonte de baixa resolução. Não sugerem uma captura clássica nativa 4K nem o retorno de Tommy no VI. |
| Primeira lista | 00:32,667 f980; 00:35,000 f1050; 00:37,000 f1110; 00:38,667 f1160 | Título sem itens, depois um, dois e três itens; ordem compatível com as âncoras da fala. Nenhuma lista completa antecipada. |
| Duas datas | 01:05,833 f1975; 01:08,500 f2055 | Primeiro LANÇAMENTO / 2002, depois HISTÓRIA / 1986 mantendo 2002. Distinção inequívoca entre lançamento e ambientação. |
| Atmosfera contemporânea | 01:44,000 f3120 | Fachadas, neon, pessoas e palmeiras sustentam a comparação de atmosfera, sem gráfico de equivalência entre endereços. |
| Pergunta da câmera e resposta | 02:01,667 f3650; 02:06,667 f3800; 02:07,700 f3831 | Contexto da apresentação mantido na pergunta e na resposta; nome Real Dimez legível e rostos livres. |
| Telefone e tela real | 02:13,167 f3995; 02:15,267 f4058; 02:17,767 f4133; 02:18,000 f4140 | Contorno externo do aparelho e depois contorno interno da apresentação. O desfoque original permanece; não há conteúdo reconstruído. O contorno sai quando o argumento volta à festa e ao conjunto. |
| Rádio | 02:49,633 f5089; 02:52,667 f5180; 02:55,000 f5250 | Rádio editorial identificado, início sem lista e revelação dos temas. A folha existente confirma o estado intermediário com Aparência e o estado final com Sucesso. Textos separados da legenda. |
| Pergunta da vitrine e varanda | 03:28,533 f6256; 03:29,167 f6275; 03:33,500 f6405; 03:33,933 f6418; 03:35,667 f6470; 03:39,667 f6590; 03:48,000 f6840 | Transição motivada da festa à varanda. Casal, piscina e praia reconhecíveis; legendas não cobrem os rostos. A piada do frigobar permanece sobre a foto, sem objeto ou preço inventado. |
| Quatro alvos da praia | 03:57,167 f7115; 03:58,900 f7167; 04:02,500 f7275; 04:04,333 f7330 | Contornos correspondem ao casal, à pessoa com detector incluindo a bobina, ao banho de sol e aos demais banhistas. Legenda superior esquerda preserva rostos e alvos. |
| Pontos de vista e resposta | 04:45,000 f8550; 04:48,333 f8650; 04:55,600 f8868; 04:58,333 f8950; 05:01,133 f9034 | Varanda/rua/telefone e as três partes da resposta surgem progressivamente. Hierarquia e separação entre cartela e legenda preservadas. |
| Pergunta final e término | 05:22,000 f9666; 05:22,667 f9680; 05:24,933 f9748; 05:25,667 f9770; 05:27,600 f9828; 05:28,833 f9865; 05:30,000 f9900; 05:30,667 f9920 | Pergunta inteira antes das opções; rádio, atmosfera e conquista aparecem em sequência. A última legenda está completa em f9900. O último frame conserva as três opções e cobre o final do áudio; não há vinheta ou resumo acrescentado depois. |

A inspeção sustenta a apresentação declarada: imagens promocionais oficiais com movimento 2D e gráficos editoriais Remotion. Não é gameplay próprio nem parallax 3D. Nas amostras, não há caixa sobre rosto importante, contorno em objeto errado, texto cortado ou divergência material entre a legenda e o argumento previsto.

## Capa e publicação

`../publicacao/capa_youtube.jpg` foi aberta e inspecionada: frase “A MESMA / SENSAÇÃO?” legível, marca e logo preservados e indicação “MONTAGEM EDITORIAL”. A ilustração do telefone e da apresentação corresponde ao eixo do episódio. A descrição informa que a capa é ilustrativa e não uma captura oficial ou cena nova confirmada.

Guia e descrição finais usam os mesmos capítulos: 00:00, 00:46, 02:01, 02:49, 03:29 e 04:50, coerentes com os parágrafos definidos e o arredondamento informado. O guia ainda dizia “revisão visual independente em finalização” no momento desta passagem; cabe ao coordenador atualizar somente esse estado e o checkpoint após receber o parecer. Isso não é defeito do MP4.

## QA técnica aproveitada e limites

Foram aproveitados, sem repetir testes, `render4k/qa/validacao_final.json` e `../voz/QA_AUDIO.md`: decodificação integral sem erro, correlação AAC/WAV normalizado superior a 0,99996 em sete pontos, AAC de 330,680 s, −16,85 LUFS e −1,35 dBTP. O fluxo visual de 330,700 s cobre a voz com diferença de 0,020 s. Esses resultados são evidência técnica preexistente, não medição nova desta revisão.

Não houve escuta subjetiva, nova transcrição ASR, revisão quadro a quadro integral ou julgamento contínuo de fluidez em reprodução. A sincronia foi avaliada pelas âncoras, estados visuais e legendas nas amostras, apoiada pela comparação técnica de sinais já realizada. Portanto, o parecer não garante pronúncia, interpretação, continuidade de timbre ou ausência de defeitos em frames não amostrados. O reparo “encenar” permanece aprovado pela escuta humana registrada; não foi reaberto nem atribuído a escuta deste revisor.

Nenhum vídeo, áudio, roteiro, timeline, capa ou checkpoint foi alterado. Apenas este relatório foi acrescentado ao projeto; imagens extraídas ficaram no cache temporário. Nenhuma geração paga, nova delegação, correção, renderização ou publicação foi iniciada.
