"""Emenda PCM, offsets e alinhamento auditável L03. Preserva brutos e evidência ASR."""
import difflib,json,re,wave,unicodedata
import audio_l03 as a
import numpy as np

def read(path):
    with wave.open(str(path)) as w:
        assert w.getframerate()==24000 and w.getnchannels()==1 and w.getsampwidth()==2
        return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').copy()

def write(path,samples):
    assert not path.exists(),path
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(samples.astype('<i2').tobytes())

def load(name):return json.loads((a.P/name).read_text(encoding='utf8'))
def norm(t):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',t.lower()))

rate=24000
# Usuário ouviu o reparo2 e aprovou explicitamente encenar; ASR permaneceu divergente.
repair=read(a.P/'gemini/reparo_v2/L03_B03_REPARO_ENCENAR_narracao.wav')
repair_words=load('B03_reparo2_asr.json')
source=read(a.P/'gemini/bruto_v1/L03_B03_P08-P12_narracao.wav')
cut_start,cut_end=38.1,47.45
prefix=source[:round(cut_start*rate)];suffix=source[round(cut_end*rate):]
n=240
prefix[-n:]=(prefix[-n:]*np.linspace(1,0,n)).astype('<i2')
repair[:n]=(repair[:n]*np.linspace(0,1,n)).astype('<i2')
repair[-n:]=(repair[-n:]*np.linspace(1,0,n)).astype('<i2')
suffix[:n]=(suffix[:n]*np.linspace(0,1,n)).astype('<i2')
corrected=np.concatenate([prefix,repair,suffix]);delta=len(repair)/rate-(cut_end-cut_start)
target=a.P/'gemini/uteis_v3';target.mkdir(exist_ok=True)
rows=[];offset=0;allwords=[];allparts=[]
for i,stem in enumerate(a.STEMS):
    pcm=corrected if i==2 else read(a.P/'gemini/uteis_v1'/f'{stem}_narracao.wav')
    path=target/f'{stem}_narracao.wav';write(path,pcm);allparts.append(pcm)
    row=dict(block=stem,file=str(path.relative_to(a.ROOT)),offset=offset,duration=len(pcm)/rate)
    rows.append(row)
    raw=load('L03_B01_diagnostico_asr.json' if i==0 else f'{stem}_diagnostico_asr.json')
    if i==0:raw=raw[:119]
    elif i==1:raw=raw[:202]
    elif i==2:
        raw=[w for w in raw if w['end']<=cut_start]+[{**w,'start':w['start']+cut_start,'end':w['end']+cut_start,'source':'reparo_v2'} for w in repair_words]+[{**w,'start':w['start']+delta,'end':w['end']+delta} for w in raw if w['start']>=cut_end]
    for w in raw:
        allwords.append({**w,'start':round(w['start']+offset,3),'end':round(w['end']+offset,3),'block':stem,'timing_source':'faster-whisper-small'})
    offset+=len(pcm)/rate
savepath=a.P/'narracao_integral_util.wav';write(savepath,np.concatenate(allparts))
a.save('offsets_blocos_finais.json',rows)
a.save('reparo_B03.json',dict(attempts=2,inserted=True,status='human_confirmed',human_approval='Ouço encenar; aprove esse trecho.',approved_file='gemini/reparo_v2/L03_B03_REPARO_ENCENAR_narracao.wav',asr_divergence='ensinar',original_cut_start=cut_start,original_cut_end=cut_end,repair_duration=len(repair)/rate,delta=delta,fade_ms=10,voice_overlap=False,original_preserved=True))
a.save('palavras_asr.json',allwords)
(a.P/'transcricao_asr_util.txt').write_text(' '.join(w['word'] for w in allwords),encoding='utf8')
paragraphs=(a.P.parent/'01_NARRACAO.txt').read_text(encoding='utf8').strip().split('\n\n')
ref=[]
for pnum,para in enumerate(paragraphs,1):
    for text in para.split():ref.append(dict(word=text,paragraph=pnum))
assert len(ref)==894
# A contração de artigo é reconhecida pelos dois modelos; não restaurar "uma".
ref[121+177]['word']='a'
# O texto encenar é confirmado pela escuta humana do reparo2, preservando ASR ensinar.
target_verb=next(w for w in ref if w['paragraph']==10 and norm(w['word'])=='encenar')
target_verb['human_confirmed']=True
# O conectivo E não foi reconhecido no início da frase por dois ASRs; não forçar.
omitted=ref.pop(34)
aligned=[];review=[]
for tag,i,j,k,l in difflib.SequenceMatcher(None,[norm(w['word']) for w in allwords],[norm(w['word']) for w in ref],autojunk=False).get_opcodes():
    if tag=='equal':
        for ai,ri in zip(range(i,j),range(k,l)):
            aligned.append({**ref[ri],**{key:allwords[ai][key] for key in ('start','end')},'status':'asr_exact','asr_word':allwords[ai]['word']})
    else:
        start=allwords[i]['start'] if i<len(allwords) else allwords[-1]['end']
        end=allwords[j-1]['end'] if j>i else start
        asr=' '.join(w['word'] for w in allwords[i:j]);script=' '.join(w['word'] for w in ref[k:l])
        status='numeric_expansion' if any(c.isdigit() for c in asr) else 'asr_ambiguity_estimated'
        review.append(dict(kind=tag,start=start,end=end,asr=asr,script=script,status=status))
        for ri in range(k,l):
            aligned.append({**ref[ri],'start':round(start+(end-start)*(ri-k)/max(1,l-k),3),'end':round(start+(end-start)*(ri-k+1)/max(1,l-k),3),'status':status,'asr_span':asr})
assert len(aligned)==893
assert all(0<=w['start']<=w['end']<=offset+.05 for w in aligned)
assert all(x['start']<=y['start'] for x,y in zip(aligned,aligned[1:]))
for w in aligned:
    if w.get('human_confirmed'):w['status']='human_confirmed';w['evidence']='Usuário: Ouço encenar; aprove esse trecho.'
for i,w in enumerate(aligned):
    if w['end']==w['start']:
        w['start']=round(max(0,w['end']-.03),3);w['timing_estimated_for_caption']=True
        if i:aligned[i-1]['end']=min(aligned[i-1]['end'],w['start'])
assert all(w['end']>w['start'] for w in aligned)
a.save('palavras_alinhadas.json',aligned);a.save('revisao_alinhamento.json',dict(omitted_connective=omitted,article_change='uma linguagem → a linguagem',divergences=review))
a.save('paragrafos_alinhados.json',[dict(paragraph=n,start=next(w['start'] for w in aligned if w['paragraph']==n),end=[w['end'] for w in aligned if w['paragraph']==n][-1],text=' '.join(w['word'] for w in aligned if w['paragraph']==n)) for n in range(1,20)])
print(json.dumps(dict(duration=offset,delta=delta,asr_words=len(allwords),aligned_words=len(aligned),divergences=len(review)),indent=2))
