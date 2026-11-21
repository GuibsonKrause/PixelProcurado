"""Publicação do especial 4K no YouTube e Facebook via Postiz CLI + Cloudflare R2."""

import json
import subprocess
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from uuid import uuid4
from boto3.s3.transfer import TransferConfig

import postiz_shorts as postiz
from distribuir_l05_postiz import ROOT, write
from distribuir_l06_postiz import run_cli
from r2_media import R2Media

EP = ROOT / 'producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06'
SOCIAL = EP / 'social'
STATE_FILE = SOCIAL / 'POSTIZ_ESTADO_4K.json'
VIDEO_4K = EP / 'exportacoes/Pixel_Procurado_GTA6_2013_Longo_V2_4K.mp4'
COVER_YT = SOCIAL / 'capas/V2/longo_youtube.jpg'

CHANNELS = {
    'youtube': 'cmvsctfgl0001jncj932ovibv',
    'facebook': 'cmvzyur290001pddwolrt33em',
}

TITLE = 'GTA 6 vai humilhar o seu eu de 2013'

DESCRIPTION = (
    "A polícia de Leonida não esquece a sua cara — e muito menos a sua roupa. "
    "Se você planejava entrar em GTA 6 repetindo as mesmas fugas e hábitos de 2013, o choque de realidade vai ser grande.\n\n"
    "Neste especial do Pixel Procurado, investigamos o que muda na perseguição policial de Grand Theft Auto VI: "
    "o sistema de reconhecimento por aparência, as denúncias de testemunhas civis, a limitação de armas no porta-malas "
    "do veículo pessoal e as datas confirmadas para o pré-load de até 212 GB.\n\n"
    "Capítulos:\n"
    "00:00 A polícia lembra da sua roupa\n"
    "00:53 Você quer testar Leonida?\n"
    "01:42 O novo sistema de atenção e testemunhas\n"
    "02:49 O porta-malas e o fim do inventário infinito\n"
    "03:49 O nível de detalhe da Rockstar\n"
    "04:42 SSD e o peso da nova geração\n"
    "05:35 Pré-load no PS5 e Xbox Series: datas e horários\n"
    "06:25 A camiseta extra: por que o conselho de mãe funciona\n"
    "07:09 Preparado para 19 de novembro?\n\n"
    "Fontes e checagens oficiais:\n"
    "• Rockstar Games Newswire e GTA VI Launch Hub (rockstargames.com/VI)\n"
    "• FAQ Oficial de Pré-load da Rockstar Support\n"
    "• Entrevista técnica de Rob Nelson (IGN / Best Buy Gaming)\n\n"
    "Qual é a primeira coisa que você vai tentar fazer em Leonida que certamente vai dar errado? Deixe nos comentários!\n\n"
    "#GTA6 #GTAVI #PixelProcurado #RockstarGames #PlayStation5 #XboxSeriesX #Gameplay"
)

TAGS = [
    {"value": "GTA 6", "label": "GTA 6"},
    {"value": "GTA VI", "label": "GTA VI"},
    {"value": "Grand Theft Auto VI", "label": "Grand Theft Auto VI"},
    {"value": "Pixel Procurado", "label": "Pixel Procurado"},
    {"value": "GTA 6 policia", "label": "GTA 6 policia"},
    {"value": "GTA 6 gameplay", "label": "GTA 6 gameplay"},
    {"value": "GTA 6 lancamento", "label": "GTA 6 lancamento"},
    {"value": "GTA 6 preload", "label": "GTA 6 preload"},
    {"value": "GTA 6 2013", "label": "GTA 6 2013"},
    {"value": "GTA 6 4K", "label": "GTA 6 4K"}
]


def now():
    return datetime.now(timezone.utc)


def save_state(state):
    for attempt in range(5):
        try:
            write(STATE_FILE, state)
            return
        except PermissionError:
            time.sleep(0.5)


def posts():
    current = now()
    result = run_cli(['posts:list', '--startDate', (current - timedelta(days=2)).isoformat(),
                      '--endDate', (current + timedelta(days=2)).isoformat()])
    return result.get('posts', []) if isinstance(result, dict) else result


def stage_video_r2(path, key):
    print(f"Iniciando stage no Cloudflare R2 ({path.stat().st_size / (1024*1024):.1f} MB)...", flush=True)
    transfer = TransferConfig(
        multipart_threshold=32 * 1024 * 1024,
        multipart_chunksize=32 * 1024 * 1024,
        max_concurrency=2
    )
    media, key = R2Media().stage(path, key, transfer_config=transfer)
    print(f"Vídeo disponível em R2: {media['path']}", flush=True)
    return media


def build_payload(provider, media_obj, cover_obj=None):
    post_item = {
        "integration": {"id": CHANNELS[provider]},
        "value": [{
            "content": DESCRIPTION,
            "image": [media_obj],
            "delay": 0
        }]
    }
    if provider == "youtube":
        settings = {
            "__type": "youtube",
            "title": TITLE,
            "type": "public",
            "selfDeclaredMadeForKids": "no",
            "tags": TAGS
        }
        if cover_obj:
            settings["thumbnail"] = cover_obj
        post_item["settings"] = settings
    elif provider == "facebook":
        post_item["settings"] = {
            "__type": "facebook",
            "post_type": "post",
            "title": TITLE
        }
    return {
        "type": "now",
        "date": now().isoformat(),
        "creationMethod": "CLI",
        "shortLink": False,
        "tags": [],
        "posts": [post_item]
    }


def main():
    assert VIDEO_4K.is_file(), f"Arquivo não encontrado: {VIDEO_4K}"
    assert COVER_YT.is_file(), f"Capa não encontrada: {COVER_YT}"

    state = {
        "video": str(VIDEO_4K.name),
        "video_bytes": VIDEO_4K.stat().st_size,
        "created_at": now().isoformat(),
        "items": {}
    }
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    # 1. Upload Cover para Postiz
    cover_media = state.get("cover_media")
    if not cover_media:
        try:
            print("Fazendo upload da thumbnail do YouTube no Postiz...", flush=True)
            cover_media = postiz.upload(COVER_YT)
            state["cover_media"] = cover_media
            save_state(state)
            print("Thumbnail carregada no Postiz:", cover_media.get("id"), flush=True)
        except Exception as e:
            print(f"Aviso ao carregar thumb no Postiz: {e}", flush=True)

    # 2. Stage Video no R2
    r2_key = state.get("r2_key") or f"publicacoes/{uuid4().hex}.mp4"
    state["r2_key"] = r2_key
    save_state(state)

    media_obj = state.get("r2_media")
    if not media_obj:
        media_obj = stage_video_r2(VIDEO_4K, r2_key)
        state["r2_media"] = media_obj
        save_state(state)
    else:
        print(f"Vídeo R2 já disponível: {media_obj['path']}", flush=True)

    # 3. Disparo dos posts no Postiz
    for provider in ("youtube", "facebook"):
        item_state = state["items"].setdefault(provider, {})
        if item_state.get("post_id"):
            print(f"[{provider}] Post já criado anteriormente: {item_state['post_id']}", flush=True)
            continue

        payload = build_payload(provider, media_obj, cover_obj=cover_media if provider == "youtube" else None)
        target = SOCIAL / f"4k_{provider}_ENVIO.json"
        write(target, payload)

        print(f"[{provider}] Enviando publicação para a API do Postiz via CLI...", flush=True)
        result = run_cli(['posts:create', '--json', str(target)])
        post_ids = postiz.post_ids({'post': result})
        if not post_ids:
            raise RuntimeError(f"[{provider}] Nenhum post_id retornado pelo Postiz: {result}")
        item_state["post_id"] = post_ids[0]
        item_state["posted_at"] = now().isoformat()
        save_state(state)
        print(f"[{provider}] Post aceito pelo Postiz! ID: {item_state['post_id']}", flush=True)

    # 4. Monitoramento até PUBLISHED
    print("Monitorando status de publicação nas plataformas...", flush=True)
    deadline = now() + timedelta(minutes=45)
    all_published = False

    while now() < deadline:
        remote_posts = {p['id']: p for p in posts()}
        statuses = {}
        for provider in ("youtube", "facebook"):
            item_state = state["items"][provider]
            pid = item_state["post_id"]
            p_data = remote_posts.get(pid, {})
            item_state["remote"] = {
                "state": p_data.get("state"),
                "releaseURL": p_data.get("releaseURL"),
                "releaseId": p_data.get("releaseId"),
                "error": p_data.get("error"),
                "publishDate": p_data.get("publishDate")
            }
            statuses[provider] = p_data.get("state")

        save_state(state)
        print(f"Status atual: {statuses}", flush=True)

        if all(s == "PUBLISHED" for s in statuses.values()):
            all_published = True
            break
        if any(s == "ERROR" for s in statuses.values()):
            print("Detectado erro em uma das publicações. Verifique o estado.", flush=True)
            break

        time.sleep(30)

    # 5. Limpeza do objeto R2 após confirmação
    if all_published:
        print("Todas as publicações foram concluídas como PUBLISHED!", flush=True)
        if not state.get("r2_cleaned") and state.get("r2_key"):
            print("Removendo mídia temporária do Cloudflare R2...", flush=True)
            R2Media().remove(state["r2_key"])
            state["r2_cleaned"] = True
            save_state(state)
            print("Objeto R2 removido com sucesso.", flush=True)

    print("\nResumo Final da Publicação 4K:")
    for prov, rec in state["items"].items():
        print(f"- {prov.upper()}: {rec.get('remote', {}).get('state')} | Link: {rec.get('remote', {}).get('releaseURL')}")


if __name__ == '__main__':
    main()
