# L06 — Leonida além de Vice City

A edição parte dos 22 parágrafos de [01_NARRACAO.txt](../01_NARRACAO.txt). A [timeline](edicao_l06.json) tem âncoras por palavra, limites em frames, pontos de entrada de mídia, créditos de cada plano e as legendas. As fontes estão na raiz do projeto.

As imagens oficiais correspondem aos detalhes citados, incluindo Leonida Keys 01 e 02, Grassrivers 03, Vice City 06, Port Gellhorn 01, Ambrosia 06 e Mount Kalaga National Park 06. A iguana, a viatura, o letreiro e o caiaque têm tempo de leitura na captura em que aparecem. Clipes em movimento vêm dos trailers e de An Extended Look, sem áudio de origem. A montagem identifica as capturas, os clipes oficiais e as cartelas editoriais. A sequência segue as comparações da locução e não estabelece um trajeto ou mapa.

Vídeo em 3840 × 2160 a 30 fps com legendas incorporadas e SRT. As fotografias têm movimento 2D. As cartelas animadas foram compostas no Remotion e integradas ao vídeo pelo FFmpeg. Créditos fixos e legendas dos demais planos foram desenhados na exportação. Alguns clipes oficiais têm barras do enquadramento original ou resolução nativa diferente do master.

## Reproduzir a edição

Use Python 3.12 com os módulos audiovisuais locais. A partir da raiz do projeto:

```powershell
py -3.12 automacao/preparar_l06.py
py -3.12 automacao/renderizar_l06.py
py -3.12 automacao/verificar_l06.py
py -3.12 automacao/pacote_l06.py
```

O [mapa de planos](mapa_de_planos.txt) define as âncoras e as escolhas editoriais. O script de preparação converte as entradas para frames a partir da [locução alinhada](../voz/palavras_alinhadas.json). A normalização tem referência −16 LUFS e pico verdadeiro −1,5 dBTP. O [relatório de retomadas](../voz/revisao_retomadas.json) registra as escolhas feitas com ASR e a locução bruta original permanece na pasta de voz.

## Fontes

- [Rockstar Games, GTA VI e vídeos oficiais](https://www.rockstargames.com/VI)
- [Rockstar Games, galeria de capturas](https://www.rockstargames.com/VI/media/screenshots)
- [Rockstar Games, Only in Leonida](https://www.rockstargames.com/VI/only-in-leonida)

As pranchas de inspeção em `../midia/` documentam quadros dos vídeos por segundo. A validação técnica fica em `render4k/qa/`. A revisão visual examina amostras identificadas e a conferência de voz usa ASR e medições.
