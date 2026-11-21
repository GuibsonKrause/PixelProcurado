import sys
from pathlib import Path
R=Path(r'C:\Users\guibson.krause\Documents\ChatGPT\GamePlay')
sys.path[:0]=[str(R/'.production-tools/python'),str(R/'.course-tools')]
from faster_whisper import WhisperModel
import numpy as np, subprocess, imageio_ffmpeg, tempfile
f=sys.argv[1]; model=sys.argv[2]
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',f,'-ar','16000','-ac','1','-f','f32le','tmp.f32'],check=True)
a=np.fromfile('tmp.f32',dtype=np.float32)
m=WhisperModel(model,device='cpu',compute_type='int8',cpu_threads=4,download_root=str(R/'.course-tools/models'),local_files_only=True)
segs,_=m.transcribe(a,language='pt',beam_size=5,word_timestamps=True,vad_filter=False,initial_prompt=None)
print(' '.join(f"{w.word.strip()}[{w.start:.2f}-{w.end:.2f}]" for s in segs for w in s.words))
