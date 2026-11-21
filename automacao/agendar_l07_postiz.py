"""Agendamento de L07 no Postiz via postiz_shorts.py."""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.production-tools/python'), str(ROOT / '.course-tools')]

import postiz_shorts as p

P = ROOT / 'producao/L07'
MP4 = P / 'exportacoes/Pixel_Procurado_L07_4K.mp4'
THUMB = P / 'publicacao/capa_youtube.jpg'

titulo = (P / 'publicacao/01_TITULO.txt').read_text(encoding='utf8').strip()
descricao = (P / 'publicacao/02_DESCRICAO.txt').read_text(encoding='utf8').strip()
tags_str = (P / 'publicacao/04_TAGS.txt').read_text(encoding='utf8').strip()
tags = [t.strip() for t in tags_str.split(',') if t.strip()]

# 07 de novembro de 2026 às 12:00 BRT
when = datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone(timedelta(hours=-3)))

print(f"1. Fazendo upload do vídeo {MP4.name} no Postiz...")
video_upload = p.upload(MP4)
print(f"Vídeo enviado: {video_upload}")

print(f"2. Fazendo upload da capa {THUMB.name} no Postiz...")
thumb_upload = p.upload(THUMB)
print(f"Capa enviada: {thumb_upload}")

channel_youtube = 'cmvsctfgl0001jncj932ovibv'

settings = {
    "__type": "youtube",
    "title": titulo,
    "type": "public",
    "privacyStatus": "public",
    "selfDeclaredMadeForKids": "no",
    "tags": [{"value": tag, "label": tag} for tag in tags],
    "thumbnail": {"id": thumb_upload.get("id"), "path": thumb_upload["path"]}
}

payload = {
    "type": "schedule",
    "creationMethod": "CLI",
    "date": when.isoformat(),
    "shortLink": False,
    "tags": [],
    "posts": [
        {
            "integration": {"id": channel_youtube},
            "value": [
                {
                    "content": f"{titulo}\n\n{descricao}",
                    "image": [video_upload],
                    "delay": 0
                }
            ],
            "settings": settings
        }
    ]
}

target_json = P / 'publicacao/postiz_payload.json'
target_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf8')

print("3. Criando agendamento no Postiz CLI...")
output = p.run_postiz(['posts:create', '--json', str(target_json)])
res = p.extract_json(output)
print("Resultado do agendamento:")
print(json.dumps(res, ensure_ascii=False, indent=2))

(P / 'publicacao/POSTIZ_AGENDAMENTO.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf8')
print("Agendamento concluído com sucesso!")
