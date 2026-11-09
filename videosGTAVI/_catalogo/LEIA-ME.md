# Catálogo de mídia de GTA VI

Varredura concluída em 23 de outubro de 2026.

## O que foi catalogado

- 309 arquivos: 295 imagens JPG e 14 vídeos MP4.
- Aproximadamente 16,32 GB.
- Cada arquivo recebeu um ID estável, metadados técnicos e recomendação de uso.
- Todos os vídeos principais têm folhas de contato; os quatro vídeos longos também têm índices visuais por tempo.

## Por onde começar

1. Abra `GUIA_EDITORIAL.md` para escolher a fonte certa por assunto.
2. Abra `INDICE_VIDEOS.md` para localizar cenas e timecodes.
3. Consulte `GUIA_IMAGENS.md` para escolher screenshots e formatos de arte.
4. Use `inventario_midia.csv` para pesquisar, filtrar e automatizar a montagem.
5. Veja as miniaturas em `folhas_imagens`, `folhas_videos` e `indices_detalhados` antes de abrir arquivos de vários gigabytes.

## Arquivos gerados

| Arquivo/pasta | Função |
|---|---|
| `inventario_midia.csv` | Uma linha para cada um dos 309 arquivos; ideal para Excel, scripts e filtros. |
| `inventario_midia.json` | O mesmo inventário em formato adequado a Remotion, Python e outras automações. |
| `GALERIA.html` | Catálogo visual pesquisável com todos os 309 arquivos e filtros. |
| `GUIA_EDITORIAL.md` | Regras práticas e mapa de uso do acervo. |
| `INDICE_VIDEOS.md` | Timecodes dos trailers e do vídeo de 26:48. |
| `GUIA_IMAGENS.md` | Descrição visual dos screenshots e uso dos formatos. |
| `folhas_imagens/` | 42 painéis de miniaturas agrupados por personagem, região ou pacote. |
| `folhas_videos/` | 14 painéis gerais, um para cada vídeo. |
| `indices_detalhados/` | Quadros com timecode a cada 5 ou 10 segundos para os vídeos principais. |

## Campos do inventário

`id`, `relative_path`, `file_name`, `media_type`, `category`, `subject`, `variant`, `width`, `height`, `orientation`, `duration_seconds`, `fps`, `video_codec`, `audio_codec`, `size_bytes`, `fingerprint` e `recommended_use`.

O `relative_path` é a chave que deve ser usada na automação. Ele permanece válido enquanto a estrutura interna de `videosGTAVI` não for alterada.

## Regras editoriais

- Identifique material de GTA V quando ele aparecer. O arquivo `GTA-B02...mp4` não é GTA VI.
- Artwork e wallpaper servem para capa, cartela e apoio visual. Não os apresente como captura de gameplay.
- Screenshot oficial comprova apenas o que está visível no quadro. Não conclua tamanho do mapa, mecânica ou desfecho narrativo a partir de uma imagem.
- Benefícios da Ultimate Edition e do Vintage Vice City Pack devem ser identificados como conteúdo de edição/pacote. Não os atribua automaticamente ao jogo base.
- Na montagem narrada, deixe o áudio original dos trailers mudo ou muito baixo, salvo quando a fala ou o efeito do trecho for analisado diretamente.
- Para evitar repetição, alterne vídeo, screenshot com movimento de câmera e artwork. Em vídeo longo, use preferencialmente arquivos `landscape` ou `ultrawide`.

## Recriar o catálogo

Os scripts estão em `../../automacao/`:

- `catalogar_midias_gta.py`: recria CSV, JSON e folhas de contato.
- `indexar_videos_gta.py`: recria os índices detalhados dos vídeos principais.
- `gerar_galeria_gta.py`: recria a galeria HTML a partir do JSON.

