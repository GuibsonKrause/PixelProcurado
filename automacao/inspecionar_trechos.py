import subprocess
import os

# Let's inspect the last 60 seconds with silencedetect or export segments to inspect
script = """
import json

with open("producao/starlink/transcricao_gemini.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for s in data["segments"]:
    print(f"[{s['start']:6.1f} -> {s['end']:6.1f}] {s['text']}")
"""

print(script)
