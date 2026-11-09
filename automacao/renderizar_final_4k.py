"""Native 4K edit: Remotion graphics + FFmpeg camera moves, captions and Intel encoding."""
import json, math, re, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
import imageio_ffmpeg
import av
FF=imageio_ffmpeg.get_ffmpeg_exe()
DATA=json.loads((ROOT/'remotion/src/edicao.json').read_text(encoding='utf8'))
WORK=ROOT/'producao/L01/projeto/render4k';WORK.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'producao/L01/exportacoes/Pixel_Procurado_L01_4K.mp4'
def run(args,log):
 with log.open('w',encoding='utf8') as f:
  p=subprocess.run([FF,'-hide_banner','-y','-nostdin',*map(str,args)],cwd=ROOT,stdout=f,stderr=f)
 if p.returncode:raise RuntimeError(log.read_text(encoding='utf8',errors='replace')[-3000:])
def stamp(t):
 cs=round(max(0,t)*100);return f'{cs//360000}.{cs//6000%60:02}.{cs//100%60:02}.{cs%100:02}'.replace('.',':',2)
HEADER='''[Script Info]
ScriptType: v4.00+
PlayResX: 3840
PlayResY: 2160
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial,86,&H00FFFFFF,&H00FFFFFF,&H3020180C,&H3020180C,-1,0,0,0,100,100,0,0,3,16,0,2,300,300,180,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
allsubs=[]
for c in DATA['captions']:
 text=' '.join(w['word'] for w in c['words'])
 text=text.replace('Hoje gente','Hoje, a gente').replace('dupla sim,','dupla assim,')
 if text.endswith('esse quebra-'):text=text[:-len('esse quebra-')]+'esse quebra-cabeça.'
 if text.startswith('cabeça. '):text=text[len('cabeça. '):]
 text=text.replace('Grass Rivers','Grassrivers').replace('pixel procurado','Pixel Procurado')
 allsubs.append({**c,'text':text})
def styled(text):
 return re.sub(r'\b(Rockstar|Jason|Lucia|Leonida|fonte|evidência|hipótese|confiança|PC)\b',r'{\\c&H003DD3FF&}\1{\\c&H00FFFFFF&}',text,flags=re.I)
for i,s in enumerate(DATA['shots']):
 target=WORK/f'{i:03}.mp4'
 if target.exists():
  try:
   with av.open(str(target)) as c:valid=abs(c.duration/1e6-s['frames']/30)<.08
   if valid:print(f'Skip {i+1}/{len(DATA["shots"])}',flush=True);continue
  except Exception:pass
 overlay=ROOT/f'remotion/out/overlays/{i:03}.png'
 while not overlay.exists():time.sleep(1)
 time.sleep(.1)
 events=[]
 for c in allsubs:
  a=max(c['start'],s['start']);b=min(c['end'],s['end'])
  if b>a:
   events.append(f'Dialogue: 0,{stamp(a-s["start"])},{stamp(b-s["start"])},Main,,0,0,0,,{{\\fad(70,50)}}{styled(c["text"])}')
 ass=WORK/f'{i:03}.ass';ass.write_text(HEADER+'\n'.join(events),encoding='utf-8-sig')
 relative=ass.relative_to(ROOT).as_posix()
 source=ROOT/'videosGTAVI'/s['file'];n=s['frames'];d=n/30
 inputs=[]
 if s['kind']=='video':
  inputs=['-ss',s['offset'],'-i',source]
  base='[0:v]fps=30,scale=3840:2160:flags=lanczos,setsar=1,setpts=PTS-STARTPTS,eq=contrast=1.015:saturation=1.02[base]'
 else:
  inputs=['-i',source]
  z=f'1.035+0.035*on/{n}' if s['motion']%2==0 else f'1.07-0.035*on/{n}'
  x=f'(iw-iw/zoom)*(0.35+0.3*on/{n})' if s['motion']%2 else '(iw-iw/zoom)/2'
  base=f"[0:v]scale=4096:2304:force_original_aspect_ratio=increase,crop=4096:2304,zoompan=z='{z}':x='{x}':y='(ih-ih/zoom)/2':d={n}:s=3840x2160:fps=30,setsar=1,eq=contrast=1.015:saturation=1.02[base]"
 # Graphic layer rises gently into position; imagery stays continuous beneath it.
 graphic="[1:v]format=rgba[graphics]"
 filters=f"{base};{graphic};[base][graphics]overlay=x=0:y='16*max(0,1-t/0.35)':eval=frame,ass='{relative}',format=nv12[out]"
 run([*inputs,'-i',overlay,'-filter_complex_threads','2','-filter_complex',filters,'-map','[out]','-an','-frames:v',n,'-c:v','h264_qsv','-preset','medium','-global_quality','19','-look_ahead','0','-g','60',target],WORK/f'{i:03}.log')
 print(f'Rendered {i+1}/{len(DATA["shots"])}: {s["start"]:.2f}-{s["end"]:.2f}',flush=True)
concat=WORK/'concat.txt';concat.write_text('\n'.join(f"file '{i:03}.mp4'\nduration {s['frames']/30:.9f}" for i,s in enumerate(DATA['shots'])),encoding='utf8')
run(['-f','concat','-safe','0','-i',concat,'-i',ROOT/'producao/L01/voz/gemini/narracao_guibson2_normalizada.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-t',DATA['duration'],'-movflags','+faststart',OUT],WORK/'mux.log')
def srtstamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
srt=OUT.with_suffix('.srt');srt.write_text('\n\n'.join(f'{i+1}\n{srtstamp(c["start"])} --> {srtstamp(c["end"])}\n{c["text"]}' for i,c in enumerate(allsubs)),encoding='utf8')
with av.open(str(OUT)) as c:
 v=c.streams.video[0];a=c.streams.audio[0]
 report={'file':str(OUT),'duration':c.duration/1e6,'width':v.width,'height':v.height,'fps':float(v.average_rate),'video_codec':v.codec_context.name,'audio_codec':a.codec_context.name,'shots':len(DATA['shots']),'captions':len(allsubs),'narration_preserved':True}
 assert v.width==3840 and v.height==2160 and abs(c.duration/1e6-DATA['duration'])<.1
(WORK/'validacao.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report),flush=True)
