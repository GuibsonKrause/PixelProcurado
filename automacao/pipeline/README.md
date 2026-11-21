# Pipeline V2 (genérico)

Um único conjunto de scripts para qualquer episódio. Só os **dados** mudam e ficam em `<episodio>/episodio.json`
(documentado em `episodio.schema.json`; exemplo real: `producao/L08/episodio.json`).
Baseado no padrão aprovado do L08. Sempre `py -3.12`, a partir da raiz do projeto.

## Novo episódio

1. Copie o modelo: `copy automacao\pipeline\episodio.modelo.json producao\L09\episodio.json` e preencha
   `id`, `formatos.*.stem/voz/alinhamento`, a lista `planos` (card + mídia do acervo + `corte` [início, fim] na narração),
   `correcoes_legenda` e a seção `publicacao` (textos, títulos, peças). Remova o formato que não existir.
2. Narração e alinhamento já prontos (Gemini TTS + faster-whisper, ver skills). Os `corte` devem ser contíguos e terminar na duração da voz.
3. Confira os insumos sem gravar nada:
   `py -3.12 automacao/pipeline/produzir_v2.py --episodio producao/L09 --dry-run`
   Depois rode o **pré-voo** (obrigatório antes de qualquer render; ~3 s por plano em fonte 4K):
   `py -3.12 automacao/pipeline/prevoo_v2.py --episodio producao/L09`
   Ele acusa ERRO para quadros pretos dentro da janela de cada plano, janela além do fim da fonte, timeline que não
   termina junto com a narração e mídia sem rótulo obrigatório (`"rotulos_obrigatorios": {"GTAV": "GTA V"}` no
   `episodio.json`; o selo persistente conta como cobertura e sai como INFO), AVISA trechos repetidos da mesma fonte e grava folhas de contato em `montagem/prevoo/`
   (3 quadros por plano ao lado do card). Olhe as folhas: é ali que se vê card que não bate com a imagem.
4. Amostra rápida (só os planos que cobrem o intervalo; sai em `<episodio>/amostra/`, nunca sobre os arquivos finais):
   `py -3.12 automacao/pipeline/produzir_v2.py --episodio producao/L09 --amostra 0-12`
   `py -3.12 automacao/pipeline/validar_v2.py --episodio producao/L09 --amostra 0-12`
5. Render final (`--formato longo|short|ambos`, padrão `ambos`; `--saida DIR` muda a pasta base):
   `py -3.12 automacao/pipeline/produzir_v2.py --episodio producao/L09`
6. QA técnico (blackdetect, LUFS/pico, decodificação integral, quadros/duração, folha de contato; grava `montagem/<stem>.qa.json`):
   `py -3.12 automacao/pipeline/validar_v2.py --episodio producao/L09`
7. Thumbnails e pacote de publicação seguem as skills próprias; depois confira o plano de distribuição (dry-run, não envia nada):
   `py -3.12 automacao/pipeline/distribuir_postiz.py --episodio producao/L09`
   Só com `--publicar` ele faz upload/stage no R2 e agenda no Postiz (`--data` sobrescreve a data).
   Peças já agendadas em `POSTIZ_ESTADO.json` são puladas. `--agora` publica já; `--so a,b` limita as peças;
   `--status [--limpar]` confere o estado real e limpa o R2 do que está `PUBLISHED`.
   O plano mostra o tamanho de cada mídia e marca `ACIMA DO LIMITE DA REDE` (vídeo do Instagram: 300 MB); o envio
   é barrado antes de começar. Vídeo de YouTube com 1 GB ou mais vai por URL do R2 (o upload local dá HTTP 413).
   Se uma peça ficar com tentativa registrada e sem `post_id`, o script se recusa a reenviar (evita duplicata):
   confira no Postiz e grave o ID, ou use `--reenviar` de propósito.

## Velocidade (sem mexer na qualidade)

- **Decodificação por GPU**: as fontes são decodificadas com `-hwaccel d3d11va` por padrão (quadros bit a bit idênticos aos da CPU,
  conferido por MD5; ~40% menos tempo por plano 4K num i7-1355U). Se falhar num plano, ele é repetido na CPU sozinho.
  `--hwaccel nenhum` desliga. Quick Sync (`qsv`) falhou nesta máquina; o encode continua em libx264.
- **Vertical + d3d11va**: o fundo desfocado (split -> boxblur) saía com metade verde chapada nos planos de vídeo; `produzir_v2.py` agora
  força `format=yuv420p` logo após o scale no ramo vertical (conferido por quadro; o QA não detecta esse defeito, então olhe um quadro de
  cada plano de vídeo vertical). Se aparecer de novo, use `--hwaccel nenhum` e apague os clipes em cache (`montagem/<stem>/NN.mp4`).
- **`"limite_mb"` no formato** (ex.: 300 no vertical integral do Instagram): os clipes saem em um único encode no bitrate que cabe
  (preset medium, crf 20 com teto VBV) e o render falha se o MP4 passar do limite. Substitui o reencode manual do arquivo grande.
  Ao ligar/desligar `limite_mb`, apague `montagem/<stem>/` (os clipes ficam em cache).
- **Revisão barata**: revisão independente primeiro nas folhas do pré-voo; vídeo só em `--amostra` dos trechos que precisam de
  movimento; segunda rodada só nos trechos alterados. **Um processo pesado por vez.**

## Notas

- Clipes por plano ficam em `montagem/<stem>/NN.mp4` e são reaproveitados; apague a pasta se mudar a direção de um plano.
- Painéis Hyperframes (`paineis_long|short.mov`) só são renderizados se ainda não existirem.
- Resolução: a geometria dos cards e legendas escala com a largura (4K = `[3840, 2160]` / `[2160, 3840]`),
  mas o `.mov` de painéis continua em 900x250 e é ampliado. Exportações 4K/vertical específicas por rede
  (matriz do `dia01_produzir.py`) não estão cobertas.
- `capa` é anexada no YouTube (`settings.thumbnail`) e no Instagram (`image[0].thumbnail`); o Facebook não tem rota de capa.

## TikTok no Postiz

Adicione o ID da integração em `publicacao.canais.tiktok` e a legenda em `publicacao.textos.tiktok_short`.
Exemplo de item em `publicacao.pecas`.

```json
{
  "chave": "tiktok_short",
  "rede": "tiktok",
  "tipo": "video",
  "midia": "producao/EPISODIO/exportacoes/Short.mp4",
  "texto": "tiktok_short",
  "titulo": "Título do vídeo",
  "tiktok": {"comment": true, "video_made_with_ai": true}
}
```

A peça usa um MP4, via R2, com `DIRECT_POST` e visibilidade `PUBLIC_TO_EVERYONE`.
O TikTok usa o texto da legenda como caption do vídeo.
`duet`, `stitch`, `comment`, `brand_content_toggle`, `brand_organic_toggle` e `video_made_with_ai` são booleanos opcionais,
com padrão `false`. Ative `video_made_with_ai` em peças com narração sintética realista. A publicação pública
também depende da auditoria do aplicativo pelo TikTok e das opções disponíveis para a conta.

## Opções por plano (em `planos[]`)

- `"card_posicao": [x, y]`: posiciona o canto superior esquerdo do painel V2 na geometria-base de 1920×1080 (horizontal)
  ou 1080×1920 (vertical). A posição escala pela largura de saída: em 4K horizontal, `[58,180]` vira `[116,360]`;
  em 4K vertical, `[150,190]` vira `[300,380]`. Esses exemplos deixam o painel no terço superior. Ausente, preserva
  as posições anteriores `[58,730]` / `[150,1060]`. A posição explícita deve manter o painel inteiro dentro do quadro;
  essa validação também acontece no dry-run. Use números finitos não negativos e confira rostos, fontes e legendas
  na amostra. Mudar essa posição exige invalidar só os clipes afetados; a arte dos painéis não muda.
- **Selo de rótulo** (automático): todo plano cuja `midia` esteja em `rotulos_obrigatorios` (ex.: `GTAV` -> "GTA V") recebe um
  selo pequeno no canto superior esquerdo (fundo escuro semitransparente, texto amarelo do canal) durante o plano INTEIRO,
  independente do card, que continua como está. Escala com a resolução (prévia, 1080p, 4K, vertical; no vertical fica sobre o canto
  do miolo 16:9). `"selo": false` desliga no plano.
- `"movimento": "fixo"`: em imagem estática, desliga o zoom/pan lento (ausente = comportamento antigo). Use quando o detalhe
  (HUD, botão, texto) não pode sair do quadro.
- `"enquadramento": "conter"`: mantém o quadro inteiro e centralizado, com o espaço livre em grafite. Uma fonte 9:16
  preenche a saída 9:16 e ganha laterais na saída 16:9. Em imagem estática, o quadro fica fixo.
- `"legenda_alta": true` (ou um número = MarginV em px da geometria-base): sobe a legenda naquele plano para não cobrir texto
  do material (ex.: "NOVEMBER 19, 2026" do último plano). `true` = 300 no horizontal; no vertical a legenda já fica abaixo do
  vídeo e `true` não muda nada (use número para forçar). A legenda que cai majoritariamente no plano é a que sobe.
- Clipes são cacheados em `montagem/<stem>/NN.mp4` com a legenda/selo já gravados: ao mexer em `selo`, `movimento`, `enquadramento` ou
  `legenda_alta`, apague os clipes dos planos afetados (ou use `--saida` novo).

## Falhas de render

`produzir_v2.py` sai com código diferente de zero se o FFmpeg falhar, se algum clipe estiver ausente/vazio, se um clipe não tiver
exatamente a contagem de quadros do plano ou se o MP4 final tiver contagem diferente da esperada (o `.mp4` final não é gerado).
