"""Validação local da voz Dia01 e legendas preservando palavras do roteiro."""
import difflib
import json
import re
import wave
from pathlib import Path
import producao

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'producao/SERIE_AQUECIMENTO_GTA6/DIA_01_2026-11-09'
AUDIO = BASE / 'audio'

def token(s):
    return re.sub(r'[^\w]', '', s.lower())

def main():
    wav = AUDIO / 'narracao_normalizada.wav'
    words = json.loads((AUDIO / 'palavras_asr.json').read_text(encoding='utf-8'))
    clean = (BASE / '01_NARRACAO_PUBLICACAO_2026-11-10.txt').read_text(encoding='utf-8-sig')
    original = clean.split()
    match = difflib.SequenceMatcher(None, [token(x) for x in original], [token(x['word']) for x in words], autojunk=False)
    mapped = [None] * len(original)
    divergences = []
    for kind,a,b,c,d in match.get_opcodes():
        if kind == 'equal':
            for i,j in zip(range(a,b),range(c,d)):
                mapped[i] = (words[j]['start'], words[j]['end'])
        else:
            divergences.append({'kind':kind,'script':' '.join(original[a:b]),'asr':' '.join(x['word'] for x in words[c:d]),'start':words[min(c,len(words)-1)]['start']})
    with wave.open(str(wav),'rb') as w:
        info={'duration':w.getnframes()/w.getframerate(),'sample_rate':w.getframerate(),'channels':w.getnchannels(),'sample_width':w.getsampwidth()}
    # Interpolate only unmatched script words between neighbouring ASR anchors.
    i=0
    while i<len(mapped):
        if mapped[i] is not None:
            i+=1
            continue
        j=i
        while j<len(mapped) and mapped[j] is None:
            j+=1
        start=mapped[i-1][1] if i else 0
        end=mapped[j][0] if j<len(mapped) else info['duration']
        end=max(start+0.02*(j-i),end)
        for k in range(i,j):
            mapped[k]=(start+(end-start)*(k-i)/(j-i),start+(end-start)*(k-i+1)/(j-i))
        i=j
    aligned=[{'word':t,'start':round(s,3),'end':round(e,3)} for t,(s,e) in zip(original,mapped)]
    (AUDIO/'palavras_roteiro_alinhadas.json').write_text(json.dumps(aligned,ensure_ascii=False,indent=2),encoding='utf-8')
    subtitles=BASE/'legendas'
    subtitles.mkdir(exist_ok=True)
    lines=[]
    ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1920','PlayResY: 1080','WrapStyle: 0','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Default,Arial,54,&H00FFFFFF,&H000000FF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,100,100,80,1','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    def ass_stamp(t):
        cs=round(t*100)
        return f'{cs//360000:01}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
    for i in range(0,len(aligned),7):
        group=aligned[i:i+7]
        lines.append(f"{len(lines)+1}\n{producao.stamp(group[0]['start'])} --> {producao.stamp(group[-1]['end'])}\n{' '.join(w['word'] for w in group)}\n")
        caption=' '.join(w['word'] for w in group).replace('{','').replace('}','')
        ass.append(f"Dialogue: 0,{ass_stamp(group[0]['start'])},{ass_stamp(group[-1]['end'])},Default,,0,0,0,,{caption}")
    (subtitles/'dia01.srt').write_text('\n'.join(lines),encoding='utf-8')
    (subtitles/'dia01.ass').write_text('\n'.join(ass)+'\n',encoding='utf-8-sig')
    stats=producao.run(['-i',wav,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    loudness=json.loads(stats[stats.rfind('{'):stats.rfind('}')+1])
    silences=producao.run(['-i',wav,'-af','silencedetect=noise=-40dB:d=0.8','-f','null','-'])
    (AUDIO/'silencios.log').write_text(silences,encoding='utf-8')
    report={'wav':info,'loudness':loudness,'script_words':len(original),'asr_words':len(words),'asr_first':words[:8],'asr_last':words[-8:],'matching_ratio':match.ratio(),'divergences':divergences,'subtitle_alignment':'ASR anchors; unmatched script words interpolated and flagged in divergences','hook_first_five_words_end':aligned[4]['end']}
    (AUDIO/'VALIDACAO_AUDIO.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('divergences','asr_first','asr_last')},ensure_ascii=False,indent=2))
    print('ASR divergence count:',len(divergences))

if __name__=='__main__':
    main()
