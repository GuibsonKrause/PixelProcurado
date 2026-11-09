# Voz do Pixel Procurado — pesquisa e direção

Preparado em 22/10/2026. Objetivo: criar no Gemini Voice Design uma voz masculina em português brasileiro adequada ao canal e aos vídeos longos. Esta é uma proposta editorial fundamentada em documentação e pesquisa; ainda não houve geração nem audição de uma voz Gemini nesta etapa.

## Recomendação pronta para usar

Nome sugerido para salvar: **Pixel Procurado — Investigador**.

No Voice Design, cole apenas o conteúdo de `01_DESCRICAO_VOICE_DESIGN.txt`:

> Voz masculina de aproximadamente 35 anos, de um falante nativo de português brasileiro com sotaque regional pouco marcado, timbre médio-grave natural, quente e limpo, e articulação clara e relaxada. A personalidade é a de um comentarista de games inteligente e acessível, com presença serena, curiosidade investigativa e humor sutil, que conversa com outro fã adulto de GTA e conecta as palavras com fluidez.

Se houver seletores separados, escolha português do Brasil (`pt-BR`) e masculino. Para a primeira avaliação, use Gemini 3.8 Flash TTS. A documentação posiciona esse modelo para maior fidelidade, interpretação e narração longa; isso não substitui ouvir o resultado específico. Fonte: [guia oficial de TTS](https://ai.google.dev/gemini-api/docs/speech-generation).

Depois de criar e salvar a voz, teste o roteiro com o campo de estilo vazio. Se precisar orientar a leitura, use somente o conteúdo de `02_ESTILO_NARRACAO.txt`:

> Conversacional, curioso e seguro, com energia moderada, frases fluidas e pausas guiadas pelo sentido.

O roteiro falado deve ficar no campo de texto; a descrição de voz e o estilo pertencem aos respectivos campos de configuração.

## Por que esse perfil corresponde ao canal

O planejamento local define o Pixel Procurado como investigador e explicador do universo de GTA, com público inicial hipotético de brasileiros adultos, curiosidade e humor moderado. O primeiro episódio deve separar anúncio, interpretação e pergunta aberta. A direção já pede um investigador curioso, próximo e seguro.

Referências locais: [plano do canal](../../../../PLANO_PIXELPROCURADO_2026-10-21.md), [direção do primeiro episódio](../../02_DIRECAO_E_CENAS.md) e [base de conhecimento](../../../../BASE_CONHECIMENTO_CANAL_DARK.md). Nessa base, “dark” se refere ao formato sem rosto.

| Escolha editorial | Função pretendida |
|---|---|
| Idade percebida próxima de 35 anos | Criar uma presença adulta e familiar para a proposta do canal. |
| Médio-grave natural, quente e limpo | Dar corpo à voz preservando clareza e flexibilidade de entonação. |
| Articulação clara e relaxada | Tornar explicações compreensíveis, com ligação fluida entre palavras. |
| Curiosidade investigativa e presença serena | Sustentar perguntas, apuração e distinções entre evidência e interpretação. |
| Humor sutil | Permitir leveza quando o próprio roteiro oferece espaço. |

Essas escolhas são direção artística. As fontes consultadas não demonstram uma idade, altura vocal ou velocidade universalmente ideal para retenção em canais brasileiros de GTA.

## O que a pesquisa mudou na descrição

**1. Duas frases para criar a identidade.** O Google recomenda descrições específicas e concisas de uma ou duas frases. Idade percebida, timbre, sotaque e personalidade habitual entram na criação; instruções momentâneas de atuação ficam separadas. Por isso, a descrição foi condensada. [Google — Voice Design](https://ai.google.dev/gemini-api/docs/voice-design).

**2. Pouca orientação durante a leitura.** O guia do Gemini 3.8 recomenda testar inicialmente sem estilo e reutilizar a voz salva. Identidades muito extensas repetidas a cada geração e ordens para manter o timbre podem aumentar a variação indesejada. A orientação de estilo proposta é deliberadamente curta. [Google Cloud — guia de prompting](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/text-to-speech/prompting-guide?hl=en).

**3. A duração da audição importa.** Um estudo do Google de 2019 comparou avaliação de frases e parágrafos e encontrou diferenças que nem sempre se correlacionavam. Isso apoia ouvir trechos longos, mas não estabelece uma voz ideal para o canal. [Clark e colaboradores — avaliação de TTS longo](https://research.google/pubs/evaluating-long-form-text-to-speech-comparing-the-ratings-of-sentences-and-paragraphs/).

**4. Qualidade tem várias dimensões.** Pesquisa de 2020 divulgada pela Mozilla avaliou 18 vozes sintéticas, três humanas e uma condição de texto. Nenhuma voz venceu todas as dimensões de avaliação. Clareza, compreensão e experiência de escuta devem ser consideradas juntas. É pesquisa anterior ao Gemini atual, usada aqui para orientar a avaliação. [Mozilla — Choice of Voices](https://www.mozillafoundation.org/en/research/library/choice-of-voices-a-large-scale-evaluation-of-text-to-speech-voice-quality-for-long-form-content/).

Não encontrei, nas fontes consultadas, comprovação de que escrever a descrição inteira em inglês produza melhor português. A recomendação específica do Google para inglês se refere às tags de áudio, como `<short pause>`, caso sejam usadas. O teste inicial dispensa tags e usa português.

## Audição prática antes de escolher

Este procedimento é uma proposta editorial de baixo esforço, não um protocolo científico validado.

1. Crie três candidatas com a mesma descrição. Identifique-as como A, B e C.
2. Gere o mesmo `03_TEXTO_AUDICAO.txt` com cada candidata, inicialmente sem estilo adicional. O arquivo contém dois parágrafos do roteiro existente, sem adaptações; não representa uma nova checagem dos fatos do episódio.
3. Ouça sem trilha, com volumes semelhantes, primeiro em fones e depois no alto-falante do celular.
4. Dê notas de 1 a 5 para português brasileiro natural, clareza das palavras, fluidez entre frases, adequação ao canal e conforto de escuta. Registre erros de nomes separadamente.
5. Com as duas melhores, gere o mesmo trecho contínuo de dois a três minutos do roteiro. Avalie se a leitura continua agradável, se as perguntas soam naturais e se a voz muda ao longo do trecho.
6. Na finalista, compare o estilo vazio com a orientação curta proposta. Mantenha o que soar mais natural.
7. Salve a voz escolhida e reutilize seu identificador nos próximos blocos e episódios. Registre modelo, descrição, estilo e nomes das amostras aprovadas.

A faixa de 140–155 palavras por minuto já prevista na direção do episódio serve como referência editorial. Não é uma garantia do modelo nem deve obrigar a acelerar uma leitura boa. Meça a duração do áudio gerado e priorize compreensão e ritmo do texto.

## Como ajustar um resultado insatisfatório

| Resultado ouvido | Próximo ajuste, um por vez |
|---|---|
| Grave exagerado ou voz pesada | Na criação, troque “médio-grave” por “registro médio, leve e claro” e gere nova candidata. |
| Leitura muito lenta | Mantenha a voz e teste estilo “Conversacional e curioso, com ritmo um pouco mais ágil”. |
| Leitura rígida | Mantenha a voz e teste “Como numa conversa espontânea, com articulação relaxada”. Confira também se as frases do roteiro são faláveis. |
| Excesso de entusiasmo | Mantenha a voz e teste “Calmo, curioso e contido”. |
| Nomes próprios incorretos | Corrija a pronúncia no trecho de síntese, preservando grafias oficiais na tela e nas legendas. Ouça novamente. |
| Mudança de identidade | Confirme que a mesma voz salva foi selecionada e reduza instruções adicionais. |

Evite acumular termos como “épico”, “ameaçador”, “extremamente grave”, “rouco” e “cinematográfico” no primeiro teste: eles conduzem a um personagem diferente da proposta conversacional. Também não acrescente hesitações, risos ou respirações em todas as frases para simular naturalidade.

A descrição final deverá ser aprovada pelo áudio gerado. Pesquisa ajuda a direcionar a criação; a escuta decide a voz do canal.
