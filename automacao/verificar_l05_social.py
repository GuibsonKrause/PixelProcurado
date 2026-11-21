"""QA por amostragem das derivações L05 já decodificadas pelo distribuidor."""
import array
import json
import math
import subprocess
import sys
from pathlib import Path
import distribuir_l05_postiz as s

sys.path.insert(0,str(s.ROOT/'.course-tools'))
sys.path.insert(0,str(s.ROOT/'.production-tools/python'))
import av
from PIL import Image, ImageDraw


def audio(path, start, duration=3):
    result=subprocess.run([str(s.FFMPEG),'-v','error','-ss',str(start),'-i',str(path),'-t',str(duration),
                           '-map','0:a:0','-vn','-ac','1','-ar','8000','-f','f32le','-'],capture_output=True,check=True)
    samples=array.array('f');samples.frombytes(result.stdout)
    return samples


def correlation(first,second):
    size=min(len(first),len(second))
    a,b=first[:size:8],second[:size:8]
    ma,mb=sum(a)/len(a),sum(b)/len(b)
    covariance=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    return covariance/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))


def main():
    qa=json.loads(s.read(s.SOCIAL/'DERIVACOES_QA.json'))
    assert qa['source_sha256']==s.digest(s.SOURCE)
    report={'method':'amostragem visual + correlação de áudio; decodificação integral em DERIVACOES_QA.json','assets':{}}
    for name,times in {'facebook_feed':[.5,4,18,82,172,267,319],
                       'instagram_feed':[.5,4,18,82,172,267,319],
                       'facebook_story':[.5,4,13,18,23.8]}.items():
        path=s.FILES[name]
        assert qa['assets'][name]['sha256']==s.digest(path)
        with av.open(str(path)) as container:
            stream=container.streams.video[0]
            timing={'video_duration':float(stream.duration*stream.time_base),'frames':stream.frames,'fps':float(stream.average_rate),'bytes':path.stat().st_size}
        assert timing['fps']==30
        expected=qa['story_end'] if name=='facebook_story' else 9746/30
        assert abs(timing['video_duration']-expected)<=1/30
        frames=[]
        thumb_size=(480,270) if name=='facebook_feed' else (270,480)
        for stamp in times:
            target=s.SOCIAL/f'{name}_{stamp:g}s.jpg'
            s.command(['-v','error','-y','-threads','2','-ss',str(stamp),'-i',str(path),'-frames:v','1',
                       '-vf',f'scale={thumb_size[0]}:{thumb_size[1]}','-threads','2',str(target)])
            frame=Image.open(target).convert('RGB')
            tile=Image.new('RGB',(thumb_size[0],thumb_size[1]+30),'#242424');tile.paste(frame,(0,30))
            ImageDraw.Draw(tile).text((10,8),f'{name} / {stamp:g}s',fill='white')
            frames.append(tile)
        columns=3 if name=='facebook_feed' else 4
        rows=math.ceil(len(frames)/columns)
        sheet=Image.new('RGB',(columns*frames[0].width,rows*frames[0].height),'#111318')
        for index,frame in enumerate(frames):sheet.paste(frame,((index%columns)*frame.width,(index//columns)*frame.height))
        sheet.save(s.SOCIAL/f'{name}_CONTATO.jpg',quality=92)
        positions=[1,11,20] if name=='facebook_story' else [1,160,319]
        correlations=[{'start':t,'seconds':3,'correlation':correlation(audio(s.SOURCE,t),audio(path,t))} for t in positions]
        assert min(x['correlation'] for x in correlations)>.98,correlations
        report['assets'][name]={'sha256':s.digest(path),'sample_frames_seconds':times,'timing':timing,'audio':correlations,'technical_result':'PASS'}
        s.write(s.SOCIAL/'QA_SOCIAL_AMOSTRAS.json',report)
        print(name+': amostras e áudio PASS',flush=True)


if __name__=='__main__':main()
