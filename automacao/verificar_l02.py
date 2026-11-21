"""QA visual por amostragem e verificação técnica integral do arquivo L02."""
import argparse,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
import av,imageio_ffmpeg,numpy as np
from PIL import Image,ImageOps,ImageDraw
FF=imageio_ffmpeg.get_ffmpeg_exe();P=ROOT/'producao/L02';W=P/'projeto/render4k';Q=W/'qa';Q.mkdir(exist_ok=True)
D=json.loads((P/'projeto/edicao_l02.json').read_text(encoding='utf8'))
FINAL=P/'exportacoes/Pixel_Procurado_L02_4K.mp4'
def run(args):
 r=subprocess.run([FF,'-hide_banner','-nostdin','-y',*map(str,args)],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace')[-3000:])
 return r.stderr.decode(errors='replace')
def contact(samples):
 samples=[i for i in samples if (W/f'{i:03}.mp4').exists() and (W/f'{i:03}.json').exists() and (W/f'{i:03}.json').stat().st_mtime_ns>=(W/f'{i:03}.mp4').stat().st_mtime_ns]
 sheet=Image.new('RGB',(1440,310*((len(samples)+2)//3)),(8,12,20));draw=ImageDraw.Draw(sheet)
 for k,i in enumerate(samples):
  s=D['shots'][i];t=min(1.8,s['frames']/60)
  # Inspect fully-revealed staged graphics too.
  if s['graphic'] in ['questions','checklist']:t=min(s['frames']/30-.1,s['animationFrames']/30+.15)
  dst=Q/f'{i:03}.jpg'
  run(['-loglevel','error','-ss',t,'-i',W/f'{i:03}.mp4','-frames:v','1','-update','1',dst])
  with Image.open(dst) as im:sheet.paste(ImageOps.fit(im,(480,270)),((k%3)*480,(k//3)*310))
  time=s['start']+t;draw.text(((k%3)*480+8,(k//3)*310+280),f'{int(time)//60:02}:{int(time)%60:02} | {i:02} | {s["kind"]}',fill='white')
 dest=Q/('amostra.jpg' if len(samples)<10 else 'contato_final.jpg');sheet.save(dest,quality=92);print(dest,flush=True)
def validate():
 with av.open(str(FINAL)) as c:
  v=c.streams.video[0];a=c.streams.audio[0]
  info=dict(file=str(FINAL),duration=c.duration/1e6,video_duration=float(v.duration*v.time_base),audio_duration=float(a.duration*a.time_base),width=v.width,height=v.height,fps=float(v.average_rate),frames=v.frames,video_codec=v.codec_context.name,audio_codec=a.codec_context.name,audio_rate=a.codec_context.sample_rate,bytes=FINAL.stat().st_size)
  assert (v.width,v.height)==(3840,2160)
  assert abs(float(v.average_rate)-30)<.001
  assert abs(info['duration']-D['duration'])<.05
  assert abs(info['video_duration']-D['frames']/30)<1/30+.001
  assert abs(v.frames-D['frames'])<=1
 # Decode the entire delivered file to catch corrupt segments or broken concatenation.
 integrity=run(['-v','error','-i',FINAL,'-f','null','-'])
 assert not integrity.strip(),integrity
 (Q/'decodificacao_integral.txt').write_text('Decodificação integral concluída sem erros.\n',encoding='utf8')
 signals=[]
 for name,src in [('original',ROOT/D['voice']),('exportado',FINAL)]:
  dest=Q/f'{name}.f32';run(['-loglevel','error','-i',src,'-vn','-ar','16000','-ac','1','-f','f32le',dest]);signals.append(np.fromfile(dest,dtype=np.float32))
 correlations={}
 for t in [1,30,60,100,140,180,220,260,300,306]:
  a,b=[s[t*16000:min(len(s),(t+3)*16000)] for s in signals];n=min(len(a),len(b));correlations[str(t)]=float(np.corrcoef(a[:n],b[:n])[0,1])
 assert min(correlations.values())>.98,correlations
 assert abs(len(signals[0])-len(signals[1]))/16000<.05
 loud=run(['-i',FINAL,'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
 loudness=json.loads(loud[loud.rfind('{'):loud.rfind('}')+1])
 info.update(audio_correlation=correlations,loudness=loudness,shots=len(D['shots']),captions=len(D['captions']),animated_shots=sum(s['animate'] for s in D['shots']),full_decode_pass=True)
 (Q/'validacao_final.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(info),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--sample',action='store_true');ap.add_argument('--contact-only',action='store_true');args=ap.parse_args()
 contact([0,24,33,49,50,61] if args.sample else [0,1,3,6,11,17,20,24,28,30,33,34,35,37,39,40,44,48,49,50,52,55,56,60,61,67,72,75])
 if not args.sample and not args.contact_only:validate()
