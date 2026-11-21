# L05 — distribuição autorizada para 03/11/2026, 12h de Brasília

Estado: três derivações fechadas com QA técnico e amostragem visual do executor PASS; aguardam revisão independente. Nenhum upload ou agendamento executado por este fluxo.

| Destino | Arquivo | Configuração Postiz |
|---|---|---|
| YouTube | master 3840×2160 integral | youtube, public |
| Facebook feed | integral 1920×1080 | facebook, post_type=post |
| Instagram feed/Reel | integral 1080×1920, quadro 16:9 inteiro | instagram, post_type=post |
| Facebook Story | trecho inicial completo, 24,45s de áudio, 1080×1920 | facebook, post_type=story |
| Instagram Story | mesmo trecho | instagram, post_type=story |

As versões verticais preservam o quadro inteiro; painéis grafite com título amarelo e identidade do canal ocupam o espaço livre. Para leitura em celular, somente a faixa reservada à legenda original reduzida é coberta: a mesma SRT aparece em48px na área livre, sem duplicação. Fotos, gráficos e créditos permanecem completos. Não há recorte de praia, carro ou aeronave, nem nova fala sintetizada. O recorte Story termina em24,45s, após “print numa disputa de console.” no SRT final24,30s, encerrando descoberta e escopo antes da fala seguinte25,32s.

## Evidência técnica revalidada em 03/11/2026

`postiz integrations:settings` confirmou post_type=post/story nas duas integrações Meta. O texto resumido do schema Instagram fala “only one picture”; a implementação realmente executada em `/app/libraries/nestjs-libraries/src/integrations/social/instagram.provider.ts`, linhas733–772, aceita um MP4 e produz `video_url=...&media_type=STORIES`. Sua validação de mídia retorna true para vídeo Story sem áudio adicional da biblioteca. Portanto usamos um único MP4 por Story. O Facebook implementa `/video_stories` nas fases start/upload/finish, linhas583–725; o override ativo também contém esse fluxo.

Integrações habilitadas: Instagram `cmvzyw7vj0003pddwkgtivv8i`; Facebook `cmvzyur290001pddwolrt33em`; YouTube `cmvsctfgl0001jncj932ovibv`. Os schemas completos ficam em CAPACIDADES_POSTIZ.json após `discover`.

A [coleção oficial da Meta no Postman](https://www.postman.com/meta/instagram/folder/830j7my/reels-publishing) permite Reel de3s a15min, MP4 H264/AAC, 23–60fps e largura máxima1920px. O episódio de aproximadamente325s cabe no limite; a exportação proposta é30fps e1080px de largura. Consulta direta à referência developers.facebook.com retornou429, por isso a coleção oficial é a evidência legível. A aceitação remota de Stories só se comprova após processamento Meta. O corte deste episódio é24,45s de áudio, arredondado ao quadro seguinte a30fps no vídeo.

## Execução e prevenção de duplicação

Script: `automacao/distribuir_l05_postiz.py`. Padrão `plan`; `discover` só lê schemas; `derive` só processa localmente; `publish --coordinator-approved` envia e agenda os cinco destinos. Não executar publish antes de revisão final independente PASS.

O coordenador deve escrever `social/QA_FINAL.json` com `approved: true`, `source_sha256` do master, `thumbnail_sha256` de publicacao/capa_youtube.jpg e `assets` contendo SHA256 para cada chave de PLANO_CINCO_DESTINOS.json. Isso é uma liberação de QA da equipe, não um novo pedido de autorização ao usuário. O script confere todos os hashes e a data fixa antes de enviar qualquer mídia e antes de criar cada agendamento. Não altera automaticamente horário se12h já passou.

O estado persistente fica exclusivamente em `social/POSTIZ_ESTADO.json`. Cada destino tem assinatura de asset+payload, IDs de mídia e tentativa de criação gravada antes da chamada. Uma resposta ambígua interrompe a execução; exige reconciliação remota antes de repetir. A checagem de posts compara integração, conteúdo e post/story; feed e Story não se confundem. Mudanças de assinatura são bloqueadas. Mantém IDs e resultados para retomada sem duplicar.

O HTTPS de `.production-tools/postiz-https.json` é usado nas URLs Meta. Docker/ngrok precisam permanecer disponíveis enquanto Meta baixa e processa. Não são expostos tokens. Derivações recebem metadados, SHA256 e decodificação integral; inspeção visual/áudio permanece pendente até os arquivos existirem.
