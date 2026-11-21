"""Editorial choices for the 14 Shorts. Anchors refer to the unchanged narration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'videosGTAVI'
def pic(group, who, n):
    return f'videosGTAVI/GTAVI_Screenshots/{group}/{who}/{who.replace(" ", "_")}_{n:02}.jpg'
J=lambda n:pic('People','Jason Duval',n)
L=lambda n:pic('People','Lucia Caminos',n)
C=lambda n:pic('People','Jason and Lucia',n)
B=lambda n:pic('People','Brian Heder',n)
R=lambda n:pic('People','Raul Bautista',n)
V=lambda n:pic('Places','Vice City',n)
K=lambda n:pic('Places','Leonida Keys',n)
G=lambda n:pic('Places','Grassrivers',n)
D=lambda n:pic('People','Real Dimez',n)
ART='videosGTAVI/GTAVI_Artwork_Wallpapers/Jason_and_Lucia_01/Jason_and_Lucia_01_landscape.jpg'
OLD='producao/shorts/_acervo/Vice_City_classico.jpg'
CHEETAH='producao/shorts/_acervo/GTA_V_Cheetah_2012.jpg'
T1='videosGTAVI/GTAVI_Trailer_1.mp4'
T2='videosGTAVI/GTAVI_Trailer_2.mp4'
TL='videosGTAVI/GTAVI_Launch_Trailer.mp4'
TV='videosGTAVI/GTA-B02-001_P001 - 00-00-00 a 00-04-50 - 1280x720 [N-xHcvug3WI].mp4'

def shot(anchor, file='', title='', label='LEITURA DO CANAL', mode='panel', offset=0, **kw):
    return dict(anchor=anchor,file=file,title=title,label=label,mode=mode,offset=offset,**kw)
def graph(anchor,title,items,label='ANÁLISE',**kw):
    return shot(anchor,title=title,label=label,mode='graphic',items=items,**kw)
def vid(anchor,file,offset,title='',label='GTA VI • TRAILER',**kw):
    return shot(anchor,file,title,label,offset=offset,**kw)

PLANS = {
'C01':[
 graph(None,'DATA CERTA.\nVERSÃO ERRADA?',['DATA','PLATAFORMA?'],'GTA VI • CONFIRA A FONTE',hook=True),
 shot('Basta ela aparecer',V(1),'FALTA UMA PEÇA.','GTA VI • IMAGEM DE APOIO'),
 graph('Você vê um dia','O RECORTE ENGANA',['DIA','JOGO','E A VERSÃO?']),
 graph('Aqui está a primeira armadilha','LEIA O ANÚNCIO INTEIRO',['LANÇAMENTO','PLATAFORMAS'],'COMO CONFERIR'),
 shot('Se a página cita',ART,'A LISTA FAZ PARTE.','ARTWORK • NÃO É ANÚNCIO DE VERSÃO'),
 graph('Recortar só a data','A PROMESSA CRESCE',['DATA ISOLADA','CONTEXTO PERDIDO']),
 vid('Mas encontrar o logo',T2,31,'CAPTURA ≠ CALENDÁRIO'),
 graph('Um trailer capturado','O QUE A CAPTURA INFORMA',['ONDE O VÍDEO FOI CAPTURADO'],'CRITÉRIO DE CHECAGEM'),
 graph('Isso sozinho','O QUE ELA NÃO RESOLVE',['EXCLUSIVIDADE?','TODAS AS VERSÕES?']),
 graph('Agora vem o teste','TRÊS PEÇAS JUNTAS',['FONTE','DATA','PLATAFORMA'],'COMO CONFERIR'),
 shot('Para uma versão de PC',V(3),'PC: PROCURE O ANÚNCIO.','GTA VI • IMAGEM DE APOIO'),
 graph('O erro pode estar','A ASSOCIAÇÃO IMPORTA',['DATA + VERSÃO + FONTE']),
 graph('É assim que','DATA CERTA.\nVERSÃO ERRADA?',['DATA','PLATAFORMA?'],'GTA VI • CONFIRA A FONTE',hook=True)],
'C02':[
 shot(None,C(1),'O MESMO SONHO.\nOUTRA ESCOLHA.','JASON + LUCIA',hook=True,crop=[.12,.05,.55,.9]),
 shot('O contraste está',J(2),'VIDA FÁCIL.','JASON • PERFIL OFICIAL'),
 shot('Lucia tem um plano',L(9),'UM PLANO.','LUCIA • PERFIL OFICIAL'),
 graph('Parece uma combinação','DESTINO ≠ CAMINHO',['O QUE QUEREM','COMO CHEGAR LÁ']),
 graph('Mas imagine','UMA OPORTUNIDADE',['DINHEIRO','RISCO'],'EXEMPLO HIPOTÉTICO'),
 graph('Quem procura sossego','RECUAR OU AVANÇAR?',['SOSSEGO → RECUAR','CONTROLE → AVANÇAR'],'EXEMPLO HIPOTÉTICO'),
 shot('Só que a premissa',C(12),'O PLANO SAI DO CONTROLE.','PREMISSA • GTA VI'),
 vid('o problema cresce',T2,121,'PRESSÃO DOS DOIS LADOS.',motion=2),
 shot('Nesse cenário',C(11),'UMA ESCOLHA. DOIS CUSTOS.','ANÁLISE DA PARCERIA'),
 graph('Agora repare','OBSERVE AS DECISÕES',['QUEM PROPÕE?','QUEM HESITA?','O QUE TEME PERDER?']),
 shot('Essa é a minha leitura',C(3),'UMA LEITURA, NÃO UM FINAL.','ANÁLISE'),
 shot('Gostar de alguém',C(13),'AFETO NÃO ALINHA TUDO.','ANÁLISE'),
 shot('A tensão começa',J(2),'A CHANCE DE UM.\nO MEDO DO OUTRO.','ANÁLISE'),
 shot('Por isso',C(1),'O MESMO SONHO.\nOUTRA ESCOLHA.','JASON + LUCIA',hook=True,crop=[.12,.05,.55,.9])],
'C03':[
 shot(None,C(13),'OLHE ATRÁS\nDO ABRAÇO.','UMA IMAGEM • DUAS HISTÓRIAS',hook=True,crop=[.25,0,.5,1]),
 shot('Nessa imagem oficial',C(13),'O OLHAR ENCONTRA O CASAL.','JASON + LUCIA',crop=[.25,0,.5,1]),
 shot('e o sol aparece',C(13),'INTIMIDADE NO CENTRO.','ANÁLISE VISUAL',crop=[.34,.15,.32,.45]),
 shot('Se você recorta',C(13),'O RECORTE MUDA A LEITURA.','RECORTE EDITORIAL',crop=[.25,0,.5,1]),
 shot('Mas abra a imagem',C(13),'AGORA VEJA O FUNDO.','QUADRO INTEIRO',ring=[.72,.01,.25,.3]),
 shot('embarcações policiais',C(13),'POLÍCIA NAS BORDAS.','DETALHE DA MESMA IMAGEM',ring=[.01,.46,.24,.49]),
 shot('Quem mudou foi você',C(13),'A IMAGEM É A MESMA.','ANÁLISE VISUAL'),
 shot('Só que existe um truque',C(13),'O PERIGO FICA NAS BORDAS.','COMPOSIÇÃO',ring=[.75,.36,.25,.55]),
 shot('Meu olhar volta',C(13),'O FUNDO NÃO DESAPARECE.','ANÁLISE VISUAL',crop=[.25,0,.5,1]),
 shot('Agora faça a comparação',C(13),'PRIMEIRO, O RECORTE.','RECORTE EDITORIAL',crop=[.25,0,.5,1]),
 shot('depois o quadro inteiro',C(13),'DEPOIS, O CONTEXTO.','QUADRO INTEIRO'),
 vid('Essa leitura visual',T2,61,'O FINAL CONTINUA EM ABERTO.','GTA VI • IMAGEM DE APOIO'),
 shot('Para mim a força',C(13),'ABRIGO CERCADO DE PERIGO.','CONCLUSÃO VISUAL'),
 shot('Porque',C(13),'OLHE ATRÁS\nDO ABRAÇO.','UMA IMAGEM • DUAS HISTÓRIAS',hook=True,crop=[.25,0,.5,1])],
'C04':[
 shot(None,OLD,'DE QUAL ÉPOCA\nÉ A SAUDADE?','VICE CITY • IMAGEM DO CLÁSSICO',hook=True),
 graph('O jogo chegou','DOIS RELÓGIOS',['2002 • LANÇAMENTO','1986 • HISTÓRIA'],'VICE CITY CLÁSSICO'),
 shot('Você explorava',OLD,'O JOGO E A SUA VIDA.','VICE CITY • IMAGEM PROMOCIONAL'),
 vid('Mas essa mistura',T1,31,'A CIDADE QUE VOCÊ LEMBRA.',motion=3.3),
 shot('Recuperar a sensação',OLD,'A PRIMEIRA VEZ NÃO VOLTA.','LEITURA SOBRE NOSTALGIA'),
 shot('Só que uma imagem',D(2),'A PLATEIA VIROU CÂMERA.','REAL DIMEZ • SCREENSHOT',ring=[.02,.25,.2,.6]),
 shot('mas agora a própria multidão',D(2),'A VITRINE CABE NA MÃO.','DETALHE DA IMAGEM',crop=[0,.1,.5,.9]),
 vid('Agora o retorno',T1,31,'MESMA CIDADE. OUTRO OLHAR.',motion=3.3),
 shot('O que elas mostram',D(2),'PARA ONDE APONTAM?','REAL DIMEZ • SCREENSHOT'),
 shot('Na minha leitura',V(6),'A PERSONALIDADE PERMANECE?','LEITURA DO CANAL'),
 shot('Talvez você reconheça',OLD,'SAUDADE DE QUEM JOGAVA.','VICE CITY CLÁSSICO'),
 shot('Afinal',OLD,'DE QUAL ÉPOCA\nÉ A SAUDADE?','VICE CITY • IMAGEM DO CLÁSSICO',hook=True)],
'C05':[
 vid(None,T2,31,'TEM GAMEPLAY.\nMAS ONDE?','GTA VI • TRAILER 2',hook=True),
 graph('A descrição da Rockstar','A DESCRIÇÃO INFORMA',['GAMEPLAY','CENAS CINEMATOGRÁFICAS'],'TRAILER 2 • SÍNTESE DA DESCRIÇÃO'),
 graph('capturada dentro','CAPTURADO NO PS5',['DENTRO DO JOGO'],'DESCRIÇÃO DO TRAILER 2'),
 vid('O problema começa',T2,61,'CADA PLANO É OUTRA PERGUNTA.'),
 graph('Porque metade do conjunto','METADE ≠ ALTERNÂNCIA',['PROPORÇÃO DO VÍDEO','CLASSIFICAÇÃO DOS PLANOS']),
 vid('Não dá para escolher',T2,140,'CÂMERA BONITA NÃO RESPONDE.'),
 graph('A descrição informa','CONJUNTO ≠ CADA CENA',['UMA INFORMAÇÃO','DOIS NÍVEIS DE ANÁLISE']),
 vid('Mas o erro também',T2,79,'O CONTRÁRIO TAMBÉM VALE.'),
 graph('Para classificar','PROVA ESPECÍFICA',['ESTA CENA','ESTE CONTROLE']),
 graph('Agora separe','DUAS PERGUNTAS',['CAPTURADO ONDE?','CONTROLADO POR QUEM?']),
 vid('A mistura anunciada',T2,31,'HÁ GAMEPLAY. A DÚVIDA CONTINUA.'),
 graph('A conclusão cabe','O QUE VOCÊ CONTROLA?',['INVESTIGUE CADA CENA']),
 vid('Esse é o detalhe',T2,140,'TEM GAMEPLAY.\nMAS ONDE?','GTA VI • TRAILER 2',hook=True)],
'C06':[
 shot(None,ART,'OFICIAL.\nMAS É CAPTURA?','GTA VI • ARTWORK',hook=True),
 shot('Imagine ampliar',ART,'ZOOM NO ARQUIVO ERRADO.','ARTWORK • RECORTE',crop=[.25,.15,.42,.55]),
 graph('Só falta conferir','ANTES DE COMPARAR',['QUE TIPO DE IMAGEM É?']),
 graph('Aqui está a virada','DUAS CATEGORIAS',['SCREENSHOTS','ARTWORK & WALLPAPERS'],'BIBLIOTECA OFICIAL'),
 shot('A ilustração de Jason',ART,'ARTE OFICIAL.','ARTWORK'),
 shot('Ser oficial',C(1),'CAPTURA OFICIAL.','SCREENSHOT'),
 graph('Mas por que isso','CADA MATERIAL RESPONDE',['ARTE → IDENTIDADE','CAPTURA → QUADRO DO JOGO']),
 shot('A arte ajuda',ART,'CORES E APRESENTAÇÃO.','ARTWORK'),
 shot('Uma captura permite',C(1),'O QUADRO DIVULGADO.','SCREENSHOT'),
 shot('Agora pense',ART,'O RECORTE APAGA A ORIGEM.','ARTWORK • RECORTE',crop=[.25,.15,.42,.55]),
 graph('O espectador pode','A LEGENDA MUDA A LEITURA',['ORIGEM','CATEGORIA','COMPARAÇÃO']),
 shot('Antes do zoom',ART,'MOSTRE A CATEGORIA.','ARTWORK'),
 vid('sem transformar um único quadro',T2,31,'UM QUADRO NÃO É UM TESTE.','GTA VI • TRAILER 2'),
 shot('É por isso que',ART,'OFICIAL.\nMAS É CAPTURA?','GTA VI • ARTWORK',hook=True)],
'C07':[
 shot(None,V(9),'O CARRO\nNÃO É TUDO.','GTA VI • OLHE AO REDOR',hook=True,crop=[.36,.42,.4,.48]),
 shot('O azul chama atenção',V(9),'MOTOS. PESSOAS. MURAIS.','GTA VI • QUADRO INTEIRO'),
 shot('Se você amplia',V(9),'O RECORTE ELIMINA O BAIRRO.','RECORTE EDITORIAL',crop=[.36,.42,.4,.48]),
 shot('Agora compare',CHEETAH,'A MÁQUINA DOMINA.','GTA V • DIVULGAÇÃO DE 2012'),
 shot('O olhar encontra',CHEETAH,'UM FOCO PRINCIPAL.','GTA V • IMAGEM PROMOCIONAL'),
 graph('Mas cuidado','COMPOSIÇÃO, NÃO BENCHMARK',['DUAS IMAGENS','DOIS ENQUADRAMENTOS']),
 shot('Em uma o carro',CHEETAH,'O CARRO DOMINA.','GTA V • DIVULGAÇÃO DE 2012'),
 shot('Na outra',V(9),'O BAIRRO DISPUTA ATENÇÃO.','GTA VI • SCREENSHOT'),
 shot('Só que essa disputa',V(9),'CONTINUE OLHANDO.','DETALHES DO MESMO QUADRO',crop=[.01,.01,.46,.98]),
 shot('Depois quer olhar',V(9),'A CIDADE AO REDOR.','DETALHES DO MESMO QUADRO',crop=[.56,.04,.44,.96]),
 vid('O quadro oferece',T1,31,'OUTRAS COISAS PARA DESCOBRIR.','GTA VI • IMAGEM DE APOIO',motion=3.3),
 shot('Minha leitura',V(9),'UM CARRO. UM CONVITE.','GTA VI • QUADRO INTEIRO'),
 shot('Porque',V(9),'O CARRO\nNÃO É TUDO.','GTA VI • OLHE AO REDOR',hook=True,crop=[.36,.42,.4,.48])],
'C08':[
 shot(None,K(2),'A DONA\nDA RUA.','LEONIDA KEYS • GTA VI',hook=True,crop=[.05,.65,.38,.35]),
 shot('É uma iguana',K(2),'PEQUENA. IMPOSSÍVEL DE IGNORAR.','LEONIDA KEYS • QUADRO INTEIRO',ring=[.07,.71,.31,.18]),
 shot('O engraçado',K(2),'A ESCALA FAZ A PIADA.','ANÁLISE VISUAL'),
 graph('Mas esconda','EXERCÍCIO DE IMAGINAÇÃO',['PAISAGEM','PESSOAS','+ UM IMPREVISTO'],'EXEMPLO IMAGINADO'),
 shot('Quando você a coloca',K(2),'TEM ALGO NO CAMINHO.','A MESMA IMAGEM',ring=[.07,.71,.31,.18]),
 shot('O detalhe transforma',K(2),'UM MOMENTO PARA CONTAR.','DETALHE DO QUADRO',crop=[.05,.65,.38,.35]),
 graph('Só que a piada','A IMAGEM NÃO PROVA',['BLOQUEIO DE CARROS?','REAÇÃO AO JOGADOR?'],'LIMITES DA EVIDÊNCIA'),
 shot('O que temos',K(2),'ELA ESTÁ ALI.','LEONIDA KEYS • SCREENSHOT'),
 shot('Agora olhe de novo',K(2),'QUEM OCUPA A RUA?','ANÁLISE VISUAL'),
 shot('até o olhar pousar',K(2),'A ATENÇÃO MUDA DE DONO.','DETALHE DO QUADRO',crop=[.05,.65,.38,.35]),
 shot('É pequena no quadro',K(2),'PEQUENA NO QUADRO.\nENORME NA LEMBRANÇA.','ANÁLISE VISUAL'),
 vid('Você pode chegar',T2,6.8,'MAR, BARCOS...','GTA VI • AMBIENTAÇÃO DAS KEYS',motion=1.1),
 shot('Quem recebe',K(2),'A DONA\nDA RUA.','LEONIDA KEYS • GTA VI',hook=True,crop=[.05,.65,.38,.35])],
'C09':[
 shot(None,K(1),'VOCÊ VÊ TUDO.\nE QUEM VÊ VOCÊ?','LEONIDA • DUAS PAISAGENS',hook=True),
 shot('Essa é a sensação',G(3),'O QUE A MARGEM ESCONDE?','GRASSRIVERS • LEITURA VISUAL'),
 shot('Nas Keys',K(1),'HORIZONTE ABERTO.','LEONIDA KEYS'),
 vid('O olhar consegue',T1,36,'A VISTA VAI LONGE.','GTA VI • KEYS',motion=1.1),
 shot('Agora troque',G(3),'A VEGETAÇÃO FECHA O QUADRO.','GRASSRIVERS'),
 shot('Em vez de procurar',G(3),'OLHE PARA AS MARGENS.','GRASSRIVERS • MESMA IMAGEM',ring=[.05,.1,.3,.7]),
 graph('Mas repare','VISIBILIDADE TEM DOIS LADOS',['ABERTO → EXPOSIÇÃO','FECHADO → OCULTAÇÃO'],'LEITURA DAS IMAGENS'),
 shot('O corredor oferece',G(3),'MENOS VISÃO. MAIS MARGENS.','GRASSRIVERS'),
 shot('Nenhuma das duas',K(1),'A EXPECTATIVA VEM DO CENÁRIO.','LEONIDA KEYS'),
 graph('Só que isso','SENSAÇÃO ≠ MECÂNICA',['COMPOSIÇÃO VISUAL','NÃO É TESTE DE EMBOSCADA']),
 shot('A água permanece',G(3),'MUDA A FORMA DE OLHAR.','GRASSRIVERS'),
 shot('Se eu mostrar',K(1),'QUEM PODE ME VER?','LEONIDA KEYS'),
 shot('no outro',G(3),'O QUE EU NÃO VEJO?','GRASSRIVERS'),
 shot('É nesse sentido',K(1),'VOCÊ VÊ TUDO.\nE QUEM VÊ VOCÊ?','LEONIDA • DUAS PAISAGENS',hook=True)],
'C10':[
 graph(None,'SUA PLAYLIST.\nCOM LOCUTOR.',['MÚSICA','DJ'],'GTA V • SELF RADIO NO PC',hook=True,radio=True),
 graph('No PC o modo','MODO RADIO',['FAIXA PESSOAL','ANÚNCIO + DJ','PRÓXIMA FAIXA'],'SELF RADIO • PC',radio=True),
 vid('A função está descrita',TV,149,'SUA MÚSICA, DENTRO DA CIDADE.','GTA V • IMAGEM DE APOIO',motion=7),
 graph('Mas a parte interessante','QUANDO A MÚSICA PARA',['A EMISSORA CONTINUA'],'EXERCÍCIO AUDITIVO',radio=True),
 graph('Imagine dirigir','SÓ OS SEUS ARQUIVOS',['FAIXA 01','FAIXA 02'],'EXEMPLO IMAGINADO',radio=True),
 graph('Agora imagine essas mesmas','ENTRE UMA FAIXA E OUTRA',['MÚSICA','VOZES + ANÚNCIOS','MÚSICA'],'EXEMPLO IMAGINADO',radio=True),
 graph('Só que isso muda','O INTERVALO CRIA MUNDO',['OUTROS OUVINTES','OUTRAS HISTÓRIAS'],'LEITURA DO CANAL',radio=True),
 vid('Na minha leitura',TV,22,'A CIDADE EXISTE ALÉM DO CARRO.','GTA V • DIVULGAÇÃO HISTÓRICA'),
 graph('Agora pense','DUAS FORMAS DE OUVIR',['PLAYLIST EXTERNA','SELF RADIO'],'COMPARAÇÃO DE APRESENTAÇÃO',radio=True),
 graph('O detalhe não está','O QUE ACONTECE ENTRE FAIXAS',['MÚSICA → EMISSORA'],'LEITURA DO CANAL',radio=True),
 graph('O recurso descrito','GTA V • PC',['SELF RADIO','MODO RADIO'],'SUPORTE OFICIAL ROCKSTAR',radio=True),
 graph('E a graça é essa','A CIDADE ASSUME A TRANSMISSÃO',['SUA SELEÇÃO','A APRESENTAÇÃO DO MUNDO'],'LEITURA DO CANAL',radio=True),
 graph('Porque','SUA PLAYLIST.\nCOM LOCUTOR.',['MÚSICA','DJ'],'GTA V • SELF RADIO NO PC',hook=True,radio=True)],
'C11':[
 shot(None,B(4),'SEM ALUGUEL.\nCOM COBRANÇA.','JASON + BRIAN',hook=True),
 vid('Na apresentação oficial',T2,19,'UMA CASA. UMA CONTRAPARTIDA.','GTA VI • BRIAN E JASON'),
 graph('e ajuda nas cobranças','MORADIA ↔ SERVIÇOS',['BRIAN OFERECE','JASON RETRIBUI'],'SÍNTESE DO PERFIL OFICIAL'),
 shot('A facilidade e o compromisso',B(3),'O ACORDO VEM JUNTO.','BRIAN HEDER'),
 shot('Mas olha como',B(4),'MUDA A LEITURA DA RELAÇÃO.','ANÁLISE'),
 graph('Quando acrescenta','UMA VANTAGEM VIRA TROCA',['CASA','SERVIÇOS']),
 shot('O interesse deixa',J(2),'O QUE SUSTENTA O ACORDO?','JASON DUVAL'),
 graph('Só que uma troca','E SE PRECISAR RECUSAR?',['PEDIDO','TETO','ESCOLHA'],'EXEMPLO HIPOTÉTICO'),
 graph('A decisão envolve','MAIS QUE UMA TAREFA',['NECESSIDADE','COMPROMISSO'],'EXEMPLO HIPOTÉTICO'),
 graph('Agora a pergunta','QUEM PRECISA DE QUEM?',['QUEM OFERECE?','QUEM ENTREGA?','QUEM PERDE?']),
 shot('O perfil divulgado',B(4),'O ACORDO É O PONTO DE PARTIDA.','PERFIL OFICIAL + ANÁLISE'),
 shot('A minha leitura',J(2),'GRÁTIS NÃO É SEM COMPROMISSO.','LEITURA DO CANAL'),
 graph('O preço narrativo','O PREÇO DE DIZER NÃO',['FACILIDADE','LIBERDADE']),
 shot('Por isso o detalhe',B(4),'SEM ALUGUEL.\nCOM COBRANÇA.','JASON + BRIAN',hook=True)],
'C12':[
 shot(None,R(1),'VOCÊ CONFIARIA\nNESSE PLANO?','RAUL BAUTISTA',hook=True,mode='portrait',focus=.56),
 shot('Raul Bautista é apresentado',R(3),'EXPERIÊNCIA.','PERFIL OFICIAL • RAUL'),
 shot('mas seu perfil também',R(2),'RISCO CRESCENTE.','PERFIL OFICIAL • RAUL'),
 graph('As duas informações','AS DUAS COISAS JUNTAS',['HABILIDADE','RISCO']),
 graph('Mas existe uma diferença','EXECUTAR ≠ DESISTIR',['SABER FAZER','SABER PARAR']),
 shot('Um plano ruim',R(4),'COMPETÊNCIA NÃO É GARANTIA.','LEITURA DO PERFIL'),
 graph('Agora imagine','A MESMA PROPOSTA',['TAMANHO DO PRÊMIO','CUSTO DO ERRO'],'EXEMPLO HIPOTÉTICO'),
 graph('O exemplo é hipotético','ENTUSIASMO + RECEIO',['MESMO PLANO','EXPECTATIVAS DIFERENTES'],'EXEMPLO HIPOTÉTICO'),
 shot('Só que o teste',R(1),'O QUE FARIA ELE PARAR?','LEITURA DO CANAL'),
 graph('Ter uma resposta','UM LIMITE PARA O RISCO',['MUDAR DE IDEIA','TAMBÉM É UMA DECISÃO']),
 shot('Para mim a pergunta',R(3),'HABILIDADE + PRUDÊNCIA?','LEITURA DO CANAL'),
 vid('O currículo mostra','videosGTAVI/GTAVI_Videos/Raul_Bautista_Video_Clip.mp4',0,'QUANTO RISCO VOCÊ ACEITA?','GTA VI • RAUL • CLIPE OFICIAL',motion=1),
 shot('Sem fazer essa distinção',R(1),'VOCÊ CONFIARIA\nNESSE PLANO?','RAUL BAUTISTA',hook=True,mode='portrait',focus=.56)],
'L01-R02':[
 shot(None,C(12),'CONFIANÇA\nNÃO É SPOILER.','JASON + LUCIA',hook=True),
 shot('Na premissa',C(11),'PRECISAM UM DO OUTRO.','PREMISSA OFICIAL'),
 shot('Isso coloca confiança',C(13),'A RELAÇÃO SOB PRESSÃO.','LEITURA DO CANAL'),
 graph('Aqui acontece o salto','O SALTO DA TEORIA',['DEPENDÊNCIA','TRAIÇÃO?'],'HIPÓTESE ≠ CONCLUSÃO'),
 vid('É uma possibilidade',T2,61,'O FINAL NÃO ESTÁ AQUI.','GTA VI • IMAGEM DE APOIO'),
 graph('Mas dá para investigar','TROQUE A PERGUNTA',['O QUE CADA UM PODE PERDER?']),
 shot('Agora você tem um critério',L(10),'DECISÕES. HESITAÇÕES. CUSTOS.','ANÁLISE'),
 shot('Só que o cuidado',J(2),'A MONTAGEM TAMBÉM SUGERE.','EXEMPLO DE LEITURA • NÃO É SPOILER'),
 graph('O vídeo deve deixar claro','SEPARE AS CAMADAS',['INFORMAÇÃO','INTERPRETAÇÃO']),
 shot('A recompensa é conseguir',C(3),'CONFLITO SEM SPOILER FABRICADO.','LEITURA DO CANAL'),
 shot('O que ela não oferece',C(13),'NENHUM TRAIDOR REVELADO.','LEITURA DO CANAL'),
 shot('Porque',C(12),'CONFIANÇA\nNÃO É SPOILER.','JASON + LUCIA',hook=True)],
'L01-R03':[
 shot(None,V(11),'ESSA IMAGEM\nNÃO MEDE O MAPA.','GTA VI • EVIDÊNCIA VISUAL',hook=True),
 vid('Você olha uma imagem',T2,6.8,'DESTINOS DIFERENTES.','GTA VI • IMAGEM DE APOIO',motion=1.1),
 shot('quanto mais lugares',K(1),'E AS DISTÂNCIAS?','LEONIDA KEYS'),
 graph('Só que uma lista','LISTA ≠ ESCALA',['LUGARES','DISTÂNCIAS?']),
 shot('Mas o problema começa',V(11),'ONDE TERMINA O QUADRO?','VICE CITY • SCREENSHOT'),
 graph('Completar essa parte','IMAGINAR ≠ MEDIR',['TEORIA IDENTIFICADA','ESCALA COMPROVADA']),
 shot('Agora acrescente os prédios',V(10),'FACHADA NÃO CONFIRMA ENTRADA.','VICE CITY • SCREENSHOT'),
 shot('A mesma cena pode',V(3),'O QUE EXISTE ATRÁS DA PORTA?','VICE CITY • SCREENSHOT'),
 graph('Só que existe uma maneira','UMA PROVA PARA CADA PERGUNTA',['DISTÂNCIA → MEDIDA','ACESSO → DEMONSTRAÇÃO']),
 vid('Uma imagem bonita',T1,20,'BONITA NÃO SIGNIFICA COMPLETA.','GTA VI • TRAILER 1'),
 shot('O ganho é perceber',K(1),'REVELAÇÃO E EXPECTATIVA.','LEONIDA KEYS'),
 shot('Quando a promessa cresce',V(11),'ESSA IMAGEM\nNÃO MEDE O MAPA.','GTA VI • EVIDÊNCIA VISUAL',hook=True)]
}

META={
'C01':('GTA 6: a data pode estar certa… e a plataforma errada','Data e plataforma precisam pertencer ao mesmo anúncio. Veja como um recorte pode transformar informação verdadeira numa promessa errada.','Você confere a plataforma junto da data antes de compartilhar?','DATA CERTA. VERSÃO ERRADA?','L01'),
'C02':('Jason e Lucia: o mesmo sonho pode virar conflito em GTA 6','Uma vida melhor não significa escolher o mesmo caminho. A diferença entre sossego e controle muda a leitura dessa dupla.','Quem você acha que hesitaria primeiro diante de uma oportunidade arriscada?','O MESMO SONHO?','L02'),
'C03':('GTA 6: olhe atrás do abraço de Jason e Lucia','O casal chama atenção, mas o fundo transforma a imagem. Abra o quadro e veja como intimidade e perigo dividem a cena.','Você percebeu primeiro o casal ou a polícia no fundo?','OLHE ATRÁS DO ABRAÇO','L02'),
'C04':('Vice City: você sente saudade do jogo ou daquela época?','Vice City mistura a época da história com a época em que você jogou. O retorno em GTA 6 ganha outra leitura quando a plateia levanta o celular.','Sua lembrança mais forte é da cidade ou da fase da vida em que jogou?','DE QUAL ÉPOCA?','L03'),
'C05':('GTA 6 tem gameplay no Trailer 2. Mas quais cenas?','A descrição confirma gameplay e cenas cinematográficas no conjunto. Isso não identifica automaticamente o que o jogador controla em cada plano.','Qual trecho do Trailer 2 você gostaria de ver explicado com foco no controle?','TEM GAMEPLAY. MAS ONDE?','L04'),
'C06':('GTA 6: o erro de dar zoom na imagem errada','Oficial não significa screenshot. Veja por que confundir artwork com captura muda toda a comparação.','Você costuma conferir a categoria da imagem antes de comparar os detalhes?','OFICIAL. MAS É CAPTURA?','L04'),
'C07':('GTA V e GTA 6: o detalhe está ao redor do carro','O carro azul chama atenção, mas o bairro também conta uma história. Uma comparação de enquadramentos, sem transformar divulgação em benchmark.','Você prefere uma imagem que destaca o carro ou que convida a explorar o bairro?','OLHE AO REDOR','L05'),
'C08':('A dona da rua em GTA 6 é uma iguana','Um detalhe pequeno muda a lembrança de uma paisagem inteira. A iguana das Leonida Keys mostra como uma imagem ganha personalidade.','Qual detalhe pequeno faz um cenário de jogo ficar na sua memória?','A DONA DA RUA','L06'),
'C09':('GTA 6: a mesma água, duas sensações de perigo','Keys e Grassrivers mudam o que você consegue enxergar. Uma leitura visual sobre exposição e ocultação, sem presumir mecânicas do jogo.','Primeira parada: horizonte aberto das Keys ou margens de Grassrivers?','QUEM VÊ VOCÊ?','L06'),
'C10':('GTA V: sua playlist pode ter anúncios e locutor','No PC, o modo Radio da Self Radio coloca suas músicas entre anúncios e falas de DJ. O intervalo também ajuda a construir o mundo.','Você deixaria os intervalos ou preferiria ouvir só as faixas?','SUA PLAYLIST. COM LOCUTOR.','L07'),
'C11':('GTA 6: Jason não paga aluguel, mas existe uma cobrança','A moradia oferecida por Brian vem com serviços em troca. Esse acordo muda a pergunta sobre quem precisa de quem.','Esse acordo parece mais oportunidade ou dependência para Jason?','SEM ALUGUEL. COM COBRANÇA.','L08'),
'C12':('GTA 6: você confiaria num plano de Raul Bautista?','Experiência e risco crescente aparecem juntos no perfil de Raul. Saber executar também significa saber quando parar?','Você confiaria mais na experiência ou na capacidade de desistir de um plano ruim?','VOCÊ CONFIARIA?','L08'),
'L01-R02':('Jason e Lucia: a premissa de GTA 6 não revela um traidor','Confiança sob pressão já cria conflito. Transformar essa ideia em um final confirmado é um salto que a premissa não sustenta.','O que mais te interessa na dupla: a confiança ou o custo das escolhas?','CONFIANÇA NÃO É SPOILER','L01'),
'L01-R03':('Uma imagem de GTA 6 não revela o tamanho do mapa','Lugares variados não medem distâncias, e fachadas não confirmam acesso. Veja o que cada evidência realmente permite afirmar.','O que você quer explorar primeiro: a cidade, as Keys ou o pântano?','ISSO NÃO MEDE O MAPA','L01')}
