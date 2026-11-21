# Revisão independente — C04–C12

Data: 31/10/2026. Revisor independente da montagem; nenhuma fonte, mídia, produção.json ou texto de publicação foi alterado por este revisor. Única escrita: este relatório. Não houve upload, agendamento nem publicação.

## Resultado

**PASS dos nove arquivos finais no escopo técnico/editorial amostrado. Nenhuma correção obrigatória pendente.** C11 inicialmente apresentou FAIL no fechamento do loop; a cauda foi corrigida pelo executor e revalidada antes deste resultado. PASS não significa escuta humana integral, aprovação de toda pronúncia ou inspeção de todos os frames.

## Método e limites

- Lidas as skills de produção completa, vídeo, thumbnails e publicação, com suas referências de QA/formato. Lidos roteiros, timelines, títulos, descrições e tags finais, além dos relatórios de produção e alinhamento pertinentes.
- Inspecionadas visualmente as nove pranchas projeto/qa/contato.jpg e as capas reais: C04–C08 em prancha reduzida; C09–C12 em resolução integral e reduzida. As frases principais mantêm boa leitura, com identidade grafite/branco/amarelo e identificação GTA V correta em C10. Nenhuma imagem da capa foi tratada como nova captura oficial.
- Extraídos diretamente dos MP4s, via PyAV/Pillow em memória, os frames com timecodes abaixo. Esses frames não foram gravados no projeto; são reproduzíveis a partir do MP4 e seu SHA-256. Incluem início, 3 s, encerramento, painéis de mídia, listas/gráficos editoriais e detalhes marcados. Amostragem estática não prova fluidez integral.
- Metadados do stream de vídeo lidos independentemente: todos 1080×1920, 30 fps, H.264; áudio AAC 48 kHz. SRTs analisados independentemente: zero intervalos inválidos, zero sobreposições; timelines com zero lacunas entre planos. A duração visual cobre a voz dentro de um frame.
- Decodificação integral, loudness/picos e correlações foram aproveitados dos relatórios existentes projeto/qa/validacao_final.json; logs de decodificação sem mensagens de erro e hashes finais conferidos. Não repeti a decodificação integral já suficiente nem apresento essa etapa como executada pessoalmente. Correlações mínimas entre áudio exportado e WAV normalizado: ≥0,999955, em cinco janelas por vídeo. Isso evidencia preservação/alinhamento do sinal, não qualidade subjetiva ou fidelidade factual.
- AAC medido nos relatórios: −16,70 a −17,16 LUFS; picos −1,41 a −1,29 dBTP. Pequeno overshoot sobre o alvo inicial −1,5 dBTP, sem evidência de clipping. Não confundir input_i/input_tp medidos com output_i/output_tp projetados pelo filtro loudnorm.
- Não há ferramenta de escuta perceptiva disponível nesta revisão. Não afirmo ter ouvido o áudio. C06 15–19 s (Jason/Lucia) e C11 20–25,4 s (recuperação/alinhamento ASR) continuam como limitações explícitas. Legendas corretas na imagem não comprovam a pronúncia. C12 também tem correções contextuais de ASR registradas pelo executor. Nenhum desses pontos foi apresentado como erro sonoro confirmado.
- Verificada a coerência interna dos textos/fontes listadas, sem nova auditoria web das regras ou fatos já reconferidos pela produção. Não houve teste no YouTube Studio ou em dispositivo físico.

## Amostragem direta e conclusão por ID

Tempos em segundos, relativos ao MP4. As pranchas de cada episódio ampliam a cobertura com 0,30 / 1,30 / 2,80 s e pontos do corpo/fim rotulados nelas.

| ID | Resultado final | Vídeo / legendas | Frames diretos examinados | Constatação editorial |
|---|---|---|---|---|
| C04 | PASS | 77,900 s / 38 | 0; 3; 43; 49; 77,7 | Nostalgia distingue clássico e GTA VI. Real Dimez sobre o carro e plateia filmando correspondem à fala. Gráfico das três épocas legível. Gancho retorna no fim. |
| C05 | PASS | 83,667 s / 42 | 0; 3; 5,2; 7; 44; 83,5 | Gameplay no conjunto não vira classificação de cada plano. Lista oficial e hipótese da porta/carro claramente rotuladas. Entrada/estado estabelecido do gráfico amostrados. |
| C06 | PASS com limite de escuta | 74,333 s / 37 | 0; 3; 16,5; 29; 47,5; 74,2 | Artwork de Jason/Lucia e screenshot apresentados como categorias distintas. A fala sobre imagem específica justifica fotografias. Comparação hipotética não é tratada como prova. Pronúncia 15–19 s não validada por escuta. |
| C07 | PASS | 71,000 s / 39 | 0; 3; 8; 43; 70,9 | Duas fotografias específicas sustentam a comparação; a prancha mostra Cheetah e detalhe do bairro. Ausência de clipe é justificável neste ensaio de enquadramentos. Hipótese do churrasco rotulada. |
| C08 | PASS | 72,133 s / 39 | 0; 3; 8; 35; 68; 72 | Iguana identificável no recorte e no quadro inteiro, contorno aponta o animal. Ausência imaginada apresentada em gráfico, sem fabricar outra captura. |
| C09 | PASS | 82,533 s / 42 | 0; 3; 10; 23,5; 38; 82,4 | Barco em Grassrivers confirmado visualmente a 10 e 23,5 s, inclusive na legenda “A viagem continua de barco”. Não aparece jet ski nesse trecho corrigido. Keys/Grassrivers preservam a comparação de horizonte/ocultação; hipótese não confirma mecânica. |
| C10 | PASS | 81,733 s / 38 | 0; 3; 12; 33; 51; 72; 81,6 | Trechos de direção de GTA V contextualizados, sem menu de oficina nas amostras dos blocos corrigidos. Gráficos de rádio e limite “não é confirmação de GTA VI” claros. Título e descrição delimitam PC/modo Radio. |
| C11 | PASS após correção | 85,667 s / 43 | 0; 3; 5; 10; 22; 25; 35; 51; revisão final 84,8; 85,25; 85,6 | Jason/Brian e moradia contextualizados. A troca oficial é separada da hipótese de recusa e de traição. “Porque...” permanece no fechamento; cauda longa removida. Escuta do trecho 20–25,4 s não comprovada. |
| C12 | PASS | 84,167 s / 39 | 0; 3; 7; 18; 32; 45; 61; 83,3; 84 | Raul aparece nos planos próprios; pizza/plano e missão inventada explicitamente rotulados. Gráficos de risco/confiança legíveis. Final “Afinal...” liga ao gancho por texto/tema; muda a imagem no reinício, sem promessa de loop visual imperceptível. |

Título, descrição e capa dos nove mantêm a promessa do roteiro. C09 usa pergunta de suspense sem declarar emboscada; C11 trata troca/dependência sem confirmar traição; C12 questiona confiança sem anunciar missão específica. C10 usa identificação GTA V, não GTA VI. Todos possuem MP4, SRT, timeline, guia, título, descrição, comentário, tags, master, JPG, arte-base e prompt nos caminhos padrão. Presença dos arquivos auxiliares foi conferida; não equivale a revisão de cada linha de cada guia.

## Correção obrigatória encontrada e resolvida

C11 anterior: duração 88,867 s e última legenda encerrada a 85,510 s. Frames a 86 e 88,7 s mostravam plano sem legenda; validação do WAV bruto registrava silêncio de 85,571 a 88,840 s. A cauda de aproximadamente 3,3 s interrompia o loop.

O executor aparou somente o final silencioso, preservou o bruto e regenerou os derivados afetados. Resultado: WAV 85,650 s, MP4 85,667 s, SRT final 85,510 s, margem de 0,157 s. Novos frames 84,8 / 85,25 / 85,6 s, metadados, hash, continuidade, relatório de decodificação e correlações conferidos. **Achado encerrado; não resta FAIL aberto.**

## Melhorias opcionais e limites de apresentação

- C04: bloco isolado “dois,” com 0,695 s a 3,565–4,260 s. Legível, porém juntar a unidade do ano numa revisão editorial futura daria leitura mais natural. Outros blocos breves de 0,80–0,85 s são palavras finais; não justificam novo render por si só.
- C04/C05/C10/C11 reutilizam trechos curtos; C10 repete direção em vários blocos. A mídia é pertinente, mas mais variedade contextual poderia melhorar ritmo em próxima versão. Não confundir quantidade de planos originados de vídeo com movimento real: há quadros sustentados.
- Movimento real declarado pelos executores: C04 14,47 s; C05 25,30 s; C06 2,70 s; C07 0; C08 2,00 s; C09 4,70 s; C10 26,53 s; C11 23,07 s; C12 4,00 s. C06–C09 dependem de fotografias específicas; C12 tem um clipe oficial curto e análise de perfil/hipóteses. Não é um lote predominantemente feito de vídeo em movimento. Esta limitação deve acompanhar a entrega, em respeito à prioridade do usuário por clipes contextualizados.
- Quadros horizontais em painéis preservam os assuntos, mas alguns detalhes ficam pequenos em celular. Capas têm frases principais fortes; assinatura inferior é secundária e pouco legível reduzida, com pequeno avanço além do painel em algumas. Não prejudica a promessa principal.
- A recomendação de escuta pontual de C06 15–19 s e C11 20–25,4 s continua válida antes de publicar. Não houve autorização nem ação de publicação neste processo.

## Identidade dos artefatos revisados — SHA-256

Os hashes abaixo foram recalculados dos arquivos finais; caminhos relativos a producao/shorts/<ID>/.

### C04

- exportacoes/Pixel_Procurado_C04_Short_1080x1920.mp4: 8576448f0b60e150f6e5da95e7e03bf84e38b1d040a7f58cf0180ff94024cf60
- exportacoes/C04_legendas.srt: 04ff45b42b7d70c217482d49a49de422081aad1c077bed1e613fcc2cde3ba6ee
- publicacao/capa_youtube.jpg: a915b108a0746b16b9dac6765b5b8c9f72a1e5f177e148f73d725b1af4e9ffdc
- projeto/timeline.json: bbbb064dd64a4a0ad46f130cafaf3dc880b99db8e8ba5e5f0b1a187be3321ce8

### C05

- exportacoes/Pixel_Procurado_C05_Short_1080x1920.mp4: bae3805329a409badf26c3257ee145645c223e62fdecf12bebba36afb6249dd2
- exportacoes/C05_legendas.srt: 648509c3a6a03b686986859b86a0eb4166fccb80a59e7260bb0728c0e8051933
- publicacao/capa_youtube.jpg: e6ab0857eeedafff8af5c8a0837749d6e8a8f4f8e26ffef95974e04c0edaac14
- projeto/timeline.json: c050fdb217c33ed58c0c70e1fc6ade1107bf54a28c416c767411dd6e9a99ced8

### C06

- exportacoes/Pixel_Procurado_C06_Short_1080x1920.mp4: 0e943052aab7fee4448e590e21504b1c3fae9d901dbd1d625a1816b99265e9ad
- exportacoes/C06_legendas.srt: 87d9f5ddb5177c0d5dbfc097daadd6c8e869f5ab2f3152d5c5ae3f48b030f553
- publicacao/capa_youtube.jpg: 7269bf13afb385617fcc6b21871f749c7f2a7f0a9679b6ba47486fbaddcde992
- projeto/timeline.json: 2f0604545fafd25a3e0720471406eacf663c4d600d4e7d32a92db81ccfc633c7

### C07

- exportacoes/Pixel_Procurado_C07_Short_1080x1920.mp4: 29d64fcf17927b98e71f50bc351181aeccfd65a764455d506e4f01206eb16db7
- exportacoes/C07_legendas.srt: 8cf5b1753fc7044a9ee6c622e13273c12edfc43cdeb3847f9bb9997367cab296
- publicacao/capa_youtube.jpg: 90fbd0028a41f69083d7cad69519abfc7f1e45d29935c9ae7ea6445a3938c31c
- projeto/timeline.json: 927b9d1a173c98805343468c92e4f88b79ff3537e0da727adb5cdf76c966fe7b

### C08

- exportacoes/Pixel_Procurado_C08_Short_1080x1920.mp4: ad0292afce282e1cf024777c57d67d1ed1911b2fb924888e7605b94449996e1b
- exportacoes/C08_legendas.srt: 3cd0d82279fe7b5a9ff829ad01515257d28a2977124391f74decdb5d79435717
- publicacao/capa_youtube.jpg: 8b27fcd8ce14520001d8387935a008813f1514ca11265c6b266705432b968d92
- projeto/timeline.json: 64ecab931996a27daf87cf904bc71c76c681176eeac5d8690810f5a2e875de73

### C09

- exportacoes/Pixel_Procurado_C09_Short_1080x1920.mp4: c4147a8e0bb11b8a4fb6ea08e30a81445740dbb631b022e0f7c46f6535e1d982
- exportacoes/C09_legendas.srt: 7d5422d232c3723070696afd402344dea15b8553966616beb0ae8316993d62cb
- publicacao/capa_youtube.jpg: f322c37abb0b6b1b340021d76e2ed92f2f179a15cb96efe21b380b34ffc7c0b3
- projeto/timeline.json: 1c02760a14967f868fe8aca1c4c4aa663850b9bae54f4564078bb4736f572c5f

### C10

- exportacoes/Pixel_Procurado_C10_Short_1080x1920.mp4: 224bd572201f4f62a45f7245744321b1ffa68f9e38b11cd466cda4872f831d12
- exportacoes/C10_legendas.srt: 51999780579e1164faf80a7c1e442e677a26937323b69d83a4a871e6a16f03f6
- publicacao/capa_youtube.jpg: c301f8bbfb2daad09570bd1e6d47cb9be88d32cb09af872b4a807d8e0e19ae8b
- projeto/timeline.json: 1a19d19437f26746db28c4f53f97f4fafc1d58bf7f76f370808c5575eb474a49

### C11

- exportacoes/Pixel_Procurado_C11_Short_1080x1920.mp4: bb1d8d1436c8272bacf41abf7a9134a0c165675c80b93269286dd4c55d89daa0
- exportacoes/C11_legendas.srt: 2c4a5f640eb0867dcc4a73c01d452e3e9ebf0100aa91acc0eecb2548ef12e4ba
- publicacao/capa_youtube.jpg: c64f5eca2ce11c0e2df370ea23a945c7c2d47e9c6bceb8e5be88a8426ea0f4fa
- projeto/timeline.json: fb4b4bc0aeaf117fc4fc0362aa520a22b114969d09a3de39c678b779159e5c44

### C12

- exportacoes/Pixel_Procurado_C12_Short_1080x1920.mp4: 017bd138cc2aeadc57ee5546f139cca1bea6be623987b186f9bb3a321c7d8e42
- exportacoes/C12_legendas.srt: c3b63c3909996c6a09fd8eda30276e08e8fdd02b59faf66b606b836bbfefc50e
- publicacao/capa_youtube.jpg: b403d7bb1c7527039867409351243684ac8d4f667d947b40dd89373cd85d0bb3
- projeto/timeline.json: fe1520fd0686707505fed96dc128f3459b45146f28529714d021cd8b34138c51

