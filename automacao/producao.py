"""Ferramentas locais do Pixel Procurado. Nenhum upload, API paga ou overwrite implícito."""
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / '.production-tools/python'), str(ROOT / '.course-tools')]

def run(args):
    import imageio_ffmpeg
    p = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-nostdin', '-n', *map(str, args)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode:
        raise RuntimeError(p.stderr[-5000:])
    return p.stderr

def probe(path):
    import av
    with av.open(str(path)) as c:
        duration = c.duration / av.time_base if c.duration else None
        return {'path': str(path), 'duration': duration,
                'streams': [{'type': s.type, 'codec': s.codec_context.name} for s in c.streams]}

def output(path):
    path = Path(path).resolve()
    if path.exists():
        raise ValueError(f'Saída já existe; escolha outro nome: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def seconds(value):
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError('Tempo deve ser finito e não negativo')
    return value

def normalize(src, dest):
    log = run(['-i', src, '-vn', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    stats = json.loads(log[log.rfind('{'):log.rfind('}') + 1])
    names = {'input_i': 'measured_I', 'input_tp': 'measured_TP', 'input_lra': 'measured_LRA',
             'input_thresh': 'measured_thresh', 'target_offset': 'offset'}
    if not all(math.isfinite(float(stats[k])) for k in names):
        raise ValueError('Áudio silencioso ou medição inválida; revise a gravação')
    filt = 'loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:' + ':'.join(f'{v}={stats[k]}' for k, v in names.items())
    run(['-i', src, '-vn', '-af', filt, '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', dest])

def stamp(t):
    ms = round(t * 1000)
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}'

def transcribe(src, dest, model):
    from faster_whisper import WhisperModel
    import numpy as np
    m = WhisperModel(model, device='cpu', compute_type='int8', cpu_threads=4,
                     download_root=str(ROOT / '.course-tools/models'), local_files_only=True)
    with tempfile.TemporaryDirectory(prefix='pixel-asr-') as tmp:
        decoded = Path(tmp) / 'audio.f32'
        run(['-i', src, '-vn', '-ar', '16000', '-ac', '1', '-f', 'f32le', decoded])
        audio = np.fromfile(decoded, dtype=np.float32)
    segments, _ = m.transcribe(audio, language='pt', beam_size=5, vad_filter=True,
                              initial_prompt='Pixel Procurado. GTA VI. Jason. Lucia. Leonida. Vice City.')
    lines = []
    for i, s in enumerate(segments, 1):
        lines.append(f'{i}\n{stamp(s.start)} --> {stamp(s.end)}\n{s.text.strip()}\n')
    if not lines:
        raise ValueError('Nenhuma fala identificada')
    dest.write_text('\n'.join(lines), encoding='utf-8')

def words(src, dest, model):
    """Exporta marcações por palavra para revisão e correções cirúrgicas."""
    from faster_whisper import WhisperModel
    import numpy as np
    m = WhisperModel(model, device='cpu', compute_type='int8', cpu_threads=4,
                     download_root=str(ROOT / '.course-tools/models'), local_files_only=True)
    with tempfile.TemporaryDirectory(prefix='pixel-asr-') as tmp:
        decoded = Path(tmp) / 'audio.f32'
        run(['-i', src, '-vn', '-ar', '16000', '-ac', '1', '-f', 'f32le', decoded])
        audio = np.fromfile(decoded, dtype=np.float32)
    segments, _ = m.transcribe(audio, language='pt', beam_size=5, vad_filter=True,
                               word_timestamps=True,
                               initial_prompt='Pixel Procurado. GTA VI. Jason. Lucia. Leonida. Vice City.')
    result = [{'start': round(w.start, 3), 'end': round(w.end, 3),
               'word': w.word.strip(), 'probability': round(w.probability, 4)}
              for segment in segments for w in (segment.words or [])]
    if not result:
        raise ValueError('Nenhuma palavra identificada')
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

def clip(src, dest, start, end, vertical):
    info = probe(src)
    if end <= start or not info['duration'] or end > info['duration'] + 0.05:
        raise ValueError('Intervalo fora da duração da mídia')
    vf = ('scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1'
          if vertical else 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1')
    run(['-ss', start, '-i', src, '-t', end-start, '-map', '0:v:0', '-map', '0:a?', '-vf', vf,
         '-r', '30', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', dest])

def assemble(manifest, dest):
    data = json.loads(manifest.read_text(encoding='utf-8-sig'))
    base = manifest.parent
    voice = (base / data['voice']).resolve()
    voice_info = probe(voice)
    if not any(s['type'] == 'audio' for s in voice_info['streams']):
        raise ValueError('Narração não contém áudio')
    clips = data['clips']
    if not clips:
        raise ValueError('Nenhuma cena')
    total = sum(seconds(c['duration']) for c in clips)
    if not voice_info['duration'] or abs(total - voice_info['duration']) > 0.25:
        raise ValueError(f'Cenas ({total:.2f}s) devem cobrir a voz ({voice_info["duration"]}s), tolerância 0,25s')
    for c in clips:
        src = (base / c['file']).resolve()
        duration, start = seconds(c['duration']), seconds(c.get('start', 0))
        if duration <= 0 or not src.is_file() or not c.get('source') or c.get('use_reviewed') is not True:
            raise ValueError(f'Cena sem arquivo, duração positiva, fonte ou revisão de uso: {c}')
        if c['kind'] not in ('image', 'video'):
            raise ValueError('kind deve ser image ou video')
        if c['kind'] == 'video':
            media_duration = probe(src)['duration']
            if not media_duration or start + duration > media_duration + 0.05:
                raise ValueError(f'Cena excede o vídeo: {src}')
    with tempfile.TemporaryDirectory(prefix='pixel-', dir=dest.parent) as tmp:
        tmp = Path(tmp)
        for i, c in enumerate(clips):
            src = (base / c['file']).resolve()
            inputs = ['-loop', '1', '-i', src] if c['kind'] == 'image' else ['-ss', c.get('start', 0), '-i', src]
            vf = 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
            if c.get('label'):
                label = str(c['label']).replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'")
                vf += (",drawbox=x=38:y=h-96:w=520:h=56:color=black@0.72:t=fill"
                       ",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':"
                       f"text='{label}':fontcolor=white:fontsize=28:x=56:y=h-82")
            run([*inputs, '-t', c['duration'], '-an', '-vf',
                 vf,
                 '-r', '30', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', tmp / f'{i:04}.mp4'])
        listing = tmp / 'list.txt'
        listing.write_text(''.join(f"file '{i:04}.mp4'\n" for i in range(len(clips))), encoding='utf-8')
        run(['-f', 'concat', '-safe', '1', '-i', listing, '-i', voice, '-map', '0:v:0', '-map', '1:a:0',
             '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', dest])

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)
    for name in ('probe', 'normalize', 'transcribe', 'words', 'clip', 'assemble'):
        q = sub.add_parser(name)
        q.add_argument('input', type=Path)
        if name != 'probe': q.add_argument('output', type=Path)
        if name in ('transcribe', 'words'): q.add_argument('--model', default='base', choices=['base', 'small'])
        if name == 'clip':
            q.add_argument('--start', required=True, type=seconds)
            q.add_argument('--end', required=True, type=seconds)
            q.add_argument('--vertical', action='store_true')
    a = p.parse_args()
    if not a.input.is_file(): p.error(f'Arquivo não encontrado: {a.input}')
    if a.cmd == 'probe': print(json.dumps(probe(a.input), ensure_ascii=False, indent=2)); return
    dest = output(a.output)
    if a.cmd == 'normalize': normalize(a.input, dest)
    elif a.cmd == 'transcribe': transcribe(a.input, dest, a.model)
    elif a.cmd == 'words': words(a.input, dest, a.model)
    elif a.cmd == 'clip': clip(a.input, dest, a.start, a.end, a.vertical)
    elif a.cmd == 'assemble': assemble(a.input.resolve(), dest)
    print(f'Gerado: {dest}')

if __name__ == '__main__':
    try: main()
    except (ValueError, RuntimeError, KeyError) as e:
        print(f'ERRO: {e}', file=sys.stderr)
        sys.exit(1)
