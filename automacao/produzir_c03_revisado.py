"""C03 revised narration: reuse the local renderer with episode-specific direction."""
import sys
from pathlib import Path
import shorts_vertical as edit
from shorts_editorial import shot, graph, C

edit.PLANS['C03'] = [
    shot(None,C(13),'ESSE ABRAÇO TEM\nPOLÍCIA NO FUNDO.','GTA VI • OLHE O QUADRO',hook=True,ring=[.76,.34,.24,.57]),
    shot('No recorte',C(13),'O SOL ENTRE OS ROSTOS.','RECORTE EDITORIAL',crop=[.25,0,.5,1]),
    shot('Parece que falta',C(13),'A PESSOA CERTA…','ANÁLISE VISUAL',crop=[.30,.05,.42,.80]),
    shot('A pessoa certa veio',C(13),'…O CONTEXTO COMPLICADO.','QUADRO INTEIRO'),
    shot('Na arte inteira',C(13),'BARCOS DA POLÍCIA.','DETALHE DA MESMA IMAGEM',ring=[.01,.46,.24,.49]),
    shot('e um helicóptero',C(13),'E UM HELICÓPTERO.','DETALHE DA MESMA IMAGEM',ring=[.72,.01,.25,.3]),
    shot('Esses elementos',C(13),'AFETO + PERIGO.','COMPOSIÇÃO VISUAL'),
    shot('O romance continua',C(13),'O ENTORNO MUDA O ABRAÇO.','QUADRO INTEIRO'),
    graph('É como escolher','A FOTO DA VIAGEM',['FOTO PERFEITA','GUINCHO FORA DO RECORTE'],'COMPARAÇÃO HIPOTÉTICA'),
    graph('O momento bonito','O MOMENTO ACONTECEU.',['O RECORTE MOSTRA UMA PARTE'],'COMPARAÇÃO HIPOTÉTICA'),
    graph('E o guincho','O GUINCHO TAMBÉM FOI.',['PARTICIPAÇÃO ESPECIAL NAS FÉRIAS'],'COMPARAÇÃO HIPOTÉTICA'),
    shot('Aqui, a leitura',C(13),'A POSIÇÃO CONTA.','ANÁLISE DA COMPOSIÇÃO'),
    shot('O casal ocupa',C(13),'O CASAL NO CENTRO.','ANÁLISE VISUAL',crop=[.25,0,.5,1]),
    shot('a perseguição sugerida',C(13),'PRESSÃO NO ENTORNO.','QUADRO INTEIRO',ring=[.76,.34,.24,.57]),
    graph('Isso não revela','O QUADRO NÃO REVELA',['QUANDO ACONTECE','QUEM TRAI QUEM','A PRÓXIMA MISSÃO'],'LIMITES DA EVIDÊNCIA'),
    shot('O detalhe interessante',C(13),'PRÓXIMOS. SOB PRESSÃO.','CONTRASTE VISUAL'),
    shot('Ao fechar',C(13),'RECORTE:\nMAIS AFETO.','RECORTE EDITORIAL',crop=[.25,0,.5,1]),
    shot('Ao abrir',C(13),'O PERIGO ENTRA NA IMAGEM.','QUADRO INTEIRO'),
    shot('Antes de usar',C(13),'CONFIRA O QUADRO INTEIRO.','CRITÉRIO DE LEITURA'),
    shot('O recorte pode',C(13),'O RECORTE MUDA A PERGUNTA.','ANÁLISE VISUAL'),
    shot('Porque',C(13),'ESSE ABRAÇO TEM\nPOLÍCIA NO FUNDO.','GTA VI • OLHE O QUADRO',hook=True,ring=[.76,.34,.24,.57]),
]

if __name__ == '__main__':
    action=sys.argv[1]
    if action=='prepare':edit.prepare('C03')
    elif action=='sample':edit.render('C03',{0,1,10,18})
    elif action=='render':edit.render('C03')
    elif action=='qa':edit.qa('C03')
    else:raise ValueError(action)
