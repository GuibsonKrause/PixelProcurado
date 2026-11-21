"""Plano local e envio retomável do Dia 01 pelos clientes Postiz/R2 existentes."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from uuid import uuid4

from dia01_validar import BASE
from PIL import Image
import postiz_shorts as postiz
from distribuir_l05_postiz import digest, write
from distribuir_l06_postiz import run_cli
from publicar_especial_postiz import now, posts
from r2_media import R2Media

PUB = BASE / 'publicacao'
DRY = PUB / 'POSTIZ_DRY_RUN.json'
STATE = PUB / 'POSTIZ_ESTADO.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save_state(state):
    temporary = STATE.with_suffix('.tmp')
    write(temporary, state)
    temporary.replace(STATE)


def compatible_cover(source):
    if source.suffix.lower() in ('.jpg', '.jpeg') and source.stat().st_size <= 2_000_000:
        return source
    target = PUB / f'{source.parent.name}_{source.stem}_postiz.jpg'
    with Image.open(source) as source_image:
        rgb = source_image.convert('RGB')
        for quality in (96, 92, 88, 84, 80):
            rgb.save(target, quality=quality, optimize=True, subsampling=0)
            if target.stat().st_size <= 2_000_000:
                return target
    raise ValueError(f'Capa excede 2 MB: {source.name}')


def dry_run():
    plan = read(PUB / 'PLANO_POSTIZ_DIA01.json')
    pack = read(BASE / plan['metadata'])
    social = read(BASE / plan['social_metadata'])
    description = (BASE / pack['descricao_efetiva_para_publicar']).read_text(encoding='utf-8-sig').strip()
    title = pack['titulos_ab'][0]['titulo']
    assert len(title) <= 100 and len(description.encode('utf-8')) <= 5000
    tags = [{'label': tag, 'value': tag} for tag in pack['tags']]
    assert tags and len(','.join(tag['value'] for tag in tags)) <= 500
    chapters = [line.strip() for line in pack['capitulos'].splitlines() if line.strip()]
    assert all(line in description for line in chapters)
    times = []
    for line in chapters:
        stamp = re.match(r'^(\d{2}):(\d{2})\s', line)
        assert stamp, line
        times.append(int(stamp[1]) * 60 + int(stamp[2]))
    master_qa = read(BASE / 'qa/DIA01_Master_4K/RELATORIO_QA.json')
    assert len(times) >= 3 and times[0] == 0
    assert all(b - a >= 10 for a, b in zip(times, times[1:] + [master_qa['video_duration']]))
    assets, jobs, cover_paths, file_hashes = {}, [], {}, {}
    short_description = social['reel']['description']
    story_description = social['story']['description']
    carousel_description = ('Quatro quadros do gameplay oficial de GTA VI. No carro vermelho, '
                            'você escolheria Smash Window ou Slim Jim? #GTA6 #GTAVI #PixelProcurado')
    meta_long = '\n\n'.join(description.split('\n\n')[:2]) + '\n\n#GTA6 #GTAVI #PixelProcurado'

    def add_asset(path, transport, job_id):
        assert path.is_file() and path.stat().st_size > 0, path
        if path not in file_hashes:
            file_hashes[path] = digest(path)
        sha = file_hashes[path]
        key = f'{transport}:{sha}'
        asset = assets.setdefault(key, {'path': str(path), 'sha256': sha, 'bytes': path.stat().st_size,
                                        'transport': transport, 'needed_by': []})
        if job_id not in asset['needed_by']:
            asset['needed_by'].append(job_id)
        return key

    for row in plan['jobs']:
        job_id = row['id']
        provider, kind = job_id.split('_', 1)
        files = row.get('files') or [row['file']]
        transport = 'postiz' if provider == 'youtube' else 'r2'
        media = [add_asset(BASE / file, transport, job_id) for file in files]
        for file, key in zip(files, media):
            if file.endswith('.mp4'):
                qa = read(BASE / 'qa' / Path(file).stem / 'RELATORIO_QA.json')
                assert qa['full_decode_pass'] and qa['sha256'] == assets[key]['sha256'], file
                if provider == 'instagram':
                    assert assets[key]['bytes'] < 1_000_000_000 and 3 <= qa['video_duration'] <= 900
        settings = {'__type': provider, 'post_type': row.get('post_type', 'post')}
        if provider == 'youtube':
            content = description if kind == 'longo' else short_description + ' #Shorts'
            settings = {'__type': 'youtube', 'title': title if kind == 'longo' else social['reel']['title'],
                        'type': 'public', 'selfDeclaredMadeForKids': 'no', 'tags': tags}
        elif kind == 'integral':
            content = meta_long
        elif kind == 'story':
            content = story_description
        elif kind in ('carrossel', 'multifoto'):
            content = carousel_description
        else:
            content = short_description
        if provider == 'facebook' and kind in ('integral', 'curto'):
            settings['title'] = title if kind == 'integral' else social['reel']['title']
        if provider == 'instagram':
            assert len(content) <= 2200
        cover = None
        if row.get('thumbnail') and provider in ('youtube', 'instagram'):
            source = BASE / row['thumbnail']
            if source not in cover_paths:
                cover_paths[source] = compatible_cover(source)
            cover = add_asset(cover_paths[source], transport, job_id)
        job = {'id': job_id, 'integration_id': plan['channels'][provider], 'provider': provider,
               'media': media, 'cover': cover, 'content': content, 'settings': settings}
        job['fingerprint'] = hashlib.sha256(json.dumps(job, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        jobs.append(job)
    assert len(jobs) == 10 and len({(j['integration_id'], j['content']) for j in jobs}) == len(jobs)
    write(DRY, {'jobs': jobs, 'assets': assets, 'chapters': chapters, 'chapter_seconds': times,
                'covers_supported': {'youtube': 'settings.thumbnail', 'instagram': 'image[0].thumbnail'},
                'youtube_ab': 'Studio no mesmo vídeo', 'dry_run': True})
    print(f'Dry-run local: {len(jobs)} destinos, {len(assets)} mídias, {len(chapters)} capítulos. {DRY}', flush=True)


def state_for(plan):
    previous = BASE / 'POSTIZ_ESTADO.json'
    state_path = STATE if STATE.is_file() else previous
    state = read(state_path) if state_path.is_file() else {'items': {}, 'assets': {}}
    for job in plan['jobs']:
        record = state['items'].setdefault(job['id'], {'fingerprint': job['fingerprint']})
        if record['fingerprint'] != job['fingerprint']:
            raise RuntimeError(f'Conteúdo do destino alterado após início do envio: {job["id"]}')
    return state


def refresh(plan, state, persist=True):
    rows = posts()
    by_id = {row['id']: row for row in rows}
    for job in plan['jobs']:
        record = state['items'][job['id']]
        if not record.get('post_id'):
            matches = [row for row in rows if (row.get('integration') or {}).get('id') == job['integration_id']
                       and row.get('content') == job['content']
                       and (row.get('state') != 'ERROR' or row.get('releaseURL') or row.get('releaseId'))]
            if len(matches) > 1:
                record['reconciliation_error'] = 'Mais de uma publicação existente com a mesma descrição'
            elif matches:
                record.pop('reconciliation_error', None)
                record['post_id'] = matches[0]['id']
        row = by_id.get(record.get('post_id'))
        if row:
            record['remote'] = {k: row.get(k) for k in ('state', 'releaseURL', 'releaseId', 'publishDate')}
            record['remote']['has_error'] = bool(row.get('error'))
    if persist:
        save_state(state)


def stage(asset_key, plan, state):
    asset = plan['assets'][asset_key]
    record = state['assets'].setdefault(asset_key, {})
    if record.get('removed'):
        raise RuntimeError(f'Mídia já removida: {asset_key}')
    if not record.get('media'):
        path = Path(asset['path'])
        if asset['transport'] == 'postiz':
            record['media'] = postiz.upload(path)
        else:
            record.setdefault('r2_key', f'publicacoes/{uuid4().hex}{path.suffix.lower()}')
            save_state(state)
            record['media'], _ = R2Media().stage(path, record['r2_key'])
        save_state(state)
    return dict(record['media'])


def send_job(job, plan, state):
    record = state['items'][job['id']]
    if record.get('post_id'):
        return
    if record.get('attempted_at') or record.get('reconciliation_error'):
        raise RuntimeError(f'Tentativa anterior precisa de reconciliação: {job["id"]}')
    media = [stage(key, plan, state) for key in job['media']]
    settings = dict(job['settings'])
    if job['cover']:
        cover = stage(job['cover'], plan, state)
        if job['provider'] == 'youtube':
            settings['thumbnail'] = cover
        else:
            media[0]['thumbnail'] = cover['path']
    payload = {'type': 'now', 'creationMethod': 'CLI', 'date': now().isoformat(), 'shortLink': False,
               'tags': [], 'posts': [{'integration': {'id': job['integration_id']}, 'settings': settings,
                                      'value': [{'content': job['content'], 'image': media, 'delay': 0}]}]}
    target = PUB / f'{job["id"]}_ENVIO.json'
    write(target, payload)
    record['attempted_at'] = now().isoformat()
    record['cover_attached_in_payload'] = bool(job['cover'])
    save_state(state)
    result = run_cli(['posts:create', '--json', str(target)])
    ids = postiz.post_ids({'post': result})
    if len(ids) != 1:
        raise RuntimeError(f'Resposta ambígua para {job["id"]}')
    record['post_id'] = ids[0]
    record.pop('submission_error', None)
    save_state(state)
    print(f'{job["id"]} aceito {ids[0]}', flush=True)


def publish(plan, state):
    for asset in plan['assets'].values():
        assert digest(Path(asset['path'])) == asset['sha256'], asset['path']
    integrations = {entry['id']: entry for entry in postiz.integrations()}
    refresh(plan, state)
    for job in plan['jobs']:
        entry = integrations.get(job['integration_id'], {})
        profile = re.sub(r'[^a-z0-9]', '', str(entry.get('profile', '')).lower())
        if entry.get('identifier') != job['provider'] or entry.get('disabled') or profile != 'pixelprocurado':
            state['items'][job['id']]['submission_error'] = 'IntegrationUnavailable'
            save_state(state)
            print(f'{job["id"]} indisponível no canal autorizado', flush=True)
            continue
        try:
            send_job(job, plan, state)
        except Exception as exc:
            record = state['items'][job['id']]
            record['submission_error'] = type(exc).__name__
            save_state(state)
            print(f'{job["id"]} falhou na submissão ({type(exc).__name__})', flush=True)
    refresh(plan, state)


def cleanup(plan, state):
    for key, record in state['assets'].items():
        if not record.get('r2_key') or record.get('removed'):
            continue
        users = [state['items'][i].get('remote', {}) for i in plan['assets'][key]['needed_by']]
        if users and all(item.get('state') == 'PUBLISHED' and item.get('releaseURL') for item in users):
            R2Media().remove(record['r2_key'])
            record['removed'] = True
            save_state(state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', default='dry-run', choices=('dry-run', 'publish', 'peek', 'status', 'cleanup'))
    args = parser.parse_args()
    if args.action == 'dry-run':
        dry_run()
        return
    plan = read(DRY)
    state = state_for(plan)
    if args.action == 'publish':
        publish(plan, state)
    else:
        refresh(plan, state, persist=args.action != 'peek')
        if args.action == 'cleanup':
            cleanup(plan, state)
    print(json.dumps({k: {'post_id': v.get('post_id'), 'submission_error': v.get('submission_error'), **v.get('remote', {})}
                      for k, v in state['items'].items()}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
