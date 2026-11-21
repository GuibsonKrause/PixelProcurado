"""Valida REVISAO_FINAL.json: revisao final so vale com evidencias reais e artefatos atuais.

  py -3.12 automacao/validar_revisao.py producao/L09                 # valida <pasta>/REVISAO_FINAL.json
  py -3.12 automacao/validar_revisao.py producao/L09 --modelo producao/L09/exportacoes/X.mp4 [--cards cards.json]
      imprime um modelo vazio ja com os timecodes minimos (cards.json: lista de segundos, ou {"X.mp4": [...]})

Regras (video de duracao D, medida com PyAV): audio ouvido cobrindo 0-10 s, o final (ultimos 10 s) e ao menos
um trecho por janela de 120 s; ao menos 1 frame por janela de 30 s e 1 por card (-0,3/+1,5 s), cada frame em
imagem propria e existente; legendas com 5+ amostras (inicio/meio/fim) conferidas contra o SRT real; thumbnail
com preview reduzido (<=640 px); sha256 de cada artefato igual ao atual (senao a revisao esta velha).
'aprovado' exige zero problemas abertos de severidade alta/media; 'aprovado_com_ressalvas', zero abertos de alta.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parent
sys.path[:0] = [str(AQUI), str(ROOT / '.production-tools/python'), str(ROOT / '.course-tools')]
from _schema_mini import validar as validar_schema  # noqa: E402

SCHEMA = json.loads((AQUI / 'schemas/revisao.schema.json').read_text(encoding='utf-8'))
JANELA_AUDIO, JANELA_FRAME = 120, 30


def tempo(v):
    """segundos (numero) ou 'mm:ss' / 'hh:mm:ss' -> float; ValueError se invalido."""
    if isinstance(v, (int, float)):
        return float(v)
    return sum(float(p) * 60 ** i for i, p in enumerate(reversed(str(v).split(':'))))


def caminho(c, pasta):
    for base in (ROOT, pasta):
        if (base / c).is_file():
            return base / c
    return None


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for bloco in iter(lambda: f.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


def duracao(p):
    import av
    with av.open(str(p)) as c:
        return c.duration / av.time_base


def largura_imagem(p):
    from PIL import Image
    with Image.open(p) as im:
        im.load()
        return im.width


def ler_srt(p):
    cues = []
    for bloco in re.split(r'\n\s*\n', Path(p).read_text(encoding='utf-8-sig').replace('\r', '')):
        m = re.search(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)\s*\n(.*)', bloco, re.S)
        if m:
            g = [int(x) for x in m.groups()[:8]]
            cues.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                         m.group(9)))
    return cues


def norm(t):
    return re.sub(r'\W+', ' ', t.lower()).strip()


def janelas(d, passo):
    n = max(1, int(-(-d // passo)))
    return [(i * passo, min((i + 1) * passo, d)) for i in range(n)]


def rel(p):
    p = p.resolve()
    return str(p.relative_to(ROOT)).replace('\\', '/') if ROOT in p.parents else str(p)


def modelo(mp4, cards_arq, pasta):
    mp4 = Path(mp4)
    d = duracao(mp4)
    cards = []
    if cards_arq:
        dado = json.loads(Path(cards_arq).read_text(encoding='utf-8'))
        cards = dado.get(mp4.name, []) if isinstance(dado, dict) else dado
    srt = mp4.with_suffix('.srt')
    audio = [{'inicio': 0, 'fim': 10, 'observacao': ''}]
    audio += [{'inicio': round(a + 5, 1), 'fim': round(min(a + 20, d), 1), 'observacao': ''}
              for a, _ in janelas(d, JANELA_AUDIO)[1:]]
    audio.append({'inicio': round(max(0, d - 10), 1), 'fim': round(d, 1), 'observacao': ''})
    frames = [{'timecode': round(a + 15 if a + 15 < b else a, 1), 'arquivo_imagem': '', 'observacao': ''}
              for a, b in janelas(d, JANELA_FRAME)]
    frames += [{'timecode': round(tempo(c) + 0.5, 2), 'arquivo_imagem': '', 'observacao': ''} for c in cards]
    return {
        'schema_versao': 1, 'episodio': pasta.name,
        'revisor': {'modelo': '', 'agent_id': ''}, 'data': '',
        'artefatos': [{'caminho': rel(p), 'sha256': sha256(p)} for p in (mp4, srt) if p.exists()],
        'audio_trechos_ouvidos': audio, 'frames_inspecionados': frames,
        'legendas': {'srt': rel(srt),
                     'amostras': [{'timecode': round(d * f, 1), 'texto': '', 'sincronizado': True, 'observacao': ''}
                                  for f in (0.05, 0.3, 0.5, 0.7, 0.95)]},
        'thumbnail': {'arquivo': '', 'preview_reduzido': '', 'observacao': ''},
        'problemas': [], 'resultado': 'reprovado',
    }


def validar_revisao(rev, pasta, cards_arq=None):
    erros = validar_schema(rev, SCHEMA)
    if erros:
        return erros
    E = erros.append
    arts = {}
    for a in rev['artefatos']:
        p = caminho(a['caminho'], pasta)
        if not p:
            E(f'artefato inexistente: {a["caminho"]}')
        elif sha256(p) != a['sha256']:
            E(f'REVISAO VELHA: sha256 de {a["caminho"]} mudou desde a revisao (refaca a revisao do artefato atual)')
        else:
            arts[a['caminho']] = p
    abertos = [p for p in rev['problemas'] if p['status'] == 'aberto']
    res = rev['resultado']
    if res == 'reprovado':
        if not rev['problemas']:
            E('resultado reprovado sem nenhum problema registrado')
        return erros
    if any(p['severidade'] == 'alta' for p in abertos):
        E(f'resultado {res!r} com problema(s) de severidade alta em aberto')
    if res == 'aprovado' and any(p['severidade'] == 'media' for p in abertos):
        E('resultado "aprovado" com problema(s) de severidade media em aberto (use aprovado_com_ressalvas)')
    videos = {c: p for c, p in arts.items() if p.suffix.lower() in ('.mp4', '.mov', '.mkv')}
    if not videos:
        E('nenhum video (mp4/mov/mkv) valido listado em artefatos')
        return erros
    durs = {c: duracao(p) for c, p in videos.items()}
    cards = {}
    if cards_arq:
        dado = json.loads(Path(cards_arq).read_text(encoding='utf-8'))
        cards = dado if isinstance(dado, dict) else {Path(c).name: dado for c in videos}
    else:
        print('AVISO: cards nao conferidos (passe --cards <json com inicios em segundos>).')

    def alvo(item, rotulo):
        c = item.get('artefato')
        if c is None and len(videos) == 1:
            return next(iter(videos))
        if c not in videos:
            E(f'{rotulo}: informe "artefato" com um dos videos revisados ({", ".join(videos)})')
            return None
        return c

    for v, d in durs.items():
        nome = Path(v).name
        ints = []
        for t in rev['audio_trechos_ouvidos']:
            if alvo(t, 'audio_trechos_ouvidos') != v:
                continue
            try:
                i, f = tempo(t['inicio']), tempo(t['fim'])
            except ValueError:
                E(f'audio_trechos_ouvidos: tempo invalido {t}')
                continue
            if f <= i or i < 0 or f > d + 1:
                E(f'audio_trechos_ouvidos: intervalo invalido {i}-{f} ({nome} tem {d:.1f}s)')
            else:
                ints.append((i, f))

        def coberto(a, b):
            pos = a
            for i, f in sorted(ints):
                if i <= pos + 0.5:
                    pos = max(pos, f)
            return pos >= b - 0.5
        if not coberto(0, min(10, d)):
            E(f'{nome}: audio do gancho (0-10s) nao coberto')
        if not coberto(max(0, d - 10), d):
            E(f'{nome}: audio do final ({max(0, d - 10):.0f}-{d:.0f}s) nao coberto')
        for a, b in janelas(d, JANELA_AUDIO):
            if not any(i < b and f > a for i, f in ints):
                E(f'{nome}: nenhum trecho de audio ouvido na janela {a}-{b:.0f}s')

        tcs, usados = [], set()
        for fr in rev['frames_inspecionados']:
            if alvo(fr, 'frames_inspecionados') != v:
                continue
            try:
                tc = tempo(fr['timecode'])
            except ValueError:
                E(f'frames_inspecionados: timecode invalido {fr["timecode"]!r}')
                continue
            img = caminho(fr['arquivo_imagem'], pasta)
            if not img:
                E(f'frame {tc}s: imagem inexistente: {fr["arquivo_imagem"]}')
            elif img.stat().st_size < 1000:
                E(f'frame {tc}s: imagem pequena demais: {fr["arquivo_imagem"]}')
            elif img in usados:
                E(f'frame {tc}s: mesma imagem usada em mais de um frame ({fr["arquivo_imagem"]}); um arquivo por frame')
            else:
                usados.add(img)
                tcs.append(tc)
        for a, b in janelas(d, JANELA_FRAME):
            if not any(a <= t < b or (b >= d and t >= a) for t in tcs):
                E(f'{nome}: nenhum frame inspecionado na janela {a}-{b:.0f}s')
        for c in cards.get(nome, []):
            c = tempo(c)
            if not any(c - 0.3 <= t <= c + 1.5 for t in tcs):
                E(f'{nome}: card em {c:.1f}s sem frame inspecionado ({c - 0.3:.1f}-{c + 1.5:.1f}s)')

    leg = rev['legendas']
    srt = arts.get(leg['srt'])
    if not srt:
        E(f'legendas.srt precisa estar em artefatos (com sha256) e existir: {leg["srt"]}')
    else:
        cues = ler_srt(srt)
        d = max(durs.values())
        am = leg['amostras']
        if len(am) < 5:
            E(f'legendas: minimo de 5 amostras (tem {len(am)})')
        for faixa, (lo, hi) in {'inicio': (0, .2), 'meio': (.4, .6), 'fim': (.8, 1.01)}.items():
            if not any(lo * d <= tempo(x['timecode']) < hi * d for x in am):
                E(f'legendas: sem amostra no {faixa} do video')
        for x in am:
            tc = tempo(x['timecode'])
            ativos = [norm(t) for i, f, t in cues if i - 1.5 <= tc <= f + 1.5]
            if not any(norm(x['texto']) in t for t in ativos):
                E(f'legendas: texto da amostra em {tc:.1f}s nao confere com o SRT real ({x["texto"]!r})')
            if not x['sincronizado']:
                E(f'legendas: amostra em {tc:.1f}s marcada como NAO sincronizada')

    th = rev['thumbnail']
    if th['arquivo'] not in arts:
        E(f'thumbnail.arquivo precisa estar em artefatos (com sha256) e existir: {th["arquivo"]}')
    pv = caminho(th['preview_reduzido'], pasta)
    if not pv:
        E(f'thumbnail.preview_reduzido inexistente: {th["preview_reduzido"]}')
    else:
        try:
            if largura_imagem(pv) > 640:
                E('thumbnail.preview_reduzido deve ter no maximo 640 px de largura (teste de leitura em miniatura)')
        except Exception as ex:
            E(f'thumbnail.preview_reduzido ilegivel: {ex}')
    return erros


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('alvo', help='pasta do episodio ou REVISAO_FINAL.json')
    ap.add_argument('--modelo', metavar='VIDEO', help='imprime modelo vazio para este video')
    ap.add_argument('--cards', help='JSON com inicios (s) dos cards')
    a = ap.parse_args()
    p = Path(a.alvo)
    pasta = p if p.is_dir() else p.parent
    if a.modelo:
        print(json.dumps(modelo(a.modelo, a.cards, pasta), ensure_ascii=False, indent=2))
        return 0
    arq = p / 'REVISAO_FINAL.json' if p.is_dir() else p
    if not arq.exists():
        print(f'REPROVADA: {arq} nao existe. Revisao final exige relatorio com evidencias (use --modelo).')
        return 1
    erros = validar_revisao(json.loads(arq.read_text(encoding='utf-8')), pasta, a.cards)
    for e in erros:
        print('ERRO:', e)
    print(f'{arq}: ' + (f'REPROVADA pelo validador ({len(erros)} problema(s))' if erros else 'evidencias OK'))
    return 1 if erros else 0


if __name__ == '__main__':
    sys.exit(main())
