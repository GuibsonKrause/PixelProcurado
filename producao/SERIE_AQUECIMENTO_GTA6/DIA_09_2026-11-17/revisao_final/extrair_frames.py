"""Extrai frames reduzidos (um arquivo por timecode) e monta pranchas para inspecao.
uso: py -3.12 extrair_frames.py <video> <pasta_saida> <prefixo> <largura> t1 t2 ...
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

video, out, pref, larg = sys.argv[1], Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
tcs = [float(x) for x in sys.argv[5:]]
out.mkdir(parents=True, exist_ok=True)
arqs = []
for t in tcs:
    f = out / f'{pref}_{t:07.2f}.jpg'
    if not f.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1',
                        '-vf', f'scale={larg}:-2', '-q:v', '3', str(f)], check=True)
    arqs.append((t, f))
# pranchas 3x3 para leitura
ims = [(t, Image.open(f)) for t, f in arqs]
w, h = ims[0][1].size
for k in range(0, len(ims), 9):
    lote = ims[k:k + 9]
    pr = Image.new('RGB', (w * 3, h * ((len(lote) + 2) // 3)), 'black')
    for j, (t, im) in enumerate(lote):
        pr.paste(im, ((j % 3) * w, (j // 3) * h))
        d = ImageDraw.Draw(pr)
        d.rectangle([(j % 3) * w, (j // 3) * h, (j % 3) * w + 110, (j // 3) * h + 26], fill='red')
        d.text(((j % 3) * w + 4, (j // 3) * h + 4), f'{t:.2f}s', fill='white')
    pr.save(out.parent / f'prancha_{pref}_{k // 9:02d}.jpg', quality=85)
print(len(arqs), 'frames')
