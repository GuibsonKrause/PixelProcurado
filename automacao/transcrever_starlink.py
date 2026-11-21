import subprocess
import os
import sys

os.makedirs("producao/starlink", exist_ok=True)
audio_wav = "producao/starlink/audio_original.wav"

cmd = [
    "ffmpeg", "-y",
    "-i", r"C:\Users\guibson.krause\Downloads\IMG_3177.MOV",
    "-vn",
    "-ac", "1",
    "-ar", "16000",
    audio_wav
]
print("Extracting audio...", flush=True)
subprocess.run(cmd, check=True)
print("Audio extracted successfully.", flush=True)

# Test faster_whisper
try:
    from faster_whisper import WhisperModel
    print("faster_whisper is installed!", flush=True)
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_wav, language="pt", beam_size=5)
    print(f"Detected language: {info.language} with probability {info.language_probability:.2f}", flush=True)
    
    transcript_path = "producao/starlink/transcricao.json"
    import json
    results = []
    full_text = []
    for s in segments:
        print(f"[{s.start:.2f}s -> {s.end:.2f}s] {s.text}", flush=True)
        results.append({
            "start": s.start,
            "end": s.end,
            "text": s.text.strip(),
            "words": [{"word": w.word, "start": w.start, "end": w.end, "probability": w.probability} for w in (s.words or [])]
        })
        full_text.append(s.text.strip())
        
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump({"text": " ".join(full_text), "segments": results}, f, indent=2, ensure_ascii=False)
    print("Transcription saved.", flush=True)

except Exception as e:
    print(f"Whisper failed or not installed: {e}", flush=True)
