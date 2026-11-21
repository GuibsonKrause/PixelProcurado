"""ASR independente dos blocos retornados, sem modificar WAVs."""
import json, re, sys, difflib, unicodedata
from pathlib import Path
import audio_l03 as a
from faster_whisper import WhisperModel
import numpy as np

model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,
    download_root=str(a.ROOT/'.course-tools/models'),local_files_only=True)
report=[]
for stem in a.STEMS:
    source=a.P/'gemini/bruto_v1'/f'{stem}_narracao.wav'
    if not source.exists():continue
    out=a.P/f'{stem}_diagnostico_asr.json'
    if stem==a.STEMS[0]:out=a.P/'L03_B01_diagnostico_asr.json'
    if out.exists(): words=json.loads(out.read_text(encoding='utf8'))
    else:
        decoded=a.P/f'{stem}_diagnostico.f32'
        a.producao.run(['-i',source,'-ar','16000','-ac','1','-f','f32le',decoded])
        samples=np.fromfile(decoded,dtype=np.float32);decoded.unlink()
        segments,_=model.transcribe(samples,language='pt',beam_size=5,vad_filter=True,word_timestamps=True)
        words=[dict(word=w.word.strip(),start=round(w.start,3),end=round(w.end,3),probability=round(w.probability,4)) for s in segments for w in(s.words or [])]
        assert words
        a.save(out.name,words)
    ref=re.sub(r'<[^>]+>','',(a.P/f'{stem}_GEMINI.txt').read_text(encoding='utf8')).split()
    def norm(t):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',t.lower()))
    diffs=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,[norm(x['word']) for x in words],[norm(x) for x in ref],autojunk=False).get_opcodes():
        if tag!='equal':diffs.append(dict(kind=tag,start=words[min(i,len(words)-1)]['start'],end=words[max(i,j-1)]['end'],asr=' '.join(x['word'] for x in words[i:j]),script=' '.join(ref[k:l]),asr_indices=[i,j],script_indices=[k,l]))
    report.append(dict(block=stem,script_words=len(ref),asr_words=len(words),diffs=diffs))
    a.save('diagnostico_divergencias_v1.json',report)
    print(json.dumps(report[-1],ensure_ascii=False,indent=2),flush=True)
