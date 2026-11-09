"""Render L02: animated native-4K Remotion overlays, FFmpeg camera and subtitles."""
import argparse,hashlib,json,math,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
import av,imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
P=ROOT/'producao/L02'; WORK=P/'projeto/render4k';WORK.mkdir(parents=True,exist_ok=True)
OUT=P/'exportacoes/Pixel_Procurado_L02_4K.mp4'; OUT.parent.mkdir(exist_ok=True)
DATA=json.loads((P/'projeto/edicao_l02.json').read_text(encoding='utf8'))
def run(args,log):
 with log.open('w',encoding='utf8') as f:
  p=subprocess.run([FF,'-hide_banner','-nostdin','-y',*map(str,args)],cwd=ROOT,stdout=f,stderr=f)
 if p.returncode:raise RuntimeError(log.read_text(encoding='utf8',errors='replace')[-4000:])
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
 return re.sub(r'\b(Jason|Lucia|confiança|liberdade|recomeço|risco|riscos|escolha|escolhas|futuro|controle)\b',r'{\\c&H003DD3FF&}\1{\\c&H00FFFFFF&}',text,flags=re.I)
def render(i):
 s=DATA['shots'][i];n=s['frames'];d=n/30
 folder=P/f'projeto/overlays/{i:03}'
 # Ready marker is written only after every animation frame has been rendered.
 deadline=time.monotonic()+1800
 component_mtime=(ROOT/'remotion/src/l02-overlays.tsx').stat().st_mtime_ns
 while not (folder/'complete.json').is_file() or (folder/'complete.json').stat().st_mtime_ns < component_mtime:
  if time.monotonic()>deadline:raise RuntimeError(f'Overlay {i} not ready after 30 min')
  time.sleep(2)
 source=ROOT/'videosGTAVI'/s['file'] if s['file'] else None
 caps=[c for c in DATA['captions'] if c['end']>s['start'] and c['start']<s['end']]
 state=dict(shot=s,captions=caps,overlay=(folder/'complete.json').read_text(),source=(source.stat().st_size,source.stat().st_mtime_ns) if source else None,renderer=Path(__file__).read_text(encoding='utf8'))
 sig=hashlib.sha256(json.dumps(state,sort_keys=True).encode()).hexdigest()
 target=WORK/f'{i:03}.mp4';marker=WORK/f'{i:03}.json'
 if target.exists() and marker.exists() and json.loads(marker.read_text())['signature']==sig:
  print(f'Reuse {i+1}/{len(DATA["shots"])}',flush=True);return
 events=[]
 for c in caps:
  a=max(c['start'],s['start']);b=min(c['end'],s['end'])
  events.append(f'Dialogue: 0,{stamp(a-s["start"])},{stamp(b-s["start"])},Main,,0,0,0,,{{\\fad(55,40)}}{styled(c["text"])}')
 ass=WORK/f'{i:03}.ass';ass.write_text(HEADER+'\n'.join(events),encoding='utf-8-sig')
 rel=ass.relative_to(ROOT).as_posix()
 if s['kind']=='video':
  inputs=['-ss',s['offset'],'-i',source]
  base='[0:v]fps=30,scale=3840:2160:flags=lanczos,setsar=1,setpts=PTS-STARTPTS[base]'
 elif s['kind']=='graphic':
  inputs=['-f','lavfi','-i',f'color=c=0x080d15:s=3840x2160:r=30:d={d}'];base='[0:v]setsar=1[base]'
 else:
  inputs=['-i',source]
  z0,z1=s.get('zoom',[1.02,1.055] if i%2==0 else [1.055,1.02])
  fx,fy=s.get('focus',[.5,.46])
  z=f'{z0}+({z1}-{z0})*on/{max(1,n-1)}'
  x=f'(iw-iw/zoom)*{fx}';y=f'(ih-ih/zoom)*{fy}'
  if 'zoom' not in s and i%4==3:x=f'(iw-iw/zoom)*(0.35+0.2*on/{max(1,n-1)})'
  base=f"[0:v]scale=4096:2304:force_original_aspect_ratio=increase,crop=4096:2304,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=3840x2160:fps=30,setsar=1[base]"
 inputs+=['-framerate','30','-start_number','0','-i',folder/'frame-%04d.png']
 graph=f'[1:v]format=rgba,tpad=stop_mode=clone:stop_duration={d},setpts=PTS-STARTPTS[graphics]'
 fade=f',fade=t=out:st={max(0,d-.25)}:d=0.25' if i==len(DATA['shots'])-1 else ''
 filters=f"{base};{graph};[base][graphics]overlay=shortest=1,ass='{rel}'{fade},format=nv12[out]"
 run([*inputs,'-filter_complex_threads','2','-filter_complex',filters,'-map','[out]','-an','-frames:v',n,'-c:v','h264_qsv','-preset','medium','-global_quality','19','-look_ahead','0','-g','60',target],WORK/f'{i:03}.log')
 with av.open(str(target)) as c: assert c.streams.video[0].frames==n,(i,c.streams.video[0].frames,n)
 marker.write_text(json.dumps(dict(signature=sig,frames=n)),encoding='utf8')
 print(f'Rendered {i+1}/{len(DATA["shots"])} | {s["start"]:.2f}–{s["end"]:.2f}',flush=True)
def mux():
 concat=WORK/'concat.txt'
 concat.write_text('\n'.join(f"file '{i:03}.mp4'\nduration {s['frames']/30:.9f}" for i,s in enumerate(DATA['shots'])),encoding='utf8')
 run(['-f','concat','-safe','0','-i',concat,'-i',ROOT/DATA['voice'],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-t',DATA['duration'],'-movflags','+faststart',OUT],WORK/'mux.log')
 log=(WORK/'mux.log').read_text(encoding='utf8')
 assert not re.search(r'non.monoton|invalid|error',log,re.I),log[-3000:]
 OUT.with_suffix('.srt').write_text('\n\n'.join(f'{i+1}\n{srtstamp(c["start"])} --> {srtstamp(c["end"])}\n{c["text"]}' for i,c in enumerate(DATA['captions'])),encoding='utf8')
 print(f'FINAL: {OUT}',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--shots');ap.add_argument('--mux-only',action='store_true');args=ap.parse_args()
 if not args.mux_only:
  for i in map(int,args.shots.split(',')) if args.shots else range(len(DATA['shots'])):render(i)
 if args.mux_only or not args.shots:mux()
