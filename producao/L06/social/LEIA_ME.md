# Distribuição do L06

O Postiz confirmou três canais ativos do Pixel Procurado em 4 de novembro de 2026. A matriz separa a íntegra, um corte original sobre iluminação urbana e as peças em fotos.

| Canal | Formatos | Peças |
| --- | --- | --- |
| YouTube | Vídeo longo e Short | Master 4K com thumbnail aprovada. Short vertical Vice City × Port Gellhorn. |
| Facebook | Vídeo integral/Reel, Story, publicação com quatro fotos | Cópia integral em 1080p, Story e cartões comparativos. |
| Instagram | Reel, Story e carrossel | Corte vertical, Story e cartões comparativos com texto alternativo. |

O Facebook disponibiliza os vídeos como Reels e o provedor Postiz usa o mesmo envio de vídeo para a íntegra. O histórico remoto mostrou C08 e C09 na fila. O corte novo acompanha o bloco de iluminação urbana e evita duplicar os dois cortes já programados.

O carrossel percorre três contrastes em seis locais. O Story usa uma arte vertical com a comparação entre Leonida Keys e Grassrivers. Os recortes e cartões usam material promocional da Rockstar Games e análise editorial do Pixel Procurado.

## Operação

- `py -3.12 automacao/distribuir_l06_postiz.py discover` consulta as integrações e o histórico.
- `py -3.12 automacao/cartoes_l06_social.py` renderiza e valida as imagens.
- `py -3.12 automacao/vertical_l06_social.py --bounds-only` identifica os limites do trecho a partir do SRT final.
- `py -3.12 automacao/vertical_l06_social.py` deriva o vertical e reposiciona as legendas. O recorte inferior usa a posição da legenda embutida. Os créditos por plano são repostos a partir da timeline.
- `py -3.12 automacao/distribuir_l06_postiz.py derive` gera a cópia de Facebook e valida os MP4.
- Após revisão e preenchimento de `QA_FINAL.json`, `py -3.12 automacao/distribuir_l06_postiz.py publish --coordinator-approved` cria os posts públicos. `--only` permite escolher chaves da matriz.
- `py -3.12 automacao/distribuir_l06_postiz.py status` reconcilia os IDs e consulta os estados e links retornados. O aceite do Postiz é separado da confirmação de publicação.

O estado local preserva os IDs e bloqueia o reenvio após uma tentativa ambígua. A automação consulta a disponibilidade HTTPS de cada mídia Meta usada, seguindo o fluxo do L05.

## Referências

- [YouTube Help — Shorts de até três minutos](https://support.google.com/youtube/answer/15424877)
- [Meta — fluxo unificado de publicação de vídeos](https://about.fb.com/news/2025/06/making-it-easier-create-videos-facebook/)
- [Postiz — implementação Facebook](https://github.com/gitroomhq/postiz-app/blob/main/libraries/nestjs-libraries/src/integrations/social/facebook.provider.ts)
- [Postiz — implementação Instagram](https://github.com/gitroomhq/postiz-app/blob/main/libraries/nestjs-libraries/src/integrations/social/instagram.provider.ts)
- [Rockstar Games — mídia oficial GTA VI](https://www.rockstargames.com/VI/media)

## Reel integral do Instagram

Em 4 de novembro de 2026, o episódio integral de 5min11s foi publicado separadamente do Reel curto. A primeira tentativa recebeu erro de download enquanto o ngrok devolvia HTTP 403 por cota mensal de tráfego. O retry foi reconciliado com o Postiz e usou uma cópia leve de 47,63 MB e um túnel temporário que serviu apenas aquele MP4. O túnel foi encerrado após a confirmação. [Reel integral](https://www.instagram.com/reel/DfVQOHwhDAQ/) · [Código do ngrok](https://ngrok.com/docs/errors/err_ngrok_725)
