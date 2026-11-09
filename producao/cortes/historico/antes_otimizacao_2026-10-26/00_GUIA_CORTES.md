# Cortes C02–C12 — roteiros com entrega própria

Revisão editorial: 26/10/2026. Os onze arquivos `Cxx_NARRACAO.txt` preservam a fala limpa para edição e legendas. Os arquivos `Cxx_GEMINI.txt` trazem a mesma fala preparada para geração de áudio, com expressões pontuais compatíveis com a interface atual do Gemini. São versões autônomas reescritas a partir dos longos L02–L08, não intervalos já localizados em um vídeo. C01 pertence ao primeiro episódio e conserva seu material anterior.

## Geração da voz no Gemini

1. Selecione a voz personalizada do canal.
2. No campo **Style**, cole exatamente o conteúdo de `00_ESTILO_GEMINI_SHORTS.txt`.
3. No bloco de fala, cole somente o conteúdo do arquivo `Cxx_GEMINI.txt` desejado.
4. Gere cada corte separadamente para manter ritmo, consistência e facilidade de correção.
5. Escute principalmente nomes próprios, a primeira frase e a pergunta final antes de baixar o WAV.

Os comandos entre sinais de menor e maior são eventos locais, não texto para legenda. `<short pause>` cria uma pausa breve; `<chuckle>` aparece somente no C08, onde existe uma pequena virada de humor. Não adicionar várias expressões seguidas. Se a risada do C08 ficar artificial na voz personalizada, retirar apenas `<chuckle>` e gerar novamente.

O estilo global é propositalmente curto porque a identidade da voz já está salva no Voice Design. A direção pede português brasileiro, dicção clara, curiosidade investigativa e energia controlada, sem transformar o canal em locução de anúncio.

### Automação local

A integração direta está em `../../automacao/gemini_tts.py`, com os atalhos PowerShell documentados em `../../automacao/GEMINI_TTS_README.md`. O projeto usa por padrão o modelo `gemini-3.8-flash-tts` e a voz `voice_iagtq1gnk2br`. Os WAVs gerados são gravados em `audio_gemini/`. A chave permanece na variável de usuário `GEMINI_API_KEY` e não deve ser copiada para os roteiros ou arquivos do projeto.

## Roteiros e direção

| Corte | Título de trabalho e texto | Longo / evidência | Gancho e recompensa | Imagem e voz |
|---|---|---|---|---|
| C02 | [Jason e Lucia querem o mesmo futuro?](C02_NARRACAO.txt) | L02, fichas oficiais de Jason/Lucia | “Vida fácil” e “plano” abrem um contraste; o texto explica que desejos comuns podem envolver escolhas diferentes | Retratos identificados; mostrar “leitura do canal” quando entrar a hipótese. Curiosidade, sem suspense de traição |
| C03 | [O detalhe atrás de Jason e Lucia](C03_NARRACAO.txt) | L02, `Jason_and_Lucia_13.jpg` observado | Revela polícia no fundo já na segunda frase; explica intimidade versus perigo | Começar no casal e abrir o quadro para barcos/helicóptero. Descrever na voz para funcionar sem a tela |
| C04 | [De qual Vice City você sente saudade?](C04_NARRACAO.txt) | L03, lançamento 2002 / história 1986; `Real_Dimez_02.jpg` | Diferença entre duas datas leva a duas formas de nostalgia e ao contraste dos celulares | Cartela “lançamento / história”, seguida da plateia. Tom próximo, humor leve, sem prometer retorno de Tommy |
| C05 | [Tem gameplay no Trailer 2 de GTA 6?](C05_NARRACAO.txt) | L04, descrição oficial do Trailer 2 | Responde “tem” imediatamente; diferencia informação do conjunto e classificação dos planos | Texto resumido da descrição, rótulo Trailer 2. Não classificar uma sequência específica sem verificação |
| C06 | [Duas imagens oficiais, duas funções](C06_NARRACAO.txt) | L04, biblioteca e comparação artwork/screenshot | Duas categorias; o exemplo do zoom no pôster demonstra a consequência | `Jason_and_Lucia_01_landscape.jpg` da pasta Artwork e `Jason_and_Lucia_01.jpg` da pasta Screenshots. Rótulos persistentes |
| C07 | [GTA V e VI: olha o que tem ao redor do carro](C07_NARRACAO.txt) | L05, galeria Transport de 2012 e `Vice_City_09.jpg` | Carro → rua; comparação revela como o contexto muda o assunto | Cheetah com “GTA V — divulgação, 2012”; VI com “imagem oficial”. Mostrar quadro inteiro antes do detalhe; sem placar de gráficos |
| C08 | [A dona da rua nas Keys de GTA 6](C08_NARRACAO.txt) | L06, `Leonida_Keys_02.jpg` | Iguana no meio da rua; humor explica personalidade de lugar | Mostrar iguana e entorno, preservando pessoas. Um sorriso na voz basta; não inventar reação da IA do jogo |
| C09 | [A mesma água, dois climas de Leonida](C09_NARRACAO.txt) | L06, `Leonida_Keys_01.jpg` e `Grassrivers_03.jpg` | Horizonte aberto versus corredor de vegetação; preferência ao final | Comparar imagens inteiras com nomes. A sensação de exposição/ocultação é leitura autoral |
| C10 | [Sua playlist também tem locutor em GTA V](C10_NARRACAO.txt) | L07, suporte oficial da Self Radio, modo Radio, PC | Recurso verificável na abertura; explica a sensação de emissora | Diagrama músicas → DJ/anúncio; “GTA V — PC” visível. Não precisa tocar música comercial |
| C11 | [O aluguel de Jason tem uma contrapartida](C11_NARRACAO.txt) | L08, ficha Brian Heder | Moradia e cobranças aparecem nas primeiras frases; consequência é compromisso | Brian/Jason, gráfico “moradia ↔ serviços” e fonte. “Prisão” na pergunta final é metáfora sobre dependência, não evento do enredo |
| C12 | [Você confiaria num plano de Raul?](C12_NARRACAO.txt) | L08, ficha Raul Bautista | Experiência e risco crescente; distingue interesse de quem propõe e de quem executa | Raul identificado e contraste “prêmio / risco”. Exemplo não afirma equipe ou missão específica |

## Uso na produção

Começar com a primeira frase do TXT. Sem saudação, apresentação do canal ou pedido de inscrição antes da resposta. A pergunta de comentário já está ligada à entrega; não acrescentar três chamadas genéricas no final.

A referência inicial é uma locução de aproximadamente 30–45 segundos por corte a 140–155 palavras por minuto, com variação conforme as pausas. Isso é estimativa de texto, não duração medida. Medir ao gravar. Se passar de um minuto, revisar pausas e concisão; não mutilar a resposta para terminar com “veja no vídeo completo”.

Um corte não precisa reproduzir literalmente um trecho do longo. Ao extrair sem regravar, localizar e conferir se o segmento escolhido tem pergunta, contexto e conclusão próprios. Os textos desta pasta foram feitos para gravação separada; não há MP4 curto novo nesta entrega.

Para fontes exatas, arquivos visuais e contexto da apuração, usar as direções dos respectivos episódios: [L02](../L02/02_DIRECAO_E_FONTES.md), [L03](../L03/02_DIRECAO_E_FONTES.md), [L04](../L04/02_DIRECAO_E_FONTES.md), [L05](../L05/02_DIRECAO_E_FONTES.md), [L06](../L06/02_DIRECAO_E_FONTES.md), [L07](../L07/02_DIRECAO_E_FONTES.md), [L08](../L08/02_DIRECAO_E_FONTES.md). Manter na descrição as fontes realmente usadas, com a data da consulta.

## Alteração da pauta temporal

C12 substitui o antigo “GTA VI amanhã”. A nova versão funciona por seu conteúdo e pode ser publicada sem depender de contagem regressiva. Se a edição de publicação quiser usar “amanhã”, revalidar o calendário oficial no dia da postagem e ajustar texto/capa juntos. O plano preserva a posição na fila, sem agendar ou publicar automaticamente.

Os horários do calendário original continuam sendo planejamento. Não há evidência aqui de que as datas passadas tenham sido cumpridas.
