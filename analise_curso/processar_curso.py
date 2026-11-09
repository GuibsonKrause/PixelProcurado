"""Local inventory, visual sampling and full audio transcription of supplied course."""
from pathlib import Path
import sys, os, json, argparse, time

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / '.course-tools'))
OUT = ROOT / 'analise_curso'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['HF_HUB_DISABLE_XET'] = '1'
os.environ['HF_HOME'] = str(ROOT / '.course-tools' / 'hf-cache')

def stamp(t):
    t = int(t)
    return f'{t//3600:02}:{t%3600//60:02}:{t%60:02}'

def inventory():
    import av
    from PIL import Image, ImageDraw
    rows = []
    for path in sorted(ROOT.glob('*.mp4')):
        with av.open(str(path)) as c:
            seconds = c.duration / av.time_base
            streams = [{'type':s.type, 'codec':s.codec_context.name} for s in c.streams]
            rows.append({'file':path.name,'seconds':seconds,'duration':stamp(seconds),'streams':streams})
            video = c.streams.video[0]
            points = [min(seconds-1, 5+i*max(1,(seconds-10)/11)) for i in range(12)]
            sheet = Image.new('RGB',(1200,4*250),'#202020')
            draw = ImageDraw.Draw(sheet)
            for i, point in enumerate(points):
                c.seek(int(point / video.time_base), stream=video)
                frame = next(c.decode(video))
                img = frame.to_image()
                img.thumbnail((400,225))
                x,y=(i%3)*400,(i//3)*250
                sheet.paste(img,(x,y))
                draw.text((x+5,y+228),f'{path.name[:2]} | {stamp(float(frame.time or point))}',fill='white')
            sheet.save(OUT / f'{path.name[:2]}_amostras.jpg',quality=85)
        print(json.dumps(rows[-1], ensure_ascii=False),flush=True)
    (OUT/'inventario.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')

def pdf():
    from pypdf import PdfReader
    for path in ROOT.glob('*.pdf'):
        r=PdfReader(path)
        text='\n\n'.join(f'## Página {i+1}\n\n{p.extract_text()}' for i,p in enumerate(r.pages))
        (OUT/(path.stem+'.pdf.txt')).write_text(text,encoding='utf-8')
        print(text,flush=True)

def transcribe(modelname, only):
    from faster_whisper import WhisperModel, BatchedInferencePipeline
    import av
    import numpy as np
    model=WhisperModel(modelname,device='cpu',compute_type='int8',cpu_threads=8,num_workers=1,download_root=str(ROOT/'.course-tools'/'models'))
    pipeline=BatchedInferencePipeline(model=model)
    for path in sorted(ROOT.glob('*.mp4')):
        if only and path.name[:2] not in only: continue
        dest=OUT/(path.stem+'.json')
        if dest.exists():
            print('ALREADY COMPLETE '+path.name,flush=True)
            continue
        print('START '+path.name,flush=True)
        started=time.time()
        # Decode explicitly: PyAV 19 no longer accepts metadata_errors in av.open.
        arrays=[]
        with av.open(str(path)) as container:
            resampler=av.AudioResampler(format='fltp',layout='mono',rate=16000)
            for frame in container.decode(audio=0):
                for out in resampler.resample(frame): arrays.append(out.to_ndarray().reshape(-1))
            for out in resampler.resample(None): arrays.append(out.to_ndarray().reshape(-1))
        audio=np.concatenate(arrays)
        del arrays
        segments, info=pipeline.transcribe(audio,language='pt',beam_size=1,vad_filter=True,batch_size=8)
        records=[]
        partial=OUT/(path.stem+'.partial.txt')
        with partial.open('w',encoding='utf-8') as f:
            last=0
            for s in segments:
                item={'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob}
                records.append(item)
                f.write(f'[{stamp(s.start)}–{stamp(s.end)}] {s.text.strip()}\n');f.flush()
                if s.end-last>=60:
                    print(f'PROGRESS {path.name[:2]} {stamp(s.end)} / {stamp(info.duration)} elapsed={int(time.time()-started)}s',flush=True)
                    last=s.end
        data={'source':path.name,'model':modelname,'language':info.language,'duration':info.duration,'duration_after_vad':info.duration_after_vad,'segments':records}
        dest.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        partial.rename(OUT/(path.stem+'.txt'))
        print('DONE '+path.name+' '+str(round(time.time()-started))+'s',flush=True)

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    p=argparse.ArgumentParser();p.add_argument('action',choices=['inventory','pdf','transcribe']);p.add_argument('--model',default='small');p.add_argument('--only',nargs='*')
    a=p.parse_args()
    if a.action=='inventory':inventory()
    elif a.action=='pdf':pdf()
    else:transcribe(a.model,a.only)
