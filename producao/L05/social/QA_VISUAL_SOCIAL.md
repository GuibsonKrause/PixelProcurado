# QA das derivações sociais — 03/11/2026

Resultado do executor: PASS técnico e amostragem visual. Os três MP4s estão fechados e estáveis. Revisão independente e liberação de publicação ficam com o coordenador. Nenhum upload/agendamento foi executado por este fluxo.

| Arquivo | Resolução | Duração real de vídeo | Frames / fps | Bytes |
|---|---|---|---|---|
| L05_Facebook_1080p.mp4 | 1920×1080 | 324,866667s | 9746 / 30 | 21.263.680 |
| L05_Instagram_integral_1080x1920.mp4 | 1080×1920 | 324,866667s | 9746 / 30 | 14.611.122 |
| L05_Story_1080x1920.mp4 | 1080×1920 | 24,466667s | 734 / 30 | 1.304.868 |

Todos H264/AAC, decodificados integralmente sem erro pelo FFmpeg. Streams integrais têm exatamente o mesmo número de frames do master. Story contém áudio até24,45s e o vídeo arredonda ao quadro seguinte; encerra depois de “print numa disputa de console.”, cuja legenda termina24,30s, antes da próxima fala25,32s.

Inspeção real das folhas facebook_feed_CONTATO.jpg, instagram_feed_CONTATO.jpg e facebook_story_CONTATO.jpg, mais prévia vertical540×960 e frame Story4s. Longos amostrados em0,5/4/18/82/172/267/319s. Story em0,5/4/13/18/23,8s. Fotos, painéis, títulos, marcas e créditos preservados, sem recorte do canvas de imagem. Legenda vertical original pequena coberta somente na sua faixa e substituída pela mesma SRT em48px, área livre, sem duplicação observada. Foi verificada leitura em redução; títulos laterais explicativos ficam menores por preservar o quadro inteiro.

Áudio comparado ao master em3janelas de3s por arquivo: correlação mínima0,999344 nos integrais e0,999258 no Story. Isso indica preservação/alinhamento do sinal após AAC; não substitui escuta subjetiva integral. Nenhuma nova fala ou síntese foi produzida.

Hashes, assinaturas de cache e decodificação: DERIVACOES_QA.json. Tempos de streams, amostras e correlações: QA_SOCIAL_AMOSTRAS.json. Master conferido antes e depois das derivações: b286b951c08767d4266dd398b5872c5ac35b6b64b95a17adf1f7a82fb92a0665.
