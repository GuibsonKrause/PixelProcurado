import sys
import os
import wave
import json
import numpy as np

sys.path.extend([
    os.path.abspath(".course-tools"),
    os.path.abspath(".production-tools/python")
])

from faster_whisper import WhisperModel

audio_wav = "producao/starlink/audio_original.wav"

with wave.open(audio_wav, "rb") as wf:
    sample_rate = wf.getframerate()
    num_frames = wf.getnframes()
    raw_data = wf.readframes(num_frames)
    audio_np = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0

print(f"Loaded audio: {len(audio_np)} samples at {sample_rate}Hz = {len(audio_np)/sample_rate:.2f}s", flush=True)

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_np, language="pt", beam_size=5, word_timestamps=True)

print("Transcription started:", flush=True)
all_segments = []
for s in segments:
    words = []
    if s.words:
        for w in s.words:
            words.append({"word": w.word, "start": round(w.start, 2), "end": round(w.end, 2)})
    item = {
        "start": round(s.start, 2),
        "end": round(s.end, 2),
        "text": s.text.strip(),
        "words": words
    }
    all_segments.append(item)
    print(f"[{item['start']:6.2f} -> {item['end']:6.2f}] {item['text']}", flush=True)

with open("producao/starlink/whisper_exato.json", "w", encoding="utf-8") as f:
    json.dump(all_segments, f, indent=2, ensure_ascii=False)

print("Saved exact whisper transcription to producao/starlink/whisper_exato.json", flush=True)
