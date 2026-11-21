import os
import sys
import json
import subprocess

video_path = "producao/starlink/STARLINK_PROMOCAO_FINAL_MAX_QUALITY.mp4"
qa_dir = "producao/starlink/qa"
os.makedirs(qa_dir, exist_ok=True)

# 1. FFprobe verification
cmd_probe = [
    "ffprobe", "-v", "error",
    "-show_format", "-show_streams",
    "-print_format", "json",
    video_path
]
res = subprocess.run(cmd_probe, capture_output=True, text=True, check=True)
info = json.loads(res.stdout)

dur = float(info["format"]["duration"])
size_mb = os.path.getsize(video_path) / (1024 * 1024)
print(f"=== QA VERIFICATION ===")
print(f"File: {video_path}")
print(f"Size: {size_mb:.2f} MB")
print(f"Duration: {dur:.2f}s (Target <= 90s: {'PASS' if dur <= 90.0 else 'FAIL'})")

for s in info["streams"]:
    c_type = s["codec_type"]
    c_name = s["codec_name"]
    w = s.get("width")
    h = s.get("height")
    r_frame = s.get("r_frame_rate")
    print(f"Stream {c_type}: {c_name} {w}x{h} @ {r_frame}")

# 2. Full decode test (corruption check)
print("\nRunning full decode test...")
cmd_decode = [
    "ffmpeg", "-v", "error",
    "-i", video_path,
    "-f", "null", "-"
]
res_dec = subprocess.run(cmd_decode, capture_output=True, text=True)
if res_dec.stderr.strip():
    print(f"Decode warnings/errors: {res_dec.stderr}")
else:
    print("Full decode test: 100% CLEAN, ZERO CORRUPTION!")

# 3. Sample frames generation for visual QA
timestamps = [2.0, 5.0, 15.0, 24.0, 33.0, 44.0, 54.0, 70.0, 80.0, 85.0]
for t in timestamps:
    out_frame = f"{qa_dir}/frame_{int(t):02d}s.jpg"
    cmd_frame = [
        "ffmpeg", "-y",
        "-ss", str(t),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        out_frame
    ]
    subprocess.run(cmd_frame, check=True)
    print(f"Sample frame at {t:4.1f}s saved: {out_frame}")

print("\nQA check completed successfully!")
