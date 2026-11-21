---
name: pixel-procurado-publicacao
description: Preparar o pacote de publicação dos vídeos do Pixel Procurado no YouTube, com thumbnail, título, descrição, capítulos, comentário fixado, tags e orientação do Studio. Use após definir o conteúdo ou finalizar o vídeo; não faz upload nem publica por conta própria.
---

# Pacote de publicação do Pixel Procurado

Entregar assets reais e textos prontos para copiar. O objetivo é despertar curiosidade compatível com a entrega do vídeo, mantendo o posicionamento do canal: “a pista vem acompanhada da fonte”. Não prometer cliques, CTR ou desempenho garantido.

## Base editorial
- Ler o roteiro/transcrição final e, quando disponível, a timeline e o MP4. Usar a duração e os tempos reais.
- Encontrar a promessa principal do episódio, sua pergunta e o benefício para quem assiste. Não reaproveitar título, fatos, datas ou personagens do primeiro episódio em temas diferentes.
- Para anúncios e informações voláteis que irão ao título/descrição, reconferir fontes primárias e registrar a data efetiva. Se houver divergência material com o vídeo, apontá-la e preparar a correção necessária; não esconder o conflito no texto de publicação.
- No projeto GamePlay, consultar [references/padrao-e-arquivos.md](references/padrao-e-arquivos.md) para a identidade e o pacote aprovado.

## Título e thumbnail como conjunto
- Antes de qualquer envio ou agendamento autorizado, exigir uma capa pronta por peça. Quando o pacote incluir longo e Short, preparar duas propostas próprias e adaptar a proporção aos destinos. Reaproveitar uma capa já aprovada quando ela ainda corresponder ao corte, ao título e à rede.
- Selecionar um título recomendado e até duas alternativas com enfoques distintos. Ser direto e natural; palavra-chave quando útil, sem empilhamento.
- A capa deve complementar o título. Poucas palavras, leitura em celular, foco claro, rosto/objeto significativo, contraste e espaço para o marcador de duração.
- Identidade inicial: grafite, branco e amarelo #FFD33D. Usar composição, iluminação e tipografia adequadas ao tema; não repetir automaticamente um layout.
- Evitar promessas não entregues: vazamento, experiência própria de jogo, segredo exclusivo, traição confirmada ou fatos não demonstrados.
- Para criação ou edição raster, aplicar a skill imagegen disponível e usar a ferramenta integrada de geração. Se usar referência local, inspecioná-la primeiro e especificar o que deve ser preservado.
- Gerar a thumbnail de fato; não entregar apenas um prompt. Inspecionar texto, rostos, enquadramento e leitura reduzida. Corrigir problemas antes da entrega.
- Preferir 16:9 exato e alta resolução, sem alegar detalhe nativo a partir de ampliação. Verificar os requisitos atuais do YouTube antes de exportar; não congelar limites antigos de tamanho.
- Salvar o master e uma versão pronta para upload (JPG/PNG compatível), no projeto. Guardar o prompt e método usados. Tratar a imagem como montagem editorial quando houver recomposição, não como uma nova captura oficial.
- Uma boa capa basta se o pedido não exigir variantes. Testes A/B só fazem sentido com alternativas de hipótese distintas e recurso disponível.
- Usar termos que o público procura no início do título e nas primeiras linhas da descrição. Priorizar consultas e dados do próprio canal quando disponíveis. A capa completa a promessa com uma pergunta, contraste ou detalhe visual. Ao testar, variar só o título ou só a capa quando a meta for isolar seu efeito. Usar CTR por origem de tráfego e tempo de exibição ou retenção para interpretar o teste.

## Textos prontos
Criar, em uma pasta de publicação do episódio:
1. Título principal em TXT.
2. Descrição em TXT: duas linhas iniciais fortes, resumo fiel, pergunta para comentários, capítulos, fontes verificadas, data de referência quando relevante, créditos e poucas hashtags pertinentes.
3. Comentário fixado ligado à pergunta do vídeo; facilitar resposta e orientar a próxima investigação.
4. Tags curtas e relevantes, incluindo grafias alternativas úteis; não despejar tags na descrição.
5. Guia de publicação com arquivos, preenchimento no Studio, tela final, alternativas de título e próximos passos.
6. Thumbnail pronta, master e prompt.

Não inventar patrocínio, links de redes sociais, vídeos futuros já publicados ou canal/playlist existentes. Nomes de playlists podem ser sugestões claramente identificadas.

Capítulos: validar início em 00:00, ordem crescente, duração mínima e requisitos atuais. Derivar os tempos do vídeo final, não do storyboard antigo. Se ainda não houver vídeo final, marcar os tempos como provisórios e não vendê-los como pacote pronto.

## Configurações e envio
- Avaliar as fontes nativas e o projeto antes de escolher o arquivo de envio. Produzir exportações próprias por rede e formato quando necessário para atingir a maior qualidade aceita. Se as fontes permitirem 4K e o destino oferecer esse suporte, reexportar o projeto em 4K. Conferir a resolução efetivamente disponibilizada após o processamento e registrar diferenças entre o arquivo enviado e a reprodução pública.
- Publicar o master aprovado na maior qualidade aceita pelo destino. Conferir limites atuais da plataforma e da integração. Quando o arquivo exceder um limite confirmado, reduzir apenas o necessário. Para limite de tamanho, calcular o bitrate pela duração incluindo áudio e margem, escolher uma codificação eficiente e preservar resolução e fps quando compatíveis. Validar detalhes, legendas e movimento na derivação.
- Tratar erros de download ou upload pelo transporte primeiro, conferindo URL, disponibilidade, tempo de resposta e configuração. Registrar o motivo de cada derivação, o limite observado e os metadados efetivamente enviados. Conferir o processamento em alta resolução na rede antes de avaliar a qualidade pública.
- Quando a publicação via Postiz estiver autorizada, conferir o suporte a capa de cada conta e formato. Anexar a versão apropriada antes do envio e verificar o resultado na rede quando possível. Distinguir capa preparada, anexada e confirmada publicamente. Registrar seleção de quadro ou edição nativa pendente quando a integração não aceitar a capa.
  - **Fluxo técnico Postiz + Cloudflare R2 neste projeto (`py -3.12`)**:
    - Validar conexão e canais antes do envio: `py -3.12 automacao/postiz_shorts.py check`.
    - Canais ativos: YouTube `@pixelprocurado` (`cmvsctfgl0001jncj932ovibv`), Instagram `@pixelprocurado` (`cmvzyw7vj0003pddwkgtivv8i`), Facebook `pixelprocurado` (`cmvzyur290001pddwolrt33em`).
    - **YouTube**: upload local pelo cliente `PostizClient` (`automacao/postiz_shorts.py`) com `type="public"`, `selfDeclaredMadeForKids="no"`, tags reais e thumbnail 16:9 (`capa_youtube.jpg`).
    - **Meta (Instagram Reels / Stories / Feed e Facebook)**: como a Graph API da Meta exige URL HTTPS pública para baixar a mídia, faça stage temporário do MP4 e da capa no bucket privado Cloudflare R2 (`pixel-procurado-publicacoes`) via `R2Media().stage(path)` (`automacao/r2_media.py`, configurado em `.production-tools/postiz-r2.json` + `%LOCALAPPDATA%\PixelProcurado\r2.xml`). Após confirmação de `state == "PUBLISHED"` e `releaseURL`, remova o objeto do R2 com `R2Media().remove(key)` e salve o manifesto JSON auditável na pasta `publicacao/`.
    - **Script padrão**: preencher o bloco `publicacao` do `<pasta>/episodio.json` e rodar `py -3.12 automacao/pipeline/distribuir_postiz.py --episodio <pasta>` (só mostra o plano). O envio real exige `--publicar` e autorização explícita do usuário. Não criar `distribuir_<id>_postiz.py` por episódio.
    - O script padrão anexa a capa no YouTube (`settings.thumbnail`) e no Instagram (`image[0].thumbnail`); o Facebook não tem rota de capa. `--publicar --agora` publica imediatamente, `--so chave1,chave2` reenvia peças específicas, `--status` consulta o Postiz e `--status --limpar` remove do R2 o que já está `PUBLISHED` com `releaseURL`.
    - **Limites observados (11/11/2026) — conferir no plano, antes do envio**:
      - Upload local do Postiz (`postiz upload`): recusa arquivos acima de ~1 GB com HTTP 413. O script já envia pelo R2 (URL) os arquivos de YouTube com 1 GB ou mais.
      - Instagram (vídeo, inclusive o integral como Reel): o erro do Postiz cita 300 MB, 1920 px e 25 Mbps. Um integral de 832 MB foi recusado. Calcular o bitrate pela duração para ficar abaixo de 300 MB (ex.: 7 min ≈ 5,2 Mbps de vídeo + 128 kbps de áudio), mantendo 1080x1920 e 30 fps.
      - YouTube e Facebook aceitaram o master 4K30 de 1,37 GB (~26 Mbps) por URL do R2.
    - **IDs dos posts**: o script procura o ID na resposta do `posts:create` e, se não vier, pelo post novo que apareceu na integração; sem ID ele para com erro e se recusa a reenviar a peça (só com `--reenviar`). Nesse caso, listar os posts do Postiz (`publicar_especial_postiz.posts()`), casar por canal, horário e título, e gravar o ID no estado antes do `--status`. O plano (sem `--publicar`) mostra o tamanho de cada mídia e marca o que passa do limite da rede.
    - "Aceito" pelo Postiz não é publicado: só `PUBLISHED` com `releaseURL` conta, e cada peça é conferida separadamente.
    - Teste A/B de título e miniatura não existe na integração: entregar título B e capa B para o usuário aplicar no YouTube Studio.
    - Scripts de referência (histórico): `automacao/postiz_shorts.py`, `automacao/distribuir_l06_postiz.py` e `automacao/publicar_especial_postiz.py`.
- Recomendar categoria, jogo quando aplicável, idioma, público e playlist conforme o episódio.
- “Não é conteúdo para crianças” e restrição etária são decisões distintas. Não inferir automaticamente 18+ só pela classificação do jogo.
- Orientar o campo de IA pela política vigente e uso efetivo; não marcar automaticamente “sim” para todo uso de ferramentas. Não afirmar clonagem da própria voz quando isso não estiver confirmado.
- Indicar que o MP4 já legendado e a faixa SRT selecionável podem exibir legendas simultâneas. Oferecer o SRT como entrega de acessibilidade, com essa informação.
- Sugerir envio como Não listado e conferência do processamento em alta resolução antes de tornar público. Isso é uma orientação, não autorização para acessar a conta ou publicar.
- Tela final no intervalo suportado, sem cobrir texto, legenda ou rostos. No primeiro vídeo, não sugerir links para episódios inexistentes.
- Sem dados do canal, não inventar “melhor horário”. Recomendar um horário em que o criador possa acompanhar e depois aprender com o Analytics.
- Não transformar créditos em promessa de licença ou ausência de reivindicação.

## Entrega e acompanhamento
Entregar a combinação recomendada e links absolutos para assets e textos. O guia deve permitir ao usuário preencher o Studio sem reconstruir a conversa. Dizer se houve ou não upload.

Para acompanhamento, sugerir observar impressões, CTR por origem de tráfego, retenção inicial e duração média; não impor metas universais ou diagnosticar cedo com poucas impressões. Não criar monitoramento, publicar comentários ou postar em outras redes sem pedido correspondente.

Consultar fontes oficiais atuais para regras de thumbnails, capítulos, tags, tela final e transparência de IA; inserir os links pertinentes no guia. Uma skill é um fluxo editorial, não uma cópia permanente das regras da plataforma.
