"""Distribuição L06 por Postiz. O padrão é plan; publish exige QA assinada."""
import argparse
import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4

import postiz_shorts as postiz
from distribuir_l05_postiz import ROOT, command, digest, metadata, read, write
from r2_media import R2Media

EP = ROOT / 'producao/L06'
SOCIAL = EP / 'social'
STATE = SOCIAL / 'POSTIZ_ESTADO.json'
QA = SOCIAL / 'QA_FINAL.json'
MASTER = EP / 'exportacoes/Pixel_Procurado_L06_4K.mp4'
CHANNELS = {
    'youtube': 'cmvsctfgl0001jncj932ovibv',
    'facebook': 'cmvzyur290001pddwolrt33em',
    'instagram': 'cmvzyw7vj0003pddwkgtivv8i',
}
CARDS = tuple(SOCIAL / f'L06_Carrossel_{i:02d}.jpg' for i in range(1, 5))
STORY = SOCIAL / 'L06_Story_1080x1920.jpg'
FB = SOCIAL / 'L06_Facebook_1080p.mp4'
VERTICAL = SOCIAL / 'L06_Vice_City_Port_Gellhorn_1080x1920.mp4'
SOURCES = {
    'youtube_longo': (MASTER,),
    'youtube_short': (VERTICAL,),
    'facebook_integral': (FB,),
    'facebook_story': (STORY,),
    'facebook_multifoto': CARDS,
    'instagram_reel': (VERTICAL,),
    'instagram_integral': (SOCIAL / 'L06_Instagram_Integral_1080x1920_Leve.mp4',),
    'instagram_story': (STORY,),
    'instagram_carrossel': CARDS,
}
THUMB = EP / 'publicacao/capa_youtube.jpg'
L06_COPY = ('Leonida muda de clima sem mudar de estado. Nas Keys, o olhar vai até o horizonte. '
            'Em Grassrivers, a vegetação esconde o que vem depois. A Rockstar usa a paisagem '
            'para criar sensações diferentes em cada região. Qual seria a sua primeira parada?\n\n'
            'Análise visual de material promocional de GTA VI. Imagens: Rockstar Games. '
            'Fonte: https://www.rockstargames.com/VI/media\nNarração sintética com auxílio de IA.\n\n#GTA6 #GTAVI #PixelProcurado')
CAROUSEL_COPY = ('Leonida em três contrastes: horizonte e vegetação, dois jeitos de iluminar '
                 'a cidade, indústria e montanha. Veja os seis lugares lado a lado. '
                 'Qual seria a sua primeira parada?\n\n'
                 'Imagens: Rockstar Games. Leitura visual do material promocional de GTA VI. '
                 'Fonte: https://www.rockstargames.com/VI/media\n\n#GTA6 #PixelProcurado')
VERTICAL_TITLE = 'Vice City e Port Gellhorn brilham por motivos diferentes'
VERTICAL_COPY = ('Em Vice City, a fachada do Ocean View faz a rua virar espetáculo. '
                 'Em Port Gellhorn, o letreiro do Starlet Motel se destaca no entorno. '
                 'O que muda na sua leitura da cena?\n\n'
                 'Trecho de Leonida além de Vice City, do Pixel Procurado. '
                 'Imagens oficiais de GTA VI: https://www.rockstargames.com/VI/media\n'
                 'Narração sintética com auxílio de IA.\n\n'
                 '#GTA6 #GTAVI #PixelProcurado')
ALT = (
    'Capa Leonida além de Vice City. Imagens de Leonida Keys e Grassrivers.',
    'Horizonte aberto nas Leonida Keys e margens fechadas pela vegetação em Grassrivers.',
    'Fachadas iluminadas de Vice City e o letreiro de motel em Port Gellhorn.',
    'Linhas industriais em Ambrosia e estrada ao lado dos paredões em Mount Kalaga.',
)


def run_cli(args):
    return postiz.extract_json(postiz.run_postiz(args))


def remote_posts():
    now = datetime.now(timezone.utc)
    # Consulta janelas mensais para abranger a história recente dos cortes e posts futuros.
    cursor = (now - timedelta(days=90)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    limit = now + timedelta(days=60)
    rows = {}
    while cursor < limit:
        end = (cursor + timedelta(days=32)).replace(day=1)
        result = run_cli(['posts:list', '--startDate', cursor.isoformat(), '--endDate', end.isoformat()])
        for item in result['posts'] if isinstance(result, dict) else result:
            rows[item['id']] = item
        cursor = end
    return list(rows.values())


def normalized(value):
    return unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode().lower()


def discover():
    integrations = postiz.integrations()
    active = [item for item in integrations if not item.get('disabled')]
    enabled = {item['identifier']: item['id'] for item in active}
    if enabled != CHANNELS or len(active) != len(CHANNELS):
        raise ValueError(f'Integrações ativas divergiram da matriz revisada: {list(enabled)}')
    schemas = {provider: run_cli(['integrations:settings', channel])
               for provider, channel in CHANNELS.items()}
    for provider in ('facebook', 'instagram'):
        settings = schemas[provider]['output']['settings']['properties']
        if not {'post', 'story'} <= set(settings['post_type']['enum']):
            raise ValueError(f'{provider} não oferece post e story no schema atual.')
    posts = remote_posts()
    terms = ('iguana', 'grassrivers', 'leonida keys', 'l06')
    matches = []
    for entry in posts:
        if any(term in normalized(entry.get('content')) for term in terms):
            matches.append({k: entry.get(k) for k in
                            ('id', 'integration', 'state', 'releaseURL', 'content', 'settings')})
    write(SOCIAL / 'CAPACIDADES_POSTIZ.json',
          {'checked_at': datetime.now(timezone.utc).isoformat(),
           'enabled': enabled, 'schemas': schemas, 'remote_posts_checked': len(posts),
           'potential_matches': matches})
    print(f'{len(enabled)} integrações; {len(posts)} posts consultados; {len(matches)} coincidências temáticas.')
    return posts


def plan():
    write(SOCIAL / 'PLANO_POSTIZ.json',
          {name: {'integration': CHANNELS[name.split('_')[0]],
                  'files': [str(path.relative_to(ROOT)) for path in paths],
                  'ready': all(path.is_file() for path in paths)}
           for name, paths in SOURCES.items()})


def derive():
    SOCIAL.mkdir(parents=True, exist_ok=True)
    before = digest(MASTER)
    manifest_path = SOCIAL / 'DERIVACOES_QA.json'
    previous = json.loads(read(manifest_path)) if manifest_path.exists() else {}
    decoded = set()
    if not (FB.exists() and previous.get('master_sha256') == before and
            previous.get('assets', {}).get('facebook_integral', {}).get('sha256') == digest(FB)):
        temp = FB.with_suffix('.rendering.mp4')
        command(['-hide_banner', '-loglevel', 'error', '-y', '-hwaccel', 'qsv',
                 '-hwaccel_output_format', 'qsv', '-i', str(MASTER),
                 '-map', '0:v:0', '-map', '0:a:0', '-vf', 'scale_qsv=w=1920:h=1080:format=nv12',
                 '-c:v', 'h264_qsv', '-preset', 'veryfast', '-b:v', '3200k',
                 '-maxrate', '4800k', '-bufsize', '9600k', '-c:a', 'aac',
                 '-b:a', '128k', '-movflags', '+faststart', str(temp)])
        command(['-v', 'error', '-xerror', '-i', str(temp), '-f', 'null', '-'])
        decoded.add(FB)
        temp.replace(FB)
    report = {'master_sha256': before, 'assets': {}}
    for name in ('facebook_integral', 'youtube_short'):
        path = SOURCES[name][0]
        sha = digest(path)
        old = previous.get('assets', {}).get(name, {})
        vertical = json.loads(read(SOCIAL / 'VERTICAL_QA.json')) if path == VERTICAL else {}
        verified = any(record.get('sha256') == sha and record.get('full_decode_pass')
                       for record in (old, vertical))
        if path not in decoded and not verified:
            command(['-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'])
        meta = metadata(path)
        expected = (1920, 1080) if name == 'facebook_integral' else (1080, 1920)
        if (meta['width'], meta['height']) != expected or not (meta['h264'] and meta['aac']):
            raise ValueError(f'Mídia de vídeo incompatível: {name}')
        if name == 'facebook_integral' and abs(meta['duration'] - metadata(MASTER)['duration']) > .2:
            raise ValueError('A duração da cópia de Facebook difere do master.')
        if name != 'facebook_integral' and not 3 <= meta['duration'] <= 180:
            raise ValueError(f'Duração vertical fora do intervalo: {name}')
        report['assets'][name] = {**meta, 'sha256': sha, 'full_decode_pass': True}
    report['assets']['instagram_reel'] = report['assets']['youtube_short']
    if digest(MASTER) != before:
        raise ValueError('Master mudou durante as derivações.')
    write(manifest_path, report)
    plan()


def checksums():
    derived = json.loads(read(SOCIAL / 'DERIVACOES_QA.json'))
    cards = json.loads(read(SOCIAL / 'CARTOES_QA.json'))['assets']
    master_sha256 = digest(MASTER)
    if derived['master_sha256'] != master_sha256:
        raise ValueError('Derivações foram feitas de outro master.')
    assets = {}
    hashes = {}
    for name, paths in SOURCES.items():
        assets[name] = []
        for path in paths:
            if path not in hashes:
                hashes[path] = digest(path)
            sha = hashes[path]
            if path.suffix == '.jpg' and cards.get(path.name) != sha:
                raise ValueError(f'Cartão atualizado depois da validação: {path.name}')
            if name in derived['assets'] and derived['assets'][name]['sha256'] != sha:
                raise ValueError(f'MP4 atualizado depois da validação: {path.name}')
            assets[name].append(sha)
    write(SOCIAL / 'QA_PENDENTE.json',
          {'approved': False, 'source_sha256': master_sha256,
           'thumbnail_sha256': digest(THUMB), 'assets': assets})
    print(f'{len(assets)} destinos, {len(hashes)} arquivos únicos. Revisão final ainda pendente.')


def payload(name, media, thumbnail=None):
    provider, kind = name.split('_', 1)
    settings = {'__type': provider, 'post_type': 'story' if kind == 'story' else 'post'}
    content = L06_COPY
    if provider == 'youtube':
        if kind == 'longo':
            pub = EP / 'publicacao'
            title = read(pub / '01_TITULO.txt')
            content = read(pub / '02_DESCRICAO.txt')
            tags = [tag.strip() for tag in read(pub / '04_TAGS.txt').split(',') if tag.strip()]
        else:
            title, content = VERTICAL_TITLE, VERTICAL_COPY + ' #Shorts'
            tags = ['GTA 6', 'GTA VI', 'Vice City', 'Port Gellhorn', 'Pixel Procurado']
        settings = {'__type': 'youtube', 'title': title, 'type': 'public',
                    'selfDeclaredMadeForKids': 'no',
                    'tags': [{'value': tag, 'label': tag} for tag in tags]}
        if thumbnail:
            settings['thumbnail'] = thumbnail
        if not (2 <= len(title) <= 100 and len(content) <= 5000 and len(','.join(tags)) <= 500):
            raise ValueError(f'Metadados YouTube inválidos: {name}')
    elif kind == 'integral':
        if provider == 'facebook':
            settings['title'] = read(EP / 'publicacao/01_TITULO.txt')
        else:
            content = ('Episódio completo | Leonida além de Vice City.\n\n'
                       'Do mar aberto das Keys ao pântano de Grassrivers, passando pelas luzes '
                       'de Vice City e Port Gellhorn, pela indústria de Ambrosia e pelas montanhas '
                       'de Kalaga. O que muda no seu olhar a cada paisagem?\n\n'
                       'Análise visual das imagens promocionais de GTA VI. Imagens: Rockstar Games. '
                       'Narração sintética com auxílio de IA.\n\n#GTA6 #GTAVI #PixelProcurado')
    elif kind == 'story':
        content = 'Do horizonte ao pântano | Pixel Procurado L06'
    elif kind == 'reel':
        content = VERTICAL_COPY
    elif kind in ('carrossel', 'multifoto'):
        content = CAROUSEL_COPY
    if kind == 'carrossel':
        media = [{**asset, 'alt': alt} for asset, alt in zip(media, ALT, strict=True)]
    if provider == 'instagram' and len(content) > 2200:
        raise ValueError(f'Legenda Instagram acima do limite: {name}')
    return {'integration': {'id': CHANNELS[provider]},
            'value': [{'content': content, 'image': media, 'delay': 0}], 'settings': settings}


def comparable(entry, target):
    if (entry.get('integration') or {}).get('id') != target['integration']['id']:
        return False
    settings = entry.get('settings') or {}
    if isinstance(settings, str):
        settings = json.loads(settings)
    spec = target['settings']
    text = target['value'][0]['content']
    remote = str(entry.get('content', '')).replace('<br>', '\n')
    return (settings.get('post_type', 'post') == spec.get('post_type', 'post') and
            (remote.strip() == text.strip() or
             spec['__type'] == 'youtube' and settings.get('title') == spec['title']))


def verified_ig_media(url, path, sha):
    uri = urlsplit(url)
    if (uri.scheme != 'https' or not uri.hostname or not uri.hostname.endswith('.trycloudflare.com')
            or uri.username or uri.password or uri.query or uri.fragment
            or not re.fullmatch(r'/[a-f0-9]{40}/L06[.]mp4', uri.path)):
        raise ValueError('URL temporária do Reel inválida.')
    total = path.stat().st_size
    with urlopen(Request(url, headers={'Range': 'bytes=1048576-1048831'}), timeout=30) as response:
        if (response.status != 206 or response.headers.get('Content-Type') != 'video/mp4'
                or response.headers.get('Content-Range') != f'bytes 1048576-1048831/{total}'
                or len(response.read()) != 256):
            raise ValueError('O servidor temporário não fornece intervalos HTTP válidos.')
    with urlopen(url, timeout=45) as response:
        h = hashlib.sha256()
        while chunk := response.read(1024 * 1024):
            h.update(chunk)
        if (response.status != 200 or response.headers.get('Content-Type') != 'video/mp4'
                or response.headers.get('Content-Length') != str(total) or h.hexdigest() != sha):
            raise ValueError('O arquivo servido via HTTPS diverge da revisão.')
    return {'id': '', 'path': url}


def publish(names, retry_failed_download=False, media_url=None):
    gate = json.loads(read(QA))
    if gate.get('approved') is not True or gate.get('source_sha256') != digest(MASTER):
        raise ValueError('Revisão final aprovada e hash atual do master são obrigatórios.')
    if gate.get('thumbnail_sha256') != digest(THUMB):
        raise ValueError('Thumbnail diverge da aprovada.')
    for name in names:
        if gate.get('assets', {}).get(name) != [digest(path) for path in SOURCES[name]]:
            raise ValueError(f'Mídia diverge da aprovada: {name}')
    temporary_media = (verified_ig_media(media_url, SOURCES['instagram_integral'][0],
                                         gate['assets']['instagram_integral'][0])
                       if media_url else None)
    posts = discover()
    state = json.loads(read(STATE)) if STATE.exists() else {'episode': 'L06', 'items': {}}
    media_cache = state.setdefault('media_by_sha256', {})
    r2 = None
    errors = []
    for name in names:
        rec = state['items'].setdefault(name, {})
        try:
            thumbnail = {'id': '', 'path': 'PENDING'} if name == 'youtube_longo' else None
            target = payload(name, [{'id': '', 'path': 'PENDING'} for _ in SOURCES[name]], thumbnail)
            if retry_failed_download:
                prior_id = rec.get('post_id')
                prior = next((entry for entry in posts if entry['id'] == prior_id), None)
                others = [entry for entry in posts
                          if entry['id'] != prior_id and comparable(entry, target)]
                if (not prior or rec.get('previous_attempts') or others
                        or not comparable(prior, target) or prior.get('state') != 'ERROR'
                        or prior.get('error') != 'Instagram Video download failed'
                        or prior.get('releaseId') or prior.get('releaseURL')):
                    raise ValueError('Post anterior não é uma falha exclusiva de download sem publicação.')
                rec['remote'] = {k: prior.get(k) for k in
                                 ('state', 'releaseURL', 'releaseId', 'error', 'publishDate')}
                rec = {'previous_attempts': [rec]}
                state['items'][name] = rec
                write(STATE, state)
            ignored = {entry['post_id'] for entry in rec.get('previous_attempts', [])}
            for entry in posts:
                if entry['id'] in ignored and (entry.get('state') != 'ERROR'
                                                or entry.get('releaseId') or entry.get('releaseURL')):
                    raise ValueError('Uma tentativa anteriormente encerrada mudou de estado.')
            identity = {'payload': target, 'media_sha256': gate['assets'][name],
                        'thumbnail_sha256': gate['thumbnail_sha256'] if thumbnail else None}
            if rec.get('identity', identity) != identity:
                raise ValueError('Artefato ou conteúdo mudou após tentativa; reconciliar.')
            rec['identity'] = identity
            matches = [entry for entry in posts if entry['id'] not in ignored
                       and (comparable(entry, target) or entry['id'] == rec.get('post_id'))]
            if len(matches) > 1:
                raise ValueError('Mais de um post equivalente no histórico.')
            if matches:
                rec.update(post_id=matches[0]['id'], remote={k: matches[0].get(k) for k in
                           ('state', 'releaseURL', 'releaseId', 'error', 'publishDate')})
                write(STATE, state)
                print(name, rec['remote'], flush=True)
                continue
            if rec.get('post_id') or rec.get('creation_attempted_at'):
                raise ValueError('Tentativa anterior ambígua; reconciliar antes de reenviar.')
            if temporary_media:
                media = [temporary_media]
            elif name.startswith('youtube_'):
                uploads = rec.setdefault('uploads', [])
                for path, sha in zip(SOURCES[name][len(uploads):], gate['assets'][name][len(uploads):], strict=True):
                    if sha not in media_cache:
                        media_cache[sha] = postiz.upload(path)
                    uploads.append(media_cache[sha])
                    write(STATE, state)
                media = uploads
            else:
                if 'r2_keys' not in rec:
                    rec['r2_keys'] = [f'publicacoes/{uuid4().hex}{path.suffix.lower()}' for path in SOURCES[name]]
                    write(STATE, state)
                r2 = r2 or R2Media()
                media = [r2.stage(path, key)[0] for path, key in zip(SOURCES[name], rec['r2_keys'], strict=True)]
            if name == 'youtube_longo' and not rec.get('thumbnail'):
                rec['thumbnail'] = postiz.upload(THUMB)
                write(STATE, state)
            data = {'type': 'now', 'creationMethod': 'CLI',
                    'date': datetime.now(timezone.utc).isoformat(), 'shortLink': False, 'tags': [],
                    'posts': [payload(name, media, rec.get('thumbnail'))]}
            target_file = SOCIAL / f'{name}_ENVIO.json'
            write(target_file, data)
            rec['creation_attempted_at'] = data['date']
            write(STATE, state)
            rec['response'] = run_cli(['posts:create', '--json', str(target_file)])
            ids = postiz.post_ids({'post': rec['response']})
            if len(ids) != 1:
                raise ValueError('Resposta inesperada. Verificar estado antes de repetir.')
            rec['post_id'] = ids[0]
            write(STATE, state)
            print(name, 'aceito pelo Postiz', ids[0], flush=True)
        except Exception as exc:
            errors.append(f'{name}: {exc}')
            rec['last_error'] = str(exc)
            write(STATE, state)
    if errors:
        raise RuntimeError('\n'.join(errors))


def status():
    state = json.loads(read(STATE)) if STATE.exists() else {'items': {}}
    by_id = {entry['id']: entry for entry in remote_posts()}
    r2 = None
    for name, rec in state['items'].items():
        entry = by_id.get(rec.get('post_id'))
        if entry:
            rec['remote'] = {key: entry.get(key) for key in ('state', 'releaseURL', 'releaseId', 'error', 'publishDate')}
            if (entry.get('state') == 'PUBLISHED' and entry.get('releaseURL')
                    and rec.get('r2_keys') and not rec.get('r2_cleaned_at')):
                try:
                    r2 = r2 or R2Media()
                    for key in rec['r2_keys']:
                        r2.remove(key)
                except Exception as exc:
                    print(name, 'limpeza R2 pendente:', type(exc).__name__, flush=True)
                else:
                    rec['r2_cleaned_at'] = datetime.now(timezone.utc).isoformat()
        print(name, rec.get('post_id'), rec.get('remote'), flush=True)
    if state['items']:
        write(STATE, state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs='?', choices=('plan', 'discover', 'derive', 'checksums', 'publish', 'status'), default='plan')
    parser.add_argument('--coordinator-approved', action='store_true')
    parser.add_argument('--only', nargs='+', choices=list(SOURCES))
    parser.add_argument('--retry-failed-download', action='store_true')
    parser.add_argument('--temporary-instagram-media-url')

    args = parser.parse_args()
    if args.command != 'publish':
        {'plan': plan, 'discover': discover, 'derive': derive, 'checksums': checksums, 'status': status}[args.command]()
        return
    if args.temporary_instagram_media_url and not args.retry_failed_download:
        parser.error('URL temporária exige a reconciliação da falha de download.')
    if args.retry_failed_download and args.only != ['instagram_integral']:
        parser.error('Retry autorizado somente para instagram_integral.')
    if not args.coordinator_approved:
        parser.error('publish exige liberação explícita do coordenador e QA_FINAL.json')
    lock = SOCIAL / 'POSTIZ_EXECUCAO.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(fd)
        publish(args.only or list(SOURCES), args.retry_failed_download, args.temporary_instagram_media_url)
    finally:
        lock.unlink()


if __name__ == '__main__':
    main()
