"""Copy-ready package for the revised C03; no network mutation."""
import json, shutil
from pathlib import Path
p=Path(__file__).resolve().parents[1]
t=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'))
out=p/'publicacao'
def put(name,text): (out/name).write_text(text.rstrip()+'\n',encoding='utf8')
for name in ['capa_master.png','capa_youtube.jpg']:
    shutil.copy2(p/'historico/v1_anterior_2026-10-29/publicacao'/name,out/name)
put('01_TITULO.txt','GTA 6: esse abraço tem polícia no fundo')
put('02_DESCRICAO.txt','''Um abraço, o sol entre os rostos… e polícia nas bordas.
O recorte muda o que você percebe na imagem de Jason e Lucia.

Nesta análise visual, abrimos o quadro para observar barcos, helicóptero e o contraste entre afeto e perigo. Isso não revela uma missão, uma traição ou a ordem das cenas. A comparação com a viagem e o guincho é hipotética.

Qual detalhe do fundo você viu primeiro?

Fonte das imagens: biblioteca oficial da Rockstar Games — https://www.rockstargames.com/VI/media
Imagem local: Jason_and_Lucia_13.jpg, preservada no acervo do projeto.
Imagens: Rockstar Games. Análise, gráficos e edição: Pixel Procurado.
Narração sintética: Gemini TTS. Capa: montagem editorial com arte-base gerada por IA; não é captura oficial.

#GTA6 #GTAVI #Shorts''')
put('03_COMENTARIO_FIXADO.txt','Você viu primeiro o casal, os barcos ou o helicóptero? O que mudou quando abriu o quadro?')
put('04_TAGS.txt','GTA 6, GTA VI, Grand Theft Auto VI, Jason e Lucia, Jason Duval, Lucia Caminos, detalhes GTA 6, Pixel Procurado')
put('05_TITULOS_ALTERNATIVOS.txt','A — GTA 6: esse abraço tem polícia no fundo\nB — O abraço de Jason e Lucia muda quando você abre a imagem\nC — Você reparou no fundo desta imagem de GTA 6?\n\nA é o recomendado; alternativas sem teste A/B realizado.')
markers=[(0,'O abraço e o fundo')]
for phrase,title in [('É como escolher','A foto da viagem'),('O detalhe interessante','Afeto e perigo no mesmo quadro')]:
    s=next(s for s in t['shots'] if s['anchor']==phrase)
    markers.append((s['start'],title))
put('06_TEMPOS_OPCIONAIS.txt','\n'.join(f'{int(a)//60:02}:{int(a)%60:02} {b}' for a,b in markers)+'\n\nMarcadores de consulta derivados da montagem final; descrição principal sem capítulos para este Short.')
media=[{k:s.get(k) for k in ['start','end','file','crop','ring','label','title']} for s in t['shots']]
put('07_CREDITOS_E_MIDIAS.json',json.dumps(media,ensure_ascii=False,indent=2))
put('07_CREDITOS_E_MIDIAS.md','''# Créditos e mídia

Imagem única analisada: videosGTAVI/GTAVI_Screenshots/People/Jason and Lucia/Jason_and_Lucia_13.jpg, 3840×2160. Inspeção direta confirmou casal, sol, barcos policiais e helicóptero. Origem: https://www.rockstargames.com/VI/media . O nome da pasta local não determina a categoria editorial.

Recortes, movimentos 2D, contornos amarelos e gráficos explicativos: Pixel Procurado. A comparação com foto de viagem e guincho usa gráficos próprios identificados como COMPARAÇÃO HIPOTÉTICA. Sem clipes genéricos, música ou áudio de trailer. A imagem inteira permanece visível durante a análise do entorno; contornos usam enquadramento fixo.

Capa reaproveitada após inspeção de coerência: montagem editorial gerada anteriormente, com texto e logo compostos separadamente. Arte-base e prompt preservados. Não se apresenta como screenshot oficial. Crédito não equivale a licença ou liberação de Content ID.
''')
put('00_GUIA_DE_PUBLICACAO.md',f'''# Publicação — C03 revisado

Preparado em 29/10/2026. Nenhum upload, agendamento ou alteração do Postiz foi executado nesta produção.

Título recomendado: GTA 6: esse abraço tem polícia no fundo

MP4: ../exportacoes/Pixel_Procurado_C03_Short_1080x1920.mp4 — {t['frames']/30:.3f}s, 1080×1920, 30 fps, H.264/AAC. Legendas incorporadas. SRT de acessibilidade: ../exportacoes/C03_legendas.srt; ativar o SRT também pode produzir duas camadas de legenda.

Capa: capa_youtube.jpg; master capa_master.png; arte e método em thumbnail_base_gerada.png e PROMPT_THUMBNAIL.txt. A capa existente continua fiel ao novo texto e foi preservada sem nova geração. Use os TXT numerados para título, descrição, comentário e tags. Os tempos opcionais vêm da timeline final.

No Studio, selecione Jogos, Grand Theft Auto VI se disponível e Português (Brasil). Sugestão editorial de público: não é conteúdo para crianças; avalie restrição etária separadamente. Playlist sugerida: Pixel Procurado — Shorts de GTA, somente se existir/criar por decisão do responsável. Não há patrocínio informado.

Envie inicialmente como Não listado e confira o processamento em 1080p, a abertura, a região central, o fim e a reprodução em celular. Depois, o responsável decide visibilidade e horário. Sem Analytics, não se presume horário ideal. Não há tela final desenhada; o fim conecta o “Porque...” ao gancho de abertura. Um vídeo relacionado pode ser escolhido somente se já estiver disponível e corresponder ao tema.

As regras oficiais foram consultadas em 29/10/2026:

- Miniatura personalizada de Shorts: Studio para computadores, com conta verificada; se a opção não estiver disponível, use a seleção de quadro oferecida na conta. [Ajuda](https://support.google.com/youtube/answer/72431?hl=pt-BR).
- Não são necessários capítulos nesta descrição. Em contexto compatível, capítulos manuais começam em 00:00, com pelo menos três marcações e duração mínima de dez segundos. [Ajuda](https://support.google.com/youtube/answer/9884579?hl=pt-BR).
- Tags ficam no campo próprio; sua contribuição costuma ser pequena fora de grafias alternativas. [Ajuda](https://support.google.com/youtube/answer/146402?hl=pt-BR).
- Tela final é um recurso distinto da montagem; a política geral prevê os últimos 5–20 segundos e mínimo de 25 segundos de vídeo. Não adicionar elementos que cubram o loop. [Ajuda](https://support.google.com/youtube/answer/6388789?hl=pt-BR).
- Avalie “Uso de IA” conforme o conteúdo real e a origem da voz personalizada. Representação realista de outra pessoa exige declaração; não presumimos que a voz seja clonagem da própria voz. A descrição já informa TTS e a capa sintética. [Ajuda](https://support.google.com/youtube/answer/14328491?hl=pt-BR).

Confira as verificações de direitos antes de publicar. Fixe o comentário somente após publicação e por decisão do responsável. Observe retenção inicial, duração média e quem assistiu versus deslizou; não há promessa de desempenho.

Reedição: timeline.json, DIRECAO.md e publicacao_revisada.py nesta pasta de projeto; direção executável em automacao/produzir_c03_revisado.py na raiz do projeto. Versão anterior integral em ../historico/v1_anterior_2026-10-29/.
''')
