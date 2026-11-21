"""Pacote textual L04 a partir dos tempos finais da timeline validada."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'producao/L04';O=P/'publicacao';O.mkdir(exist_ok=True)
D=json.loads((P/'projeto/edicao_l04.json').read_text(encoding='utf8'))
def stamp(t):s=int(t);return f'{s//60:02}:{s%60:02}'
chapters=[(0,'Tem gameplay no Trailer 2?'),(D['paragraphs'][3]['start'],'O que a câmera realmente prova'),(D['paragraphs'][9]['start'],'Capturado no PS5: é exclusivo?'),(D['paragraphs'][15]['start'],'Ilustração e captura de tela'),(D['paragraphs'][21]['start'],'O limite de um único quadro'),(D['paragraphs'][23]['start'],'Três checagens antes da certeza')]
assert all(b[0]-a[0]>=10 for a,b in zip(chapters,chapters[1:])) and D['duration']-chapters[-1][0]>=10
chaptertext='\n'.join(f'{stamp(t)} {name}' for t,name in chapters)
def save(name,text):(O/name).write_text(text.strip()+'\n',encoding='utf8')
save('01_TITULO.txt','GTA 6: tem gameplay no Trailer 2? Três dúvidas resolvidas')
save('02_DESCRICAO.txt',f'''O Trailer 2 de GTA 6 tem gameplay, sim. Mas a posição da câmera não resolve cada cena.
PS5 na gravação também não significa exclusividade. E um pôster não serve para medir os gráficos.

Neste episódio do Pixel Procurado, separamos três coisas: gameplay e cenas prontas; aparelho da captura e plataformas anunciadas; ilustração e screenshot. Com imagens do Trailer 2 e duas peças concretas da biblioteca oficial da Rockstar.

Qual detalhe do material oficial você quer ver examinado no próximo vídeo?

CAPÍTULOS
{chaptertext}

FONTES E RECORTE
Trailer 2 — Rockstar Games: https://www.youtube.com/watch?v=VQRLujxTm3c
Página do Trailer 2: https://www.rockstargames.com/VI/trailer-2
Comunicado oficial de 07/05/2025 sobre captura no PS5 e gameplay/cutscenes: https://x.com/RockstarGames/status/1920181314092765494
Plataformas oficiais: https://www.rockstargames.com/VI
Biblioteca de screenshots e artwork: https://www.rockstargames.com/VI/media

Plataformas e categorias rechecadas em 31/10/2026. A declaração técnica do Trailer 2 segue a apuração histórica do roteiro; a descrição do YouTube e a postagem do X não puderam ser novamente extraídas nesta consulta. O episódio trata especificamente do Trailer 2, não dos materiais posteriores, e não classifica cada plano individualmente.

CRÉDITOS
Imagens de GTA VI e personagens: Rockstar Games. Análise, edição e gráficos: Pixel Procurado. Narração produzida com Gemini TTS e voz personalizada; thumbnail é uma montagem editorial criada com IA, sem representar captura oficial. Os trechos originais estão sem o áudio do trailer.

#GTA6 #GTAVI #PixelProcurado''')
save('03_COMENTARIO_FIXADO.txt','Qual imagem ou trecho oficial você quer que a gente examine? Manda o nome do vídeo e o minuto — ou identifica a imagem da biblioteca. A próxima pista começa por aí.')
save('04_TAGS.txt','GTA 6, GTA VI, GTA6 trailer 2, gameplay GTA 6, Rockstar Games, PlayStation 5, Xbox Series X, Xbox Series S, screenshot, artwork, Pixel Procurado')
save('05_CAPITULOS.txt',chaptertext)
save('00_GUIA_DE_PUBLICACAO.md',f'''# L04 — pacote para publicação

Vídeo: `../exportacoes/Pixel_Procurado_L04_4K.mp4`; legendas: mesmo nome `.srt`. Duração planejada a conferir contra QA: {D['frames']/30:.3f}s; composição 3840×2160, 30fps, H.264/AAC.

Título recomendado no arquivo 01. Alternativas: “GTA 6 no PS5: o que o Trailer 2 realmente confirma” e “Gameplay, PS5 e screenshots: três cuidados com GTA 6”. A capa “TEM GAMEPLAY?” complementa a resposta imediata do vídeo.

1. Usar MP4, `capa_youtube.jpg` (1280×720), título e descrição. Categoria Jogos; jogo Grand Theft Auto VI; idioma português (Brasil). Público sugerido: não destinado a crianças; restrição etária é uma decisão distinta, baseada no vídeo real.
2. O usuário solicitou programação pública em 01/11/2026 às 12h de Brasília (15h UTC). Este executor não fez upload nem agendamento; o coordenador executará depois da revisão independente. Caso haja envio manual, conferir vídeo e áudio após processamento em 4K antes de disponibilizar.
3. Importar SRT como acessibilidade quando desejado. O MP4 já contém legendas incorporadas; ativar também a faixa selecionável pode sobrepor dois conjuntos.
4. Capítulos vêm dos tempos desta locução, começam em 00:00 e têm intervalos superiores a dez segundos. Conferir disponibilidade de recursos avançados da conta. Não substituir por tempos de versões antigas.
5. IA: há voz personalizada sintetizada e arte editorial da capa. Não foi confirmado que a voz é do próprio usuário. Recomenda-se declarar o uso de IA para transparência sobre a narração realista; nenhum rosto de pessoa real é falsificado. Não afirmar clonagem própria. Consulte o campo e a política vigentes ao enviar.
6. Tela final opcional nos últimos 5–20s: um elemento discreto de inscrição ou vídeo realmente existente, fora da legenda inferior e dos rostos. O encerramento continua narrado. Não inserir link de episódio inexistente.
7. Tags no campo próprio, sem despejá-las na descrição. Playlist, se necessário, é sugestão: “Pixel Procurado — Dossiês GTA”. Nenhum patrocínio ou link social foi inventado. Créditos não garantem licença nem ausência de reivindicação.

Regras oficiais consultadas em 31/10/2026:
- Thumbnail: https://support.google.com/youtube/answer/72431?hl=pt-BR
- Capítulos: https://support.google.com/youtube/answer/9884579?hl=pt-BR
- Tags: https://support.google.com/youtube/answer/146402?hl=pt-BR
- Tela final: https://support.google.com/youtube/answer/6388789?hl=pt-BR
- IA: https://support.google.com/youtube/answer/14328491?hl=pt-BR

Conferir `../projeto/FONTES_VERIFICADAS.md` e `../projeto/render4k/qa/validacao_final.json` para procedência e validação. Revisão visual por amostragem não equivale a escuta subjetiva integral. Não houve upload por este executor.
''')
print(chaptertext)
