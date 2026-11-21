import json,sys,re
d=json.load(open(sys.argv[1]+'/audio/palavras_asr.json',encoding='utf-8'))
ws=d if isinstance(d,list) else d.get('palavras') or d.get('words') or list(d.values())[0]
print(type(d), (list(d.keys()) if isinstance(d,dict) else len(d)))
def g(w,k): 
    for kk in k:
        if kk in w: return w[kk]
for i,w in enumerate(ws):
    t=str(g(w,['word','palavra','texto','w']))
    if re.search(r'(?i)star|drake|dre|mobili|car[ae]ca|joh|jouh', t): print(g(w,['start','inicio','s']), ' '.join(str(g(x,['word','palavra','texto','w'])) for x in ws[max(0,i-3):i+4]))
