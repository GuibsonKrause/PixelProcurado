"""Re-transcribe selected passages with a larger model, keeping absolute timestamps."""
from processar_curso import ROOT, OUT, stamp
import json, sys, time
import av
import numpy as np
from faster_whisper import WhisperModel, BatchedInferencePipeline

jobs=json.loads((OUT/'trechos_para_revisar.json').read_text(encoding='utf-8'))
dest=OUT/'revisoes';dest.mkdir(exist_ok=True)
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(ROOT/'.course-tools'/'models'))
pipeline=BatchedInferencePipeline(model=model)
for job in jobs:
    path=next(ROOT.glob(job['lesson']+'_*.mp4'))
    start,end=job['start'],job['end']
    output=dest/f"{job['lesson']}_{start:04}_{end:04}.txt"
    if output.exists():continue
    print('REVIEW '+output.name,flush=True)
    chunks=[]
    with av.open(str(path)) as c:
        r=av.AudioResampler(format='fltp',layout='mono',rate=16000)
        for f in c.decode(audio=0):
            for o in r.resample(f): chunks.append(o.to_ndarray().reshape(-1))
        for o in r.resample(None):chunks.append(o.to_ndarray().reshape(-1))
    audio=np.concatenate(chunks)[int(start*16000):int(end*16000)]
    segs,info=pipeline.transcribe(audio,language='pt',beam_size=3,batch_size=4,vad_filter=True)
    lines=[]
    for s in segs:
        lines.append(f'[{stamp(start+s.start)}–{stamp(start+s.end)}] {s.text.strip()}')
    output.write_text('\n'.join(lines),encoding='utf-8')
    print('\n'.join(lines),flush=True)
