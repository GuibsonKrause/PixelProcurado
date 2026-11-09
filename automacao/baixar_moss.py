"""Baixa cópias reais dos pesos MOSS para evitar links quebrados no Windows."""
import json
from pathlib import Path
from huggingface_hub import snapshot_download

root = Path(__file__).resolve().parent.parent / ".production-tools" / "models"
root.mkdir(parents=True, exist_ok=True)
items = [
    ("OpenMOSS-Team/MOSS-TTS-Nano", "44502f80dbf9743528fa921cc544d662c685ebec", root / "MOSS-TTS-Nano"),
    ("OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano", None, root / "MOSS-Audio-Tokenizer-Nano"),
]
result = {}
for repo, revision, dest in items:
    path = snapshot_download(repo_id=repo, revision=revision, local_dir=dest)
    result[repo] = {"path": path, "revision_requested": revision}
(root / "moss-download.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2), flush=True)
