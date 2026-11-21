"""Direção contextual de L04, exclusivamente Trailer 2 e mídia examinada."""
import json, math, re, unicodedata, wave, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'producao/L04'; W=P/'projeto'; W.mkdir(exist_ok=True)
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()))
words=json.loads((P/'voz/palavras_alinhadas.json').read_text(encoding='utf8'))
with wave.open(str(P/'voz/narracao_normalizada.wav')) as w:duration=w.getnframes()/w.getframerate()
tokens=[norm(w['word']) for w in words]
def anchor(s):
 t=[norm(x) for x in s.split()];hits=[i for i in range(len(tokens)-len(t)+1) if tokens[i:i+len(t)]==t];assert len(hits)==1,(s,hits)
 return hits[0]
shots=[];trailer='videosGTAVI/GTAVI_Trailer_2.mp4'
art='videosGTAVI/GTAVI_Artwork_Wallpapers/Jason_and_Lucia_01/Jason_and_Lucia_01_landscape.jpg'
screen='videosGTAVI/GTAVI_Screenshots/People/Jason and Lucia/Jason_and_Lucia_01.jpg'
def add(a,file='',offset=0,label='',graphic='',title='',sub='',**extra):
 i=anchor(a) if a else 0;frame=round(words[i]['start']*30) if a else 0
 d=dict(anchor=a or 'INÍCIO',anchorWordIndex=i,fromFrame=frame,kind='video' if file.endswith('.mp4') else 'image' if file else 'graphic',file=file,offset=offset,label=label,graphic=graphic,title=title,sub=sub,source='GTA VI • Trailer 2 • Rockstar Games' if file==trailer else 'GTA VI • Biblioteca de mídia • Rockstar Games' if file else 'PIXEL PROCURADO • GRÁFICO EDITORIAL',presentation='full' if file else 'graphic',zoom=[1,1.025],focus=[.5,.5],captionPosition='bottom',panelSide='left',evidence='official-material' if file else 'editorial-graphic',editorialPurpose=a or 'Abrir com a questão e responder imediatamente')
 d.update(extra);shots.append(d);return d
def video(a,offset,label='TRAILER 2 / MATERIAL OFICIAL'):return add(a,trailer,offset,label)
def graphic(a,title,sub='',label='LEITURA DA EVIDÊNCIA'):return add(a,label=label,graphic='headline',title=title,sub=sub,layout=dict(side='left',top=280,width=1500))
video(None,28,'GAMEPLAY OU CINEMA?')
graphic('A Rockstar descreve metade','50% gameplay\n50% cenas prontas','Composição informada pela Rockstar • não classifica cada plano','TRAILER 2 / DECLARAÇÃO OFICIAL')
video('O problema é quando a gente pausa',65,'A CÂMERA NÃO RESOLVE SOZINHA')
add('E eu entendo a empolgação','producao/L04/midia/L04_Trailer2_agua_05x.mp4',label='EMPOLGAÇÃO / LUZ NA ÁGUA',source='GTA VI • Trailer 2 • Rockstar Games • Velocidade 0,5× (edição)')
s=add('Mas dá pra aproveitar o trailer',label='TRÊS CHECAGENS',graphic='list',title='O que a imagem prova?',items=['Gameplay ou cena pronta?','Captura ou plataforma?','Ilustração ou screenshot?'],stage=3)
s['cuePhrases']=['o que é gameplay onde','onde o jogo vai sair','e qual imagem realmente']
video('Vamos usar o Trailer dois',12,'RECORTE DESTE VÍDEO / TRAILER 2')
video('Começa pela câmera atrás',24.8,'CÂMERA / UMA PISTA')
video('Esse ângulo lembra',25,'ENQUADRAMENTO NÃO CONFIRMA CONTROLE')
video('Só que uma cena pronta',44)
graphic('A câmera dá uma pista','Ângulo ≠ controle','Quem decidiu a ação?')
graphic('Foto de anúncio de apartamento','O ângulo vende.','ANALOGIA • anúncio de apartamento','HUMOR / ANALOGIA')
graphic('Você visita e precisa escolher','Geladeira\nou cozinha?','ANALOGIA • o enquadramento pode enganar','HUMOR / ANALOGIA')
video('Com o trailer a pergunta',31,'O QUE A IMAGEM MOSTRA?')
graphic('Pensa numa cena','Entrar → sentar → sair','EXEMPLO HIPOTÉTICO • nenhuma mecânica confirmada','HIPÓTESE / AÇÃO VISÍVEL')
graphic('Mas isso sozinho','Hora? Destino?','EXEMPLO HIPOTÉTICO • quem escolheu?','HIPÓTESE / ESCOLHA DO JOGADOR')
graphic('O exemplo é hipotético','Ação na tela\n≠ liberdade de decidir','Exemplo explicativo, sem atribuir comandos a um plano real','HIPÓTESE / NÃO É CONFIRMAÇÃO')
video('A declaração da Rockstar',75,'MISTURA CONFIRMADA / TRAILER 2')
video('Ela não identifica',105,'CLASSIFICAÇÃO CENA A CENA / NÃO INFORMADA')
graphic('Então dá pra dizer','Tem gameplay.','Identificar cada plano exige evidência adicional.','TRAILER 2 / RESPOSTA CONFIRMADA')
graphic('Agora olha o detalhe','Capturado no PS5','Trailer 2 • captura dentro do jogo','01 / APARELHO DA CAPTURA')
graphic('Isso faz de GTA seis','Exclusivo? Não.','Página oficial: PlayStation 5 e Xbox Series X|S','02 / PLATAFORMAS ANUNCIADAS')
s=add('Uma informação diz',label='DUAS PERGUNTAS DIFERENTES',graphic='list',title='Captura ≠ exclusividade',items=['Gravação: PlayStation 5','Plataformas: PS5 + Xbox Series X|S'],stage=2);s['cuePhrases']=['Uma informação diz','A outra diz']
graphic('Gravar um churrasco','Gravou no iPhone…','…a linguiça não virou exclusiva.','HUMOR / ANALOGIA')
graphic('Embora vender o pão','Pão de alho\nvendido à parte.','ANALOGIA / HUMOR','HUMOR / ANALOGIA')
graphic('O destaque dado','Veja a lista completa.','PlayStation 5 • Xbox Series X|S','PÁGINA OFICIAL / PLATAFORMAS')
video('Eu quero jogar GTA',32,'QUERO JOGAR / NÃO DEFENDER MARCA')
graphic('E tem uma terceira','Ilustração\nou captura?','Biblioteca oficial: categorias diferentes','03 / ORIGEM DA IMAGEM')
add('Olha a arte de Jason',art,label='ILUSTRAÇÃO / ARTWORK',zoom=[1,1])
add('Aquilo é um desenho',art,label='ILUSTRAÇÃO / ARTWORK',zoom=[1,1.035])
add('Foi feito pra ficar bonito',art,label='ILUSTRAÇÃO / PÔSTER E PAPEL DE PAREDE',zoom=[1.035,1])
add('Agora compara com a imagem',screen,label='CAPTURA DE TELA / SCREENSHOT',zoom=[1,1])
add('Esse é outro tipo',screen,label='CAPTURA DE TELA / OUTRA CATEGORIA',zoom=[1,1.025])
add('Se a pergunta é sobre',screen,label='CAPTURA / DETALHES DESTE QUADRO',zoom=[1.025,1.04])
add('O desenho mostra',art,label='ILUSTRAÇÃO / REPRESENTAÇÃO ARTÍSTICA',zoom=[1,1.025])
graphic('Usar o pôster','Planta do apartamento\n≠ ventilação','ANALOGIA • representação e comportamento','HUMOR / ANALOGIA')
graphic('Tem uma seta desenhada','Uma seta.\nUm vento maravilhoso.','ANALOGIA / HUMOR','HUMOR / ANALOGIA')
add('E vale o cuidado',screen,label='CAPTURA / UM INSTANTE',zoom=[1,1.02])
graphic('Sozinha ela não demonstra','Um quadro\n≠ desempenho','Movimento e resposta ao controle exigem outro material.','LIMITE DA EVIDÊNCIA')
video('Pra isso a gente precisa',139,'TRAILER 2 / IMAGEM EM MOVIMENTO')
video('Gostar da imagem é fácil',151,'ORIGEM + FUNÇÃO DA IMAGEM')
s=add('No Trailer dois a Rockstar',label='TRÊS CHECAGENS / RESPOSTAS',graphic='list',title='Antes de distribuir certeza',items=['Trailer 2 mistura gameplay e cenas prontas','Captura: PS5 • plataformas incluem Xbox','Artwork e screenshot têm funções diferentes'],stage=3)
s['cuePhrases']=['No Trailer dois a Rockstar','O PS5 foi o aparelho','Na biblioteca desenho']
video('Qual detalhe do material',117,'QUAL DETALHE VOCÊ QUER EXAMINAR?')
video('Aqui é o Pixel Procurado',128,'PIXEL PROCURADO / A PISTA VEM COM A FONTE')
video('Só traz a prudência',155,'TRAGA A PRUDÊNCIA DE VOLTA')
total=math.ceil(duration*30)
for i,s in enumerate(shots):
 end=shots[i+1]['fromFrame'] if i+1<len(shots) else total;s.update(frames=end-s['fromFrame'],start=s['fromFrame']/30,end=end/30)
 assert s['frames']>0,(i,s)
 if s['file']:assert (ROOT/s['file']).is_file()
 if s['kind']=='video':assert s['offset']+s['frames']/30<160,(i,s['offset'],s['frames']/30)
 if s.get('cuePhrases'):s['cues']=[round(words[anchor(a)]['start']*30)-s['fromFrame'] for a in s.pop('cuePhrases')]
 s['animate']=bool(s['graphic']);s['animationFrames']=min(s['frames'],max(s.get('cues',[0]))+20) if s['animate'] else 1
caps=[];batch=[]
for i,w in enumerate(words):
 batch.append(w);text=' '.join(w['word'] for w in batch)
 if len(batch)>=8 or len(text)>=48 or (len(batch)>=3 and w['word'].endswith(('.','?','!',':',';'))) or i==len(words)-1:
  caps.append(dict(start=batch[0]['start'],end=min(duration,w['end']+.10),text=text));batch=[]
for a,b in zip(caps,caps[1:]):a['end']=min(max(a['end'],a['start']+.85),b['start'])
# Both local ASRs identify the brief spoken contraction here. Keep the
# untouched script/alignment as audit input; captions follow the utterance.
for cap in caps:cap['text']=cap['text'].replace('Vamos usar o Trailer','Vamos ao Trailer')
paragraphs=[]
for i,p in enumerate((P/'01_NARRACAO.txt').read_text(encoding='utf8').strip().split('\n\n')):
 ix=anchor(' '.join(p.split()[:8]));paragraphs.append(dict(paragraph=i+1,start=words[ix]['start'],text=p))
d=dict(episode='L04',title='GTA 6: tem gameplay no Trailer 2? Três dúvidas resolvidas',duration=duration,frames=total,fps=30,width=3840,height=2160,logicalWidth=1920,logicalHeight=1080,voice='producao/L04/voz/narracao_normalizada.wav',alignment='producao/L04/voz/palavras_alinhadas.json',pathBase='project-root',contractVersion='L04-1920-logical-v1',status='final-direction',alignmentStatus='validated-input',shots=shots,captions=caps,paragraphs=paragraphs)
(W/'edicao_l04.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(duration=duration,shots=len(shots),captions=len(caps),videos=sum(s['kind']=='video' for s in shots)),indent=2))
