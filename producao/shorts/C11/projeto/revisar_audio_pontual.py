import sys,json
from pathlib import Path
sys.path[:0]=['.production-tools/python','.course-tools','automacao']
import producao,numpy as np
from faster_whisper import WhisperModel
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2,download_root='.course-tools/models',local_files_only=True)
for rid,start,end in [('C11',16,31),('C12',81,84.28)]:
 folder=Path('producao/shorts')/rid/'voz';out=folder/f'revisao_{start}.wav'
 if not out.exists():producao.run(['-ss',start,'-i',folder/'narracao.wav','-t',end-start,'-ar','16000','-ac','1',out])
 temp=folder/f'revisao_{start}.f32'
 if not temp.exists():producao.run(['-i',out,'-f','f32le',temp])
 seg,_=model.transcribe(np.fromfile(temp,dtype=np.float32),language='pt',beam_size=5,vad_filter=False,word_timestamps=True,initial_prompt='Jason. Brian. Raul Bautista.')
 segments=list(seg)
 data=[dict(start=float(s.start+start),end=float(s.end+start),text=s.text) for s in segments]
 words=[dict(start=round(float(w.start+start),3),end=round(float(w.end+start),3),word=w.word.strip(),probability=float(w.probability)) for s in segments for w in (s.words or [])]
 old=json.loads((folder/'palavras_asr.json').read_text(encoding='utf8'))
 merged=[w for w in old if float(w['end'])<=start or float(w['start'])>=end]+words
 merged.sort(key=lambda w:w['start'])
 (folder/'palavras_asr.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding='utf8')
 (folder/f'revisao_palavras_{start}.json').write_text(json.dumps(words,ensure_ascii=False,indent=2),encoding='utf8')
 (folder/f'revisao_pontual_{start}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(rid,start,data,flush=True)


