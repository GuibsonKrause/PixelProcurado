# DIA10 — revisão independente parcial do pré-voo

**Estado: peças estáticas aprovadas; revisão da timeline pendente. Não libera render integral.**

Foram efetivamente abertas com view_image as folhas de 4 capas A/B (16:9 e 9:16), 4 slides e 12 cartelas (6 conteúdos horizontal/vertical). Hashes das três evidências constam em REVISAO_PREVOO.json. O revisor não planejou nem implementou essas peças.

Não há bloqueio nas peças vistas: textos sem cortes aparentes, contraste e leitura reduzida adequados, rostos livres nas capas, fundo sólido e fontes/ressalvas nas cartelas. Números de fuso, lançamento, pré-carregamento e condição digital Vintage concordam com o roteiro e FONTES canônico. Não se promete jogadores online, proteção total contra spoilers ou vantagem mecânica de veículo.

As folhas de pré-voo da timeline e episodio.json ainda não estavam disponíveis na consulta. A direção informou correção de assert P14 antes da geração. Portanto não foram conferidos planos, janelas reais, posição final do overlay, rótulos sobre imagens, legenda ou movimento. A revisão será retomada nesses artefatos, preservando a aprovação estática se os hashes não mudarem.

Áudio: **NÃO OUVIDO POR HUMANO**; nenhuma escuta feita por este revisor, conforme pedido. QA automático consultado:385,48s,48kHz PCM16 mono,18.503.040 samples,−16,3LUFS/−1,6dBTP; dois ASR sustentam os números/datas e registram incertezas de nomes/palavras. Isso não equivale a escuta ou validação de pronúncia.

Próxima rodada: folhas início/meio/fim + fala de todos os planos e formatos; confirmar fonte acima da legenda, rótulos, imagem x afirmação, janelas Launch antes do fade1:26 e ausência de extrapolação além89,1667s. Só depois amostras reais, com cobertura de abertura/encerramento/tipos de card e formatos verticais. REVISAO_FINAL não foi emitida e validar_revisao.py --modelo não foi executado.

## Rodada R01 — longo, planos01–69

Sete folhas com fala efetivamente vistas; cópias e hashes preservados em montagem/revisao_prevoo/r01. **Bloqueio D01:** apenas4s de vídeo nos69planos; cinco screenshots de cidade repetidos dominam o apoio. Repetições adjacentes em93,700–104,733s,128,267–136,667s e320,067–331,433s. Diretor aceitou substituir apoios por janelas oficiais contextualizadas; preservar cartelas, imagens literais de bônus e relógio mestre.

Sem bloqueio factual nas cartelas ou no bloco46–55(246,5–303,933s): fontes reais mostram Cheetah, Squalo, interior, Stanier, roupas/penteados e padrão de arma correspondentes. Launch81–85s no plano08 está dentro da fonte e seus três quadros vistos não atingem fade1:26. Rótulos declarados na configuração, ainda não vistos compostos.

**Limite:** as folhas não compõem card, legenda e selo sobre a imagem. Posições, oclusões e animação requerem amostras reais; não foram aprovadas por leitura de código. Verticais/derivados ainda pendentes.

**Alerta textual ASR:** plano54(292,867–298,400s) registra “Ter um carro num action demonstra...”, perdendo a negação do roteiro. Não prova erro na voz, que não foi ouvida; se esse texto entrar no SRT, porém, inverte o sentido. Alertado coordenador para tratamento conforme regras de legenda, sem correção silenciosa. Outras incertezas nos planos45/59/62 preservadas noJSON.
