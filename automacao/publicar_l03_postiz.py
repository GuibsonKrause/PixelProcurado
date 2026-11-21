"""Publicacao pontual do L03 pelo Postiz instalado, evitando duplicacao."""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import postiz_shorts as postiz

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / 'producao/L03'
PUBLICATION = EPISODE / 'publicacao'
STATE = PUBLICATION / 'POSTIZ_ESTADO.json'
PAYLOAD = PUBLICATION / 'POSTIZ_ENVIO.json'
VIDEO = EPISODE / 'exportacoes/Pixel_Procurado_L03_4K.mp4'
THUMBNAIL = PUBLICATION / 'capa_youtube.jpg'


def text(name):
    return (PUBLICATION / name).read_text(encoding='utf-8').strip()


def save(state):
    state['updated_at'] = datetime.now(timezone.utc).isoformat()
    temporary = STATE.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(STATE)


def all_posts():
    result = postiz.extract_json(postiz.run_postiz(['posts:list']))
    return result['posts'] if isinstance(result, dict) else result


def matching_posts(integration, title, description):
    matches = []
    for entry in all_posts():
        settings = entry.get('settings') or {}
        if isinstance(settings, str):
            settings = json.loads(settings)
        if (entry.get('integration', {}).get('id') == integration
                and settings.get('title') == title
                and entry.get('content') == description):
            matches.append(entry)
    return matches


def status(state):
    record = state.get('post_id')
    if not record:
        print('Ainda nao ha post registrado para L03.')
        return
    matches = [entry for entry in all_posts() if entry['id'] == record]
    if len(matches) != 1:
        raise postiz.PostizError('Post registrado nao localizado; nao recriar automaticamente.')
    entry = matches[0]
    state['status'] = {key: entry.get(key) for key in
                       ('id', 'state', 'publishDate', 'releaseURL', 'releaseId', 'error')}
    if entry.get('state') == 'PUBLISHED':
        state.setdefault('confirmed_published_at', datetime.now(timezone.utc).isoformat())
        if state.get('last_error'):
            state['resolved_error'] = state.pop('last_error')
    save(state)
    print(json.dumps(state['status'], ensure_ascii=False, indent=2))


def publish(state):
    title = text('01_TITULO.txt')
    description = text('02_DESCRICAO.txt')
    tags = [tag.strip() for tag in text('04_TAGS.txt').split(',') if tag.strip()]
    assert VIDEO.is_file() and THUMBNAIL.is_file()
    assert 2 <= len(title) <= 100 and len(description) <= 5000
    assert len(','.join(tags)) <= 500
    checkpoint = json.loads((EPISODE / 'producao.json').read_text(encoding='utf-8'))
    assert checkpoint['estado'] == 'validado'
    assert checkpoint['validacoes']['video_final']['full_decode_pass']
    integration = postiz.youtube_integration_id()
    schema = postiz.extract_json(postiz.run_postiz(['integrations:settings', integration]))['output']
    assert 'public' in schema['settings']['properties']['type']['enum']
    existing = matching_posts(integration, title, description)
    if len(existing) > 1:
        raise postiz.PostizError('Mais de um post correspondente; revisar sem criar outro.')
    if existing:
        state['post_id'] = existing[0]['id']
        save(state)
        status(state)
        return
    if state.get('post_id') or state.get('creation_attempted_at'):
        raise postiz.PostizError('Criacao anterior registrada sem reconciliacao; nao repetir automaticamente.')
    state.update(episode='L03', integration_id=integration, visibility='public',
                 channel='Pixel Procurado', authorization='Usuario pediu postar agora pelo agendador instalado.')
    save(state)
    for field, path in [('video', VIDEO), ('thumbnail', THUMBNAIL)]:
        if not state.get(field):
            print(f'Enviando {path.name} ao Postiz local...', flush=True)
            state[field] = postiz.upload(path)
            save(state)
    scheduled = datetime.now(timezone.utc) + timedelta(seconds=30)
    payload = {
        'type': 'schedule', 'creationMethod': 'CLI', 'date': scheduled.isoformat(),
        'shortLink': False, 'tags': [],
        'posts': [{
            'integration': {'id': integration},
            'value': [{'content': description, 'image': [{
                'id': state['video']['id'], 'path': state['video']['path']}], 'delay': 0}],
            'settings': {
                '__type': 'youtube', 'title': title, 'type': 'public',
                'selfDeclaredMadeForKids': 'no',
                'tags': [{'value': tag, 'label': tag} for tag in tags],
                'thumbnail': {'id': state['thumbnail']['id'], 'path': state['thumbnail']['path']},
            },
        }],
    }
    PAYLOAD.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state['creation_attempted_at'] = datetime.now(timezone.utc).isoformat()
    state['scheduled_at'] = scheduled.isoformat()
    save(state)
    response = postiz.extract_json(postiz.run_postiz(['posts:create', '--json', str(PAYLOAD)]))
    state['creation_response'] = response
    post_ids = postiz.post_ids({'post': response})
    if len(post_ids) != 1:
        save(state)
        raise postiz.PostizError('Criacao retornou resposta inesperada; reconciliar antes de nova tentativa.')
    state['post_id'] = post_ids[0]
    save(state)
    status(state)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['publish', 'status'])
    parser.add_argument('--confirm-youtube', action='store_true')
    args = parser.parse_args()
    if args.command == 'publish' and not args.confirm_youtube:
        parser.error('publish exige --confirm-youtube')
    state = json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {}
    try:
        publish(state) if args.command == 'publish' else status(state)
    except Exception as error:
        message = str(error)
        postiz.load_env()
        secret = postiz.os.environ.get('POSTIZ_API_KEY')
        if secret:
            message = message.replace(secret, '[redacted]')
        state['last_error'] = message
        save(state)
        print('ERRO: ' + message, file=sys.stderr)
        sys.exit(1)
