import json
import subprocess
import os
import sys

mov_path = r"C:\Users\guibson.krause\Downloads\IMG_3177.MOV"
output_json = r"producao/starlink_probe.json"

os.makedirs("producao", exist_ok=True)

print(f"Checking {mov_path}: exists = {os.path.exists(mov_path)}")
if os.path.exists(mov_path):
    print(f"Size: {os.path.getsize(mov_path)} bytes")

# Run ffprobe
cmd = [
    "ffprobe",
    "-v", "error",
    "-show_format",
    "-show_streams",
    "-print_format", "json",
    mov_path
]

try:
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    probe = json.loads(res.stdout)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(probe, f, indent=2)
    print("Probe written successfully.")
    
    # Print summary
    for s in probe.get("streams", []):
        codec_type = s.get("codec_type")
        codec_name = s.get("codec_name")
        width = s.get("width")
        height = s.get("height")
        duration = s.get("duration") or probe.get("format", {}).get("duration")
        rotation = s.get("tags", {}).get("rotate")
        print(f"Stream {codec_type}: {codec_name}, {width}x{height}, duration: {duration}s, rotate: {rotation}")
except Exception as e:
    print(f"Error running ffprobe: {e}")
