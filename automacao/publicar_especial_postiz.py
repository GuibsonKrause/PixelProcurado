"""Publicação do especial de 06/11/2026, com retomada por ID do Postiz."""

import argparse
import json
import subprocess
from datetime import datetime, timedelta, timezone
from time import sleep
from uuid import uuid4

import postiz_shorts as postiz
from distribuir_l05_postiz import ROOT, write
from distribuir_l06_postiz import CHANNELS, run_cli
from r2_media import R2Media

EP = ROOT / 'producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06'
SOCIAL = EP / 'social'
STATE = SOCIAL / 'POSTIZ_ESTADO.json'
SHORT = SOCIAL / 'Short_9x16.mp4'
LONG = SOCIAL / 'Longo_16x9.mp4'
VERTICAL = SOCIAL / 'Longo_Instagram_Leve.mp4'
TITLES = {
    'longo': 'GTA 6 vai humilhar o seu eu de 2013',
    'short': 'GTA 6: sua roupa pode entregar você',
    'story': 'GTA 6: sua roupa pode entregar você',
}
COPY = {
    'longo': ('Em GTA 6, até a roupa pode entregar você. O que muda quando a fuga pede '
              'planejamento, e como uma camiseta extra vira conselho de mãe?'),
    'short': ('A polícia lembra da sua roupa. Em GTA 6, uma troca no carro pode fazer '
              'parte do plano de fuga. O que você levaria?'),
    'story': 'Uma camiseta extra pode fazer parte da fuga em GTA 6.',
}
CREDIT = ('\n\nAnálise do material de pré-lançamento. Imagens: Rockstar Games.'
          '\n\n#GTA6 #GTAVI #PixelProcurado')
LONG_JOBS = [(provider, 'longo') for provider in CHANNELS]
SHORT_JOBS = [(provider, 'short') for provider in CHANNELS] + [
    ('facebook', 'story'), ('instagram', 'story'),
]


def now():
    return datetime.now(timezone.utc)


def posts():
    current = now()
    result = run_cli(['posts:list', '--startDate', (current - timedelta(days=2)).isoformat(),
                      '--endDate', (current + timedelta(days=2)).isoformat()])
    return result['posts'] if isinstance(result, dict) else result


def discover():
    active = [entry for entry in postiz.integrations() if not entry.get('disabled')]
    if {entry['identifier']: entry['id'] for entry in active} != CHANNELS or len(active) != len(CHANNELS):
        raise ValueError('A matriz de canais ativos mudou; conferir destinos.')
    for provider in ('facebook', 'instagram'):
        result = run_cli(['integrations:settings', CHANNELS[provider]])
        options = result['output']['settings']['properties']['post_type']['enum']
        if not {'post', 'story'} <= set(options):
            raise ValueError(f'{provider} não oferece post e story nesta configuração.')


def text_for(provider, kind):
    return COPY[kind] + (CREDIT if kind != 'story' else '') + (
        ' #Shorts' if provider == 'youtube' and kind == 'short' else '')


def payload(provider, kind, media):
    settings = {'__type': provider, 'post_type': 'story' if kind == 'story' else 'post'}
    if provider == 'youtube':
        settings = {'__type': provider, 'title': TITLES[kind], 'type': 'public',
                    'selfDeclaredMadeForKids': 'no',
                    'tags': [{'value': name, 'label': name}
                             for name in ('GTA 6', 'GTA VI', 'Pixel Procurado')]}
    elif provider == 'facebook' and kind != 'story':
        settings['title'] = TITLES[kind]
    return {'integration': {'id': CHANNELS[provider]},
            'value': [{'content': text_for(provider, kind), 'image': [media], 'delay': 0}],
            'settings': settings}


def stage(state, provider, kind):
    key = f'{provider}_{kind}'
    record = state['items'].setdefault(key, {})
    if record.get('media'):
        return
    path = SHORT if kind != 'longo' else VERTICAL if provider == 'instagram' else LONG
    if not path.is_file():
        raise FileNotFoundError(path.name)
    # Compartilhar o upload interno do curto apenas no YouTube. Cada post Meta tem sua chave.
    if provider == 'youtube':
        record['media'] = postiz.upload(path)
    else:
        record.setdefault('r2_key', f'publicacoes/{uuid4().hex}.mp4')
        write(STATE, state)
        record['media'], _ = R2Media().stage(path, record['r2_key'])
    write(STATE, state)
    print(key, 'mídia disponível', flush=True)


def validate_assets():
    probe = EP / 'montagem/ffprobe.exe'
    for path, dimensions, duration in ((LONG, (1920, 1080), 447.8),
                                       (VERTICAL, (720, 1280), 447.8),
                                       (SHORT, (1080, 1920), 53.03)):
        output = subprocess.check_output([str(probe), '-v', 'error', '-show_streams',
                                          '-show_format', '-of', 'json', str(path)])
        report = json.loads(output)
        streams = {stream['codec_type']: stream for stream in report['streams']}
        video = streams['video']
        if ((video['width'], video['height']) != dimensions or video['codec_name'] != 'h264'
                or streams['audio']['codec_name'] != 'aac'
                or abs(float(report['format']['duration']) - duration) > .12):
            raise ValueError(f'Derivação incompatível: {path.name}')


def send(state, jobs, due=None):
    existing = posts()
    for provider, kind in jobs:
        key = f'{provider}_{kind}'
        record = state['items'][key]
        if record.get('post_id'):
            continue
        content = text_for(provider, kind)
        matches = [row for row in existing
                   if (row.get('integration') or {}).get('id') == CHANNELS[provider]
                   and row.get('content') == content]
        if len(matches) == 1:
            record['post_id'] = matches[0]['id']
            write(STATE, state)
            continue
        if matches or record.get('attempted_at'):
            raise RuntimeError(f'{key}: reconciliar tentativa anterior antes de reenviar.')
        date = (due or now()).isoformat()
        data = {'type': 'schedule' if due else 'now', 'creationMethod': 'CLI',
                'date': date, 'shortLink': False, 'tags': [],
                'posts': [payload(provider, kind, record['media'])]}
        target = SOCIAL / f'{key}_ENVIO.json'
        write(target, data)
        record['attempted_at'] = now().isoformat()
        write(STATE, state)
        result = run_cli(['posts:create', '--json', str(target)])
        ids = postiz.post_ids({'post': result})
        if len(ids) != 1:
            raise RuntimeError(f'{key}: resposta ambígua, consulte o Postiz.')
        record['post_id'] = ids[0]
        write(STATE, state)
        print(key, 'aceito', ids[0], date, flush=True)


def refresh(state, jobs):
    remote = {row['id']: row for row in posts()}
    statuses = {}
    for provider, kind in jobs:
        key = f'{provider}_{kind}'
        record = state['items'].get(key, {})
        row = remote.get(record.get('post_id'), {})
        if row:
            record['remote'] = {k: row.get(k) for k in
                                ('state', 'releaseURL', 'releaseId', 'error', 'publishDate')}
        statuses[key] = record.get('remote', {}).get('state')
        if (statuses[key] == 'PUBLISHED' and row.get('releaseURL')
                and record.get('r2_key') and not record.get('r2_removed')):
            try:
                R2Media().remove(record['r2_key'])
                record['r2_removed'] = True
            except Exception as exc:
                print(key, 'limpeza R2 pendente', type(exc).__name__, flush=True)
    write(STATE, state)
    print(statuses, flush=True)
    return statuses


def wait_for(state, jobs, deadline):
    while now() < deadline:
        statuses = refresh(state, jobs)
        if all(value == 'PUBLISHED' for value in statuses.values()):
            return
        if 'ERROR' in statuses.values():
            raise RuntimeError('Postiz registrou falha. Conferir o estado salvo.')
        sleep(90)
    raise TimeoutError('Ainda há publicações sem confirmação no Postiz.')


def revise_queue(state):
    thumb = postiz.upload(SOCIAL / 'capas/short_vertical/capa_youtube.jpg')
    for provider in ('youtube', 'facebook', 'instagram'):
        key = f'{provider}_short'
        record = state['items'][key]
        row = next(entry for entry in posts() if entry['id'] == record['post_id'])
        if row['state'] != 'QUEUE' or datetime.fromisoformat(row['publishDate'].replace('Z', '+00:00')) <= now():
            print(key, 'fora da fila editável', row['state'], flush=True)
            continue
        item = payload(provider, 'short', record['media'])
        item['group'] = row['group']
        item['value'][0]['id'] = row['id']
        if provider == 'youtube':
            item['settings']['thumbnail'] = thumb
        data = {'type': 'update', 'date': row['publishDate'], 'shortLink': False,
                'tags': [], 'posts': [item]}
        target = SOCIAL / f'{key}_REVISAO.json'
        write(target, data)
        result = run_cli(['posts:create', '--json', str(target)])
        updated = next(entry for entry in posts() if entry['id'] == row['id'])
        if (updated['state'] != 'QUEUE' or updated['publishDate'] != row['publishDate']
                or 'auxílio de IA' in updated['content']):
            raise RuntimeError(f'{key}: atualização não confirmada no mesmo agendamento.')
        if provider == 'youtube':
            settings = updated['settings']
            if isinstance(settings, str):
                settings = json.loads(settings)
            if settings.get('thumbnail', {}).get('path') != thumb['path']:
                raise RuntimeError(f'{key}: capa não consta na configuração.')
        print(key, 'atualizado no mesmo horário', updated['publishDate'], flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('publish', 'status', 'revise-queue'))
    args = parser.parse_args()
    SOCIAL.mkdir(exist_ok=True)
    state = json.loads(STATE.read_text(encoding='utf-8-sig')) if STATE.exists() else {'items': {}}
    if args.action == 'status':
        refresh(state, LONG_JOBS + SHORT_JOBS)
        return
    if args.action == 'revise-queue':
        revise_queue(state)
        return
    validate_assets()
    discover()
    for provider, kind in LONG_JOBS:
        stage(state, provider, kind)
    send(state, LONG_JOBS)
    wait_for(state, LONG_JOBS, now() + timedelta(minutes=20))
    if 'short_due_utc' not in state:
        state['short_due_utc'] = (now() + timedelta(minutes=30)).isoformat()
        write(STATE, state)
    due = datetime.fromisoformat(state['short_due_utc'])
    for provider, kind in SHORT_JOBS:
        stage(state, provider, kind)
    send(state, SHORT_JOBS, due if due > now() else None)
    print('Horário do curto e Stories (UTC):', due.isoformat(), flush=True)
    sleep(max(0, (due - now()).total_seconds()))
    wait_for(state, SHORT_JOBS, now() + timedelta(minutes=20))


if __name__ == '__main__':
    main()
