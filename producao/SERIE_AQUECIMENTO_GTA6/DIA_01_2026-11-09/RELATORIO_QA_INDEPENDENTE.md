# Revisão final independente — DIA01

Data: 2026-11-10. Revisão independente da montagem e dos artefatos finais; nenhum upload realizado por este revisor.

## Veredito

**APROVAÇÃO PENDENTE de uma correção visual objetiva e da classificação dos intervalos escuros.** O material representativo do master, capas A/B, capa vertical, carrossel, legendas e pacote editorial está coerente. Os contatos reais do Reel e Story revelam um retângulo grafite que substitui o footage por um instante; é necessário localizar sua duração e removê-lo caso não tenha função editorial demonstrada. Não liberar essas versões com a anomalia sem esclarecimento.

Não há indicação, nesta amostragem, de necessidade de nova narração, nova arte-base ou reconstrução integral da edição. Corrigir somente os planos afetados e revalidar esses trechos, com QA técnico dos novos arquivos quando houver remux/render.

## Evidência visual examinada diretamente

Foram abertos com view_image, e não apenas descritos por outro agente:

- qa/DIA01_Master_4K/contato_representativo.jpg: 16 quadros em 0,600; 5; 10; 15; 27; 65; 125; 151; 190; 220; 250; 265; 300; 339; 360; 371 segundos. Os caminhos nativos e o SHA256 do master constam de QUADROS_REPRESENTATIVOS.json.
- qa/DIA01_Master_4K/quadros_representativos/05_027.000_HUD.jpg, aberto separadamente: HUD real com triângulo Slim Jim e círculo Smash Window; ampliação e legenda sem sobreposição prejudicial.
- qa/DIA01_Instagram_Integral/contato_16_quadros.jpg: tempos 11,633; 34,900; 58,167; 81,433; 104,700; 127,967; 151,233; 174,500; 197,767; 221,033; 244,300; 267,567; 290,833; 314,100; 337,367; 360,633 s.
- qa/DIA01_Reel_HUD/contato_16_quadros.jpg: 16 amostras entre 1,957 e 60,664 s, tempos completos em RELATORIO_QA.json.
- qa/DIA01_Story_HUD/contato_16_quadros.jpg: 16 amostras entre 0,527 e 16,328 s, tempos completos em RELATORIO_QA.json.
- comparacao_capas_AB.jpg; social/capa_vertical_hud.png; social/carrossel_01.jpg a carrossel_04.jpg, estes últimos abertos individualmente em dimensão integral.

## Achados que exigem resolução

1. **Retângulo grafite nos cortes verticais.** Story em 6,847 s (contato, linha 2/coluna 3) e Reel em 52,837 s (linha 4/coluna 2) mostram a área do gameplay substituída por uma cartela grafite, com texto tênue no Story. HUD superior, card inferior e legenda permanecem. Ambos correspondem ao início do bloco “No primeiro dia de jogo...”, associado ao parágrafo 28. O revisor comunicou o achado imediatamente e solicitou ao executor frames nativos adjacentes e duração. A origem (fonte, overlay ou extração) ainda não foi comprovada nesta revisão. Se está no MP4, eliminar a cartela acidental, preservando duração e áudio. Inspecionar o mesmo bloco nos dois integrais, pois os contatos gerais não amostram o instante exato.
2. **Intervalos escuros precisam ser reconciliados com a fonte.** O relatório técnico do master marca 202,167–202,633 s, 210,867–212,400 s e 268,167–268,533 s. O Instagram integral marca os equivalentes e mais 216,067–216,267 s e 217,567–217,767 s. O quadro de 220 s mostra uma cena escura legítima com velas; ele não prova a origem dos intervalos anteriores. Solicitei ao executor evidência focada. Fades intencionais e escuridão da cena podem ser aceitos se documentados; lacunas ou cartelas acidentais devem ser corrigidas. Não chamar blackdetect isoladamente de erro de render.

## Resultado das demais verificações

- Abertura: imagem do jogo e frase “Esquece a bazuca na cueca.” no quadro de 0,6 s, sem vinheta anterior. A timeline reserva 2,4 s ao gancho de cinco palavras.
- Relação fala/plano: prédio aos 65 s, laboratório aos 125 s, equipamento/pistola aos 151 s, fumaça/corredor aos 190 s, ambiente de velas aos 220 s, escritório aos 250/265 s e carro/HUD aos 27/300/339 s correspondem ao assunto narrado/legendado. O encerramento usa footage de ambientação; não o apresenta como evidência técnica do tamanho de instalação.
- Diversidade: a timeline contém 31 blocos, com fontes do prédio, laboratório, combate, escritório, carro e ambientação. Reprises do HUD têm função de gancho/payoff e de comparação dos comandos. O trecho de inventário retorna ao combate para analisar equipamento. Não identifiquei repetição gratuita nas amostras; esta é uma avaliação amostral, não inspeção quadro a quadro.
- Cards: nos quadros de 0,6 e 5 s há cards compactos; aos 10 s a cena está livre. Isso comprova estados de entrada/leitura e ausência depois, sem comprovar subjetivamente a suavidade de toda animação. Cards não encobrem o HUD ampliado no frame de 27 s. Os contatos verticais preservam HUD destacado e legendas em zona separada.
- HUD: símbolos conferidos visualmente; os nomes corretos também aparecem na timeline/publicação. Referência de fonte é aproximadamente 6 minutos, com frame 364,9 s documentado em RECONCILIACAO_HUD.md, sem usar um rótulo falso de 370 s como prova.
- Legendas: nas amostras lidas, texto branco legível, contorno consistente e sem colisão com HUD. Relatórios técnicos registram limites válidos e ausência de sobreposição temporal: 194 cues em cada integral, 30 no Reel e 9 no Story.
- Fato versus interpretação: pacote identifica análise de imagens, sem teste jogável próprio; timeline rotula consequências como análise editorial; carrossel 04 explicita a diferença. Isso é necessário porque falas sobre perseguição, silêncio e “três segundos” não são comprovadas apenas pelo HUD. A descrição e os avisos devem acompanhar a publicação. O título B expressa a hipótese editorial; não tratá-lo como resultado de teste próprio.
- Capas: variantes “ESQUECE O GTA 5” e “QUAL BOTÃO?” são legíveis em comparação reduzida, com marca, logo e uma tensão visual coerente com a porta do carro. A descrição declara montagem editorial. Capa vertical e slides usam captura autêntica e ampliação do comando. Os quatro slides não confundem círculo e triângulo; textos cabem sem truncamento.
- Capítulos: comparados com a timeline e o ledger finais. 00:59 → 59,833 s; 01:57 → 117,367 s; 02:24 → 144,733 s; 03:01 → 181,900 s; 03:32 → 212,400 s; 03:57 → 237,367 s; 04:37 → 277,733 s; 05:44 → 344,633 s. Arredondamento para segundo anterior inferior a 1 s, adequado. Duração final 6:12,267.

## QA técnico consultado, sem duplicação dos processos longos

Fonte: RELATORIO_QA.json dos quatro finais, VALIDACAO_AUDIO_FINAL_HUD.json e ledger final.

| Arquivo | Duração vídeo | Decode integral | LUFS / pico AAC | Correlação mínima consultada |
|---|---:|---|---|---:|
| DIA01_Master_4K.mp4 | 372,266667 s | passou | -16,8 / -1,4 dB | 0,999983 |
| DIA01_Instagram_Integral.mp4 | 372,266667 s | passou | -16,8 / -1,0 dB | 0,999543 |
| DIA01_Reel_HUD.mp4 | 62,600 s | passou | -16,7 / -1,2 dB | 0,999547 |
| DIA01_Story_HUD.mp4 | 16,833333 s | passou | -16,8 / -1,3 dB | 0,999667 |

Os quatro relatórios têm temporal_errors vazio. Master 3840×2160; peças verticais 1080×1920; H.264/yuv420p, 30 fps, AAC 48 kHz. Diferença entre áudio e vídeo integral inferior a um frame. Picos AAC acima do alvo inicial -1,5 dBTP, porém abaixo de 0 dB; não constituem clipping pelos valores medidos e não exigem normalização adicional isoladamente.

## Limitações e fechamento

Esta foi revisão visual real por amostragem e leitura dos relatórios técnicos. **Não houve escuta subjetiva do áudio nesta revisão**; correlação e ASR não provam pronúncia, naturalidade nem continuidade perceptiva das emendas 296,24–300,48; 308,28–311,24; 337,44–339,78 s. Registro de alinhamento informa 1150 palavras e equivalência de sequência, sem substituir escuta. Também não houve reprodução contínua integral para avaliar ritmo/movimento.

A pesquisa factual externa não foi repetida: o coordenador confirmou ter verificado diretamente as páginas oficiais Rockstar sobre gameplay, pré-load 10/11, lançamento 19/11 e instalação até 212 GB conforme dispositivo. Esse é um relato atribuído ao coordenador, não uma verificação web independente deste revisor.

Após resolver os dois achados visuais, o executor pode registrar evidência focada e o coordenador atualizar a decisão, sem repetir a revisão completa. Os demais artefatos examinados ficam aprovados dentro do escopo e das limitações acima.
