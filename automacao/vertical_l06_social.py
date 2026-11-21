"""Extraia do master do L06 a comparação urbana, com legendas verticais."""
import argparse
import json
import re
import subprocess
import textwrap
from pathlib import Path

from distribuir_l05_postiz import FFMPEG
from distribuir_l06_postiz import MASTER, SOCIAL, VERTICAL, command, digest, metadata, read, write

STAMP = r'(\d+):(\d+):(\d+),(\d+)'
ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial,50,&H00FFFFFF,&H00FFFFFF,&H00181311,&H00181311,-1,0,0,0,100,100,0,0,1,2,0,8,76,76,1210,1
Style: Credit,Arial,24,&H00C6C3C0,&H00FFFFFF,&H00181311,&H00181311,0,0,0,0,100,100,0,0,1,1,0,8,62,62,1136,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def seconds(stamp):
    h, m, s, ms = map(int, stamp)
    return h * 3600 + m * 60 + s + ms / 1000


def ass_time(value):
    centiseconds = max(0, round(value * 100))
    h, remainder = divmod(centiseconds, 360000)
    m, remainder = divmod(remainder, 6000)
    s, cs = divmod(remainder, 100)
    return f'{h}:{m:02}:{s:02}.{cs:02}'


def cue_data(path):
    for block in re.split(r'\n\s*\n', read(path)):
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        times = re.findall(STAMP, lines[1])
        if len(times) == 2:
            yield (seconds(times[0]), seconds(times[1]), ' '.join(lines[2:]))


def time_bounds(cues, paragraphs):
    opening = next(p for p in paragraphs if p['text'].startswith('Vice City aparece'))
    first = next(i for i, row in enumerate(cues) if 'Vice City aparece' in row[2])
    last = next(i for i, row in enumerate(cues) if i > first and 'hotel de verdade.' in row[2])
    start = opening['start'] - .025
    end = min(cues[last + 1][0] - .02, cues[last][1] + .14)
    if not 10 <= end - start < 120:
        raise ValueError('Intervalo urbano inesperado.')
    return start, end


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--srt', default=str(MASTER.with_suffix('.srt')))
    parser.add_argument('--bounds-only', action='store_true')
    parser.add_argument('--crop-bottom', type=int, default=86,
                        help='Altura a retirar da imagem horizontal já escalada para remover legenda anterior.')
    args = parser.parse_args()

    srt = Path(args.srt)
    cues = list(cue_data(srt))
    alignment = MASTER.parents[1] / 'voz/paragrafos_alinhados.json'
    start, end = time_bounds(cues, json.loads(read(alignment)))
    print(f'{start:.3f}–{end:.3f} ({end-start:.3f}s)', flush=True)
    if args.bounds_only:
        return
    if not 0 <= args.crop_bottom <= 120 or args.crop_bottom % 2:
        raise ValueError('Recorte inferior deve ser par e estar entre 0 e 120 pixels.')
    SOCIAL.mkdir(parents=True, exist_ok=True)
    subtitle = SOCIAL / 'L06_vertical_legendas.ass'
    title = SOCIAL / 'L06_vertical_titulo.txt'
    footer = SOCIAL / 'L06_vertical_rodape.txt'
    title.write_text('VICE CITY ×\nPORT GELLHORN', encoding='utf8')
    footer.write_text('DOIS TIPOS DE BRILHO\nPIXEL PROCURADO', encoding='utf8')
    captions = []
    for cue_start, cue_end, copy in cues:
        if cue_start < end and cue_end > start:
            if cue_start < start:
                copy = 'Vice City aparece' + copy.split('Vice City aparece', 1)[1]
            clean = copy.replace('{', '').replace('}', '').replace('\\', '')
            formatted = r'\N'.join(textwrap.wrap(clean, width=34, break_long_words=False))
            captions.append(f'Dialogue: 0,{ass_time(cue_start-start)},{ass_time(min(cue_end,end)-start)},Main,,0,0,0,,{formatted}')
    timeline = MASTER.parents[1] / 'projeto/edicao_l06.json'
    shots = json.loads(read(timeline))['shots']
    for shot in shots:
        if shot['start'] < end and shot['end'] > start:
            if shot.get('captionBox'):
                raise ValueError('Este trecho tem legenda em posição variável no master.')
            credit = shot['source'].replace('{', '').replace('}', '')
            t0 = ass_time(shot['start'] - start)
            t1 = ass_time(min(shot['end'], end) - start)
            captions.append(f'Dialogue: 0,{t0},{t1},Credit,,0,0,0,,{credit}')
    subtitle.write_text(ASS + '\n'.join(captions) + '\n', encoding='utf8')
    filters = [
        'scale=1080:608:flags=lanczos', f'crop=1080:{608-args.crop_bottom}:0:0',
        'pad=1080:1920:0:580:color=0x111318', 'setsar=1', 'ass=L06_vertical_legendas.ass',
        r"drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':textfile='L06_vertical_titulo.txt':fontcolor=0xFFD33D:fontsize=75:x=(w-tw)/2:y=278:line_spacing=20",
        r"drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':textfile='L06_vertical_rodape.txt':fontcolor=0xC0C3C6:fontsize=37:x=(w-tw)/2:y=1470:line_spacing=12",
    ]
    temp = VERTICAL.with_suffix('.rendering.mp4')
    master_hash = digest(MASTER)
    spec = dict(start=start, end=end, filters=filters, master_sha256=master_hash,
                srt_sha256=digest(srt), alignment_sha256=digest(alignment), timeline_sha256=digest(timeline), captions_sha256=digest(subtitle), title_sha256=digest(title),
                footer_sha256=digest(footer))
    manifest = SOCIAL / 'VERTICAL_QA.json'
    if VERTICAL.exists() and manifest.exists():
        old = json.loads(read(manifest))
        if old.get('spec') == spec and old.get('sha256') == digest(VERTICAL) and old.get('full_decode_pass'):
            return
    args = ['-hide_banner', '-loglevel', 'error', '-y', '-ss', str(start), '-threads', '4', '-i', str(MASTER),
            '-t', str(end-start), '-map', '0:v:0', '-map', '0:a:0', '-vf', ','.join(filters),
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-maxrate', '6M', '-bufsize', '12M',
            '-threads', '4', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
            '-ar', '48000', '-movflags', '+faststart', str(temp)]
    subprocess.run([str(FFMPEG), *args], cwd=SOCIAL, check=True)
    command(['-v', 'error', '-xerror', '-i', str(temp), '-f', 'null', '-'])
    meta = metadata(temp)
    if (meta['width'], meta['height']) != (1080, 1920) or not (meta['h264'] and meta['aac']):
        raise ValueError('Características incompatíveis para o corte vertical.')
    if abs(meta['duration'] - (end-start)) > .2 or master_hash != digest(MASTER):
        raise ValueError('Duração divergente ou master mudou durante a derivação.')
    temp.replace(VERTICAL)
    write(manifest, {'spec': spec, 'sha256': digest(VERTICAL), 'full_decode_pass': True, **meta})


if __name__ == '__main__':
    main()
