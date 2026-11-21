"""L04: sequential native-4K Remotion overlays + FFmpeg; Python 3.12."""
import argparse,hashlib,json,math,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
import av,imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
P=ROOT/'producao/L04'; WORK=P/'projeto/render4k'; OUT=P/'exportacoes/Pixel_Procurado_L04_4K.mp4'
DATA=json.loads((P/'projeto/edicao_l04.json').read_text(encoding='utf8'))
FPS=30
def run(args,log):
 log.parent.mkdir(parents=True,exist_ok=True)
 with log.open('w',encoding='utf8') as f:
  p=subprocess.run([FF,'-hide_banner','-nostdin','-y',*map(str,args)],cwd=ROOT,stdout=f,stderr=f)
 if p.returncode:raise RuntimeError(log.read_text(encoding='utf8',errors='replace')[-4000:])
def validate_timeline():
 assert DATA['status']=='final-direction' and DATA['contractVersion']=='L04-1920-logical-v1'
 assert (DATA['width'],DATA['height'],DATA['fps'])==(3840,2160,30)
 assert DATA['frames']==math.ceil(DATA['duration']*30)
 assert (ROOT/DATA['voice']).is_file()
 pos=0
 for i,s in enumerate(DATA['shots']):
  assert s['fromFrame']==pos and s['frames']>0,(i,'continuity')
  assert round(s['start']*30)==pos and round(s['end']*30)==pos+s['frames']
  assert s['presentation'] in ['full','classic-card','graphic']
  assert s['graphic'] in ['','focus','headline','list','dates','radio']
  if s['file']:assert (ROOT/s['file']).is_file(),s['file']
  if s.get('focusRects'):assert s['zoom']==[1,1]
  if s['presentation']=='classic-card':
   v=s['viewport'];assert abs(v['width']/v['height']-10/7)<.0001
  if s['animate']:assert 1<s['animationFrames']<=s['frames']
  pos+=s['frames']
 assert pos==DATA['frames']
 previous=0
 for c in DATA['captions']:
  assert previous<=c['start']<c['end']<=DATA['duration']+.001,c
  assert '\ufffd' not in c['text'];previous=c['end']
def stamp(t):
 cs=round(max(0,t)*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
def srtstamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
HEADER='''[Script Info]
ScriptType: v4.00+
PlayResX: 3840
PlayResY: 2160
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial,84,&H00FFFFFF,&H00FFFFFF,&H30120C08,&H30120C08,-1,0,0,0,100,100,0,0,3,15,0,2,300,300,180,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def styled(text):
 text=text.replace('{','').replace('}','').replace('\n',r'\N')
 return re.sub(r'\b(Vice City|Real Dimez|identidade|nostalgia|memória|rádio)\b',r'{\\c&H003DD3FF&}\1{\\c&H00FFFFFF&}',text,flags=re.I)
def state(i,encoder):
 s=DATA['shots'][i];source=ROOT/s['file'] if s['file'] else None
 caps=[c for c in DATA['captions'] if c['end']>s['start'] and c['start']<s['end']]
 code=''.join((ROOT/f).read_text(encoding='utf8') for f in ['automacao/renderizar_l04.py','remotion/src/l04-overlays.tsx','remotion/src/l04-index.tsx','remotion/render-l04-overlays.mjs'])
 data=dict(shot=s,captions=caps,source=(source.stat().st_size,source.stat().st_mtime_ns) if source else None,code=code,encoder=encoder)
 return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),caps
def cached(i,encoder):
 target=WORK/f'{i:03}.mp4';marker=WORK/f'{i:03}.json'
 if not target.is_file() or not marker.is_file():return False
 m=json.loads(marker.read_text());return m.get('signature')==state(i,encoder)[0] and m.get('bytes')==target.stat().st_size
def clean_overlay(i):
 folder=(P/f'projeto/overlays/{i:03}').resolve();base=(P/'projeto/overlays').resolve()
 assert folder.parent==base and folder.name==f'{i:03}'
 removed=[]
 for f in folder.glob('frame-*.png'):
  assert f.parent.resolve()==folder;removed.append(dict(path=f.relative_to(ROOT).as_posix(),bytes=f.stat().st_size));f.unlink()
 if (folder/'complete.json').exists():(folder/'complete.json').unlink()
 with (WORK/'limpeza_derivados.jsonl').open('a',encoding='utf8') as log:log.write(json.dumps(dict(shot=i,reason='segment encoded and frame-count validated',removed=removed))+'\n')
def render(i,encoder='qsv',keep_overlays=False):
 if cached(i,encoder):print(f'Reuse {i}',flush=True);return
 started=time.monotonic();s=DATA['shots'][i];n=s['frames'];d=n/30;folder=P/f'projeto/overlays/{i:03}'
 component=''.join((ROOT/f).read_text(encoding='utf8') for f in ['remotion/src/l04-overlays.tsx','remotion/src/l04-index.tsx'])
 compact=json.dumps(s,ensure_ascii=False,separators=(',',':'))
 compact=re.sub(r'(?<=\d)\.0(?=[,}\]])','',compact)
 expected=hashlib.sha256((compact+component).encode()).hexdigest()
 marker_overlay=folder/'complete.json'
 complete=json.loads(marker_overlay.read_text()) if marker_overlay.exists() else {}
 count=s['animationFrames'] if s['animate'] else 1
 ready=complete.get('sig')==expected and complete.get('frames')==count and all((folder/f'frame-{j:04}.png').is_file() for j in range(count))
 if not ready:subprocess.run(['node',str(ROOT/'remotion/render-l04-overlays.mjs'),str(i)],cwd=ROOT/'remotion',check=True)
 done=json.loads((folder/'complete.json').read_text());assert done['frames']==(s['animationFrames'] if s['animate'] else 1)
 signature,caps=state(i,encoder);target=WORK/f'{i:03}.mp4';marker=WORK/f'{i:03}.json'
 events=[]
 for c in caps:
  a=max(c['start'],s['start']);b=min(c['end'],s['end']);tags=r'{\fad(45,35)}';ml=mr=mv=0
  if s.get('captionBox'):
   box=s['captionBox'];ml=round(box['x']*2);mr=3840-round((box['x']+box['width'])*2);mv=round(box['y']*2);tags=r'{\an7\fad(45,35)}'
  events.append(f'Dialogue: 0,{stamp(a-s["start"])},{stamp(b-s["start"])},Main,,{ml},{mr},{mv},,{tags}{styled(c["text"])}')
 ass=WORK/f'{i:03}.ass';ass.write_text(HEADER+'\n'.join(events),encoding='utf-8-sig');rel=ass.relative_to(ROOT).as_posix()
 source=ROOT/s['file'] if s['file'] else None
 if s['kind']=='graphic':
  inputs=['-f','lavfi','-i',f'color=c=0x080d15:s=3840x2160:r=30:d={d}'];base='[0:v]setsar=1[base]'
 elif s['presentation']=='classic-card':
  inputs=['-loop','1','-framerate','30','-i',source]
  box=s['viewport'];x,y,w,h=[round(box[k]*2) for k in ['x','y','width','height']];z0,z1=s.get('zoom',[1,1]);delta=z1-z0
  # Scale the entire 10:7 card; the source is never cropped to achieve camera motion.
  z=f'({z0}+({delta})*n/{max(1,n-1)})'
  base=f"color=c=0x080d15:s=3840x2160:r=30:d={d}[bg];[0:v]scale=w='trunc({w}*{z}/10)*10':h='trunc({w}*{z}/10)*7':eval=frame:flags=lanczos,setsar=1[card];[bg][card]overlay=x='{x}+({w}-overlay_w)/2':y='{y}+({h}-overlay_h)/2':shortest=1[base]"
 elif s['kind']=='video':
  inputs=['-ss',s['offset'],'-i',source];base='[0:v]fps=30,scale=3840:2160:flags=lanczos,setsar=1,setpts=PTS-STARTPTS[base]'
 else:
  inputs=['-i',source];z0,z1=s.get('zoom',[1,1]);fx,fy=s.get('focus',[.5,.46]);z=f'{z0}+({z1}-{z0})*on/{max(1,n-1)}'
  base=f"[0:v]scale=3840:2160:flags=lanczos,zoompan=z='{z}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d={n}:s=3840x2160:fps=30,setsar=1[base]"
 inputs+=['-framerate','30','-start_number','0','-i',folder/'frame-%04d.png']
 graph=f'[1:v]format=rgba,tpad=stop_mode=clone:stop_duration={d},setpts=PTS-STARTPTS[graphics]'
 filters=f"{base};{graph};[base][graphics]overlay=shortest=1,ass='{rel}',format=nv12[out]"
 codec=['-c:v','h264_qsv','-preset','medium','-global_quality','19','-look_ahead','0'] if encoder=='qsv' else ['-c:v','libx264','-preset','fast','-crf','19']
 run([*inputs,'-filter_complex_threads','1','-filter_complex',filters,'-map','[out]','-an','-frames:v',n,*codec,'-g','60',target],WORK/f'{i:03}.log')
 with av.open(str(target)) as c:
  v=c.streams.video[0];assert v.frames==n and (v.width,v.height)==(3840,2160),(i,v.frames,n)
 marker.write_text(json.dumps(dict(signature=signature,frames=n,bytes=target.stat().st_size,seconds=time.monotonic()-started)),encoding='utf8')
 if not keep_overlays:clean_overlay(i)
 print(f'Rendered {i} {s["start"]:.3f}-{s["end"]:.3f} in {time.monotonic()-started:.1f}s',flush=True)
def srt():
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.with_suffix('.srt').write_text('\n\n'.join(f'{i+1}\n{srtstamp(c["start"])} --> {srtstamp(c["end"])}\n{c["text"]}' for i,c in enumerate(DATA['captions']))+'\n',encoding='utf8')
def mux(encoder='qsv'):
 assert all(cached(i,encoder) for i in range(len(DATA['shots']))),'Missing/stale segments; render them before mux'
 concat=WORK/'concat.txt';concat.write_text('\n'.join(f"file '{i:03}.mp4'\nduration {s['frames']/30:.9f}" for i,s in enumerate(DATA['shots'])),encoding='utf8')
 OUT.parent.mkdir(parents=True,exist_ok=True)
 run(['-f','concat','-safe','0','-i',concat,'-i',ROOT/DATA['voice'],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-t',DATA['frames']/30,'-movflags','+faststart',OUT],WORK/'mux.log')
 log=(WORK/'mux.log').read_text(encoding='utf8');assert not re.search(r'non.monoton|invalid|error',log,re.I),log[-3000:]
 srt();print(OUT,flush=True)
def samples(indices):
 folder=P/'projeto/amostras';folder.mkdir(parents=True,exist_ok=True)
 for i in indices:
  s=DATA['shots'][i]
  run(['-i',WORK/f'{i:03}.mp4','-ss',s['start'],'-i',ROOT/DATA['voice'],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',s['frames']/30,'-movflags','+faststart',folder/f'plano_{i:03}_4K.mp4'],folder/f'plano_{i:03}_mux.log')
 manifest=[dict(index=i,start=DATA['shots'][i]['start'],end=DATA['shots'][i]['end'],graphic=DATA['shots'][i]['graphic'],file=f'plano_{i:03}_4K.mp4') for i in indices]
 (folder/'amostras.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--shots');ap.add_argument('--mux-only',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--srt-only',action='store_true');ap.add_argument('--samples',action='store_true');ap.add_argument('--keep-overlays',action='store_true');ap.add_argument('--encoder',choices=['qsv','cpu'],default='qsv');args=ap.parse_args()
 validate_timeline();WORK.mkdir(parents=True,exist_ok=True)
 if args.check:print('L04 timeline and sources valid');sys.exit()
 if args.srt_only:srt();sys.exit()
 indices=list(map(int,args.shots.split(','))) if args.shots else list(range(len(DATA['shots'])))
 if not args.mux_only:
  for i in indices:render(i,args.encoder,args.keep_overlays)
 if args.samples:samples(indices)
 elif args.mux_only or not args.shots:mux(args.encoder)
