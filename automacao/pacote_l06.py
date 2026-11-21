"""Textos de publicação sincronizados com o master entregue."""
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]/'producao/L06'
O = P/'publicacao'
master = P/'exportacoes/Pixel_Procurado_L06_4K.mp4'
assert master.is_file()
data = json.loads((P/'projeto/edicao_l06.json').read_text(encoding='utf8'))


def save(name, text):
    (O/name).write_text(text.strip()+'\n',encoding='utf8')


def stamp(seconds):
    seconds = int(seconds)
    return f'{seconds//60:02}:{seconds%60:02}'


chapter_starts = [(0, 'O contraste de Leonida')]
for n, name in [
    (3,'Leonida Keys e a iguana'),
    (7,'Grassrivers entre água e mata'),
    (10,'Vice City do neon ao viaduto'),
    (13,'Port Gellhorn e o Starlet Motel'),
    (16,'Ambrosia, indústria e lama'),
    (19,'Mount Kalaga, estrada e rio'),
    (21,'Seis lugares, seis climas'),
]:
    chapter_starts.append((data['paragraphs'][n-1]['start'], name))
assert all(int(y[0])-int(x[0])>=10 for x,y in zip(chapter_starts,chapter_starts[1:]))
assert data['duration']-chapter_starts[-1][0]>=10
chapters = '\n'.join(f'{stamp(t)} {name}' for t,name in chapter_starts)
sources = '''Rockstar Games — GTA VI e vídeos oficiais: https://www.rockstargames.com/VI
Rockstar Games — galeria oficial de capturas: https://www.rockstargames.com/VI/media/screenshots
Rockstar Games — Only in Leonida: https://www.rockstargames.com/VI/only-in-leonida'''
save('01_TITULO.txt',data['title'])
save('02_DESCRICAO.txt',f'''
Nas Keys, o olhar vai até o horizonte. Em Grassrivers, a mata esconde o que vem depois da curva.
As imagens oficiais de GTA 6 mostram seis lugares de Leonida com climas bem diferentes.

Da iguana na rua ao caiaque sob a ponte, a gente compara como luz, vegetação, arquitetura e pessoas mudam a sensação de cada lugar. É uma leitura do material divulgado pela Rockstar, com observações sobre as imagens e a atmosfera que elas passam.

Se você pudesse escolher a primeira parada em Leonida, onde iria? Conta também qual detalhe te fez escolher.

CAPÍTULOS
{chapters}

FONTES
{sources}

Créditos: imagens e vídeos de GTA VI por Rockstar Games. Análise, edição e gráficos por Pixel Procurado. Narração sintetizada com Gemini TTS e voz personalizada. Capa ilustrativa gerada com IA.

#GTA6 #GTAVI #PixelProcurado
''')
save('03_COMENTARIO_FIXADO.txt','Se a primeira parada em Leonida fosse sua, qual lugar você escolheria? Vale responder com o lugar e o detalhe que te fez parar. A iguana já votou nas Keys.')
save('04_TAGS.txt','GTA 6, GTA VI, GTAVI, Leonida, Leonida Keys, Grassrivers, Grass Rivers, Vice City, Port Gellhorn, Ambrosia, Mount Kalaga, Rockstar Games, Pixel Procurado')
save('05_CAPITULOS.txt',chapters)
save('06_FONTES.txt',sources)
save('00_GUIA_DE_PUBLICACAO.md',f'''
# L06 — pacote de publicação

Use o [MP4 4K](../exportacoes/Pixel_Procurado_L06_4K.mp4) e a [capa JPG](capa_youtube.jpg). A duração do projeto é {stamp(data["duration"])}. O master PNG sem perdas e o JPG de envio têm 1280 × 720. O JPG pesa 327.040 bytes. A capa complementa o título com “PARAÍSO DÁ MEDO?”.

O título principal está em [01_TITULO.txt](01_TITULO.txt). Alternativas:

- GTA 6: da iguana no asfalto ao pântano de Leonida
- GTA 6: o que muda entre Vice City e os outros lugares de Leonida

No YouTube Studio, use a descrição e as tags dos arquivos 02 e 04, respectivamente. Selecione categoria Jogos, jogo Grand Theft Auto VI e idioma Português (Brasil). Público sugerido “Não é conteúdo para crianças”. Restrição etária é um campo separado a decidir pelo conteúdo efetivo. Sugestão de nome de playlist “Pixel Procurado — Dossiês GTA”.

Os capítulos na descrição começam em 00:00, seguem os tempos da edição e respeitam o mínimo de 10 segundos. A legenda já aparece no MP4. O SRT separado serve como faixa selecionável de acessibilidade e pode duplicar o texto na tela se usado ao mesmo tempo.

O episódio usa voz personalizada sintetizada pelo Gemini TTS e uma ilustração de capa gerada por IA. A capa é apresentada como ilustração editorial. Confira a opção de transparência no Studio pelo uso efetivo da voz. A identidade associada ao modelo personalizado não foi confirmada. Se a voz reproduzir uma pessoa real diferente do criador, a orientação oficial pede declaração.

Se usar tela final, selecione um vídeo ou uma playlist efetivamente existentes. O YouTube permite a tela nos últimos 5 a 20 segundos. Posicione os elementos longe da iguana e da legenda ou pule a tela final se a interface não permitir a composição.

Confira a reprodução e o processamento em 4K em modo Não listado antes de tornar público. Fixe o texto do arquivo 03 quando o episódio estiver publicado. Créditos identificam o material utilizado. A etapa de produção deste pacote foi local.

Fontes oficiais consultadas em 04/11/2026:

- [Miniaturas](https://support.google.com/youtube/answer/72431?hl=pt-BR)
- [Capítulos](https://support.google.com/youtube/answer/9884579?hl=pt-BR)
- [Tags](https://support.google.com/youtube/answer/146402?hl=pt-BR)
- [Tela final](https://support.google.com/youtube/answer/6388789?hl=pt-BR)
- [Transparência sobre uso de IA](https://support.google.com/youtube/answer/14328491?hl=pt-BR)
''')
save('PROMPT_THUMBNAIL.txt','''
Ferramenta: ImageGen integrada. Arte de capa editorial para L06.

Wide 16:9 YouTube thumbnail background, no text, no logos. Cinematic high-end stylized editorial illustration inspired by subtropical Florida geography, not an official game screenshot. Strong diagonal transition between bright cyan island ocean and a low distant Keys bridge on left, and dark dense Everglades-like mangroves with an airboat and spray on the lower right. A single distinctly recognizable green iguana in dramatic close-up in the right foreground, sharp face and crest, glancing left toward the bright ocean. High contrast, golden rim light, graphite-green shadows, subtle tropical turquoise. Preserve the left 45 percent as open sky and darker smooth ocean for separately added white/yellow type. Low bridge still visible near middle horizon. No people, no letters, no symbols, no watermarks.

Composição determinística: compose_thumbnail.py, modo long, primeira linha PARAÍSO, segunda DÁ MEDO?, selo do Pixel Procurado e logo GTA VI do acervo da skill.
''')
print(chapters)
