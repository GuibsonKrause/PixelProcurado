# L05 — revisão independente final

Revisão em 03/11/2026. Escopo: artefatos locais finais; nenhuma publicação ou alteração de conta executada por este revisor. Somente este relatório é de sua responsabilidade. Revisão visual por amostragem, leitura editorial e conferências deterministas; **não houve escuta subjetiva integral**.

## Resultado por formato

| Formato | Resultado | Base |
|---|---|---|
| YouTube/master 4K integral | **PASS** | 58 quadros próprios do MP4 final, 47 planos representados, legenda/timeline/capa/pacote coerentes e QA técnica existente conferida |
| Facebook feed 1080p | **PASS** | Arquivo fechado: metadados/hash próprios, amostras próprias e QA integral/áudio conferida |
| Instagram integral 1080×1920 | **PASS** | Arquivo fechado: quadro completo, legendas legíveis e sem duplicação nas amostras |
| Facebook/Instagram Story 1080×1920 | **PASS** | Mesmo arquivo fechado para ambos: 24,45s áudio/24,466667s vídeo, início e último quadro conferidos |

PASS master vale estritamente para o SHA256 abaixo. Não libera outros arquivos por semelhança de nome. Nenhuma correção obrigatória identificada no master/capa/pacote YouTube.

## Evidência visual própria

Foram extraídos quadros diretamente de `exportacoes/Pixel_Procurado_L05_4K.mp4` com FFmpeg, em pasta temporária `C:/Users/GUIBSO~1.KRA/AppData/Local/Temp/L05_QA_INDEPENDENTE/`. Inspecionadas quatro pranchas dos pontos médios dos 47 planos, mais prancha de 11 pontos críticos. As imagens temporárias não alteram a mídia de produção.

Pontos médios, plano 00–46, em segundos: 1.433; 8.567; 19.800; 28.633; 35.483; 41.250; 49.967; 59.233; 63.367; 71.383; 80.833; 87.200; 93.650; 99.900; 105.067; 110.067; 120.050; 129.750; 136.333; 146.433; 154.800; 163.850; 173.500; 182.567; 190.583; 197.750; 206.550; 211.900; 216.233; 220.250; 226.083; 230.800; 235.350; 241.983; 250.483; 258.767; 265.333; 272.283; 278.383; 283.350; 289.517; 296.033; 299.900; 302.817; 307.783; 313.933; 320.650.

Pontos adicionais: 0; 0.5; 2; 2.9; 65.5; 69.5; 74; 77; 237.8; 324.3; 324.833s. Abertura entrega fotografia/evidência desde o primeiro quadro; gancho legível e plano muda em 2,867s. Encerramento conserva a imagem até o último frame, sem tela preta ou truncamento visual nas amostras. Em 324,3s a frase final está legível; no último quadro já terminou.

Comparadas as seis fontes na prancha `midia/seis_fontes_inspecao.jpg`: ciclista/píer, Cheetah/fumaça, jato/cidade; praia/detector, carro azul/motos/murais, helicóptero/água/edifício lateral. Todas correspondem ao contexto narrado. Fotografias são a evidência central; não se exigem clipes genéricos neste episódio. GTA V é identificado como divulgação de 2012, com fonte 640×360 ampliada; a composição 4K não é alegada como detalhe nativo das fontes V.

Destaques progressivos da praia examinados em 65,5/69,5/74/77s: tomando sol, casal e detector aparecem na sequência e contornos apontam os elementos corretos. Carro/aerofólio/fumaça, motos/fios/viaduto e helicóptero/água também coerentes. Em 237,8s o prédio lateral permanece visível. Contornos, legendas e títulos não ocultam materialmente os detalhes analisados nas amostras.

Cartelas em 93,650/120,050/197,750/250,483/258,767/278,383/296,033s diferenciam interpretação, analogia e limites da comparação. Texto legível, sem promessa de benchmark ou tamanho mensurado do mapa. A repetição das seis fotos é motivada pela análise de composição.

## Técnica, legenda e áudio

Hash recalculado do master: `b286b951c08767d4266dd398b5872c5ac35b6b64b95a17adf1f7a82fb92a0665`.

QA existente conferida em `projeto/render4k/qa/validacao_final.json` e relatório executor: 3840×2160, H.264, 30fps, 9746 frames, vídeo 324,866667s, AAC 48kHz/324,84s; decodificação integral concluída sem erros. Não se repetiu a decodificação integral já suficiente. Correlação com WAV normalizado em 1/32/81/162/244/292/320s, mínimo 0,999968076, sustenta preservação/alinhamento técnico do sinal, não prova pronúncia ou interpretação.

Conferência própria do SRT: 132 blocos, exposição mínima 0,85s, nenhuma sobreposição; último bloco 321,940–324,540s. Conferência própria dos limites dos 47 planos: nenhuma lacuna ou sobreposição de frames. Nomes/acentos e leitura do texto no vídeo real coerentes nas amostras. Alguns pontos amostrados caem no fade de entrada/saída; isso não significa legenda ausente durante todo o bloco.

Loudness/pico final documentados: −16,92 LUFS/−1,23 dBTP. Pico 0,27dB acima do alvo inicial −1,5 dBTP, abaixo de 0; não configura por si só correção obrigatória. Não houve escuta subjetiva integral. Permanecem documentadas ambiguidades ASR em Cheetah (~129/205s), prédio (~236–238s) e início de Pensa numa (~245s); esta revisão não as declara resolvidas por áudio nem as transforma em erro comprovado.

SHA256 SRT recalculado: `4ddf76af1ed7434376c7f770a359d3f869f853ebb0e49b56dfff0b0a7e1725c0`.

## Capa e pacote

Capa vista a 320×180: OLHE AO REDOR legível, assunto reconhecível, identidade GTA V × GTA VI explícita, logo VI proporcional e sem conflito com texto. Montagem editorial informada no prompt e descrição; não se confunde com prova oficial dentro do vídeo. SHA256 JPG recalculado: `4a49eb28fda4e2462aa5fd4a9766613806c6d4ca0c4ff1a4a7e74ada88986185`.

Título, descrição, comentário e tags correspondem ao corpus de seis fotos e três pares. Capítulos 00:00/00:25/02:06/03:34/04:35/04:53 acompanham os inícios de seções reais (25,333/126,833/214,133/275,333/293,767s), sem diferença editorial relevante por arredondamento. Todos com mais de 10s e ordem crescente. As [regras oficiais de capítulos](https://support.google.com/youtube/answer/9884579?hl=pt-BR) e [miniaturas](https://support.google.com/youtube/answer/72431?hl=pt-BR) foram reabertas em 03/11/2026. A [biblioteca Rockstar VI](https://www.rockstargames.com/VI/media) foi reaberta; distingue screenshots e artwork. Não se alegou validar todo material novo da biblioteca. Fonte histórica Transport e limitação de extração da página estão explicitadas pelo executor, com JPGs oficiais identificados.

## Derivações sociais — revisão final concluída

A prévia estável `social/vertical_preview_4s.jpg` foi vista: quadro 16:9 inteiro, foto e títulos preservados; legenda ampliada na área livre e sem duplicação, rótulos/créditos existentes conservados. Legenda de 48px legível na redução exibida. A leitura de detalhes muito pequenos continua limitada pelo formato vertical e tamanho de tela, embora não haja recorte.

Correção documental solicitada foi concluída pelo executor: `social/PLANO_DISTRIBUICAO.md` agora usa 24,45s de áudio para Story, sem a referência anterior de 55,15s. Conferência própria por leitura do arquivo corrigido.

Após sinal explícito de arquivos fechados, foram recalculados os três hashes e consultados metadados diretamente por FFmpeg. Todos H.264 High, AAC LC 48kHz mono, 30fps, proporções sem distorção. Vídeos integrais: 324,866667s/9746 frames. Story: 24,466667s/734 frames, áudio cortado em 24,45s. As durações exatas e contagens foram conferidas no QA do executor; o FFmpeg independente confirmou resolução, fps, codecs e duração arredondada. A mensagem de FFmpeg “At least one output file must be specified” deriva de consulta de metadados sem saída, não indica falha de mídia.

| Arquivo | SHA256 recalculado |
|---|---|
| `social/L05_Facebook_1080p.mp4` | `e4dae61fecf5afd229f579f4808c96ab93695fcf2af780488d3fb956ba308e6e` |
| `social/L05_Instagram_integral_1080x1920.mp4` | `d23a2976db329ca90c15665135ddd29f16d43e526dba9c21960a765150e4189e` |
| `social/L05_Story_1080x1920.mp4` | `57367db3aaffd45e1f184c1a25bf4d9a2d987fd026335a26e11fe6b1b482b523` |

Inspeção visual independente dos finais incluiu as pranchas do executor (FB/IG em 0,5/4/18/82/172/267/319s; Story em 0,5/4/13/18/23,8s). Foram também extraídas e vistas amostras próprias adicionais diretamente dos arquivos finais na pasta temporária já identificada:

- Facebook: 4/136/237,8/324,833s, em `fb_review.jpg`.
- Instagram integral: 4/136/237,8/278/324,833s, em `ig_review.jpg`.
- Story: 0/0,5/23,8/24,433s, em `story_review.jpg`.

Facebook mantém composição/legendas do master em 1920×1080, sem recortes. Instagram conserva foto inteira, aerofólio/fumaça, helicóptero/água/edifício e cartela Não é um benchmark. Legenda ampliada está fora da evidência e permanece legível na redução para 432×768; faixa cobre somente o espaço reservado à legenda antiga. Créditos/rótulos e títulos laterais são menores por preservar o canvas completo; essa limitação foi aceita, sem esconder detalhes por sobreposição nas amostras. O fim dos integrais mantém a fotografia, sem preto ou congelamento inesperado identificado por estes pontos.

Story: em 0s já há foto e legenda O carro distrai.; em 23,8s aparece a última frase print numa disputa de console.; em 24,433s a frase já terminou e a foto permanece íntegra. O SRT termina essa frase em 24,30s e a próxima começa apenas em 25,32s. Corte coerente com o fechamento de gancho/escopo, sem entrada da próxima frase. Não se alega escuta subjetiva desse corte; preservação do sinal é sustentada pelas correlações técnicas e pelos limites temporais.

`DERIVACOES_QA.json` registra decodificação integral sem erros para os três MP4s. `QA_SOCIAL_AMOSTRAS.json` registra correlação de áudio contra o master em três janelas de 3s por arquivo: 1/160/319s nos integrais, mínimo 0,999344735; 1/11/20s no Story, mínimo 0,999258494. Resultados reutilizados sem repetir processamento suficiente, com hashes independentes coincidentes.

**Resultado global: PASS local dos cinco destinos**, estritamente para os hashes registrados. **Correções obrigatórias remanescentes: nenhuma.** A revisão não comprova aceitação, transcodificação, recortes de interface ou reprodução remota das plataformas; esses estados devem ser verificados após o envio pelo coordenador. Não houve upload/agendamento por este revisor, nem alteração de `producao.json`. Nenhum limite de ferramenta impediu esta conclusão.
