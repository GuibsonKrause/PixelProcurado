import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.course-tools'),str(ROOT/'.production-tools/python')]
from PIL import Image,ImageOps,ImageDraw
import av,imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
WORK=ROOT/'producao/L01/projeto/render4k'
FINAL=ROOT/'producao/L01/exportacoes/Pixel_Procurado_L01_4K.mp4'
QA=WORK/'qa';QA.mkdir(exist_ok=True)
data=json.loads((ROOT/'remotion/src/edicao.json').read_text(encoding='utf8'))
samples=[0,4,9,12,14,21,28,32,34,39,45,48,52,57,63,67,70,73,78,84,87]
sheet=Image.new('RGB',(1440,310*((len(samples)+2)//3)),(10,12,18))
draw=ImageDraw.Draw(sheet)
for k,i in enumerate(samples):
 clip=WORK/f'{i:03}.mp4'
 if not clip.exists():continue
 seek=min(1.5,data['shots'][i]['frames']/60)
 dst=QA/f'{i:03}.jpg'
 subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-ss',str(seek),'-i',str(clip),'-frames:v','1','-update','1',str(dst)],check=True)
 with Image.open(dst) as im:sheet.paste(ImageOps.fit(im,(480,270)),((k%3)*480,(k//3)*310))
 t=data['shots'][i]['start']+seek
 draw.text(((k%3)*480+10,(k//3)*310+278),f'{int(t)//60:02}:{int(t)%60:02} | plano {i+1}',fill='white')
sheet.save(QA/'contato_final.jpg',quality=90)
print(QA/'contato_final.jpg')
if FINAL.exists():
 with av.open(str(FINAL)) as c:
  v=c.streams.video[0];a=c.streams.audio[0]
  info={'duration':c.duration/1e6,'width':v.width,'height':v.height,'fps':float(v.average_rate),'codec':v.codec_context.name,'audio_codec':a.codec_context.name,'audio_rate':a.codec_context.sample_rate,'frames':v.frames,'bytes':FINAL.stat().st_size}
  assert (v.width,v.height)==(3840,2160)
  assert abs(float(v.average_rate)-30)<.001
  assert abs(info['duration']-data['duration'])<.1
  assert abs(v.frames-data['frames'])<=1
 (QA/'parametros_final.json').write_text(json.dumps(info,indent=2),encoding='utf8')
 print(json.dumps(info))
 import numpy as np
 signals=[]
 for label,source in [('original',ROOT/'producao/L01/voz/gemini/narracao_guibson2_normalizada.wav'),('exportado',FINAL)]:
  dest=QA/f'{label}.f32'
  subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-i',str(source),'-vn','-ar','16000','-ac','1','-f','f32le',str(dest)],check=True)
  signals.append(np.fromfile(dest,dtype=np.float32))
 correlations={}
 for t in [5,60,120,180,240,300,360,420]:
  a,b=[x[t*16000:(t+4)*16000] for x in signals]
  n=min(len(a),len(b));correlations[str(t)]=float(np.corrcoef(a[:n],b[:n])[0,1])
 audio={'seconds_original':len(signals[0])/16000,'seconds_exportado':len(signals[1])/16000,'correlation_by_second':correlations}
 assert min(correlations.values())>.98,audio
 assert abs(audio['seconds_exportado']-audio['seconds_original'])<.1
 (QA/'audio_preservado.json').write_text(json.dumps(audio,indent=2),encoding='utf8')
 print(json.dumps(audio))
