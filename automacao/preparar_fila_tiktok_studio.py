"""Fila local de arquivos/captions; não publica nem acessa TikTok."""
import json,re
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'producao/TIKTOK_CATALOGO_2026-11-10'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def caption(title,description):
 lines=[line for line in description.splitlines() if not re.match(r'(?i)\s*(Imagem local:|Capítulos?:|\d{1,2}:\d{2}\s)',line) and not line.strip().startswith('#')]
 title=title.replace(' #Shorts','')
 text=title+'\n\n'+'\n'.join(lines).strip()
 if len(text)>1700:text=text[:1700].rsplit('\n',1)[0]
 if 'narração sintética' not in text.lower():text+='\n\nNarração sintética com auxílio de IA.'
 return text.strip()+'\n\n#GTA6 #GTAVI #PixelProcurado'
state=load(BASE/'POSTIZ_ESTADO.json');quality=load(BASE/'qualidade_maxima/QUALIDADE.json');quality={i['id']:i for i in quality['items']}
studio_state=load(BASE/'TIKTOK_STUDIO_ESTADO.json')
items=[];captiondir=BASE/'captions';captiondir.mkdir(exist_ok=True)
for key,old in state['items'].items():
 source=ROOT/old['source'];pub=source.parent.parent/'publicacao'
 if key=='L08_short':pub=ROOT/'producao/shorts/L08/publicacao'
 title=old['title'];description=old['content'].split('\n\n',1)[-1]
 titlefile=pub/'TITULOS_AB.txt'
 if key.startswith('L08') and titlefile.exists():
  lines=titlefile.read_text(encoding='utf-8-sig').splitlines()
  ix=next((i for i,l in enumerate(lines) if 'RECOMENDADO' in l.upper()),None)
  if ix is not None:title=next(l.strip() for l in lines[ix+1:] if l.strip())
 for name in ('02_DESCRICAO.txt','DESCRICAO.txt'):
  f=pub/name
  if f.exists():description=f.read_text(encoding='utf-8-sig').strip();break
 title=title.replace(' #Shorts','');text=caption(title,description);captionfile=captiondir/(key+'.txt');captionfile.write_text(text+'\n',encoding='utf-8')
 cover=ROOT/old['approved_cover'];probe=old['probe'];ready=False;qa='Approved original master; maximum-quality source review/reexport pending'
 if key in quality:
  q=quality[key];source=Path(q['path']);probe=q['probe'];ready=key in ('L08_longo','L08_short');qa='Independent reviewer approved L08 long and short 4K reexports' if ready else 'Reexport technical QA available; independent visual review pending'
 else:
  v=next(s for s in probe['streams'] if s['codec_type']=='video');ready=key.endswith('_longo') and max(v['width'],v['height'])>=3840
  if ready:qa='Existing approved 4K master retained without transcoding'
 v=next(s for s in probe['streams'] if s['codec_type']=='video');assert source.is_file() and cover.is_file() and len(text)<2000
 assert max(v['width'],v['height'])<=4096 and 23<=float(Fraction(v['r_frame_rate']))<=60 and source.stat().st_size<4_000_000_000
 srt=list((ROOT/old['source']).parent.glob(Path(old['source']).stem+'.srt'))
 items.append({'id':key,'ready_for_upload':ready,'video_path':str(source.resolve()),'bytes':source.stat().st_size,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'duration':float(probe['format']['duration']),'title':title,'caption':text,'caption_file':str(captionfile.resolve()),'cover_path':str(cover.resolve()),'subtitles_burned_in':True,'srt_sidecar':str(srt[0].resolve()) if srt else None,'quality_qa':qa,'public_visibility_required':True,'aigc_label_required':True,'public_url':studio_state.get('items',{}).get(key,{}).get('public_url'),'historical_metadata':'Original production context preserved; no promise of current release dates','original_reference':old['source']})
items.sort(key=lambda i:({'L08_short':0,'L08_longo':1}.get(i['id'],2),i['id']))
save(BASE/'FILA_STUDIO.json',{'account':'@pixelprocurado','count':len(items),'starlink':'EXCLUDED_BY_USER','items':items})
print(json.dumps([i for i in items if i['id'].startswith('L08')],ensure_ascii=False,indent=2));print('QUEUE_READY',len(items),'UPLOAD_READY',sum(i['ready_for_upload'] for i in items))
