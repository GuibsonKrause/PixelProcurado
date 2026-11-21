# Publicação no Facebook e Instagram

## Entrega de mídia pelo R2 — a partir de 06/11/2026

O painel e a API do Postiz usam `http://localhost:4007`. Para novos posts de
Instagram e Facebook, gerar os endereços de mídia pelo Worker e pelo bucket
R2 privado com `automacao/r2_media.py`. Em agendamentos, passar
`available_until` com pelo menos dois dias de margem após a publicação.
Para YouTube, usar os uploads locais do Postiz.

Os manifestos `postiz-r2-reparo-2026-11-06-*.json` em `.production-tools`
registram os IDs, horários e mídias da fila de 06 a 17/11 e dos reenvios de
04 e 05/11. Após as publicações, `py -3.12 automacao/reparar_fila_postiz_r2.py cleanup`
remove do R2 os arquivos cujos posts associados já estão `PUBLISHED` com link.

## Histórico do domínio fixo ngrok — ativado em 02/11/2026

Endereço utilizado na época: https://elephant-sprite-engulf.ngrok-free.dev

O domínio foi preservado ao recriar o container. Ele está explícito no
comando `--url` do compose. O container `postiz-ngrok` usa reinício
`unless-stopped` e não expõe sua API de inspeção em portas do Windows.

O Quick Tunnel desapareceu mesmo com o processo ativo. Reinício automático
não reserva um endereço trycloudflare. Foi preparada a alternativa ngrok
com o dev domain fixo vinculado à conta do usuário (sem domínio próprio).

No projeto Postiz, `docker-compose.ngrok.yaml` usa a rede existente, reinício
automático, imagem oficial fixada por digest e inspeção de conteúdo de
requisições desativada. `.env.ngrok.local` está ignorado pelo Git.
`overrides/salvar-ngrok-token.ps1` recebe o authtoken com entrada oculta;
não inicia o serviço nem modifica a origem do Postiz.

O authtoken foi salvo pelo usuário localmente, o compose foi ativado e as
três variáveis de origem do Postiz foram migradas. A política de privacidade
descreve o ngrok. Falta o usuário atualizar callbacks Meta/Google para o
domínio fixo. Não alterar chaves nem remover contas para atualizar URLs.
O plano gratuito tem cotas; domínio estável não significa disponibilidade
quando o computador/Docker estiverem desligados ou a cota for esgotada.

## Histórico da configuração temporária

O Postiz continua no computador, mas o login Meta em modo Ao vivo usa HTTPS.
O container `pixel-postiz-https` encaminha para `postiz:5000`. Cadastro público
de usuários está desativado (`DISABLE_REGISTRATION=true`).

O endereço vigente fica em `.production-tools/postiz-https.json` (ignorado).
O Quick Tunnel é temporário: recriar/reiniciar seu processo pode mudar o nome.
Não atualizar o domínio na Meta sem conferir o endereço atual nos logs.

Na Meta: cadastrar apenas o hostname em Domínios do aplicativo e as URLs
completas `/integrations/social/facebook` e `/integrations/social/instagram`
em Login do Facebook para Empresas > URIs de redirecionamento válidos.
Abrir o Postiz pela origem HTTPS antes de iniciar a conexão; o login local
e o login no novo domínio usam cookies diferentes.

`MAIN_URL`, `FRONTEND_URL` e `NEXT_PUBLIC_BACKEND_URL` no compose usam a origem
HTTPS. A API de automação local permanece acessível na porta 4007. O override
do YouTube aceita a origem atual e o endereço histórico exato
`http://localhost:4007` somente para uploads próprios, datados e aleatórios.
As verificações de origem, caminho e SSRF para outros endereços permanecem.
O teste `overrides/test-youtube-local.cjs` cobre ambas as origens.

Cloudflare passa a atuar como intermediário de tráfego, inclusive de
autenticação. A política publicada foi atualizada para descrever esse fluxo.
A declaração de provedores no painel Meta deve refletir esse uso.

## Retomada dos Shorts C01–C03

`producao/shorts/POSTIZ_META_ESTADO.json` registra tentativas e resultados;
`automacao/publicar_shorts_meta.py` prepara e publica com `type=now`.
Não usar seu comando publish às cegas após apagar e recriar conexões.

Em 01/11/2026, C01 foi confirmado no Instagram:
https://www.instagram.com/reel/DfM86OEuQUm/
C01/Facebook falhou pedindo reautenticação. C02 e C03/Instagram estavam em
processamento quando o usuário removeu as duas integrações no Postiz. Os
posts foram marcados como excluídos no banco. Conferir o feed remoto após
reconectar e reconciliar IDs antes de retomar, para evitar duplicações.
