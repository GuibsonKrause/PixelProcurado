import json,sys
e=json.load(open(sys.argv[1]+'/episodio.json',encoding='utf-8'))
L=e['formatos']['longo']; print({k:(v if not isinstance(v,(list,dict)) else type(v).__name__) for k,v in L.items()})
for k,v in L.items():
    if isinstance(v,list):
        for i,p in enumerate(v):
            s=json.dumps(p,ensure_ascii=False)
            if any(x in s for x in ('C0','C1','C2','"midia": "EXT"')) or k!='planos': print(k,i,s[:200])
