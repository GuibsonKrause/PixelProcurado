import json,sys,re
sys.path.insert(0,'automacao')
from validar_revisao import ler_srt
ep=sys.argv[1]
cues=ler_srt(ep+'/exportacoes/Pixel_Procurado_DIA09_Longo_V2.srt')
ws=json.load(open(ep+'/audio/palavras_asr.json',encoding='utf-8'))
k=list(ws[0].keys()); print(k)
for tc in (21.0,126.1,210.2,294.3,399.4,250.0,258.0):
    c=[x for x in cues if x[0]<=tc<=x[1]]
    near=[w for w in ws if abs(float(w[k[1]] if 'start' not in w else w['start'])-tc)<1.2]
    print(tc, c, '| ASR:', ' '.join(f"{w.get('word',w.get('palavra'))}@{w.get('start',0):.2f}" for w in near))
