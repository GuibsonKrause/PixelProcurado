"""Fila segura dos Shorts do Pixel Procurado para o Postiz self-hosted.

Por padrão este programa apenas valida e mostra o plano. Upload e criação de
rascunho exigem o comando ``draft``. Um agendamento que poderá chegar ao
YouTube exige, além disso, ``--confirm-youtube``. A troca segura de um
rascunho antigo por uma produção nova usa ``replace-schedule``.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "producao" / "shorts"
CONTROL = BASE / "CONTROLE_DE_PUBLICACAO.csv"
STATE_FILE = BASE / "POSTIZ_ESTADO.json"
ENV_FILE = ROOT / ".env.postiz.local"
TIMEZONE = datetime.now().astimezone().tzinfo
API_URL = "http://localhost:4007/api"

MAIN_ORDER = [
    "C03", "C08", "C02", "C11", "C12", "C09",
    "C04", "C07", "C06", "C05", "C01", "C10",
]
RESERVES = ["L01-R02", "L01-R03"]


class PostizError(RuntimeError):
    pass


def load_env() -> None:
    """Carrega somente chaves simples do arquivo local ignorado pelo Git."""
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    if os.name == "nt":
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                for name in ("POSTIZ_API_KEY", "POSTIZ_API_URL"):
                    if name not in os.environ:
                        value, _ = winreg.QueryValueEx(key, name)
                        os.environ[name] = str(value)
        except (FileNotFoundError, OSError):
            pass


def read_rows() -> dict[str, dict[str, str]]:
    with CONTROL.open(encoding="utf-8-sig", newline="") as handle:
        return {row["id"]: row for row in csv.DictReader(handle)}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def item_data(short_id: str, row: dict[str, str]) -> dict[str, object]:
    folder = BASE / short_id
    publication = folder / "publicacao"
    video = BASE / row["file"]
    thumbnail = publication / "capa_youtube.jpg"
    title = read_text(publication / "01_TITULO.txt")
    description = read_text(publication / "02_DESCRICAO.txt")
    tags = [tag.strip() for tag in read_text(publication / "04_TAGS.txt").split(",") if tag.strip()]
    comment = read_text(publication / "03_COMENTARIO_FIXADO.txt")

    errors: list[str] = []
    if row["status"] != "validado":
        errors.append(f"estado é {row['status']!r}, não 'validado'")
    if not video.is_file():
        errors.append(f"vídeo ausente: {video}")
    if not thumbnail.is_file():
        errors.append(f"capa ausente: {thumbnail}")
    if not 2 <= len(title) <= 100:
        errors.append(f"título tem {len(title)} caracteres (limite 2–100)")
    if len(description) > 5000:
        errors.append(f"descrição tem {len(description)} caracteres (limite 5000)")
    if len(",".join(tags)) > 500:
        errors.append("tags ultrapassam 500 caracteres")
    if errors:
        raise PostizError(short_id + ": " + "; ".join(errors))

    return {
        "id": short_id,
        "title": title,
        "description": description,
        "tags": tags,
        "comment": comment,
        "video": video,
        "thumbnail": thumbnail,
        "duration": float(row["duration"]),
    }


def select_ids(raw: str | None, include_reserves: bool) -> list[str]:
    if raw:
        selected = [part.strip().upper() for part in raw.split(",") if part.strip()]
    else:
        selected = MAIN_ORDER.copy()
        if include_reserves:
            selected.extend(RESERVES)
    unknown = [short_id for short_id in selected if short_id not in MAIN_ORDER + RESERVES]
    if unknown:
        raise PostizError("IDs desconhecidos: " + ", ".join(unknown))
    if len(selected) != len(set(selected)):
        raise PostizError("a lista contém IDs repetidos")
    return selected


def parse_start(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise PostizError("use --start no formato AAAA-MM-DDTHH:MM") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=TIMEZONE)
    return parsed.astimezone(TIMEZONE)


def scheduled_at(start: datetime | None, position: int, interval_days: int) -> datetime | None:
    return start + timedelta(days=position * interval_days) if start else None


def show_plan(items: list[dict[str, object]], start: datetime | None, interval_days: int) -> None:
    print("PLANO — nenhuma postagem foi criada\n")
    total_mib = 0.0
    for index, item in enumerate(items):
        path = item["video"]
        assert isinstance(path, Path)
        size_mib = path.stat().st_size / 1024**2
        total_mib += size_mib
        when = scheduled_at(start, index, interval_days)
        date_label = when.strftime("%d/%m/%Y %H:%M %Z") if when else "data ainda não definida"
        print(f"{index + 1:02}. {item['id']} — {date_label} — {size_mib:.1f} MiB")
        print(f"    {item['title']}")
    print(f"\n{len(items)} Shorts validados; {total_mib:.1f} MiB no total.")
    print("Visibilidade preparada: não listado. Reservas fora da fila principal.")


def cli_path() -> str:
    executable = shutil.which("postiz") or shutil.which("postiz.cmd")
    if not executable:
        raise PostizError("CLI do Postiz não encontrada; instale com: npm install -g postiz")
    return executable


def api_environment() -> dict[str, str]:
    load_env()
    if not os.environ.get("POSTIZ_API_KEY"):
        raise PostizError(f"POSTIZ_API_KEY ausente. Configure-a em {ENV_FILE}")
    env = os.environ.copy()
    env.setdefault("POSTIZ_API_URL", API_URL)
    return env


def run_postiz(arguments: list[str]) -> str:
    result = subprocess.run(
        [cli_path(), *arguments],
        cwd=ROOT,
        env=api_environment(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise PostizError(detail or f"postiz retornou código {result.returncode}")
    return result.stdout.strip()


def extract_json(output: str) -> object:
    decoder = json.JSONDecoder()
    for index, char in enumerate(output):
        if char not in "[{":
            continue
        try:
            value, end = decoder.raw_decode(output[index:])
        except json.JSONDecodeError:
            continue
        if not output[index + end :].strip():
            return value
    raise PostizError("a CLI não retornou JSON reconhecível")


def integrations() -> list[dict[str, object]]:
    result = extract_json(run_postiz(["integrations:list"]))
    if not isinstance(result, list):
        raise PostizError("resposta inesperada ao listar integrações")
    return [entry for entry in result if isinstance(entry, dict)]


def youtube_integration_id() -> str:
    matches = [
        entry for entry in integrations()
        if str(entry.get("provider") or entry.get("identifier") or "").lower() == "youtube"
    ]
    if len(matches) != 1:
        names = ", ".join(str(entry.get("name") or entry.get("provider")) for entry in matches) or "nenhum"
        raise PostizError(f"esperava um único canal do YouTube; encontrados: {names}")
    integration_id = matches[0].get("id")
    if not integration_id:
        raise PostizError("integração do YouTube sem ID")
    return str(integration_id)


def load_state() -> dict[str, object]:
    if not STATE_FILE.exists():
        return {"version": 1, "items": {}}
    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("items"), dict):
        raise PostizError(f"estado inválido em {STATE_FILE}")
    return data


def save_state(state: dict[str, object]) -> None:
    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE_FILE)


def upload(path: Path) -> dict[str, object]:
    result = extract_json(run_postiz(["upload", str(path)]))
    if isinstance(result, list) and len(result) == 1 and isinstance(result[0], dict):
        result = result[0]
    if not isinstance(result, dict) or not result.get("path"):
        raise PostizError(f"upload sem caminho retornado para {path.name}")
    return result


def create_post(
    item: dict[str, object], integration_id: str, video: dict[str, object],
    thumbnail: dict[str, object], when: datetime, post_type: str,
    visibility: str = "unlisted",
) -> object:
    settings = {
        "__type": "youtube",
        "title": item["title"],
        "type": visibility,
        "selfDeclaredMadeForKids": "no",
        "tags": [{"value": tag, "label": tag} for tag in item["tags"]],
        "thumbnail": {"id": thumbnail.get("id"), "path": thumbnail["path"]},
    }
    payload = {
        "type": post_type,
        "creationMethod": "CLI",
        "date": when.isoformat(),
        "shortLink": False,
        "tags": [],
        "posts": [{
            "integration": {"id": integration_id},
            "value": [{
                "content": item["description"],
                "image": [{"id": video.get("id"), "path": video["path"]}],
                "delay": 0,
            }],
            "settings": settings,
        }],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False)
        temporary = Path(handle.name)
    try:
        return extract_json(run_postiz(["posts:create", "--json", str(temporary)]))
    finally:
        temporary.unlink(missing_ok=True)


def post_ids(record: dict[str, object]) -> list[str]:
    value = record.get("post")
    if isinstance(value, dict) and value.get("postId"):
        return [str(value["postId"])]
    if isinstance(value, list):
        return [str(entry["postId"]) for entry in value if isinstance(entry, dict) and entry.get("postId")]
    return []


def execute(
    items: list[dict[str, object]], start: datetime, interval_days: int,
    post_type: str, visibility: str = "unlisted", replace_existing: bool = False,
) -> None:
    integration_id = youtube_integration_id()
    state = load_state()
    records = state["items"]
    assert isinstance(records, dict)

    for index, item in enumerate(items):
        short_id = str(item["id"])
        record = records.setdefault(short_id, {})
        if not isinstance(record, dict):
            raise PostizError(f"estado inválido para {short_id}")
        if record.get("post"):
            when = scheduled_at(start, index, interval_days)
            assert when is not None
            if replace_existing:
                if record.get("mode") != "draft":
                    raise PostizError(
                        f"{short_id}: substituição só aceita rascunho; estado atual é {record.get('mode')}"
                    )
                if record.get("scheduled_at") != when.isoformat():
                    raise PostizError(
                        f"{short_id}: o rascunho usa {record.get('scheduled_at')}; "
                        "a substituição exige a mesma data"
                    )
                previous_ids = post_ids(record)
                if not previous_ids:
                    raise PostizError(f"{short_id}: rascunho antigo sem postId no estado")
                replacement = record.setdefault("replacement", {})
                if not isinstance(replacement, dict):
                    raise PostizError(f"{short_id}: estado de substituição inválido")
                print(f"{short_id}: enviando o novo vídeo ao Postiz local...")
                if not replacement.get("video"):
                    replacement["video"] = upload(item["video"])
                    save_state(state)
                print(f"{short_id}: enviando a nova thumbnail ao Postiz local...")
                if not replacement.get("thumbnail"):
                    replacement["thumbnail"] = upload(item["thumbnail"])
                    save_state(state)
                if not replacement.get("post"):
                    print(f"{short_id}: criando agendamento substituto para {when.isoformat()}...")
                    replacement["post"] = create_post(
                        item, integration_id, replacement["video"], replacement["thumbnail"],
                        when, "schedule", visibility,
                    )
                    replacement["mode"] = "schedule"
                    replacement["scheduled_at"] = when.isoformat()
                    replacement["visibility"] = visibility
                    save_state(state)
                for post_id in previous_ids:
                    print(f"{short_id}: removendo rascunho antigo {post_id}...")
                    run_postiz(["posts:delete", post_id])
                replacement["replaced_draft_post_ids"] = previous_ids
                records[short_id] = replacement
                save_state(state)
                print(f"{short_id}: produção nova agendada e rascunho antigo removido")
                continue
            if post_type == "schedule" and record.get("mode") == "draft":
                if record.get("scheduled_at") != when.isoformat():
                    raise PostizError(
                        f"{short_id}: o rascunho usa {record.get('scheduled_at')}; "
                        "use a mesma data ou ajuste-o no Postiz"
                    )
                ids = post_ids(record)
                if not ids:
                    raise PostizError(f"{short_id}: rascunho sem postId no estado")
                for post_id in ids:
                    run_postiz(["posts:status", post_id, "--status", "schedule"])
                record["mode"] = "schedule"
                save_state(state)
                print(f"{short_id}: rascunho promovido a agendamento")
            else:
                print(f"{short_id}: já possui post no estado; ignorado")
            continue

        print(f"{short_id}: enviando vídeo ao Postiz local...")
        if not record.get("video"):
            record["video"] = upload(item["video"])
            save_state(state)
        print(f"{short_id}: enviando thumbnail ao Postiz local...")
        if not record.get("thumbnail"):
            record["thumbnail"] = upload(item["thumbnail"])
            save_state(state)

        when = scheduled_at(start, index, interval_days)
        assert when is not None
        print(f"{short_id}: criando {post_type} para {when.isoformat()}...")
        record["post"] = create_post(
            item, integration_id, record["video"], record["thumbnail"], when,
            post_type, visibility,
        )
        record["mode"] = post_type
        record["scheduled_at"] = when.isoformat()
        save_state(state)
        print(f"{short_id}: pronto")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepara Shorts validados no Postiz")
    parser.add_argument(
        "command", nargs="?",
        choices=["plan", "check", "draft", "schedule", "replace-schedule"],
        default="plan",
    )
    parser.add_argument("--ids", help="IDs separados por vírgula; o padrão é a ordem editorial principal")
    parser.add_argument("--include-reserves", action="store_true", help="inclui L01-R02 e L01-R03")
    parser.add_argument("--start", help="primeira data local, no formato AAAA-MM-DDTHH:MM")
    parser.add_argument("--interval-days", type=int, default=2, help="dias entre Shorts (padrão: 2)")
    parser.add_argument(
        "--confirm-youtube", action="store_true",
        help="confirma que posts agendados poderão ser enviados ao YouTube",
    )
    parser.add_argument(
        "--visibility", choices=["unlisted", "public"], default="unlisted",
        help="visibilidade preparada para o YouTube (padrão: unlisted)",
    )
    parser.add_argument(
        "--confirm-public", action="store_true",
        help="confirma publicação pública quando --visibility public",
    )
    parser.add_argument(
        "--confirm-replace", action="store_true",
        help="confirma substituir e remover o rascunho antigo no Postiz",
    )
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()
    try:
        if args.interval_days < 1:
            raise PostizError("--interval-days precisa ser pelo menos 1")
        rows = read_rows()
        selected = select_ids(args.ids, args.include_reserves)
        items = [item_data(short_id, rows[short_id]) for short_id in selected]
        start = parse_start(args.start)

        if args.command == "plan":
            show_plan(items, start, args.interval_days)
            return 0
        if args.command == "check":
            connected = integrations()
            print(json.dumps(connected, ensure_ascii=False, indent=2))
            print("\nConexão com o Postiz validada.")
            return 0
        if not start:
            raise PostizError("draft e schedule exigem --start AAAA-MM-DDTHH:MM")
        if args.command in {"schedule", "replace-schedule"} and not args.confirm_youtube:
            raise PostizError(f"{args.command} exige --confirm-youtube; revise o plano antes")
        if args.visibility == "public" and not args.confirm_public:
            raise PostizError("--visibility public exige --confirm-public")
        if args.command == "replace-schedule" and not args.confirm_replace:
            raise PostizError("replace-schedule exige --confirm-replace")
        execute(
            items, start, args.interval_days,
            "draft" if args.command == "draft" else "schedule",
            args.visibility,
            args.command == "replace-schedule",
        )
        return 0
    except (OSError, ValueError, PostizError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
