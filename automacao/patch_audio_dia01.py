"""Encaixa três frases corrigidas sem retranscrever a narração integral."""
import difflib
import hashlib
import json
import re
import wave
from pathlib import Path
import producao
import numpy as np

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'producao/SERIE_AQUECIMENTO_GTA6/DIA_01_2026-11-09'
A=BASE/'audio'
P=A/'patch_hud'
RATE=48000

def readwav(path):
    with wave.open(str(path),'rb') as w:
        assert w.getframerate()==RATE and w.getnchannels()==1 and w.getsampwidth()==2
        return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)

def norm(t): return re.sub(r'[^\w]','',t.lower())

def main():
    orig=readwav(A/'narracao_normalizada.wav')
    patch=readwav(P/'patch_normalizado.wav')
    ow=json.loads((A/'palavras_roteiro_alinhadas.json').read_text(encoding='utf-8'))
    pw=json.loads((P/'palavras_patch_asr.json').read_text(encoding='utf-8'))
    pt=(BASE/'05_PATCH_MINIMO.txt').read_text(encoding='utf-8').split()
    clean=(BASE/'01_NARRACAO_PUBLICACAO_2026-11-10.txt').read_text(encoding='utf-8-sig').split()
    assert len(clean)==len(ow)
    matcher=difflib.SequenceMatcher(None,[norm(x) for x in pt],[norm(x['word']) for x in pw],autojunk=False)
    mapped=[None]*len(pt)
    diverg=[]
    for kind,a,b,c,d in matcher.get_opcodes():
        if kind=='equal':
            for i,j in zip(range(a,b),range(c,d)):mapped[i]=(pw[j]['start'],pw[j]['end'])
        else:diverg.append({'kind':kind,'script':' '.join(pt[a:b]),'asr':' '.join(x['word'] for x in pw[c:d])})
    for i in range(len(mapped)):
        if mapped[i] is None:
            left=next((j for j in range(i-1,-1,-1) if mapped[j] is not None),None)
            right=next((j for j in range(i+1,len(mapped)) if mapped[j] is not None),None)
            lo=mapped[left][1] if left is not None else 0
            hi=mapped[right][0] if right is not None else len(patch)/RATE
            mapped[i]=(lo,max(lo+.03,hi))
    circles=[i for i,w in enumerate(pw) if 'círculo' in w['word'].lower() or 'circulo' in w['word'].lower()]
    assert len(circles)==3, f'Esperadas três ocorrências círculo: {circles}'
    old_i=[i for i,w in enumerate(ow) if 'quadrado' in w['word'].lower()]
    assert len(old_i)==3
    spans=[(old_i[0]-1,old_i[0]+10,0,11),(old_i[1]-12,old_i[1]+1,11,24),(old_i[2],old_i[2]+10,24,34)]
    assert [norm(x) for x in pt]==[norm(clean[k]) for a,b,_,_ in spans for k in range(a,b)], 'Texto patch diverge da cópia limpa'
    segments=[]
    cursor=0
    for a,b,c,d in spans:
        lo=max(0,ow[a]['start']-.08)
        hi=ow[b-1]['end']+.08
        pl=max(0,mapped[c][0]-.08)
        pr=min(len(patch)/RATE,mapped[d-1][1]+.08)
        segments.extend([{'kind':'old','start':cursor,'end':lo,'data':orig[round(cursor*RATE):round(lo*RATE)]},{'kind':'patch','start':pl,'end':pr,'data':patch[round(pl*RATE):round(pr*RATE)],'range':(a,b,c,d)}])
        cursor=hi
    segments.append({'kind':'old','start':cursor,'end':len(orig)/RATE,'data':orig[round(cursor*RATE):]})
    out=np.zeros(0,dtype=np.float64)
    fade=round(.02*RATE)
    for seg in segments:
        data=seg.pop('data')
        n=min(fade,len(data),len(out))
        seg['output_start']=(len(out)-n)/RATE
        if n:
            ramp=np.linspace(0,1,n)
            out[-n:]=out[-n:]*(1-ramp)+data[:n]*ramp
            out=np.concatenate([out,data[n:]])
        else:out=np.concatenate([out,data])
    finalwords=[]
    replacement={k for a,b,_,_ in spans for k in range(a,b)}
    for i,w in enumerate(ow):
        if i in replacement:continue
        seg=next(s for s in segments if s['kind']=='old' and s['start']<=w['start']<s['end'])
        delta=seg['output_start']-seg['start']
        finalwords.append({'index':i,'word':clean[i],'start':round(w['start']+delta,3),'end':round(w['end']+delta,3),'alignment':'base_asr_preserved'})
    for seg in segments:
        if seg['kind']!='patch':continue
        a,b,c,d=seg['range']
        for i,j in zip(range(a,b),range(c,d)):
            lo,hi=mapped[j]
            finalwords.append({'index':i,'word':clean[i],'start':round(seg['output_start']+lo-seg['start'],3),'end':round(seg['output_start']+hi-seg['start'],3),'alignment':'patch_asr'})
    finalwords.sort(key=lambda x:x['index'])
    assert [w['word'] for w in finalwords]==clean
    final=A/'narracao_final_hud.wav'
    assert not final.exists(), 'Não sobrescrever final existente'
    with wave.open(str(final),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE)
        w.writeframes(np.clip(np.round(out),-32768,32767).astype('<i2').tobytes())
    (A/'palavras_final_hud.json').write_text(json.dumps(finalwords,ensure_ascii=False,indent=2),encoding='utf-8')
    dest=BASE/'legendas'
    srt=[]
    for i in range(0,len(finalwords),7):
        g=finalwords[i:i+7]
        srt.append(f"{len(srt)+1}\n{producao.stamp(g[0]['start'])} --> {producao.stamp(g[-1]['end'])}\n{' '.join(w['word'] for w in g)}\n")
    (dest/'dia01_final_hud.srt').write_text('\n'.join(srt),encoding='utf-8')
    oldass=(dest/'dia01.ass').read_text(encoding='utf-8-sig')
    header=oldass.split('Dialogue:',1)[0]
    def st(t):
        cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
    events=[]
    for i in range(0,len(finalwords),7):
        g=finalwords[i:i+7]
        events.append(f"Dialogue: 0,{st(g[0]['start'])},{st(g[-1]['end'])},Default,,0,0,0,,{' '.join(w['word'] for w in g)}")
    (dest/'dia01_final_hud.ass').write_text(header+'\n'.join(events)+'\n',encoding='utf-8-sig')
    log=producao.run(['-i',final,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    loudness=json.loads(log[log.rfind('{'):log.rfind('}')+1])
    report={'duration':len(out)/RATE,'base_duration':len(orig)/RATE,'delta_seconds':(len(out)-len(orig))/RATE,'crossfade_seconds':.02,'patch_spans':segments,'script_words':len(clean),'word_sequence_exact':True,'patch_asr_divergences':diverg,'loudness':loudness,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'previous_audio_preserved':True}
    (A/'VALIDACAO_AUDIO_FINAL_HUD.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
