# Revisao independente previa — ONLY IN DADE

Data: 2026-11-14. Revisor independente /root/revisao.

## Parecer

LIBERADO VISUALMENTE PARA RENDER 4K, condicionado somente ao saneamento da legenda cue 77 e verificacao do SRT/ASS e de um quadro composto afetado. Nao e aprovacao final de publicacao.

Pendencia textual: em 02:38,840–02:40,180 o SRT observado traz “No Extended Look, o que?”. O roteiro tem “No Extended Look,” seguido de “a Rockstar mostra...”. Remover “o que?” da legenda, sem inferir defeito de voz a partir do ASR. A escuta humana continua necessaria para validar a fala real.

## Evidencias inspecionadas

Leitura do roteiro mestre 00_ROTEIRO_COMPLETO.md, narracao limpa 01_NARRACAO.txt, configuracao de planos/rotulos, transcricao palavras_alinhadas.json e SRT exportado. Inspecao visual efetiva das sete folhas do pre-voo principal (62 planos), duas do Reel (20 planos) e uma do Story (4 planos). Foram vistos os quadros de fonte nas folhas, nao os clipes completos em reproducao.

Originais JAN/ESQ mostram os dois pontos de vista e a ordem dos carros descritos. Os pares de fotografias WCC/capturas sao coerentes com modelos e pinturas. Repeticoes sao retomadas comparativas justificadas. A narracao preserva em aberto o controle/celular; o card FUNCAO A CONFIRMAR reforca essa limitacao.

Sete folhas de amostras compostas vistas, oito quadros por folha (56 quadros):

- 0-16: gancho, imagem original vertical preservada dentro do horizontal, legenda legivel e cards Only in Dade/Vice City sem colisao.
- 42-50: alternancia correta GTA VI • CAPTURA / REPLICA REAL, com selo persistindo apos o card WCC desaparecer. Card SEIS CARROS acompanha a imagem do grupo.
- 82-89: fachada e curva coerentes; card A CAMERA NA ESQUINA presente e depois ausente, cena liberada.
- 191-197: retomada da pintura rosa e CTA sem card; enquadramentos e legendas legiveis.
- vertical: abertura em 1080x1920, legenda legivel sem corte lateral.
- 155-167: correcao P50/P51 confirmada visualmente. A camera traseira, minimapa e estrelas aparecem durante a explicacao. O salto do telhado indevido foi substituido.
- vertical-card: selo de captura/replica legivel, card WCC separado da legenda e selo continua apos o card desaparecer. Imagem horizontal contida sem cortar os carros.

## Correcao da primeira passagem

P1 resolvido nas imagens compostas: P50 final e P51 antes mostravam telhado/salto durante “camera atras do carro” (162,06–163,12) e “minimapa e estrelas de procurado na tela” (163,44–165,70). Fontes agora informadas como EXT 924–927,5 e 927,5–930,75 e coerentes com os quadros revisados.

## Limites e QA

Nao houve escuta real. Nao foi alegada reproducao integral nem inspecao continua de animacao quadro a quadro: as folhas demonstram presenca e desaparecimento dos cards, mas nao certificam sozinhas toda a curva de saida. QA tecnico dos primeiros cinco recortes foi lido: contagem de quadros coincide, zero intervalo preto, 30 fps, audio/video com duracoes coerentes, LUFS -17,0 a -16,5 e pico -1,5 a -1,4 dBFS. Os recortes corrigido e vertical-card foram informados pelo executor como QA exit 0. O render final ainda requer seu proprio QA e revisao dos artefatos atuais.

## Identificacao dos artefatos amostrados

Hashes abaixo identificam os arquivos existentes no momento deste registro; qualquer regeneracao muda a identidade e precisa ser registrada na passagem seguinte.

### 0-16

- `qa/amostras/0-16/exportacoes/Pixel_Procurado_Only_In_Dade_Previa_V2_amostra.mp4` — SHA256 `c8f49ae96defb3a874d680a9ccb29d3637cbb32ca5e6a296fac50d4cecb88a26`
- `qa/amostras/0-16/montagem/long_v2_qa_amostra.jpg` — SHA256 `1e19262632558430399a3fc3940d3e79e8b8e568c431cdbf9ef8025c4498fb5b`

### 42-50

- `qa/amostras/42-50/exportacoes/Pixel_Procurado_Only_In_Dade_Previa_V2_amostra.mp4` — SHA256 `9ac9114b63ea860b29e0ebabe515d4544f3e0901be0c0df08798f0f0ab5fd813`
- `qa/amostras/42-50/montagem/long_v2_qa_amostra.jpg` — SHA256 `987f437465682ddd8b1ea1f696cfc17ddc1497b0336368f65cef84487feeea75`

### 82-89

- `qa/amostras/82-89/exportacoes/Pixel_Procurado_Only_In_Dade_Previa_V2_amostra.mp4` — SHA256 `d1642fcf10ecf54a8f71b8382372337237201be3096d08ba6e70f32e359a3235`
- `qa/amostras/82-89/montagem/long_v2_qa_amostra.jpg` — SHA256 `0666f342a94fc35b28f2179cc7098b8e8eba973fe070e922efff9a429c83fc90`

### 191-197

- `qa/amostras/191-197/exportacoes/Pixel_Procurado_Only_In_Dade_Previa_V2_amostra.mp4` — SHA256 `9f6d11b04c9fc67865684d7c2a6641490318fde8100553dbfe9fccb82c64bfcc`
- `qa/amostras/191-197/montagem/long_v2_qa_amostra.jpg` — SHA256 `6314cef0958a907ee611344f1fa170a47ad1268f84b5921b141ef68df82f519e`

### vertical

- `qa/amostras/vertical/exportacoes/Pixel_Procurado_Only_In_Dade_Story_V2_amostra.mp4` — SHA256 `4b46076aae4a47e60c0b715479c282e635fe0881a630a9fce3d35fcbff2efce8`
- `qa/amostras/vertical/montagem/short_v2_qa_amostra.jpg` — SHA256 `dd80d381a6d2a04e17888a10252fbaf8d68152e76d2683f442d2b170af4b318c`

### 155-167

- `qa/amostras/155-167/exportacoes/Pixel_Procurado_Only_In_Dade_Previa_V2_amostra.mp4` — SHA256 `7374c6f179c4fac5592decb2f6e4e9eeda332f642d255f867ccc6e86f947a2af`
- `qa/amostras/155-167/montagem/long_v2_qa_amostra.jpg` — SHA256 `09e4b422634085881cac9d1f9a8e36b11a96ba4be91af3634d638681b30f325d`

### vertical-card

- `qa/amostras/vertical-card/exportacoes/Pixel_Procurado_Only_In_Dade_Vertical_V2_amostra.mp4` — SHA256 `18ff60fe77c082c798825c56e87736df50d780e295005221eb94bab0cd00fd72`
- `qa/amostras/vertical-card/montagem/short_v2_qa_amostra.jpg` — SHA256 `935658c0200112dd94cde1eeec7987379470ca7d9859fbd9baccf283ec6fd32c`

