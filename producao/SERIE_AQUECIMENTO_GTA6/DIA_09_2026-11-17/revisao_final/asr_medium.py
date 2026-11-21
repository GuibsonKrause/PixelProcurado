import subprocess,sys,numpy as np
from faster_whisper import WhisperModel
v=sys.argv[1]
m=WhisperModel('medium',device='cpu',compute_type='int8')
for i,f in ((246.5,252.0),(118.0,123.0),(255.5,260.0),(95.5,99.0)):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(i),'-t',str(f-i),'-i',v,'-vn','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,dtype=np.float32)
    segs,_=m.transcribe(a,language='pt',beam_size=5)
    print(i,f,' '.join(s.text.strip() for s in segs),flush=True)
