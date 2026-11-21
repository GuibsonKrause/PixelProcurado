"""Isolated source-project reexports; approved masters are read-only."""
import argparse
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'producao/TIKTOK_CATALOGO_2026-11-10/qualidade_maxima'
sys.path[:0] = [str(ROOT / '.production-tools/python'), str(ROOT / '.course-tools')]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf8')


def load(path):
    spec = importlib.util.spec_from_file_location('source_l08', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def validate(movie, old, frames, size, fps=60):
    import numpy as np
    from PIL import Image, ImageDraw
    q = movie.parent.parent / 'qa' / movie.stem
    q.mkdir(parents=True, exist_ok=True)
    info, previous = probe(movie), probe(old)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    assert (video['width'], video['height']) == size
    assert video['codec_name'] == 'h264' and audio['codec_name'] == 'aac'
    assert int(video['nb_frames']) == frames
    assert abs(float(video['duration']) - frames / fps) < .02
    assert movie.stat().st_size < 4_000_000_000
    ff = str(next((ROOT / '.production-tools/python/imageio_ffmpeg/binaries').glob('*.exe')))
    with (q / 'decode_black_loudness.log').open('w', encoding='utf8') as log:
        subprocess.run([ff, '-hide_banner', '-nostdin', '-nostats', '-xerror', '-threads', '2', '-i', str(movie), '-vf', 'blackdetect=d=0.15:pic_th=0.98:pix_th=0.10', '-af', 'ebur128=peak=true:framelog=verbose', '-f', 'null', 'NUL'], check=True, stdout=subprocess.DEVNULL, stderr=log)
    report = (q / 'decode_black_loudness.log').read_text(encoding='utf8')
    blacks = re.findall(r'black_start:([^\n]+)', report)
    correlations = []
    duration = frames / fps
    for t in [.3, duration * .5, duration - 3]:
        signals = []
        for p in [old, movie]:
            raw = subprocess.check_output([ff, '-v', 'error', '-ss', str(t), '-i', str(p), '-t', '2', '-vn', '-ar', '48000', '-ac', '1', '-f', 'f32le', '-'])
            signals.append(np.frombuffer(raw, dtype='<f4'))
        n = min(map(len, signals))
        corr = float(np.corrcoef(signals[0][:n], signals[1][:n])[0, 1])
        assert corr > .97, (t, corr)
        correlations.append({'time': t, 'correlation': corr})
    times = [.3, 1.2, 3, duration * .3, duration * .5, duration * .8, duration - .6]
    tw, th = ((480, 270) if size[0] > size[1] else (270, 480))
    sheet = Image.new('RGB', (tw * len(times), (th + 32) * 2), '#151c28')
    draw = ImageDraw.Draw(sheet)
    for row, path in enumerate([old, movie]):
        for i, t in enumerate(times):
            frame = q / f'{row}_{i}.jpg'
            subprocess.run([ff, '-v', 'error', '-y', '-ss', str(t), '-i', str(path), '-frames:v', '1', '-q:v', '2', str(frame)], check=True)
            image = Image.open(frame); image.thumbnail((tw, th))
            sheet.paste(image, (i * tw, row * (th + 32)))
            draw.text((i * tw + 5, row * (th + 32) + th + 5), f'{"APPROVED" if row == 0 else "4K"} {t:.2f}s', fill='white')
    contact = q / 'comparacao.jpg'
    sheet.save(contact, quality=93)
    result = {'path': str(movie), 'approved_reference': str(old), 'bytes': movie.stat().st_size, 'probe': info, 'reference_probe': previous, 'frames': frames, 'decode_integral': 'passed', 'black_intervals': blacks, 'audio_correlations': correlations, 'contact': str(contact), 'loudness_log': str(q / 'decode_black_loudness.log')}
    write(q / 'validacao.json', result)
    return result


def l08(modes):
    source = ROOT / 'producao/L08/produzir_l08.py'
    m = load(source)
    m.BUILD = DEST / 'L08/montagem'
    m.OUT = DEST / 'L08/exportacoes'
    m.BUILD.mkdir(parents=True, exist_ok=True)
    m.OUT.mkdir(parents=True, exist_ok=True)
    original_prepare = m.prepare_hyperframes
    def prepare(direction, out_html):
        original_prepare(direction, out_html)
        page = out_html.read_text(encoding='utf8')
        page = re.sub(r'(-?\d+(?:\.\d+)?)px', lambda x: f'{float(x[1])*2:g}px', page)
        page = page.replace('data-width="900"', 'data-width="1800"').replace('data-height="250"', 'data-height="500"')
        out_html.write_text(page, encoding='utf8')
    m.prepare_hyperframes = prepare
    cut = inspect.getsource(m.cut_shot)
    substitutions = {
        '1920:1080': '3840:2160', 'flags=fast_bilinear': 'flags=lanczos',
        '780 if vertical else 720': '1560 if vertical else 1440',
        'scale=1080:1920': 'scale=2160:3840', 'scale=1080:608': 'scale=2160:1216',
        'overlay=0:425': 'overlay=0:850', 'overlay=150:1060': 'overlay=300:2120',
        'overlay=58:730': 'overlay=116:1460',
        '"libx264", "-preset", "ultrafast", "-crf", "17"': '"h264_qsv", "-preset", "medium", "-global_quality", "18", "-look_ahead", "0"',
    }
    for a, b in substitutions.items():
        assert a in cut, a
        cut = cut.replace(a, b)
    exec(compile(cut, str(source), 'exec'), m.__dict__)
    # ASS resolution stays in original coordinates; libass rasterizes the vector glyphs at 4K.
    os.chdir(m.BUILD)
    output = DEST / 'QUALIDADE.json'
    manifest = json.loads(output.read_text(encoding='utf8')) if output.exists() else {'items': []}
    manifest.update(method='Project source reexport, native source frames, double-resolution graphics, vector ASS subtitles; no ready-made 1080p MP4 upscale.', source_script_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    write(output, manifest)
    for mode in modes:
        movie = m.render_movie(mode)
        old = ROOT / 'producao/L08/exportacoes' / movie.name
        frames = round((m.SLICES_SHORT if mode == 'short' else m.SLICES_LONG)[-1][1] * 60)
        size = (2160, 3840) if mode == 'short' else (3840, 2160)
        result = validate(movie, old, frames, size)
        result['id'] = 'L08_short' if mode == 'short' else 'L08_longo'
        result['limitations'] = ['Source trailers are 30fps; approved 60fps timing is retained by frame duplication.', 'Vertical export preserves full landscape inside its frame; blurred background is intentionally enlarged.'] if mode == 'short' else ['Source trailers are 30fps; approved 60fps timing is retained by frame duplication.']
        manifest['items'] = [i for i in manifest['items'] if i['id'] != result['id']] + [result]
        write(output, manifest)
        print('VALIDATED ' + str(movie), flush=True)


def especial():
    original = ROOT / 'producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06'
    m = load(original / 'produzir_especial.py')
    m.SCALE = 2
    m.BUILD = DEST / 'legados/especial/montagem'
    m.OUT = DEST / 'legados/especial/exportacoes'
    m.BUILD.mkdir(parents=True, exist_ok=True)
    m.OUT.mkdir(parents=True, exist_ok=True)
    m.PANELS = m.BUILD / 'paineis_short_4k.mov'
    indices = [0, 43, 44, 45, 46, 49]
    m.HF = m.BUILD / 'hyperframes_short_4k'
    if not m.PANELS.exists():
        m.prepare()
        page = m.HF / 'index.html'
        content = page.read_text(encoding='utf8')
        def keep(match):
            section = match[0]
            index = int(re.search(r'id="p(\d+)"', section)[1])
            if index not in indices:
                return ''
            return re.sub(r'data-start="[^"]+"', f'data-start="{indices.index(index)*m.SLOT:.2f}"', section)
        content = re.sub(r'<section\b.*?</section>', keep, content, flags=re.S)
        content = content.replace('data-duration="40.00"', 'data-duration="4.80"')
        assert content.count('<section') == 6
        page.write_text(content, encoding='utf8')
        gsap = original / 'montagem/hyperframes_v2/gsap.min.js'
        (m.HF / 'gsap.min.js').write_bytes(gsap.read_bytes())
        subprocess.run(['hyperframes.cmd', 'render', str(m.HF), '--format', 'mov', '-f', '60', '-o', str(m.PANELS)], cwd=m.BUILD, check=True)
    m.PANEL_INDICES = indices
    cut = inspect.getsource(m.cut).replace('f"{index*SLOT:.2f}"', 'f"{PANEL_INDICES.index(index)*SLOT:.2f}"')
    exec(compile(cut, str(original / 'produzir_especial.py'), 'exec'), m.__dict__)
    render = inspect.getsource(m.render).replace('max_workers=2', 'max_workers=1')
    exec(compile(render, str(original / 'produzir_especial.py'), 'exec'), m.__dict__)
    p = next(s for s in probe(m.PANELS)['streams'] if s['codec_type'] == 'video')
    assert (p['width'], p['height']) == (1800, 500), p
    os.chdir(m.BUILD)
    m.render('short')
    movie = m.OUT / 'Pixel_Procurado_GTA6_Camiseta_Short_V2_4K.mp4'
    old = original / 'exportacoes/Pixel_Procurado_GTA6_Camiseta_Short_V2.mp4'
    frames = int(next(s for s in probe(old)['streams'] if s['codec_type'] == 'video')['nb_frames'])
    result = validate(movie, old, frames, (2160, 3840))
    result['id'] = 'ESPECIAL_PRE_LANCAMENTO_2026-11-06_short'
    result['limitations'] = ['Native 3840x2160 landscape retained in a 2160-wide panel; blurred background is intentionally enlarged.', 'Source trailers are 30fps; approved 60fps timeline is preserved.']
    result['panels_source'] = str(m.PANELS)
    path = DEST / 'QUALIDADE.json'
    manifest = json.loads(path.read_text(encoding='utf8'))
    manifest['items'] = [i for i in manifest['items'] if i['id'] != result['id']] + [result]
    write(path, manifest)
    print('VALIDATED ' + str(movie), flush=True)


def l06():
    # The approved 4K long master is reduced to a 2160-wide panel, never enlarged.
    sys.path.insert(0, str(ROOT / 'automacao'))
    source = ROOT / 'automacao/vertical_l06_social.py'
    m = load(source)
    old = m.VERTICAL
    m.SOCIAL = DEST / 'legados/L06'
    m.VERTICAL = m.SOCIAL / 'L06_Vice_City_Port_Gellhorn_2160x3840.mp4'
    m.SOCIAL.mkdir(parents=True, exist_ok=True)
    native = next(s for s in probe(m.MASTER)['streams'] if s['codec_type'] == 'video')
    assert (native['width'], native['height']) == (3840, 2160)
    code = inspect.getsource(m.main)
    replacements = {
        'scale=1080:608': 'scale=2160:1216', 'crop=1080:{608-args.crop_bottom}': 'crop=2160:{1216-args.crop_bottom*2}',
        'pad=1080:1920:0:580': 'pad=2160:3840:0:1160',
        'fontsize=75:': 'fontsize=150:', 'fontsize=37:': 'fontsize=74:',
        ':y=278:line_spacing=20': ':y=556:line_spacing=40', ':y=1470:line_spacing=12': ':y=2940:line_spacing=24',
        "'libx264', '-preset', 'veryfast', '-crf', '19', '-maxrate', '6M', '-bufsize', '12M'": "'h264_qsv', '-preset', 'medium', '-global_quality', '18', '-look_ahead', '0'",
        "(1080, 1920)": "(2160, 3840)",
        "command(['-v', 'error', '-xerror', '-i', str(temp), '-f', 'null', '-'])": '# Full decode is performed by shared QA below.',
    }
    for a, b in replacements.items():
        assert a in code, a
        code = code.replace(a, b)
    exec(compile(code, str(source), 'exec'), m.__dict__)
    before = sys.argv
    try:
        sys.argv = [str(source)]
        m.main()
    finally:
        sys.argv = before
    reference = probe(old)
    v = next(s for s in reference['streams'] if s['codec_type'] == 'video')
    result = validate(m.VERTICAL, old, int(v['nb_frames']), (2160, 3840), fps=30)
    subtitles = []
    for line in (m.SOCIAL / 'L06_vertical_legendas.ass').read_text(encoding='utf8').splitlines():
        if not line.startswith('Dialogue:'):
            continue
        fields = line.split(',', 9)
        if fields[3] != 'Main':
            continue
        def srt_time(value):
            h, minute, sec = value.split(':')
            return f"{int(h):02}:{minute}:{sec.replace('.', ',')}0"
        subtitles.append(f"{len(subtitles)+1}\n{srt_time(fields[1])} --> {srt_time(fields[2])}\n{fields[9].replace(chr(92)+'N', ' ')}")
    srt = m.VERTICAL.with_suffix('.srt')
    srt.write_text('\n\n'.join(subtitles)+'\n', encoding='utf8')
    result.update(id='L06_short', srt=str(srt), method='Recompose the existing social project from the approved native 4K long master, reducing its width from 3840 to 2160; regenerate vector subtitles and drawtext at final resolution.', limitations=['The native 4K long master contains baked graphics; those remain at native source resolution before reduction.', 'Lower strip containing the old subtitles is removed using the same crop as the approved Short.'])
    path = DEST / 'QUALIDADE.json'
    manifest = json.loads(path.read_text(encoding='utf8'))
    manifest['items'] = [i for i in manifest['items'] if i['id'] != result['id']] + [result]
    write(path, manifest)
    print('VALIDATED ' + str(m.VERTICAL), flush=True)


def catalog():
    path = DEST / 'QUALIDADE.json'
    manifest = json.loads(path.read_text(encoding='utf8'))
    inventory = json.loads((DEST.parent / 'INVENTARIO.json').read_text(encoding='utf8'))['items']
    items = {i['id']: i for i in manifest['items']}
    for i in inventory:
        v = next(s for s in i['probe']['streams'] if s['codec_type'] == 'video')
        if i['id'].endswith('_longo') and (v['width'], v['height']) == (3840, 2160):
            items.setdefault(i['id'], dict(i, path=str((ROOT / i['path']).resolve()), decision='reuse_existing_approved_4k_master', qa_scope='Existing approved project QA retained; no re-render or fresh full decode in this export task.'))
    short_file = DEST / 'shorts/QUALIDADE_SHORTS.json'
    if short_file.exists():
        shorts = json.loads(short_file.read_text(encoding='utf8'))['items']
        for rid, item in shorts.items():
            if item.get('status') == 'validated':
                items[rid + '_short'] = dict(item, id=rid + '_short', probe=probe(Path(item['path'])), limitations=sorted({s['limitation'] for s in item.get('shots', []) if s.get('limitation')}))
    expected = {i['id'] for i in inventory}
    assert set(items) <= expected
    manifest['items'] = [items[i['id']] for i in inventory if i['id'] in items]
    manifest['catalog'] = dict(expected=len(expected), ready=len(items), pending=sorted(expected - items.keys()))
    write(path, manifest)
    print(json.dumps(manifest['catalog'], ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('modes', nargs='*', choices=['long', 'short', 'especial', 'l06', 'catalog'])
    args = parser.parse_args()
    modes = args.modes or ['long', 'short']
    if any(mode in ('long', 'short') for mode in modes):
        l08([mode for mode in modes if mode in ('long', 'short')])
    if 'especial' in modes:
        especial()
    if 'l06' in modes:
        l06()
    if 'catalog' in modes:
        catalog()
