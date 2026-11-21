# L03 — implementação e amostra de montagem

Escopo: amostra representativa antes do render integral. Projeto existente reaproveitado, sem gerar voz, imagem ou capa. A narração aprovada é `producao/L03/voz/narracao_normalizada.wav`, 330,68 s; SHA256 `700311CC62811827581F30CFF51B4070A5960B4875B7B0478339757746CD2636`.

## Método e retomada

- Timeline atual: 61 planos, 146 legendas, 9.921 frames, 330,7 s visuais. Último frame cobre a cauda integral da voz.
- Composição nativa 3840×2160, 30 fps, H.264 Quick Sync, `global_quality=19`, preset medium; AAC 48 kHz. Fontes do clássico 640×448 ampliadas dentro de cartão 10:7, sem recorte ou esticamento 16:9.
- Remotion `renderFrames` gera PNGs transparentes 4K para entrada de contornos, datas e itens; FFmpeg sustenta o último frame quando o gráfico termina de animar. Rádio 31 tem 170 frames reais de animação, preservando as três entradas vinculadas à fala.
- Um plano por vez. Depois da codificação, resolução e contagem de frames são conferidas antes de gravar assinatura e remover somente PNGs L03 regeneráveis daquela pasta. Registro em `render4k/limpeza_derivados.jsonl`. MP4s, fontes e entregas preservados.
- Cache por assinatura inclui fonte, plano, legendas, configuração e código do renderizador/overlays. Plano012 validado e reaproveitado. Não editar scripts assinados durante produção; mudança real invalida os segmentos afetados pela assinatura.
- Auditoria inicial: nenhum render L03 ativo; C: com 2,94 GB livres. Não houve limpeza de outros episódios ou arquivos externos. Render integral não iniciado nesta etapa.
- A legenda isolada `retorno:` já estava unida à pergunta anterior no arquivo atual. Relatório `inspecoes/validacao_timeline.json` foi atualizado sobre a timeline efetiva:146 blocos, zero menores que 0,85 s; conteúdo narrado preservado.

## Amostra e revisão

Índices: `0,1,12,15,16,31,39,40,41,42,43,44`. Cobrem abertura/telefone, clássico, duas datas, rádio com revelações e praia com quatro alvos e legenda superior esquerda. O salto entre os trechos é intencional na amostra; os tempos originais constam de `amostras/amostras.json`.

Entregas concluídas: `amostras/L03_AMOSTRA_4K.mp4`,12 MP4s individuais `amostras/plano_NNN_4K.mp4`, folha `render4k/qa/contato_amostra.jpg`, quadros individuais `render4k/qa/NNN_J.jpg`, relatório `render4k/qa/validacao_amostras.json` e SRT integral em `exportacoes/Pixel_Procurado_L03_4K.srt`.

Resultado medido: amostra unida de 49,366667 s, 1.481 frames, 3840×2160/30 fps, 14.963.689 bytes. As 12 amostras e o MP4 unido decodificaram inteiros sem erros; menor correlação AAC/WAV 0,999944936. Os 12 caches permaneceram válidos. Zero PNG temporário restante nos diretórios de overlays; 12 registros de incorporação/limpeza incluindo a execução anterior de 012. Integral continua pendente da revisão da amostra.

QA automatizado da amostra: resolução, frames, fps, H.264/AAC48k, decodificação integral de cada amostra e do MP4 unido, correlação AAC com o trecho exato do WAV aprovado. Quadros amostrados antes da entrada, no fim das animações/cues e no hold final. Essa verificação não equivale à escuta humana integral ou revisão estética de todos os frames.

Revisão visual efetiva dos quadros: abertura destaca o telefone esquerdo correto e preserva as artistas; cartão do clássico mantém a imagem 10:7 e seu logo; datas entram na ordem 2002→1986, mantendo 2002 visível; rádio revela Consumo→Aparência→Sucesso em momentos diferentes e mantém estado final. Na praia, conferidos casal, detector incluindo a bobina, pessoa tomando sol e banhistas à direita. Legenda superior esquerda preserva os quatro alvos e os rostos. Os gráficos e legendas dessas cenas não se sobrepõem.

## Comandos exatos — PowerShell na raiz GamePlay

```powershell
py -3.12 automacao/renderizar_l03.py --check
py -3.12 automacao/renderizar_l03.py --shots 0,1,12,15,16,31,39,40,41,42,43,44 --samples
py -3.12 automacao/verificar_l03.py --sample --shots 0,1,12,15,16,31,39,40,41,42,43,44
```

Depois da revisão da amostra, render completo sequencial com retomada e QA:

```powershell
py -3.12 automacao/renderizar_l03.py
py -3.12 automacao/verificar_l03.py
```

Se todos os segmentos estiverem prontos e apenas o mux precisar ser repetido:

```powershell
py -3.12 automacao/renderizar_l03.py --mux-only
py -3.12 automacao/verificar_l03.py --validate-only
```

Saída integral prevista: `producao/L03/exportacoes/Pixel_Procurado_L03_4K.mp4`; validação em `render4k/qa/validacao_final.json`. O comando integral exige espaço para segmentos restantes e arquivo final; não foi executado sem a revisão da amostra.
