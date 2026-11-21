# Como pedir o fluxo (copie, troque os links e envie)

## Prompt completo (cobertura com publicacao)

```
Use a skill pixel-procurado-live.

Lives para cobrir agora:
- https://www.twitch.tv/CANAL_1
- https://www.twitch.tv/CANAL_2   (opcional)

Quero o fluxo completo e automatico:
1. Grave as lives (aguarde entrar no ar) e ache sozinho os momentos virais de GTA VI.
2. Guarde so os melhores no acervo (videosGTAVI/_live) e apague o resto da gravacao.
3. Corte cada momento com no minimo 1 minuto, alinhado em pausa de fala.
4. Narre com a voz do canal os clipes com nota >= 75 (pode gastar TTS, no maximo 12 por live).
5. Monte vertical com legenda e credito, horizontal, story e capa.
6. Publique no Postiz (YouTube, Instagram, Facebook e TikTok) so o que passar no filtro de risco;
   a primeira publicacao de cada live fica retida ate eu criar o arquivo APROVADO.
7. Imagem/thumbnail: [Codex/Antigravity: gere automaticamente | Claude: so me entregue o prompt pronto de cada capa,
   eu gero em outro lugar e salvo no caminho indicado].
8. Me avise (notificacao do Windows) quando algo precisar de mim: aprovacao, clipe retido, imagem pendente,
   disco baixo, gravacao caida.

Nao poste nada com sinal de vazamento, spoiler grande ou cinematica isolada.
Depois de umas 3 horas de lives, monte o video longo de melhores momentos e me mostre antes de publicar.
```

## Variacoes curtas
- Só gravar e guardar (sem postar, sem narrar): `Use a skill pixel-procurado-live nesta live: <link>. So grave, escolha e guarde no acervo.`
- Empacotar sem publicar: `... Empacote os cortes e gere o plano do Postiz, mas nao publique nada.`
- Encerrar: `Pare as lives e me diga o que ficou no acervo, o que esta retido e o que aguarda aprovacao.`
- Liberar publicação: crie o arquivo vazio `videosGTAVI/_live/<AAAA-MM-DD>/<canal>/APROVADO` (ou diga "aprovado" e a skill cria).
- Marcar momento: `py -3.12 automacao/captura_live.py marcar --saida producao/live/<nome_da_live>`.
