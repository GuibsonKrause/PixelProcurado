"""Distribuição/agendamento Postiz (YouTube, TikTok, Instagram e Facebook), guiada por episodio.json.

SEGURANÇA: por padrão é um dry-run (imprime o plano; não faz upload, não usa R2, não chama o Postiz).
Só envia de verdade com --publicar (agendado) ou --publicar --agora (imediato).

Uso: py -3.12 automacao/pipeline/distribuir_postiz.py --episodio producao/L08 [--data ISO8601] [--publicar [--agora]]
                                                       [--so chave1,chave2] [--status [--limpar]]
- `midia` de uma peça pode ser um arquivo ou uma lista (carrossel/multifoto).
- `capa` é anexada no YouTube (settings.thumbnail) e no Instagram (image[0].thumbnail); Facebook não tem rota de capa.
- Peças com post_id no estado são puladas. `--status` consulta o Postiz; `--limpar` remove do R2 o que já está
  PUBLISHED com releaseURL.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from uuid import uuid4

from comum import ROOT, caminho, carregar, erro

sys.path.insert(0, str(ROOT / "automacao"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# Limites observados em 11/11/2026 (bytes por arquivo de vídeo). O Instagram recusou 832 MB citando 300 MB.
LIMITE_VIDEO = {"instagram": 300_000_000}
VIDEO = (".mp4", ".mov")


def acima_do_limite(peca):
    lim = LIMITE_VIDEO.get(peca["rede"])
    return [a for a in arquivos(peca) if lim and a.is_file() and a.suffix.lower() in VIDEO and a.stat().st_size > lim]


def tamanho_tags_youtube(tags):
    """Conta como o YouTube (limite 500): tag com espaço ganha aspas, mais as vírgulas entre tags."""
    tags = [t.strip() for t in tags]
    return sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0)


def achar_id(obj):
    """Procura o ID do post na resposta do posts:create (formatos variam: id, postId, aninhado em listas/dicts)."""
    if isinstance(obj, dict):
        for k in ("postId", "id"):
            if isinstance(obj.get(k), str) and obj[k]:
                return obj[k]
        obj = list(obj.values())
    if isinstance(obj, list):
        for v in obj:
            achado = achar_id(v) if isinstance(v, (dict, list)) else None
            if achado:
                return achado
    return None


def ids_no_postiz(integracao):
    from publicar_especial_postiz import posts
    return {r["id"] for r in posts() if (r.get("integration") or {}).get("id") == integracao}


def arquivos(peca):
    m = peca["midia"]
    arqs = [caminho(x) for x in (m if isinstance(m, list) else [m])]
    if peca["rede"] == "tiktok" and (peca["tipo"] != "video" or len(arqs) != 1 or arqs[0].suffix.lower() != ".mp4"):
        erro(f"[{peca['chave']}] TikTok DIRECT_POST exige tipo video e um único arquivo MP4.")
    return arqs


def montar_payload(pub, peca, medias, data, capa=None, agora=False):
    """Corpo do posts:create; `medias` são objetos já enviados ao destino; `capa` o objeto da capa enviada."""
    rede, tipo = peca["rede"], peca["tipo"]
    if rede == "youtube":
        settings = {"__type": rede, "title": peca["titulo"], "type": pub.get("youtube_visibilidade", "public"),
                    "selfDeclaredMadeForKids": "no",
                    "tags": [{"value": t.strip(), "label": t.strip()} for t in pub["tags_youtube"]]}
        if capa:
            settings["thumbnail"] = capa
    elif rede == "tiktok":
        options = peca.get("tiktok", {})
        # o app TikTok não tem aprovação para post público direto: padrão é enviar privado à caixa do app
        settings = {"__type": rede, "title": peca.get("titulo", "")[:90],
                    "privacy_level": options.get("privacy_level", "SELF_ONLY"),
                    "content_posting_method": options.get("content_posting_method", "UPLOAD"), "autoAddMusic": "no"}
        for field in ("duet", "stitch", "comment", "brand_content_toggle", "brand_organic_toggle", "video_made_with_ai"):
            settings[field] = options.get(field, False)
    else:
        settings = {"__type": rede, "post_type": tipo}
        if rede == "facebook" and tipo != "story" and peca.get("titulo"):
            settings["title"] = peca["titulo"]
        if capa and rede == "instagram":
            medias = [dict(medias[0], thumbnail=capa["path"]), *medias[1:]]
    return {"type": "now" if agora else "schedule", "creationMethod": "CLI", "date": data, "shortLink": False, "tags": [],
            "posts": [{"integration": {"id": pub["canais"][rede]},
                       "value": [{"content": pub["textos"][peca["texto"]], "image": medias, "delay": 0}],
                       "settings": settings}]}


def plano(pub, estado, data):
    print(f"DRY-RUN: nada será enviado. Data: {data}")
    for p in pub["pecas"]:
        arqs = arquivos(p)
        rec = estado["items"].get(p["chave"], {})
        marca = f"JÁ ENVIADO (post_id={rec.get('post_id')})" if rec.get("post_id") else "pendente"
        via = "postiz upload" if p["rede"] == "youtube" and all(a.is_file() and a.stat().st_size < 1_000_000_000 for a in arqs) else "R2 stage"
        print(f"- {p['chave']:18s} {p['rede']:9s} {p['tipo']:5s} via {via:13s} {marca}")
        for arq in arqs:
            tam = f"{arq.stat().st_size / 1e6:.0f} MB" if arq.is_file() else "AUSENTE"
            excede = " ACIMA DO LIMITE DA REDE" if arq in acima_do_limite(p) else ""
            print(f"    mídia: {arq} [{tam}]{excede}")
        if p.get("capa"):
            print(f"    capa : {caminho(p['capa'])} [{'OK' if caminho(p['capa']).is_file() else 'AUSENTE'}]")
        if p.get("titulo"):
            print(f"    título: {p['titulo']}")
        if p["rede"] == "youtube":
            n = tamanho_tags_youtube(pub["tags_youtube"])
            print(f"    tags : {n}/500 caracteres" + (" ACIMA DO LIMITE DO YOUTUBE" if n > 500 else ""))
        print(f"    texto ({p['texto']}): {pub['textos'][p['texto']][:90]!r}...")
    print("\nPara enviar de fato: repita com --publicar (e --agora para publicar já)")


def enviar(p, rec, arq, r2, postiz, campo_chave):
    # upload local do Postiz recusa ~>1 GB (HTTP 413): arquivos grandes vão por URL via R2, mesmo no YouTube
    if p["rede"] == "youtube" and arq.stat().st_size < 1_000_000_000:
        return postiz.extract_json(postiz.run_postiz(["upload", str(arq)]))
    rec.setdefault(campo_chave, f"publicacoes/{uuid4().hex}{arq.suffix.lower()}")
    obj, _ = r2.stage(arq, rec[campo_chave])
    return obj


def publicar(pub, estado_path, envio_dir, estado, data, agora, reenviar=False):
    import postiz_shorts as postiz
    from r2_media import R2Media

    r2 = R2Media()
    for p in pub["pecas"]:  # barra tudo antes de enviar qualquer coisa
        rec = estado["items"].get(p["chave"], {})
        if rec.get("post_id"):
            continue
        if p["rede"] == "tiktok":
            arquivos(p)
        grandes = acima_do_limite(p)
        if grandes:
            erro(f"[{p['chave']}] {grandes[0].name} tem {grandes[0].stat().st_size / 1e6:.0f} MB; limite de vídeo do "
                 f"{p['rede']}: {LIMITE_VIDEO[p['rede']] / 1e6:.0f} MB. Gere uma versão menor antes de enviar.")
        if p["rede"] == "youtube" and tamanho_tags_youtube(pub["tags_youtube"]) > 500:
            erro(f"[{p['chave']}] tags_youtube somam {tamanho_tags_youtube(pub['tags_youtube'])} caracteres na contagem do "
                 "YouTube (limite 500; tag com espaço conta as aspas). Remova tags antes de enviar.")
        if rec.get("tentativa_em") and not reenviar:
            erro(f"[{p['chave']}] já houve tentativa em {rec['tentativa_em']} sem post_id gravado. Confira no Postiz se "
                 "o post existe (grave o ID no estado) ou repita com --reenviar para enviar de novo de propósito.")
    print("Iniciando " + ("publicação imediata" if agora else f"agendamento para {data}") + "...")
    for p in pub["pecas"]:
        chave = p["chave"]
        rec = estado["items"].setdefault(chave, {})
        if rec.get("post_id"):
            print(f"[{chave}] Já enviado (post_id={rec['post_id']})")
            continue
        arqs = arquivos(p)
        faltam = [str(a) for a in arqs if not a.is_file()]
        if faltam:
            erro(f"[{chave}] mídia ausente: {faltam}")
        print(f"[{chave}] Preparando mídia: {', '.join(a.name for a in arqs)}...", flush=True)
        if not rec.get("medias"):
            rec["medias"] = [enviar(p, rec, a, r2, postiz, f"r2_key_{i}") for i, a in enumerate(arqs)]
            write_json(estado_path, estado)
        capa = None
        if p.get("capa") and caminho(p["capa"]).is_file() and p["rede"] in ("youtube", "instagram"):
            if not rec.get("capa_obj"):
                rec["capa_obj"] = enviar(p, rec, caminho(p["capa"]), r2, postiz, "r2_key_capa")
                write_json(estado_path, estado)
            capa = rec["capa_obj"]
        envio = envio_dir / f"{chave}_ENVIO.json"
        agora_iso = datetime.now(timezone.utc).isoformat()
        write_json(envio, montar_payload(pub, p, rec["medias"], agora_iso if agora else data, capa, agora))
        rec["capa_anexada"] = bool(capa)
        rec["tentativa_em"] = agora_iso
        write_json(estado_path, estado)  # registra antes de enviar
        integracao = pub["canais"][p["rede"]]
        antes = ids_no_postiz(integracao)
        print(f"[{chave}] Enviando ao Postiz...", flush=True)
        result = postiz.extract_json(postiz.run_postiz(["posts:create", "--json", str(envio)]))
        post_id = achar_id(result)
        if not post_id:  # resposta sem ID: descobre pelo post novo que apareceu nesta integração
            novos = ids_no_postiz(integracao) - antes
            post_id = novos.pop() if len(novos) == 1 else None
        if not post_id:
            rec["resposta_sem_id"] = result
            write_json(estado_path, estado)
            erro(f"[{chave}] o Postiz aceitou mas não foi possível identificar o post. NÃO reenvie: localize o post no "
                 "Postiz e grave o post_id no estado.")
        rec.update(post_id=post_id, enviado_em=agora_iso, modo="agora" if agora else "agendado")
        write_json(estado_path, estado)
        print(f"[{chave}] Aceito! Post ID: {post_id}", flush=True)
    print(f"\nRegistrado em {estado_path.name}.")


def conferir(estado_path, estado, limpar):
    from publicar_especial_postiz import posts
    from r2_media import R2Media

    por_id = {r["id"]: r for r in posts()}
    for chave, rec in estado["items"].items():
        r = por_id.get(rec.get("post_id"))
        if r:
            rec["remote"] = {k: r.get(k) for k in ("state", "releaseURL", "releaseId", "publishDate")}
            rec["remote"]["error"] = r.get("error")
        rm = rec.get("remote", {})
        print(f"{chave:18s} {rm.get('state')} {rm.get('releaseURL')} {('ERRO: ' + str(rm.get('error'))) if rm.get('error') else ''}")
        if limpar and rm.get("state") == "PUBLISHED" and rm.get("releaseURL") and not rec.get("r2_limpo"):
            for k in [k for k in rec if k.startswith("r2_key")]:
                R2Media().remove(rec[k])
            rec["r2_limpo"] = True
    write_json(estado_path, estado)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episodio", required=True)
    ap.add_argument("--data", help="data/hora ISO 8601 (padrão: publicacao.data_padrao)")
    ap.add_argument("--publicar", action="store_true", help="envia de verdade; sem esta flag é só dry-run")
    ap.add_argument("--agora", action="store_true", help="com --publicar: publica imediatamente (type=now)")
    ap.add_argument("--status", action="store_true", help="consulta o Postiz e atualiza o estado remoto")
    ap.add_argument("--limpar", action="store_true", help="com --status: remove do R2 as mídias já PUBLISHED")
    ap.add_argument("--reenviar", action="store_true", help="permite reenviar peça com tentativa anterior sem post_id")
    ap.add_argument("--so", help="chaves das peças separadas por vírgula")
    a = ap.parse_args()
    ep = carregar(a.episodio)
    pub = ep["publicacao"]
    data = a.data or pub["data_padrao"]
    estado_path = caminho(pub["estado"])
    estado = json.loads(estado_path.read_text(encoding="utf-8")) if estado_path.is_file() else {"version": 1, "items": {}}
    if a.so:
        pub = dict(pub, pecas=[p for p in pub["pecas"] if p["chave"] in a.so.split(",")])
    if a.status:
        conferir(estado_path, estado, a.limpar)
        return
    if not a.publicar:
        plano(pub, estado, data)
        return
    publicar(pub, estado_path, caminho(pub["pasta_envio"]), estado, data, a.agora, a.reenviar)


if __name__ == "__main__":
    main()
