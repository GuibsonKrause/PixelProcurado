"""Alinha a locução L04 ao roteiro e conserva divergências ASR para auditoria."""
import difflib,json,re,wave,unicodedata
from pathlib import Path
import audio_l04 as a
def norm(t):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',t.lower()))
raw=json.loads((a.P/'palavras_asr.json').read_text(encoding='utf8'))
paragraphs=(a.P.parent/'01_NARRACAO.txt').read_text(encoding='utf8').strip().split('\n\n')
ref=[dict(word=t,paragraph=i+1) for i,p in enumerate(paragraphs) for t in p.split()]
aligned=[];review=[]
for tag,i,j,k,l in difflib.SequenceMatcher(None,[norm(w['word']) for w in raw],[norm(w['word']) for w in ref],autojunk=False).get_opcodes():
 if tag=='equal':
  for ai,ri in zip(range(i,j),range(k,l)):aligned.append({**ref[ri],**{key:raw[ai][key] for key in ('start','end')},'status':'asr_exact','asr_word':raw[ai]['word']})
 else:
  start=raw[i]['start'] if i<len(raw) else raw[-1]['end'];end=raw[j-1]['end'] if j>i else start
  if end<=start:end=min(raw[-1]['end'],start+.05)
  recognized=' '.join(w['word'] for w in raw[i:j]);script=' '.join(w['word'] for w in ref[k:l])
  review.append(dict(kind=tag,start=start,end=end,asr=recognized,script=script))
  for ri in range(k,l):aligned.append({**ref[ri],'start':round(start+(end-start)*(ri-k)/max(1,l-k),3),'end':round(start+(end-start)*(ri-k+1)/max(1,l-k),3),'status':'asr_ambiguity_estimated','asr_span':recognized})
for i,w in enumerate(aligned):
 if w['end']<=w['start']:
  w['start']=max(0,w['end']-.03)
  if i:aligned[i-1]['end']=min(aligned[i-1]['end'],w['start'])
assert len(aligned)==len(ref)
a.save('palavras_alinhadas.json',aligned);a.save('revisao_alinhamento.json',review)
a.save('paragrafos_alinhados.json',[dict(paragraph=n,start=next(w['start'] for w in aligned if w['paragraph']==n),end=[w['end'] for w in aligned if w['paragraph']==n][-1],text=p) for n,p in enumerate(paragraphs,1)])
print(json.dumps(review,ensure_ascii=False,indent=2))
