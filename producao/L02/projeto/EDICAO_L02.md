# Pixel Procurado — Dossiê 02

**Jason e Lucia: eles querem a mesma vida?**

## Base da edição

Narração recebida: `C:/Users/guibson.krause/Downloads/Generated Audio October 25, 2026 - 11_37PM.wav`.
Duração medida: **309,76 segundos**. Toda a narração é preservada, na ordem original, com ajuste de volume em duas passagens. Não há cortes, aceleração ou nova voz.

O roteiro `../01_NARRACAO.txt` orienta o conteúdo. As palavras foram reconhecidas localmente com faster-whisper small e alinhadas ao texto do roteiro. `revisao_asr.json` registra as diferenças entre reconhecimento e roteiro; `../voz/palavras_alinhadas.json` guarda os tempos corrigidos. Essas verificações são por reconhecimento, texto e medição, não uma alegação de escuta subjetiva integral.

## Direção aplicada

- 76 planos, com cortes nas mudanças de ideia e intervalos medidos pela narração.
- 136 blocos de legenda, com alto contraste, tempo mínimo de leitura quando o próximo bloco permite e destaques seletivos em amarelo.
- 26 planos recebem animações produzidas quadro a quadro no Remotion em 3840 × 2160: títulos, entrada progressiva de perguntas, comparação risco/recompensa e traçado de destaques visuais.
- Fotos recebem aproximação, afastamento ou panorâmica sutis. Os movimentos são bidimensionais; não foi aplicado parallax com camadas inventadas.
- Os trailers e a apresentação estendida entram como imagens de apoio contextual, com áudio de origem silenciado.
- A análise da fotografia mantém `Jason_and_Lucia_13.jpg` na tela pelo tempo necessário. Os destaques acompanham a fala sobre casal, embarcações e helicóptero.
- O exemplo hipotético usa gráfico próprio, identificado na tela, sem sugerir que a oportunidade imaginada seja uma cena real do jogo.
- Identidade visual: grafite, branco e amarelo `#FFD33D`, marca discreta, créditos e referências curtas na tela.
- Narração em primeiro plano, sem trilha musical adicionada. A cor das fontes foi preservada; gradientes da composição ajudam a leitura do texto.

As fichas dos protagonistas e a sinopse foram reconsultadas em **26/10/2026**, horário de Brasília:

- https://www.rockstargames.com/VI/only-in-leonida
- https://www.rockstargames.com/VI

O catálogo local foi usado como índice, com inspeção das folhas de contato dos personagens e timecodes de vídeo. Foi respeitada a correção já identificada no roteiro: `Lucia_Caminos_06.jpg` mostra uma festa. A cena de prisão utilizada é `Lucia_Caminos_05.jpg`, além do trecho correspondente do Trailer 1.

## Arquivos e reprodução

- `edicao_l02.json`: linha do tempo com fontes, timecodes, duração de cada plano, intenção editorial, animações e legendas.
- `../../../automacao/preparar_l02.py`: preparação específica deste episódio.
- `../../../remotion/src/l02-overlays.tsx`: composição dos gráficos animados.
- `../../../remotion/render-l02-overlays.mjs`: renderização das sequências transparentes.
- `../../../automacao/renderizar_l02.py`: câmera, composição, legendas, codificação e junção.
- `../../../automacao/verificar_l02.py`: conferência de metadados, decodificação, contato visual, volume e alinhamento do áudio.

Na raiz do projeto, com o Python 3.12 instalado, a ordem é:

```powershell
& 'C:/Users/guibson.krause/AppData/Local/Programs/Python/Python312/python.exe' -X utf8 automacao/preparar_l02.py
Push-Location remotion
node render-l02-overlays.mjs
Pop-Location
& 'C:/Users/guibson.krause/AppData/Local/Programs/Python/Python312/python.exe' -X utf8 automacao/renderizar_l02.py
& 'C:/Users/guibson.krause/AppData/Local/Programs/Python/Python312/python.exe' -X utf8 automacao/verificar_l02.py
```

A renderização reutiliza apenas planos cujas entradas e assinatura correspondam à configuração atual. A concatenação registra a duração de cada plano explicitamente, evitando acúmulo de diferenças entre vídeo e áudio.

## Entrega e validação

Destino do vídeo: `../exportacoes/Pixel_Procurado_L02_4K.mp4`.
Legenda separada: `../exportacoes/Pixel_Procurado_L02_4K.srt`.
Formato: 3840 × 2160, 16:9, 30 fps, H.264, AAC a 48 kHz, com legenda incorporada e faststart.

O resultado final da verificação fica em `render4k/qa/validacao_final.json`. Sua existência com `full_decode_pass: true` confirma que o arquivo entregue foi decodificado integralmente sem erros e passou pelos testes registrados. A revisão estética é por amostragem; o contato final fica em `render4k/qa/contato_final.jpg`.

**Verificação concluída em 26/10/2026:** 3840 × 2160, 30 fps exatos, 9.293 frames, vídeo de 309,7667 s e áudio de 309,7600 s. Arquivo de 444.926.916 bytes. Decodificação integral sem erros e junção sem avisos de timestamps. Correlação entre narração normalizada e áudio exportado acima de 0,99996 nos dez trechos medidos, incluindo 306 s. Volume final −16,85 LUFS; pico verdadeiro −1,27 dBTP após AAC. As 801 palavras do roteiro estão cobertas pelas 136 legendas, sem sobreposição temporal entre blocos. Foram inspecionados 28 quadros distribuídos pela montagem, além das amostras de ajuste.

Este projeto não publica o vídeo nem altera o episódio 1.
