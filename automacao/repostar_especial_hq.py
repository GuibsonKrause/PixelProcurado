"""Republicação autorizada após remoção manual dos posts antigos."""
import json
import subprocess
import time
import msvcrt
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from boto3.s3.transfer import TransferConfig

import publicar_especial_postiz as original
from distribuir_l05_postiz import write
from r2_media import R2Media

BASE = original.SOCIAL / 'qualidade_maxima'
STATE = BASE / 'POSTIZ_REPUBLICACAO.json'
MASTER = original.EP / 'exportacoes/Pixel_Procurado_GTA6_2013_Longo_V2.mp4'
SHORT = original.EP / 'exportacoes/Pixel_Procurado_GTA6_Camiseta_Short_V2.mp4'
IG_LONG = BASE / 'Longo_Instagram_HEVC_1080p60.mp4'
IG_SHORT = BASE / 'Short_Instagram_1080p60.mp4'
EXPORT_SCALE = 1


def stage_url(path, key, copy_from=None):
    transfer = TransferConfig(multipart_threshold=32 * 1024 * 1024,
                              multipart_chunksize=32 * 1024 * 1024,
                              max_concurrency=2)
    return R2Media().stage(path, key, transfer_config=transfer, copy_from=copy_from)


def now():
    return datetime.now(timezone.utc)


def save(state):
    for attempt in range(6):
        try:
            write(STATE, state)
            return
        except PermissionError:
            if attempt == 5:
                raise
            time.sleep(.4 * (attempt + 1))


def validate(path, kind, provider):
    output = subprocess.check_output([str(original.EP / 'montagem/ffprobe.exe'), '-v', 'error',
                                      '-show_streams', '-show_format', '-of', 'json', str(path)])
    meta = json.loads(output)
    video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in meta['streams'] if s['codec_type'] == 'audio')
    width, height = (1920, 1080) if kind == 'longo' and provider != 'instagram' else (1080, 1920)
    width, height = width * EXPORT_SCALE, height * EXPORT_SCALE
    fps_n, fps_d = map(int, video['avg_frame_rate'].split('/'))
    expected = 447.8 if kind == 'longo' else 53.0333
    assert (video['width'], video['height']) == (width, height)
    assert abs(fps_n / fps_d - 60) < .01
    assert abs(float(video['duration']) - expected) < .05
    assert abs(float(video['duration']) - float(audio['duration'])) < .05
    assert video['codec_name'] in (('h264', 'hevc') if provider == 'instagram' else ('h264',))
    assert audio['codec_name'] == 'aac'
    if provider == 'instagram':
        assert path.stat().st_size < 1_000_000_000
    return {'width': width, 'height': height, 'fps': fps_n / fps_d,
            'duration': float(video['duration']), 'bytes': path.stat().st_size,
            'file': str(path.relative_to(original.EP))}


def prepare(state, provider, kind):
    name = f'{provider}_{kind}'
    rec = state['items'].setdefault(name, {})
    if rec.get('media') and rec.get('cover_ready'):
        return
    path = (IG_LONG if kind == 'longo' else IG_SHORT) if provider == 'instagram' else (
        MASTER if kind == 'longo' else SHORT)
    rec['source'] = validate(path, kind, provider)
    save(state)
    if not rec.get('media'):
        if provider == 'youtube' and path.stat().st_size < 1_000_000_000:
            rec['media'] = original.postiz.upload(path)
        else:
            # O upload local do Postiz rejeitou o master com HTTP 413.
            # A mídia por URL usa o transporte já configurado sem recomprimir o master.
            rec.setdefault('r2_key', f'publicacoes/{uuid4().hex}.mp4')
            save(state)
            reusable = next((other['r2_key'] for other in state['items'].values()
                             if other is not rec and other.get('media') and other.get('r2_key')
                             and not other.get('cleaned')
                             and other.get('source', {}).get('file') == rec['source']['file']), None)
            rec['media'], _ = stage_url(path, rec['r2_key'], copy_from=reusable)
        save(state)
    if provider == 'youtube':
        folder = 'longo_youtube' if kind == 'longo' else 'short_vertical'
        rec['cover'] = original.postiz.upload(original.SOCIAL / f'capas/V2/{folder}.jpg')
    elif provider == 'instagram' and kind != 'story':
        folder = 'longo_reels' if kind == 'longo' else 'short_vertical'
        rec.setdefault('cover_key', f'publicacoes/{uuid4().hex}.jpg')
        save(state)
        rec['cover'], _ = stage_url(original.SOCIAL / f'capas/V2/{folder}.jpg', rec['cover_key'])
    rec['cover_ready'] = True
    save(state)
    print(name, 'arquivo conferido e upload pronto', rec['source'], flush=True)


def send(state, provider, kind, due=None):
    name = f'{provider}_{kind}'
    rec = state['items'][name]
    if rec.get('post_id'):
        return
    old_ids = set(state['previous_post_ids'])
    content = rec.get('content_override') or original.text_for(provider, kind)
    matches = [row for row in original.posts()
               if row['id'] not in old_ids
               and row.get('integration', {}).get('id') == original.CHANNELS[provider]
               and row.get('content') == content]
    if len(matches) == 1:
        rec['post_id'] = matches[0]['id']
        save(state)
        print(name, 'publicação anterior reconciliada', rec['post_id'], flush=True)
        return
    if matches:
        raise RuntimeError(f'{name}: múltiplos posts equivalentes; conferir antes de enviar.')
    if rec.get('attempted_at'):
        raise RuntimeError(f'{name}: reconciliar tentativa anterior antes de repetir.')
    media = dict(rec['media'])
    if provider == 'instagram' and rec.get('cover'):
        media['thumbnail'] = rec['cover']['path']
    item = original.payload(provider, kind, media)
    item['value'][0]['content'] = content
    if provider == 'youtube':
        item['settings']['thumbnail'] = rec['cover']
    date = due or now()
    data = {'type': 'schedule' if due else 'now', 'date': date.isoformat(),
            'creationMethod': 'CLI', 'shortLink': False, 'tags': [], 'posts': [item]}
    target = BASE / f'{name}_ENVIO.json'
    write(target, data)
    rec['attempted_at'] = now().isoformat()
    save(state)
    response = original.run_cli(['posts:create', '--json', str(target)])
    ids = original.postiz.post_ids({'post': response})
    if len(ids) != 1:
        raise RuntimeError(f'{name}: resposta ambígua, consultar o Postiz.')
    rec['post_id'] = ids[0]
    save(state)
    print(name, 'aceito', rec['post_id'], date.isoformat(), flush=True)


def refresh(state, names):
    remote = {p['id']: p for p in original.posts()}
    statuses = {}
    for name in names:
        rec = state['items'][name]
        row = remote.get(rec.get('post_id'), {})
        rec['remote'] = {k: row.get(k) for k in ('state', 'releaseURL', 'releaseId', 'error', 'publishDate')}
        statuses[name] = rec['remote']['state']
        if statuses[name] == 'PUBLISHED' and rec['remote']['releaseURL'] and not rec.get('cleaned'):
            for key in ('r2_key', 'cover_key'):
                if rec.get(key):
                    R2Media().remove(rec[key])
            rec['cleaned'] = True
    save(state)
    print(statuses, flush=True)
    return statuses


def wait_published(state, names):
    deadline = now() + timedelta(minutes=40)
    while now() < deadline:
        statuses = refresh(state, names)
        if all(s == 'PUBLISHED' for s in statuses.values()):
            return
        if 'ERROR' in statuses.values():
            raise RuntimeError('Falha de publicação. Conferir estado antes de repetir.')
        time.sleep(90)
    raise TimeoutError('Postiz ainda sem confirmação final.')


def main():
    BASE.mkdir(exist_ok=True)
    old = json.loads(original.STATE.read_text(encoding='utf-8-sig'))
    state = json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {
        'items': {}, 'old_posts_removed_by_user': True,
        'confirmation': 'eu mesmo exclui. pode postar',
        'previous_post_ids': [r['post_id'] for r in old['items'].values()]}
    save(state)
    original.discover()
    for provider in ('youtube', 'facebook'):
        prepare(state, provider, 'longo')
        send(state, provider, 'longo')
    print('Aguardando a derivação Instagram completar.', flush=True)
    while not IG_LONG.is_file() or not IG_SHORT.is_file():
        time.sleep(30)
    for path in (IG_LONG, IG_SHORT):
        marker = path.with_suffix('.decode_ok')
        if not marker.exists():
            subprocess.run([str(original.EP / 'montagem/ffmpeg.exe'), '-v', 'error', '-xerror',
                            '-threads', '2', '-i', str(path), '-f', 'null', 'NUL'], check=True)
            marker.touch()
    prepare(state, 'instagram', 'longo')
    send(state, 'instagram', 'longo')
    wait_published(state, [f'{p}_longo' for p in original.CHANNELS])
    if not state.get('short_due_utc'):
        state['short_due_utc'] = (now() + timedelta(minutes=30)).isoformat()
        save(state)
    due = datetime.fromisoformat(state['short_due_utc'])
    for provider, kind in original.SHORT_JOBS:
        prepare(state, provider, kind)
        send(state, provider, kind, due if due > now() else None)
    print('Curtos e Stories previstos para', due.isoformat(), flush=True)
    time.sleep(max(0, (due - now()).total_seconds()))
    wait_published(state, [f'{p}_{k}' for p, k in original.SHORT_JOBS])


if __name__ == '__main__':
    BASE.mkdir(exist_ok=True)
    with (BASE / 'republicacao.lock').open('a+b') as lock:
        if not lock.tell():
            lock.write(b'0')
            lock.flush()
        lock.seek(0)
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        try:
            main()
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
