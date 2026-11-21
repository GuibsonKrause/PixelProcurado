# DIA 10 — fontes oficiais e limites de afirmação

Consulta: 18/11/2026, madrugada, America/Sao_Paulo. Pesquisa restrita a documentação oficial; nenhuma fonte de rumor, vazamento ou gameplay antecipado. O horário editorial de publicação usado nas contas é 18/11/2026 às 18h de Brasília/São Paulo.

## Lançamento e pré-carregamento

- [Rockstar Support — horários regionais](https://support.rockstargames.com/articles/29jV3Cv2cCgvwM1XgtMO5o/grand-theft-auto-vi-regional-pre-load-and-release-times-on-playstation-5-and-xbox-series-x-or-s), atualização 03/11/2026, lido integralmente na consulta: lançamento em 19/11/2026 à meia-noite local, em ambas as plataformas PS5 e Xbox Series X|S. Pré-carregamento digital: PS5 em 10/11 à meia-noite local; Xbox em 10/11 à 0h GMT. Pré-carregar não significa desbloquear o jogo.

## Fusos: conta auditável

- [Governo da Nova Zelândia — datas do horário de verão](https://www.govt.nz/browse/recreation-and-the-environment/daylight-saving/?lang=en), atualização 11/08/2026: verão de 27/09/2026 a 04/04/2027.
- [Governo da Nova Zelândia — base legal dos fusos](https://www.govt.nz/browse/recreation-and-the-environment/daylight-saving/governing-legislation/), atualização 15/09/2021: padrão UTC+12; o verão acrescenta uma hora. Auckland está em UTC+13 em 19/11/2026. Não generalizar para Chatham, que possui diferença própria de 45 minutos.
- [Observatório Nacional — Hora Legal Brasileira](https://www.gov.br/observatorio/pt-br/assuntos/areas-de-atuacao/tempo-e-frequencia/brasil): tabela oficial dos estados, São Paulo no fuso UTC−3.
- [Presidência — Decreto 9.772/2019](https://legislacao.presidencia.gov.br/atos/?ano=2019&ato=eaaIzY65keZpWTb46&numero=9772&tipo=DEC): o resultado oficial indexado informa encerramento da hora de verão. A abertura integral deste endereço teve timeout nesta consulta; a conta usa as regras oficiais da Nova Zelândia e a tabela atual do Observatório. A tentativa Python zoneinfo não validou por ausência de tzdata; não foi instalada dependência.

Conta: (+13) − (−3) = 16 horas. `2026-11-19 00:00 Pacific/Auckland = 2026-11-18 11:00 UTC = 2026-11-18 08:00 America/Sao_Paulo`. Confirmado por Node `Intl.DateTimeFormat` com IANA/ICU: instante `2026-11-18T11:00:00Z` formatado em Auckland retornou `19/11/2026, 00:00:00 GMT+13`; em São Paulo, `18/11/2026, 08:00:00 GMT-3`. Às 18h brasileiras de 18/11, esse horário previsto da Nova Zelândia terá passado há 10h; faltarão 6h para a meia-noite de 19/11 no fuso de Brasília. Não dizer “faltam 24 horas exatas”. A conta de horário previsto não comprova servidores funcionais, jogadores efetivamente jogando nem circulação de spoilers reais.

Limite: o anúncio de meia-noite local não prova que trocar a região do console/conta funcione. Não oferecer tutorial nem promessa de acesso pela troca de região. O suporte de edições registra restrições regionais de resgate e recomenda compatibilidade entre compra e conta; isso é uma questão diferente da liberação temporal.

## Edições e bônus

- [Rockstar Support — plataformas, edições e versões](https://support.rockstargames.com/articles/4QfG4FmZCf5W1gS8jy4UVT/grand-theft-auto-vi-platform-editions-and-versions), atualização 04/11/2026, lido integralmente: existem Standard e Ultimate; o upgrade Ultimate pode ser adquirido separadamente. Vintage Vice City Pack é bônus de pré-compra/compra digital anterior a 20/11, em ambas as edições, com Stanier, roupas/penteados e padrão de arma. Ultimate possui seu conjunto próprio de extras. Não classificar Vintage como exclusivo Ultimate; a listagem indistinta da loja não serve para essa separação. A fonte descreve desbloqueio dos bônus Ultimate pela história, sem prometer todos os itens no primeiro minuto.
- [Loja oficial — GTA VI](https://store.rockstargames.com/game/buy-gta-vi): apoio visual/comercial; classificação de edições deve seguir o suporte acima. Não registrar preços sem consulta específica.

## Reduzir exposição a spoilers: ações reais, sem blindagem total

- [YouTube Help — recomendações e pesquisa](https://support.google.com/youtube/answer/6342839?hl=en), lido na consulta: menu junto ao vídeo permite “Não tenho interesse”/“Não recomendar canal”; pausar o histórico evita que novas visualizações/pesquisas alimentem experiências baseadas nesse histórico. São controles de recomendação, não um filtro universal de spoilers.
- [X Help — palavras silenciadas](https://help.x.com/en/using-x/advanced-x-mute-options), lido na consulta: silenciar palavras/expressões/hashtags com período e aplicação escolhidos; palavras também cobrem suas hashtags. A documentação ressalva que resultados de pesquisa continuam mostrando o conteúdo e notificações móveis ativadas para contas seguidas podem escapar. Não prometer análise de texto dentro de imagens/vídeos.

Recomendação editorial, explicitamente nossa: evitar buscas, comentários, títulos/miniaturas e DMs sobre a estreia; combinar termos “GTA VI”, “GTA 6”, “final” e “spoiler” conforme os controles disponíveis. Nenhuma dessas ações garante exposição zero. Se citar Instagram, verificar a documentação específica antes de dar caminho de menu; esta etapa não validou o Instagram.

## Acervo e comprovação visual

Fontes locais selecionadas: `videosGTAVI/GTAVI_Launch_Trailer.mp4`, `videosGTAVI/GTAVI_Ultimate_Edition_Benefits/` e `videosGTAVI/GTAVI_Vintage_Vice_City_Pack/`. Conteúdo visual é comprovado pelos quadros efetivamente extraídos e olhados em `montagem/referencias/RELATORIO_VISUAL.md`; nome de arquivo não substitui inspeção. As folhas e quadros são referências de trabalho, não novos materiais oficiais.

Não identificar pessoas por roupa, não chamar trailer de captura jogável, não extrair mecânica do que apenas parece ser ação cinematográfica. Cards de horários, pré-carregamento e protocolo antisspoiler são gráficos editoriais baseados nas fontes acima.
