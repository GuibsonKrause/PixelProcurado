"""Repara a fila de 4–17/11/2026, preservando IDs e horários agendados."""

import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4

import postiz_shorts as postiz
from r2_media import R2Media

CHANNELS = ('cmvzyur290001pddwolrt33em', 'cmvzyw7vj0003pddwkgtivv8i')
YOUTUBE = 'cmvsctfgl0001jncj932ovibv'
FAILED = ('cmw29leu50000mm97dulc9vof', 'cmw29lgfp0003mm97616datf2',
          'cmw29lggg0004mm97m3zw3bpj', 'cmw29lm3d0005mm97emh10buk',
          'cmw29lm3v0006mm97lp0xya40')
OLD_HOST = 'elephant-sprite-engulf.ngrok-free.dev'
LOCAL = 'http://localhost:4007'
STATE = Path(__file__).resolve().parents[1] / '.production-tools'


def literal(value):
    return "'" + value.replace("'", "''") + "'"


def sql(query):
    result = subprocess.run(
        ['docker', 'exec', '-i', 'postiz-postgres', 'sh', '-c',
         'exec psql -U $POSTGRES_USER -d $POSTGRES_DB -Atq -v ON_ERROR_STOP=1'],
        input=query.encode('utf-8'), capture_output=True, timeout=40,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace').strip())
    return result.stdout.decode('utf-8').strip()


def rows(where):
    return json.loads(sql(f'''SELECT coalesce(json_agg(r ORDER BY r.date,r.id),'[]') FROM (
        SELECT id, state::text, "integrationId" AS channel, content, delay,
               settings::jsonb AS settings, image::jsonb AS image,
               to_char("publishDate",'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') AS date,
               error, "releaseId" AS release_id, "releaseURL" AS release_url
        FROM "Post" WHERE "deletedAt" IS NULL AND ({where})
    ) r;'''))


def save(path, value):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


def old_path(value):
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    if parsed.hostname != OLD_HOST:
        return None
    if not re.fullmatch(r'/uploads/\d{4}/\d{2}/\d{2}/[0-9a-f]+\.(mp4|jpg|jpeg|png|webp)', parsed.path):
        raise ValueError('Caminho de upload fora do formato local conhecido.')
    return parsed.path


def swap(row, mapping, external=True):
    items = []
    for original in row['image']:
        item = dict(original)
        for field in ('path', 'thumbnail'):
            if source := old_path(item.get(field)):
                item[field] = mapping[source]['url']
                if field == 'path' and external:
                    item['id'] = ''
        items.append(item)
    return items


def stage(records, manifest_path, manifest):
    assets = manifest.setdefault('assets', {})
    wanted = sorted({source for row in records for item in row['image']
                     for field in ('path', 'thumbnail') if (source := old_path(item.get(field)))})
    if not wanted:
        raise RuntimeError('Nenhuma mídia do ngrok nos registros selecionados.')
    now = datetime.now(timezone.utc)
    until = max(now + timedelta(days=2), max(datetime.fromisoformat(row['date']) for row in records) + timedelta(days=2))
    r2 = R2Media()
    for source in wanted:
        assets.setdefault(source, {'key': f'publicacoes/{uuid4().hex}{Path(source).suffix}'})
    save(manifest_path, manifest)

    def upload(source):
        key = assets[source]['key']
        with TemporaryDirectory() as folder:
            local = Path(folder) / Path(source).name
            with urlopen(LOCAL + source, timeout=45) as response, local.open('wb') as output:
                if response.geturl() != LOCAL + source or response.headers.get_content_maintype() not in ('image', 'video'):
                    raise ValueError('O upload original não está acessível localmente.')
                size = int(response.headers['Content-Length'])
                shutil.copyfileobj(response, output)
            if local.stat().st_size != size:
                raise ValueError('Cópia local incompleta.')
            media, _ = r2.stage(local, key, available_until=until)
        return source, media['path'], size

    pending = [source for source in wanted if not assets[source].get('url')]
    print(f'{len(records)} posts, {len(wanted)} arquivos, {len(pending)} para enviar.', flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for source, url, size in pool.map(upload, pending):
            assets[source].update(url=url, size=size, expires_at=until.isoformat())
            save(manifest_path, manifest)
            print(f'R2 {sum(bool(assets[s].get("url")) for s in wanted)}/{len(wanted)}', flush=True)
    return assets


def repair_queue(records, assets, external=True):
    # The running workflows use post IDs. Touch only media, preserving dates,
    # settings, batches and grouping that the general upsert would rewrite.
    updates = []
    for row in records:
        settings = dict(row['settings'])
        thumbnail = settings.get('thumbnail')
        if isinstance(thumbnail, dict) and (source := old_path(thumbnail.get('path'))):
            settings['thumbnail'] = {**thumbnail, 'path': assets[source]['url']}
        updates.append({'id': row['id'], 'channel': row['channel'], 'date': row['date'],
                        'old': row['image'], 'new': swap(row, assets, external),
                        'old_settings': row['settings'], 'new_settings': settings})
    values = literal(json.dumps(updates, ensure_ascii=False))
    sql(f'''BEGIN;
        DO $repair$ DECLARE n integer; BEGIN
        UPDATE "Post" p SET image = x.new::text, "updatedAt" = now() AT TIME ZONE 'UTC',
            settings = CASE WHEN x.new_settings = x.old_settings THEN p.settings ELSE x.new_settings::text END
        FROM jsonb_to_recordset({values}::jsonb)
          AS x(id text, channel text, date text, old jsonb, new jsonb, old_settings jsonb, new_settings jsonb)
        WHERE p.id=x.id AND p."integrationId"=x.channel AND p.state::text='QUEUE'
          AND p."deletedAt" IS NULL AND p.image::jsonb=x.old AND p.settings::jsonb=x.old_settings
          AND p."publishDate"=x.date::timestamptz AT TIME ZONE 'UTC'
          AND p."publishDate">(now() AT TIME ZONE 'UTC') + interval '10 minutes';
        GET DIAGNOSTICS n = ROW_COUNT;
        IF n <> {len(records)} THEN RAISE EXCEPTION 'Fila mudou: % linhas', n; END IF;
        END $repair$; COMMIT;''')
    confirmed = {row['id']: row for row in rows('id IN (' + ','.join(literal(row['id']) for row in records) + ')')}
    for update in updates:
        row = confirmed[update['id']]
        if (row['state'] != 'QUEUE' or row['date'] != update['date'] or row['image'] != update['new']
                or row['settings'] != update['new_settings']):
            raise RuntimeError('Verificação da fila não confere.')
    print(f'{len(records)} agendamentos confirmados com {"R2" if external else "arquivos locais"} e mesmos horários.', flush=True)


def repair_youtube():
    records = rows(f'''"integrationId"={literal(YOUTUBE)} AND state::text='QUEUE'
        AND "publishDate">='2026-11-06 03:00' AND "publishDate"<'2026-11-18 03:00'
        AND (image LIKE '%{OLD_HOST}%' OR settings LIKE '%{OLD_HOST}%')''')
    if not records:
        return
    assets = {}
    for row in records:
        thumbnail = row['settings'].get('thumbnail')
        candidates = [item.get(field) for item in row['image'] for field in ('path', 'thumbnail')]
        if isinstance(thumbnail, dict):
            candidates.append(thumbnail.get('path'))
        for value in candidates:
            if (source := old_path(value)) and source not in assets:
                url = LOCAL + source
                with urlopen(Request(url, method='HEAD'), timeout=12) as response:
                    if response.geturl() != url or int(response.headers.get('Content-Length', 0)) <= 0:
                        raise RuntimeError('Upload do YouTube indisponível localmente.')
                assets[source] = {'url': url}
    save(STATE / 'postiz-r2-reparo-2026-11-06-youtube.json', {'originals': records, 'assets': assets})
    repair_queue(records, assets, external=False)


def cleanup():
    r2 = R2Media()
    for mode in ('retry', 'queue'):
        path = STATE / f'postiz-r2-reparo-2026-11-06-{mode}.json'
        if not path.exists():
            continue
        manifest = json.loads(path.read_text(encoding='utf-8'))
        attempts = manifest.get('attempts', {})
        ids = {row['id']: (attempts.get(row['id'], {}).get('id') if mode == 'retry' else row['id'])
               for row in manifest['originals']}
        present = [value for value in ids.values() if value]
        if not present:
            continue
        by_id = {row['id']: row for row in rows('id IN (' + ','.join(map(literal, present)) + ')')}
        removed = 0
        for source, asset in manifest['assets'].items():
            if not asset.get('url') or asset.get('removed_at'):
                continue
            linked = [ids[row['id']] for row in manifest['originals']
                      if any(old_path(item.get(field)) == source for item in row['image'] for field in ('path', 'thumbnail'))]
            if linked and all(post_id in by_id and by_id[post_id]['state'] == 'PUBLISHED'
                              and by_id[post_id]['release_url'] for post_id in linked):
                r2.remove(asset['key'])
                asset['removed_at'] = datetime.now(timezone.utc).isoformat()
                save(path, manifest)
                removed += 1
        print(f'{mode}: {removed} cópias de publicações confirmadas removidas.', flush=True)


def retry(records, assets, path, manifest):
    attempts = manifest.setdefault('attempts', {})
    for row in records:
        equivalents = rows(f'''"integrationId"={literal(row['channel'])} AND content={literal(row['content'])}
                             AND id<>{literal(row['id'])} AND state::text IN ('PUBLISHED','QUEUE','PROCESSING','PENDING')''')
        if equivalents:
            print(f'{row["id"]}: já existe publicação ou envio equivalente.', flush=True)
            continue
        if row['id'] in attempts or row['state'] != 'ERROR' or row['release_id'] or row['release_url']:
            raise RuntimeError(f'Reenvio anterior ou estado ambíguo para {row["id"]}.')
        now = datetime.now(timezone.utc).isoformat()
        payload = {'type': 'now', 'creationMethod': 'CLI', 'date': now,
                   'shortLink': False, 'tags': [], 'posts': [{
                       'integration': {'id': row['channel']}, 'settings': row['settings'],
                       'value': [{'content': row['content'], 'delay': row['delay'], 'image': swap(row, assets)}],
                   }]}
        with TemporaryDirectory() as directory:
            file = Path(directory) / 'post.json'
            file.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
            attempts[row['id']] = {'requested_at': now}
            save(path, manifest)
            result = postiz.extract_json(postiz.run_postiz(['posts:create', '--json', str(file)]))
        ids = postiz.post_ids({'post': result})
        if len(ids) != 1:
            raise RuntimeError(f'Resposta ambígua para {row["id"]}.')
        attempts[row['id']]['id'] = ids[0]
        save(path, manifest)
        print(f'{row["id"]} -> {ids[0]}', flush=True)


def main(mode):
    if mode == 'youtube':
        return repair_youtube()
    if mode == 'cleanup':
        return cleanup()
    if mode not in ('queue', 'retry'):
        raise SystemExit('Use queue, retry, youtube ou cleanup.')
    path = STATE / f'postiz-r2-reparo-2026-11-06-{mode}.json'
    manifest = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    channels = ','.join(map(literal, CHANNELS))
    where = (f'''state::text='QUEUE' AND "publishDate">='2026-11-06 03:00' AND "publishDate"<'2026-11-18 03:00'
                  AND image LIKE '%{OLD_HOST}%' ''' if mode == 'queue'
             else 'id IN (' + ','.join(map(literal, FAILED)) + ')')
    records = rows(f'"integrationId" IN ({channels}) AND ({where})')
    if not records:
        print('Nenhum registro restante nesta etapa.')
        return
    manifest.setdefault('originals', records)
    assets = stage(records, path, manifest)
    if mode == 'queue':
        repair_queue(records, assets)
    else:
        retry(records, assets, path, manifest)


if __name__ == '__main__':
    main(sys.argv[1])
