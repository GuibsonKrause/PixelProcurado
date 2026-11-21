"""Aplicação única da revisão editorial; não gera áudio nem altera mídia.

Registro reprodutível desta entrega, não comando para sobrescrever edições futuras.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P = ROOT / "producao"
BACKUP = P / "historico/antes_humor_br_2026-10-29"
MARKER = HERE / "manifesto_revisao.json"
if MARKER.exists():
    raise SystemExit("Revisão já aplicada. Não sobrescrever ajustes posteriores.")

def read(path):
    return path.read_text(encoding="utf-8-sig")

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path):
    return path.relative_to(ROOT).as_posix()

def clean(text):
    text = re.sub(r"<[^>]+>", "", text)
    return "\n\n".join(re.sub(r"[ \t]+", " ", p).strip() for p in text.strip().split("\n\n"))

backup_records = json.loads(read(BACKUP / "manifesto_backup.json"))
for record in backup_records:
    assert sha(BACKUP / record["path"]).upper() == record["sha256"].upper(), record

protected = []
for directory in (P / "L01", P / "L02", P / "shorts/C01", P / "shorts/C02"):
    protected.extend(p for p in directory.rglob("*") if p.is_file() and p.suffix in (".txt", ".md", ".json"))
protected.extend(p for p in (P / "cortes").glob("*.txt") if p.name.startswith(("C01_", "C02_", "L01-")))
protected_hashes = {rel(path): sha(path) for path in protected}

allowed = set("argh|breath|heavy breath|exhales|cackle|cheer|chuckle|chuckles|cough|cry|gasp|giggle|groan|growl|grunt|grr|hiss|laugh|laughter|moan|pant|pff|phew|scream|shout|shriek|sigh|sighs|sneeze|snicker|snort|sob|throat-clearing|tsk|whimper|whispers|whispering|yawn|short pause|long pause".split("|"))
style = "Conversa próxima e curiosa, com energia variada, humor seco e leve autoironia. Clareza nos fatos; pequeno sorriso nas comparações e final de piada seco. Pausas pelo sentido. Respirações discretas e risadas curtas nos pontos marcados, sem gritaria."
write(P / "editorial/ESTILO_NARRACAO_HUMOR_BR.txt", style)
write(P / "cortes/00_ESTILO_GEMINI_SHORTS.txt", style + " Conclusão firme; ponte final contínua para o reinício.")

# Promover a prévia já lapidada do L04, mantendo as prévias como histórico.
l04 = read(P / "L04/01_NARRACAO_HUMOR_BR_V2_PREVIA.txt").strip()
for before, after in [
    ("E eu entendo a empolgação.", "E eu entendo a empolgação. <short pause>"),
    ("abre a geladeira ou fica dentro da cozinha.", "abre a geladeira ou fica dentro da cozinha. <chuckle>"),
    ("Agora olha o detalhe da gravação:", "<breath> Agora olha o detalhe da gravação:"),
    ("Embora vender o pão de alho separado", "<short pause> Embora vender o pão de alho separado"),
    ("Defender multinacional de graça já é um segundo emprego.", "Defender multinacional de graça já é um segundo emprego. <pff>"),
    ("Tem uma seta desenhada.", "<short pause> Tem uma seta desenhada."),
]:
    assert l04.count(before) == 1, before
    l04 = l04.replace(before, after)
write(P / "L04/03_NARRACAO_GEMINI.txt", l04)

shorts = dict(re.findall(r"^## (C\d{2})\n\n(.*?)(?=^## C\d{2}\n|\Z)", read(HERE / "SHORTS_GEMINI.md"), re.M | re.S))
assert set(shorts) == {f"C{n:02}" for n in range(3, 13)}
entries = []
for ident in [f"L{n:02}" for n in range(3, 9)] + list(shorts):
    long = ident.startswith("L")
    directory = P / ident if long else P / "cortes"
    gemini = directory / ("03_NARRACAO_GEMINI.txt" if long else f"{ident}_GEMINI.txt")
    plain = directory / ("01_NARRACAO.txt" if long else f"{ident}_NARRACAO.txt")
    tagged = read(gemini).strip() if long else shorts[ident].strip()
    events = re.findall(r"<([^>]+)>", tagged)
    assert set(events) <= allowed, ident
    assert not tagged.startswith("<") and not tagged.endswith(">"), ident
    assert not re.search(r"<[^>]+>\s*<", tagged), ident
    text = clean(tagged)
    words = len(text.split())
    assert (600 <= words <= 1100) if long else (160 <= words <= 450), (ident, words)
    write(gemini, tagged)
    write(plain, text)
    style_file = directory / "04_ESTILO_GEMINI.txt" if long else P / "cortes/00_ESTILO_GEMINI_SHORTS.txt"
    if long:
        write(style_file, style)
    else:
        assert text.endswith(("Porque...", "Afinal...", "Então...", "É por isso que...")), ident
        for name, content in (("NARRACAO.txt", text), ("GEMINI.txt", tagged)):
            write(P / "shorts" / ident / "voz" / name, content)
        write(P / "shorts" / ident / "voz/ESTILO_GEMINI.txt", read(style_file))
    assert clean(read(gemini)) == read(plain).strip(), ident
    entries.append({"id": ident, "palavras": words, "paragrafos": len(text.split("\n\n")),
        "eventos": dict(Counter(events)), "narracao": rel(plain), "gemini": rel(gemini),
        "style": rel(style_file), "sha256_narracao": sha(plain), "sha256_gemini": sha(gemini),
        "estado": "texto_revisado_audio_novo_nao_gerado"})

by_id = {entry["id"]: entry for entry in entries}

def notice(path, content):
    if path.exists():
        write(path, content + "\n\n---\n\n" + read(path))

for entry in entries:
    ident = entry["id"]
    long = ident.startswith("L")
    directory = P / ident if long else P / "shorts" / ident
    msg = ("**Revisão de roteiro — 29/10/2026:** humor brasileiro e expressões Gemini aplicados. "
           "Áudios, legendas, blocos de voz, timecodes, projetos e vídeos já existentes pertencem à versão anterior; "
           "não estão validados para este texto. A revisão requer nova locução e sincronização antes de uma nova exportação. ")
    if ident == "L03":
        msg += "O vídeo L03 publicado permanece preservado; esta é uma revisão local, sem republicação. "
    if long:
        msg += "Entradas atuais: `01_NARRACAO.txt`, `03_NARRACAO_GEMINI.txt` e `04_ESTILO_GEMINI.txt`. Ver `05_DIRECAO_HUMOR_BR.md`."
        notice(directory / "02_DIRECAO_E_FONTES.md", msg + " O mapa de parágrafos e as contagens abaixo são históricos; conservar a apuração e os caminhos de mídia como referência.")
        notice(directory / "00_COMECE_AQUI.md", msg)
        if ident == "L03":
            write(directory / "voz/00_REVISAO_EDITORIAL.md", "# Voz anterior do L03\n\n" + msg +
                  "\n\nOs TXT integrais, blocos B01–B05 e reparos desta pasta documentam o áudio antigo. Para a revisão usar [Gemini atual](../03_NARRACAO_GEMINI.txt) e [Style atual](../04_ESTILO_GEMINI.txt). Não concatenar os blocos antigos para narrar o roteiro novo.")
    else:
        msg += f"Texto atual: `voz/NARRACAO.txt`; Gemini: `voz/GEMINI.txt`; Style: `voz/ESTILO_GEMINI.txt`. Origem canônica: `../../cortes/{ident}_NARRACAO.txt`."
        notice(directory / "00_LEIA_ME.md", msg)
    write(directory / "REVISAO_EDITORIAL_2026-10-29.md", "# " + ident + " — revisão editorial\n\n" + msg)

    tagged = read(ROOT / entry["gemini"])
    directions = []
    for number, para in enumerate(tagged.strip().split("\n\n"), 1):
        tags = re.findall(r"<[^>]+>", para)
        if tags:
            excerpt = " ".join(clean(para).split()[:13]) + "…"
            directions.append(f"| {number} | {excerpt} | {'; '.join('`' + tag + '`' for tag in tags)} |")
    if long:
        write(directory / "05_DIRECAO_HUMOR_BR.md", f"""# {ident} — direção atual de narração

Revisão de 29/10/2026. {entry['palavras']} palavras, {entry['paragrafos']} parágrafos. Leitura estimada: {entry['palavras']/155:.1f}–{entry['palavras']/140:.1f} minutos, antes de pausas. Duração não medida em áudio.

[Texto limpo](01_NARRACAO.txt) · [Texto Gemini](03_NARRACAO_GEMINI.txt) · [Style](04_ESTILO_GEMINI.txt) · [Apuração e imagens](02_DIRECAO_E_FONTES.md)

Aplicar o [perfil editorial](../editorial/PERFIL_NARRACAO.md). Fatos claros, curiosidade nos detalhes, comparações com leve sorriso e conclusão seca. Usar o mesmo assunto visual durante a comparação ou uma cartela própria; piadas não dependem de memes externos. Hipóteses devem continuar identificadas na fala e na imagem. Não transformar sugestões de atmosfera em recursos confirmados do jogo.

Os números a seguir correspondem aos blocos separados por linha em branco nos textos atuais. Pontuação já fornece pausas naturais; as tags abaixo marcam somente eventos adicionais.

| Parágrafo | Início da fala | Eventos |
|---|---|---|
{chr(10).join(directions)}

{msg}

Na futura gravação, ouvir a interpretação completa: conferir pronúncias, palavras omitidas, leitura indevida de tags, volume das respirações e risadas. Depois alinhar imagens e legendas pelo áudio novo. Não reaproveitar tempos do mapa antigo.
""")

# Tornar explícito no estado de produção do L03 que a nova revisão não tem mídia validada.
status_path = P / "L03/producao.json"
if status_path.exists():
    saved = BACKUP / rel(status_path)
    if not saved.exists():
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(status_path.read_bytes())
        backup_records.append({"path": rel(status_path), "sha256": sha(saved)})
    status = json.loads(read(status_path))
    status["estado_anterior_preservado"] = {"estado": status.get("estado"), "etapa_atual": status.get("etapa_atual"), "backup": rel(saved)}
    status["estado"] = "roteiro_revisado_pendente_de_nova_narracao"
    status["etapa_atual"] = "roteiro"
    status["revisao_editorial"] = {"data": "2026-10-29", "perfil": "humor_br", "audio_corresponde_ao_roteiro_atual": False, "video_publicado_preservado": True,
        "gemini": "producao/L03/03_NARRACAO_GEMINI.txt", "style": "producao/L03/04_ESTILO_GEMINI.txt", "direcao_atual": "producao/L03/05_DIRECAO_HUMOR_BR.md"}
    write(status_path, json.dumps(status, ensure_ascii=False, indent=2))
    write(BACKUP / "manifesto_backup.json", json.dumps(backup_records, ensure_ascii=False, indent=2))

# Perfil permanente e guia de escrita.
profile_path = P / "editorial/PERFIL_NARRACAO.md"
profile = read(profile_path)
profile = re.sub(r"Versão editorial de 29/10/2026\..*?aprovação de áudio\.",
    "Padrão editorial adotado por solicitação do usuário em 29/10/2026 para todos os novos roteiros, longos e Shorts. Aplicado a L03–L08 e C03–C12. Fundamentação: [pesquisa](PESQUISA_HUMOR_BR_2026-10-29.md). [Entrega e validação](revisao_humor_2026-10-29/LEIA_ME.md). A atuação ainda precisa ser ouvida; texto revisado não significa áudio aprovado.", profile, count=1)
profile = profile.replace("A frase pode ter um sorriso discreto; não inserir risadas, suspiros e hesitações para fingir espontaneidade.",
    "A frase pode ter um sorriso discreto. Risadas curtas, respirações e suspiros podem entrar quando houver uma intenção concreta, sem virar efeito automático depois de cada piada. O usuário solicitou essas expressões; escolher posição e intensidade pelo sentido.")
profile += "\n\n## Entrega para o Gemini e manutenção\n\nConsultar o [catálogo completo das expressões recomendadas](EXPRESSOES_GEMINI.md). Salvar a fala sem tags e uma versão Gemini com exatamente as mesmas palavras, além de eventos pontuais. Usar o estilo curto no campo Style; não colar o perfil inteiro no TTS. Em Shorts, começar pela descoberta e conservar a ponte final sem efeito depois dela. Em longos, variar energia entre descoberta, comparação e conclusão. Sincronizar os consolidados e cópias de produção; marcar áudio e montagem anteriores como pertencentes à versão antiga.\n"
write(profile_path, profile)
guide_path = P / "GUIA_ROTEIROS_RETENCAO.md"
guide = read(guide_path)
guide = re.sub(r"\*\*Atualização de voz.*?(?=\n\n)",
    "**Padrão de voz — 29/10/2026:** aplicar o [perfil de humor brasileiro](editorial/PERFIL_NARRACAO.md) a todos os roteiros futuros, longos e Shorts. L03–L08 e C03–C12 foram reescritos e receberam cópias Gemini com eventos pontuais. Consultar [entrega e validação](editorial/revisao_humor_2026-10-29/LEIA_ME.md) e [expressões Gemini](editorial/EXPRESSOES_GEMINI.md). Originais preservados no histórico; mídias anteriores não correspondem ao texto novo. As exigências de evidência e clareza continuam válidas.", guide, count=1, flags=re.S)
write(guide_path, guide)

# Consolidado dos 14 cortes: substituir só as dez seções do lote.
consolidated_path = P / "cortes/01_ROTEIROS_OTIMIZADOS.md"
old = read(consolidated_path)
sections = list(re.finditer(r"^## ([A-Z0-9-]+) — [^\n]+\n", old, re.M))
assert len(sections) == 14, len(sections)
parts = []
untouched_sections = []
for index, match in enumerate(sections):
    end = sections[index + 1].start() if index + 1 < len(sections) else len(old)
    original = old[match.start():end].strip()
    ident = match.group(1)
    if ident in shorts:
        parts.append(match.group().strip() + "\n\n" + read(P / f"cortes/{ident}_NARRACAO.txt").strip())
    else:
        parts.append(original)
        untouched_sections.append(original)
write(consolidated_path, "# Shorts — roteiros atuais\n\nRevisão de 29/10/2026: C03–C12 com humor brasileiro. C01, C02 e reservas L01 mantidos. Textos limpos abaixo; tags nos arquivos `*_GEMINI.txt`. [Guia e fontes](00_GUIA_CORTES.md). Áudios anteriores são de outra versão.\n\n" + "\n\n".join(parts))
assert all(part in read(consolidated_path) for part in untouched_sections)

cutguide_path = P / "cortes/00_GUIA_CORTES.md"
old_cutguide = read(cutguide_path)
evidence = re.search(r"\| Roteiro \| Evidência.*?(?=\n\n)", old_cutguide, re.S).group()
rows = "\n".join(f"| {e['id']} | {e['palavras']} | {sum(e['eventos'].values())} | {e['palavras']/155:.2f}–{e['palavras']/140:.2f} min |" for e in entries if e['id'].startswith("C"))
write(cutguide_path, f"""# Shorts — humor brasileiro e direção de voz

Revisão de 29/10/2026. [14 roteiros completos](01_ROTEIROS_OTIMIZADOS.md). C03–C12 reescritos; C01, C02 e as reservas de L01 mantidos. C03 deriva de L02, mas integra a revisão porque o corte começa no terceiro Short.

Fala limpa: `<ID>_NARRACAO.txt`. Eventos: `<ID>_GEMINI.txt`. Style: `00_ESTILO_GEMINI_SHORTS.txt`. As cópias em `../shorts/<ID>/voz` estão sincronizadas. [Perfil permanente](../editorial/PERFIL_NARRACAO.md) · [Expressões documentadas](../editorial/EXPRESSOES_GEMINI.md).

| Short | Palavras | Eventos | Estimativa antes de pausas |
|---|---:|---:|---|
{rows}

São estimativas a 140–155 palavras/minuto, não durações medidas. Todos os dez têm seis parágrafos e estão na faixa editorial de 160–450 palavras. Começar no gancho sem vinheta; usar a evidência logo na abertura. A conclusão antecede uma ponte falada que retorna à primeira frase. Não acrescentar CTA, efeito ou silêncio depois da ponte. Ouvir o encaixe no replay quando houver áudio novo.

As expressões variam por intenção, sem cota fixa: pausa para compreensão, respiração na mudança de ideia, riso curto na cumplicidade e suspiro na frustração. A pontuação fornece o restante do ritmo.

## Evidência visual

Manter a apuração nas direções dos episódios L02–L08. As comparações absurdas são comentário do narrador, nunca imagens apresentadas como vazamento ou recurso confirmado. Usar material do assunto ou cartelas próprias. Comparações gráficas não devem introduzir mecânicas ou acontecimentos inventados.

{evidence}

## Estado da mídia

Os WAVs, legendas, projetos e vídeos já existentes de C03–C12 correspondem aos textos anteriores. Esta entrega não gerou áudio nem renderizou vídeo. Gerar nova locução antes de alinhar legendas e remontar. Relatórios de QA e diagnósticos de 26/10 continuam como histórico da versão antiga.

Originais preservados em `../historico/antes_humor_br_2026-10-29`. [Manifesto da revisão](../editorial/revisao_humor_2026-10-29/manifesto_revisao.json). Não utilizar as pastas de histórico como entrada da produção.
""")
notice(P / "cortes/02_DIAGNOSTICO_RETENCAO.md", "**Histórico de 26/10/2026:** contagens, eventos e diagnósticos de C03–C12 abaixo precedem a revisão de humor de 29/10. Para os textos atuais, consultar `00_GUIA_CORTES.md` e `01_ROTEIROS_OTIMIZADOS.md`. Isso não representa medição de retenção dos novos roteiros.")

# Índice longo: contagens e links atuais, sem modificar o L02.
index_path = P / "00_ROTEIROS_L02_EM_DIANTE.md"
index_text = read(index_path)
for entry in entries[:6]:
    ident = entry["id"]
    index_text = re.sub(rf"^\| {ident} \| \d+ \| \d+ \|[^\n]+", f"| {ident} | {entry['palavras']} | {entry['paragrafos']} | {entry['palavras']/155:.1f}–{entry['palavras']/140:.1f} min |", index_text, flags=re.M)
    index_text = index_text.replace(f"({ident}/01_NARRACAO.txt) |", f"({ident}/01_NARRACAO.txt) · [Gemini]({ident}/03_NARRACAO_GEMINI.txt) · [Style]({ident}/04_ESTILO_GEMINI.txt) |")
    index_text = index_text.replace(f"[Abrir direção]({ident}/02_DIRECAO_E_FONTES.md)", f"[Direção atual]({ident}/05_DIRECAO_HUMOR_BR.md) · [Fontes]({ident}/02_DIRECAO_E_FONTES.md)")
index_text = re.sub(r"L04 é intencionalmente.*?(?=\n\n)", "As estimativas excluem eventos e precisam ser medidas na locução. A abertura entrega uma observação antes da apresentação do canal; variar interpretação pelo sentido, sem acelerar para cumprir uma duração fixa.", index_text, count=1, flags=re.S)
index_text = re.sub(r"\[Abrir os roteiros dos Shorts.*?(?=\n\n)", "[Shorts e direção](cortes/00_GUIA_CORTES.md): C03–C12 revisados em 29/10/2026. O guia traz contagens atuais, eventos e estimativas. As cópias de produção e o consolidado foram sincronizados.", index_text, count=1, flags=re.S)
write(index_path, "**Atualização de 29/10/2026:** L03–L08 e C03–C12 usam o perfil de humor brasileiro. [Entrega](editorial/revisao_humor_2026-10-29/LEIA_ME.md). Os textos são atuais; áudio/vídeo previamente produzidos pertencem à versão anterior. L03 publicado preservado.\n\n" + index_text)
short_index = P / "shorts/00_COMECE_AQUI.md"
short_text = read(short_index)
for ident in shorts:
    short_text = re.sub(rf"^(\| {ident} \|[^\n]*?)\| validado \|$", r"\1| mídia anterior; roteiro revisado, nova produção pendente |", short_text, flags=re.M)
write(short_index, "**Revisão de 29/10/2026:** C03–C12 têm texto novo em `voz/NARRACAO.txt` e `voz/GEMINI.txt`. As durações e os links de MP4 abaixo pertencem à edição anterior; não representam a versão com humor. Consultar o aviso de revisão em cada pasta antes da produção.\n\n" + short_text)

for relative, expected in protected_hashes.items():
    assert sha(ROOT / relative) == expected, relative
for entry in entries:
    assert sha(ROOT / entry['narracao']) == entry['sha256_narracao']
    assert sha(ROOT / entry['gemini']) == entry['sha256_gemini']
    if entry['id'].startswith('C'):
        base = P / 'shorts' / entry['id'] / 'voz'
        assert read(base / 'NARRACAO.txt') == read(ROOT / entry['narracao'])
        assert read(base / 'GEMINI.txt') == read(ROOT / entry['gemini'])

manifest = {"data": "2026-10-29", "modelo": "gemini-3.8-flash-tts", "voz": "voice_iagtq1gnk2br",
    "estado": "textos_validados_sem_geracao_de_audio", "quantidade": len(entries),
    "backup": rel(BACKUP), "arquivos_backup": len(backup_records), "protegidos_conferidos": len(protected_hashes),
    "tags_documentadas": sorted(allowed), "roteiros": entries}
write(MARKER, json.dumps(manifest, ensure_ascii=False, indent=2))
print(json.dumps({"roteiros": entries, "backup_verificado": len(backup_records), "arquivos_preservados_conferidos": len(protected_hashes), "tags_documentadas": len(allowed)}, ensure_ascii=False, indent=2))
