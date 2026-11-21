import sys
import os
import json
import subprocess

# Add local libraries
sys.path.extend([
    os.path.abspath(".course-tools"),
    os.path.abspath(".production-tools/python")
])

audio_wav = "producao/starlink/audio_original.wav"
clean_wav = "producao/starlink/audio_limpo.wav"
transcript_json = "producao/starlink/transcricao_completa.json"

# 1. Transcribe with faster-whisper
print("--- 1. Transcribing with faster-whisper ---", flush=True)
try:
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_wav, language="pt", beam_size=5, word_timestamps=True)
    print(f"Detected language: {info.language} ({info.language_probability:.2f})", flush=True)
    
    seg_list = []
    full_text_parts = []
    for s in segments:
        words = []
        if s.words:
            for w in s.words:
                words.append({
                    "word": w.word,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3)
                })
        seg_data = {
            "id": s.id,
            "start": round(s.start, 3),
            "end": round(s.end, 3),
            "text": s.text.strip(),
            "words": words
        }
        seg_list.append(seg_data)
        full_text_parts.append(s.text.strip())
        print(f"[{s.start:6.2f}s -> {s.end:6.2f}s] {s.text.strip()}", flush=True)

    with open(transcript_json, "w", encoding="utf-8") as f:
        json.dump({
            "duration": info.duration,
            "full_text": " ".join(full_text_parts),
            "segments": seg_list
        }, f, indent=2, ensure_ascii=False)
    print(f"Transcription saved to {transcript_json}", flush=True)

except Exception as e:
    print(f"Error in transcription: {e}", flush=True)
    import traceback
    traceback.print_exc()

# 2. Denoise and enhance audio using FFmpeg
print("\n--- 2. Denoising and enhancing audio ---", flush=True)
# Filters:
# - highpass=f=80: cut sub-bass rumble / mic handling / wind
# - lowpass=f=11000: cut high frequency electrical noise/hiss
# - afftdn=nf=-25:tn=1:ba=20: adaptive FFT denoiser (removes continuous background noise)
# - equalizer: gentle boost around 2.5kHz-3.5kHz for vocal intelligibility
# - acompressor: smooth out dynamic range so voice is clear and present
# - loudnorm: normalize to -16 LUFS (broadcasting standard for online video)
af_filter = (
    "highpass=f=85,"
    "lowpass=f=12000,"
    "afftdn=nf=-25:tn=1:ba=20,"
    "equalizer=f=3000:t=q:w=1.5:g=3,"
    "equalizer=f=250:t=q:w=1.0:g=-2,"
    "acompressor=threshold=-18dB:ratio=3:attack=5:release=50,"
    "loudnorm=I=-16:TP=-1.5:LRA=11"
)

cmd_denoise = [
    "ffmpeg", "-y",
    "-i", audio_wav,
    "-af", af_filter,
    "-ar", "48000",
    clean_wav
]
print(f"Running ffmpeg denoise...", flush=True)
res = subprocess.run(cmd_denoise, capture_output=True, text=True)
if res.returncode == 0:
    print(f"Clean audio created at {clean_wav}", flush=True)
else:
    print(f"Denoise error: {res.stderr}", flush=True)

print("Done processing.", flush=True)
