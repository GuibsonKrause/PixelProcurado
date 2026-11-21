"""Word-level local transcription for the fourteen vertical edits; preserves voice files."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import producao

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.production-tools/python'), str(ROOT / '.course-tools')]
from faster_whisper import WhisperModel
import numpy as np

ids = [f'C{i:02}' for i in range(1, 13)] + ['L01-R02', 'L01-R03']
model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4,
                     download_root=str(ROOT / '.course-tools/models'), local_files_only=True)
for rid in ids:
    target = ROOT / 'producao/shorts' / rid
    for name in ('voz', 'projeto', 'exportacoes', 'publicacao'):
        (target / name).mkdir(parents=True, exist_ok=True)
    source = ROOT / f'producao/cortes/audio_gemini/normalizados/{rid}_narracao_normalizada.wav'
    voice = target / 'voz/narracao.wav'
    if not voice.exists():
        shutil.copy2(source, voice)
    for suffix in ('NARRACAO', 'GEMINI'):
        shutil.copy2(ROOT / f'producao/cortes/{rid}_{suffix}.txt', target / f'voz/{suffix}.txt')
    output = target / 'voz/palavras_asr.json'
    if output.exists():
        print(f'{rid}: reuse word timestamps', flush=True)
        continue
    with tempfile.TemporaryDirectory(prefix='shorts-asr-') as temp:
        decoded = Path(temp) / 'audio.f32'
        producao.run(['-i', voice, '-vn', '-ar', '16000', '-ac', '1', '-f', 'f32le', decoded])
        samples = np.fromfile(decoded, dtype=np.float32)
    segments, info = model.transcribe(samples, language='pt', beam_size=5, vad_filter=True,
        word_timestamps=True, initial_prompt='GTA seis. Jason. Lucia. Brian. Raul Bautista. Leonida Keys. Grassrivers. Vice City. Rockstar. screenshots. Self Radio. Real Dimez. Cheetah.')
    words, lines = [], []
    for segment in segments:
        words.extend({'word': w.word.strip(), 'start': round(w.start, 3), 'end': round(w.end, 3),
                      'probability': round(w.probability, 4)} for w in (segment.words or []))
        lines.append({'start': segment.start, 'end': segment.end, 'text': segment.text.strip()})
    assert words and words[-1]['end'] <= info.duration + .5, rid
    output.write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding='utf8')
    (target / 'voz/segmentos_asr.json').write_text(json.dumps(lines, ensure_ascii=False, indent=2), encoding='utf8')
    print(f'{rid}: {len(words)} words / {info.duration:.2f}s', flush=True)
