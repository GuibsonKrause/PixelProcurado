"""Compara as retomadas locais com a locução integral e monta uma cópia revisada."""
import difflib
import json
import re
import sys
import unicodedata
import wave
from pathlib import Path

import audio_l05 as a

import numpy as np
from faster_whisper import WhisperModel

P = a.P = a.ROOT / 'producao/L06/voz'
raw_path = P / '03_NARRACAO_narracao.wav'
paragraphs = (P.parent/'01_NARRACAO.txt').read_text(encoding='utf8').strip().split('\n\n')
original_words = json.loads((P/'L06_INTEGRAL_asr.json').read_text(encoding='utf8'))['words']
intervals = {
    13: (173.0, 187.47),
    18: (234.92, 245.1),
    19: (245.1, 259.23),
    21: (280.70, 294.82),
}


def norm(word):
    return re.sub('[^a-z0-9]', '', unicodedata.normalize('NFD', word.lower()))


def compare(ref, got):
    a = [norm(x) for x in ref.split()]
    b = [norm(x['word']) for x in got]
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return matcher.ratio()


def load(path):
    with wave.open(str(path)) as wav:
        assert (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) == (24000,1,2)
        return np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').copy()


def clip(samples, words):
    # Preserve brief speech lead-in and a natural gap at the splice.
    start = max(0, words[0]['start'] - .20)
    end = min(len(samples)/24000, words[-1]['end'] + .42)
    result = samples[round(start*24000):round(end*24000)].copy()
    fade = np.linspace(0,1,120)
    result[:120] = result[:120]*fade
    result[-120:] = result[-120:]*fade[::-1]
    return result, start


def shift(words, offset):
    return [{**w, 'start':round(w['start']+offset,3), 'end':round(w['end']+offset,3)} for w in words]


model = WhisperModel('small', device='cpu', compute_type='int8',cpu_threads=4,
                     download_root=str(a.ROOT/'.course-tools/models'),local_files_only=True)
original = load(raw_path)
cursor, output_time = 0.0, 0.0
assembled, aligned, report = [], [], []
for n, (start, end) in intervals.items():
    retake_dir = 'retomadas_v2' if n in {19,21} else 'retomadas'
    path = P/f'{retake_dir}/L06_P{n:02d}_narracao.wav'
    if not path.is_file():
        report.append(dict(paragraph=n, decision='ausente'))
        continue
    samples = load(path)
    f32 = P/f'L06_P{n:02d}.f32'
    a.producao.run(['-i', path, '-ar','16000','-ac','1','-f','f32le',f32])
    audio = np.fromfile(f32,dtype=np.float32)
    f32.unlink()
    segments, _ = model.transcribe(audio,language='pt',beam_size=5,vad_filter=True,word_timestamps=True,
                                   initial_prompt='Rockstar Games, Port Gellhorn, Mount Kalaga, Leonida Keys, Grassrivers, Vice City, Ambrosia.')
    got = [dict(word=w.word.strip(),start=w.start,end=w.end,probability=w.probability) for s in segments for w in (s.words or [])]
    before = [w for w in original_words if start <= w['start'] < end]
    text = paragraphs[n-1]
    if n == 21:
        cut = next((i for i,w in enumerate(got) if norm(w['word']) == 'nas'), None)
        if cut is not None:
            got = got[cut:]
        text = text.split('Nas Keys',1)[1]
        text = 'Nas Keys' + text
    old, new = compare(text,before), compare(text,got)
    spoken = ' '.join(norm(w['word']) for w in got)
    place_clear = 'kalaga' in spoken.split() if n in {19,21} else True
    six_places = spoken.startswith('nas keys') if n == 21 else True
    use = bool(got) and new >= .87 and new >= old and place_clear and six_places
    report.append(dict(paragraph=n, original_score=old, retake_score=new, decision='retomada' if use else 'original',
                       original=' '.join(w['word'] for w in before), retake=' '.join(w['word'] for w in got),
                       original_bounds=[start,end]))
    if not use:
        continue
    assembled.append(original[round(cursor*24000):round(start*24000)])
    aligned.extend(shift([w for w in original_words if cursor <= w['start'] < start], output_time-cursor))
    output_time += start-cursor
    inserted, trim = clip(samples,got)
    assembled.append(inserted)
    aligned.extend(shift(got, output_time-trim))
    output_time += len(inserted)/24000
    cursor = end
assembled.append(original[round(cursor*24000):])
aligned.extend(shift([w for w in original_words if w['start']>=cursor],output_time-cursor))
assert aligned[0]['start'] == original_words[0]['start']
a.save('revisao_retomadas.json', report)
if cursor > 0:
    with wave.open(str(P/'narracao_bruta_revisada.wav'),'wb') as wav:
        wav.setparams((1,2,24000,0,'NONE','not compressed'))
        wav.writeframes(np.concatenate(assembled).tobytes())
    a.save('palavras_asr.json',aligned)
    (P/'transcricao_asr.txt').write_text(' '.join(w['word'] for w in aligned)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
