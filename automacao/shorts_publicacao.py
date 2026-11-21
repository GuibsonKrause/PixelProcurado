"""Copy-ready publication packages based on the actual vertical timelines."""
import csv,json,math
from shorts_editorial import ROOT,PLANS,META

BASE=ROOT/'producao/shorts'
ROCK='https://www.rockstargames.com/VI'
MEDIA=ROCK+'/media'
PROFILES=ROCK+'/only-in-leonida'
T2='https://www.youtube.com/watch?v=VQRLujxTm3c'
RADIO='https://support.rockstargames.com/articles/5L6IP5RzI8kQXyXCddPO2Z/how-to-play-custom-music-on-the-self-radio-station-in-gtav-and-gta-online-on-pc'
VICE='https://www.rockstargames.com/games/vicecity'
TRANSPORT='https://www.rockstargames.com/newswire/article/89k8a5545o2k8k/transport.html'
SOURCES={
 'C01':[('Página oficial: anúncios e plataformas',ROCK)],
 'C02':[('Perfis de Jason e Lucia',PROFILES),('Premissa do Trailer 2',ROCK+'/trailer-2')],
 'C03':[('Biblioteca oficial: Jason and Lucia, imagem 13',MEDIA)],
 'C04':[('Vice City clássico',VICE),('Lançamento original: Take-Two', 'https://ir.take2games.com/static-files/fbf04d7a-8b78-4537-beca-2ea45ddb590d'),('Vice City em 1986: arquivo de rádio','https://www.rockstargames.com/newswire/article/51974aa3858ak3/advertising-council-site-updated-with-classic-radio-ads-from-pet.html')],
 'C05':[('Trailer 2: canal oficial',T2),('Comunicado da Rockstar de 07/05/2025','https://x.com/rockstargames/status/1920181314092765494')],
 'C06':[('Biblioteca: Screenshots e Artwork & Wallpapers',MEDIA)],
 'C07':[('Transport: divulgação histórica de GTA V em 2012',TRANSPORT),('Screenshot de Vice City em GTA VI',MEDIA)],
 'C08':[('Leonida Keys: imagem 02 da biblioteca oficial',MEDIA)],
 'C09':[('Leonida Keys e Grassrivers: biblioteca oficial',MEDIA)],
 'C10':[('Self Radio no PC: suporte oficial',RADIO)],
 'C11':[('Perfil de Brian Heder',PROFILES)],
 'C12':[('Perfil de Raul Bautista',PROFILES)],
 'L01-R02':[('Premissa oficial do Trailer 2',ROCK+'/trailer-2')],
 'L01-R03':[('Lugares de Leonida',PROFILES),('Biblioteca oficial de mídia',MEDIA)]}
ALTS={
 'C01':['GTA 6: conferir só a data pode te enganar','Você conferiu a versão junto da data de GTA 6?'],
 'C02':['Jason quer sossego. Lucia quer um plano. E agora?','O conflito de Jason e Lucia pode começar no mesmo sonho'],
 'C03':['Você reparou no fundo desta imagem de GTA 6?','O abraço distrai. O fundo muda tudo em GTA 6'],
 'C04':['Vice City: saudade de 1986 ou de 2002?','A plateia de Vice City mudou — e isso diz muito'],
 'C05':['Trailer 2 de GTA 6: câmera bonita não prova controle','GTA 6: gameplay no trailer não explica cada cena'],
 'C06':['Artwork ou screenshot? Esse detalhe muda GTA 6','Antes do zoom em GTA 6, confira a categoria'],
 'C07':['O carro azul de GTA 6 divide o protagonismo','GTA 6: o bairro também quer sua atenção'],
 'C08':['A iguana que rouba a cena em GTA 6','GTA 6: um detalhe minúsculo muda a paisagem'],
 'C09':['Keys ou Grassrivers? GTA 6 muda seu jeito de olhar','GTA 6: o perigo de enxergar tudo — ou quase nada'],
 'C10':['Self Radio: o intervalo também faz parte de GTA V','GTA V no PC: sua música dentro de uma emissora'],
 'C11':['Brian oferece a casa. O que Jason entrega em troca?','GTA 6: grátis não significa sem compromisso'],
 'C12':['Raul Bautista: saber fazer é saber parar?','O risco de confiar na experiência em GTA 6'],
 'L01-R02':['GTA 6: confiança sob pressão não confirma traição','Quem trai quem? A premissa de GTA 6 não responde'],
 'L01-R03':['GTA 6: fachadas não confirmam portas abertas','O mapa de GTA 6 não cabe nesta conclusão']}
KEYS={
 'C01':['GTA 6 PC','GTA 6 plataformas'], 'C02':['Jason e Lucia','história GTA 6'],
 'C03':['Jason e Lucia','detalhes GTA 6'],'C04':['Vice City','GTA Vice City','nostalgia'],
 'C05':['GTA 6 trailer 2','GTA 6 gameplay','PS5'],'C06':['GTA 6 screenshots','GTA 6 artwork'],
 'C07':['GTA V','carros GTA 6','Vice City'],'C08':['iguana GTA 6','Leonida Keys'],
 'C09':['Leonida Keys','Grassrivers'],'C10':['Self Radio','Self Radio PC','rádio GTA V'],
 'C11':['Jason Duval','Brian Heder'],'C12':['Raul Bautista'],
 'L01-R02':['Jason e Lucia','história GTA 6'],'L01-R03':['mapa GTA 6','Leonida']}

def put(p,t):p.write_text(t.rstrip()+'\n',encoding='utf8')
def mm(t):return f'{int(t)//60:02}:{int(t)%60:02}'
def source_for(p):
 if 'Cheetah_2012' in p:return TRANSPORT
 if 'Vice_City_classico' in p:return VICE
 if 'N-xHcvug3WI' in p:return 'https://www.youtube.com/watch?v=N-xHcvug3WI'
 if 'Trailer_2' in p:return T2
 if 'Trailer_1' in p:return ROCK+'/trailer-1'
 if 'Launch_Trailer' in p:return ROCK+'/media'
 return MEDIA

def make(rid):
 folder=BASE/rid;p=folder/'publicacao';p.mkdir(exist_ok=True)
 data=json.loads((folder/'projeto/timeline.json').read_text(encoding='utf8'))
 title,summary,question,cover,parent=META[rid]
 assert len(title)<=100
 game='Grand Theft Auto V' if rid=='C10' else 'Grand Theft Auto VI'
 hashtags='#GTAV #SelfRadio #Shorts' if rid=='C10' else '#GTA6 #GTAVI #Shorts'
 refs=list(SOURCES[rid]);refs += [('Imagens de divulgação e trechos do acervo Rockstar',MEDIA)] if rid!='C10' and not any(u==MEDIA for _,u in refs) else []
 desc=summary+'\n\n'+question+'\n\nPixel Procurado — detalhes, histórias e evidências dos jogos.\nAnálise editorial: interpretações e exemplos são identificados no vídeo.\n\nFontes e referências:\n'+'\n'.join(f'{name}: {url}' for name,url in refs)
 desc+='\n\nImagens e trechos de divulgação: Rockstar Games. Edição, gráficos e análise: Pixel Procurado. Narração sintética produzida com Gemini TTS.\n\n'+hashtags
 assert len(desc)<5000
 tags=', '.join((['GTA V','GTA 5','Grand Theft Auto V'] if rid=='C10' else ['GTA 6','GTA VI','Grand Theft Auto VI'])+KEYS[rid]+['Pixel Procurado','análise de jogos'])
 assert len(tags)<500
 put(p/'01_TITULO.txt',title);put(p/'02_DESCRICAO.txt',desc);put(p/'03_COMENTARIO_FIXADO.txt',question);put(p/'04_TAGS.txt',tags)
 put(p/'05_TITULOS_ALTERNATIVOS.txt','A — '+title+'\nB — '+ALTS[rid][0]+'\nC — '+ALTS[rid][1]+'\n\nA é a recomendação inicial. As alternativas são hipóteses editoriais; não são resultados de teste A/B.')
 shots=[s for s in data['shots'] if s['part']==0 and 'SEGUNDA BATIDA' not in str(s['anchor'])]
 second=min((s for s in shots if 18<=s['start']<=40),key=lambda s:abs(s['start']-25))
 third=min((s for s in shots if s['start']>=45 and s['start']<=data['duration']-11),key=lambda s:abs(s['start']-data['duration']*.73))
 chapters=f"00:00 {data['shots'][0]['title'].replace(chr(10),' ')}\n{mm(second['start'])} {second['title'].replace(chr(10),' ')}\n{mm(third['start'])} {third['title'].replace(chr(10),' ')}"
 put(p/'06_TEMPOS_OPCIONAIS.txt',chapters+'\n\nTempos obtidos da montagem final. A descrição principal fica curta, sem capítulos. Estes marcadores são opcionais para consulta; não pressupõem capítulos no player de Shorts.')
 media=[]
 for s in data['shots']:
  if s['file']:
   media.append(dict(start=round(s['start'],3),end=round(s['end'],3),file=s['file'],source=source_for(s['file']),source_start=s['offset'],motion_seconds=s.get('motion'),treatment=s['mode'],crop=s.get('crop'),highlight=s.get('ring')))
 put(p/'07_CREDITOS_E_MIDIAS.json',json.dumps(media,ensure_ascii=False,indent=2))
 rows=['# Mídias e decisões de edição','', 'Cada entrada aponta o arquivo usado e a página de referência do acervo. Uma página de origem não equivale a autorização ou liberação do Content ID. Os arquivos locais de trailers foram fornecidos pelo projeto; seus nomes não comprovam, por si só, a identidade de cada download.', '', '| Vídeo final | Arquivo | Entrada na fonte | Movimento e tratamento | Referência |','|---|---|---|---|---|']
 for m in media:
  treatment=m['treatment']+(f"; movimento por até {m['motion_seconds']:.2f}s e quadro final sustentado" if m['motion_seconds'] is not None else '')
  rows.append(f"| {mm(m['start'])}–{mm(m['end'])} | {m['file']} | {m['source_start']:.2f}s | {treatment} | [Origem]({m['source']}) |")
 rows+=['','Gráficos: composição original em Remotion. Imagens fixas recebem recortes, aproximações ou destaques; não representam gameplay novo. O áudio original dos trailers foi removido. A locução aprovada permanece integral, sem trilha comercial acrescentada.','', 'A capa é uma montagem editorial em 1080×1920: arte-base temática gerada por IA, frase aplicada separadamente e identificação oficial do jogo adicionada no acabamento. Ela não é uma captura oficial nem promete uma cena existente no jogo. O PNG master, o JPG para envio e o prompt estão nesta pasta.']
 if rid=='C05':rows+=['','Apuração reconfirmada em 27/10/2026: o campo público shortDescription retornado pelo YouTube informa captura integral dentro do jogo no PS5 e proporção igual de gameplay e cenas cinematográficas. O trecho pertinente e o método estão em ../projeto/fonte_descricao_trailer2.txt. Essa informação se refere ao conjunto do trailer; não identifica o controle de cada plano.']
 put(p/'07_CREDITOS_E_MIDIAS.md','\n'.join(rows))
 movie=folder/'exportacoes'/f'Pixel_Procurado_{rid}_Short_1080x1920.mp4'
 size=f'{movie.stat().st_size/1024**2:.1f} MiB' if movie.exists() else 'tamanho disponível após a renderização'
 guide=f'''# Publicação — {rid}

Preparado em 27/10/2026. O pacote não executa upload nem publicação.

**Título recomendado:** {title}

**Capa:** capa_youtube.jpg. A arte temática e a frase curta resumem o conflito central deste Short; texto e identificação do jogo foram aplicados separadamente para preservar a grafia.

## Arquivos

- Vídeo: ../exportacoes/{movie.name} — {data['duration']:.2f}s, 1080×1920, 30 fps, H.264/AAC, {size}.
- Capa: capa_youtube.jpg; master em capa_master.png e direção em PROMPT_THUMBNAIL.txt, todos preparados em 1080×1920.
- Texto: 01_TITULO.txt, 02_DESCRICAO.txt, 03_COMENTARIO_FIXADO.txt e 04_TAGS.txt.
- Legendas: ../exportacoes/{rid}_legendas.srt. O MP4 já contém legendas gravadas; ativar também o SRT pode produzir duas camadas na tela.
- Fontes e trechos usados: 07_CREDITOS_E_MIDIAS.md e .json.
- Edição recuperável: ../projeto/timeline.json, DIRECAO.md e ../voz/narracao.wav. Os originais de imagem permanecem no acervo compartilhado do projeto.

## Preenchimento sugerido no Studio

| Campo | Valor |
|---|---|
| Categoria | Jogos |
| Jogo | {game}, se a entrada correta aparecer |
| Idioma | Português (Brasil) |
| Público | Não é conteúdo para crianças |
| Playlist | Pixel Procurado — Shorts de GTA |
| Licença | Padrão do YouTube |
| Comentários | Ativados, com moderação básica |
| Promoção paga | Não, se não houve patrocínio ou relação comercial |
| Local de gravação | Deixar vazio |
| Visibilidade inicial | Não listado, para revisão do processamento |
| Visibilidade final | Público ou Programado |

“Não é para crianças” e restrição etária são campos diferentes. Avalie esta edição efetiva ao responder sobre idade; a classificação do jogo não define automaticamente a do Short.

## Envio

1. No YouTube Studio, abra Criar → Enviar vídeos e selecione o MP4 final.
2. Cole os arquivos de título e descrição; coloque as tags no campo próprio. A descrição já inclui três hashtags pertinentes.
3. Confira público, idioma, categoria e os demais campos acima.
4. Envie capa_youtube.jpg no Studio para computadores, em Conteúdo → Shorts → edição → Miniatura. A conta precisa estar verificada. O arquivo tem 9:16; se o recurso não aparecer, use a seleção de quadro oferecida pela sua conta, perto de 1,1 segundo. [Instruções oficiais](https://support.google.com/youtube/answer/72431?hl=pt-BR).
5. Aguarde processamento em 1080p. Assista à abertura, à região de {mm(data['duration']/2)} e aos segundos finais; confira a leitura no celular e a continuidade ao repetir.
6. Examine Verificações. Todos estes vídeos ultrapassam um minuto: uma reivindicação ativa de Content ID pode bloquear um Short dessa duração. A trilha dos trailers foi removida, mas isso não libera automaticamente as imagens. [Regra para Shorts de até três minutos](https://support.google.com/youtube/answer/15424877?hl=pt-BR).
7. Escolha Público ou programe para um horário do seu relatório “Quando seus espectadores estão no YouTube”. Sem dados do canal, teste uma janela consistente, sem presumir um horário universal.
8. Depois de publicar, poste e fixe o comentário de 03_COMENTARIO_FIXADO.txt.
9. Em Conteúdo → edição deste Short, adicione como vídeo relacionado o episódio {parent} deste projeto, **somente se ele já estiver no canal e corresponder ao assunto**. Precisa estar público ou não listado, com recursos avançados habilitados. Sem episódio disponível, deixe vazio. [Ajuda oficial](https://support.google.com/youtube/answer/14075157?hl=pt-BR).

## IA e áudio

A descrição informa o uso de narração sintética com Gemini, e os créditos registram a arte-base gerada da thumbnail. No campo “Uso de IA”, responda conforme a origem efetiva da voz e o conteúdo final: a clonagem da própria voz está entre as exceções documentadas; uma representação realista de outra pessoa dizendo algo que não disse exige declaração. Não presumimos aqui de quem é a voz personalizada. Gameplay, legendas e auxílio em roteiro não exigem declaração por si sós. [Exemplos oficiais](https://support.google.com/youtube/answer/14328491?hl=pt-BR).

## Retenção e acompanhamento

Abertura sem vinheta exclusiva; texto de conflito desde o início. As mudanças de imagem acompanham as falas, e o último plano retoma a promessa da abertura. O áudio completo foi preservado. A edição não inclui uma tela de encerramento que interrompa esse retorno.

Observe a curva de retenção, a porcentagem média visualizada (APV), a duração média e a relação entre quem ficou assistindo e quem deslizou. Compare com Shorts seus de duração e tema semelhantes. Faça uma primeira leitura após 48–72 horas e uma segunda após sete dias; esses intervalos são uma rotina sugerida, não uma regra do algoritmo. Não há garantia de viralização.

Se houver queda nos primeiros segundos, teste primeiro o enquadramento/primeira frase visual. Queda no meio pede verificar a fala e a imagem naquele instante. Não altere título, capa e montagem simultaneamente se quiser entender qual mudança ajudou. Títulos B e C estão em 05_TITULOS_ALTERNATIVOS.txt; não são testes já realizados.

Capítulos não são necessários para esta versão. 06_TEMPOS_OPCIONAIS.txt contém três marcadores reais caso queira usá-los em contexto compatível. Para levar a outro vídeo, priorize o campo de vídeo relacionado.
'''
 put(p/'00_GUIA_DE_PUBLICACAO.md',guide)
 return dict(id=rid,title=title,duration=round(data['duration'],2),file=movie.relative_to(BASE).as_posix(),status='validado' if (folder/'projeto/qa/validacao_final.json').exists() else 'em renderização')

if __name__=='__main__':
 allrows=[make(rid) for rid in PLANS]
 index=['# Shorts — Pixel Procurado','', 'Cada pasta reúne vídeo, capa, narração, legendas, projeto e textos de postagem. Comece pelo guia de publicação do vídeo escolhido.','', '| ID | Título | Duração | Vídeo | Publicação | Estado |','|---|---|---|---|---|---|']
 for r in allrows:index.append(f"| {r['id']} | {r['title']} | {mm(r['duration'])} | [MP4]({r['file']}) | [Guia]({r['id']}/publicacao/00_GUIA_DE_PUBLICACAO.md) | {r['status']} |")
 index+=['','## Estrutura de cada pasta','', '- exportacoes: MP4 final e SRT.','- publicacao: capa JPG/PNG, título, descrição, comentário, tags, alternativas, guia e créditos.','- voz: WAV integral, texto limpo, direção Gemini e transcrição com tempos.','- projeto: linha do tempo, imagens de sobreposição, planos intermediários e validação técnica.','', 'O acervo original permanece compartilhado em videosGTAVI e _acervo para evitar duplicação. Mantenha a raiz do projeto para reeditar. Os MP4s finais e as capas podem ser copiados e usados independentemente.','', 'Os 12 cortes C01–C12 são a série principal. L01-R02 e L01-R03 são duas reservas, também montadas. Total de narração: 19min05s.','', 'Sugestão editorial de ordem: C03, C08, C02, C11, C12, C09, C04, C07, C06, C05, C01, C10; encaixar as duas reservas conforme o interesse observado. A ordem alterna detalhes visuais, personagens e explicações. Não é uma previsão de desempenho.','', 'Não houve upload. Os guias refletem a consulta às regras oficiais em 27/10/2026. Antes de tornar público, confira o resultado de Verificações no Studio.']
 put(BASE/'00_COMECE_AQUI.md','\n'.join(index))
 with (BASE/'CONTROLE_DE_PUBLICACAO.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['id','title','duration','file','status']);w.writeheader();w.writerows(allrows)
 print('PUBLICATION PACKAGES: '+str(len(allrows)))
