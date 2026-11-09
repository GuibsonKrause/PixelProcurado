import json, math, os, re, sys, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.course-tools'),str(ROOT/'.production-tools/python')]
import av
PUBLIC=ROOT/'remotion/public/l01'
PUBLIC.mkdir(parents=True,exist_ok=True)
BANK=ROOT/'videosGTAVI'
VOICE=ROOT/'producao/L01/voz/gemini/narracao_guibson2_normalizada.wav'
with av.open(str(VOICE)) as c: duration=c.duration/1e6
# Explicit editorial decisions, keyed to narration time, not randomly selected B-roll.
shots=[]
def add(t,file,offset=0,label='',title='',sub=''):
    shots.append(dict(start=t,file=file,offset=offset,label=label,title=title,sub=sub))
def pic(t,who,n,label='',title='',sub=''):
    group='People' if who in ['Jason and Lucia','Jason Duval','Lucia Caminos','Brian Heder','Cal Hampton'] else 'Places'
    add(t,f'GTAVI_Screenshots/{group}/{who}/{who.replace(" ","_")}_{n:02}.jpg',label=label,title=title,sub=sub)
def vid(t,which,offset,label='',title='',sub=''):
    add(t,f'GTAVI_{which}.mp4',offset,label,title,sub)
vid(0,'Launch_Trailer',44,'DOSSIÊ 01','GTA VI','O que foi confirmado?')
vid(3.5,'Trailer_2',34)
pic(6.8,'Jason and Lucia',4)
vid(10,'Trailer_1',44,'TRAILER 1')
pic(14,'Jason and Lucia',1,'A PERGUNTA','O que é oficial?')
pic(19,'Jason Duval',2,'JASON DUVAL')
pic(22,'Lucia Caminos',10,'LUCIA CAMINOS')
pic(25,'Vice City',10,'LEONIDA')
pic(29,'Mount Kalaga National Park',4,'IMAGEM ≠ CONCLUSÃO')
add(32,'GTAVI_Artwork_Wallpapers/Official_Cover_Art/Official_Cover_Art_landscape.jpg',label='PIXEL PROCURADO',title='A pista vem\ncom a fonte.',sub='DOSSIÊ 01 / GTA VI')
pic(37,'Vice City',11,'CHECAGEM DO EPISÓDIO','23 OUT 2026','Fontes na descrição')
vid(43,'Launch_Trailer',10,'DOSSIÊ 01')
pic(48,'Vice City',10,'ANÚNCIO CITADO','19 NOV 2026','PlayStation 5 • Xbox Series X|S')
pic(55,'Jason and Lucia',3,'PLATAFORMAS','PS5  /  XBOX SERIES X|S')
pic(61,'Vice City',3,'EM ABERTO','E no PC?','A lista de consoles não estabelece uma data para PC')
vid(68,'Trailer_2',30,'ANÁLISE')
pic(73,'Vice City',8,'HIPÓTESE','Previsão ≠ anúncio')
pic(78,'Jason and Lucia',11,'EVIDÊNCIA','Um dia confirmado exige um anúncio')
pic(83,'Jason Duval',4,'EXPECTATIVA','“Acredito que venha depois”')
pic(88,'Jason and Lucia',3,'AFIRMAÇÃO','“A Rockstar anunciou”','Esta frase precisa de uma fonte')
vid(94,'Launch_Trailer',43,'FONTE + CONTEXTO')
pic(101,'Jason and Lucia',8,'02 / HISTÓRIA','Um golpe dá errado')
pic(106,'Jason and Lucia',4,'PREMISSA')
pic(111,'Jason and Lucia',12,'JASON + LUCIA')
vid(116,'Trailer_2',79,'PARCERIA SOB PRESSÃO')
pic(122,'Jason and Lucia',13,'ANÁLISE','Em quem confiar?')
pic(128,'Jason and Lucia',5,'LEITURA DA PREMISSA')
pic(134,'Jason and Lucia',6,'TENSÃO')
pic(139,'Jason and Lucia',1,'ANÁLISE','Tensão não prova traição')
vid(145,'Launch_Trailer',39,'DEPENDÊNCIA')
pic(150,'Jason and Lucia',11,'O QUE CADA UM ESPERA?')
pic(155,'Jason Duval',2,'03 / PERSONAGENS')
pic(159,'Jason Duval',1,'JASON DUVAL','Passado militar')
pic(163,'Leonida Keys',1,'LEONIDA KEYS')
pic(166,'Lucia Caminos',5,'LUCIA CAMINOS','Penitenciária de Leonida')
pic(171,'Lucia Caminos',9,'APRESENTAÇÕES DOS PERSONAGENS')
pic(176,'Jason and Lucia',3,'ANÁLISE','Bagagens diferentes')
pic(182,'Jason and Lucia',11,'PARCERIA')
pic(187,'Jason and Lucia',6,'QUEM DECIDE?')
pic(192,'Jason and Lucia',5,'INTERESSES EM CONFLITO?')
pic(197,'Jason and Lucia',13,'PERGUNTAS PARA ACOMPANHAR')
vid(202,'An_Extended_Look',390,'BIOGRAFIA ≠ MECÂNICA')
vid(208,'An_Extended_Look',500,'EVIDÊNCIAS DIFERENTES')
pic(213,'Vice City',10,'04 / LEONIDA')
pic(217,'Vice City',1,'VICE CITY')
pic(221.8,'Leonida Keys',1,'LEONIDA KEYS')
pic(223,'Grassrivers',5,'GRASSRIVERS')
pic(224,'Port Gellhorn',6,'PORT GELLHORN')
pic(225,'Ambrosia',4,'AMBROSIA')
pic(226,'Mount Kalaga National Park',4,'MOUNT KALAGA')
pic(228,'Leonida Keys',4,'UM MUNDO PARA INVESTIGAR')
pic(233,'Mount Kalaga National Park',6,'EXPLORAÇÃO')
pic(238,'Vice City',10,'EM ABERTO','Paisagem não é régua')
pic(243,'Mount Kalaga National Park',4,'TAMANHO • DISTÂNCIA • TRAVESSIA')
pic(248,'Vice City',11,'EDIFÍCIOS','Uma fachada não comprova acesso')
vid(253,'An_Extended_Look',1310,'DEMONSTRAÇÃO COM CONTEXTO')
pic(259,'Port Gellhorn',1,'GUARDE A PERGUNTA')
pic(265,'Vice City',3,'MOSTRADO / IMAGINADO')
vid(271,'Launch_Trailer',10,'05 / FONTES','Confira a idade da informação')
vid(276,'Launch_Trailer',44,'LAUNCH TRAILER')
vid(280,'An_Extended_Look',500,'AN EXTENDED LOOK')
vid(284,'Trailer_1',18,'TRAILER 1')
vid(288,'Trailer_2',35,'TRAILER 2')
vid(292,'An_Extended_Look',840,'QUAL É O CONTEXTO?')
vid(298,'An_Extended_Look',860,'RECORTE ≠ TESTE COMPLETO','Uma cena não mede uma sessão')
pic(304,'Jason and Lucia',3,'ANTES + DEPOIS')
vid(309,'Trailer_2',79,'CENA COM CONTEXTO')
pic(315,'Vice City',10,'06 / O FILTRO','Três perguntas')
pic(322,'Vice City',11,'01 / ORIGEM','Quem publicou?','Fonte oficial • Veículo identificado • Origem desconhecida')
pic(330,'Jason Duval',4,'02 / AFIRMAÇÃO','O que foi dito?','Abra o link. Leia a afirmação completa.')
pic(337,'Vice City',3,'03 / CONCLUSÃO','A evidência sustenta?')
pic(342,'Vice City',11,'EXEMPLO HIPOTÉTICO','Um prédio aparece…')
pic(346,'Vice City',10,'SALTO LÓGICO','…todos serão acessíveis?','Imagem de um prédio ≠ promessa sobre todos')
pic(352,'Vice City',3,'EXEMPLO DE RACIOCÍNIO')
pic(358,'Jason and Lucia',1,'O FILTRO VALE PARA NÓS')
pic(363,'Jason and Lucia',13,'INTERPRETAÇÃO','Uma possibilidade, não um fato')
vid(369,'Trailer_2',79,'ACOMPANHE O ARGUMENTO')
pic(375,'Vice City',10,'07 / RECAPITULAÇÃO','O que fica do dossiê?')
pic(378,'Jason and Lucia',3,'DATA + PLATAFORMAS','19 NOV 2026','PS5 • Xbox Series X|S')
pic(381,'Jason and Lucia',12,'JASON + LUCIA')
pic(385,'Leonida Keys',1,'LUGARES DE LEONIDA')
pic(390,'Grassrivers',3,'TEORIAS FAZEM PARTE')
pic(395,'Jason and Lucia',5,'ANÁLISE')
pic(400,'Vice City',8,'INFORMAÇÃO ≠ HIPÓTESE')
pic(405,'Jason and Lucia',1,'PRÓXIMO DOSSIÊ','Personagens?','A relação entre Jason e Lucia')
pic(410,'Mount Kalaga National Park',4,'OU…','Lugares?','Os destinos de Leonida')
pic(414,'Jason and Lucia',3,'PARTICIPE','PERSONAGENS  /  LUGARES','Escreva sua escolha nos comentários')
add(420,'GTAVI_Artwork_Wallpapers/Official_Cover_Art/Official_Cover_Art_landscape.jpg',label='PIXEL PROCURADO',title='A pista vem\ncom a fonte.',sub='Inscreva-se • Fontes na descrição')
for i,s in enumerate(shots):
    s['end']=shots[i+1]['start'] if i+1<len(shots) else duration
    source=BANK/s['file']; assert source.is_file(),source
    dest=PUBLIC/source.name
    if not dest.exists():
        os.link(source,dest)
    s['src']='l01/'+dest.name
    s['kind']='video' if source.suffix=='.mp4' else 'image'
    s['frames']=round(s['end']*30)-round(s['start']*30)
    s['from']=round(s['start']*30)
    s['motion']=i%4
    assert s['frames']>0
dest=PUBLIC/'narracao.wav'
if not dest.exists(): shutil.copy2(VOICE,dest)
words=json.loads((VOICE.parent/'narracao_guibson2_palavras.json').read_text(encoding='utf8'))
fix={'Lúcia':'Lucia','Lúcia.':'Lucia.','quies,':'Keys,','quies':'Keys','Jellhorn,':'Gellhorn,','Malt':'Mount','Calaga.':'Kalaga.','sede.':'cede.','dossier?':'dossiê?','dossier,':'dossiê,','Atenção':'A tensão'}
for w in words:
    w['word']=fix.get(w['word'],w['word'])
    if 219<=w['start']<220: w['word']={'vai':'Vice','Siri':'City'}.get(w['word'],w['word'])
    if 182<=w['start']<185 and w['word']=='sim,':w['word']='assim,'
    if 17<=w['start']<19:w['word']={'e':'esse','se':'','quebra':'quebra-','a':'','cabeça.':'cabeça.'}.get(w['word'],w['word'])
words=[w for w in words if w['word']]
caps=[]; batch=[]
for i,w in enumerate(words):
    batch.append(w)
    size=len(' '.join(x['word'] for x in batch))
    pause=i+1==len(words) or words[i+1]['start']-w['end']>.4
    if size>=36 or len(batch)>=7 or (len(batch)>=3 and (w['word'].endswith(('.', '?','!')) or pause)):
        caps.append({'start':batch[0]['start'],'end':w['end']+.12,'words':batch});batch=[]
if batch:caps.append({'start':batch[0]['start'],'end':batch[-1]['end']+.12,'words':batch})
for a,b in zip(caps,caps[1:]):a['end']=min(a['end'],b['start'])
data={'duration':duration,'frames':math.ceil(duration*30),'shots':shots,'captions':caps}
out=ROOT/'remotion/src/edicao.json';out.write_text(json.dumps(data,ensure_ascii=False),encoding='utf8')
project=ROOT/'producao/L01/projeto/edicao_final_4k.json';project.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'shots':len(shots),'captions':len(caps),'duration':duration,'frames':data['frames']}))
