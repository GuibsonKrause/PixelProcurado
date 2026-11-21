import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
with open(ROOT / 'voz/alinhamento_palavras.json', encoding='utf-8') as f:
    words = json.load(f)

# Agrupar por sentenças ou blocos de 15 segundos
current_t = 0
chunk = []
for w in words:
    chunk.append(w['word'])
    if w['end'] - current_t >= 15 or w['word'].endswith('.'):
        if w['end'] - current_t >= 10:
            print(f"[{current_t:06.2f} - {w['end']:06.2f}] {' '.join(chunk)}")
            current_t = w['end']
            chunk = []
if chunk:
    print(f"[{current_t:06.2f} - {words[-1]['end']:06.2f}] {' '.join(chunk)}")
