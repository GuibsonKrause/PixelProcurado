import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

with open(ROOT / '01_NARRACAO.txt', encoding='utf-8') as f:
    paragraphs = [p.strip() for p in f.read().split('\n\n') if p.strip()]

with open(ROOT / 'voz/alinhamento_palavras.json', encoding='utf-8') as f:
    words = json.load(f)

print(f"Total paragrafos: {len(paragraphs)}")
idx = 0
results = []
for i, p in enumerate(paragraphs, 1):
    first_words = [w.strip('.,!?:;"\'').lower() for w in p.split()[:3]]
    found_time = None
    for w_idx in range(idx, len(words) - len(first_words) + 1):
        match = True
        for k in range(len(first_words)):
            if words[w_idx + k]['word'].strip('.,!?:;"\'').lower() != first_words[k]:
                match = False
                break
        if match:
            found_time = words[w_idx]['start']
            idx = w_idx + 1
            break
    if found_time is None:
        # fallback search
        target = first_words[0]
        for w_idx in range(idx, len(words)):
            if words[w_idx]['word'].strip('.,!?:;"\'').lower() == target:
                found_time = words[w_idx]['start']
                idx = w_idx + 1
                break
    results.append((i, found_time, p))
    print(f"P{i:02d}: {found_time}s | {p[:50]}...")
