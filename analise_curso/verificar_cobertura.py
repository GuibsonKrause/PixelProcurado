"""Audit transcript coverage without treating silence as missed speech."""
from pathlib import Path
import json

folder=Path(__file__).resolve().parent
manifest=json.loads((folder/'inventario.json').read_text(encoding='utf-8'))
report=[]
for source in manifest:
    file=folder/(Path(source['file']).stem+'.json')
    if not file.exists():
        report.append({'source':source['file'],'status':'missing'});continue
    data=json.loads(file.read_text(encoding='utf-8'));segs=data['segments']
    gaps=[];previous=0
    for s in segs:
        if s['start']-previous>10: gaps.append([round(previous,2),round(s['start'],2)])
        previous=s['end']
    report.append({'source':source['file'],'status':'transcribed','model':data['model'],
                   'duration':round(source['seconds'],2),'segments':len(segs),
                   'first_start':segs[0]['start'] if segs else None,
                   'last_end':segs[-1]['end'] if segs else None,
                   'tail_seconds':round(source['seconds']-previous,2),
                   'vad_duration':round(data['duration_after_vad'],2),
                   'gaps_over_10s':gaps,
                   'low_confidence':[{'start':s['start'],'end':s['end'],'text':s['text']}
                      for s in segs if s['avg_logprob'] < -0.8],
                   'suspicious_density':[{'start':s['start'],'end':s['end'],'text':s['text']}
                      for s in segs if (s['end']-s['start']>15 and len(s['text'].split())<15)
                      or (len(s['text'].split())>30 and len(set(s['text'].lower().split()))/len(s['text'].split())<0.3)]})
(folder/'auditoria_transcricoes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
