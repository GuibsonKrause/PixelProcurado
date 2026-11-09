from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import sys
import wave
from pathlib import Path

from google import genai


DEFAULT_MODEL = "gemini-3.8-flash-tts"
DEFAULT_VOICE = "voice_iagtq1gnk2br"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera narracao WAV com uma voz personalizada do Gemini TTS."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Arquivos de roteiro. Ex.: producao/cortes/C02_GEMINI.txt",
    )
    parser.add_argument(
        "--all-shorts",
        action="store_true",
        help="Gera todos os arquivos C*_GEMINI.txt de producao/cortes.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument(
        "--style-file",
        type=Path,
        default=Path("producao/cortes/00_ESTILO_GEMINI_SHORTS.txt"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("producao/cortes/audio_gemini"),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida arquivos e mostra a configuracao sem chamar a API.",
    )
    return parser.parse_args()


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def collect_inputs(root: Path, args: argparse.Namespace) -> list[Path]:
    files = [resolve(root, item) for item in args.inputs]
    if args.all_shorts:
        files.extend(sorted((root / "producao" / "cortes").glob("C*_GEMINI.txt")))
    unique: list[Path] = []
    seen: set[Path] = set()
    for item in files:
        normalized = item.resolve()
        if normalized not in seen:
            unique.append(normalized)
            seen.add(normalized)
    if not unique:
        raise ValueError("Informe um roteiro ou use --all-shorts.")
    missing = [str(item) for item in unique if not item.is_file()]
    if missing:
        raise FileNotFoundError("Roteiro nao encontrado: " + ", ".join(missing))
    return unique


def decode_audio(data: object) -> bytes:
    if isinstance(data, bytes):
        return data
    if data is None:
        raise RuntimeError("A resposta do Gemini nao trouxe dados de audio.")
    encoded = str(data)
    try:
        return base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise RuntimeError("O audio retornado nao esta em base64 valido.") from exc


def pcm_to_wav(raw: bytes, sample_rate: int, channels: int) -> bytes:
    import io

    target = io.BytesIO()
    with wave.open(target, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(raw)
    return target.getvalue()


def generate(
    client: genai.Client,
    transcript: str,
    style: str,
    model: str,
    voice: str,
) -> tuple[bytes, str, int, int]:
    interaction = client.interactions.create(
        model=model,
        input=[
            {
                "type": "user_input",
                "content": [
                    {
                        "type": "text",
                        "text": transcript,
                        "annotations": [
                            {"type": "speech_metadata", "style": style}
                        ],
                    }
                ],
            }
        ],
        response_format={"type": "audio"},
        generation_config={"speech_config": [{"voice": voice}]},
        timeout=300,
    )
    audio = interaction.output_audio
    if audio is None:
        raise RuntimeError("O Gemini concluiu a requisicao sem retornar audio.")
    mime_type = str(audio.mime_type or "audio/wav").lower()
    sample_rate = int(audio.sample_rate or 24000)
    channels = int(audio.channels or 1)
    raw = decode_audio(audio.data)
    if mime_type.startswith("audio/l16") and not raw.startswith(b"RIFF"):
        raw = pcm_to_wav(raw, sample_rate, channels)
        mime_type = "audio/wav"
    if not raw.startswith(b"RIFF"):
        raise RuntimeError(f"Formato inesperado: {mime_type}. Era esperado WAV.")
    return raw, mime_type, sample_rate, channels


def main() -> int:
    args = parse_args()
    root = project_root()
    try:
        inputs = collect_inputs(root, args)
        style_path = resolve(root, args.style_file).resolve()
        output_dir = resolve(root, args.output_dir).resolve()
        style = style_path.read_text(encoding="utf-8").strip()
        if not style:
            raise ValueError(f"O arquivo de estilo esta vazio: {style_path}")
        transcripts = [(path, path.read_text(encoding="utf-8").strip()) for path in inputs]
        empty = [str(path) for path, text in transcripts if not text]
        if empty:
            raise ValueError("Roteiro vazio: " + ", ".join(empty))

        summary = {
            "model": args.model,
            "voice": args.voice,
            "language": "pt-BR (definido pela voz, pelo estilo e pelo texto)",
            "style_file": str(style_path),
            "output_dir": str(output_dir),
            "inputs": [str(path) for path, _ in transcripts],
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        if args.dry_run:
            print("Validacao concluida; nenhuma chamada foi enviada a API.")
            return 0

        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY nao esta configurada. Execute "
                "automacao/configurar_chave_gemini.ps1 primeiro."
            )

        output_dir.mkdir(parents=True, exist_ok=True)
        client = genai.Client(api_key=api_key)
        for index, (path, transcript) in enumerate(transcripts, start=1):
            output = output_dir / f"{path.stem.replace('_GEMINI', '')}_narracao.wav"
            print(f"[{index}/{len(transcripts)}] Gerando {path.name}...")
            audio, mime_type, sample_rate, channels = generate(
                client, transcript, style, args.model, args.voice
            )
            temporary = output.with_suffix(".wav.part")
            temporary.write_bytes(audio)
            temporary.replace(output)
            print(
                f"Salvo: {output} | {mime_type} | "
                f"{sample_rate} Hz | {channels} canal(is) | {len(audio)} bytes"
            )
        return 0
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
