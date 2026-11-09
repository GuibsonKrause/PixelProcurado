"""Geração local via API do VoiceStudio. Reutiliza blocos existentes e registra parâmetros."""
import argparse
import json
from pathlib import Path
import time
import urllib.request
import wave
import os,sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'producao/L01/voz/voicestudio'
SDK = None
SAMPLE = ('No Pixel Procurado, cada pista vem acompanhada da fonte. '
          'GTA seis tem uma data anunciada. Mas uma informação oficial e uma teoria não são a mesma coisa. '
          'Vamos investigar o que a Rockstar revelou sobre Jason, Lucia e Leonida.')

def generate(text, voice, dest, speed):
    payload = {'model':'supertonic3','voice':voice,'input':text,'language':'pt',
               'response_format':'wav','speed':speed,'seed':42}
    if dest.exists():
        print('Já existe:',dest.name,flush=True)
        return
    req=urllib.request.Request('http://127.0.0.1:3900/v1/audio/speech',
        data=json.dumps(payload).encode('utf-8'),headers={'Content-Type':'application/json'})
    started=time.monotonic()
    if SDK is not None:
        import numpy as np
        np.random.seed(42)
        arr,_=SDK.synthesize(text,voice_style=SDK.get_voice_style(voice),lang='pt',speed=speed,total_steps=10)
        pcm=(np.clip(np.asarray(arr).ravel(),-1,1)*32767).astype('<i2')
        with wave.open(str(dest),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(SDK.sample_rate);w.writeframes(pcm.tobytes())
        payload['execution']='Supertonic SDK 1.3.1, same engine as VoiceStudio; local CPU'
        payload['steps']=10
    else:
        with urllib.request.urlopen(req,timeout=900) as r:
            content=r.read()
            if not content.startswith(b'RIFF'): raise ValueError('Resposta não é WAV RIFF')
        dest.write_bytes(content)
    with wave.open(str(dest),'rb') as w: duration=w.getnframes()/w.getframerate()
    dest.with_suffix('.json').write_text(json.dumps({'request':payload,'duration':duration,
        'generation_seconds':time.monotonic()-started},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{dest.name}: {duration:.2f}s; geração {time.monotonic()-started:.1f}s',flush=True)

def main():
    global SDK
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=['samples','full'])
    p.add_argument('--voice',default='M1',choices=['M1','M3','M4','M5'])
    p.add_argument('--speed',type=float,default=1.0)
    p.add_argument('--sdk',action='store_true',help='Usa diretamente o mesmo motor local quando a API está iniciando')
    a=p.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    if a.sdk:
        sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
        from supertonic import TTS
        model=Path(os.environ['LOCALAPPDATA'])/'OmniVoice/hf_cache/models--Supertone--supertonic-3/snapshots/724fb5abbf5502583fb520898d45929e62f02c0b'
        SDK=TTS(model_dir=model,auto_download=False,intra_op_num_threads=4,inter_op_num_threads=1)
    if a.mode=='samples':
        for voice in ['M1','M3','M4','M5']: generate(SAMPLE,voice,OUT/f'amostra_{voice}.wav',a.speed)
    else:
        source=ROOT/'producao/L01/01_NARRACAO.txt'
        paragraphs=[x.strip() for x in source.read_text(encoding='utf-8').split('\n\n') if x.strip()]
        folder=OUT/f'blocos_{a.voice}_{a.speed}'
        folder.mkdir(exist_ok=True)
        for i,text in enumerate(paragraphs,1):
            generate(text,a.voice,folder/f'{i:02}.wav',a.speed)
        dest=OUT/f'narracao_{a.voice}_bruta.wav'
        if dest.exists(): raise ValueError('Narração concatenada já existe')
        with wave.open(str(folder/'01.wav'),'rb') as first: params=first.getparams()
        timeline=[]; cursor=0
        with wave.open(str(dest),'wb') as out:
            out.setparams(params)
            for i,text in enumerate(paragraphs,1):
                with wave.open(str(folder/f'{i:02}.wav'),'rb') as w:
                    if w.getparams()[:3]!=params[:3]: raise ValueError('Formatos diferentes')
                    n=w.getnframes(); out.writeframes(w.readframes(n))
                duration=n/params.framerate
                timeline.append({'paragraph':i,'start':cursor,'end':cursor+duration,'text':text})
                cursor+=duration
                if i<len(paragraphs):
                    pause=round(params.framerate*.32)
                    out.writeframes(b'\0'*(pause*params.nchannels*params.sampwidth)); cursor+=pause/params.framerate
        (OUT/'timeline_narracao.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
        print('Completo:',dest,'duração:',cursor,flush=True)

if __name__=='__main__': main()
