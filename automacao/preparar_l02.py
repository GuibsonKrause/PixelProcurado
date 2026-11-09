"""Timeline editorial L02, vinculada às palavras da narração fornecida."""
import difflib, json, math, re, sys, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.production-tools/python'), str(ROOT/'.course-tools')]
import av
P = ROOT/'producao/L02'
WORK = P/'projeto'; WORK.mkdir(exist_ok=True)
def norm(t):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', t.lower()))
paragraphs = (P/'01_NARRACAO.txt').read_text(encoding='utf8').strip().split('\n\n')
script = ' '.join(paragraphs).split()
raw = json.loads((P/'voz/palavras_asr.json').read_text(encoding='utf8'))
a,b = [norm(w['word']) for w in raw], [norm(w) for w in script]
words=[]; corrections=[]
for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if tag == 'equal':
        words.extend(dict(word=script[n],start=raw[i+n-k]['start'],end=raw[i+n-k]['end']) for n in range(k,l))
    else:
        start=raw[i]['start'] if i<len(raw) else raw[-1]['end']
        end=raw[j-1]['end'] if j>i else start
        if end<=start: start=max(raw[i-1]['end'] if i else 0,start-.12)
        corrections.append(dict(time=start,recognized=' '.join(a['word'] for a in raw[i:j]),script=' '.join(script[k:l])))
        for n in range(k,l):
            words.append(dict(word=script[n],start=start+(end-start)*(n-k)/max(1,l-k),end=start+(end-start)*(n-k+1)/max(1,l-k)))
assert len(words)==len(script)
for i,w in enumerate(words):
    w['end']=max(w['end'], w['start']+.03)
    if i+1<len(words): w['end']=min(w['end'],words[i+1]['start'])
    assert w['end']>=w['start'],w
(P/'voz/palavras_alinhadas.json').write_text(json.dumps(words,ensure_ascii=False,indent=2),encoding='utf8')
(WORK/'revisao_asr.json').write_text(json.dumps(corrections,ensure_ascii=False,indent=2),encoding='utf8')
with av.open(str(P/'voz/narracao_normalizada.wav')) as c: duration=c.duration/1e6
fps=30
def at(phrase):
    needle=[norm(x) for x in phrase.split()]
    matches=[i for i in range(len(b)-len(needle)+1) if b[i:i+len(needle)]==needle]
    assert len(matches)==1,(phrase,matches)
    return round(words[matches[0]]['start']*fps)/fps
def pic(who,n):
    group='Places' if who=='Leonida Keys' else 'People'
    return f'GTAVI_Screenshots/{group}/{who}/{who.replace(" ","_")}_{n:02}.jpg'
J=lambda n:pic('Jason Duval',n)
L=lambda n:pic('Lucia Caminos',n)
C=lambda n:pic('Jason and Lucia',n)
shots=[]
def add(phrase,file='',offset=0,label='',title='',sub='',graphic='',**extra):
    t=0 if phrase is None else at(phrase)
    shots.append(dict(start=t,file=file,offset=offset,label=label,title=title,sub=sub,graphic=graphic,anchor=phrase or 'INÍCIO',**extra))
def v(phrase,offset,**kw): add(phrase,'GTAVI_Trailer_2.mp4',offset,**kw)
add(None,J(3),label='DOSSIÊ 02 • JASON DUVAL',title='Uma vida fácil.',sub='Síntese da apresentação oficial',graphic='headline',side='right')
add('Lucia tem um plano',L(1),label='LUCIA CAMINOS',title='Um plano próprio.',graphic='headline',side='right')
add('essa diferença pode pesar',C(9),label='JASON + LUCIA')
v('As apresentações oficiais',79,label='UM FUTURO EM COMUM')
add('eles concordam sobre o preço',C(1),label='A PERGUNTA',title='O mesmo plano?',graphic='headline',side='right')
v('Começa pelo Jason',18,label='01 / O PERCURSO DE JASON')
add('Ele passou pelo Exército',J(2),label='APRESENTAÇÃO OFICIAL',title='Exército → Keys',sub='Trajetória apresentada pela Rockstar',graphic='headline',side='right',source='rockstargames.com/VI/only-in-leonida • 26/10/2026')
add('A minha leitura desse percurso',pic('Leonida Keys',1),label='LEITURA DO CANAL')
v('mas continuou perto',28,label='DESEJO E TRAJETÓRIA')
add('Isso dá outro sabor',J(3),label='O DESEJO DE SOSSEGO')
add('Saber construir uma vida tranquila',J(6),label='QUERER / CONSTRUIR')
add('É uma contradição fácil de reconhecer',J(4),label='LEITURA DO CANAL',title='Desejo ≠ escolha',graphic='headline',side='right')
v('mas aceita justamente',29,label='A OPORTUNIDADE COMPLICA')
add('No caso de Jason',J(2),label='JASON DUVAL')
add('Ainda assim reduzir',J(8),label='UMA HISTÓRIA EM ABERTO')
add('A questão interessante',J(3),label='O QUE ELE VAI ESCOLHER?')
add('Lucia chega a essa conversa',L(9),label='02 / O RECOMEÇO DE LUCIA')
add('Sua apresentação liga a prisão',L(5),label='APRESENTAÇÃO OFICIAL',source='rockstargames.com/VI/only-in-leonida • 26/10/2026')
v('e destaca a determinação',63,label='UMA NOVA OPORTUNIDADE')
add('Isso faz a ideia de recomeço',L(1),label='RECOMEÇO')
add('Para alguém que já perdeu',L(5),label='O PESO DA LIBERDADE')
add('E o medo de perder',L(10),label='O CUSTO DE UMA ESCOLHA')
v('Repare como muda a pergunta',112,label='O QUE ELA QUER PROTEGER?')
add('eu quero observar',L(9),label='LEITURA DO CANAL')
add('Dinheiro Autonomia Um futuro compartilhado',L(2),label='POSSIBILIDADES DE LEITURA',title='Dinheiro? Autonomia?\nUm futuro juntos?',graphic='questions',side='right')
add('Elas ajudam a enxergar',L(3),label='UMA PESSOA FAZENDO ESCOLHAS')
add('em vez de transformar',L(10),label='ALÉM DA FICHA DO PERSONAGEM')
add('GTA já tem polícia',C(6),label='ANTECEDENTES NÃO CONTAM TUDO')
add('Juntando os dois',C(3),label='03 / DOIS CAMINHOS',title='O mesmo futuro.',sub='Critérios diferentes para chegar lá',graphic='headline',side='right')
add('Jason pode associar',J(3),label='LEITURA DO CANAL',title='Menos complicação',graphic='headline',side='right')
add('Lucia pode associá-la',L(9),label='LEITURA DO CANAL',title='Assumir o controle',graphic='headline',side='right')
add('Esses desejos podem se completar',C(1),label='PARCERIA')
add('Mas o que acontece',C(11),label='QUANDO É PRECISO ESCOLHER')
add('Imagine este exemplo',label='EXEMPLO HIPOTÉTICO',title='Uma oportunidade.',sub='Recompensa e risco na mesma decisão',graphic='dilemma',stage=0)
add('Uma pessoa enxerga',label='EXEMPLO HIPOTÉTICO',title='A chance de parar.',sub='O mesmo futuro pode sugerir caminhos opostos',graphic='dilemma',stage=1)
add('A outra vê o risco',label='EXEMPLO HIPOTÉTICO',title='O medo de perder.',sub='O mesmo futuro pode sugerir caminhos opostos',graphic='dilemma',stage=2)
add('Mesmo assim podem discordar',label='EXEMPLO HIPOTÉTICO',title='Qual é o próximo passo?',sub='Objetivo em comum ≠ decisão em comum',graphic='dilemma',stage=3)
add('Não é uma cena anunciada',label='EXEMPLO HIPOTÉTICO',title='Um dilema de confiança.',sub='Exemplo criado para explicar a análise',graphic='dilemma',stage=4)
add('E a premissa oficial',C(12),label='04 / A PRESSÃO EXTERNA')
add('um golpe dá errado',C(4),label='PREMISSA OFICIAL',title='O golpe dá errado.',graphic='headline',side='right',source='rockstargames.com/VI • sinopse • 26/10/2026')
add('numa conspiração criminosa',C(8),label='PREMISSA OFICIAL',title='O conflito se amplia.',graphic='headline',side='right')
add('e precisa depender ainda',C(11),label='SOBREVIVÊNCIA')
v('Aqui o problema muda',105,label='AS OPÇÕES DIMINUEM')
add('É preciso reagir',C(9),label='PRESSÃO EXTERNA')
add('Sob essa pressão',C(3),label='05 / CONFIANÇA',title='Confiar tem um custo.',graphic='headline',side='right')
add('aceitar uma decisão do outro',C(6),label='DECISÕES + CONSEQUÊNCIAS')
v('É esse problema',79,label='RELAÇÃO SOB PRESSÃO')
add('E o material oficial',C(13),label='UMA IMAGEM, DOIS SENTIDOS',zoom=[1.2,1.22],focus=[.5,.36])
add('Falando em fotografia',C(13),label='06 / ANÁLISE DA IMAGEM',zoom=[1,1],source='Rockstar Games • Jason_and_Lucia_13.jpg')
add('Jason e Lucia aparecem abraçados',C(13),label='OBSERVAÇÃO VISUAL',graphic='focus',focusType='couple',zoom=[1,1])
add('Ao fundo há embarcações',C(13),label='OBSERVAÇÃO VISUAL',graphic='focus',focusType='boats',zoom=[1,1])
add('O centro da imagem',C(13),label='INTIMIDADE NO CENTRO',zoom=[1,1.04],focus=[.48,.38])
add('O entorno faz o perigo',C(13),label='PERIGO NO ENTORNO',graphic='focus',focusType='surround',zoom=[1,1])
add('É um contraste que você entende',C(13),label='A FORÇA DA COMPOSIÇÃO',zoom=[1,1])
add('O que me chama atenção',C(13),label='LEITURA VISUAL DO CANAL',zoom=[1,1])
add('Primeiro vemos a intimidade',C(13),label='01 / INTIMIDADE',graphic='focus',focusType='couple',zoom=[1,1])
add('Depois percebemos o cerco',C(13),label='02 / CERCO',graphic='focus',focusType='surround',zoom=[1,1])
add('A composição faz a relação',C(13),label='PROTEÇÃO / CENÁRIO HOSTIL',zoom=[1,1.06],focus=[.49,.42])
add('Essa é a nossa leitura visual',C(13),label='INTERPRETAÇÃO DA COMPOSIÇÃO',zoom=[1.06,1],focus=[.49,.42])
add('Mas ela dá uma forma',C(13),label='UM FUTURO PARA DOIS?',zoom=[1,1])
add('Então quando uma nova conversa',C(3),label='07 / COMO ACOMPANHAR A DUPLA')
add('vale prestar atenção',C(11),label='TRÊS PISTAS',title='Quem propõe?\nQuem hesita?\nO que teme perder?',graphic='checklist',side='right')
add('Uma hesitação pode revelar',L(10),label='HESITAR TAMBÉM DIZ ALGO')
v('Uma concordância pode custar',79,label='CONCORDÂNCIA TEM UM CUSTO')
add('O interesse está nessa diferença',C(1),label='ACEITAR / QUERER')
add('É aí que um casal',C(3),label='ALÉM DO MESMO PERCURSO')
add('Por isso a pergunta',C(13),label='08 / A PERGUNTA QUE FICA',zoom=[1,1.03])
add('Jason e Lucia conseguem construir',C(1),label='UM FUTURO EM COMUM',title='Faz sentido\npara os dois?',graphic='headline',side='right')
add('Os passados dão motivos',J(2),label='PASSADO → MUDANÇA')
add('O golpe coloca essa mudança',C(8),label='MUDANÇA SOB PRESSÃO')
add('E o vínculo entre eles',C(3),label='DECISÕES QUE AFETAM O OUTRO')
add('A história fica interessante',C(13),label='A RESPOSTA AINDA ESTÁ EM ABERTO',zoom=[1,1.025])
add('Qual diferença você acha',C(1),label='PARTICIPE DO DOSSIÊ',title='Risco ou projeto de vida?',graphic='headline',side='right')
add('a disposição para correr riscos',C(11),label='QUAL DIFERENÇA PESA MAIS?')
add('Conta o motivo nos comentários',C(3),label='CONTA O MOTIVO NOS COMENTÁRIOS')
add('Aqui no Pixel Procurado',C(13),label='PIXEL PROCURADO',title='Cada escolha\nrevela alguém.',sub='Inscreva-se para acompanhar os próximos dossiês',graphic='headline',side='right')
# Inserts chosen from inspected source contact sheets; no source audio is used.
video_inserts={2:('Trailer_2',145),13:('Trailer_2',19),14:('An_Extended_Look',50),15:('Launch_Trailer',28),20:('Trailer_1',9),21:('Launch_Trailer',68),27:('Launch_Trailer',54),32:('Launch_Trailer',41),38:('An_Extended_Look',24),41:('Trailer_1',69),45:('Launch_Trailer',43),46:('Trailer_1',74),60:('An_Extended_Look',27),63:('Launch_Trailer',39),65:('An_Extended_Look',10),70:('Trailer_2',79)}
for i,(name,offset) in video_inserts.items():
    shots[i].update(file=f'GTAVI_{name}.mp4',offset=offset)
for i,s in enumerate(shots):
    end=shots[i+1]['start'] if i+1<len(shots) else math.ceil(duration*fps)/fps
    s.update(end=end,frames=round(end*fps)-round(s['start']*fps),fromFrame=round(s['start']*fps),motion=i%4)
    assert s['frames']>0,s
    s['kind']='graphic' if not s['file'] else 'video' if s['file'].endswith('.mp4') else 'image'
    if s['file']:
        source=ROOT/'videosGTAVI'/s['file']; assert source.is_file(),source
        if s['kind']=='video':
            with av.open(str(source)) as c: assert s['offset']+s['frames']/fps<=c.duration/1e6
    s['animate']=bool(s['graphic'])
    s['animationFrames']=25 if s['animate'] else 1
    if s['graphic']=='questions':
        s['cues']=[0,round((at('Autonomia Um futuro')-s['start'])*fps),round((at('Um futuro compartilhado')-s['start'])*fps)]
        s['animationFrames']=max(s['cues'])+25
    if s['graphic']=='checklist':
        s['cues']=[round((at('quem propõe')-s['start'])*fps),round((at('quem hesita')-s['start'])*fps),round((at('o que cada um teme perder')-s['start'])*fps)]
        s['animationFrames']=max(s['cues'])+25
    if s['graphic']=='focus' and s.get('focusType')=='boats':
        s['heliCue']=round((at('e um helicóptero')-s['start'])*fps)
        s['animationFrames']=s['heliCue']+25
    s['animationFrames']=min(s['frames'],s['animationFrames'])
caps=[];batch=[]
for i,w in enumerate(words):
    batch.append(w)
    pause=i+1==len(words) or words[i+1]['start']-w['end']>.65
    if len(' '.join(x['word'] for x in batch))>=44 or len(batch)>=8 or w['word'].endswith(('.', '?','!',';',':')) or (len(batch)>=3 and pause):
        caps.append(dict(start=batch[0]['start'],end=min(duration,w['end']+.1),text=' '.join(x['word'] for x in batch)));batch=[]
if batch:caps.append(dict(start=batch[0]['start'],end=min(duration,batch[-1]['end']+.12),text=' '.join(x['word'] for x in batch)))
for a,bcap in zip(caps,caps[1:]):a['end']=min(max(a['end'],a['start']+.85),bcap['start'])
assert all(c['end']>c['start'] for c in caps)
ps=[];idx=0
for i,p in enumerate(paragraphs):
    ps.append(dict(paragraph=i+1,start=words[idx]['start'],text=p));idx+=len(p.split())
data=dict(episode='L02',title='Jason e Lucia: eles querem a mesma vida?',duration=duration,frames=math.ceil(duration*fps),fps=fps,voice='producao/L02/voz/narracao_normalizada.wav',shots=shots,captions=caps,paragraphs=ps)
assert sum(s['frames'] for s in shots)==data['frames']
(WORK/'edicao_l02.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(duration=duration,shots=len(shots),captions=len(caps),animated=sum(s['animate'] for s in shots)),ensure_ascii=False))
for s in shots: print(f'{s["start"]:6.2f} {s["end"]:6.2f} {s["kind"]:7} {s["anchor"]}')
