"""L05: seis fontes exatas, cortes e destaques ancorados na voz."""
import json,math,re,unicodedata,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'producao/L05';W=P/'projeto';W.mkdir(exist_ok=True)
words=json.loads((P/'voz/palavras_alinhadas.json').read_text(encoding='utf8'))
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()))
tokens=[norm(w['word']) for w in words]
def anchor(s):
 t=[norm(x) for x in s.split()];hits=[i for i in range(len(tokens)-len(t)+1) if tokens[i:i+len(t)]==t];assert len(hits)==1,(s,hits);return hits[0]
with wave.open(str(P/'voz/narracao_normalizada.wav')) as w:duration=w.getnframes()/w.getframerate()
shots=[]
files={**{f'V{i}':f'producao/L05/midia/V{i}.jpg' for i in range(1,4)},**{f'VI{i}':f'videosGTAVI/GTAVI_Screenshots/Places/Vice City/Vice_City_{n:02}.jpg' for i,n in enumerate([5,9,11],1)}}
def add(a,key='',title='',sub='',label='',**kw):
 i=anchor(a) if a else 0;classic=bool(key)
 s=dict(anchor=a or 'INÍCIO',anchorWordIndex=i,fromFrame=round(words[i]['start']*30) if a else 0,kind='image' if classic else 'graphic',file=files.get(key,''),offset=0,label=label or ('GTA V / DIVULGAÇÃO, 2012' if key.startswith('V') and not key.startswith('VI') else 'GTA VI / IMAGEM OFICIAL' if key else 'LEITURA DA COMPOSIÇÃO'),graphic='' if classic else 'headline',title=title,sub=sub,source='Rockstar Games • Transport (2012) • fonte 640×360, ampliada' if key in ['V1','V2','V3'] else 'Rockstar Games • Biblioteca oficial • screenshot' if key else 'PIXEL PROCURADO • GRÁFICO EDITORIAL',presentation='classic-card' if classic else 'graphic',viewport=dict(x=64,y=150,width=1280,height=720),zoom=[1,1.012] if classic else [1,1],focus=[.5,.5],captionPosition='bottom',panelSide='left',layout=dict(side='left',top=280,width=1550),evidence='official-material' if key else 'editorial-graphic',editorialPurpose=a or 'Entregar contraste de abertura')
 s.update(kw);shots.append(s);return s
# Rect coordinates normalized to the 16:9 source, mapped to the image card.
def focus(a,key,title,rects,sub=''):
 s=add(a,key,title,sub,graphic='focus',zoom=[1,1]);s['focusRects']=[]
 for n,(phrase,x,y,w,h,label) in enumerate(rects):
  s['focusRects'].append(dict(id=str(n),cuePhrase=phrase,x=64+x*1280,y=150+y*720,width=w*1280,height=h*720,label=label))
 return s
add(None,'VI2','Olhe a rua.','O contexto também participa da imagem.')
focus('Na foto de GTA seis tem','VI2','Carro + bairro',[('tem moto empinando',.25,.42,.22,.34,'Motos'),('e pilares pintados',.01,.05,.20,.83,'Murais')])
add('Vamos comparar seis fotos oficiais','VI1','6 fotos\n3 pares','Praia • carros • vista aérea',label='O RECORTE / SEIS IMAGENS OFICIAIS')
add('Começa pelo ciclista','V1','Uma ação\nprincipal','Transport • 20 de agosto de 2012')
focus('A câmera fica baixa','V1','Ângulo + ação',[('A câmera fica baixa',.40,.02,.40,.96,'Ciclista'),('O píer e a roda-gigante',.08,.32,.88,.60,'Píer e roda-gigante')])
add('Você bate o olho','V1','A ação\nconduz o olhar','Pedalar pela praia.')
add('O lugar ajuda','V1','O cenário\napoia a ação','Píer, luz e enquadramento.',zoom=[1.012,1])
add('É uma imagem direta','V1','Assunto\nprincipal','Uma leitura imediata.')
add('Agora muda pra praia','VI1','Várias\nparadas','O olhar explora o mesmo quadro.',zoom=[1,1])
focus('Tem uma pessoa tomando sol','VI1','Observe\na ordem',[('Tem uma pessoa tomando sol',.00,.68,.55,.31,'Tomando sol'),('um casal andando',.49,.11,.34,.76,'Casal'),('o homem com detector',.18,.29,.17,.44,'Detector')])
focus('O detector é um detalhe ótimo','VI1','Uma atividade\nno quadro',[('O detector é um detalhe ótimo',.18,.29,.17,.44,'Detector de metais')])
add('A gente olha e já imagina','VI1','A joia…\nou a tampinha?','Imaginação a partir de um objeto visível.',zoom=[1.012,1])
add('Essa história é nossa imaginação','',title='Imaginação\n≠ missão anunciada',sub='A cena permite uma leitura; não anuncia uma mecânica.')
add('O que está visível é suficiente','VI1','Diferentes\nocupações','Pessoas com poses e atividades distintas.')
add('Na foto do ciclista acompanhamos','V1','Uma ação','Comparação de enquadramentos.',zoom=[1,1])
add('Nessa praia exploramos','VI1','Pequenas\nsituações','Comparação de enquadramentos.',zoom=[1,1])
add('Ela não prova','',title='Fotos escolhidas\npara divulgação',sub='Este recorte não mede a densidade média dos jogos.')
add('E com os carros','V2','A máquina\nprimeiro','Traseira próxima e rua ao fundo.')
focus('O aerofólio chama atenção','V2','A máquina\ndomina',[('O aerofólio chama atenção',.34,.15,.55,.21,'Aerofólio'),('tem fumaça junto dos pneus',.02,.48,.42,.39,'Fumaça')])
add('Tem cara de anúncio','V2','Vontade\nde dirigir','A leitura da imagem, sem som de motor.')
add('Na foto de GTA seis o carro','VI2','A rua\nparticipa','O veículo pertence a uma cena coletiva.',zoom=[1,1])
focus('Só que o entorno insiste','VI2','Além\nda lataria',[('tem moto gente empinando',.24,.40,.26,.34,'Motos e pessoas'),('fios e um viaduto',.20,.00,.79,.40,'Fios e viaduto')])
focus('Os murais ocupam','VI2','Personalidade\ndo lugar',[('Os murais ocupam',.00,.03,.24,.85,'Pilares pintados')])
add('As pessoas e as motos','VI2','Carro, gente\ne bairro','Minha leitura da composição.',zoom=[1.012,1])
add('Se você recorta só o automóvel','VI2','O entorno\nfaz falta','Retorno ao quadro inteiro.',zoom=[1,1])
add('É como mostrar a foto de um churrasco','',title='A churrasqueira\nsem o encontro',sub='ANALOGIA • o objeto sozinho não conta toda a cena.',label='HUMOR / ANALOGIA')
add('Isso não diminui','V2','Outra\nprioridade','A máquina ocupa o centro da leitura.')
add('a outra dá mais espaço','VI2','Uma relação','Carro • gente • bairro',zoom=[1,1])
add('Agora vamos subir','V3','A aeronave\nconduz','Próxima, sobre as luzes da cidade.')
focus('um jato ocupa boa parte','V3','O jato\nem primeiro plano',[('um jato ocupa boa parte',.03,.15,.94,.76,'Aeronave')])
add('O avião fica próximo','V3','Veículo +\npaisagem','O cenário passa embaixo dele.',zoom=[1.012,1])
add('Na imagem de GTA seis','VI3','A cidade\nganha espaço','A aeronave ajuda a perceber as partes.',zoom=[1,1])
focus('o helicóptero aparece menor','VI3','Outra\nrelação',[('o helicóptero aparece menor',.60,.22,.09,.10,'Helicóptero'),('Há água barcos e luzes',.67,.53,.32,.43,'Água e barcos')])
add('A cidade ganha mais espaço','VI3','Cidade\n+ aeronave','Prioridade do enquadramento.',zoom=[1,1.012])
add('Pensa numa foto de viagem','',title='Você ou\no lugar?',sub='ANALOGIA • mudar o enquadramento muda o protagonismo.',label='HUMOR / ANALOGIA')
add('Nenhuma das fotos mede','',title='Enquadramento\n≠ tamanho do mapa',sub='Uma foto muda a prioridade, não mede quilômetros.')
add('É esse cuidado','VI3','Sem régua\npara o mapa','Um helicóptero pequeno não mede o mundo.',zoom=[1,1])
add('Assim como um jato enorme','V3','Sem régua\npara o mapa','Um jato próximo não limita o mundo.',zoom=[1,1])
add('E comparar os gráficos','',title='Não é um\nbenchmark',sub='Datas, luz, situações e enquadramentos diferentes.')
add('O material de GTA cinco','V1','Divulgação\nde 2012','Não representa um teste da versão atual.',zoom=[1,1])
add('Os enquadramentos a luz','VI1','Analisar\na fotografia','O corpus tem limites.',zoom=[1,1])
add('O que os três pares mostram','',title='O caminho\ndo olhar',sub='Três pares, três relações entre assunto e contexto.')
add('O ciclista e as pequenas','VI1','Praia','Ação principal → pequenas situações.',zoom=[1,1])
add('O carro e a rua','VI2','Carros','Máquina → relação com o bairro.',zoom=[1,1])
add('A aeronave e a cidade','VI3','Vista aérea','Veículo → cidade ao redor.',zoom=[1,1])
add('Qual desses lugares','VI1','Praia, carros\nou orla?','Onde você esqueceria a missão?',zoom=[1,1.012])
add('o encontro de carros ou','VI2','Olhe\nas bordas.','O carro já tem a nossa atenção.',zoom=[1,1.012])
total=math.ceil(duration*30)
for i,s in enumerate(shots):
 end=shots[i+1]['fromFrame'] if i+1<len(shots) else total;s.update(frames=end-s['fromFrame'],start=s['fromFrame']/30,end=end/30);assert s['frames']>0,(i,s)
 if s['file']:assert (ROOT/s['file']).is_file()
 for r in s.get('focusRects',[]):r['cue']=round(words[anchor(r.pop('cuePhrase'))]['start']*30)-s['fromFrame'];assert r['cue']>=0
 s['animate']=bool(s['graphic']);s['animationFrames']=min(s['frames'],max([r['cue'] for r in s.get('focusRects',[])] or [0])+20) if s['animate'] else 1
caps=[];batch=[]
for i,w in enumerate(words):
 batch.append(w);text=' '.join(w['word'] for w in batch)
 if len(batch)>=8 or len(text)>=48 or (len(batch)>=3 and w['word'].endswith(('.','?','!',':',';'))) or i==len(words)-1:
  caps.append(dict(start=batch[0]['start'],end=min(duration,w['end']+.10),text=text));batch=[]
if len(caps[-1]['text'].split())<3:
 caps[-2]['text']+=' '+caps[-1]['text'];caps[-2]['end']=caps[-1]['end'];caps.pop()
for a,b in zip(caps,caps[1:]):a['end']=min(max(a['end'],a['start']+.85),b['start'])
paragraphs=[]
for i,p in enumerate((P/'01_NARRACAO.txt').read_text(encoding='utf8').strip().split('\n\n')):
 ix=anchor(' '.join(p.split()[:8]));paragraphs.append(dict(paragraph=i+1,start=words[ix]['start'],text=p))
d=dict(episode='L05',title='GTA V e GTA VI: três diferenças que estas imagens revelam',duration=duration,frames=total,fps=30,width=3840,height=2160,logicalWidth=1920,logicalHeight=1080,voice='producao/L05/voz/narracao_normalizada.wav',alignment='producao/L05/voz/palavras_alinhadas.json',pathBase='project-root',contractVersion='L05-1920-logical-v1',status='final-direction',alignmentStatus='validated-input',shots=shots,captions=caps,paragraphs=paragraphs)
(W/'edicao_l05.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8');print(dict(duration=duration,shots=len(shots),captions=len(caps)))
