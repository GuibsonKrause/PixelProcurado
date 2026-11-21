"""DIA01: timeline por parágrafos alinhados, cards V2 e composição FFmpeg."""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import wave

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'producao/SERIE_AQUECIMENTO_GTA6/DIA_01_2026-11-09'
W = P / 'montagem'
EXP = P / 'exportacoes'
SOURCE = ROOT / 'videosGTAVI/GTAVI_An_Extended_Look.mp4'
FPS = 30
# Cada janela é pertinente ao parágrafo, sem loop. HUD tem pausa para leitura.
WINDOWS = [
 [(262,269)], [(18,38)], [(1561,1568),(1599,1605)], [(363.6,369),(264,270)],
 [(28,54)], [(276,284)], [(52,80)], [(116,127)], [(135,158)],
 [(75,87)], [(230,240)], [(180,215)], [(252,264)], [(267,271)],
 [(255,277)], [(280,297)], [(296,304)], [(279,310)], [(310,329)],
 [(330,350)], [(1494,1502)], [(1435,1444),(1495,1510),(1524,1538)],
 [(1510,1519)], [(430,439.6)], [(347,357),(364.9,366.5)],
 [(364.9,366.5)], [(365.2,369)], [(364.9,366.5)], [(364.9,366.5)],
 [(1579,1593)], [(1549,1582)],
]
CARDS = {
 0: ('SEM BOLSO MÁGICO','Análise do gameplay oficial'),
 1: ('19 DE NOVEMBRO','Lançamento · Rockstar Games'),
 2: ('212 GB','Pré-load · 10 de novembro'),
 3: ('QUAL BOTÃO?','Fonte: aproximadamente 6 min'),
 6: ('LEIA O AMBIENTE','Interação com moradores'),
 7: ('ATÉ O CACHORRO','Interações mostradas no gameplay'),
 11: ('O MALOTE','Observe o equipamento levado'),
 14: ('ARMA NO CHÃO','Moreland 850 · recolher arma'),
 17: ('CORREDOR FECHADO','Fumaça, cobertura e ângulos'),
 19: ('CLARO → ESCURO','Análise da sequência exibida'),
 21: ('OUTRA ABORDAGEM','Prédio comercial · gameplay oficial'),
 25: ('CÍRCULO / TRIÂNGULO','Smash Window / Slim Jim'),
 26: ('CÍRCULO','Smash Window · consequência: análise editorial'),
 27: ('TRIÂNGULO','Slim Jim · consequência: análise editorial'),
 28: ('OBSERVE AS OPÇÕES','Leitura do HUD · sem teste jogável próprio'),
 29: ('PRÉ-LOAD DISPONÍVEL','Consulte as orientações da sua plataforma'),
 30: ('PIXEL PROCURADO','Próximo vídeo: o tamanho de Leonida'),
}

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')

def run(args, log):
    with log.open('w', encoding='utf8') as handle:
        result = subprocess.run(list(map(str,args)), cwd=ROOT, stdout=handle, stderr=handle)
    if result.returncode:
        raise RuntimeError(log.read_text(encoding='utf8', errors='replace')[-3500:])

def stamp(t, srt=False):
    n = round(max(0,t) * (1000 if srt else 100))
    q = 1000 if srt else 100
    return f'{n//(3600*q):02}:{n//(60*q)%60:02}:{n//q%60:02}' + (f',{n%q:03}' if srt else f'.{n%q:02}')

def prepare(voice, words_path):
    words = json.loads(words_path.read_text(encoding='utf8'))
    paras = re.split(r'\n\s*\n', (P/'01_NARRACAO_PUBLICACAO_2026-11-10.txt').read_text(encoding='utf8').strip())
    assert len(paras) == len(WINDOWS) == 31
    assert sum(len(p.split()) for p in paras) == len(words), 'Alinhamento não cobre as palavras do roteiro'
    with wave.open(str(voice)) as wav:
        duration = wav.getnframes()/wav.getframerate()
    cursor = 0
    starts = []
    for para in paras:
        starts.append(round(words[cursor]['start']*FPS))
        cursor += len(para.split())
    starts[0] = 0
    starts.append(math.ceil(duration*FPS))
    shots = []
    for i, para in enumerate(paras):
        a,b = starts[i:i+2]
        remaining = b-a
        source_parts = []
        for x,y in WINDOWS[i]:
            n = min(remaining, round((y-x)*FPS))
            if n > 0:
                source_parts.append({'source_start':x, 'frames':n, 'freeze':False})
                remaining -= n
        if remaining:
            # Pausa explícita de análise; não repetir automaticamente a ação.
            last = source_parts[-1]
            source_parts.append({'source_start':min(WINDOWS[i][-1][1]-.1,last['source_start']+last['frames']/FPS-.1), 'frames':remaining, 'freeze':True})
        if i==3:
            # Sustentar HUD ate a frase de leitura terminar.
            remaining=b-a
            source_parts=[]
            for point,n,freeze in [(364.9,180,True),(264,300,False)]:
                frames=min(remaining,n)
                if frames>0:
                    source_parts.append({'source_start':point,'frames':frames,'freeze':freeze})
                    remaining-=frames
            if remaining:source_parts.append({'source_start':273.9,'frames':remaining,'freeze':True})
        elif i in (25,27,28):
            for part in source_parts:
                part.update(source_start=364.9, freeze=True)
        shots.append({'paragraph':i,'start_frame':a,'end_frame':b,'anchor':para[:100],
          'parts':source_parts,'card':CARDS.get(i),
          'reprise':'gancho/payoff do mesmo HUD' if i in (3,24,25,26,27,28) else None})
    save(W/'timeline_dia01.json',{'fps':FPS,'duration':duration,'voice':str(voice),'words':str(words_path),'shots':shots})
    # Reutiliza a composição Hyperframes V2 aprovada; não executa seu renderer antigo.
    original = ROOT/'producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06/produzir_especial.py'
    spec = importlib.util.spec_from_file_location('dia01_cards_v2',original)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HF = W/'hyperframes_dia01'
    module.DIRECTION = [(CARDS.get(i,('',''))[0],CARDS.get(i,('',''))[1],'',0) for i in range(31)]
    module.SCALE = 2
    module.panel_art = lambda _: '<path d="M20 20h114v112H20zM40 55h74M40 77h52M40 99h65"/>'
    module.prepare()
    shutil.copy2(original.parent/'montagem/hyperframes_v2_4k/gsap.min.js',module.HF/'gsap.min.js')
    print(f'Timeline específica: {W / "timeline_dia01.json"}',flush=True)

def subtitles(words_path, begin, end, vertical, stem):
    words = json.loads(words_path.read_text(encoding='utf8'))
    groups=[]; group=[]
    for word in words:
        if word['end']<=begin or word['start']>=end: continue
        group.append(word)
        if len(group)>=7 or word['word'].endswith(('.', '?', '!', ';', ':')):
            groups.append(group); group=[]
    if group: groups.append(group)
    header = f'''[Script Info]\nScriptType: v4.00+\nPlayResX: {1080 if vertical else 3840}\nPlayResY: {1920 if vertical else 2160}\nWrapStyle: 0\nScaledBorderAndShadow: yes\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Main,Arial,{58 if vertical else 86},&H00FFFFFF,&H00FFFFFF,&H00100A08,&H80000000,-1,0,0,0,100,100,0,0,1,{4 if vertical else 7},0,2,{75 if vertical else 260},{75 if vertical else 260},{330 if vertical else 160},1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
    source_style=f'Style: Source,Arial,{27 if vertical else 34},&H00FFFFFF,&H00FFFFFF,&H00100A08,&H80000000,-1,0,0,0,100,100,0,0,1,2,0,7,{60 if vertical else 110},110,{1390 if vertical else 70},1\n'
    header=header.replace('[Events]',source_style+'[Events]')
    events=[f'Dialogue: 1,{stamp(0)},{stamp(end-begin)},Source,,0,0,0,,Rockstar Games | GTA VI | Análise do gameplay']; srt=[]
    for i,g in enumerate(groups,1):
        a=max(0,g[0]['start']-begin); b=min(end-begin,g[-1]['end']-begin)
        text=' '.join(w['word'] for w in g)
        assert b>a
        events.append(f'Dialogue: 0,{stamp(a)},{stamp(b)},Main,,0,0,0,,{text}')
        srt.append(f'{i}\n{stamp(a,True)} --> {stamp(b,True)}\n{text}\n')
    ass=W/f'{stem}.ass'; ass.write_text(header+'\n'.join(events),encoding='utf-8-sig')
    (EXP/f'{stem}.srt').write_text('\n'.join(srt),encoding='utf8')
    return ass

def render(begin,end,vertical,stem):
    data=json.loads((W/'timeline_dia01.json').read_text(encoding='utf8'))
    assert (W/'paineis_dia01.mov').is_file(), 'Renderize primeiro a composição Hyperframes em paineis_dia01.mov'
    end=min(end if end is not None else data['duration'],data['duration'])
    first=round(begin*FPS); stop=math.ceil(end*FPS)
    assert stop>first>=0
    ass=subtitles(Path(data['words']),begin,end,vertical,stem)
    assrel=ass.relative_to(ROOT).as_posix()
    target=W/stem; target.mkdir(exist_ok=True)
    clips=[]; ledger=[]
    for shot in data['shots']:
        sa=max(first,shot['start_frame']); sb=min(stop,shot['end_frame'])
        if sb<=sa:continue
        inputs=[]; filters=[]; pts=shot['start_frame']; count=sb-sa
        parts=[]
        for part in shot['parts']:
            a=max(sa,pts);b=min(sb,pts+part['frames'])
            if b>a:
                parts.append({**part,'frames':b-a,'source_start':part['source_start']+(0 if part['freeze'] else (a-pts)/FPS)})
            pts+=part['frames']
        for j,part in enumerate(parts):
            inputs+=['-ss',part['source_start'],'-i',SOURCE]
            vf='fps=30,scale=3840:2160,setsar=1,setpts=PTS-STARTPTS'
            if part['freeze']:
                n=part['frames']
                vf=f"trim=end_frame=1,setpts=PTS-STARTPTS,zoompan=z='1+0.025*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s=3840x2160:fps=30,setsar=1"
            filters.append(f'[{j}:v]{vf},trim=end_frame={part["frames"]}[p{j}]')
        filters.append(''.join(f'[p{j}]' for j in range(len(parts)))+f'concat=n={len(parts)}:v=1:a=0[base]')
        if vertical:
            filters+=['[base]split[fg][bg]','[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=12:1,scale=1080:1920,eq=brightness=-0.35[back]', '[fg]scale=1080:608[front]','[back][front]overlay=0:470[canvas]']
        else:filters.append('[base]null[canvas]')
        output='canvas'; extras=0
        if shot['card'] and sa==shot['start_frame']:
            visible=min(count/FPS-.1,max(2.5,.85+len(' '.join(shot['card']).split())/3.4))
            if visible>1:
                j=len(parts)
                inputs+=['-ss',shot['paragraph']*.8,'-t',.8,'-i',W/'paineis_dia01.mov']
                extras+=1
                hold=max(0,visible-.8)
                filters.append(fr'[{j}:v]fps=60,format=rgba,scale={780 if vertical else 1440}:-2,setpts=PTS-STARTPTS+gte(N\,24)*{hold}/TB,fps=30[card]')
                filters.append(fr'[canvas][card]overlay={150 if vertical else 116}:{1120 if vertical else 1460}:eof_action=pass:enable=lt(t\,{visible})[carded]')
                output='carded'
        if (vertical and shot['paragraph'] in (3,25,26,27,28)) or (not vertical and shot['paragraph']==3):
            inputs+=['-loop','1','-i',P/'evidencia_hud_botoes.png']
            filters.append(f'[{len(parts)+extras}:v]scale={940 if vertical else 1440}:-2,format=rgba[hud]')
            position='70:70' if vertical else r'2120:800:enable=lt(t\,6)'
            filters.append(f'[{output}][hud]overlay={position}[hudcanvas]')
            output='hudcanvas'
        offset=(sa-first)/FPS
        filters.append(f'[{output}]setpts=PTS+{offset}/TB,ass=filename={assrel},setpts=PTS-STARTPTS,format=nv12[out]')
        signature=hashlib.sha256(json.dumps([shot,sa,sb,vertical,ass.read_text(encoding='utf-8-sig')]).encode()).hexdigest()[:12]
        clip=target/f'{shot["paragraph"]:02}_{signature}.mp4'
        if not clip.exists():
            quality=['-b:v','18M','-maxrate','20M','-bufsize','40M'] if vertical else ['-global_quality','18']
            run(['ffmpeg','-hide_banner','-loglevel','warning','-y',*inputs,'-filter_complex_threads','2','-filter_complex',';'.join(filters),'-map','[out]','-frames:v',count,'-an','-c:v','h264_qsv','-preset','slow',*quality,'-g',60,'-r',30,clip],clip.with_suffix('.log'))
        clips.append((clip,count));ledger.append({'paragraph':shot['paragraph'],'output_start':offset,'frames':count,'parts':parts,'intentional_reprise':shot['reprise']})
        print(f'{stem}: parágrafo{shot["paragraph"]:02} pronto',flush=True)
    assert sum(n for _,n in clips)==stop-first
    concat=target/'concat.ffconcat'
    concat.write_text('ffconcat version 1.0\n'+''.join(f"file '{p.as_posix()}'\nduration {n/FPS:.9f}\n" for p,n in clips),encoding='utf8')
    out=EXP/f'{stem}.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','concat','-safe',0,'-i',concat,'-ss',begin,'-i',data['voice'],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k' if vertical else '320k','-ar',48000,'-t',(stop-first)/FPS,'-movflags','+faststart',out],target/'mux.log')
    save(target/'ledger.json',{'file':str(out),'frames':stop-first,'fps':FPS,'shots':ledger,'qa_status':'aguarda revisão técnica e independente'})
    print(out,flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['prepare','render'])
    parser.add_argument('--voice',type=Path,default=P/'audio/narracao_normalizada.wav')
    parser.add_argument('--words',type=Path,default=P/'audio/palavras_roteiro_alinhadas.json')
    parser.add_argument('--from',dest='begin',type=float,default=0)
    parser.add_argument('--to',type=float)
    parser.add_argument('--vertical',action='store_true')
    parser.add_argument('--name',default='DIA01_Master_4K')
    args=parser.parse_args()
    W.mkdir(parents=True,exist_ok=True);EXP.mkdir(exist_ok=True)
    if args.mode=='prepare':prepare(args.voice.resolve(),args.words.resolve())
    else:render(args.begin,args.to,args.vertical,args.name)

if __name__=='__main__':main()
