# L06 — revisão independente

Data: 04/11/2026. Resultado: **PASS**, no escopo visual, editorial, de legendas e das evidências técnicas descritas abaixo. **Correções obrigatórias: nenhuma identificada.**

Revisão realizada em contexto independente da produção. Não houve alteração do master, derivados, capa, textos, checkpoint ou aprovação operacional, nem upload/publicação por este revisor. O parecer se aplica somente aos arquivos e hashes abaixo.

## Artefatos e resultado

| Artefato | Resultado | Evidência |
| --- | --- | --- |
| Master 4K | PASS | 3840×2160, 30 fps, H.264/AAC, 310,833333 s; 9.325 frames; 12 quadros extraídos diretamente do MP4 final, além da folha de contato existente. |
| Legendas e timeline | PASS | 85 planos sem lacuna ou sobreposição na continuidade por frames; soma de 9.325 frames. 122 legendas, zero sobreposição e zero intervalo inválido; exposição mínima de 0,85 s. Última legenda encerra em 310,460 s. |
| Corte Vice City × Port Gellhorn | PASS | 1080×1920, 66,20 s, H.264/AAC. Seis quadros extraídos do arquivo final e inspecionados a 360×640; título, legendas reposicionadas e contexto visual legíveis, sem duplicação da legenda inferior do master nas amostras. |
| Facebook integral | PASS | 1920×1080, 310,83 s, H.264/AAC. Cinco quadros extraídos do MP4 final; começo, gráfico editorial, motel, caiaque e última fala preservados. |
| Capa YouTube | PASS | Arquivo de upload e miniatura de 320 px inspecionados. Texto “PARAÍSO DÁ MEDO?” legível; identidade do canal e logo presentes. A abertura entrega o contraste proposto. A descrição identifica a capa como ilustração gerada por IA. |
| Story | PASS | JPG vertical inspecionado: contraste Keys/Grassrivers, identificação dos locais, chamada e crédito legíveis e com margens. |
| Carrossel / quatro fotos | PASS | Os quatro JPGs foram abertos. Sequência 01–04, três comparações, nomes completos e créditos visíveis; títulos e legendas não cortados. |
| Descrição, capítulos e fontes | PASS | Descrição coerente com a análise de atmosfera; não promete mecânicas. Oito capítulos de 00:00 a 04:39 correspondem aos blocos da timeline. Créditos incluem Rockstar, edição, Gemini TTS e capa IA. |

## Inspeção visual executada

Quadros extraídos independentemente por FFmpeg, após confirmação de que cada arquivo estava fechado. Timecodes em segundos do próprio arquivo, ordem esquerda→direita e cima→baixo nas folhas temporárias:

- **Master:** 1,000; 12,000; 21,200; 68,000; 114,700; 133,000; 175,000; 214,000; 247,000; 265,000; 300,000; 310,000. Cobrem gancho, Keys/iguana, Grassrivers, os três títulos editoriais, Vice City/Ocean View, Port Gellhorn/Starlet Motel, Ambrosia, Kalaga/estrada/caiaque e encerramento. Legendas contrastadas e sem colisões relevantes nas amostras; nomes de lugares preservados. Os títulos “SENSAÇÃO DE ALERTA / Leitura das imagens” e a pergunta final aparecem sobre composição editorial própria identificada.
- **Vertical:** 0,200; 10,000; 21,000; 42,200; 55,000; 65,800. Preserva a evidência de Vice City e Port Gellhorn, as quadras urbanas e o panorama. O último quadro contém “não estamos avaliando um hotel de verdade.”, mantendo o limite interpretativo do trecho. A janela de imagem horizontal dentro do quadro vertical é uma escolha de composição; deixa os cenários reconhecíveis. Créditos miúdos têm leitura secundária, enquanto título e legenda permanecem legíveis na redução.
- **Facebook:** 1,000; 114,700; 175,000; 265,000; 310,000. Reprodução visual consistente com o master nas amostras; o quinto quadro é o encerramento, não uma tela preta. O bloco preto restante da folha de contato é apenas a sexta célula vazia do mosaico.
- **Folha existente:** `projeto/render4k/qa/contato_amostra.jpg`, com entradas/estados/finais dos planos 000, 003, 005, 011, 016, 029, 036, 046, 055, 062, 071, 075, 081 e 084, também foi inspecionada. A linha do plano 062 mostra material de trailer identificado como vídeo oficial, sem atribuir uma cena genérica a uma localidade específica.
- **Imagens estáticas:** `publicacao/capa_youtube.jpg`, `projeto/capa_miniatura_320.jpg`, `social/L06_Story_1080x1920.jpg` e `social/L06_Carrossel_01.jpg` a `04.jpg`.

As extrações de apoio estão em `%TEMP%/L06_revisao_independente/` (`master_sheet.jpg`, `vertical_sheet.jpg`, `facebook_sheet.jpg` e quadros individuais). São evidências temporárias reproduzíveis pelos timecodes acima; não integram o pacote de publicação.

## Evidência temporal e técnica

Recalculados nesta revisão: hashes dos arquivos, continuidade e soma dos frames da timeline, validade/sobreposição/duração mínima das legendas. Extração independente de 23 quadros dos três MP4s bem-sucedida.

Reaproveitados, sem repetir trabalho determinístico suficiente:

- `projeto/render4k/qa/validacao_final.json`: decodificação integral PASS; vídeo 310,833333 s e áudio 310,82 s; 4K30; AAC 48 kHz. Correlação com a **narração normalizada** entre 0,999963 e 0,999984 em sete pontos (1, 31, 78, 155, 233, 280 e 306 s).
- `social/VERTICAL_QA.json` e `social/DERIVACOES_QA.json`: decodificação integral PASS dos derivados e metadados compatíveis. Janela do corte: 131,695–197,890 s do master, abrangendo Vice City e Port Gellhorn com conclusão de frase.
- `social/CARTOES_QA.json`: identidade dos cinco JPGs conferida pelos hashes recalculados; os arquivos foram também inspecionados visualmente.

No relatório de loudness, `input_i=-16,85 LUFS` e `input_tp=-1,38 dBTP` descrevem a entrada analisada, isto é, o áudio do MP4. Os campos `output_*` são previsão da passagem de normalização usada na medição e não devem ser apresentados como nova medição do arquivo entregue. O pico de −1,38 dBTP está 0,12 dB acima do alvo inicial de −1,5 dBTP, sem evidência de clipping; não é correção impeditiva neste parecer.

## Fontes e textos

Foram lidos `publicacao/01_TITULO.txt`, `02_DESCRICAO.txt`, `05_CAPITULOS.txt`, `06_FONTES.txt`, a direção/fontes local e os textos de distribuição. As páginas oficiais [Only in Leonida](https://www.rockstargames.com/VI/only-in-leonida) e [Screenshots](https://www.rockstargames.com/VI/media/screenshots) responderam à consulta em 04/11/2026. A galeria apresenta capturas identificadas pelos lugares usados na edição. A revisão não transforma o crédito ou a presença no acervo em licença de uso, nem constitui auditoria jurídica.

Capítulos conferidos com os começos de bloco: Keys 35,68 s; Grassrivers 87,10 s; Vice City 131,72 s; Port Gellhorn 173,00 s; Ambrosia 211,15 s; Kalaga 245,65 s; síntese 279,22 s. Os tempos publicados são aproximações em segundos inteiros e preservam a entrada de cada assunto.

## Identidade dos arquivos revisados — SHA-256

| Arquivo | SHA-256 |
| --- | --- |
| `exportacoes/Pixel_Procurado_L06_4K.mp4` | `5dd1b491627948635b5f6b2702b4bdd20a14ef9b37340400209c9f58b6fe497b` |
| `social/L06_Vice_City_Port_Gellhorn_1080x1920.mp4` | `036cd23e5d26c7f08750e5f21cacd5cd621ef2feaaaf60ca6cbbc86379a58280` |
| `social/L06_Facebook_1080p.mp4` | `ef890ce07cbb5238a6169e20558340abbffb71780bceb0da93665ecce811b46b` |
| `publicacao/capa_youtube.jpg` | `7c36c450cdc3f4275ddab60f25325c61319af3c4b65c076a71a7cf96b2d23076` |
| `social/L06_Story_1080x1920.jpg` | `529b2a9b4609e96fa33afb27fe0475a05c6ca30388056f5cc62d22a9f2fba10b` |
| `social/L06_Carrossel_01.jpg` | `41ac9e34879ab70fc46c11ad88f0c71ccaff9d4d92e9cc54b8a0c68ebb7baadb` |
| `social/L06_Carrossel_02.jpg` | `d7f6b53ff85bf76258d0eeb0d96a15e5a5246cecc958b2895d237de5cc35933b` |
| `social/L06_Carrossel_03.jpg` | `f7aa71b188b2375c0cd093a8e7d34fbe61ac55a06d671b939764dbd82b5cb05f` |
| `social/L06_Carrossel_04.jpg` | `0d2dbe85fed3f20201dda7559ddc0420d2f48b3812bf2d5c3eec858b3fe86663` |

## Limites do parecer

- Inspeção visual **amostral**, não revisão quadro a quadro dos 5min11s nem reprodução contínua de todos os movimentos/transições.
- **Não houve escuta subjetiva do áudio** nesta revisão. Pronúncia, naturalidade e cortes perceptivos da locução não são aprovados por alegação de escuta. Correlação, ASR e metadados não substituem essa escuta.
- Decodificação integral e medições de áudio foram aceitas dos relatórios existentes vinculados aos arquivos por hashes; não foram reexecutadas pelo revisor.
- Não houve teste pós-compressão nos apps sociais, nem certificação de todas as sobreposições possíveis da interface de cada plataforma.
- O parecer libera os artefatos revisados no escopo acima. Autorização e execução de publicação, confirmação dos IDs/links remotos e eventuais critérios operacionais pertencem ao coordenador.
