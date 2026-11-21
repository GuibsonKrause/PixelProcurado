# Publicação L03 — pacote do vídeo completo

Preparação editorial: 29/10/2026. **Pacote concluído e vídeo publicado pelo Postiz**, após pedido explícito do usuário: [assistir no YouTube](https://www.youtube.com/watch?v=tH56UHaRo54). MP4 completo decodificado sem erros e aprovado em revisão visual independente por amostragem de 45 frames.

Publicação confirmada em 29/10/2026, 16h22 (São Paulo): Postiz **PUBLISHED**, post `cmvtwp2k90006jncj27z1e8dx`, YouTube `tH56UHaRo54`. A consulta pública oEmbed retornou o título correto e o canal Pixel Procurado. Foram enviados vídeo, thumbnail, título, descrição com capítulos, tags, visibilidade pública e indicação de que não é conteúdo para crianças. Registro em `POSTIZ_ESTADO.json`; não criar outro post para este episódio. A resolução disponível no player do YouTube ainda depende do processamento da plataforma; não foi afirmada conclusão do processamento 4K.

O conector instalado não expõe categoria, idioma, campo de IA, envio de SRT selecionável nem fixação de comentário. Conferir esses campos no Studio, usando as orientações abaixo; as legendas já estão gravadas no MP4, e o comentário está preparado em `03_COMENTARIO_FIXADO.txt`. Esses passos não foram feitos automaticamente.

Foi corrigido um erro de mídia local do Postiz v2.25.3 que bloqueava localhost antes do envio. O provedor agora lê apenas seus uploads próprios em disco, mantendo proteção de rede para outras URLs. O ajuste persistente e a reversão estão documentados em `C:/Users/guibson.krause/Documents/ChatGPT/Postiz/overrides/FIX_LOCAL_YOUTUBE.md`. O mesmo post foi retomado; não houve upload duplicado nem publicação de outros episódios.

Vídeo: `../exportacoes/Pixel_Procurado_L03_4K.mp4`, **3840×2160, 30 fps, H.264/AAC a 48 kHz**, 9.921 frames, **5min30,700s**, **207.556.151 bytes**. O áudio tem 330,680 s: o quadro final completa o arredondamento a 30 fps, diferença de 0,020 s. São 61 planos e 146 blocos de legenda. O MP4 inclui legendas gravadas na imagem; o SRT separado está no mesmo diretório. Referência editável: `../projeto/edicao_l03.json`.

QA técnica: `../projeto/render4k/qa/validacao_final.json`. Volume observado depois da codificação AAC: **−16,85 LUFS / −1,35 dBTP**. A correlação do sinal com a narração normalizada ficou acima de 0,99996 em sete amostras distribuídas. Isso verifica preservação e alinhamento técnico, não substitui escuta subjetiva integral.

Revisão independente: `../projeto/QA_FINAL_INDEPENDENTE.md`, parecer **APROVADO**, sem correção material. Foram inspecionados começo, fim, listas progressivas, datas, contornos, varanda, praia e capa. É revisão visual por amostragem; não houve escuta subjetiva integral. A frase de reparo “encenar” tem aprovação auditiva explícita do usuário, registrada no QA de áudio. A montagem usa imagens oficiais com movimentos 2D e gráficos animados; não é gameplay próprio nem parallax 3D. As fontes clássicas de 640×448 são apresentadas com a proporção preservada em uma composição 4K.

## Combinação recomendada

**Título:** Vice City clássica e GTA VI: o que mudou além dos gráficos

**Capa:** `capa_youtube.jpg`, frase **A MESMA / SENSAÇÃO?**. O título delimita a análise cultural; a capa coloca a dúvida sobre reconhecimento e nostalgia. A arte está pronta e foi preservada.

Alternativas, caso se queira mudar o enfoque editorial:

- A nova Vice City ainda tem a alma do clássico?
- GTA VI: o que o celular muda em Vice City?

Não acrescentar data de lançamento, gameplay próprio, retorno de Tommy ou comparação do mesmo endereço: essas promessas não pertencem ao episódio.

## Arquivos para publicar

| Entrega | Estado |
|---|---|
| `01_TITULO.txt` | Pronto para copiar |
| `02_DESCRICAO.txt` | Descrição pronta com seis capítulos; usar este arquivo em vez do rascunho antigo |
| `03_COMENTARIO_FIXADO.txt` | Pronto; publicação e fixação ficam com o usuário |
| `04_TAGS.txt` | Pronto; usar no campo Tags |
| `capa_youtube.jpg` | 1280 × 720, 433.785 bytes, RGB, 16:9 |
| `capa_master.png` | 1920 × 1080; composição com base nativa 1672 × 941 |
| `PROMPT_THUMBNAIL.txt` e `QA_THUMBNAIL.md` | Método, resolução e inspeção visual documentados |
| `../exportacoes/Pixel_Procurado_L03_4K.mp4` | Vídeo completo com QA técnica aprovada |
| `../exportacoes/Pixel_Procurado_L03_4K.srt` | 146 blocos em Português (Brasil) |
| `07_CREDITOS_E_MIDIAS.md` | Fontes e método da edição efetivamente usada |
| `../projeto/edicao_l03.json` | Timeline editável com fontes, tempos e animações |

O arquivo `02_DESCRICAO_RASCUNHO.txt` foi preservado como versão anterior; não é a referência para copiar no Studio. Os capítulos finais derivam da timeline efetivamente renderizada e da duração observada no MP4, arredondados ao segundo mais próximo.

## Preenchimento no Studio

| Campo | Orientação para L03 |
|---|---|
| Categoria | Jogos |
| Jogo | Grand Theft Auto VI, se a entrada correspondente estiver disponível |
| Idioma do vídeo, título e descrição | Português (Brasil) |
| Público | Não é conteúdo para crianças; trata-se de análise de um jogo para público adulto |
| Restrição etária | Avaliar as cenas efetivamente exibidas; é uma decisão separada de conteúdo para crianças |
| Playlist | Sugestão: “Vice City — memória e transformação”; não foi verificada a existência de uma playlist no canal |
| Licença | Licença padrão do YouTube |
| Comentários | Ativados, com moderação conforme a preferência do canal |
| Promoção paga | Responder conforme relações comerciais reais; não há patrocínio identificado neste pacote |
| Local de gravação | Deixar vazio |
| Tags | Colar `04_TAGS.txt` no campo próprio |
| Visibilidade inicial | Não listado, para conferir o processamento |

### Uso de IA

A produção utiliza narração sintética com Gemini e thumbnail ilustrada gerada por IA. Isso consta nos créditos e na descrição. O MP4 usa imagens promocionais de jogos e gráficos próprios. A origem da voz personalizada não está documentada como clonagem da própria voz do criador. A orientação é declarar a narração sintética se ela se enquadrar como áudio realista no campo **Uso de IA** do Studio; essa recomendação decorre da voz, não do simples uso de ferramentas na capa ou nas legendas.

A política atual distingue assistência à produção e conteúdo irrealista de material gerado que parece real. Thumbnail assistida, legendas e ajustes estéticos são exemplos que dispensam declaração por si só. Voz/áudio gerado com aparência realista deve ser avaliado pela regra de declaração; uma fabricação realista que represente pessoa ou acontecimento real exige “Sim”. Não está documentado aqui que a voz seja clonagem da própria voz do criador; portanto, não aplicar essa exceção por suposição. [Regra oficial](https://support.google.com/youtube/answer/14328491?hl=pt-BR).

## Capítulos do arquivo final

```text
00:00 O celular na nova Vice City
00:46 A memória do clássico
02:01 Quem segura a câmera?
02:49 Rádio, ambição e aparência
03:29 Da varanda à praia
04:50 A mesma Vice City?
```

Tempos derivados dos inícios reais dos parágrafos 1, 4, 8, 11, 13 e 18 da timeline, confirmada no MP4 sem inserção ou corte adicional. Durações dos capítulos: 46, 75, 48, 40, 81 e 40,70 segundos. O último inclui a pergunta final. Não se estimaram tempos pela quantidade de palavras.

Os seis tempos começam em 00:00, estão em ordem crescente e têm duração superior a dez segundos, inclusive o último. [Regras de capítulos](https://support.google.com/youtube/answer/9884579?hl=pt-BR).

## Tela final

O YouTube admite tela final nos últimos cinco a vinte segundos de um vídeo com pelo menos 25 segundos. Neste arquivo, a janela máxima é **05:10,70–05:30,70**. A recomendação para esta edição é priorizar a pergunta e suas opções, deixando a tela final opcional: não há vinheta vazia reservada. Se adicionar inscrição, confira no preview do Studio um intervalo mínimo de cinco segundos e uma posição que não cubra legendas, rostos ou opções. Se não houver área livre, deixe sem elemento. Só vincule vídeo ou playlist que já exista no canal; nenhum destino foi presumido. [Regra oficial](https://support.google.com/youtube/answer/6388789?hl=pt-BR).

## Conferência e envio, após a finalização

1. Selecionar o MP4 efetivamente validado, preencher título e descrição final e enviar a capa JPG.
2. Ajustar público, idioma, categoria e o campo Uso de IA de acordo com o conteúdo final.
3. Adicionar o SRT em Português (Brasil), se desejar a faixa selecionável. Caso o MP4 tenha legendas gravadas na imagem, ativar o SRT poderá exibir duas legendas; conferir a visualização. O SRT também oferece acessibilidade e tradução.
4. Configurar os capítulos validados e a tela final no intervalo documentado na versão final deste guia.
5. Enviar como Não listado e aguardar a resolução final aparecer no player. Conferir abertura, transições, exemplos visuais, pergunta final, áudio e legendas.
6. Revisar as verificações do Studio. Atribuir créditos não concede licença nem garante ausência de reivindicação.
7. Tornar público ou programar quando estiver satisfeito com a conferência. Publicar e fixar o comentário preparado é uma ação posterior do usuário.

## Regras técnicas reconferidas em 29/10/2026

- [Thumbnails](https://support.google.com/youtube/answer/72431?hl=pt-BR): JPG/PNG, 16:9, largura mínima de 640 pixels; recomendação atual 3840 × 2160. Limites: 2 MB em dispositivo móvel e 50 MB em computador. A capa entregue atende ao mínimo e aos dois limites; não se criou ampliação 4K apenas para imitar detalhe nativo.
- [Capítulos](https://support.google.com/youtube/answer/9884579?hl=pt-BR): 00:00, três ou mais entradas crescentes, dez segundos mínimos por capítulo.
- [Tags](https://support.google.com/youtube/answer/146402?hl=pt-BR): contribuição geralmente pequena, útil para grafias alternativas; título, capa e descrição têm maior papel. Não despejar tags na descrição.
- [Tela final](https://support.google.com/youtube/answer/6388789?hl=pt-BR): últimos cinco a vinte segundos; vídeo mínimo de 25 segundos; até quatro elementos em 16:9. O pacote buscará apenas os elementos que couberem na composição final.
- [Transparência de IA](https://support.google.com/youtube/answer/14328491?hl=pt-BR): avaliar realismo e alteração significativa, não apenas a presença de ferramentas de IA.

## Fontes editoriais e escopo da checagem

- [Rockstar — Vice City](https://www.rockstargames.com/games/vicecity): origem das imagens clássicas documentada no roteiro e na direção em 25/10/2026. Página acessada novamente em 29/10, mas o extrator não retornou corpo textual; não se alega nova inspeção completa da página nesta etapa.
- [Take-Two — décimo aniversário](https://ir.take2games.com/static-files/fbf04d7a-8b78-4537-beca-2ea45ddb590d): PDF reconferido em 29/10; sustenta lançamento original em outubro de 2002 e contexto satírico dos anos 1980.
- [Rockstar — comerciais de rádio](https://www.rockstargames.com/newswire/article/51974aa3858ak3/advertising-council-site-updated-with-classic-radio-ads-from-pet.html): conteúdo oficial recuperado pela busca em 29/10; lista “Vice City, 1986” e os comerciais citados como contexto histórico. A página aberta diretamente não trouxe corpo no extrator.
- [Rockstar — Only in Leonida](https://www.rockstargames.com/VI/only-in-leonida): perfil de Real Dimez reconferido em 29/10; relação entre música e presença nas redes sustentada pelo texto oficial. A interpretação sobre a plateia é do episódio.
- [Rockstar — mídia](https://www.rockstargames.com/VI/media): biblioteca oficial acessível em 29/10; o episódio analisa uma seleção do acervo, não promete inventário atualizado de tudo que existe.

## Após publicar

Escolher um horário em que o criador possa acompanhar os comentários; não há histórico do canal nesta tarefa para indicar um horário vencedor. Observar impressões, CTR por origem, retenção inicial e duração média, levando em conta o volume de dados. Não definir meta universal nem trocar título e capa em resposta a poucas impressões. Este guia não cria monitoramento nem autoriza postagem.
