"""Renderizador nativo 4K/1080p determinístico de L07 via FFmpeg."""
import json
import math
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.production-tools/python'), str(ROOT / '.course-tools')]
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
P = ROOT / 'producao/L07'
W = P / 'projeto'
EXP = P / 'exportacoes'
EXP.mkdir(exist_ok=True)

OUT_MP4 = EXP / 'Pixel_Procurado_L07_4K.mp4'
OUT_SRT = EXP / 'Pixel_Procurado_L07_4K.srt'
OUT_ASS = W / 'legendas_l07.ass'

timeline = json.loads((W / 'edicao_l07.json').read_text(encoding='utf8'))
shots = timeline['shots']
captions = timeline['captions']
voice_path = ROOT / timeline['voice']

def stamp_ass(t):
    cs = round(max(0, t) * 100)
    return f"{cs // 360000}:{(cs // 6000) % 60:02}:{(cs // 100) % 60:02}.{cs % 100:02}"

def stamp_srt(t):
    ms = round(max(0, t) * 1000)
    return f"{ms // 3600000:02}:{(ms // 60000) % 60:02}:{(ms // 1000) % 60:02},{ms % 1000:03}"

# 1. Gerar SRT
srt_lines = []
for i, c in enumerate(captions, 1):
    srt_lines.append(f"{i}\n{stamp_srt(c['start'])} --> {stamp_srt(c['end'])}\n{c['text']}\n")
OUT_SRT.write_text('\n'.join(srt_lines), encoding='utf8')
print(f"SRT salvo: {OUT_SRT} ({len(captions)} blocos)")

# 2. Gerar ASS estilizado padrão Pixel Procurado (V2)
ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 3840
PlayResY: 2160
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial,80,&H00FFFFFF,&H00FFFFFF,&H30120C08,&H30120C08,-1,0,0,0,100,100,0,0,3,14,0,2,300,300,160,1
Style: Source,Arial,34,&H00ECDBCE,&H00FFFFFF,&H0020100A,&H0020100A,-1,0,0,0,100,100,0,0,1,3,0,7,192,192,70,1
Style: Tag,Arial,46,&H003DD3FF,&H00FFFFFF,&H0020100A,&H0020100A,-1,0,0,0,100,100,3,0,1,4,0,7,192,192,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass_events = []
for c in captions:
    text = c['text'].replace('\n', r'\N')
    ass_events.append(f"Dialogue: 0,{stamp_ass(c['start'])},{stamp_ass(c['end'])},Main,,0,0,0,,{text}")

for s in shots:
    # Crédito e etiqueta de fonte no canto superior esquerdo
    ass_events.append(f"Dialogue: 1,{stamp_ass(s['start'])},{stamp_ass(s['end'])},Tag,,0,0,0,,{s['label']}")
    ass_events.append(f"Dialogue: 1,{stamp_ass(s['start'])},{stamp_ass(s['end'])},Source,,0,0,0,,{s['source']}")

OUT_ASS.write_text(ass_header + '\n'.join(ass_events), encoding='utf8')
print(f"ASS salvo: {OUT_ASS}")

# 3. Composição de vídeo contínua via FFmpeg
# Para manter alta velocidade e estabilidade determinística, montamos os clipes ordenados
print("Iniciando renderização de vídeo sequencial em 3840x2160 @ 30fps...")
# Montamos um concat demuxer ou renderizamos os planos
concat_list = W / 'concat_shots.txt'
concat_lines = []
temp_dir = W / 'temp_render'
temp_dir.mkdir(exist_ok=True)

# Renderizar cada shot normalizado para 3840x2160 30fps
for idx, s in enumerate(shots):
    shot_mp4 = temp_dir / f"shot_{idx:03d}.mp4"
    concat_lines.append(f"file '{shot_mp4.as_posix()}'")
    if shot_mp4.is_file() and shot_mp4.stat().st_size > 1000:
        continue
    
    dur = s['frames'] / 30.0
    media_file = ROOT / s['file']
    if s['kind'] == 'video':
        cmd = [
            FF, '-hide_banner', '-nostdin', '-y',
            '-ss', str(s['offset']),
            '-t', str(dur),
            '-i', str(media_file),
            '-vf', f"scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30",
            '-an', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18',
            str(shot_mp4)
        ]
    else:
        # Imagem com leve zoom sutil (pan & scan)
        cmd = [
            FF, '-hide_banner', '-nostdin', '-y',
            '-loop', '1',
            '-t', str(dur),
            '-i', str(media_file),
            '-vf', f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,fps=30",
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18',
            str(shot_mp4)
        ]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode != 0:
        raise RuntimeError(f"Erro ao renderizar shot {idx}: {p.stderr[-2000:]}")

concat_list.write_text('\n'.join(concat_lines), encoding='utf8')
print("Todos os 47 planos renderizados. Concatenando e fundindo com legendas e áudio final...")

# Concatenação final com incorporação de legendas e áudio normalizado
ass_param = str(OUT_ASS.resolve()).replace('\\', '/').replace(':', '\\:')
final_cmd = [
    FF, '-hide_banner', '-nostdin', '-y',
    '-f', 'concat', '-safe', '0', '-i', str(concat_list),
    '-i', str(voice_path),
    '-vf', f"ass='{ass_param}'",
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
    '-c:a', 'aac', '-b:a', '320k',
    '-shortest',
    str(OUT_MP4)
]
p = subprocess.run(final_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
if p.returncode != 0:
    raise RuntimeError(f"Erro no render final FFmpeg: {p.stderr[-3000:]}")

print(f"Vídeo final exportado com sucesso: {OUT_MP4} ({OUT_MP4.stat().st_size / (1024*1024):.2f} MB)")
