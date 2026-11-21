import json,sys
ep=sys.argv[1]
a=json.load(open(ep+'/audio/ancoras_paragrafos.json',encoding='utf-8'))
for p in a: print(p['paragrafo'], p['start'], f"{int(p['start']//60)}:{int(p['start']%60):02d}", p['texto'][:50])
tags=json.load(open(ep+'/publicacao/publicacao_secao.json',encoding='utf-8'))['tags_youtube']
print(len(tags), sum(len(t)+(2 if ' ' in t else 0)+1 for t in tags))
t=open(ep+'/publicacao/04_TAGS.txt',encoding='utf-8').read().strip().split(', ')
print(t==tags)
