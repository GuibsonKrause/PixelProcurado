"""L05 somente: derivações locais e cinco destinos Postiz; plan é o padrão."""
import argparse
import hashlib
import json
import re
import subprocess
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import postiz_shorts as p

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'producao/L05'
SOCIAL = EP / 'social'
STATE = SOCIAL / 'POSTIZ_ESTADO.json'
SOURCE = EP / 'exportacoes/Pixel_Procurado_L05_4K.mp4'
WHEN = datetime.fromisoformat('2026-11-03T12:00:00-03:00')
FFMPEG = ROOT / '.production-tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
CHANNELS = {'youtube': 'cmvsctfgl0001jncj932ovibv', 'facebook': 'cmvzyur290001pddwolrt33em',
            'instagram': 'cmvzyw7vj0003pddwkgtivv8i'}
FILES = {'youtube_feed': SOURCE, 'facebook_feed': SOCIAL / 'L05_Facebook_1080p.mp4',
         'instagram_feed': SOCIAL / 'L05_Instagram_integral_1080x1920.mp4',
         'facebook_story': SOCIAL / 'L05_Story_1080x1920.mp4',
         'instagram_story': SOCIAL / 'L05_Story_1080x1920.mp4'}
CAPTION = ('O carro distrai. Olha a rua. 🔎\n\nSeis fotos oficiais de GTA V e GTA VI, três pares: praia, carros e vista aérea. '
           'Analisamos como o enquadramento conduz nosso olhar e como o cenário participa da imagem. '
           'É uma leitura de composição de imagens promocionais, sem medir desempenho, densidade de NPCs ou tamanho do mapa.\n\n'
           'Qual lugar faria você esquecer a missão: praia, encontro de carros ou orla vista do alto?\n\n'
           'GTA V: divulgação de 2012. Fontes: https://www.rockstargames.com/newswire/article/89k8a5545o2k8k/transport.html '
           'e https://www.rockstargames.com/VI/media\n\n'
           'Imagens: Rockstar Games. Análise e edição: Pixel Procurado. Narração sintética com auxílio de IA. '
           'Análise independente.\n\n#GTA6 #GTAV #PixelProcurado')


def digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def read(path):
    return path.read_text(encoding='utf-8-sig').strip()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def command(arguments):
    result = subprocess.run([str(FFMPEG), *arguments], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    return result


def metadata(path):
    result = subprocess.run([str(FFMPEG), '-hide_banner', '-i', str(path)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', result.stderr)
    size = re.search(r'Video:.*?(\d{3,5})x(\d{3,5})', result.stderr)
    if not duration or not size:
        raise ValueError('Metadados ausentes: ' + str(path))
    h, m, s = map(float, duration.groups())
    return {'duration': h*3600+m*60+s, 'width': int(size[1]), 'height': int(size[2]),
            'h264': 'Video: h264' in result.stderr, 'aac': 'Audio: aac' in result.stderr}


def discover():
    channels = p.integrations()
    enabled = {v['id'] for v in channels if not v.get('disabled')}
    if not set(CHANNELS.values()) <= enabled:
        raise ValueError('Uma integração autorizada está ausente/desabilitada.')
    schemas = {name: p.extract_json(p.run_postiz(['integrations:settings', channel])) for name, channel in CHANNELS.items()}
    write(SOCIAL/'CAPACIDADES_POSTIZ.json', {'checked_at': datetime.now(timezone.utc).isoformat(), 'integrations': channels, 'schemas': schemas})
    print('Três integrações e schemas gravados; nenhuma mídia enviada.')


def derive():
    source_hash = digest(SOURCE)
    source_meta = metadata(SOURCE)
    assert 3 <= source_meta['duration'] <= 900, 'Duração integral fora do limite Reel consultado.'
    # shortcut: trecho inicial delimitado por legendas pontuadas; revisar o fim visual antes do envio.
    srt = read(SOURCE.with_suffix('.srt'))
    sentences = []
    scope_end = None
    captions = []
    for block in re.split(r'\n\s*\n', srt):
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        times = re.findall(r'(\d+):(\d+):(\d+),(\d+)', lines[1])
        if len(times)==2:
            def ass_time(parts):
                h,m,s,ms=map(int,parts)
                return f'{h}:{m:02}:{s:02}.{ms//10:02}'
            text=' '.join(lines[2:]).replace('{','').replace('}','')
            wrapped=r'\N'.join(textwrap.wrap(text,width=36,break_long_words=False))
            captions.append(f'Dialogue: 0,{ass_time(times[0])},{ass_time(times[1])},Main,,0,0,0,,{wrapped}')
        match = re.search(r'--> (\d+):(\d+):(\d+),(\d+)', lines[1])
        if match and re.search(r'[.!?][\"”]?$' , ' '.join(lines[2:]).strip()):
            h,m,s,ms = map(int, match.groups())
            end = h*3600+m*60+s+ms/1000
            if 12 <= end <= 55:
                sentences.append(end)
                if 'console' in ' '.join(lines[2:]).lower():
                    scope_end = end
    if not sentences:
        raise ValueError('Não encontrei uma frase completa entre12 e55s; definir corte editorial.')
    story_end = (scope_end or sentences[-1]) + 0.15
    title = SOCIAL/'vertical_titulo.txt'
    footer = SOCIAL/'vertical_rodape.txt'
    title.write_text('GTA V × GTA VI\nOLHE AO REDOR', encoding='utf-8')
    footer.write_text('Seis imagens oficiais. Três comparações.\nPIXEL PROCURADO', encoding='utf-8')
    ass_header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial,48,&H00FFFFFF,&H00FFFFFF,&H00181311,&H00181311,-1,0,0,0,100,100,0,0,1,2,0,8,80,80,1240,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    (SOCIAL/'vertical_legendas.ass').write_text(ass_header+'\n'.join(captions)+'\n',encoding='utf-8')
    # Somente a faixa de legenda do master é coberta; foto, gráficos e créditos permanecem inteiros.
    vertical = ("scale=1080:608:flags=lanczos,pad=1080:1920:0:570:color=0x111318,setsar=1,"
                "drawbox=x=0:y=1065:w=1080:h=77:color=0x111318:t=fill,ass=vertical_legendas.ass,"
                "drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':textfile='vertical_titulo.txt':fontcolor=0xFFD33D:fontsize=64:x=(w-tw)/2:y=320:line_spacing=18,"
                "drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':textfile='vertical_rodape.txt':fontcolor=white:fontsize=36:x=(w-tw)/2:y=1480:line_spacing=16")
    qa = {'source_sha256': source_hash, 'source': str(SOURCE.relative_to(ROOT)), 'story_end': story_end,
          'captions_sha256':digest(SOCIAL/'vertical_legendas.ass'), 'caption_fontsize':48,'assets': {}}
    previous = json.loads(read(SOCIAL/'DERIVACOES_QA.json')) if (SOCIAL/'DERIVACOES_QA.json').exists() else {}
    for name in ('facebook_feed','instagram_feed','facebook_story'):
        output = FILES[name]
        config = {'source_sha256': source_hash, 'filter': 'scale=1920:1080:flags=lanczos' if name=='facebook_feed' else vertical,
                  'duration': story_end if name=='facebook_story' else source_meta['duration'],
                  'captions_sha256':qa['captions_sha256'], 'version': 2}
        signature = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
        old = previous.get('assets',{}).get(name,{})
        if not (output.exists() and old.get('signature')==signature and old.get('sha256')==digest(output) and old.get('full_decode_pass')):
            args = ['-hide_banner','-loglevel','error','-y','-threads','4','-i',str(SOURCE)]
            if name=='facebook_story':
                args += ['-t', str(story_end)]
            temporary = output.with_name(output.stem+'.rendering.mp4')
            args += ['-map','0:v:0','-map','0:a:0','-vf',config['filter'],'-c:v','libx264','-preset','veryfast','-crf','20',
                     '-maxrate','5M','-bufsize','10M','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart',str(temporary)]
            result = subprocess.run([str(FFMPEG),*args],cwd=SOCIAL,capture_output=True,text=True,encoding='utf-8',errors='replace')
            if result.returncode:
                raise RuntimeError(result.stderr[-2500:])
            command(['-v','error','-xerror','-i',str(temporary),'-f','null','-'])
            temporary.replace(output)
        meta = metadata(output)
        expected = (1920,1080) if name=='facebook_feed' else (1080,1920)
        assert (meta['width'],meta['height'])==expected and meta['h264'] and meta['aac']
        assert abs(meta['duration']-config['duration']) < .2
        assert output.stat().st_size < (100 if name=='facebook_story' else 300)*1024**2, 'Asset acima da margem de tamanho Meta.'
        qa['assets'][name] = {**meta,'file':str(output.relative_to(ROOT)), 'signature':signature,'sha256':digest(output),'full_decode_pass':True}
        write(SOCIAL/'DERIVACOES_QA.json',qa)
        print(name+': derivação decodificada integralmente',flush=True)
    assert digest(SOURCE)==source_hash, 'Master mudou durante as derivações.'
    qa['assets']['instagram_story'] = qa['assets']['facebook_story']
    write(SOCIAL/'DERIVACOES_QA.json',qa)


def payload(name, media, thumbnail=None):
    provider, kind = name.split('_')
    title = read(EP/'publicacao/01_TITULO.txt')
    settings = {'__type':provider, 'post_type':'story' if kind=='story' else 'post'}
    content = CAPTION
    if provider=='youtube':
        content = read(EP/'publicacao/02_DESCRICAO.txt')
        tags = [t.strip() for t in read(EP/'publicacao/04_TAGS.txt').split(',') if t.strip()]
        settings = {'__type':'youtube','title':title,'type':'public','selfDeclaredMadeForKids':'no',
                    'tags':[{'value':t,'label':t} for t in tags],'thumbnail':thumbnail}
        assert 2<=len(title)<=100 and len(content)<=5000 and len(','.join(tags))<=500
    elif provider=='facebook' and kind=='feed':
        settings['title'] = title
    elif kind=='story':
        content = 'O carro distrai. Olha a rua. | Pixel Procurado — L05'
    assert provider!='instagram' or len(content)<=2200
    return {'type':'schedule','creationMethod':'CLI','date':WHEN.isoformat(),'shortLink':False,'tags':[],
            'posts':[{'integration':{'id':CHANNELS[provider]},'value':[{'content':content,'image':[media],'delay':0}], 'settings':settings}]}


def posts():
    result=p.extract_json(p.run_postiz(['posts:list','--startDate','2026-11-02T00:00:00-03:00','--endDate','2026-11-05T00:00:00-03:00']))
    return result['posts'] if isinstance(result,dict) else result


def publish():
    if WHEN <= datetime.now(timezone.utc):
        raise ValueError('03/11/2026 12h Brasília já passou; data não será alterada automaticamente.')
    gate = json.loads(read(SOCIAL/'QA_FINAL.json'))
    if gate.get('approved') is not True or gate.get('source_sha256')!=digest(SOURCE):
        raise ValueError('Revisão final aprovada e hash do master são obrigatórios.')
    if gate.get('thumbnail_sha256')!=digest(EP/'publicacao/capa_youtube.jpg'):
        raise ValueError('Thumbnail não corresponde à revisão final.')
    for name,path in FILES.items():
        if gate.get('assets',{}).get(name)!=digest(path):
            raise ValueError('Asset não aprovado na revisão final: '+name)
    discover()
    state=json.loads(read(STATE)) if STATE.exists() else {'episode':'L05','scheduled_at':WHEN.isoformat(),'items':{}}
    if state.get('scheduled_at')!=WHEN.isoformat():
        raise ValueError('Estado usa outra data; reconciliar.')
    base=json.loads(read(ROOT/'.production-tools/postiz-https.json'))['url']
    assert base.startswith('https://')
    existing=posts()
    for name,path in FILES.items():
        rec=state['items'].setdefault(name,{})
        expected=payload(name,{'id':'','path':'PENDING'}, {'id':'','path':'PENDING'})
        signature=hashlib.sha256((digest(path)+json.dumps(expected,sort_keys=True,ensure_ascii=False)).encode()).hexdigest()
        if rec.get('signature') and rec['signature']!=signature:
            raise ValueError('Assinatura mudou; reconciliar antes de substituir '+name)
        rec['signature']=signature
        matches=[]
        for entry in existing:
            settings=entry.get('settings') or {}
            if isinstance(settings,str): settings=json.loads(settings)
            target=expected['posts'][0]
            if (entry.get('integration') or {}).get('id')==target['integration']['id'] and entry.get('content')==target['value'][0]['content'] and (settings.get('post_type','post')==target['settings'].get('post_type','post')):
                matches.append(entry)
        if len(matches)>1: raise ValueError('Duplicatas remotas: '+name)
        if matches:
            rec['post_id']=matches[0]['id'];rec['status']={k:matches[0].get(k) for k in ('state','releaseURL','releaseId','error','publishDate')};write(STATE,state);continue
        if rec.get('post_id') or rec.get('creation_attempted_at'):
            raise ValueError('Tentativa anterior ambígua; reconciliar '+name)
        if not rec.get('media'):
            rec['media']=p.upload(path);write(STATE,state)
        media=dict(rec['media'])
        if name!='youtube_feed': media={'id':'','path':base+urlsplit(media['path']).path}
        thumbnail=None
        if name=='youtube_feed':
            if not rec.get('thumbnail'):
                rec['thumbnail']=p.upload(EP/'publicacao/capa_youtube.jpg');write(STATE,state)
            thumbnail=rec['thumbnail']
        data=payload(name,media,thumbnail)
        target=SOCIAL/(name+'_ENVIO.json');write(target,data)
        if WHEN <= datetime.now(timezone.utc):
            raise ValueError('Horário solicitado passou durante a preparação; não criar agendamento passado.')
        rec['creation_attempted_at']=datetime.now(timezone.utc).isoformat();write(STATE,state)
        rec['response']=p.extract_json(p.run_postiz(['posts:create','--json',str(target)]));write(STATE,state)
        ids=p.post_ids({'post':rec['response']})
        if len(ids)!=1: raise ValueError('Resposta inesperada; não repetir '+name)
        rec['post_id']=ids[0];write(STATE,state)
        print(name+': agendado '+ids[0],flush=True)


def plan():
    result={name:{'file':str(path.relative_to(ROOT)),'integration':CHANNELS[name.split('_')[0]],'scheduled_at':WHEN.isoformat(),'exists':path.exists()} for name,path in FILES.items()}
    write(SOCIAL/'PLANO_CINCO_DESTINOS.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['plan','discover','derive','publish'],nargs='?',default='plan')
    parser.add_argument('--coordinator-approved',action='store_true')
    args=parser.parse_args()
    if args.command=='publish' and not args.coordinator_approved:
        parser.error('publish exige liberação explícita do coordenador e social/QA_FINAL.json')
    {'plan':plan,'discover':discover,'derive':derive,'publish':publish}[args.command]()
