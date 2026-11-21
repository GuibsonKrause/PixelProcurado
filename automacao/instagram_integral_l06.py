"""Adapte toda a duração do L06 para Reel do Instagram e valide a saída."""
import argparse
import json
import subprocess
import textwrap

from distribuir_l05_postiz import FFMPEG
from distribuir_l06_postiz import MASTER, SOCIAL, command, digest, metadata, read, write
from vertical_l06_social import ASS, ass_time, cue_data

OUTPUT = SOCIAL / 'L06_Instagram_Integral_1080x1920.mp4'
REPORT = SOCIAL / 'INSTAGRAM_INTEGRAL_QA.json'


def safe_ass(text):
    return text.replace('{', '').replace('}', '').replace('\\', '')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', type=float, help='Gera amostra de quatro segundos no ponto indicado.')
    parser.add_argument('--light', action='store_true', help='Cópia de menor bitrate para transferência.')
    args = parser.parse_args()
    output = OUTPUT.with_stem(OUTPUT.stem + '_Leve') if args.light else OUTPUT
    report = REPORT.with_stem(REPORT.stem + '_LEVE') if args.light else REPORT
    rate = ('1400k', '2100k', '4200k') if args.light else ('3100k', '4600k', '9200k')
    source_hash = digest(MASTER)
    source_meta = metadata(MASTER)
    duration = source_meta['duration']
    if not (3 <= duration <= 900 and source_meta['h264'] and source_meta['aac']):
        raise ValueError('Master incompatível com o limite de Reel.')
    source_srt = MASTER.with_suffix('.srt')
    timeline = MASTER.parents[1] / 'projeto/edicao_l06.json'
    shots = json.loads(read(timeline))['shots']
    if any(shot.get('captionBox') for shot in shots):
        raise ValueError('Há legendas fora da faixa padrão no master.')
    start = args.sample if args.sample is not None else 0
    end = min(start + 4, duration) if args.sample is not None else duration
    subtitles = SOCIAL / ('L06_ig_integral_amostra.ass' if args.sample is not None else 'L06_ig_integral.ass')
    captions = []
    for t0, t1, text in cue_data(source_srt):
        if t0 < end and t1 > start:
            copy = r'\N'.join(textwrap.wrap(safe_ass(text), width=34, break_long_words=False))
            captions.append(f'Dialogue: 0,{ass_time(t0-start)},{ass_time(min(t1,end)-start)},Main,,0,0,0,,{copy}')
    for shot in shots:
        t0, t1 = shot['start'], shot['end']
        if t0 < end and t1 > start:
            credit = safe_ass(shot['source'])
            captions.append(f'Dialogue: 0,{ass_time(t0-start)},{ass_time(min(t1,end)-start)},Credit,,0,0,0,,{credit}')
    subtitles.write_text(ASS + '\n'.join(captions) + '\n', encoding='utf8')
    line1 = SOCIAL / 'L06_ig_integral_titulo1.txt'
    line2 = SOCIAL / 'L06_ig_integral_titulo2.txt'
    line1.write_text('LEONIDA ALÉM', encoding='utf8')
    line2.write_text('DE VICE CITY', encoding='utf8')
    font = r"fontfile='C\:/Windows/Fonts/arialbd.ttf'"
    filters = ['scale_qsv=w=1080:h=608:format=nv12', 'hwdownload', 'format=nv12',
               'crop=1080:522:0:0', 'pad=1080:1920:0:580:color=0x111318', 'setsar=1',
               f'ass={subtitles.name}',
               f"drawtext={font}:textfile={line1.name}:fontcolor=0xFFD33D:fontsize=79:x=(w-tw)/2:y=284",
               f"drawtext={font}:textfile={line2.name}:fontcolor=0xFFD33D:fontsize=79:x=(w-tw)/2:y=386",
               f"drawtext={font}:text='PIXEL PROCURADO  /  EPISÓDIO COMPLETO':fontcolor=0xC0C3C6:fontsize=34:x=(w-tw)/2:y=1510"]
    signature = {'master_sha256': source_hash, 'srt_sha256': digest(source_srt),
                 'timeline_sha256': digest(timeline), 'subtitles_sha256': digest(subtitles),
                 'filters': filters, 'bitrate': rate[0]}
    if args.sample is None and output.is_file() and report.is_file():
        prior = json.loads(read(report))
        if (prior.get('signature') == signature and prior.get('sha256') == digest(output)
                and prior.get('full_decode_pass')):
            print('Integral existente validado.', flush=True)
            return
    target = SOCIAL / 'L06_ig_integral_amostra.mp4' if args.sample is not None else output
    temp = target.with_suffix('.rendering.mp4')
    ff = ['-hide_banner', '-loglevel', 'error', '-y', '-hwaccel', 'qsv',
          '-hwaccel_output_format', 'qsv', '-ss', str(start), '-i', str(MASTER),
          '-map', '0:v:0', '-map', '0:a:0', '-vf', ','.join(filters),
          '-filter_threads', '4', '-c:v', 'h264_qsv', '-preset', 'veryfast',
          '-b:v', rate[0], '-maxrate', rate[1], '-bufsize', rate[2],
          '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', '-movflags', '+faststart']
    if args.sample is not None:
        ff += ['-t', str(end-start)]
    ff.append(str(temp))
    print(f'Render Instagram: {end-start:.2f}s', flush=True)
    subprocess.run([str(FFMPEG), *ff], cwd=SOCIAL, check=True)
    print('Decodificação integral em curso.', flush=True)
    command(['-v', 'error', '-xerror', '-i', str(temp), '-f', 'null', '-'])
    meta = metadata(temp)
    if ((meta['width'], meta['height']) != (1080, 1920)
            or not (meta['h264'] and meta['aac']) or abs(meta['duration']-(end-start)) > .15
            or temp.stat().st_size >= 300_000_000 or source_hash != digest(MASTER)):
        raise ValueError('Derivação diverge das propriedades esperadas.')
    temp.replace(target)
    if args.sample is None:
        write(report, {**meta, 'bytes': target.stat().st_size, 'signature': signature,
                       'sha256': digest(target), 'full_decode_pass': True})
    print(f'{target.name}: {meta}', flush=True)


if __name__ == '__main__':
    main()
