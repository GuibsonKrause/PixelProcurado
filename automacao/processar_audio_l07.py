"""Processamento e alinhamento de áudio determinístico para L07."""
import argparse
import difflib
import json
import re
import sys
import unicodedata
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.production-tools/python'), str(ROOT / '.course-tools')]
import producao

P = ROOT / 'producao/L07/voz'

def norm(t):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', t.lower()))

def save(name, data):
    (P / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')

def metric(path):
    import numpy as np
    with wave.open(str(path)) as w:
        frames = w.readframes(w.getnframes())
        info = dict(file=str(path.relative_to(ROOT)), duration=w.getnframes() / w.getframerate(),
                    sample_rate=w.getframerate(), channels=w.getnchannels(), sample_width=w.getsampwidth(), frames=w.getnframes())
        assert w.getsampwidth() == 2 and w.getnchannels() == 1
    samples = np.frombuffer(frames, dtype='<i2').astype(float) / 32768
    peak = abs(samples).max()
    info['sample_peak_dbfs'] = float(20 * np.log10(peak)) if peak > 0 else -99.0
    info['clipped_samples'] = int((abs(samples) >= 32767 / 32768).sum())
    log = producao.run(['-i', path, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    info['loudnorm'] = json.loads(log[log.rfind('{'):log.rfind('}') + 1])
    log = producao.run(['-i', path, '-af', 'silencedetect=noise=-40dB:d=0.5', '-f', 'null', '-'])
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    if len(starts) > len(ends):
        ends.append(info['duration'])
    info['silences_40db_500ms'] = [dict(start=a, end=b, duration=b - a) for a, b in zip(starts, ends)]
    return info

def normalizar():
    src = P / '03_NARRACAO_narracao.wav'
    dst = P / 'narracao_normalizada.wav'
    if dst.exists():
        dst.unlink()
    print(f"Normalizando {src} -> {dst}...")
    # Normalização EBU R128 (-16 LUFS, True Peak -1.5) sem passar -y pois producao.run já passa -n por padrão
    # Podemos chamar subprocess diretamente com ffmpeg para controle total
    import subprocess, imageio_ffmpeg
    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-nostdin', '-y',
        '-i', str(src),
        '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
        '-ar', '24000',
        str(dst)
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-5000:])
    info = metric(dst)
    save('medicoes_narracao_normalizada.json', info)
    print("Áudio normalizado com sucesso. Duração:", info['duration'])

def transcrever_e_alinhar():
    from faster_whisper import WhisperModel
    import numpy as np

    wav_path = P / 'narracao_normalizada.wav'
    decoded = P / 'temp_16k.raw'
    if decoded.exists():
        decoded.unlink()
    import subprocess, imageio_ffmpeg
    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-nostdin', '-y',
        '-i', str(wav_path),
        '-ar', '16000', '-ac', '1', '-f', 'f32le', str(decoded)
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-5000:])
    samples = np.fromfile(decoded, dtype=np.float32)
    decoded.unlink()

    print("Carregando WhisperModel (small, cpu)...")
    model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4,
                         download_root=str(ROOT / '.course-tools/models'), local_files_only=True)
    
    print("Transcrevendo áudio com timestamps...")
    segments, info = model.transcribe(samples, language='pt', beam_size=1, vad_filter=True, word_timestamps=True)
    
    raw_words = []
    lines = []
    for segment in segments:
        for w in (segment.words or []):
            raw_words.append(dict(word=w.word.strip(), start=round(w.start, 3), end=round(w.end, 3), probability=round(w.probability, 4)))
        lines.append(dict(start=round(segment.start, 3), end=round(segment.end, 3), text=segment.text.strip()))

    save('palavras_asr.json', raw_words)
    save('segmentos_asr.json', lines)
    (P / 'transcricao_asr.txt').write_text('\n'.join(s['text'] for s in lines), encoding='utf8')
    print(f"ASR concluído: {len(raw_words)} palavras detectadas.")

    # Alinhar com o roteiro oficial 01_NARRACAO.txt
    paragraphs = (P.parent / '01_NARRACAO.txt').read_text(encoding='utf8').strip().split('\n\n')
    ref = [dict(word=t, paragraph=i + 1) for i, p in enumerate(paragraphs) for t in p.split()]
    aligned = []
    review = []

    for tag, i, j, k, l in difflib.SequenceMatcher(None, [norm(w['word']) for w in raw_words], [norm(w['word']) for w in ref], autojunk=False).get_opcodes():
        if tag == 'equal':
            for ai, ri in zip(range(i, j), range(k, l)):
                aligned.append({**ref[ri], **{key: raw_words[ai][key] for key in ('start', 'end')}, 'status': 'asr_exact', 'asr_word': raw_words[ai]['word']})
        else:
            start = raw_words[i]['start'] if i < len(raw_words) else (raw_words[-1]['end'] if raw_words else 0.0)
            end = raw_words[j - 1]['end'] if j > i else start
            if end <= start:
                end = min((raw_words[-1]['end'] if raw_words else start + 1.0), start + 0.05)
            recognized = ' '.join(w['word'] for w in raw_words[i:j])
            script = ' '.join(w['word'] for w in ref[k:l])
            review.append(dict(kind=tag, start=start, end=end, asr=recognized, script=script))
            for ri in range(k, l):
                aligned.append({
                    **ref[ri],
                    'start': round(start + (end - start) * (ri - k) / max(1, l - k), 3),
                    'end': round(start + (end - start) * (ri - k + 1) / max(1, l - k), 3),
                    'status': 'asr_ambiguity_estimated',
                    'asr_span': recognized
                })

    for i, w in enumerate(aligned):
        if w['end'] <= w['start']:
            w['start'] = max(0.0, w['end'] - 0.03)
            if i > 0:
                aligned[i - 1]['end'] = min(aligned[i - 1]['end'], w['start'])

    assert len(aligned) == len(ref), f"Alinhamento incompleto: {len(aligned)} != {len(ref)}"
    save('palavras_alinhadas.json', aligned)
    save('revisao_alinhamento.json', review)

    par_list = []
    for n, p in enumerate(paragraphs, 1):
        matching = [w for w in aligned if w['paragraph'] == n]
        if matching:
            par_list.append(dict(paragraph=n, start=matching[0]['start'], end=matching[-1]['end'], text=p))
    save('paragrafos_alinhados.json', par_list)
    print(f"Alinhamento concluído com sucesso: {len(aligned)} palavras, {len(par_list)} parágrafos.")

if __name__ == '__main__':
    normalizar()
    transcrever_e_alinhar()
