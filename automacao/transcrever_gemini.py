import os
import json
from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # try user env
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
        api_key, _ = winreg.QueryValueEx(key, "GEMINI_API_KEY")
    except Exception:
        pass

client = genai.Client(api_key=api_key)

audio_path = r"producao/starlink/audio_original.wav"

print(f"Uploading {audio_path} to Gemini Files API...", flush=True)
audio_file = client.files.upload(file=audio_path)
print(f"File uploaded: {audio_file.name}", flush=True)

prompt = """Você é um assistente de edição de vídeo profissional.
Ouça o áudio completo deste vídeo onde uma pessoa fala sobre a Starlink e a promoção da mensalidade.

Transcreva o áudio de forma completa e estruturada, dividindo em frases com os timecodes (início e fim em segundos) aproximados de cada fala.
Formate a resposta como um JSON válido contendo:
{
  "full_transcript": "texto completo...",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "fala..."
    }
  ],
  "summary": "resumo do que é falado e quais os números/preços mencionados",
  "suggested_cuts_for_90s": [
    {
      "part": 1,
      "start": 0.0,
      "end": ...,
      "reason": "..."
    }
  ]
}
Responda APENAS com o JSON válido.
"""

print("Generating transcription with Gemini 3.8 Flash...", flush=True)
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[audio_file, prompt]
)

print("Transcription response received:", flush=True)
output_text = response.text.strip()
if output_text.startswith("```json"):
    output_text = output_text[7:]
if output_text.endswith("```"):
    output_text = output_text[:-3]

with open("producao/starlink/transcricao_gemini.json", "w", encoding="utf-8") as f:
    f.write(output_text.strip())

print("Saved to producao/starlink/transcricao_gemini.json", flush=True)
