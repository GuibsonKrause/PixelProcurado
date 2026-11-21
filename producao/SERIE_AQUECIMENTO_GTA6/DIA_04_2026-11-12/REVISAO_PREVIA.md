# Revisão visual independente — prévia DIA 04

## Terceira passagem — último ponto resolvido

**Conclusão vigente: LIBERADO PARA RENDER 4K.**

A correção por clipe foi confirmada diretamente nos PNGs exatos da amostra independente P52: `qa/teste_rotulo_p52/quadro_01.png` (n=0) e `quadro_02.png` (n=202). O texto GTA V está presente e legível no primeiro e no último quadro, sem kicker GTA VI. A única pendência da segunda passagem está encerrada; os quatro demais ajustes já estavam aprovados.

Amostra usada: `qa/teste_rotulo_p52/exportacoes/Pixel_Procurado_DIA04_Previa_V2_amostra.mp4`.
SHA-256 da amostra: `ac981b30768bab52af5f21dcb77067a754ca56e0e3552725d38b0e365e3c5df9`.
SHA-256 quadro n=0: `48af0439c321130efdf5db167a0a1d571af76cc0095dcc631a7273c004194c5e`.
SHA-256 quadro n=202: `31e033cd27410cee8c6a91c2020cc2d6fa4fd3d9b8422c35b7267856be187f76`.

Escopo desta liberação: autorizar o render 4K com o rótulo aplicado por clipe. Não é aprovação de publicação nem revisão final do master ainda não renderizado. Não houve escuta real nesta passagem. Conferir a identificação nos extremos de P52 novamente no master 4K e registrar hashes atuais na revisão final.

---

## Segunda passagem — prévia revisada

**Conclusão atual: CORRIGIR somente o primeiro quadro de P52 antes do 4K. Os outros quatro pontos estão resolvidos.**

Artefato: `_previa_revisada/exportacoes/Pixel_Procurado_DIA04_Previa_V2.mp4`.
SHA-256: `b9f8943bc3054ff71fd9a02e1b5f61f6ff44284350e8e9c3c0c444eaf1806465`.
A configuração usada está em `_previa/episodio.json`; a saída revisada foi separada para preservar o MP4 original.

Inspeção independente de 18 quadros direcionados no MP4 integral: primeiros/últimos quadros dos cinco planos GTA V, luta, Planet, R1 e data. Evidências: `qa/previa_revisada/revisada_01.jpg`, `revisada_02.jpg` e `manifesto.json`. A dúvida na entrada P52 foi resolvida por mais 12 quadros consecutivos: `gtav_borda_p52.jpg`.

| Ponto | Resultado da segunda passagem |
|---|---|
| GTA V | Identificação constante e sem kicker contraditório nos nove extremos verificados de P12–15 e no fim P52. **Resta um quadro sem etiqueta:** frame 5734, aproximadamente 191,133 s, é o primeiro quadro de golfe/GTA V e não tem o texto GTA V. Frame 5733 ainda mostra animais; a etiqueta só entra no frame 5735 (191,167 s). Corrigir a borda inicial P52. Impacto visual mínimo, mas descumpre a exigência explícita de identificar toda a duração. |
| Luta | Resolvido. O card 09:30 aparece em 80,800 s durante “nove e trinta” e continua legível em 81,400 s sobre o ringue. |
| PlanetLeonidaMan | Resolvido quanto à legenda: a narração foi separada do texto nativo. Nome do perfil e texto do post estão livres e legíveis no quadro de 125,000 s. Em 122,200 s o card ainda cobre parte do perfil, mas sua saída libera tempo de leitura; não considerado bloqueio restante. |
| Cachorro / R1 | Resolvido. O cão, o comando nativo STUDY R1 e o card estão visíveis em 266,900 s e 267,300 s, cobrindo a fala R um (266,860–267,180 s). |
| Segunda data | Resolvido. 19 DE NOVEMBRO está legível em 271,900 s durante “no dia dezenove” e continua em 272,400 s. |

Esta segunda passagem não incluiu escuta real e não reabriu os trechos já aprovados na primeira revisão. Após corrigir apenas a borda de P52, basta conferir os primeiros quadros desse plano no artefato que será usado como referência e registrar o novo hash; os demais quatro ajustes estão aprovados.

---

## Histórico — primeira passagem

**Conclusão: CORRIGIR antes de liberar o render 4K.**

Artefato revisado: `_previa/exportacoes/Pixel_Procurado_DIA04_Previa_V2.mp4`.
SHA-256: `853ba789c2901ebdbac2b30d1bef356b97fb12b1a2375d11606aa819edefd39c`.
Formato medido: 960×540, aproximadamente 30 fps, vídeo 315,499967 s, áudio 315,460 s.

Revisão independente por amostragem: 104 quadros reais decodificados por índice via PyAV, quatro por cada um dos 26 cards; seis folhas `qa/previa/cards_01.jpg` a `cards_06.jpg`, com índices/tempos em `manifesto_cards.json`. Também conferidos roteiro, palavras alinhadas, SRT real em `_previa/exportacoes/`, implementação de duração e animação de cards e folha geral. Não houve reprodução subjetiva integral nem escuta real do áudio: sincronismo abaixo é contra a transcrição alinhada. O QA técnico preexistente foi consultado, não reexecutado por este revisor.

## Ajustes obrigatórios

| Prioridade | Tempo no episódio / planos | Evidência e correção |
|---|---|---|
| P1 | 00:37,467–00:55,850; 03:11,100–03:17,867 — P12–15 e P52 | O card GTA V desaparece enquanto a mídia de GTA V continua. Ausência visível em 40,967; 43,533; 45,900; 48,467; 50,833; 53,400; 55,733; 194,500 e 197,767 s. Além disso, o pequeno kicker dos próprios cards diz GTA VI. Aplicar identificação GTA V constante do primeiro ao último quadro de cada plano, sem kicker contraditório. Folhas 01–03. |
| P2 | 01:19,150–01:20,400 — P23 | “09:30 / Luta no quintal” dura apenas 1,25 s; já não aparece em 80,300 s. A fala “nove e trinta” é 80,360–81,120 s. Preservar o vídeo curto da luta e carregar o card por pelo menos ~2,5 s, atravessando a imagem LUTA seguinte, com saída completa depois da âncora. Folha 03, linha 1. |
| P2 | 02:01,300–02:06,767 — P34 | A legenda branca da narração cruza o nome nativo PlanetLeonidaMan e o texto do post. O nome é justamente a evidência citada. Reposicionar a legenda deste plano ou o enquadramento para manter perfil e legenda separados. Folha 03, linha 2. |
| P2 | 04:23,667–04:27,733 — P73–74 | O cão e o comando STUDY [R1] são visíveis, mas a fonte e o card terminam em 265,700 s. A fala “cachorro” é 266,040–266,340 s e “R um” é 266,860–267,180 s; nesse momento já se está no plano seguinte. Manter a fonte do cachorro e o destaque até depois de 267,180 s, com pequena margem/saída. Folha 05, linha 2. |
| P2 | 04:27,733–04:32,767 — P75 | O segundo “19 DE NOVEMBRO” entra antes da pergunta e já sumiu em 270,267 s; “no dia dezenove” só ocorre em 271,560–272,220 s. Deslocar a entrada do card para perto de 270,8–271,5 s e garantir leitura/saída após a fala, atravessando o plano seguinte se necessário. Folha 05, linha 3. |

## Cobertura visual dos 26 cards

| Planos | Resultado observado |
|---|---|
| P01, P02 | Contagem e primeira data legíveis; a primeira data coincide com “dezenove de novembro”. Gancho começa diretamente e tem seis palavras no SRT. |
| P09 | Mulher de rosa e elevador realmente presentes; 09:40 coincide com a transcrição; quadro final livre de card. |
| P12–15, P52 | GTA V efetivamente usado; falha de identificação contínua descrita acima. P14–15 e início de P52 são imagens gerais do jogo, não demonstração literal de pedestre correndo ou atropelamento de coiote. |
| P17 | Intervalo 09:00–09:35 acompanha a referência narrada; aproximação da ponte no gameplay. |
| P19 | Pessoa de rosa no parapeito e salto efetivamente mostrados; número 09:00 correto. |
| P21 | Motel e mulher no pátio realmente presentes; 09:20 corresponde aos “vinte segundos depois”. |
| P23 | Ringue improvisado, golpe e espectadores visíveis; corrigir duração/sincronismo do card. |
| P34 | Post PlanetLeonidaMan, posto molhado e figura sem camisa visíveis; corrigir sobreposição. A imagem é estática, não demonstra toda a fuga em movimento. |
| P51 | Conteúdo de TV com animais visível e card “07:50 / TV dentro do jogo”. A composição ocupa o quadro com o conteúdo e não exibe a moldura do televisor; a origem como TV é informada pelo rótulo, não comprovada visualmente pela moldura. |
| P53 | Cenário hipotético corretamente rotulado “CENÁRIO IMAGINADO” na entrada; sem tratar o capotamento como evento mostrado. |
| P59 | Bar Effluvia e grupo de pessoas presentes; 10:10 correto. |
| P64, P65, P68 | Comparação 09:40/09:50, mulher no elevador e saída para a área aberta presentes. No P68 a porta já está aberta no primeiro quadro amostrado; não prova o movimento de abertura isoladamente, mas integra a sequência de saída. |
| P70 | Pergunta editorial “REAÇÃO OU ATUAÇÃO?” preserva caráter de dúvida. |
| P72 | Opções de conversa realmente visíveis no canto inferior direito; card não as encobre. |
| P73 | Cão e STUDY [R1] realmente presentes; corrigir permanência pela fala do comando. |
| P75 | Data correta, mas fora da âncora narrada; ajustar. |
| P78 | Hipótese rotulada “TESTE PROPOSTO”; não apresenta a cena como comprovação do teste. |
| P85, P86 | “Amanhã / 13 de novembro” e Lucia [L2] legíveis, com o comando Lucia visível na própria fonte. |

## Legibilidade, movimento e limites

- Legendas têm contraste e permanecem separadas dos cards nas amostras; exceção objetiva é o texto nativo do post PlanetLeonidaMan.
- Quadros iniciais mostram revelação do card e os últimos quadros amostrados mostram saída completa, sem painel residual. A animação GSAP possui saída por opacidade/máscara; esta análise por quadros não equivale a assistir cada transição em velocidade normal.
- O SRT acompanha as palavras alinhadas. Há diferenças textuais frente ao roteiro (“Dead e Redemption”, “se eu vou capotar”, entre outras); sem escuta real não classifico como erro de ASR nem recomendo sobrescrever a fala automaticamente.
- QA preexistente: 9465 quadros, nenhum intervalo preto detectado, −16,8 LUFS e pico informado −1,3 dBFS. Essas medidas não substituem escuta nem são atestado de pico verdadeiro por este revisor.
- Não foi feita avaliação de capa ou do master 4K. Após os ajustes, revisar apenas os trechos alterados na nova prévia e então decidir a liberação do 4K. Aprovação final continua dependente do master atual e dos hashes correspondentes.

As folhas foram regeneradas por PyAV para assegurar associação correta entre índice e imagem. Os arquivos `raw_*.jpg` de uma tentativa FFmpeg anterior não integram a evidência desta revisão e não devem ser usados.
