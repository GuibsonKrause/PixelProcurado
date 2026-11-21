from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "videosGTAVI"
CATALOG = ROOT / "_catalogo"
DATA = CATALOG / "inventario_midia.json"
OUTPUT = CATALOG / "GALERIA.html"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def card(item: dict) -> str:
    relative = str(item["relative_path"]).replace("\\", "/")
    src = "../" + relative
    media_type = item.get("media_type", "")
    if media_type == "image":
        preview = f'<a href="{esc(src)}"><img loading="lazy" src="{esc(src)}" alt="{esc(item.get("subject"))}"></a>'
    else:
        preview = (
            '<div class="video-placeholder">'
            '<span>VÍDEO</span>'
            f'<strong>{esc(item.get("duration_seconds"))} s</strong>'
            f'<a href="{esc(src)}">Abrir arquivo</a>'
            '</div>'
        )
    search = " ".join(
        str(item.get(k, ""))
        for k in ("id", "relative_path", "category", "subject", "variant", "orientation", "recommended_use")
    ).lower()
    return f'''
    <article class="card" data-type="{esc(media_type)}" data-orientation="{esc(item.get('orientation'))}" data-search="{esc(search)}">
      {preview}
      <div class="content">
        <div class="eyebrow">{esc(item.get('id'))} · {esc(item.get('category'))}</div>
        <h2>{esc(item.get('subject'))}</h2>
        <p class="path">{esc(relative)}</p>
        <div class="chips"><span>{esc(item.get('variant'))}</span><span>{esc(item.get('orientation'))}</span><span>{esc(item.get('width'))}×{esc(item.get('height'))}</span></div>
        <p>{esc(item.get('recommended_use'))}</p>
      </div>
    </article>'''


def main() -> None:
    items = json.loads(DATA.read_text(encoding="utf-8"))
    cards = "\n".join(card(item) for item in items)
    document = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Catálogo visual GTA VI</title>
  <style>
    :root {{ color-scheme: dark; --bg:#0b0b10; --panel:#171720; --line:#2b2b38; --text:#f6f3ff; --muted:#aaa5b5; --accent:#ff66c4; }}
    * {{ box-sizing:border-box }}
    body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.45 system-ui,Segoe UI,sans-serif }}
    header {{ position:sticky; top:0; z-index:5; padding:18px 24px; background:#0b0b10ed; backdrop-filter:blur(12px); border-bottom:1px solid var(--line) }}
    h1 {{ margin:0 0 12px; font-size:24px }}
    .controls {{ display:flex; gap:10px; flex-wrap:wrap }}
    input,select {{ border:1px solid var(--line); background:var(--panel); color:var(--text); border-radius:9px; padding:10px 12px }}
    input {{ flex:1; min-width:260px }}
    #count {{ align-self:center; color:var(--muted) }}
    main {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(310px,1fr)); gap:16px; padding:20px }}
    .card {{ overflow:hidden; border:1px solid var(--line); border-radius:14px; background:var(--panel) }}
    .card[hidden] {{ display:none }}
    img {{ display:block; width:100%; height:210px; object-fit:cover; background:#050508 }}
    .content {{ padding:14px }}
    .eyebrow {{ color:var(--accent); font-size:12px; text-transform:uppercase; letter-spacing:.06em }}
    h2 {{ margin:5px 0; font-size:18px }}
    p {{ margin:9px 0 }}
    .path {{ color:var(--muted); font:12px/1.35 ui-monospace,Consolas,monospace; overflow-wrap:anywhere }}
    .chips {{ display:flex; flex-wrap:wrap; gap:6px }}
    .chips span {{ padding:3px 7px; border:1px solid var(--line); border-radius:999px; color:var(--muted); font-size:12px }}
    .video-placeholder {{ height:210px; display:grid; place-content:center; gap:8px; text-align:center; background:linear-gradient(135deg,#24142a,#17172c) }}
    .video-placeholder span {{ color:var(--accent); font-weight:800; letter-spacing:.2em }}
    .video-placeholder a {{ color:white }}
  </style>
</head>
<body>
  <header>
    <h1>Catálogo visual GTA VI · 309 arquivos</h1>
    <div class="controls">
      <input id="search" type="search" placeholder="Pesquisar personagem, lugar, formato, arquivo ou uso…">
      <select id="type"><option value="">Todos os tipos</option><option value="image">Imagens</option><option value="video">Vídeos</option></select>
      <select id="orientation"><option value="">Todas as orientações</option><option value="paisagem">Paisagem</option><option value="vertical">Vertical</option><option value="quadrado">Quadrado</option></select>
      <span id="count"></span>
    </div>
  </header>
  <main>{cards}</main>
  <script>
    const cards=[...document.querySelectorAll('.card')];
    const search=document.querySelector('#search'), type=document.querySelector('#type'), orientation=document.querySelector('#orientation'), count=document.querySelector('#count');
    function filter() {{
      const q=search.value.trim().toLowerCase(); let visible=0;
      for (const card of cards) {{
        const ok=(!q||card.dataset.search.includes(q))&&(!type.value||card.dataset.type===type.value)&&(!orientation.value||card.dataset.orientation===orientation.value);
        card.hidden=!ok; if(ok) visible++;
      }}
      count.textContent=visible+' arquivo'+(visible===1?'':'s');
    }}
    search.addEventListener('input',filter); type.addEventListener('change',filter); orientation.addEventListener('change',filter); filter();
  </script>
</body>
</html>'''
    OUTPUT.write_text(document, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
