"""ASR (faster-whisper small) de trechos de video; decodifica com ffmpeg para float32 16 kHz.
uso: py -3.12 asr_trechos.py <saida.json> <video>:<ini>:<fim> ...
"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

m = WhisperModel('small', device='cpu', compute_type='int8')
res = []
for spec in sys.argv[2:]:
    v, i, f = spec.rsplit(':', 2)
    i, f = float(i), float(f)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(i), '-t', str(f - i), '-i', v, '-vn', '-ac', '1',
                          '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32)
    rms = float(np.sqrt(np.mean(a ** 2))) if a.size else 0.0
    segs, _ = m.transcribe(a, language='pt', beam_size=5, word_timestamps=True, vad_filter=False)
    pal = [(round(w.start + i, 2), round(w.end + i, 2), w.word.strip()) for s in segs for w in s.words]
    txt = ' '.join(p[2] for p in pal)
    res.append({'video': v, 'inicio': i, 'fim': f, 'rms': round(rms, 4), 'texto': txt, 'palavras': pal})
    print(f'{v.split(chr(92))[-1]} {i}-{f} rms={rms:.4f}: {txt}', flush=True)
json.dump(res, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
