"""Prepare, render and verify the requested vertical Shorts using existing local tools."""
import argparse, difflib, hashlib, json, math, re, shutil, subprocess, sys, wave
from pathlib import Path
import producao
from shorts_editorial import ROOT, PLANS, META
sys.path[:0] = [str(ROOT/'.production-tools/python'), str(ROOT/'.course-tools')]
import av, imageio_ffmpeg, numpy as np
from PIL import Image, ImageDraw, ImageFont
import unicodedata

FF=imageio_ffmpeg.get_ffmpeg_exe()
BASE=ROOT/'producao/shorts'
FPS=30
def norm(t):
    t=''.join(c for c in unicodedata.normalize('NFD',t.lower()) if unicodedata.category(c)!='Mn')
    return re.sub('[^a-z0-9]','',t)
def write_json(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def run(args,log):
    log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('w',encoding='utf8') as f:
        r=subprocess.run([FF,'-hide_banner','-nostdin','-y',*map(str,args)],cwd=ROOT,stdout=f,stderr=f)
    if r.returncode: raise RuntimeError(log.read_text(encoding='utf8',errors='replace')[-3500:])
def stamp(t,ass=False):
    if ass:
        cs=round(max(0,t)*100); return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
    ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def prepare(rid):
    folder=BASE/rid
    raw=json.loads((folder/'voz/palavras_asr.json').read_text(encoding='utf8'))
    script=(folder/'voz/NARRACAO.txt').read_text(encoding='utf8').split()
    a,b=[norm(w) for w in script],[norm(w['word']) for w in raw]
    timings={}; captions_words=[]; review=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag=='equal':
            for z in range(i,j):
                w=dict(raw[k+z-i],word=script[z]); timings[z]=w['start'];captions_words.append(w)
        else:
            start=raw[k]['start'] if k<len(raw) else raw[-1]['end']
            end=raw[l-1]['end'] if l>k else start
            review.append(dict(op=tag,start=start,end=end,script=' '.join(script[i:j]),asr=' '.join(w['word'] for w in raw[k:l]),decision='short orthographic/contextual correction' if tag=='replace' else 'ASR-only words retained; unrecognized script words not forced into subtitles'))
            if tag=='replace' and max(j-i,l-k)<=12:
                for z in range(i,j):
                    s=start+(end-start)*(z-i)/max(1,j-i);e=start+(end-start)*(z-i+1)/max(1,j-i)
                    timings[z]=s;captions_words.append(dict(word=script[z],start=s,end=e))
            else:
                captions_words.extend(raw[k:l])
                for z in range(i,j):timings[z]=start
    with wave.open(str(folder/'voz/narracao.wav'),'rb') as w: duration=w.getnframes()/w.getframerate()
    captions=[]; group=[]
    for i,w in enumerate(captions_words):
        group.append(w)
        chars=len(' '.join(x['word'] for x in group))
        end_sentence=bool(re.search(r'[.!?;:]$',w['word']))
        next_gap=captions_words[i+1]['start']-w['end'] if i+1<len(captions_words) else 99
        if len(group)>=7 or chars>=40 or (len(group)>=3 and end_sentence) or next_gap>.35 or i+1==len(captions_words):
            start=group[0]['start']; end=min(duration,max(w['end']+.07,start+.85))
            if i+1<len(captions_words):end=min(end,captions_words[i+1]['start'])
            if end<=start:end=min(duration,start+.12)
            captions.append(dict(start=round(start,3),end=round(end,3),text=' '.join(x['word'] for x in group)))
            group=[]
    for i,c in enumerate(captions[:-1]):c['end']=min(c['end'],captions[i+1]['start'])
    shots=[];anchors=[]
    for idx,spec in enumerate(PLANS[rid]):
        s=dict(spec);phrase=s['anchor']
        if phrase is None:frame=0
        else:
            needle=[norm(x) for x in phrase.split()]
            hits=[i for i in range(len(a)-len(needle)+1) if a[i:i+len(needle)]==needle]
            if len(hits)>1 and idx==len(PLANS[rid])-1:
                selected=hits[-1];reason='terminal occurrence selected explicitly for loop'
            else:
                assert len(hits)==1,(rid,phrase,hits)
                selected=hits[0];reason='unique phrase'
            frame=round(timings[selected]*FPS)
            anchors.append(dict(phrase=phrase,script_index=selected,time=frame/FPS,reason=reason))
        s['from']=frame;shots.append(s)
    assert all(a['from']<b['from'] for a,b in zip(shots,shots[1:])),rid
    total=math.ceil(duration*FPS)
    # Subdivide only long holds; the same evidence stays on screen during analysis.
    expanded=[]
    for i,s in enumerate(shots):
        end=shots[i+1]['from'] if i+1<len(shots) else total
        count=end-s['from'];n=max(1,math.ceil(count/(6.8*FPS)))
        for part in range(n):
            t=dict(s);t['from']=s['from']+round(count*part/n);t['frames']=round(count*(part+1)/n)-round(count*part/n)
            if part:t['anchor']=f"{s['anchor']} [continuação {part+1}]";t['hook']=False
            if t['file'].endswith('.mp4'):
                elapsed=(t['from']-s['from'])/FPS
                t['offset']=s['offset']+min(elapsed,max(0,s.get('motion',999)-1/FPS))
                if 'motion' in s:t['motion']=max(1/FPS,s['motion']-elapsed)
            t['part']=part;expanded.append(t)
    # One deliberate early visual change; voice remains intact.
    first=expanded[0]
    if first['frames']>90 and first['file']:
        rest=dict(first,**{'from':42,'frames':first['frames']-42,'punch':True,'anchor':'GANCHO • SEGUNDA BATIDA'})
        first['frames']=42;expanded.insert(1,rest)
    for i,s in enumerate(expanded):
        s['index']=i;s['start']=s['from']/FPS;s['end']=(s['from']+s['frames'])/FPS
        s['animationFrames']=min(s['frames'],36 if s['mode']=='graphic' else 18)
        assert s['frames']>0
        if s['file']:
            source=ROOT/s['file'];assert source.is_file(),source
            if source.suffix.lower()=='.mp4':
                with av.open(str(source)) as c:
                    assert s['offset']+min(s['frames']/FPS,s.get('motion',999))<=c.duration/1e6+.01,(rid,s)
    assert sum(s['frames'] for s in expanded)==total
    for c in captions:assert 0<=c['start']<c['end']<=duration
    write_json(folder/'projeto/timeline.json',dict(id=rid,title=META[rid][0],fps=FPS,width=1080,height=1920,duration=duration,frames=total,voice=(folder/'voz/narracao.wav').relative_to(ROOT).as_posix(),shots=expanded,captions=captions))
    write_json(folder/'projeto/revisao_alinhamento.json',dict(corrections=review,anchors=anchors,method='Whisper small word timestamps; contextual spelling corrections; unmatched script words not forced'))
    write_json(folder/'voz/palavras_revisadas.json',captions_words)
    timeline=['# Direção sincronizada','',f'Narração integral: {duration:.2f}s. 1080×1920 / 30 fps.','', '| Início | Fim | Fala âncora | Imagem / vídeo | Entrada fonte | Tratamento | Texto |','|---|---|---|---|---|---|---|']
    for s in expanded:timeline.append(f"| {s['start']:.2f} | {s['end']:.2f} | {s['anchor'] or 'Início'} | {s['file'] or 'Gráfico original Remotion'} | {s['offset']:.2f}s | {s['mode']} | {s['title'].replace(chr(10),' / ')} |")
    (folder/'projeto/DIRECAO.md').write_text('\n'.join(timeline)+'\n',encoding='utf8')
    (folder/'exportacoes'/f'{rid}_legendas.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(captions))+'\n',encoding='utf8')
    print(f'PREPARED {rid}: {len(expanded)} shots, {len(captions)} captions, {len(review)} ASR differences',flush=True)

ASS='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial,57,&H00FFFFFF,&H00FFFFFF,&H30100C08,&H30100C08,-1,0,0,0,100,100,0,0,3,10,0,2,88,160,405,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def caption_text(t):
    words=t.split();lines=[];line=[]
    for w in words:
        if len(' '.join(line+[w]))>29 and line:lines.append(' '.join(line));line=[]
        line.append(w)
    if line:lines.append(' '.join(line))
    if len(lines)>2:
        split=len(words)//2;lines=[' '.join(words[:split]),' '.join(words[split:])]
    t=r'\N'.join(lines)
    return re.sub(r'\b(Jason|Lucia|risco|confiança|iguana|controle|mapa|oficial|Raul|Brian|playlist|gameplay)\b',r'{\\c&H003DD3FF&}\1{\\c&H00FFFFFF&}',t,flags=re.I)

def render(rid,only=None):
    folder=BASE/rid;data=json.loads((folder/'projeto/timeline.json').read_text(encoding='utf8'));work=folder/'projeto/render';work.mkdir(exist_ok=True)
    for s in data['shots']:
        i=s['index']
        if only is not None and i not in only:continue
        overlay=folder/f'projeto/overlays/{i:03}'
        done=overlay/'complete.json';assert done.exists(),f'Overlay missing {rid}/{i}'
        source=ROOT/s['file'] if s['file'] else None
        sig=hashlib.sha256((json.dumps(s,sort_keys=True)+json.dumps(data['captions'],sort_keys=True)+done.read_text()+Path(__file__).read_text(encoding='utf8')+str(source.stat().st_mtime_ns if source else 0)).encode()).hexdigest()
        output=work/f'{i:03}.mp4';marker=work/f'{i:03}.json'
        if output.exists() and marker.exists() and json.loads(marker.read_text())['sig']==sig:continue
        events=[]
        for c in data['captions']:
            a=max(c['start'],s['start']);b=min(c['end'],s['end'])
            if b>a:events.append(f"Dialogue: 0,{stamp(a-s['start'],True)},{stamp(b-s['start'],True)},Main,,0,0,0,,{{\\fad(35,25)}}{caption_text(c['text'])}")
        ass=work/f'{i:03}.ass';ass.write_text(ASS+'\n'.join(events)+'\n',encoding='utf-8-sig')
        n=s['frames'];d=n/FPS;inputs=[]
        mode=s['mode'];crop=s.get('crop')
        if source:
            video=source.suffix.lower()=='.mp4'
            inputs+=['-ss',s['offset'],'-i',source] if video else ['-i',source]
            with av.open(str(source)) as c:sw=c.streams.video[0].width;sh=c.streams.video[0].height
            prefix=''
            if crop:
                x,y,w,h=crop;cw=int(sw*w)//2*2;ch=int(sh*h)//2*2;cx=int(sw*x)//2*2;cy=int(sh*y)//2*2
                prefix=f'crop={cw}:{ch}:{cx}:{cy},';sw=cw;sh=ch
            if mode=='portrait':
                focus=s.get('focus',.5)
                base=prefix+f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-ow)*{focus}:(ih-oh)*0.4,setsar=1'
                if not video:base+=f",scale=1350:2400,zoompan=z='1.015+0.035*on/{max(1,n-1)}':x='(iw-iw/zoom)*.5':y='(ih-ih/zoom)*.5':d={n}:s=1080x1920:fps=30"
                else:base='fps=30,'+base+',setpts=PTS-STARTPTS'
            else:
                # Full landscape evidence is preserved inside a vertical editorial frame.
                base=prefix+'scale=972:730:force_original_aspect_ratio=decrease,pad=972:730:(ow-iw)/2:(oh-ih)/2:color=0x090e17,setsar=1'
                if not video:
                    z='1' if s.get('ring') else ('1.045' if s.get('punch') else f'1.0+0.022*on/{max(1,n-1)}')
                    base+=f",zoompan=z='{z}':x='(iw-iw/zoom)*.5':y='(ih-ih/zoom)*.5':d={n}:s=972x730:fps=30"
                else:base='fps=30,'+base+',setpts=PTS-STARTPTS'
                base+=',pad=1080:1920:54:560:color=0x090e17'
            if video and 'motion' in s:base+=f",trim=duration={s['motion']},tpad=stop_mode=clone:stop={n},setpts=N/(30*TB)"
            base=f'[0:v]{base}[base]'
        else:
            inputs+=['-f','lavfi','-i',f'color=c=0x090e17:s=1080x1920:r=30:d={d}'];base='[0:v]setsar=1[base]'
        inputs+=['-framerate','30','-start_number','0','-i',overlay/'frame-%04d.png']
        rel=ass.relative_to(ROOT).as_posix()
        graph=f"{base};[1:v]format=rgba,tpad=stop_mode=clone:stop_duration={d},setpts=PTS-STARTPTS[graphics];[base][graphics]overlay=shortest=1,ass='{rel}',format=nv12[out]"
        run([*inputs,'-filter_complex_threads','2','-filter_complex',graph,'-map','[out]','-an','-frames:v',n,'-c:v','h264_qsv','-preset','medium','-global_quality','20','-look_ahead','0','-g','60',output],work/f'{i:03}.log')
        with av.open(str(output)) as c:assert c.streams.video[0].frames==n,(rid,i)
        write_json(marker,dict(sig=sig,frames=n))
        print(f'RENDER {rid} {i+1}/{len(data["shots"])}',flush=True)
    if only is not None:return
    listing=work/'concat.txt';listing.write_text('\n'.join(f"file '{s['index']:03}.mp4'\nduration {s['frames']/FPS:.9f}" for s in data['shots']),encoding='utf8')
    output=folder/'exportacoes'/f'Pixel_Procurado_{rid}_Short_1080x1920.mp4'
    run(['-f','concat','-safe','0','-i',listing,'-i',ROOT/data['voice'],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',data['frames']/FPS,'-movflags','+faststart',output],work/'mux.log')
    log=(work/'mux.log').read_text(encoding='utf8');assert not re.search('non.monoton|invalid|error',log,re.I),log[-3000:]
    print(f'FINAL {rid}',flush=True)

def qa(rid):
    folder=BASE/rid;data=json.loads((folder/'projeto/timeline.json').read_text(encoding='utf8'));q=folder/'projeto/qa';q.mkdir(exist_ok=True)
    movie=folder/'exportacoes'/f'Pixel_Procurado_{rid}_Short_1080x1920.mp4'
    with av.open(str(movie)) as c:
        v=c.streams.video[0];audio=c.streams.audio[0]
        info=dict(video_duration=float(v.duration*v.time_base),video_frames=v.frames,width=v.width,height=v.height,fps=float(v.average_rate),video_codec=v.codec_context.name,audio_codec=audio.codec_context.name,audio_rate=audio.codec_context.sample_rate,voice_duration=data['duration'])
    assert (info['width'],info['height'],info['fps'])==(1080,1920,30)
    assert abs(info['video_duration']-data['duration'])<=1/FPS+.002,info
    run(['-v','error','-i',movie,'-f','null','-'],q/'decodificacao_integral.txt')
    assert not (q/'decodificacao_integral.txt').read_text().strip(),rid
    with wave.open(str(folder/'voz/narracao.wav'),'rb') as w:ref=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768
    temp=q/'exportado.f32';run(['-i',movie,'-vn','-ar','48000','-ac','1','-f','f32le',temp],q/'decode_audio.log')
    test=np.fromfile(temp,dtype=np.float32);corr=[]
    for t in [.3,data['duration']*.25,data['duration']*.5,data['duration']*.75,data['duration']-3]:
        start=int(t*48000);end=min(start+96000,len(ref),len(test));a=ref[start:end];b=test[start:end]
        value=float(np.corrcoef(a,b)[0,1]);assert value>.97,(rid,t,value);corr.append(dict(start=t,correlation=value))
    temp.unlink()
    loud=producao.run(['-i',movie,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    info['loudness_aac']=json.loads(loud[loud.rfind('{'):loud.rfind('}')+1]);info['audio_correlations']=corr
    times=[.3,1.3,2.8,data['duration']*.28,data['duration']*.52,data['duration']*.77,data['duration']-1.0]
    images=[]
    for i,t in enumerate(times):
        p=q/f'amostra_{i:02}.jpg';run(['-ss',t,'-i',movie,'-frames:v','1','-q:v','2',p],q/f'frame_{i:02}.log');im=Image.open(p);im.thumbnail((270,480));images.append((im,t))
    sheet=Image.new('RGB',(270*len(images),520),'#151c28');draw=ImageDraw.Draw(sheet)
    for i,(im,t) in enumerate(images):sheet.paste(im,(i*270,0));draw.text((i*270+10,490),f'{rid} / {t:.2f}s',fill='white')
    sheet.save(q/'contato.jpg',quality=88)
    # Native video frame is the cover master; no synthetic replacement of game art.
    master=folder/'publicacao/capa_master.png';run(['-ss','1.1','-i',movie,'-frames:v','1',master],q/'capa.log')
    Image.open(master).convert('RGB').save(folder/'publicacao/capa_youtube.jpg',quality=94,optimize=True)
    write_json(q/'validacao_final.json',info)
    print(f'QA {rid}: {info["video_duration"]:.3f}s; audio min r={min(x["correlation"] for x in corr):.5f}',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','render','qa']);parser.add_argument('ids',nargs='*');parser.add_argument('--shots');args=parser.parse_args()
    for rid in args.ids or PLANS:
        if args.action=='prepare':prepare(rid)
        elif args.action=='render':render(rid,set(map(int,args.shots.split(','))) if args.shots else None)
        else:qa(rid)
