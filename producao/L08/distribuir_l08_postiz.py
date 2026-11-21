"""Distribuição e Agendamento L08 via Postiz + Cloudflare R2."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "automacao"))

import postiz_shorts as postiz
from r2_media import R2Media

SOCIAL = HERE / "social"
STATE = SOCIAL / "POSTIZ_ESTADO.json"
OUT = HERE / "exportacoes"

VIDEO_LONG = OUT / "Pixel_Procurado_L08_Longo_V2.mp4"
VIDEO_SHORT = OUT / "Pixel_Procurado_L08_Short_V2.mp4"
THUMB_LONG = HERE / "publicacao/capa_youtube.jpg"
THUMB_SHORT = ROOT / "producao/shorts/L08/publicacao/capa_youtube.jpg"
STORY_IMG = ROOT / "producao/shorts/L08/publicacao/capa_master.png"

CHANNELS = {
    'youtube': 'cmvsctfgl0001jncj932ovibv',
    'facebook': 'cmvzyur290001pddwolrt33em',
    'instagram': 'cmvzyw7vj0003pddwkgtivv8i',
}

# Títulos otimizados por SEO
TITLES = {
    'youtube_long': 'GTA 6: quem deve a quem em Leonida?',
    'youtube_short': 'O aluguel grátis veio cobrar Jason em GTA 6 #Shorts',
    'facebook_long': 'GTA 6: quem deve a quem em Leonida? — Acordos e favores no elenco oficial',
    'facebook_short': 'O aluguel grátis veio cobrar Jason em GTA 6',
    'story': 'O aluguel grátis veio cobrar Jason em GTA 6',
}

COPY_LONG = (
    "O aluguel grátis de Jason tem preço. A apresentação oficial dos personagens de GTA 6 revela "
    "acordos de moradia, amizades com interesses duplos e assaltantes experientes assumindo riscos.\n\n"
    "Quando um favor vira obrigação, quem realmente paga a conta quando o plano dá errado? Analisamos "
    "os vínculos de Brian Heder, Cal Hampton, Raul Bautista e o núcleo musical de Leonida.\n\n"
    "Análise editorial sobre material oficial de GTA VI.\n"
    "Fonte: https://www.rockstargames.com/VI/only-in-leonida\n"
    "Narração sintética com auxílio de IA.\n\n"
    "#GTA6 #GTAVI #PixelProcurado"
)

COPY_SHORT = (
    "Jason mora sem pagar aluguel na propriedade de Brian, mas a fatura chegou em outro formato. "
    "Em GTA 6, um favor desses aproxima ou prende?\n\n"
    "Fichas oficiais dos personagens de GTA VI: https://www.rockstargames.com/VI/only-in-leonida\n"
    "Análise do material oficial. Imagens: Rockstar Games.\n"
    "Narração sintética com auxílio de IA.\n\n"
    "#GTA6 #GTAVI #Shorts #PixelProcurado"
)

COPY_STORY = (
    "O aluguel grátis de Jason tem preço. Confira a análise completa no canal Pixel Procurado! #GTA6"
)

def run_cli(args):
    return postiz.extract_json(postiz.run_postiz(args))

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def schedule_posts(target_time_iso):
    SOCIAL.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.is_file() else {"version": 1, "items": {}}
    r2 = R2Media()
    
    # Matriz de jobs de agendamento em todas as redes e formatos suportados
    jobs = [
        # YouTube
        ('youtube', 'youtube_long', VIDEO_LONG, 'post', THUMB_LONG),
        ('youtube', 'youtube_short', VIDEO_SHORT, 'post', THUMB_SHORT),
        # Instagram
        ('instagram', 'instagram_reel', VIDEO_SHORT, 'post', None),
        ('instagram', 'instagram_story', STORY_IMG, 'story', None),
        # Facebook
        ('facebook', 'facebook_video', VIDEO_LONG, 'post', None),
        ('facebook', 'facebook_reel', VIDEO_SHORT, 'post', None),
        ('facebook', 'facebook_story', STORY_IMG, 'story', None),
    ]
    
    print(f"Iniciando preparação de agendamento para {target_time_iso}...")
    
    for provider, job_key, media_path, post_type, thumb_path in jobs:
        record = state["items"].setdefault(job_key, {})
        if record.get("scheduled"):
            print(f"[{job_key}] Já agendado anteriormente com post_id: {record.get('post_id')}")
            continue
            
        print(f"[{job_key}] Preparando mídia: {media_path.name}...")
        
        # Upload / Stage
        if provider == "youtube":
            # YouTube via Postiz upload local
            media_upload = postiz.run_postiz(["upload", str(media_path)])
            record["media"] = postiz.extract_json(media_upload)
        else:
            # Meta via Cloudflare R2
            ext = media_path.suffix.lower()
            record.setdefault("r2_key", f"publicacoes/{uuid4().hex}{ext}")
            staged_url, _ = r2.stage(media_path, record["r2_key"])
            record["media"] = staged_url
            
        # Payload
        content = COPY_LONG if "long" in job_key or "video" in job_key else COPY_STORY if post_type == "story" else COPY_SHORT
        title = TITLES.get(job_key, TITLES['youtube_long'])
        
        settings = {'__type': provider, 'post_type': post_type}
        if provider == 'youtube':
            settings = {
                '__type': provider,
                'title': title,
                'type': 'public',
                'selfDeclaredMadeForKids': 'no',
                'tags': [{'value': tag.strip(), 'label': tag.strip()} for tag in ['GTA 6', 'GTA VI', 'Pixel Procurado', 'Brian Heder', 'Jason']]
            }
        elif provider == 'facebook' and post_type != 'story':
            settings['title'] = title
            
        post_data = {
            'type': 'schedule',
            'creationMethod': 'CLI',
            'date': target_time_iso,
            'shortLink': False,
            'tags': [],
            'posts': [{
                'integration': {'id': CHANNELS[provider]},
                'value': [{'content': content, 'image': [record["media"]], 'delay': 0}],
                'settings': settings
            }]
        }
        
        envio_file = SOCIAL / f"{job_key}_ENVIO.json"
        write_json(envio_file, post_data)
        
        print(f"[{job_key}] Enviando agendamento para o Postiz...")
        result = run_cli(['posts:create', '--json', str(envio_file)])
        if isinstance(result, list):
            post_id = result[0].get('id') if result and isinstance(result[0], dict) else str(result)
        elif isinstance(result, dict):
            post_id = result.get('id') or (result.get('post') or {}).get('id') or str(result)
        else:
            post_id = str(result)
        record["post_id"] = post_id
        record["scheduled"] = True
        record["scheduled_at"] = target_time_iso
        write_json(STATE, state)
        print(f"[{job_key}] Agendado com sucesso! Post ID: {post_id}")
        
    print("\nTodos os agendamentos foram criados e registrados em POSTIZ_ESTADO.json.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="2026-11-08T21:00:00.000Z")
    args = parser.parse_args()
    schedule_posts(args.date)
