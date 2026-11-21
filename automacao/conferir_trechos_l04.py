"""Segundo ASR local pontual nas divergências de maior interesse; sem API."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'.course-tools'),str(ROOT/'.production-tools/python')]
from faster_whisper import WhisperModel
import numpy as np,producao
P=ROOT/'producao/L04/voz'
model=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=2,download_root=str(ROOT/'.course-tools/models'),local_files_only=True)
out=[]
for start,end in [(34.8,40.3),(145.9,149.3),(171.5,179.2),(247.8,253.2)]:
 dest=P/f'conferencia_{start}.f32'
 producao.run(['-ss',start,'-i',P/'narracao_bruta.wav','-t',end-start,'-ar','16000','-ac','1','-f','f32le',dest])
 audio=np.fromfile(dest,dtype=np.float32);dest.unlink()
 segments,info=model.transcribe(audio,language='pt',beam_size=1,initial_prompt='Rockstar. PlayStation. Pôster. Pixel Procurado. GTA seis. Jason e Lucia.')
 text=' '.join(s.text.strip() for s in segments);row=dict(start=start,end=end,text=text);out.append(row);print(row,flush=True)
(P/'segunda_conferencia_asr.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
