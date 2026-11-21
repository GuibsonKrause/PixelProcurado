"""Segunda transcrição independente de trechos ambíguos, sem roteiro como prompt."""
import json, os
os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
import audio_l03 as a
from faster_whisper import WhisperModel
import numpy as np

model=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=1,
    download_root=str(a.ROOT/'.course-tools/models'),local_files_only=True)
tasks=[(4,0,5),(4,14,20),(4,46,52)]
rows=[]
for block,start,end in tasks:
    source=a.P/('gemini/bruto_v2' if block==4 else 'gemini/bruto_v1')/f'{a.STEMS[block]}_narracao.wav'
    temp=a.P/'revisao_temporaria.f32'
    a.producao.run(['-ss',start,'-t',end-start,'-i',source,'-ar','16000','-ac','1','-f','f32le',temp])
    samples=np.fromfile(temp,dtype=np.float32);temp.unlink()
    segs,_=model.transcribe(samples,language='pt',beam_size=3,vad_filter=False)
    row=dict(block=a.STEMS[block],start=start,end=end,text=' '.join(s.text.strip() for s in segs))
    rows.append(row);a.save('segunda_asr_B05_base.json',rows)
    print(json.dumps(row,ensure_ascii=False),flush=True)
