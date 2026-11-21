"""L05 pacote baseado na timeline da locução atual."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'producao/L05';O=P/'publicacao';O.mkdir(exist_ok=True)
D=json.loads((P/'projeto/edicao_l05.json').read_text(encoding='utf8'))
def stamp(t):s=int(t);return f'{s//60:02}:{s%60:02}'
chapters=[(0,'O carro distrai: olhe a rua'),(D['paragraphs'][2]['start'],'Praia: uma ação ou pequenas situações?'),(D['paragraphs'][9]['start'],'Carros: máquina, gente e bairro'),(D['paragraphs'][15]['start'],'Vista aérea: aeronave ou cidade?'),(D['paragraphs'][19]['start'],'Por que isso não é um benchmark'),(D['paragraphs'][20]['start'],'O caminho do olhar')]
assert all(b[0]-a[0]>=10 for a,b in zip(chapters,chapters[1:])) and D['duration']-chapters[-1][0]>=10
ct='\n'.join(f'{stamp(t)} {name}' for t,name in chapters)
def save(name,text):(O/name).write_text(text.strip()+'\n',encoding='utf8')
save('01_TITULO.txt','GTA V e GTA VI: três diferenças que estas imagens revelam')
save('02_DESCRICAO.txt',f'''O carro distrai. Mas a rua também conta a história.
Seis fotos oficiais de GTA V e GTA VI, três pares e um cuidado: olhar além do veículo.

Comparamos o ciclista e as situações da praia; o Cheetah e o encontro de carros; o jato e o helicóptero sobre a cidade. A análise é de composição e contexto nas imagens de divulgação. Este conjunto não é um benchmark de gráficos, densidade de pessoas ou tamanho de mapa.

Qual lugar faria você esquecer a missão: praia, encontro de carros ou orla vista do alto?

CAPÍTULOS
{ct}

FONTES E RECORTE
Rockstar Games — Transport (20/08/2012): https://www.rockstargames.com/newswire/article/89k8a5545o2k8k/transport.html
Ciclista: https://media.rockstargames.com/rockstargames/img/global/news/upload/actual_1345416814.jpg
Cheetah: https://media.rockstargames.com/rockstargames/img/global/news/upload/actual_1345416829.jpg
Jato: https://media.rockstargames.com/rockstargames/img/global/news/upload/actual_1345416846.jpg
GTA VI — biblioteca oficial: https://www.rockstargames.com/VI/media
Screenshots Vice City 05, 09 e 11.

Referência editorial: 03/11/2026. A galeria Transport foi acessada, mas não forneceu texto extraível nesta consulta; os três JPGs oficiais foram baixados e inspecionados. As fontes históricas de GTA V têm 640×360 e aparecem em painéis identificados; não houve ampliação por IA para inventar detalhe. Não representam um teste da versão atual de GTA V.

CRÉDITOS
Imagens e jogos: Rockstar Games. Análise, edição e gráficos: Pixel Procurado. Narração produzida com Gemini TTS e voz personalizada. Capa: montagem editorial criada com IA, não uma captura oficial ou gameplay. Movimento das fotografias em 2D; sem alegação de parallax.

#GTAV #GTAVI #GTA6 #PixelProcurado''')
save('03_COMENTARIO_FIXADO.txt','Praia, encontro de carros ou orla vista do alto: onde você esqueceria a missão? E qual detalhe na borda da foto chamou a sua atenção?')
save('04_TAGS.txt','GTA V, GTA 5, GTA VI, GTA 6, GTAVI, Rockstar Games, Vice City, screenshots GTA 6, comparação GTA V GTA VI, Cheetah GTA, Pixel Procurado')
save('05_CAPITULOS.txt',ct)
save('00_GUIA_DE_PUBLICACAO.md',f'''# L05 — pacote de publicação

Vídeo: `../exportacoes/Pixel_Procurado_L05_4K.mp4`. SRT com o mesmo nome. 3840×2160, 30fps, H.264/AAC48kHz, {D['frames']/30:.3f}s. Conferir QA final antes do envio. Master da capa1920×1080; upload1280×720.

Título recomendado no arquivo01. Alternativas: “GTA V vs GTA VI: o detalhe está ao redor dos carros” e “Seis fotos de GTA V e GTA VI: o que muda no caminho do olhar”. Capa OLHE AO REDOR complementa o título.

Categoria Jogos; identificação dos jogos GTA V e GTA VI; idioma português(Brasil). Público sugerido: não destinado a crianças; isso não equivale automaticamente a restrição18+. Usar a análise do conteúdo efetivo.

O coordenador cuida do agendamento autorizado pelo usuário para03/11/2026 às12h de Brasília(15hUTC) nos canais conectados do Postiz. Este executor não fez upload ou agendamento. Verificar processamento4K e reprodução após o envio.

O MP4 já contém legendas. A faixa SRT é adicional para acessibilidade; ativar ambas pode mostrar legendas duplicadas. Capítulos calculados da locução atual, iniciam em00:00, ordem crescente e todos>=10s; dependem dos recursos da conta.

Uso de IA: voz personalizada sintetizada e montagem editorial de capa. Não foi confirmado que a voz é a do próprio usuário. Declarar o uso efetivo conforme o campo vigente, sem alegar clonagem própria. A capa não é captura de jogo. Tela final opcional nos últimos5–20s, sem cobrir fotografia, legenda ou texto; usar somente vídeos/playlist realmente existentes.

Tags no campo próprio. Playlist sugerida: Pixel Procurado — Dossiês GTA. Não foram inventados patrocínio ou links sociais. Créditos não garantem licença nem ausência de reivindicação.

Regras oficiais consultadas em03/11/2026:
- https://support.google.com/youtube/answer/72431?hl=pt-BR
- https://support.google.com/youtube/answer/9884579?hl=pt-BR
- https://support.google.com/youtube/answer/146402?hl=pt-BR
- https://support.google.com/youtube/answer/6388789?hl=pt-BR
- https://support.google.com/youtube/answer/14328491?hl=pt-BR

Fontes e limites em `../projeto/FONTES_VERIFICADAS.md`; validação em `../projeto/render4k/qa/validacao_final.json`. A inspeção visual é amostrada; não se alega escuta subjetiva integral. Não houve upload por este executor.
''')
save('06_FONTES.txt','\n'.join(['https://www.rockstargames.com/newswire/article/89k8a5545o2k8k/transport.html','https://media.rockstargames.com/rockstargames/img/global/news/upload/actual_1345416814.jpg','https://media.rockstargames.com/rockstargames/img/global/news/upload/actual_1345416829.jpg','https://media.rockstargames.com/rockstargames/img/global/news/upload/actual_1345416846.jpg','https://www.rockstargames.com/VI/media']))
print(ct)
