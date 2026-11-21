# Produção DIA01 — execução após amostras

Os originais foram preservados. A voz final é `audio/narracao_final_hud.wav`,372.260s; alinhamento `audio/palavras_final_hud.json`,1150palavras. Três referências temporais e três nomes de botão foram corrigidos somente nas cópias de publicação. Registro em `AJUSTES_EDITORIAIS_PUBLICACAO_2026-11-10.md`.

## Renderização

O executor deve usar a timeline e o overlay existentes. Não repetir TTS, ASR integral, geração da arte-base ou Hyperframes. O master continua condicionado à aprovação das amostras e, antes de enviar, à revisão independente final.

```powershell
py -3.12 automacao/dia01_produzir.py render --name DIA01_Master_4K
py -3.12 automacao/dia01_produzir.py render --vertical --name DIA01_Instagram_Integral
py -3.12 automacao/dia01_cortes.py --render reel
py -3.12 automacao/dia01_cortes.py --render story
```

YouTube e Facebook recebem o mesmo master3840x2160,30fps,H.264/AAC48kHz. Instagram integral recebe1080x1920,30fps,vídeo18Mbps/max20Mbps e AAC128kbps. O corte Reel/Short tem62.6s; Story16.833s. Ambos usam somente falas existentes: primeira frase de leitura do HUD seguida de explicação pertinente. O início contém seis palavras em cerca de três segundos. São peças próprias, sem gerar uma nova locução.

## Direção e evidências

`montagem/timeline_dia01.json` contém31parágrafos ancorados no alinhamento final, janelas da fonte e pausas explícitas. Cada render salva `montagem/<nome>/ledger.json` com intervalos, fontes, frames e função das reprises. Não há loop automático de ação. O HUD retorna no gancho e no payoff; retornos ao combate analisam equipamento, arma recolhida e ângulos. As pausas são imagens genuínas com movimento2D discreto, não parallax3D.

O índice antigo rotula o keyframe anterior ao timestamp pedido. HUD rotulado6:10 temPTS364.9. A grade `carjack_350_a_380_cada2s.jpg` e o frame `referencia_seek_pyav370.png` confirmam a cena real. A narração mantém referência aproximada; nenhum frame é rotulado370exato como prova do HUD. O símbolo verdadeiro é círculo para Smash Window e triângulo para Slim Jim. `RECONCILIACAO_HUD.md` e `evidencia_hud_botoes.png` documentam a correção.

No parágrafo3,o HUD permanece visível até a frase que pede sua leitura terminar, aproximadamente24.1–30.1s do episódio. Os congelamentos dos parágrafos25,27e28 usam364.9. O vídeo identifica análise do gameplay; consequências não demonstradas do caminho Slim Jim são tratadas como interpretação editorial nos cards e na descrição.

## Publicação preparada

`publicacao/PACOTE_PUBLICACAO.json` e TXT01–06 contêm títulosA/B,descrição,fontes,capítulos,comentário e tags. Os capítulos vêm da voz final e devem ser confirmados contra o master. `thumbnail_A` e `thumbnail_B` usam a mesma arte-base editorial e identidade, com frases distintas. A versãoB deve participar do teste nativo no mesmo vídeo, sem segundo upload.

`social/carrossel_01.jpg` até04 são quatro slides1080x1350 com captura e HUD autênticos. `social/capa_vertical_hud.png` é a capa1080x1920 das peças sociais. Textos e fatointerpretação foram inspecionados visualmente. `PLANO_POSTIZ_DIA01.json` lista10destinos compatíveis, sem declarar upload ou capa anexada.

Executar QA técnico separado com `automacao/dia01_validar.py`,mantido pelo executor: metadados e duração do stream,decodificação integral,blackdetect,loudness/picos,correlaçãoAAC/WAV e contatos. A amostragem visual e a correlação não substituem escuta subjetiva integral nem revisão factual. A revisão independente final continua obrigatória antes do envio.
