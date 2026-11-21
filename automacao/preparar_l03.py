"""Direção L03: executar só depois de validar a voz e o alinhamento final."""
import json
import hashlib
import math
import re
import unicodedata
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'producao/L03'
WORK = P / 'projeto'
FPS = 30


def norm(text):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', text.lower()))


def build():
    # No fallback to estimated speech times or unvalidated Gemini blocks.
    voice = P / 'voz/narracao_normalizada.wav'
    alignment = P / 'voz/palavras_alinhadas.json'
    assert voice.is_file() and alignment.is_file(), 'Aguardar voz validada e palavras alinhadas.'
    words = json.loads(alignment.read_text(encoding='utf-8-sig'))
    assert isinstance(words, list) and words
    assert not any(w.get('status') == 'pending_review' for w in words), 'Aguardar decisão e WAV definitivo.'
    with wave.open(str(voice), 'rb') as wav:
        duration = wav.getnframes() / wav.getframerate()
    for i, word in enumerate(words):
        assert 0 <= word['start'] <= word['end'] <= duration + .02, (i, word)
        if i:
            assert word['start'] >= words[i - 1]['start'], (i, word)
    normalized = [norm(w['word']) for w in words]

    def anchor(phrase, occurrence=None):
        tokens = [norm(w) for w in phrase.split()]
        hits = [i for i in range(len(words) - len(tokens) + 1)
                if normalized[i:i + len(tokens)] == tokens]
        if occurrence is None:
            assert len(hits) == 1, f'Âncora ambígua/ausente: {phrase!r}: {hits}'
            occurrence = 1
        assert 1 <= occurrence <= len(hits), (phrase, occurrence, hits)
        index = hits[occurrence - 1]
        return {'phrase': phrase, 'occurrence': occurrence, 'wordIndex': index,
                'frame': round(words[index]['start'] * FPS)}

    def still(group, name, number):
        return f'videosGTAVI/GTAVI_Screenshots/{group}/{name}/{name.replace(" ", "_")}_{number:02}.jpg'

    rd = lambda n: still('People', 'Real Dimez', n)
    vc = lambda n: still('Places', 'Vice City', n)
    v1 = 'producao/L03/midia/V1_Vice_City_Classico_Screens_1.jpg'
    v2 = 'producao/L03/midia/V2_Vice_City_Classico_Screens_2.jpg'
    shots = []
    default_source = 'GTA VI • Imagens: Rockstar Games • Análise: Pixel Procurado'
    classic_source = 'Grand Theft Auto: Vice City • Imagem promocional do clássico • Rockstar Games'
    original_rects = json.loads((WORK / 'inspecoes/retangulos_fontes.json').read_text(encoding='utf8'))

    def add(phrase, file='', *, label='', title='', sub='', graphic='',
            purpose='', evidence='official-image', occurrence=None, **extra):
        resolved = anchor(phrase, occurrence) if phrase else {'phrase': 'INÍCIO', 'occurrence': 1, 'wordIndex': 0, 'frame': 0}
        kind = 'graphic' if not file else 'video' if file.endswith('.mp4') else 'image'
        shot = dict(anchor=resolved['phrase'], anchorOccurrence=resolved['occurrence'],
                    anchorWordIndex=resolved['wordIndex'], fromFrame=resolved['frame'],
                    kind=kind, file=file, offset=0, label=label, title=title, sub=sub,
                    graphic=graphic, source=default_source if file else 'PIXEL PROCURADO • GRÁFICO EDITORIAL',
                    presentation='full' if file else 'graphic', zoom=[1.01, 1.035], focus=[.5, .46],
                    evidence=evidence, editorialPurpose=purpose, captionPosition='bottom',
                    panelSide='right')
        if file in (v1, v2):
            shot.update(presentation='classic-card', source=classic_source,
                        viewport=dict(x=240, y=126, width=1040, height=728),
                        zoom=[1, 1.01], focus=[.5, .5],
                        layout=dict(side='right', top=280, width=490))
        shot.update(extra)
        shots.append(shot)
        return shot

    def focus(phrase, file, source_id, rect_id, label, **extra):
        x, y, width, height = original_rects[source_id]['rects'][rect_id]
        return add(phrase, file, label='OBSERVAÇÃO VISUAL', graphic='focus', zoom=[1, 1],
                   focusRects=[dict(id=rect_id, x=x / 2, y=y / 2,
                                    width=width / 2, height=height / 2, cue=0, label=label)],
                   purpose=f'Apontar o elemento real: {rect_id}', **extra)

    def staged(phrase, graphic, items, stage, **extra):
        return add(phrase, graphic=graphic, items=items, stage=stage,
                   cues=[-30 if i < stage - 1 else 0 for i in range(len(items))],
                   evidence='editorial-graphic', **extra)

    # P1: recompensa visual antes de qualquer apresentação do canal.
    opening = add(None, rd(2), label='VICE CITY / OUTRA ÉPOCA', graphic='focus', zoom=[1, 1],
                  purpose='Abrir com a observação concreta do telefone à esquerda.')
    x, y, w, h = original_rects['Real_Dimez_02']['rects']['telefone_esquerdo']
    opening['focusRects'] = [dict(id='telefone_esquerdo', x=x/2, y=y/2, width=w/2, height=h/2,
                                 cue=anchor('a plateia sobe o celular')['frame'], label='A plateia também filma')]
    add('duas artistas em cima de um carro', rd(2), label='REAL DIMEZ', zoom=[1, 1],
        purpose='Limpar o contorno e revelar a apresentação e o entorno.')
    add('Essa imagem entrega a grande mudança', rd(2), label='MESMA CIDADE DO EXCESSO',
        purpose='Ligar o excesso reconhecível à mudança de época.', zoom=[1, 1.035])

    # P2: memória do clássico e cultura contemporânea.
    add('Pensa na lembrança que o nome Vice City traz', v1, label='MEMÓRIA DO CLÁSSICO',
        purpose='Palmeiras e calor na imagem clássica completa.')
    add('e a camisa de Tommy Vercetti', v2, label='TOMMY VERCETTI / CLÁSSICO',
        purpose='Mostrar exatamente a camisa citada sem insinuar retorno do personagem.')
    add('Agora coloca nessa lembrança', rd(2), label='OUTRA VITRINE',
        purpose='Voltar à multidão que registra o espetáculo.', zoom=[1.025, 1])
    add('O cenário continua reconhecível', vc(6), label='RECONHECIMENTO',
        purpose='Ligar a atmosfera urbana à vitrine contemporânea.')

    # P3: itens progressivos, cada etapa é uma curta sequência nova.
    questions = ['O que preserva a identidade?', 'O que mudou de época?', 'O que a nostalgia deixa de fora?']
    staged('Vamos olhar para três coisas', 'list', questions, 0, label='TRÊS PISTAS', title='A cidade além da memória',
           purpose='Apresentar o percurso sem antecipar respostas.')
    staged('o que preserva essa identidade', 'list', questions, 1, label='TRÊS PISTAS', title='A cidade além da memória')
    staged('o que denuncia a mudança de época', 'list', questions, 2, label='TRÊS PISTAS', title='A cidade além da memória')
    staged('e qual pedaço da cidade', 'list', questions, 3, label='TRÊS PISTAS', title='A cidade além da memória')
    add('A primeira pista está', v1, label='01 / A IDENTIDADE',
        purpose='Preparar e sustentar a imagem clássica que a fala passa a descrever.')

    # P4: quadro clássico preservado, sem tentar fabricar detalhe.
    add('A foto oficial não precisa de explosão', v1, label='O LUGAR NO COTIDIANO',
        title='Um lugar\nreconhecível.', graphic='headline',
        purpose='Dar leitura à arquitetura e à vegetação com espaço fora da fonte.', evidence='editorial-reading')
    add('É aquela vontade de entrar no carro', v1, label='LEMBRANÇA DE JOGAR',
        title='Sair dirigindo.', sub='Uma sensação, além da missão', graphic='headline',
        evidence='editorial-reading', purpose='Separar a leitura afetiva da descrição factual.')

    # P5: datas só aparecem quando pronunciadas.
    dates = ['LANÇAMENTO\n2002', 'HISTÓRIA\n1986']
    staged('O jogo chegou em', 'dates', dates, 0, label='DUAS DATAS DIFERENTES',
           source='Fontes: Take-Two/Rockstar, décimo aniversário • Rockstar, arquivo de rádio',
           purpose='Abrir a distinção entre lançamento e ambientação.')
    staged('dois mil e dois', 'dates', dates, 1, label='DUAS DATAS DIFERENTES',
           source='Fonte do lançamento: Take-Two/Rockstar, décimo aniversário')
    staged('mil novecentos e oitenta e seis', 'dates', dates, 2, label='DUAS DATAS DIFERENTES', occurrence=1,
           source='1986: ambientação do clássico • Rockstar, arquivo de rádio')
    add('Quando a gente pede que GTA seis', v1, label='DUAS FORMAS DE SAUDADE',
        title='Atmosfera\nou memória?', sub='Leitura editorial sobre a nostalgia', graphic='headline',
        evidence='editorial-reading', purpose='Mostrar que lembrar a época e lembrar a experiência são desejos distintos.')

    # P6 e P7: personagem/cidade, depois linguagem urbana contemporânea.
    add('Uma imagem de Tommy com a camisa estampada', v2, label='PERSONAGEM + CIDADE',
        purpose='Ler a imagem inteira: camisa, palmeiras e prédio.')
    add('A cidade participa da identidade do personagem', v2, label='LEITURA DO CANAL',
        title='O conjunto\nvem primeiro.', graphic='headline', evidence='editorial-reading',
        purpose='Sustentar a análise de reconhecimento sem zoom de baixa resolução.')
    add('Nas imagens de GTA seis', vc(6), label='02 / UMA LINGUAGEM FAMILIAR',
        purpose='Fachadas iluminadas, palmeiras e vida de rua.', zoom=[1, 1.035])
    add('O neon ainda cumpre seu turno', vc(6), label='O NEON AINDA ESTÁ AQUI',
        purpose='Continuar a observação da iluminação urbana.', zoom=[1.035, 1.05], focus=[.23, .25])
    add('Só que reconhecer essa linguagem', vc(6), label='LIGAÇÃO DE ATMOSFERA',
        purpose='Distinguir continuidade visual de reconstrução rua por rua.', zoom=[1.035, 1])

    # P8 e P9: a pergunta termina no telefone real, sem outra imagem de celular.
    add('E existe um detalhe que torna a mudança', rd(2), label='QUEM SEGURA A CÂMERA?',
        purpose='Preparar a pergunta com as artistas e a plateia no mesmo quadro.', zoom=[1, 1])
    add('Na imagem de Real Dimez', rd(2), label='REAL DIMEZ / OBSERVAÇÃO VISUAL',
        purpose='Estabelecer artistas, capô e público.', zoom=[1, 1])
    focus('Há telefones erguidos', rd(2), 'Real_Dimez_02', 'telefone_esquerdo', 'Telefone à esquerda')
    focus('e uma das telas mostra a apresentação', rd(2), 'Real_Dimez_02', 'tela_apresentacao', 'A apresentação na tela')
    add('A festa está acontecendo para quem está ali', rd(2), label='A PLATEIA TAMBÉM PRODUZ A CENA',
        purpose='Retornar ao quadro completo e sustentar a leitura do conjunto.', zoom=[1, 1])

    # P10: fonte oficial e leitura editorial têm rótulos distintos.
    add('A descrição oficial da dupla', rd(4), label='APRESENTAÇÃO OFICIAL / REAL DIMEZ',
        source='Fonte: Rockstar Games • Only in Leonida • Real Dimez', evidence='official-description',
        purpose='Apoiar música e redes na apresentação oficial, sem inventar interface de postagem.', zoom=[1, 1.025])
    add('Isso dá contexto ao que a imagem mostra', rd(1), label='MÚSICA + ATENÇÃO',
        purpose='Mostrar o trabalho musical em estúdio.', zoom=[1.025, 1])
    add('Minha leitura é que a nova Vice City', rd(2), label='LEITURA DO CANAL',
        evidence='editorial-reading', purpose='Marcar explicitamente a interpretação sobre ambição contemporânea.')

    # P11: rádio próprio, sem áudio ou reprodução de comerciais.
    radio = add('No clássico os anúncios de rádio', label='RÁDIO / 1986', title='Comerciais fictícios',
                sub='Sátira de uma vida desejável', graphic='radio', items=['Consumo', 'Aparência', 'Sucesso'], stage=3,
                source='Fonte: Rockstar Newswire • Arquivo de comerciais fictícios • 15/07/2010',
                evidence='editorial-graphic', purpose='Explicar a sátira histórica com gráfico original.')
    radio['cues'] = [anchor(p)['frame'] - radio['fromFrame'] for p in ('consumo aparência', 'aparência e promessas', 'sucesso A Rockstar')]
    add('O exagero não nasceu com o celular', rd(2), label='UMA OBSESSÃO ANTIGA',
        evidence='editorial-reading', purpose='Conectar a sátira do rádio à apresentação contemporânea.', zoom=[1, 1.03])

    # P12: a mesma cena ganha um argumento novo; não é preenchimento.
    add('Essa comparação é mais interessante', rd(4), label='O PARENTESCO ESTÁ NO COMPORTAMENTO',
        evidence='editorial-reading', purpose='A imagem da dupla sustenta ambição e aparência, sem caça a easter eggs.')
    add('A cidade continua vendendo uma imagem de vida desejável', rd(2), label='UMA VIDA DESEJÁVEL',
        evidence='editorial-reading', purpose='Reunir palco e público sob a mesma leitura social.', zoom=[1.03, 1])

    # P13 e P14: conforto e ponto de vista; não inventar o frigobar.
    add('Mas se a festa é a vitrine', vc(2), label='03 / ALÉM DA VITRINE',
        purpose='Mudar o ponto de vista para a varanda antes da descrição.', zoom=[1, 1])
    add('Uma das imagens oficiais mostra um casal', vc(2), label='VARANDA / PISCINA / PRAIA',
        purpose='Manter a relação espacial legível no quadro inteiro.', zoom=[1, 1.025], focus=[.7, .45])
    add('A posição da câmera coloca a gente', vc(2), label='LEITURA DO PONTO DE VISTA',
        evidence='editorial-reading', purpose='Explicar o conforto de quem olha sem texto sobre o casal.',
        zoom=[1.025, 1.045], focus=[.76, .5], panelSide='left')
    add('É Vice City funcionando como promessa', vc(2), label='PROMESSA DE FÉRIAS CARAS',
        evidence='editorial-reading', purpose='Sustentar o humor seco do frigobar na imagem, sem criar objeto ou preço.',
        zoom=[1.045, 1.02], focus=[.76, .5], panelSide='left')

    # P15: mesma fonte imóvel, destaques trocam exatamente nas atividades.
    add('Agora desce desse ponto de vista para a praia', vc(5), label='OUTRO PONTO DE VISTA',
        zoom=[1, 1], captionPosition='top', purpose='Estabelecer a praia antes de apontar suas atividades.')
    focus('Há um casal caminhando', vc(5), 'Vice_City_05', 'casal_caminhando', 'Caminhada', captionPosition='top')
    focus('alguém procurando coisas na areia', vc(5), 'Vice_City_05', 'detector_metais', 'Detector de metais', captionPosition='top')
    focus('uma pessoa tomando sol em primeiro plano', vc(5), 'Vice_City_05', 'banho_sol', 'Banho de sol', captionPosition='top')
    focus('e outras ocupando o espaço ao redor', vc(5), 'Vice_City_05', 'outros_banhistas', 'Outras atividades', captionPosition='top')
    add('A mesma ideia de paraíso passa a incluir', vc(5), label='HÁBITOS / IDADES / INTERESSES',
        zoom=[1, 1], captionPosition='top', purpose='Limpar contornos e reencontrar a pluralidade do quadro.')

    # P16: o contraste é entre pontos de vista, não o mesmo endereço.
    add('É esse contraste que me interessa', vc(2), label='O SONHO DE ALGUÉM',
        evidence='editorial-reading', purpose='Retomar a promessa turística como uma leitura do canal.', zoom=[1, 1.02])
    add('e o dia comum de outra pessoa', vc(5), label='O DIA COMUM DE OUTRA PESSOA',
        evidence='editorial-reading', purpose='Dar contexto cotidiano ao glamour.', zoom=[1, 1.025], captionPosition='top')
    add('A imagem deixa de ser apenas uma paisagem bonita', vc(5), label='HISTÓRIAS AO REDOR',
        evidence='editorial-reading', purpose='Mostrar o conjunto de pequenas situações sem identificar figurantes.',
        zoom=[1.025, 1], captionPosition='top')

    # P17: descrição clássica e enumeração na ordem falada.
    add('O clássico já era apresentado pela Rockstar', v1, label='BRILHO / AMBIÇÃO / DEGRADAÇÃO',
        source='Fonte: Rockstar Games • Grand Theft Auto: Vice City • descrição oficial',
        evidence='official-description', purpose='Ancorar a continuidade dos contrastes na descrição oficial.')
    add('O retorno coloca essa identidade diante de outra cultura visual', vc(6), label='OUTRA CULTURA VISUAL',
        evidence='editorial-reading', purpose='Preparar a síntese dos pontos de vista.')
    viewpoints = add('a varanda a rua e a tela', label='QUAL VERSÃO DA CIDADE FICA?',
                     title='Três pontos de vista', graphic='list', items=['A varanda', 'A rua', 'A tela do telefone'], stage=3,
                     evidence='editorial-reading', purpose='Preservar a enumeração rápida sem um flash de imagem de oito frames.')
    viewpoints['cues'] = [anchor(p)['frame'] - viewpoints['fromFrame']
                          for p in ('a varanda a rua e a tela', 'a rua e a tela do telefone', 'e a tela do telefone disputam')]

    # P18: três respostas, cada qual entra na própria fala.
    answers = ['Identidade tropical reconhecível', 'Uma cultura de outra época', 'A memória é uma porta de entrada']
    staged('Por isso minha resposta', 'list', answers, 0, label='É A MESMA VICE CITY?', title='Três partes da resposta',
           purpose='Abrir a síntese final sem antecipar itens.')
    staged('A identidade tropical continua reconhecível', 'list', answers, 1, label='É A MESMA VICE CITY?', title='Três partes da resposta')
    staged('A cultura exibida nos materiais mudou de época', 'list', answers, 2, label='É A MESMA VICE CITY?', title='Três partes da resposta')
    staged('E a memória do jogo antigo', 'list', answers, 3, label='É A MESMA VICE CITY?', title='Três partes da resposta')

    # P19: retorno à descoberta inicial e pergunta, sem nova vinheta.
    add('Eu quero reconhecer Vice City', vc(1), label='RECONHECER E OLHAR DE NOVO',
        evidence='editorial-reading', purpose='Fechar a ideia de reconhecimento com a identidade da cidade.', zoom=[1, 1.02])
    add('A plateia filmando Real Dimez', rd(2), label='O EXCESSO É FAMILIAR',
        evidence='editorial-reading', purpose='Retomar a abertura com seu significado elaborado.', zoom=[1.02, 1])
    add('Qual lembrança sua precisaria sobreviver nesse retorno', rd(2), label='QUAL LEMBRANÇA PRECISA SOBREVIVER?',
        zoom=[1, 1], purpose='Entregar a pergunta final mantendo a cena que motivou a análise.')
    options = ['O rádio', 'A atmosfera das ruas', 'A sensação de conquistar a cidade']
    staged('o rádio a atmosfera', 'list', options, 1, label='QUAL LEMBRANÇA PRECISA SOBREVIVER?', title='A sua Vice City')
    staged('a atmosfera das ruas', 'list', options, 2, label='QUAL LEMBRANÇA PRECISA SOBREVIVER?', title='A sua Vice City')
    staged('ou a sensação de conquistar a cidade', 'list', options, 3, label='QUAL LEMBRANÇA PRECISA SOBREVIVER?', title='A sua Vice City')

    total_frames = math.ceil(duration * FPS)
    for i, shot in enumerate(shots):
        end_frame = shots[i + 1]['fromFrame'] if i + 1 < len(shots) else total_frames
        shot.update(start=shot['fromFrame'] / FPS, end=end_frame / FPS, frames=end_frame - shot['fromFrame'])
        assert shot['frames'] > 0, (i, shot)
        if shot['file']:
            assert (ROOT / shot['file']).is_file(), shot['file']
        if shot.get('focusRects'):
            assert shot['zoom'] == [1, 1], shot
        cues = shot.get('cues', [])[:shot.get('stage', len(shot.get('cues', [])))]
        cues += [r['cue'] for r in shot.get('focusRects', [])]
        new_entries = [c for c in cues if c >= 0]
        shot['animate'] = bool(shot['graphic'] and (not cues or new_entries))
        shot['animationFrames'] = min(shot['frames'], max(new_entries, default=0) + 20) if shot['animate'] else 1
        if shot.get('stage') == 0:
            shot.update(animate=False, animationFrames=1)
        if shot['kind'] == 'graphic':
            shot['zoom'] = [1, 1]
        if shot['captionPosition'] == 'top':
            shot['captionBox'] = dict(x=96, y=130, width=860, alignment='top-left')
        if not shot['editorialPurpose']:
            shot['editorialPurpose'] = f'Revelar o item {shot.get("stage", 0)} na fala, preservando os itens anteriores.'

    captions, batch = [], []
    for i, word in enumerate(words):
        batch.append(word)
        text = ' '.join(w['word'] for w in batch)
        terminal = word['word'].endswith(('.', '?', '!', ';', ':'))
        pause = i + 1 == len(words) or words[i + 1]['start'] - word['end'] > .55
        if len(text) >= 46 or len(batch) >= 8 or terminal or (pause and len(batch) >= 3):
            captions.append(dict(start=batch[0]['start'], end=min(duration, word['end'] + .10), text=text))
            batch = []
    if batch:
        captions.append(dict(start=batch[0]['start'], end=min(duration, batch[-1]['end'] + .12), text=' '.join(w['word'] for w in batch)))
    for a, b in zip(captions, captions[1:]):
        a['end'] = min(max(a['end'], a['start'] + .85), b['start'])
    merged = []
    for cap in captions:
        if (merged and len(cap['text'].split()) <= 2 and cap['end'] - cap['start'] < .85 - 1e-8
                and cap['start'] - merged[-1]['end'] < .3
                and len(merged[-1]['text']) + len(cap['text']) < 85):
            merged[-1].update(text=merged[-1]['text'] + ' ' + cap['text'], end=cap['end'])
        else:
            merged.append(cap)
    captions = merged
    # Keep the final alternatives together instead of leaving "ou a" at the previous line.
    first_option = anchor('o rádio a atmosfera')['wordIndex']
    last_option = anchor('ou a sensação de conquistar a cidade')['wordIndex']
    captions = [c for c in captions if c['start'] < words[first_option]['start']]
    for a, b in ((first_option, last_option), (last_option, len(words))):
        captions.append(dict(start=words[a]['start'], end=min(duration, words[b - 1]['end'] + .1),
                             text=' '.join(w['word'] for w in words[a:b])))
    for a, b in zip(captions, captions[1:]):
        a['end'] = min(max(a['end'], a['start'] + .85), b['start'])
    assert all(c['start'] < c['end'] <= duration for c in captions)
    assert all(a['end'] <= b['start'] for a, b in zip(captions, captions[1:]))

    paragraphs = []
    for i, paragraph in enumerate(re.split(r'\n\s*\n', (P / '01_NARRACAO.txt').read_text(encoding='utf8').strip())):
        ref = anchor(' '.join(paragraph.split()[:8]))
        paragraphs.append(dict(paragraph=i + 1, start=ref['frame'] / FPS, fromFrame=ref['frame'], text=paragraph))

    assert shots[0]['fromFrame'] == 0
    assert sum(s['frames'] for s in shots) == total_frames
    assert all(a['end'] == b['start'] for a, b in zip(shots, shots[1:]))
    data = dict(episode='L03', title='Vice City: a cidade voltou, mas o que mudou?', duration=duration,
                frames=total_frames, fps=FPS, width=3840, height=2160, logicalWidth=1920, logicalHeight=1080,
                voice=voice.relative_to(ROOT).as_posix(), alignment=alignment.relative_to(ROOT).as_posix(),
                pathBase='project-root', contractVersion='L03-1920-logical-v1',
                status='final-direction', alignmentStatus='validated-input',
                inputHashes=dict(voice=hashlib.sha256(voice.read_bytes()).hexdigest(),
                                 alignment=hashlib.sha256(alignment.read_bytes()).hexdigest()),
                shots=shots, captions=captions, paragraphs=paragraphs)
    (WORK / 'edicao_l03.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(dict(duration=duration, frames=total_frames, shots=len(shots), captions=len(captions),
                          animationFrames=sum(s['animationFrames'] for s in shots),
                          animated=sum(s['animate'] for s in shots)), ensure_ascii=False))
    for i, s in enumerate(shots):
        print(f'{i:02} {s["start"]:7.3f}–{s["end"]:7.3f} {s["frames"]:4}f {s["anchor"]}')


if __name__ == '__main__':
    build()
