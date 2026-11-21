import subprocess
import os

os.makedirs("producao/starlink/testes", exist_ok=True)

# Test 1: Direct frame extraction
cmd1 = [
    "ffmpeg", "-y",
    "-ss", "00:00:03",
    "-i", r"C:\Users\guibson.krause\Downloads\IMG_3177.MOV",
    "-vframes", "1",
    "producao/starlink/testes/frame_direto.jpg"
]
subprocess.run(cmd1, check=True)

# Test 2: Tone mapped with colormatrix/tonemap to bt709
cmd2 = [
    "ffmpeg", "-y",
    "-ss", "00:00:03",
    "-i", r"C:\Users\guibson.krause\Downloads\IMG_3177.MOV",
    "-vf", "zscale=t=linear:npl=100,tonemap=tonemap=hable:desat=0,zscale=p=709:t=709:m=709:r=limited,format=yuv420p",
    "-vframes", "1",
    "producao/starlink/testes/frame_tonemapped.jpg"
]
try:
    subprocess.run(cmd2, check=True)
    print("Tonemap supported!", flush=True)
except Exception as e:
    print(f"Tonemap test error: {e}", flush=True)

print("Frame tests generated.", flush=True)
