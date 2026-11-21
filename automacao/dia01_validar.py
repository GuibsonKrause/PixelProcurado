"""QA técnico e contatos do Dia01; não substitui inspeção visual ou escuta."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.production-tools/python'),str(ROOT/'.course-tools')]
import numpy as np

BASE=ROOT/'producao/SERIE_AQUECIMENTO_GTA6/DIA_01_2026-11-09'
FF=shutil.which('ffmpeg')
PROBE=shutil.which('ffprobe')

def run(args):
    p=subprocess.run([str(x) for x in args],capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode('utf-8',errors='replace')[-4000:])
    return p

def pcm(path,start):
    p=run([FF,'-v','error','-nostdin','-ss',start,'-i',path,'-t',3,'-vn','-ac',1,'-ar',16000,'-f','f32le','pipe:1'])
    return np.frombuffer(p.stdout,dtype=np.float32)

def correlation(a,b):
    n=min(len(a),len(b))
    assert n>=16000,'Trecho de voz menor que um segundo'
    return float(np.corrcoef(a[:n],b[:n])[0,1])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('video',type=Path)
    ap.add_argument('--reference',type=Path,default=BASE/'audio/narracao_final_hud.wav')
    ap.add_argument('--reference-start',type=float,default=0)
    ap.add_argument('--width',type=int,default=3840)
    ap.add_argument('--height',type=int,default=2160)
    ap.add_argument('--fps',type=float,default=30)
    args=ap.parse_args()
    assert FF and PROBE,'FFmpeg e FFprobe devem estar no PATH'
    assert args.video.is_file() and args.reference.is_file()
    assert abs(correlation(np.arange(16000),np.arange(16000))-1)<1e-9
    q=BASE/'qa'/args.video.stem
    q.mkdir(parents=True,exist_ok=True)
    info=json.loads(run([PROBE,'-v','error','-show_format','-show_streams','-of','json',args.video]).stdout)
    (q/'ffprobe.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    duration=float(info['format']['duration'])
    video_duration=float(v.get('duration',duration))
    audio_duration=float(a.get('duration',duration))
    fps=float(Fraction(v['avg_frame_rate']))
    assert (v['width'],v['height'])==(args.width,args.height)
    assert v['codec_name']=='h264' and abs(fps-args.fps)<.001
    assert a['codec_name']=='aac' and int(a['sample_rate'])==48000
    assert abs(video_duration-audio_duration)<=1/fps+.025, (video_duration,audio_duration)
    subtitle=args.video.with_suffix('.srt')
    assert subtitle.is_file(),f'SRT ausente: {subtitle}'
    cues=re.findall(r'(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})',subtitle.read_text(encoding='utf-8-sig'))
    assert cues,'SRT sem marcações válidas'
    def stamp_seconds(t):
        h,m,s=t.replace(',','.').split(':')
        return 3600*int(h)+60*int(m)+float(s)
    intervals=[(stamp_seconds(s),stamp_seconds(e)) for s,e in cues]
    assert all(0<=s<e<=duration+1/fps for s,e in intervals),'Limite inválido de legenda'
    assert all(intervals[i][0]>=intervals[i-1][1]-1/fps for i in range(1,len(intervals))),'Sobreposição de legendas'
    contact=q/'contato_16_quadros.jpg'
    filters=f'[0:v:0]split=2[scan][thumb];[scan]blackdetect=d=0.15:pix_th=0.10:pic_th=0.98[checked];[thumb]fps={16/duration:.12f},scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2,tile=4x4[sheet]'
    command=[FF,'-hide_banner','-nostdin','-y','-i',args.video,'-filter_complex',filters,'-map','[checked]','-map','0:a:0','-af','ebur128=peak=true','-f','null','-','-map','[sheet]','-frames:v','1',contact]
    decoded=subprocess.run([str(x) for x in command],capture_output=True)
    log=decoded.stderr.decode('utf-8',errors='replace')
    (q/'decode_black_ebur.log').write_text(log,encoding='utf-8')
    assert decoded.returncode==0,log[-4000:]
    issues=re.findall(r'^.*(?:non.monoton|corrupt|invalid data|error while decoding).*$' ,log,re.I|re.M)
    assert not issues,issues
    assert contact.is_file() and contact.stat().st_size>1000
    blacks=[dict(zip(('start','end','duration'),map(float,m))) for m in re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',log)]
    summary=log.rsplit('Summary:',1)[-1]
    loud=re.search(r'I:\s*([-\d.]+) LUFS',summary)
    peak=re.search(r'Peak:\s*([-\d.]+) dBFS',summary)
    lra=re.search(r'LRA:\s*([-\d.]+) LU',summary)
    assert loud and peak and lra,'Medição EBU R128 ausente'
    times=[.5,max(.5,duration/2-1.5),max(.5,duration-4)]
    correlations=[]
    for t in times:
        reference=pcm(args.reference,args.reference_start+t)
        encoded=pcm(args.video,t)
        correlations.append({'time':round(t,3),'correlation':correlation(reference,encoded)})
    assert min(x['correlation'] for x in correlations)>.98,correlations
    report={'file':str(args.video.resolve()),'bytes':args.video.stat().st_size,'width':v['width'],'height':v['height'],'fps':fps,'video_codec':v['codec_name'],'pixel_format':v.get('pix_fmt'),'container_duration':duration,'video_duration':video_duration,'audio_duration':audio_duration,'audio_codec':a['codec_name'],'audio_rate':int(a['sample_rate']),'full_decode_pass':True,'temporal_errors':issues,'black_intervals_review':blacks,'loudness_lufs':float(loud.group(1)),'true_peak_dbfs':float(peak.group(1)),'lra_lu':float(lra.group(1)),'audio_reference':str(args.reference.resolve()),'reference_start':args.reference_start,'audio_correlations':correlations,'contact_sheet':str(contact.resolve()),'contact_times':[round((i+.5)*duration/16,3) for i in range(16)],'limitations':'Technical full decode; visual sampling and audio correlation do not establish subjective listening or factual correctness.'}
    with args.video.open('rb') as media:
        report['sha256']=hashlib.file_digest(media,'sha256').hexdigest()
    report['video_mtime_ns']=args.video.stat().st_mtime_ns
    report['subtitles']={'file':str(subtitle.resolve()),'cues':len(cues),'first':intervals[0][0],'last':intervals[-1][1],'bounds_and_overlap_pass':True}
    (q/'RELATORIO_QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':
    main()
