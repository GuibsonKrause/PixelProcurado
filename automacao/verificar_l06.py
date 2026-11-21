"""L06 contact sheets and final technical verification; sampling is not full editorial QA."""
import argparse,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
import av,imageio_ffmpeg,numpy as np
from PIL import Image,ImageOps,ImageDraw
FF=imageio_ffmpeg.get_ffmpeg_exe();P=ROOT/'producao/L06';W=P/'projeto/render4k';Q=W/'qa'
D=json.loads((P/'projeto/edicao_l06.json').read_text(encoding='utf8'));FINAL=P/'exportacoes/Pixel_Procurado_L06_4K.mp4'
def run(args):
 r=subprocess.run([FF,'-hide_banner','-nostdin','-y',*map(str,args)],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace')[-3000:])
 return r.stderr.decode(errors='replace')
def contact(indices):
 Q.mkdir(parents=True,exist_ok=True);entries=[]
 for i in indices:
  s=D['shots'][i];src=W/f'{i:03}.mp4'
  if not src.exists():continue
  with av.open(str(src)) as c:
   v=c.streams.video[0];assert (v.width,v.height,v.frames)==(3840,2160,s['frames'])
  times=[.2,max(1,s['animationFrames']/30+.1),s['frames']/30-.08]
  times += [(r.get('cue',0)+19)/30 for r in s.get('focusRects',[])]
  times += [(cue+19)/30 for cue in s.get('cues',[]) if cue>=0]
  times=sorted(set(round(min(s['frames']/30-.04,max(.04,t)),3) for t in times))
  for j,t in enumerate(times):
   dst=Q/f'{i:03}_{j}.jpg';run(['-loglevel','error','-ss',t,'-i',src,'-frames:v','1','-update','1','-vf','scale=960:540',dst]);entries.append((i,t,dst))
 sheet=Image.new('RGB',(1440,310*((len(entries)+2)//3)),(8,12,20));draw=ImageDraw.Draw(sheet)
 for k,(i,t,dst) in enumerate(entries):
  with Image.open(dst) as im:sheet.paste(ImageOps.fit(im,(480,270)),((k%3)*480,(k//3)*310))
  draw.text(((k%3)*480+8,(k//3)*310+280),f'{i:02} | +{t:.2f}s | {D["shots"][i]["graphic"] or "base"}',fill='white')
 dest=Q/'contato_amostra.jpg';sheet.save(dest,quality=92);print(dest,flush=True)

def validate_samples(indices):
 Q.mkdir(parents=True,exist_ok=True);results=[]
 for i in indices:
  s=D['shots'][i];src=P/f'projeto/amostras/plano_{i:03}_4K.mp4'
  assert src.is_file(),src
  with av.open(str(src)) as c:
   v=c.streams.video[0];a=c.streams.audio[0]
   assert (v.width,v.height,v.frames)==(3840,2160,s['frames'])
   assert float(v.average_rate)==30 and v.codec_context.name=='h264'
   assert a.codec_context.name=='aac' and a.codec_context.sample_rate==48000
   duration=float(v.duration*v.time_base)
   assert abs(duration-s['frames']/30)<.034
  errors=run(['-v','error','-i',src,'-f','null','-']);assert not errors.strip(),errors
  signals=[]
  for source,seek in [(ROOT/D['voice'],s['start']),(src,0)]:
   args=[FF,'-v','error','-ss',str(seek+.1),'-i',str(source),'-t',str(min(3,s['frames']/30-.2)),'-vn','-ar','16000','-ac','1','-f','f32le','pipe:1']
   proc=subprocess.run(args,capture_output=True,check=True)
   signals.append(np.frombuffer(proc.stdout,dtype=np.float32))
  n=min(map(len,signals));assert n>8000
  correlation=float(np.corrcoef(signals[0][:n],signals[1][:n])[0,1]);assert correlation>.98,(i,correlation)
  results.append(dict(shot=i,start=s['start'],end=s['end'],frames=s['frames'],duration=duration,audio_correlation=correlation,full_decode_pass=True,file=str(src)))
 (Q/'validacao_amostras.json').write_text(json.dumps(dict(samples=results,voice_reference=D['voice'],editorial_review='Visual sampling of entry, cues and hold; no full subjective listening claimed.'),ensure_ascii=False,indent=2),encoding='utf8')
 print('Samples decoded, 4K30 H264/AAC and voice alignment verified',flush=True)

def sample_reel(indices):
 folder=P/'projeto/amostras';listing=folder/'concat_amostra.txt'
 listing.write_text('\n'.join(f"file '../render4k/{i:03}.mp4'\nduration {D['shots'][i]['frames']/30:.9f}" for i in indices),encoding='utf8')
 splits=''.join(f'[a{k}]' for k in range(len(indices)))
 filters=[f'[1:a]asplit={len(indices)}{splits}']
 for k,i in enumerate(indices):
  s=D['shots'][i];filters.append(f"[a{k}]atrim=start={s['start']}:duration={s['frames']/30},asetpts=PTS-STARTPTS[b{k}]")
 filters.append(''.join(f'[b{k}]' for k in range(len(indices)))+f'concat=n={len(indices)}:v=0:a=1[audio]')
 log=run(['-f','concat','-safe','0','-i',listing,'-i',ROOT/D['voice'],'-filter_complex',';'.join(filters),'-map','0:v','-map','[audio]','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',folder/'L06_AMOSTRA_4K.mp4'])
 (folder/'amostra_mux.log').write_text(log,encoding='utf8')
 assert not re.search(r'non.monoton|invalid|error',log,re.I),log[-3000:]
 with av.open(str(folder/'L06_AMOSTRA_4K.mp4')) as c:
  v=c.streams.video[0];expected=sum(D['shots'][i]['frames'] for i in indices)
  assert (v.width,v.height,v.frames)==(3840,2160,expected)
  assert abs(float(v.duration*v.time_base)-expected/30)<.034
 errors=run(['-v','error','-i',folder/'L06_AMOSTRA_4K.mp4','-f','null','-']);assert not errors.strip(),errors
 print(folder/'L06_AMOSTRA_4K.mp4',flush=True)
def validate():
 Q.mkdir(parents=True,exist_ok=True)
 with av.open(str(FINAL)) as c:
  v=c.streams.video[0];a=c.streams.audio[0]
  info=dict(file=str(FINAL),duration=c.duration/1e6,video_duration=float(v.duration*v.time_base),audio_duration=float(a.duration*a.time_base),width=v.width,height=v.height,fps=float(v.average_rate),frames=v.frames,video_codec=v.codec_context.name,audio_codec=a.codec_context.name,audio_rate=a.codec_context.sample_rate,bytes=FINAL.stat().st_size)
  assert (v.width,v.height)==(3840,2160) and v.codec_context.name=='h264'
  assert float(v.average_rate)==30 and v.frames==D['frames']
  assert abs(info['video_duration']-D['frames']/30)<1/30+.001
  assert abs(info['duration']-D['duration'])<.05
  assert a.codec_context.name=='aac' and a.codec_context.sample_rate==48000
 integrity=run(['-v','error','-i',FINAL,'-f','null','-']);assert not integrity.strip(),integrity
 (Q/'decodificacao_integral.txt').write_text('MP4 inteiro decodificado sem erros.\n',encoding='utf8')
 signals=[]
 for name,src in [('referencia_normalizada',ROOT/D['voice']),('exportado',FINAL)]:
  dst=Q/f'{name}.f32';run(['-loglevel','error','-i',src,'-vn','-ar','16000','-ac','1','-f','f32le',dst]);signals.append(np.fromfile(dst,dtype=np.float32))
 correlations={}
 for t in [1,*[round(D['duration']*f) for f in [.1,.25,.5,.75,.9]],int(D['duration'])-4]:
  a,b=[s[t*16000:(t+3)*16000] for s in signals];n=min(len(a),len(b));assert n>=16000
  correlations[str(t)]=float(np.corrcoef(a[:n],b[:n])[0,1])
 assert min(correlations.values())>.98,correlations
 assert abs(len(signals[0])-len(signals[1]))/16000<.05
 loud=run(['-i',FINAL,'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']);loudness=json.loads(loud[loud.rfind('{'):loud.rfind('}')+1])
 mux=(W/'mux.log').read_text(encoding='utf8');assert not re.search(r'non.monoton|invalid|error',mux,re.I)
 info.update(audio_correlation=correlations,audio_reference=D['voice'],loudness=loudness,shots=len(D['shots']),captions=len(D['captions']),full_decode_pass=True,editorial_review='sampled, see contact sheet; no claim of full subjective listening')
 (Q/'validacao_final.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(info),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--shots',default='0,3,5,11,16,29,36,46,55,62,71,75,81,84');ap.add_argument('--sample',action='store_true');ap.add_argument('--validate-only',action='store_true');args=ap.parse_args()
 if not args.validate_only:contact(list(map(int,args.shots.split(','))))
 if args.sample:
  indices=list(map(int,args.shots.split(',')));validate_samples(indices);sample_reel(indices)
 if not args.sample:validate()
