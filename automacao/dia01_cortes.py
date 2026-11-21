"""Cortes sociais com falas existentes, sem nova geração de voz."""
import argparse
import json
from pathlib import Path
import re
import dia01_produzir as edit

def plan():
    data=json.loads((edit.W/'timeline_dia01.json').read_text(encoding='utf8'))
    words=json.loads(Path(data['words']).read_text(encoding='utf8'))
    paras=re.split(r'\n\s*\n',(edit.P/'01_NARRACAO_PUBLICACAO_2026-11-10.txt').read_text(encoding='utf8').strip())
    first=sum(len(p.split()) for p in paras[:3])
    count=len((paras[3].split('.')[0]+'.').split())
    hook=[data['shots'][3]['start_frame']/30, words[first+count-1]['end']]
    def bounds(a,b):return [data['shots'][a]['start_frame']/30,data['shots'][b]['end_frame']/30]
    result={
      'reel':{'name':'DIA01_Reel_HUD','slices':[hook,bounds(25,28)],
        'title':'GTA 6: círculo ou triângulo? Leia o HUD antes de fugir',
        'description':'Duas opções reais na porta do carro: Smash Window e Slim Jim. Análise das imagens oficiais, sem teste jogável próprio. Episódio completo no canal Pixel Procurado. #GTA6 #GTAVI #PixelProcurado'},
      'story':{'name':'DIA01_Story_HUD','slices':[hook,bounds(28,28)],
        'title':'Qual botão você escolheria?',
        'description':'O detalhe está no HUD. Veja a análise completa no Pixel Procurado.'},
    }
    for item in result.values():
        item['slices']=[[round(a*30)/30,round(b*30)/30] for a,b in item['slices']]
        item['duration']=sum(b-a for a,b in item['slices'])
        item['status']='preparado_aguardando_render_e_QA'
        item['thumbnail']=str(edit.P/'social/capa_vertical_hud.png')
        item['intentional_reprise']='HUD no gancho e na explicação; sem loop de ação'
        assert 3<item['duration']<90
    edit.save(edit.P/'social/CORTES_SOCIAIS.json',result)
    return result

def render(kind,item):
    data=json.loads((edit.W/'timeline_dia01.json').read_text(encoding='utf8'))
    stem=item['name']; clips=[]; durations=[]
    for i,(a,b) in enumerate(item['slices']):
        part=f'{stem}_parte{i:02}'
        edit.render(a,b,True,part)
        clips.append(edit.EXP/f'{part}.mp4'); durations.append(round((b-a)*30)/30)
    concat=edit.W/f'{stem}.ffconcat'
    concat.write_text('ffconcat version 1.0\n'+''.join(f"file '{p.as_posix()}'\nduration {d:.9f}\n" for p,d in zip(clips,durations)),encoding='utf8')
    labels=''.join(f'[a{i}]' for i in range(len(clips)))
    filters=[f'[1:a]asplit={len(clips)}{labels}']
    for i,(a,b) in enumerate(item['slices']):filters.append(f'[a{i}]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[v{i}]')
    filters.append(''.join(f'[v{i}]' for i in range(len(clips)))+f'concat=n={len(clips)}:v=0:a=1[voice]')
    edit.run(['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','concat','-safe',0,'-i',concat,'-i',data['voice'],'-filter_complex',';'.join(filters),'-map','0:v:0','-map','[voice]','-c:v','copy','-c:a','aac','-b:a','128k','-ar',48000,'-t',sum(durations),'-movflags','+faststart',edit.EXP/f'{stem}.mp4'],edit.W/f'{stem}_mux.log')
    captions=[];elapsed=0
    words=json.loads(Path(data['words']).read_text(encoding='utf8'))
    for (a,b),duration in zip(item['slices'],durations):
        group=[]
        for word in words:
            if word['end']<=a or word['start']>=b:continue
            group.append(word)
            if len(group)>=7 or word['word'].endswith(('.', '?', '!', ';', ':')):
                captions.append((max(0,group[0]['start']-a)+elapsed,min(duration,group[-1]['end']-a)+elapsed,' '.join(w['word'] for w in group)));group=[]
        if group:captions.append((max(0,group[0]['start']-a)+elapsed,min(duration,group[-1]['end']-a)+elapsed,' '.join(w['word'] for w in group)))
        elapsed+=duration
    (edit.EXP/f'{stem}.srt').write_text('\n\n'.join(f'{i+1}\n{edit.stamp(a,True)} --> {edit.stamp(b,True)}\n{text}' for i,(a,b,text) in enumerate(captions)),encoding='utf8')
    print(edit.EXP/f'{stem}.mp4',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--render',choices=['reel','story'])
    args=parser.parse_args();items=plan()
    if args.render:render(args.render,items[args.render])
    else:print(json.dumps(items,ensure_ascii=False,indent=2))
