"""Incorpora a solicitação de ganchos curtos e confere a entrega sem gerar áudio."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P = ROOT / 'producao'
mp = HERE / 'manifesto_revisao.json'
manifest = json.loads(mp.read_text(encoding='utf-8'))
assert not manifest.get('ganchos_3s'), 'Ganchos já aplicados; preservar edições posteriores.'

def read(path):
    return path.read_text(encoding='utf-8-sig')

def write(path, text):
    path.write_text(text.strip() + '\n', encoding='utf-8')

def clean(text):
    return '\n\n'.join(re.sub(r'[ \t]+', ' ', re.sub(r'<[^>]+>', '', para)).strip() for para in text.strip().split('\n\n'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

hooks = {
    'L03': 'Vice City muda. A vaidade continua.',
    'L04': 'Essa cena é gameplay ou cinema?',
    'L05': 'O carro distrai. Olha a rua.',
    'L06': 'Esse paraíso também sabe dar medo.',
    'L07': 'GTA faz você gostar de propaganda.',
    'L08': 'O aluguel grátis veio cobrar Jason.',
    'C03': 'Esse abraço tem polícia no fundo.',
    'C04': 'Sua nostalgia de GTA tem truque.',
    'C05': 'Gameplay confirmado. Mas qual dessas cenas?',
    'C06': 'Estão avaliando gráficos no pôster.',
    'C07': 'O detalhe está fora do carro.',
    'C08': 'A iguana já virou síndica daqui.',
    'C09': 'Mesma água. Outro nível de desconfiança.',
    'C10': 'GTA colocou propaganda na sua playlist.',
    'C11': 'Jason mora grátis. Mas tem cobrança.',
    'C12': 'Raul sabe roubar. Mas sabe parar?',
}
replace_prefix = {
    'C03': 'O abraço de Jason e Lucia muda quando você afasta a imagem. ',
    'C04': 'Vice City guarda duas épocas, e a saudade acrescenta outra. ',
    'C05': 'GTA seis tem gameplay no Trailer dois. Mas quais cenas? ',
    'C06': '',
    'C07': 'O carro azul chama atenção, mas olha a rua de GTA seis. ',
    'C08': 'Uma iguana virou a dona da rua nas Leonida Keys. ',
    'C09': 'A água muda de clima entre as Keys e Grassrivers. ',
    'C10': 'A Self Radio pode colocar anúncio na sua própria playlist. ',
    'C11': 'Jason mora de graça, mas a ajuda tem contrapartida. ',
    'C12': 'Raul tem experiência. Isso não significa que escolhe riscos menores. ',
}
visuals = {
    'L03': 'Real Dimez e celulares; detalhe visível já no primeiro quadro.',
    'L04': 'Trecho do Trailer 2 identificado; pergunta sobre controle, sem classificar a cena por conta própria.',
    'L05': 'Carro azul e rua inteira; destacar moto e pilares, sem começar com zoom que esconda a evidência.',
    'L06': 'Contraste Keys/Grassrivers; água aberta e vegetação fechada.',
    'L07': 'Cartela própria: GTA V / PC / Self Radio; playlist → locutor/anúncio.',
    'L08': 'Brian e Jason; cartela moradia ↔ cobranças.',
    'C03': 'Arte completa de Jason/Lucia; polícia visível antes do recorte romântico.',
    'C04': 'Vice City clássico; preparar cartelas 1986 / 2002 / sua época.',
    'C05': 'Trailer 2 identificado; não usar um plano como prova isolada de gameplay.',
    'C06': 'Arte oficial identificada como ilustração; depois a categoria na biblioteca.',
    'C07': 'Foto inteira de Vice_City_09; destaque discreto no entorno.',
    'C08': 'Iguana de Leonida_Keys_02 em evidência; síndica é piada, não mecânica.',
    'C09': 'Keys e Grassrivers lado a lado, sem sugerir distâncias no mapa.',
    'C10': 'Cartela Self Radio / GTA V / PC; não mostrar GTA VI como se tivesse o recurso.',
    'C11': 'Jason/Brian e a troca moradia/cobranças; sem inventar despejo.',
    'C12': 'Raul; experiência e risco, sem simular missão inédita.',
}
consolidated = read(P / 'cortes/01_ROTEIROS_OTIMIZADOS.md')
snapshot = read(HERE / 'SHORTS_GEMINI.md')
index_text = read(P / '00_ROTEIROS_L02_EM_DIANTE.md')
cutguide = read(P / 'cortes/00_GUIA_CORTES.md')

for entry in manifest['roteiros']:
    ident = entry['id']
    gp, pp = ROOT / entry['gemini'], ROOT / entry['narracao']
    tagged, previous = read(gp).strip(), read(pp).strip()
    hook = hooks[ident]
    assert len(hook.split()) <= 6, (ident, hook)
    if ident == 'L05':
        paragraphs = tagged.split('\n\n')
        paragraphs[0] = hook + ' Na foto de GTA seis, tem moto empinando e pilares pintados atrás do carro azul. A graça também está no bairro. Olhar só a lataria é deixar metade da conversa fora do quadro.'
        paragraphs[1] = 'Vamos comparar seis fotos oficiais, em três pares: praia, carros e vista aérea. Dá pra perceber bastante coisa sem transformar um print numa disputa de console.'
        tagged = '\n\n'.join(paragraphs)
    elif ident.startswith('L'):
        tagged = hook + ' ' + tagged
    else:
        prefix = replace_prefix[ident]
        assert tagged.startswith(prefix), ident
        tagged = hook + ' ' + tagged[len(prefix):]
        if ident == 'C04':
            tagged = tagged.replace('O jogo saiu', 'Vice City saiu', 1)
        elif ident == 'C05':
            tagged = tagged.replace('A Rockstar descreve aquele vídeo', 'A Rockstar descreve o Trailer dois de GTA seis', 1)
        elif ident == 'C07':
            tagged = tagged.replace(hook + ' Tem moto', hook + ' Na imagem de GTA seis, tem moto', 1)
        elif ident == 'C08':
            tagged = tagged.replace('Pelo menos é a impressão dessa imagem:', 'Pelo menos é a impressão dessa imagem das Leonida Keys:', 1)
        elif ident == 'C12':
            tagged = tagged.removesuffix('É por isso que...') + 'Afinal...'
    text = clean(tagged)
    write(gp, tagged)
    write(pp, text)
    previous_tagged = re.search(rf'^## {ident}\n\n(.*?)(?=^## C\d{{2}}\n|\Z)', snapshot, re.M | re.S) if ident.startswith('C') else None
    if ident.startswith('C'):
        assert previous in consolidated, ident
        consolidated = consolidated.replace(previous, text, 1)
        snapshot = snapshot[:previous_tagged.start(1)] + tagged + '\n\n' + snapshot[previous_tagged.end(1):]
        base = P / 'shorts' / ident / 'voz'
        write(base / 'NARRACAO.txt', text)
        write(base / 'GEMINI.txt', tagged)
    entry.update(palavras=len(text.split()), paragrafos=len(text.split('\n\n')), eventos=dict(Counter(re.findall(r'<([^>]+)>', tagged))), sha256_narracao=sha(pp), sha256_gemini=sha(gp),
        gancho=hook, palavras_gancho=len(hook.split()), segundos_gancho_sem_pausas=[round(len(hook.split())*60/155, 2), round(len(hook.split())*60/140, 2)])
    n = entry['palavras']
    assert 160 <= n <= 450 if ident.startswith('C') else 600 <= n <= 1100
    assert clean(read(gp)) == read(pp).strip()
    if ident.startswith('L'):
        direction = P / ident / '05_DIRECAO_HUMOR_BR.md'
        d = read(direction)
        d = re.sub(r'Revisão de 29/10/2026\..*?Duração não medida em áudio\.', f"Revisão de 29/10/2026. {n} palavras, {entry['paragrafos']} parágrafos. Leitura estimada: {n/155:.1f}–{n/140:.1f} minutos, antes de pausas. Duração não medida em áudio.", d, count=1)
        event_rows = []
        for i, para in enumerate(tagged.split('\n\n'), 1):
            tags = re.findall(r'<[^>]+>', para)
            if tags:
                excerpt = ' '.join(clean(para).split()[:13]) + '…'
                event_rows.append(f"| {i} | {excerpt} | {'; '.join('`' + t + '`' for t in tags)} |")
        d = re.sub(r'\| Parágrafo \| Início da fala.*?(?=\n\n)', '| Parágrafo | Início da fala | Eventos |\n|---|---|---|\n' + '\n'.join(event_rows), d, count=1, flags=re.S)
        d += f"\n\n## Entrada de até três segundos\n\n**{hook}** {visuals[ident]} Começar a fala no primeiro quadro, sem vinheta ou evento antes do gancho. Estimativa verbal de {entry['segundos_gancho_sem_pausas'][0]}–{entry['segundos_gancho_sem_pausas'][1]} s; conferir pausas e duração no áudio. A frase seguinte entrega a evidência.\n"
        write(direction, d)
        index_text = re.sub(rf'^\| {ident} \| \d+ \| \d+ \|[^\n]+', f"| {ident} | {n} | {entry['paragrafos']} | {n/155:.1f}–{n/140:.1f} min |", index_text, flags=re.M)
    else:
        cutguide = re.sub(rf'^\| {ident} \| \d+ \| \d+ \|[^\n]+', f"| {ident} | {n} | {sum(entry['eventos'].values())} | {n/155:.2f}–{n/140:.2f} min |", cutguide, flags=re.M)

index_text = index_text.replace('Uma imagem destaca o ciclista; a outra distribui pequenas situações pela praia.', 'O carro azul chama atenção; motos e pilares pintados revelam a participação do bairro.')
write(P / '00_ROTEIROS_L02_EM_DIANTE.md', index_text)
write(P / 'cortes/01_ROTEIROS_OTIMIZADOS.md', consolidated)
write(HERE / 'SHORTS_GEMINI.md', snapshot)
write(P / 'cortes/00_GUIA_CORTES.md', cutguide + '\n\n## Primeiros três segundos\n\nAs aberturas têm cinco ou seis palavras, sem eventos antes da entrega. [Ganchos e direção visual por vídeo](../editorial/revisao_humor_2026-10-29/GANCHOS_3_SEGUNDOS.md). Começar no primeiro quadro; medir a locução antes de montar. A retenção ainda não foi medida.\n')

hook_table = '\n'.join(f"| {e['id']} | {e['gancho']} | {e['palavras_gancho']} | {e['segundos_gancho_sem_pausas'][0]}–{e['segundos_gancho_sem_pausas'][1]} s | {visuals[e['id']]} |" for e in manifest['roteiros'])
write(HERE / 'GANCHOS_3_SEGUNDOS.md', '# Primeiros três segundos — direção atual\n\nOs 16 textos começam com cinco ou seis palavras que apresentam contraste, descoberta ou pergunta. A explicação vem imediatamente, sem vinheta. Estimativas a 140–155 palavras/minuto, sem somar pausas: precisam ser medidas no áudio final. O gancho foi escrito para caber nos três primeiros segundos; não é garantia de retenção.\n\n| ID | Primeira fala | Palavras | Tempo verbal estimado | Imagem de abertura |\n|---|---|---:|---|---|\n' + hook_table + '\n\nNa produção, iniciar a voz no primeiro quadro. Se a frase ultrapassar três segundos, reduzir pausas ou reescrever antes de acelerar artificialmente. Não inserir respiração ou risada antes da descoberta. Mostrar a evidência da afirmação já na abertura. Sem susto sonoro, contagem regressiva, logo ou promessa que o restante não cumpre. Conferir especialmente o reinício dos Shorts, ligando a ponte final a esta primeira fala.\n')

future = '\n\n## Regra de abertura — atualização solicitada em 29/10/2026\n\nProjetar os primeiros três segundos com uma fala de cerca de cinco ou seis palavras que já entregue uma descoberta, contraste ou pergunta concreta. Começar a voz no primeiro quadro e mostrar uma evidência; a frase seguinte deve desenvolver ou responder o gancho. Sem apresentação do canal, vinheta, respiração ou risada antes dele. Medir o tempo real na locução e ajustar o texto se não couber, sem impor leitura corrida. A meta de três segundos é de construção; retenção depende de medição com público. Exemplos atuais em `editorial/revisao_humor_2026-10-29/GANCHOS_3_SEGUNDOS.md` (a partir da pasta producao).\n'
for path in [P / 'GUIA_ROTEIROS_RETENCAO.md', P / 'editorial/PERFIL_NARRACAO.md', P / 'AGENTS.md']:
    write(path, read(path) + future)

# Usar o ambiente já configurado do projeto; não instalar pacotes nem chamar a API.
dry_runs = []
for kind in ['L', 'C']:
    selected = [e for e in manifest['roteiros'] if e['id'].startswith(kind)]
    style_file = P / ('editorial/ESTILO_NARRACAO_HUMOR_BR.txt' if kind == 'L' else 'cortes/00_ESTILO_GEMINI_SHORTS.txt')
    command = [str(ROOT / '.venv-gemini/Scripts/python.exe'), str(ROOT / 'automacao/gemini_tts.py')] + [e['gemini'] for e in selected] + ['--style-file', str(style_file), '--dry-run']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    write(HERE / f'DRY_RUN_{kind}.txt', result.stdout + '\n' + result.stderr)
    assert result.returncode == 0, result.stderr
    dry_runs.append({'formato': kind, 'quantidade': len(selected), 'exit_code': result.returncode, 'api_chamada': False})

backup = P / 'historico/antes_humor_br_2026-10-29'
records = json.loads(read(backup / 'manifesto_backup.json'))
assert all(sha(backup / rec['path']).upper() == rec['sha256'].upper() for rec in records)
for entry in manifest['roteiros']:
    if entry['id'].startswith('C'):
        base = P / 'shorts' / entry['id'] / 'voz'
        assert read(base / 'NARRACAO.txt') == read(ROOT / entry['narracao'])
        assert read(base / 'GEMINI.txt') == read(ROOT / entry['gemini'])
    tags = re.findall(r'<([^>]+)>', read(ROOT / entry['gemini']))
    assert set(tags) <= set(manifest['tags_documentadas'])
    assert '<' not in read(ROOT / entry['gemini'])[:len(entry['gancho'])]
manifest.update(ganchos_3s=True, dry_runs=dry_runs)
write(mp, json.dumps(manifest, ensure_ascii=False, indent=2))
print(json.dumps({'roteiros': len(manifest['roteiros']), 'ganchos': {k: len(v.split()) for k, v in hooks.items()}, 'dry_runs': dry_runs, 'backup_verificado': len(records)}, ensure_ascii=False, indent=2))
