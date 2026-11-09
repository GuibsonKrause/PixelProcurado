# Shorts — guia da revisão de retenção

Revisão: 26/10/2026. [Ler os 14 roteiros completos](01_ROTEIROS_OTIMIZADOS.md). [Diagnóstico individual](02_DIAGNOSTICO_RETENCAO.md).

C01–C12 são os doze cortes da grade principal. L01-R02 e L01-R03 são as duas reservas do primeiro episódio, distintas de C02/C03. Cada arquivo NARRACAO contém a fala limpa; cada GEMINI contém a mesma fala com expressões pontuais no padrão já usado pelo projeto. Usar `00_ESTILO_GEMINI_SHORTS.txt` no campo Style para a direção geral. Gerar um roteiro por vez com a voz do canal.

Os textos têm 203–220 palavras, aproximadamente 1min19s–1min25s a 155 palavras/minuto, antes da variação de pausas. Todos estão na faixa solicitada de 160–450 palavras. Os temas não exigem ocupar o teto. As 14 narrações foram geradas e validadas em 26/10/2026. Os WAVs brutos estão em `audio_gemini/`; as cópias normalizadas para edição estão em `audio_gemini/normalizados/`. Consultar `audio_gemini/RELATORIO_GERACAO.md` para durações, formato, métricas e pontos de escuta. Nenhum vídeo ou publicação foi gerado nesta etapa.

## Montagem e voz

Começar no gancho, sem vinheta. As aberturas têm 9–11 palavras; a frase inteira ocupa cerca de 3,5–4,3 segundos a 155 palavras/minuto. O conflito começa imediatamente: imagem e cartela curta devem apoiar sua compreensão nos três primeiros segundos.

Os parágrafos três a cinco mudam a direção da análise; o sexto entrega a conclusão e prepara o retorno. Mudar enquadramento ou introduzir uma evidência conforme a ideia muda. As viradas ocorrem aproximadamente a cada 40–47 palavras. Medir na gravação, sobretudo a primeira, perto dos 20 segundos.

O conectivo final é falado e continua na abertura durante o replay. Entregar a resposta antes dele; evitar tela de encerramento, silêncio ou fade. Retornar à composição visual inicial e ouvir a junção da última frase com a primeira. Reticências indicam continuação, não pausa dramática. Não acrescentar um CTA depois do loop.

Exemplos hipotéticos e interpretações continuam identificados na fala. A edição não deve transformar uma hipótese em spoiler, uma imagem em mecânica comprovada ou divulgação em teste de desempenho.

## Evidência e material visual

Usar as fontes e caminhos de imagens registrados nas direções de [L01](../L01/03_FONTES_E_CHECAGEM.md), [L02](../L02/02_DIRECAO_E_FONTES.md), [L03](../L03/02_DIRECAO_E_FONTES.md), [L04](../L04/02_DIRECAO_E_FONTES.md), [L05](../L05/02_DIRECAO_E_FONTES.md), [L06](../L06/02_DIRECAO_E_FONTES.md), [L07](../L07/02_DIRECAO_E_FONTES.md) e [L08](../L08/02_DIRECAO_E_FONTES.md). A revisão usa a apuração existente, sem uma nova checagem externa.

| Roteiro | Evidência e direção visual |
|---|---|
| C01 | Anúncio completo versus data isolada; captura de trailer versus anúncio de plataforma. Revalidar qualquer data exibida. |
| C02 | L02: fichas de Jason/Lucia e sinopse; exemplo de risco em gráfico identificado como hipótese. |
| C03 | L02: Jason_and_Lucia_13.jpg; comparar recorte do casal com imagem inteira. |
| C04 | L03: lançamento/ambientação identificados; Real_Dimez_02.jpg com celulares. |
| C05 | L04: descrição oficial do Trailer 2; não classificar planos sem evidência específica. |
| C06 | L04: artwork Jason_and_Lucia_01_landscape.jpg e screenshot Jason_and_Lucia_01.jpg, com categorias visíveis. |
| C07 | L05: Cheetah promocional de 2012 e Vice_City_09.jpg; comparação de enquadramento. |
| C08 | L06: Leonida_Keys_02.jpg; ocultação do animal é exercício imaginativo, não captura alternativa. |
| C09 | L06: Leonida_Keys_01.jpg e Grassrivers_03.jpg; sensações são interpretação. |
| C10 | L07: suporte da Self Radio, diagrama músicas/DJ/anúncios; rótulo GTA V — PC. |
| C11 | L08: ficha de Brian, Jason e gráfico moradia/serviços. |
| C12 | L08: perfil de Raul; gráfico capacidade/risco, sem inventar missão ou equipe. |
| L01-R02 | Sinopse; distinguir hipótese de informação divulgada na tela. |
| L01-R03 | Imagens de locais, sem desenhar fronteiras ou distâncias inventadas. |

Versões anteriores preservadas em `historico/antes_otimizacao_2026-10-26/`. Não usar essa pasta como entrada da produção. A automação existente está documentada em `../../automacao/GEMINI_TTS_README.md`. Datas da grade continuam sendo planejamento; não comprovam publicação. Manter os TXT, as cópias Gemini e o documento consolidado sincronizados em futuras revisões.

## Expressões nas versões Gemini

Cada roteiro recebeu quatro marcações `<short pause>` em contrastes, revelações ou conclusões. C02, C03, C04, C09, C11 e L01-R02 também têm uma `<breath>` numa mudança de ideia. Somente C08 tem `<chuckle>`, logo após revelar a iguana. São 4–5 eventos por roteiro; nenhum antes da abertura ou depois da ponte final.

As tags são indicações de interpretação, não texto para narrar ou legendar. Este padrão foi reaproveitado dos roteiros Gemini existentes no projeto; a resposta da voz ainda precisa ser ouvida. Se o riso soar artificial, retirar apenas `<chuckle>`. Evitar somar pausas longas aos parágrafos. Os tempos publicados continuam sendo estimativas da fala limpa: as expressões podem acrescentar duração. Conferir ritmo e junção do loop após gerar o áudio.

O atalho de todos os Shorts seleciona C01–C12. Para as reservas L01-R02 e L01-R03, fornecer seus arquivos GEMINI explicitamente à automação ou gerar pela interface. O lote de 26/10/2026 incluiu os 14 roteiros.
