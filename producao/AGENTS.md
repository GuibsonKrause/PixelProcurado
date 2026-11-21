# Roteiros e narração do Pixel Procurado

Use `pixel-procurado-roteiro` para novos roteiros ou revisões, `pixel-procurado-gemini-tts` para locução e `pixel-procurado-video` para montagem. O padrão aprovado está em [REVISAO_V2.md](ESPECIAL_PRE_LANCAMENTO_2026-11-06/REVISAO_V2.md). Planeje vídeo pertinente primeiro, imagens quando necessárias e cards breves que saem após a leitura.

Para criar ou revisar roteiros longos e Shorts, ler `editorial/PERFIL_NARRACAO.md` e `GUIA_ROTEIROS_RETENCAO.md`. O perfil de humor brasileiro é o padrão solicitado pelo usuário em 29/10/2026, inclusive para episódios futuros.

Usar linguagem falada, humor ácido situacional, comparações absurdas com lógica, autoironia e entrega seca. Preservar evidências e distinguir hipótese de fato. A piada deve ajudar a entender o assunto; não preencher cotas de palavrões, memes ou risadas.

Entregar narração limpa e uma cópia Gemini com as mesmas palavras. Consultar `editorial/EXPRESSOES_GEMINI.md`; eventos vocais pontuais ficam somente na cópia Gemini e a interpretação geral fica em Style. Estilo-base: `editorial/ESTILO_NARRACAO_HUMOR_BR.txt`. Preservar a voz personalizada configurada.

Ao editar, sincronizar TXT, documento consolidado dos cortes e cópias em `shorts/<ID>/voz`. Atualizar a direção, a contagem e o estado da revisão. Áudios, legendas, timelines e vídeos de versões anteriores não validam o texto novo. Não sobrescrever mídia publicada nem recriar áudio sem solicitação de produção.

L01, L02, C01, C02 e reservas de L01 ficaram fora da reescrita de 29/10/2026. Só revisá-los por pedido específico. O padrão vale para roteiros novos de qualquer formato.

Entrada da revisão: `editorial/revisao_humor_2026-10-29/LEIA_ME.md`. Arquivos em `historico`, prévias e blocos de voz explicitamente marcados como antigos são registros, não entradas atuais de produção.


## Regra de abertura — atualização solicitada em 29/10/2026

Projetar os primeiros três segundos com uma fala de cerca de cinco ou seis palavras que já entregue uma descoberta, contraste ou pergunta concreta. Começar a voz no primeiro quadro e mostrar uma evidência; a frase seguinte deve desenvolver ou responder o gancho. Sem apresentação do canal, vinheta, respiração ou risada antes dele. Medir o tempo real na locução e ajustar o texto se não couber, sem impor leitura corrida. A meta de três segundos é de construção; retenção depende de medição com público. Exemplos atuais em `editorial/revisao_humor_2026-10-29/GANCHOS_3_SEGUNDOS.md` (a partir da pasta producao).

## Qualidade dos arquivos publicados

Antes da exportação final, avaliar a resolução nativa das fontes e a maior qualidade aceita em cada rede, formato e rota de publicação. Preparar um arquivo específico por destino quando isso permitir qualidade superior. Reexportar do projeto e das fontes nativas em 4K quando houver suporte confirmado; o master 1080p existente não define o teto dos próximos envios. Registrar as limitações das fontes de menor resolução e do processamento de cada rede.

Usar o master aprovado na maior qualidade aceita por cada destino. Conferir os limites atuais da rede e da integração antes de derivar arquivos. Quando excederem um limite confirmado, reduzir somente o necessário, priorizando preservar resolução, fps, legibilidade e enquadramento. Ajustar codificação e bitrate antes de reduzir resolução ou fps quando o limite for de tamanho. Calcular o orçamento pela duração, incluindo áudio e margem de contêiner, e validar visualmente o resultado. Falha de transferência exige diagnóstico do transporte e da URL antes de nova compressão. Registrar o limite observado, a mudança aplicada e os metadados do arquivo enviado.

## Capa para cada vídeo publicado

Antes de enviar ou agendar, preparar e conferir uma thumbnail própria para cada peça solicitada. Usar 16:9 no longo horizontal e 9:16 no Short e nos Reels. Aplicar `pixel-procurado-thumbnails` e `pixel-procurado-publicacao` para combinar intenção de busca, título e capa. Usar a logo correta e inteira, texto curto e um ponto focal legível em celular.

No Postiz, conferir o suporte à capa por integração, anexar a variante correspondente e verificar a capa pública quando for possível. Se o destino usar seleção de quadro ou edição nativa, guardar o arquivo da capa e registrar o que ficou pendente. O status de publicação do vídeo, por si só, não valida a capa.

## Publicação de episódios longos no Instagram

Quando a publicação de um novo episódio no Instagram estiver autorizada, incluir três peças distintas: o vídeo completo como Reel, o corte curto como Reel e o Story. Adaptar o vídeo integral ao formato vertical preservando todo o enquadramento relevante e a legibilidade das legendas, como no L05. Validar cada peça e confirmar separadamente seu estado no Postiz. Conferir os limites vigentes da integração antes do envio e sinalizar qualquer impedimento à publicação integral.

Para entregar mídias ao Instagram e ao Facebook pelo Postiz, usar o bucket R2 privado e o Worker configurado em `.production-tools/postiz-r2.json`, por meio de `automacao/r2_media.py`. Criar uma chave de objeto por publicação, guardar a chave no registro local e conferir se a mídia estará disponível na hora de publicar. Os links atuais expiram em sete dias. Após o Postiz confirmar `PUBLISHED` com link público, remover a cópia do R2. O comando `status` de `automacao/distribuir_l06_postiz.py` serve como referência para essa limpeza.
