"""Normaliza a narração completa, exporta MP3 e gera transcrição para revisão."""
import json
from pathlib import Path
import wave
import sys
import producao

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / 'producao/L01/voz'
raw = VOICE / 'voicestudio/narracao_M5_bruta.wav'
if '--revisada' in sys.argv:
    raw = VOICE / 'voicestudio/narracao_M5_revisada.wav'
wav = VOICE / 'narracao_normalizada.wav'
mp3 = VOICE / 'narracao_M5.mp3'
srt = VOICE / 'narracao_M5_transcricao.srt'
if not raw.exists():
    raise SystemExit('Conclua a geração dos blocos primeiro.')
if not wav.exists():
    producao.normalize(raw, wav)
if not mp3.exists():
    producao.run(['-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', mp3])
log = producao.run(['-i', wav, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
stats = json.loads(log[log.rfind('{'):log.rfind('}')+1])
with wave.open(str(wav), 'rb') as w:
    report = {'duration_seconds': w.getnframes()/w.getframerate(),
              'sample_rate': w.getframerate(), 'channels': w.getnchannels(),
              'loudness_measured': stats, 'voice': 'M5', 'engine': 'Supertonic-3'}
(VOICE / 'validacao_audio.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2), flush=True)
if not srt.exists():
    producao.transcribe(wav, srt, 'base' if '--revisada' in sys.argv else 'small')
print('WAV, MP3 e transcrição gerados.', flush=True)
