"""Publicação imediata e registrada de C01–C03 pelo Postiz, em Facebook e Instagram."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import postiz_shorts as p

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'producao/shorts/POSTIZ_META_ESTADO.json'
SESSION = ROOT / '.production-tools/postiz-https.json'
IDS = ('C01', 'C02', 'C03')
PROVIDERS = ('facebook', 'instagram')
CREDIT = 'Imagens: Rockstar Games. Análise e edição: Pixel Procurado. Narração sintética: Gemini TTS.'
COPY = {
    'C01': {
        'facebook': 'A data de GTA 6 pode estar certa… e a plataforma, errada. 🔎\n\nRecortar um anúncio pode transformar uma informação verdadeira numa promessa que ele nunca fez. Data, versão e fonte precisam pertencer ao mesmo anúncio.\n\nVocê confere a plataforma antes de compartilhar?\n\nFonte oficial: https://www.rockstargames.com/VI',
        'instagram': 'Uma data verdadeira também pode te enganar. 🔎\n\nEm GTA 6, confira a plataforma junto da data. Um trailer capturado em um console não define, sozinho, exclusividade ou o calendário de outras versões.\n\nSalve este lembrete e conte: você joga no PC ou no console?\n\nFonte: página oficial de GTA VI, Rockstar Games.',
    },
    'C02': {
        'facebook': 'Jason e Lucia podem querer uma vida melhor e discordar do caminho. 🎮\n\nSossego e controle parecem combinar… até uma oportunidade aumentar o risco para os dois. Essa é uma leitura dos perfis e da premissa de GTA 6, não uma missão confirmada nem uma previsão de traição.\n\nQuem você acha que hesitaria primeiro: Jason ou Lucia?\n\nFontes: https://www.rockstargames.com/VI/only-in-leonida e https://www.rockstargames.com/VI/trailer-2',
        'instagram': 'O mesmo sonho. Decisões diferentes. 🧩\n\nJason e Lucia podem querer melhorar de vida sem concordar sobre o risco que vale correr. Essa é a nossa leitura da dupla em GTA 6 — não uma previsão do final.\n\nQuem hesitaria primeiro diante de uma oportunidade perigosa: Jason ou Lucia?\n\nFontes: perfis oficiais e premissa do Trailer 2 de GTA VI, Rockstar Games.',
    },
    'C03': {
        'facebook': 'Esse abraço tem polícia no fundo. 🔎\n\nNo recorte, Jason, Lucia e o sol. Na arte inteira, barcos da polícia e um helicóptero também participam da cena. Abrir o quadro muda a leitura da imagem.\n\nÉ análise visual de uma arte promocional de GTA 6; não confirma missão, traição ou ordem das cenas. Qual detalhe do fundo você viu primeiro?\n\nFonte: https://www.rockstargames.com/VI/media',
        'instagram': 'O casal está no centro. A polícia também está na história. 🔎\n\nO recorte destaca o abraço de Jason e Lucia. A arte inteira deixa o perigo entrar na leitura: barcos da polícia e um helicóptero aparecem ao redor.\n\nQual detalhe do fundo você percebeu primeiro?\n\nAnálise visual de arte promocional de GTA 6, sem confirmação de missão ou traição. Fonte: biblioteca oficial de GTA VI, Rockstar Games.',
    },
}


def save(state):
    state['updated_at'] = datetime.now(timezone.utc).isoformat()
    temp = STATE.with_suffix('.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(STATE)


def all_posts():
    result = p.extract_json(p.run_postiz(['posts:list']))
    return result['posts'] if isinstance(result, dict) else result


def caption(short_id, provider):
    cover_credit = '\nCapa ilustrativa com IA; não é captura oficial.' if provider == 'instagram' else ''
    return COPY[short_id][provider] + '\n\n' + CREDIT + cover_credit + '\n\n#GTA6 #GTAVI #PixelProcurado'


def prepare(state):
    connected = p.integrations()
    integrations = {}
    for provider in PROVIDERS:
        matches = [i for i in connected if i.get('identifier') == provider and i.get('name') == 'Pixel Procurado' and not i.get('disabled')]
        if len(matches) != 1:
            raise RuntimeError(f'Esperava uma conta ativa Pixel Procurado em {provider}.')
        integrations[provider] = matches[0]['id']
    session = json.loads(SESSION.read_text(encoding='utf-8-sig'))
    state.setdefault('authorization', 'Usuário solicitou publicação imediata dos destinos selecionados, sem agendamento futuro.')
    state.setdefault('items', {})
    for short_id in IDS:
        folder = ROOT / 'producao/shorts' / short_id
        video = folder / f'exportacoes/Pixel_Procurado_{short_id}_Short_1080x1920.mp4'
        qa = json.loads((folder / 'projeto/qa/validacao_final.json').read_text(encoding='utf-8'))
        assert qa['width'] == 1080 and qa['height'] == 1920
        assert video.is_file() and video.stat().st_size < 300 * 1024 ** 2
        entry = state['items'].setdefault(short_id, {})
        if not entry.get('video'):
            print(f'{short_id}: enviando vídeo ao Postiz local', flush=True)
            entry['video'] = p.upload(video)
            save(state)
        for provider in PROVIDERS:
            text = caption(short_id, provider)
            assert 0 < len(text) <= (2200 if provider == 'instagram' else 63206)
            title = (folder / 'publicacao/01_TITULO.txt').read_text(encoding='utf-8').strip()
            assert len(title) <= 100
            record = entry.setdefault(provider, {})
            record.update(integration_id=integrations[provider], caption=text)
            # Remote media must not resolve to the historical localhost library URL.
            media = {'id': '', 'path': session['url'] + urlsplit(entry['video']['path']).path}
            if provider == 'instagram':
                if not entry.get('meta_thumbnail'):
                    entry['meta_thumbnail'] = p.upload(folder / 'publicacao/capa_youtube.jpg')
                    save(state)
                media['thumbnail'] = session['url'] + urlsplit(entry['meta_thumbnail']['path']).path
            settings = {'__type': provider, 'post_type': 'post'}
            if provider == 'facebook':
                settings['title'] = title
            payload = {'type': 'now', 'creationMethod': 'CLI', 'date': datetime.now(timezone.utc).isoformat(),
                       'shortLink': False, 'tags': [], 'posts': [{'integration': {'id': integrations[provider]},
                       'value': [{'content': text, 'image': [media], 'delay': 0}], 'settings': settings}]}
            target = folder / 'publicacao' / f'POSTIZ_{provider.upper()}_ENVIO.json'
            target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            (folder / 'publicacao' / f'LEGENDA_{provider.upper()}.txt').write_text(text + '\n', encoding='utf-8')
            record['payload_file'] = str(target.relative_to(ROOT))
            save(state)
            print(f'{short_id} {provider}: preparado, {len(text)} caracteres', flush=True)


def publish(state, ids, providers=PROVIDERS):
    existing = all_posts()
    for short_id in ids:
        for provider in providers:
            record = state['items'][short_id][provider]
            matches = [post for post in existing if (post.get('integration') or {}).get('id') == record['integration_id'] and post.get('content') == record['caption']]
            if len(matches) > 1:
                raise RuntimeError('Múltiplos posts correspondentes; revisar antes de publicar.')
            if matches:
                record['post_id'] = matches[0]['id']
                save(state)
                print(f'{short_id} {provider}: já existe {matches[0]["id"]}; não recriado', flush=True)
                continue
            if record.get('post_id') or record.get('creation_attempted_at'):
                raise RuntimeError(f'{short_id} {provider}: tentativa anterior exige reconciliação; não reenviar.')
            payload_path = ROOT / record['payload_file']
            payload = json.loads(payload_path.read_text(encoding='utf-8'))
            assert payload['type'] == 'now' and len(payload['posts']) == 1
            assert payload['posts'][0]['integration']['id'] == record['integration_id']
            payload['date'] = datetime.now(timezone.utc).isoformat()
            payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
            record['creation_attempted_at'] = datetime.now(timezone.utc).isoformat()
            save(state)
            response = p.extract_json(p.run_postiz(['posts:create', '--json', str(payload_path)]))
            record['creation_response'] = response
            post_ids = p.post_ids({'post': response})
            if len(post_ids) != 1:
                save(state)
                raise RuntimeError('Resposta inesperada; conferir o Postiz sem criar novo post.')
            record['post_id'] = post_ids[0]
            save(state)
            print(f'{short_id} {provider}: envio imediato iniciado, {post_ids[0]}', flush=True)


def status(state):
    posts = {entry['id']: entry for entry in all_posts()}
    for short_id, item in state.get('items', {}).items():
        for provider in PROVIDERS:
            record = item.get(provider, {})
            entry = posts.get(record.get('post_id'))
            if entry:
                record['status'] = {key: entry.get(key) for key in ('id','state','releaseURL','releaseId','error','publishDate')}
                print(json.dumps({'short':short_id,'provider':provider,**record['status']},ensure_ascii=False), flush=True)
    save(state)


def retry_failed(state, ids, providers=PROVIDERS):
    posts = {entry['id']: entry for entry in all_posts()}
    for short_id in ids:
        for provider in providers:
            record = state['items'][short_id][provider]
            existing = posts[record['post_id']]
            if existing.get('state') != 'ERROR' or existing.get('releaseId') or existing.get('releaseURL'):
                raise RuntimeError('Retomada exige post em ERROR e sem publicação remota registrada.')
            payload_path = ROOT / record['payload_file']
            payload = json.loads(payload_path.read_text(encoding='utf-8'))
            payload['posts'][0]['value'][0]['id'] = existing['id']
            payload['date'] = datetime.now(timezone.utc).isoformat()
            assert payload['type'] == 'now'
            assert payload['posts'][0]['value'][0]['image'][0]['id'] == ''
            payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
            record.setdefault('retries', []).append({'at':payload['date'],'reason':'Preservar URL pública da mídia, sem substituição pela biblioteca localhost.'})
            save(state)
            response = p.extract_json(p.run_postiz(['posts:create','--json',str(payload_path)]))
            assert p.post_ids({'post':response}) == [existing['id']], 'Retomada retornou outro ID; revisar.'
            print(f'{short_id} {provider}: retomado o mesmo post {existing["id"]}', flush=True)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare','publish','retry-failed','status','check'])
    parser.add_argument('--ids', default=','.join(IDS))
    parser.add_argument('--providers', default=','.join(PROVIDERS))
    parser.add_argument('--confirm-publish-now', action='store_true')
    args = parser.parse_args()
    ids = args.ids.split(',')
    providers = args.providers.split(',')
    assert len(set(providers)) == len(providers) and all(i in PROVIDERS for i in providers)
    assert len(set(ids)) == len(ids) and all(i in IDS for i in ids)
    state = json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {}
    if args.command == 'check':
        for short_id in IDS:
            for provider in PROVIDERS:
                assert len(caption(short_id, provider)) < 2200
        print('Textos verificados: seis legendas, sem agenda futura.')
    elif args.command == 'prepare':
        prepare(state)
    elif args.command in ('publish','retry-failed'):
        if not args.confirm_publish_now:
            parser.error('Exige --confirm-publish-now')
        if args.command == 'publish':
            publish(state, ids, providers)
        else:
            retry_failed(state, ids, providers)
        status(state)
    else:
        status(state)
