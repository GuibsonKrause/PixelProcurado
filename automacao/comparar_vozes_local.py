"""Teste dos presets do mesmo SDK/motor integrado ao VoiceStudio, sem nuvem."""
from pathlib import Path
import os,sys,json,time,wave
ROOT=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
from supertonic import TTS
import numpy as np
from narrar_voicestudio import OUT,SAMPLE
OUT.mkdir(parents=True,exist_ok=True)
model=Path(os.environ['LOCALAPPDATA'])/'OmniVoice/hf_cache/models--Supertone--supertonic-3/snapshots/724fb5abbf5502583fb520898d45929e62f02c0b'
tts=TTS(model_dir=model,auto_download=False,intra_op_num_threads=4,inter_op_num_threads=1)
print('Voices:',tts.voice_style_names,flush=True)
for voice in ['M1','M3','M4','M5']:
    path=OUT/f'comparacao_{voice}.wav'
    if path.exists(): continue
    np.random.seed(42)
    start=time.monotonic()
    audio,duration=tts.synthesize(SAMPLE,voice_style=tts.get_voice_style(voice),lang='pt',speed=1.0,total_steps=10)
    pcm=(np.clip(np.asarray(audio).ravel(),-1,1)*32767).astype('<i2')
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(tts.sample_rate);w.writeframes(pcm.tobytes())
    path.with_suffix('.json').write_text(json.dumps({'voice':voice,'text':SAMPLE,'duration':float(np.asarray(duration).ravel()[0]),'speed':1.0,'steps':10,'engine':'supertonic3','device':'CPU','generation_seconds':time.monotonic()-start},ensure_ascii=False,indent=2),encoding='utf-8')
    print(voice,'gerada',flush=True)
