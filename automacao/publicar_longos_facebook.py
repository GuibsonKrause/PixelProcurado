"""Exporta cópias Full HD dos longos aprovados e publica agora no Facebook pelo Postiz."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import postiz_shorts as p

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'producao/POSTIZ_FACEBOOK_LONGOS_ESTADO.json'
FFMPEG = ROOT / '.production-tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
IDS = ('L01','L02','L03','L04')
DURATIONS = {'L01':427.04,'L02':309.766667,'L03':330.7,'L04':260.366667}
COPY = {
 'L01': 'GTA 6: o que é informação oficial e onde começa a teoria? 🔎\n\nNeste dossiê completo, organizamos lançamento, plataformas, Jason, Lucia e Leonida a partir dos anúncios e das apresentações da Rockstar. Uma cena pode mostrar muita coisa sem provar tudo que a gente imagina.\n\nQual investigação você quer acompanhar: personagens ou lugares de Leonida?\n\nRecorte do episódio: outubro de 2026. Consulte as fontes para anúncios posteriores.\nFontes: https://www.rockstargames.com/VI e https://www.rockstargames.com/VI/only-in-leonida',
 'L02': 'Jason quer uma vida fácil. Lucia tem um plano. Será que os dois querem o mesmo futuro? 🎮\n\nInvestigamos os perfis dos protagonistas de GTA 6, a premissa da história e o contraste entre intimidade e perigo. Melhorar de vida não significa concordar sobre o caminho — nem sobre o risco que vale correr.\n\nEssa é uma leitura editorial: exemplos hipotéticos não representam missões anunciadas ou uma previsão do final. Qual diferença pode pesar mais nessa parceria?\n\nRecorte do episódio: outubro de 2026.\nFontes: https://www.rockstargames.com/VI/only-in-leonida e https://www.rockstargames.com/VI',
 'L03': 'Vice City mudou só nos gráficos? O celular na plateia conta outra história. 🔎\n\nNeste episódio completo, comparamos imagens promocionais do clássico com materiais oficiais de GTA VI. Neon, rádio e ambição continuam na conversa, mas as formas de viver e mostrar a cidade também mudam.\n\nA relação entre as cenas é uma interpretação editorial; não pressupõe o mesmo endereço nem uma reconstrução do mapa antigo.\n\nQual lembrança da Vice City clássica precisa sobreviver: o rádio, a atmosfera das ruas ou a sensação de conquistar a cidade?\n\nRecorte: imagens selecionadas em outubro de 2026.\nFontes: https://www.rockstargames.com/games/vicecity e https://www.rockstargames.com/VI/media',
 'L04': 'O Trailer 2 de GTA 6 tem gameplay. Mas a câmera não resolve cada cena. 🔎\n\nNeste dossiê, separamos três dúvidas: gameplay e cenas prontas; console da captura e plataformas anunciadas; ilustração e screenshot. Um pôster não serve para medir gráficos, e captura no PS5 não significa, por si só, exclusividade.\n\nO episódio examina especificamente o Trailer 2 de 2025, sem classificar cada plano individualmente nem cobrir todos os materiais posteriores. Qual detalhe você quer ver investigado?\n\nFontes: https://www.rockstargames.com/VI/trailer-2\nComunicado da Rockstar: https://x.com/RockstarGames/status/1920181314092765494\nPlataformas e mídia: https://www.rockstargames.com/VI',
}
CREDIT = '\n\nImagens e trechos: Rockstar Games. Análise, gráficos e edição: Pixel Procurado. Narração sintética produzida com auxílio de IA. Análise independente, sem vínculo oficial com a Rockstar.\n\n#GTA6 #GTAVI #PixelProcurado'


def save(state):
 state['updated_at']=datetime.now(timezone.utc).isoformat()
 temp=STATE.with_suffix('.tmp')
 temp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 temp.replace(STATE)


def title(ep):
 return (ROOT/f'producao/{ep}/publicacao/01_TITULO.txt').read_text(encoding='utf-8').strip()


def caption(ep):
 return COPY[ep]+CREDIT


def probe(path):
 result=subprocess.run([str(FFMPEG),'-hide_banner','-i',str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace')
 duration=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',result.stderr)
 dimensions=re.search(r'Video:.*?(\d{3,5})x(\d{3,5})',result.stderr)
 if not duration or not dimensions: raise RuntimeError('Metadados de vídeo ausentes: '+str(path))
 h,m,s=map(float,duration.groups())
 return {'duration':h*3600+m*60+s,'width':int(dimensions[1]),'height':int(dimensions[2]),'h264':'Video: h264' in result.stderr,'aac':'Audio: aac' in result.stderr}


def encode(state,ids):
 for ep in ids:
  source=ROOT/f'producao/{ep}/exportacoes/Pixel_Procurado_{ep}_4K.mp4'
  output=source.with_name(f'Pixel_Procurado_{ep}_Facebook_1080p.mp4')
  assert source.is_file() and 2<=len(title(ep))<=100 and len(caption(ep))<5000
  checksum=hashlib.file_digest(source.open('rb'),'sha256').hexdigest()
  rec=state.setdefault('items',{}).setdefault(ep,{})
  if output.exists() and rec.get('source_sha256')==checksum and rec.get('qa',{}).get('full_decode_pass'):
   print(ep+': cópia Full HD já validada',flush=True);continue
  print(ep+': exportando 1920x1080, áudio original preservado',flush=True)
  command=[str(FFMPEG),'-hide_banner','-loglevel','error','-y','-threads','4','-i',str(source),'-map','0:v:0','-map','0:a:0','-vf','scale=1920:1080:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','21','-maxrate','4M','-bufsize','8M','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
  subprocess.run(command,check=True,capture_output=True)
  qa=probe(output)
  assert qa['width']==1920 and qa['height']==1080 and qa['h264'] and qa['aac']
  assert abs(qa['duration']-DURATIONS[ep])<0.15
  subprocess.run([str(FFMPEG),'-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  qa['full_decode_pass']=True
  rec.update(source=str(source.relative_to(ROOT)),source_sha256=checksum,video_file=str(output.relative_to(ROOT)),qa=qa,bytes=output.stat().st_size)
  save(state)
  print(f"{ep}: Full HD validado, {qa['duration']:.2f}s, {output.stat().st_size/1024**2:.1f} MiB",flush=True)


def all_posts():
 result=p.extract_json(p.run_postiz(['posts:list']))
 return result['posts'] if isinstance(result,dict) else result


def prepare(state,ids):
 channels=[i for i in p.integrations() if i.get('identifier')=='facebook' and i.get('name')=='Pixel Procurado' and not i.get('disabled')]
 assert len(channels)==1
 base=json.loads((ROOT/'.production-tools/postiz-https.json').read_text(encoding='utf-8-sig'))['url']
 for ep in ids:
  rec=state['items'][ep]
  assert rec['qa']['full_decode_pass']
  rec.update(integration_id=channels[0]['id'],title=title(ep),caption=caption(ep))
  if not rec.get('video'):
   print(ep+': enviando cópia Full HD ao Postiz',flush=True)
   rec['video']=p.upload(ROOT/rec['video_file']);save(state)
  media={'id':'','path':base+urlsplit(rec['video']['path']).path}
  payload={'type':'now','creationMethod':'CLI','date':datetime.now(timezone.utc).isoformat(),'shortLink':False,'tags':[],
   'posts':[{'integration':{'id':channels[0]['id']},'value':[{'content':rec['caption'],'image':[media],'delay':0}],
   'settings':{'__type':'facebook','post_type':'post','title':rec['title']}}]}
  pub=ROOT/f'producao/{ep}/publicacao'
  (pub/'LEGENDA_FACEBOOK_LONGO.txt').write_text(rec['caption']+'\n',encoding='utf-8')
  target=pub/'POSTIZ_FACEBOOK_LONGO_ENVIO.json'
  target.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  rec['payload_file']=str(target.relative_to(ROOT));save(state)


def publish(state,ids):
 existing=all_posts()
 for ep in ids:
  rec=state['items'][ep]
  matches=[e for e in existing if (e.get('integration') or {}).get('id')==rec['integration_id'] and e.get('content')==rec['caption']]
  if len(matches)>1:raise RuntimeError('Duplicação detectada; revisar '+ep)
  if matches:
   rec['post_id']=matches[0]['id'];save(state);continue
  if rec.get('post_id') or rec.get('creation_attempted_at'):raise RuntimeError('Tentativa anterior precisa de reconciliação: '+ep)
  assert rec.get('remote_absence_confirmed_at'),'Conferir vídeos remotos antes do envio.'
  target=ROOT/rec['payload_file']
  payload=json.loads(target.read_text(encoding='utf-8'))
  assert payload['type']=='now' and payload['posts'][0]['settings']['__type']=='facebook'
  payload['date']=datetime.now(timezone.utc).isoformat()
  target.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
  rec['creation_attempted_at']=datetime.now(timezone.utc).isoformat();save(state)
  response=p.extract_json(p.run_postiz(['posts:create','--json',str(target)]))
  rec['response']=response;save(state)
  post_ids=p.post_ids({'post':response})
  if len(post_ids)!=1:raise RuntimeError('Resposta inesperada; não repetir o envio: '+ep)
  rec['post_id']=post_ids[0];save(state)
  print(ep+': publicação imediata iniciada, '+post_ids[0],flush=True)


def status(state):
 posts={e['id']:e for e in all_posts()}
 for ep,rec in state.get('items',{}).items():
  entry=posts.get(rec.get('post_id'))
  if entry:
   rec['status']={k:entry.get(k) for k in ('id','state','releaseId','releaseURL','error','publishDate')}
   print(json.dumps({'episode':ep,**rec['status']},ensure_ascii=False),flush=True)
 save(state)


if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8')
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('command',choices=['encode','prepare','publish','status','check'])
 parser.add_argument('--ids',default=','.join(IDS))
 parser.add_argument('--confirm-publish-now',action='store_true')
 args=parser.parse_args();ids=args.ids.split(',')
 assert len(ids)==len(set(ids)) and all(i in IDS for i in ids)
 state=json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {'authorization':'Usuário solicitou publicar todos os longos prontos no Facebook em 02/11/2026.'}
 if args.command=='check':
  for ep in IDS:assert len(title(ep))<=100 and len(caption(ep))<5000
  print('Quatro títulos e legendas validados; envio configurado como now.')
 elif args.command=='encode':encode(state,ids)
 elif args.command=='prepare':prepare(state,ids)
 elif args.command=='publish':
  if not args.confirm_publish_now:parser.error('Exige --confirm-publish-now')
  publish(state,ids);status(state)
 else:status(state)
