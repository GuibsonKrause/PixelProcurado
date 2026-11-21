"""Segundo ASR local pontual nas divergências de maior interesse; sem API."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'.course-tools'),str(ROOT/'.production-tools/python')]
from faster_whisper import WhisperModel
import numpy as np,producao
P=ROOT/'producao/L05/voz'
model=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=2,download_root=str(ROOT/'.course-tools/models'),local_files_only=True)
out=[]
for start,end in [(127.5,134.5),(203.0,207.5),(234.0,239.0),(244.3,250.0)]:
 dest=P/f'conferencia_{start}.f32'
 producao.run(['-ss',start,'-i',P/'narracao_bruta.wav','-t',end-start,'-ar','16000','-ac','1','-f','f32le',dest])
 audio=np.fromfile(dest,dtype=np.float32);dest.unlink()
 segments,info=model.transcribe(audio,language='pt',beam_size=1,initial_prompt='Cheetah. Aerofólio. GTA seis. Um prédio ocupando a lateral. Pensa numa foto de viagem.')
 text=' '.join(s.text.strip() for s in segments);row=dict(start=start,end=end,text=text);out.append(row);print(row,flush=True)
(P/'segunda_conferencia_asr.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
