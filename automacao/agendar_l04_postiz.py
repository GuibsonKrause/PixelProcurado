"""Agenda apenas L04 na data explicitamente solicitada, sem duplicação."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import postiz_shorts as postiz

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'producao/L04'
PUB = EP / 'publicacao'
STATE = EP / 'POSTIZ_ESTADO.json'
WHEN = datetime.fromisoformat('2026-11-01T12:00:00-03:00')

def read(path):
    return path.read_text(encoding='utf-8-sig').strip()

def save(state):
    temporary = STATE.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(STATE)

def posts():
    result = postiz.extract_json(postiz.run_postiz([
        'posts:list', '--startDate', '2026-10-30T00:00:00-03:00',
        '--endDate', '2026-11-03T00:00:00-03:00']))
    return result['posts']

def run(command, state):
    if command == 'check':
        print(json.dumps(postiz.integrations(), ensure_ascii=False, indent=2))
        return
    if command == 'status':
        matches = [p for p in posts() if p['id'] == state.get('post_id')]
        if len(matches) != 1:
            raise ValueError('Post registrado não localizado; não recriar automaticamente.')
        entry = matches[0]
        settings = entry.get('settings', {})
        if isinstance(settings, str):
            settings = json.loads(settings)
        state['status'] = {k: entry.get(k) for k in ['id','state','publishDate','releaseURL','releaseId','error']}
        state['status']['visibility'] = settings.get('type')
        save(state)
        print(json.dumps(state['status'], ensure_ascii=False, indent=2))
        return
    checkpoint = json.loads(read(EP / 'producao.json'))
    if checkpoint['estado'] != 'validado' or checkpoint['revisao_final']['resultado'] != 'PASS':
        raise ValueError('Vídeo e revisão independente precisam estar validados.')
    video = ROOT / checkpoint['artefatos']['mp4']
    thumbnail = PUB / 'capa_youtube.jpg'
    current_hash = hashlib.sha256(video.read_bytes()).hexdigest()
    if current_hash != checkpoint['sha256_mp4']:
        raise ValueError('MP4 diverge do arquivo validado.')
    item = {'title': read(PUB/'01_TITULO.txt'), 'description': read(PUB/'02_DESCRICAO.txt'),
            'tags': [t.strip() for t in read(PUB/'04_TAGS.txt').split(',') if t.strip()]}
    assert len(item['title']) <= 100 and len(item['description']) <= 5000
    assert len(','.join(item['tags'])) <= 500
    integration = postiz.youtube_integration_id()
    matches = []
    for p in posts():
        settings = p.get('settings') or {}
        if isinstance(settings, str):
            settings = json.loads(settings)
        if p.get('integration',{}).get('id') == integration and settings.get('title') == item['title'] and p.get('content') == item['description']:
            matches.append(p)
    if len(matches) > 1:
        raise ValueError('Posts duplicados correspondentes; revisar antes de agir.')
    if matches:
        state['post_id'] = matches[0]['id']
        save(state)
        return run('status', state)
    if state.get('post_id') or state.get('creation_attempted_at'):
        raise ValueError('Tentativa anterior registrada; reconciliar antes de repetir.')
    if WHEN <= datetime.now(timezone.utc):
        raise ValueError('Horário solicitado já passou; não alterar data automaticamente.')
    for key,path in [('video',video),('thumbnail',thumbnail)]:
        if not state.get(key):
            print(f'Enviando {path.name} ao Postiz...', flush=True)
            state[key] = postiz.upload(path)
            save(state)
    state.update(episode='L04', scheduled_at=WHEN.isoformat(), visibility='public',
                 sha256_mp4=current_hash, creation_attempted_at=datetime.now(timezone.utc).isoformat())
    save(state)
    result = postiz.create_post(item, integration, state['video'], state['thumbnail'], WHEN, 'schedule', 'public')
    state['creation_response'] = result
    ids = postiz.post_ids({'post':result})
    if len(ids) != 1:
        save(state)
        raise ValueError('Resposta inesperada; reconciliar antes de repetir.')
    state['post_id'] = ids[0]
    save(state)
    run('status',state)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check','schedule','status'])
    parser.add_argument('--confirm-youtube', action='store_true')
    args = parser.parse_args()
    if args.command == 'schedule' and not args.confirm_youtube:
        parser.error('schedule exige --confirm-youtube')
    state = json.loads(read(STATE)) if STATE.exists() else {}
    run(args.command,state)
