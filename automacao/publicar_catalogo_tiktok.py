"""Publicação idempotente do catálogo Pixel no TikTok via Postiz."""
import argparse,json,sys,hashlib,subprocess,urllib.request,urllib.error
from fractions import Fraction
from uuid import uuid4
from r2_media import R2Media
from pathlib import Path
from datetime import datetime,timezone
import postiz_shorts as postiz
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'producao/TIKTOK_CATALOGO_2026-11-10'
STATE=BASE/'POSTIZ_ESTADO.json'
def read(p):return p.read_text(encoding='utf-8-sig').strip()
def write(p,v):
 t=p.with_suffix('.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');t.replace(p)
def cli(args):return postiz.extract_json(postiz.run_postiz(args))
def current_posts():
 r=cli(['posts:list','--startDate','2026-01-01T00:00:00Z','--endDate','2027-01-01T00:00:00Z']);return r.get('posts',[]) if isinstance(r,dict) else r
def prepare(state):
 inventory=json.loads(read(BASE/'INVENTARIO.json'));items=state.setdefault('items',{})
 special={'ESPECIAL_PRE_LANCAMENTO_2026-11-06_longo':'GTA 6 vai humilhar o seu eu de 2013','ESPECIAL_PRE_LANCAMENTO_2026-11-06_short':'GTA 6: sua roupa pode entregar você','L08_longo':'GTA 6: quem deve a quem em Leonida?','L08_short':'GTA 6: o aluguel grátis de Jason tem uma cobrança','L06_short':'Vice City e Port Gellhorn brilham por motivos diferentes'}
 for item in inventory['items']:
  key=item['id'];path=ROOT/item['path'];ep=path.parent.parent;pub=ep/'publicacao'
  title=special.get(key,item.get('title'));assert title,key
  caps=[ROOT/c for c in item['cover_candidates'] if c.endswith('capa_youtube.jpg')]
  if not caps:caps=[ROOT/c for c in item['cover_candidates'] if c.endswith('.jpg') and 'teste_A' in c or c.endswith('thumbnail_confirmado_mesmo.jpg')]
  if key.startswith('ESPECIAL'):
   caps=list((ep/'social/capas/V2').glob('short_vertical*.jpg' if key.endswith('short') else 'longo_youtube*.jpg'))
  if key=='L08_short':caps=list((ROOT/'producao/shorts/L08').rglob('*capa*.jpg')) or caps
  assert caps and caps[0].is_file(),f'capa ausente {key}'
  descfile=pub/'02_DESCRICAO.txt'
  if not descfile.exists():descfile=pub/'DESCRICAO.txt'
  desc=read(descfile) if descfile.exists() else ''
  if key.startswith('ESPECIAL'):
   desc='Análise do material de pré-lançamento de GTA VI. Episódio produzido em 06/11/2026. Imagens: Rockstar Games.'
  text=title+'\n\n'+desc
  if len(text)>1850:text=text[:1800].rsplit('\n',1)[0]
  if not any(s in text.lower() for s in ('narração sintética','narracao sintetica')):text+='\n\nNarração sintética com auxílio de IA.'
  if '#PixelProcurado' not in text:text+='\n#GTA6 #GTAVI #PixelProcurado'
  record=items.setdefault(key,{})
  record.update({'source':str(path.relative_to(ROOT)),'source_bytes':path.stat().st_size,'probe':item['probe'],'title':title,'content':text,'approved_cover':str(caps[0].relative_to(ROOT)),'cover_status':'PREPARED_NOT_ATTACHABLE_CUSTOM_IMAGE_API_USES_FRAME','cover_timestamp_ms':0,'public_playback_quality':'NOT_VERIFIED'})
  record.setdefault('state','READY')
 state.update({'state':state.get('state') if state.get('state')=='BLOCKED_APP_AUDIT' else 'READY','error':state.get('error') if state.get('state')=='BLOCKED_APP_AUDIT' else None,'next_action':'Publish DIRECT_POST and verify actual public TikTok URL','pending_checks':['Independent final review','Public processing quality and selected cover frame']})
 write(STATE,state)
def publish(state,key):
 assert state.get('state')!='BLOCKED_APP_AUDIT', 'TikTok application audit blocks public API publishing; use official Studio or resolve application audit first'
 creator=json.loads(read(BASE/'CREATOR_INFO.json'));assert creator['error']['code']=='ok',creator['error']
 assert 'PUBLIC_TO_EVERYONE' in creator['data']['privacy_level_options']
 integrations=postiz.integrations();matches=[i for i in integrations if i.get('identifier')=='tiktok' and not i.get('disabled')];assert len(matches)==1
 integration=matches[0]['id'];state['integration_id']=integration
 record=state['items'][key]
 if record.get('post') or record.get('post_id') or record['state'] in ('CREATING','PUBLISHED'):raise RuntimeError('Post existente ou criação incerta: consultar status antes de repetir')
 existing=[r for r in current_posts() if integration in str(r.get('integration','')) and record['title'] in str(r.get('content','')) and r.get('state')!='ERROR']
 if existing:record['state']='REMOTE_MATCH_REVIEW';record['remote_matches']=existing;write(STATE,state);raise RuntimeError('Possível duplicata remota')
 path=ROOT/record['source'];meta=record['probe'];video=next(s for s in meta['streams'] if s['codec_type']=='video')
 assert float(meta['format']['duration'])<=creator['data']['max_video_post_duration_sec']
 assert max(video['width'],video['height'])<=4096 and 23<=float(Fraction(video['r_frame_rate']))<=60 and path.stat().st_size<=4_000_000_000
 if not record.get('media'):
  record['r2_key']=f'publicacoes/{uuid4().hex}.mp4';write(STATE,state)
  record['media'],_=R2Media().stage(path,record['r2_key']);state['uploads_attempted']=state.get('uploads_attempted',0)+1;write(STATE,state)
 media={**record['media'],'thumbnailTimestamp':0}
 settings={'__type':'tiktok','title':record['title'][:90],'privacy_level':'PUBLIC_TO_EVERYONE','duet':not creator['data']['duet_disabled'],'stitch':not creator['data']['stitch_disabled'],'comment':not creator['data']['comment_disabled'],'autoAddMusic':'no','brand_content_toggle':False,'brand_organic_toggle':False,'video_made_with_ai':True,'content_posting_method':'DIRECT_POST'}
 payload={'type':'now','creationMethod':'CLI','date':datetime.now(timezone.utc).isoformat(),'shortLink':False,'tags':[],'posts':[{'integration':{'id':integration},'value':[{'content':record['content'],'image':[media],'delay':0}],'settings':settings}]}
 request=BASE/(key+'_ENVIO.json');write(request,payload)
 record['state']='CREATING';record['requested_visibility']='PUBLIC_TO_EVERYONE';record['created_at']=datetime.now(timezone.utc).isoformat();write(STATE,state)
 result=cli(['posts:create','--json',str(request)])
 record['post']=result
 rows=result if isinstance(result,list) else [result]
 record['post_id']=next((r.get('postId') or r.get('id') for r in rows if isinstance(r,dict)),None)
 record['state']='SUBMITTED';state['state']='SUBMITTED';write(STATE,state);print('SUBMITTED',key,json.dumps(result,ensure_ascii=False),flush=True)
def status(state):
 posts=current_posts();lookup={r['id']:r for r in posts}
 for key,record in state.get('items',{}).items():
  if not record.get('post_id'):continue
  remote=lookup.get(record['post_id'])
  if not remote:continue
  record['remote_state']=remote.get('state');record['releaseURL']=remote.get('releaseURL');record['last_status_at']=datetime.now(timezone.utc).isoformat();record['state']=remote.get('state','UNKNOWN')
  record['confirmed_public_url']=bool(record['state']=='PUBLISHED' and '/video/' in str(record.get('releaseURL')))
  record['remote_snapshot']=remote
 state['published_items']=sum(bool(r.get('confirmed_public_url')) for r in state.get('items',{}).values());write(STATE,state)
 for key,r in state.get('items',{}).items():
  if r.get('post_id'):print(key,r['state'],r.get('releaseURL'),r.get('remote_snapshot',{}).get('error'))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','publish','status']);parser.add_argument('--id');a=parser.parse_args();state=json.loads(read(STATE))
 if a.action=='prepare':prepare(state);print('READY',len(state['items']))
 elif a.action=='publish':assert a.id;publish(state,a.id)
 else:status(state)
