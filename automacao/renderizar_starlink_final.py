import os
import sys
import json
import subprocess

sys.path.extend([
    os.path.abspath(".course-tools"),
    os.path.abspath(".production-tools/python")
])

input_mov = r"C:\Users\guibson.krause\Downloads\IMG_3177.MOV"
output_dir = "producao/starlink"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(f"{output_dir}/parts", exist_ok=True)

# 1. Cuts definition
clips_def = [
    (0.00, 10.20, "clip_01"),
    (11.15, 28.50, "clip_02"),
    (29.20, 39.50, "clip_03"),
    (40.50, 51.10, "clip_04"),
    (51.85, 64.65, "clip_05"),
    (64.65, 80.46, "clip_06"),
    (115.65, 122.50, "clip_07"),
    (138.70, 141.00, "clip_08"),
]

print("--- Step 1: Extracting and mapping subtitle timestamps ---", flush=True)
with open(f"{output_dir}/whisper_exato.json", "r", encoding="utf-8") as f:
    raw_segments = json.load(f)

# Map whisper words to new timeline
new_segments = []
cum_time = 0.0

for start_src, end_src, clip_id in clips_def:
    clip_dur = end_src - start_src
    for seg in raw_segments:
        # Check if segment overlaps with this cut
        s_start = seg["start"]
        s_end = seg["end"]
        if s_end > start_src and s_start < end_src:
            # Map words
            mapped_words = []
            for w in seg.get("words", []):
                w_s = w["start"]
                w_e = w["end"]
                if w_e >= start_src and w_s <= end_src:
                    n_s = max(0.0, cum_time + (w_s - start_src))
                    n_e = min(cum_time + clip_dur, cum_time + (w_e - start_src))
                    mapped_words.append({
                        "word": w["word"],
                        "start": round(n_s, 2),
                        "end": round(n_e, 2)
                    })
            if mapped_words:
                text = "".join(w["word"] for w in mapped_words).strip()
                new_segments.append({
                    "start": mapped_words[0]["start"],
                    "end": mapped_words[-1]["end"],
                    "text": text,
                    "words": mapped_words
                })
    cum_time += clip_dur

total_timeline_duration = cum_time
print(f"Total edited duration: {total_timeline_duration:.2f}s (under 90s target!)", flush=True)

# Generate ASS Subtitles
ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Segoe UI,54,&H00FFFFFF,&H000000FF,&H0012161C,&H80000000,-1,0,0,0,100,100,0,0,1,5,3,2,60,60,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def format_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def format_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

ass_events = []
srt_events = []

# Group words into clean short subtitle phrases (3-7 words per line)
phrase_words = []
phrase_start = 0.0
srt_idx = 1

for seg in new_segments:
    for w in seg["words"]:
        if not phrase_words:
            phrase_start = w["start"]
        phrase_words.append(w)
        # Break phrase on punctuation or when reached 5 words
        word_text = w["word"].strip()
        has_break = any(p in word_text for p in [".", ",", "!", "?"]) or len(phrase_words) >= 5
        if has_break:
            phrase_end = w["end"]
            p_text = "".join(pw["word"] for pw in phrase_words).strip()
            # Highlight key pricing words in yellow
            ass_text = p_text
            for kw in ["Starlink", "30%", "desconto", "R$249", "R$174", "R$49", "R$189", "R$132", "R$339", "R$237,30", "R$619", "R$433,30", "R$200", "garantida", "agora"]:
                if kw in ass_text:
                    ass_text = ass_text.replace(kw, f"{{\\c&H3DD3FF&}}{kw}{{\\c&HFFFFFF&}}")
            
            ass_line = f"Dialogue: 0,{format_ass_time(phrase_start)},{format_ass_time(phrase_end)},Default,,0,0,0,,{ass_text}"
            ass_events.append(ass_line)
            
            srt_line = f"{srt_idx}\n{format_srt_time(phrase_start)} --> {format_srt_time(phrase_end)}\n{p_text}\n"
            srt_events.append(srt_line)
            srt_idx += 1
            phrase_words = []

if phrase_words:
    phrase_end = phrase_words[-1]["end"]
    p_text = "".join(pw["word"] for pw in phrase_words).strip()
    ass_line = f"Dialogue: 0,{format_ass_time(phrase_start)},{format_ass_time(phrase_end)},Default,,0,0,0,,{p_text}"
    ass_events.append(ass_line)
    srt_line = f"{srt_idx}\n{format_srt_time(phrase_start)} --> {format_srt_time(phrase_end)}\n{p_text}\n"
    srt_events.append(srt_line)

ass_path = f"{output_dir}/legendas.ass"
srt_path = f"{output_dir}/legendas.srt"

with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ass_header + "\n".join(ass_events))
with open(srt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(srt_events))

print(f"Generated subtitles:\n  {ass_path}\n  {srt_path}", flush=True)

# 2. Extract and pre-render trimmed clips with audio denoiser
print("\n--- Step 2: Extracting trimmed clips and cleaning audio ---", flush=True)
concat_txt_path = f"{output_dir}/concat_list.txt"
concat_entries = []

audio_filter = (
    "highpass=f=80,"
    "afftdn=nr=18:nf=-35:tn=1:gs=8,"
    "equalizer=f=250:t=q:w=1.0:g=-3,"
    "equalizer=f=3200:t=q:w=1.5:g=3.5,"
    "acompressor=threshold=-18dB:ratio=3:attack=5:release=50,"
    "loudnorm=I=-16:TP=-1.5:LRA=11"
)

video_tonemap = (
    "zscale=t=linear:npl=100,"
    "tonemap=tonemap=hable:desat=0,"
    "zscale=p=709:t=709:m=709:r=limited,"
    "format=yuv420p"
)

for i, (s_start, s_end, cid) in enumerate(clips_def):
    part_path = f"{output_dir}/parts/part_{i+1:02d}.mp4"
    part_dur = s_end - s_start
    print(f"Rendering {cid} ({part_dur:.2f}s) from {s_start:.2f}s to {s_end:.2f}s...", flush=True)
    
    cmd_part = [
        "ffmpeg", "-y",
        "-ss", f"{s_start:.3f}",
        "-t", f"{part_dur:.3f}",
        "-i", input_mov,
        "-vf", video_tonemap,
        "-af", audio_filter,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        part_path
    ]
    subprocess.run(cmd_part, check=True)
    concat_entries.append(f"file 'parts/part_{i+1:02d}.mp4'")

with open(concat_txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(concat_entries))

# Concat trimmed parts into base cut
print("\n--- Step 3: Concatenating trimmed base video ---", flush=True)
base_cut_path = f"{output_dir}/base_cortada.mp4"
cmd_concat = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_txt_path,
    "-c", "copy",
    base_cut_path
]
subprocess.run(cmd_concat, check=True)
print(f"Base video assembled at {base_cut_path}", flush=True)

# 3. Final Composite: Add Cards with Animated Transitions and Subtitles
print("\n--- Step 4: Final Composition with Animated Cards & Subtitles ---", flush=True)
# Cards schedule on final timeline:
cards_schedule = [
    ("cards/card_01_hook.png", 0.4, 7.5),
    ("cards/card_02_max.png", 10.6, 26.8),
    ("cards/card_03_100mega.png", 27.8, 37.2),
    ("cards/card_04_viagem100.png", 38.2, 47.8),
    ("cards/card_05_viagem_ilim.png", 48.8, 60.5),
    ("cards/card_06_regras.png", 61.6, 76.5),
    ("cards/card_07_bonus.png", 77.1, 83.5),
    ("cards/card_08_cta.png", 83.8, 86.1),
]

final_output = f"{output_dir}/STARLINK_PROMOCAO_FINAL_MAX_QUALITY.mp4"

# Build filter_complex
input_args = ["-i", base_cut_path]
filter_parts = []
prev_layer = "[0:v]"

for idx, (c_rel, t_in, t_out) in enumerate(cards_schedule):
    c_full = os.path.join(output_dir, c_rel).replace("\\", "/")
    input_args.extend(["-loop", "1", "-t", f"{t_out - t_in + 1.0:.2f}", "-i", c_full])
    input_idx = idx + 1
    
    # Fade in over 0.3s, fade out over 0.25s
    d_in = 0.30
    d_out = 0.25
    fade_out_start = (t_out - t_in) - d_out
    card_proc = f"[{input_idx}:v]format=rgba,fade=in:st=0:d={d_in}:alpha=1,fade=out:st={fade_out_start:.2f}:d={d_out}:alpha=1[c_fade_{idx}]"
    filter_parts.append(card_proc)
    
    next_layer = f"[v_comp_{idx}]" if idx < len(cards_schedule) - 1 else "[v_with_cards]"
    overlay_expr = f"{prev_layer}[c_fade_{idx}]overlay=0:0:enable='between(t,{t_in:.2f},{t_out:.2f})'{next_layer}"
    filter_parts.append(overlay_expr)
    prev_layer = next_layer

# Add ASS Subtitles
# Escaping for filter
ass_escaped = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
filter_parts.append(f"[v_with_cards]ass='{ass_escaped}'[v_final]")

filter_complex_str = ";".join(filter_parts)

cmd_final = [
    "ffmpeg", "-y"
] + input_args + [
    "-filter_complex", filter_complex_str,
    "-map", "[v_final]",
    "-map", "0:a",
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "17",
    "-pix_fmt", "yuv420p",
    "-c:a", "copy",
    "-movflags", "+faststart",
    final_output
]

print("Running final render...", flush=True)
subprocess.run(cmd_final, check=True)
print(f"\n==========================================", flush=True)
print(f"MASTER RENDER COMPLETE: {final_output}", flush=True)
print(f"==========================================", flush=True)
