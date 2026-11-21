# DIA 10 — pacote de publicação em preparação

Referência editorial: 18/11/2026 às 18 h BRT. BLOQUEADO: a segunda tentativa de B02 atingiu o limite de 360 s às 02:09:55 BRT, sem WAV. Apenas B01 foi obtido. Não há áudio master/alinhamento aprovados; timeline, legendas, vídeos, capítulos e revisão final estão pendentes. Nenhum upload ou agendamento realizado.

## Título e capa

Conjunto A: `01_TITULO.txt` + `capas/capa_longo_A.jpg` (É AMANHÃ!). Conjunto B: `01_TITULO_B.txt` + `capas/capa_longo_B.jpg` (TUDO PRONTO?). Verticais: `capas/capa_vertical_A.jpg` e B. Os quatro masters sem perdas ficam em `capas/longo_A/`, `longo_B/`, `vertical_A/`, `vertical_B/` como `capa_master.png`.

É montagem editorial determinística de imagem oficial com texto e logo oficial; sem imagem de IA e sem cronômetro. A mesma imagem e grade nas variantes permitem comparar a frase. Para isolar um teste, mudar somente título OU capa de cada vez; o usuário aplica no Studio, a integração não configura A/B.

A ferramenta padrão compõe horizontal 1280×720 e vertical 1080×1920, com JPGs abaixo 2MB. A recomendação atual do YouTube é 3840×2160/2160×3840; o mínimo é 640 px, e o limite depende do dispositivo (2MB móvel,50MB desktop). Estes JPGs usam um tamanho conservador compatível. Não confundir o tamanho da capa com o master de vídeo 4K. [Documentação atual de thumbnails](https://support.google.com/youtube/answer/72431?hl=en), consultada 18/11/2026.

## Textos e validação

Copiar `02_DESCRICAO.txt`, `03_COMENTARIO_FIXADO.txt` e `04_TAGS.txt`. Dados completos e textos para outras redes em `METADADOS_BASE.json`. Validação em `VALIDACAO_METADADOS.json`: títulosA56/B51 caracteres, descrição 2307 caracteres,12 tags/peso 220. Teto editorial deste pacote:100/5000,até 15 tags e peso<400, calculado por len+2 quando houver espaço+1 por item. Não despejar tags na descrição; [o YouTube destaca título,capa e descrição acima das tags](https://support.google.com/youtube/answer/146402?hl=en).

O carrossel tem 4 JPGs 1080×1350 em `carrossel/01.jpg` a `04.jpg`. Fontes e ressalvas estão nas próprias peças; legenda pronta no JSON. Capas e carrossel foram inspecionados visualmente pelo executor em suas folhas reduzidas. A revisão final independente do pacote continua pendente.

## Capítulos e tela final

Ainda não há capítulos copiáveis: derivar de áudio/timeline final e conferir no MP4. Lista planejada: comparação de fusos; protocolo; horário local; exposição a spoilers; pré-carregamento; preparo do console; edições; ajustes iniciais; checklist;DIA11. A lista final deve começar 00:00, ter ao menos 3 entradas crescentes e capítulos de pelo menos 10 s. [Regras oficiais](https://support.google.com/youtube/answer/9884579?hl=en).

Tela final só após conhecer duração: escolher trecho dentro dos últimos 5–20 s, preservando legenda/rostos/textos. Vincular vídeo existente apenas depois de confirmar o endereço. Não criar link para DIA11 ainda não publicado. [Tela final oficial](https://support.google.com/youtube/answer/6388789?hl=en).

## Arquivos de vídeo por destino

Masters pedidos: longo 3840×2160 e integralvertical/Reel/Story 2160×3840,30 fps. A composição vertical pode conter a fonte 16:9 inteira sobre grafite; isso preserva o quadro e não representa detalhe nativo 3840 px em uma fontehorizontal de 2160 px de altura. VersõesIG1080×1920,30 fps,até 300MB serão preparadas genericamente apósmasters/QA para compatibilidade com o limite observado no Postiz local em 11/11/2026 (não é afirmação de teto universal da Meta). Sem reduzir masters 4K silenciosamente. Reel=P04–P06,Story=P01, samples contíguos da voz principal; não regravar.

Cada arquivo final teráQA técnico, legendas incorporadas eSRT separado. Enviar SRT como faixa selecionável pode resultar em duas legendas visíveis quando o player também mostra a incorporada; conferir antes. Conferir processamento 4K público quando houver envio autorizado; um arquivo aceito ainda pode estar processando.

## Studio e aprovação

Idioma sugerido: português(Brasil); categoria: jogos; jogo:GTA VI quando disponível. Conteúdo editorial sobre jogo adulto não foi dirigido a crianças; isso é separado de restrição etária, que depende do conteúdo real da montagem. Playlist somente se existente/confirmada. A descrição declara voz sintética; no campo de IA, avaliar uso efetivo conforme a [política atual](https://support.google.com/youtube/answer/14328491?hl=en), sem afirmar clonagem da própria voz não comprovada nem marcar todo auxílio de ferramenta automaticamente.

Após revisão final comsha 256 dos arquivos atuais, conferir plano do distribuidor genérico e anexos. Antes disso, sem upload/stageR2,registro de posts ou agendamento. O horário 18 h foi fornecido para o episódio; não é alegação sobre melhor horário de audiência. Acompanhar impressões,CTR por origem e retenção sem inventar metas universais.
