"""Medições e transcrição local L05; não faz chamadas pagas."""
import argparse, difflib, json, re, sys, unicodedata, wave
from pathlib import Path
import producao

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.production-tools/python'), str(ROOT/'.course-tools')]
P = ROOT/'producao/L05/voz'
STEMS = [f'L05_B{i:02}' for i in range(1,5)]

def save(name, data):
    (P/name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')

def metric(path):
    import numpy as np
    with wave.open(str(path)) as w:
        frames = w.readframes(w.getnframes())
        info = dict(file=str(path.relative_to(ROOT)), duration=w.getnframes()/w.getframerate(),
                    sample_rate=w.getframerate(), channels=w.getnchannels(), sample_width=w.getsampwidth(), frames=w.getnframes())
        assert w.getsampwidth()==2 and w.getnchannels()==1
    samples = np.frombuffer(frames, dtype='<i2').astype(float)/32768
    peak = abs(samples).max()
    info['sample_peak_dbfs'] = float(20*np.log10(peak))
    info['clipped_samples'] = int((abs(samples)>=32767/32768).sum())
    log = producao.run(['-i', path, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    info['loudnorm'] = json.loads(log[log.rfind('{'):log.rfind('}')+1])
    log = producao.run(['-i', path, '-af', 'silencedetect=noise=-40dB:d=0.5', '-f', 'null', '-'])
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    if len(starts)>len(ends): ends.append(info['duration'])
    info['silences_40db_500ms'] = [dict(start=a,end=b,duration=b-a) for a,b in zip(starts,ends)]
    return info

def assemble():
    rows=[]; offset=0
    dest=P/'narracao_bruta.wav'
    assert not dest.exists(),dest
    with wave.open(str(dest),'wb') as target:
        for stem in STEMS:
            path=P/'gemini/bruto_v1'/f'{stem}_narracao.wav'
            row=metric(path); row['offset']=offset
            script=re.sub(r'<[^>]+>', '', (P/f'{stem}_GEMINI.txt').read_text(encoding='utf8'))
            row['script_words']=len(script.split()); row['words_per_minute']=row['script_words']*60/row['duration']
            with wave.open(str(path)) as w:
                if not rows: target.setparams(w.getparams())
                else: assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(rows[0]['sample_rate'],rows[0]['channels'],rows[0]['sample_width'])
                target.writeframes(w.readframes(w.getnframes()))
            offset+=row['duration']; rows.append(row)
    save('medicoes_blocos.json',rows); save('medicoes_integral_bruto.json',metric(dest))
    assert sum(r['script_words'] for r in rows)>650
    print(json.dumps(rows,ensure_ascii=False,indent=2),flush=True)

def transcribe():
    from faster_whisper import WhisperModel
    import numpy as np
    model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,
        download_root=str(ROOT/'.course-tools/models'),local_files_only=True)
    rows=json.loads((P/'medicoes_blocos.json').read_text(encoding='utf8'))
    allwords=[]; allsegments=[]
    for stem,row in zip(STEMS,rows):
        out=P/f'{stem}_asr.json'
        if out.exists(): result=json.loads(out.read_text(encoding='utf8'))
        else:
            path=ROOT/row['file']; decoded=P/f'{stem}.f32'
            producao.run(['-i',path,'-ar','16000','-ac','1','-f','f32le',decoded])
            samples=np.fromfile(decoded,dtype=np.float32); decoded.unlink()
            segments,info=model.transcribe(samples,language='pt',beam_size=1,vad_filter=True,word_timestamps=True)
            words=[]; lines=[]
            for segment in segments:
                words.extend(dict(word=w.word.strip(),start=round(w.start,3),end=round(w.end,3),probability=round(w.probability,4)) for w in (segment.words or []))
                lines.append(dict(start=segment.start,end=segment.end,text=segment.text.strip()))
            assert words and words[-1]['end']<=row['duration']+.5
            result=dict(words=words,segments=lines);save(out.name,result)
        for item in result['words']:
            allwords.append({**item,'start':round(item['start']+row['offset'],3),'end':round(item['end']+row['offset'],3),'block':stem})
        for item in result['segments']:
            allsegments.append({**item,'start':round(item['start']+row['offset'],3),'end':round(item['end']+row['offset'],3)})
        print(f'{stem}: {len(result["words"])} palavras ASR',flush=True)
    save('palavras_asr.json',allwords);save('segmentos_asr.json',allsegments)
    (P/'transcricao_asr.txt').write_text('\n'.join(s['text'] for s in allsegments),encoding='utf8')
    reference=(P.parent/'01_NARRACAO.txt').read_text(encoding='utf8').split()
    def norm(t): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',t.lower()))
    diffs=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,[norm(x['word']) for x in allwords],[norm(x) for x in reference],autojunk=False).get_opcodes():
        if tag!='equal': diffs.append(dict(kind=tag,start=allwords[min(i,len(allwords)-1)]['start'],end=allwords[max(i,j-1)]['end'],asr=' '.join(x['word'] for x in allwords[i:j]),script=' '.join(reference[k:l]),asr_indices=[i,j],script_indices=[k,l]))
    save('revisao_asr.json',diffs)
    print(json.dumps(diffs,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['assemble','asr','normalized']);a=p.parse_args()
    if a.stage=='assemble':assemble()
    elif a.stage=='asr':transcribe()
    else:save('medicoes_integral_normalizado.json',metric(P/'narracao_normalizada.wav'))
