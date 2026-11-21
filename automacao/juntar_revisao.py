import json, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
V=ROOT/'producao/L01/voz'
O=V/'voicestudio'
timeline=json.loads((O/'timeline_narracao.json').read_text(encoding='utf-8'))
changes=json.loads((O/'revisao/adaptacoes.json').read_text(encoding='utf-8'))
dest=O/'narracao_M5_revisada.wav'
if dest.exists(): raise SystemExit('Revisão já concatenada.')
cursor=0
with wave.open(str(dest),'wb') as out:
    out.setparams((1,2,44100,0,'NONE','not compressed'))
    for row in timeline:
        i=row['paragraph']
        f=O/(f'revisao/{i:02}.wav' if str(i) in changes else f'blocos_M5_1.0/{i:02}.wav')
        with wave.open(str(f),'rb') as w:
            assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,44100)
            count=w.getnframes();out.writeframes(w.readframes(count))
        row['start']=cursor;cursor+=count/44100;row['end']=cursor
        row['spoken_text']=changes.get(str(i),row['text'])
        if i<len(timeline): out.writeframes(b'\0'*(14112*2));cursor+=.32
(O/'timeline_narracao_revisada.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf-8')
backup=V/'primeira_versao';backup.mkdir(exist_ok=True)
for name in ['narracao_normalizada.wav','narracao_M5.mp3','narracao_M5_transcricao.srt','validacao_audio.json','checksums.json','tempos_por_bloco.csv']:
    p=V/name
    if p.exists():
        target=backup/name
        if target.exists(): raise SystemExit(f'Backup já existe: {target}')
        p.rename(target)
print('Revisão concatenada:',cursor,flush=True)
