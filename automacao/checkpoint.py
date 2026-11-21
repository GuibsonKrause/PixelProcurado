"""producao.json padrao (schema_versao 1): criar, validar, atualizar etapa e migrar checkpoints antigos.

  py -3.12 automacao/checkpoint.py novo producao/L09 --id L09 --formato longo --roteiro producao/L09/01_NARRACAO.txt
  py -3.12 automacao/checkpoint.py validar producao/L09
  py -3.12 automacao/checkpoint.py etapa producao/L09 narracao --status validado --campo medicoes.duracao_s=335.8 [--sub longo]
  py -3.12 automacao/checkpoint.py migrar producao/L05 [--mostrar] [--aplicar]
"""
import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parent
sys.path.insert(0, str(AQUI))
from _schema_mini import validar as validar_schema  # noqa: E402

SCHEMA = json.loads((AQUI / 'schemas/producao.schema.json').read_text(encoding='utf-8'))
ETAPAS = list(SCHEMA['properties']['etapas']['properties'])
ESTADOS = SCHEMA['$defs']['estado']['enum']


def agora():
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')


def arquivo_de(alvo):
    p = Path(alvo)
    return p / 'producao.json' if p.is_dir() or p.suffix != '.json' else p


def ler(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def gravar(p, dado):
    """Escrita atomica: arquivo temporario + replace."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(tmp, p)


def etapa_vazia():
    return {'status': 'pendente'}


def proxima_etapa(dado):
    for e in ETAPAS:
        if dado['etapas'].get(e, {}).get('status') != 'validado':
            return e
    return 'concluido'


# ---------- novo ----------
def cmd_novo(a):
    destino = Path(a.pasta) / 'producao.json'
    if destino.exists():
        sys.exit(f'Erro: {destino} ja existe (nao sobrescrevo).')
    if a.formato == 'longo_e_short':
        roteiro = dict(r.split('=', 1) for r in a.roteiro if r.partition('=')[0] in ('longo', 'short'))
        if set(roteiro) != {'longo', 'short'}:
            sys.exit('Erro: em longo_e_short use --roteiro longo=<path> --roteiro short=<path>.')
    elif len(a.roteiro) != 1:
        sys.exit('Erro: informe exatamente um --roteiro <path>.')
    else:
        roteiro = a.roteiro[0]
    dado = {'schema_versao': 1, 'id': a.id, 'formato': a.formato, 'roteiro_origem': roteiro,
            'etapa_atual': ETAPAS[0], 'status': 'em_andamento', 'data_criacao': agora(),
            'etapas': {e: etapa_vazia() for e in ETAPAS}}
    if a.formato == 'longo_e_short':
        for e in ETAPAS:
            dado['etapas'][e].update(longo=etapa_vazia(), short=etapa_vazia())
    gravar(destino, dado)
    print(f'Criado {destino}')


# ---------- validar ----------
def resolver(caminho, pasta):
    for base in (ROOT, pasta):
        p = base / caminho
        if p.exists():
            return p
    return None


def caminhos(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from caminhos(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from caminhos(x)


def conferir_etapa(nome, e, pasta, erros):
    if e.get('status') == 'validado':
        for c in caminhos(e.get('artefatos', {})):
            if not re.match(r'^[a-z]+://', c) and not resolver(c, pasta):
                erros.append(f'etapas.{nome}: artefato inexistente: {c}')
        if e.get('relatorio') and not resolver(e['relatorio'], pasta):
            erros.append(f'etapas.{nome}: relatorio inexistente: {e["relatorio"]}')
    for sub in ('longo', 'short'):
        if isinstance(e.get(sub), dict):
            conferir_etapa(f'{nome}.{sub}', e[sub], pasta, erros)


def validar_dado(dado, pasta):
    erros = validar_schema(dado, SCHEMA)
    if erros:
        return erros
    for r in caminhos(dado['roteiro_origem']):
        if not resolver(r, pasta):
            erros.append(f'roteiro_origem inexistente: {r}')
    for nome, e in dado['etapas'].items():
        conferir_etapa(nome, e, pasta, erros)
    esperado = proxima_etapa(dado)
    if dado['etapa_atual'] != esperado:
        erros.append(f'etapa_atual={dado["etapa_atual"]!r}, mas a primeira etapa nao validada e {esperado!r}')
    if dado['etapas']['revisao_final']['status'] == 'validado' and not (pasta / 'REVISAO_FINAL.json').exists():
        erros.append('revisao_final validada sem REVISAO_FINAL.json (veja automacao/validar_revisao.py)')
    return erros


def cmd_validar(a):
    arq = arquivo_de(a.alvo)
    if not arq.exists():
        sys.exit(f'Erro: {arq} nao encontrado.')
    erros = validar_dado(ler(arq), arq.parent)
    for e in erros:
        print('ERRO:', e)
    print(f'{arq}: ' + (f'{len(erros)} erro(s)' if erros else 'valido'))
    return 1 if erros else 0


# ---------- etapa ----------
def valor(txt):
    try:
        return json.loads(txt)
    except ValueError:
        return txt


def cmd_etapa(a):
    arq = arquivo_de(a.pasta)
    dado = ler(arq)
    if a.etapa not in dado['etapas']:
        sys.exit(f'Erro: etapa desconhecida {a.etapa!r}. Validas: {", ".join(ETAPAS)}')
    alvo = dado['etapas'][a.etapa]
    if a.sub:
        alvo = alvo.setdefault(a.sub, etapa_vazia())
    if a.status:
        alvo['status'] = a.status
    for c in a.campo:
        chave, sep, v = c.partition('=')
        if not sep:
            sys.exit(f'Erro: --campo espera chave=valor, recebi {c!r}')
        *pai, folha = chave.split('.')
        d = alvo
        for p in pai:
            d = d.setdefault(p, {})
        d[folha] = valor(v)
    alvo['atualizado_em'] = dado['atualizado_em'] = agora()
    dado['etapa_atual'] = proxima_etapa(dado)
    dado['status'] = 'validado' if dado['etapa_atual'] == 'concluido' else 'em_andamento'
    erros = validar_schema(dado, SCHEMA)
    if erros:
        sys.exit('Erro: resultado invalido, nada gravado:\n' + '\n'.join(erros))
    gravar(arq, dado)
    print(f'{a.etapa}{"." + a.sub if a.sub else ""} -> {alvo["status"]}; etapa_atual = {dado["etapa_atual"]}')


# ---------- migrar ----------
REGRAS = [('revis', 'revisao_final'), ('thumb', 'thumbnail'), ('capa', 'thumbnail'), ('seo', 'publicacao_pacote'),
          ('pacote', 'publicacao_pacote'), ('narracao', 'narracao'), ('audio', 'narracao'), ('alinh', 'alinhamento'),
          ('montagem', 'montagem'), ('timeline', 'montagem'), ('hyperframes', 'montagem'), ('voz', 'narracao'), ('edicao', 'montagem'), ('direcao', 'montagem'), ('amostra', 'montagem'),
          ('render', 'render'), ('exporta', 'render'), ('video', 'render'), ('legenda', 'render'), ('srt', 'render'),
          ('postiz', 'distribuicao'), ('agendamento', 'distribuicao'), ('distribuic', 'distribuicao'),
          ('publicacao', 'distribuicao')]
EXEC = {'model_solicitado': 'model_solicitado', 'reasoning_effort_solicitado': 'reasoning_effort_solicitado',
        'agent_id': 'agent_id', 'model_efetivo': 'model_efetivo', 'modelo_efetivo': 'model_efetivo'}
META_TOP = {'id', 'titulo', 'formato', 'roteiro_origem', 'etapa_atual', 'data_criacao', 'agendamento_alvo'}
TOPO_COMO_ETAPA = set(ETAPAS) | {'agendamento'}


def classificar(chave):
    k = chave.lower()
    sub = 'longo' if re.search(r'(^|_)long[oa]?($|_)', k) else 'short' if re.search(r'(^|_)short($|_)', k) else None
    for trecho, etapa in REGRAS:
        if trecho in k:
            return etapa, sub
    return None, sub


def estado_de(txt):
    t = str(txt).lower()
    if any(x in t for x in ('validado', 'aprovado', 'pass', 'conclu', 'queue', 'scheduled', 'agendad', 'publicad')):
        return 'validado'
    if 'andamento' in t:
        return 'em_andamento'
    return 'bloqueado' if 'bloque' in t else 'pendente'


def parece_caminho(v):
    return (isinstance(v, str) and not re.match(r'^([a-z]+://|\d{4}-\d\d-\d\d)', v) and ' ' not in v.strip()
            and bool(re.search(r'/|\.[A-Za-z]\w{1,3}$', v)))


def converter(d, herdado=None):
    """dict de etapa antiga -> etapa nova (artefatos/medicoes/executor; resto em 'legado')."""
    out, ex, art, med, leg = {}, {}, {}, {}, {}
    for k, v in d.items():
        if k in ('status', 'estado'):
            continue
        if k in EXEC and isinstance(v, str):
            ex[EXEC[k]] = v
        elif k in ('longo', 'short') and isinstance(v, dict):
            out[k] = converter(v, d.get('status', d.get('estado', herdado)))
        elif k == 'relatorio' and isinstance(v, str):
            out[k] = v
        elif parece_caminho(v) or (isinstance(v, list) and v and all(parece_caminho(x) for x in v)):
            art[k] = v
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            med[k] = v
        else:
            leg[k] = v
    bruto = next((d[k] for k in ('status', 'estado', 'resultado') if k in d), herdado)
    if bruto is None:
        subs = [out[s]['status'] for s in ('longo', 'short') if s in out]
        out['status'] = ('validado' if subs and all(x == 'validado' for x in subs) else
                         'em_andamento' if any(x != 'pendente' for x in subs) else 'pendente')
    else:
        out['status'] = estado_de(bruto)
        if out['status'] != 'validado' and str(bruto).lower() != out['status']:
            leg['estado_original'] = bruto
    for nome, v in (('executor', ex), ('artefatos', art), ('medicoes', med), ('legado', leg)):
        if v:
            out[nome] = v
    return out


def juntar(atual, novo):
    """Mescla duas etapas antigas que caem na mesma etapa nova (sem sub-entrada)."""
    atual['status'] = ('validado' if atual['status'] == novo['status'] == 'validado' else
                       'pendente' if atual['status'] == novo['status'] == 'pendente' else 'em_andamento')
    for k, v in novo.items():
        if isinstance(v, dict) and isinstance(atual.get(k), dict):
            atual[k].update({x: y for x, y in v.items() if x not in atual[k]})
        else:
            atual.setdefault(k, v)


def migrar_dado(velho, pasta):
    pend = []
    novo = {'schema_versao': 1, 'id': velho.get('id', pasta.name), 'etapas': {e: None for e in ETAPAS}}
    for k in ('titulo', 'data_criacao', 'agendamento_alvo'):
        if k in velho:
            novo[k] = velho[k]
    fm = str(velho.get('formato', '')).lower()
    novo['formato'] = ('longo_e_short' if 'longo_e_short' in fm or ('short' in fm and 'long' in fm)
                       else 'short' if 'short' in fm else 'longo')
    if not fm:
        pend.append('formato ausente: assumido "longo"')
    novo['roteiro_origem'] = velho.get('roteiro_origem') or ''
    if not novo['roteiro_origem']:
        pend.append('roteiro_origem ausente')
    legado = {k: v for k, v in velho.items() if k not in META_TOP and k != 'etapas'}
    legado['formato_original'] = velho.get('formato')
    legado['etapa_atual_original'] = velho.get('etapa_atual')

    fontes = []  # (etapa_nova, sub, dict_antigo)
    for k, v in velho.get('etapas', {}).items():
        et, sub = classificar(k)
        if isinstance(v, dict) and et:
            fontes.append((et, sub, v))
        else:
            legado.setdefault('etapas_nao_mapeadas', {})[k] = v
            pend.append(f'etapa antiga sem equivalente (guardada em legado): {k}')
    for k in [k for k, v in velho.items() if k in TOPO_COMO_ETAPA and isinstance(v, dict) and k != 'etapas']:
        et, sub = classificar(k)
        fontes.append((et, sub, velho[k]))
        legado.pop(k, None)
    if isinstance(velho.get('artefatos'), dict):  # lista plana: distribui por nome da chave
        legado.pop('artefatos')
        for k, v in velho['artefatos'].items():
            et, _ = classificar(k)
            if et and parece_caminho(v):
                fontes.append((et, None, {'status': 'pendente', k: v}))
            else:
                legado.setdefault('artefatos_nao_classificados', {})[k] = v

    for et, sub, d in fontes:
        conv = converter(d)
        if et == 'revisao_final' and conv['status'] == 'validado':
            # sem REVISAO_FINAL.json com evidencias nao ha como validar
            conv['status'] = 'pendente'
            conv.setdefault('legado', {})['aprovacao_antiga_sem_evidencia'] = d
            pend.append('revisao_final: aprovacao antiga sem evidencias; refazer com validar_revisao.py')
        atual = novo['etapas'][et]
        if sub:
            atual = atual or etapa_vazia()
            atual[sub] = conv
            subs = [atual[s]['status'] for s in ('longo', 'short') if s in atual]
            atual['status'] = 'validado' if all(x == 'validado' for x in subs) else 'em_andamento'
            novo['etapas'][et] = atual
        elif atual is None:
            novo['etapas'][et] = conv
        else:
            juntar(atual, conv)

    for e, v in novo['etapas'].items():
        if v is None:
            novo['etapas'][e] = etapa_vazia()
            pend.append(f'etapa {e}: sem dados no checkpoint antigo (pendente)')
        elif v['status'] == 'pendente' and v.get('artefatos'):
            pend.append(f'etapa {e}: ha artefatos mas nenhum estado registrado (confirmar e marcar validado)')
    novo['etapa_atual'] = proxima_etapa(novo)
    novo['status'] = 'validado' if novo['etapa_atual'] == 'concluido' else 'em_andamento'
    novo['legado'] = {k: v for k, v in legado.items() if v is not None}
    novo['atualizado_em'] = agora()
    return novo, pend, validar_dado(novo, pasta)


def cmd_migrar(a):
    arq = arquivo_de(a.pasta)
    velho = ler(arq)
    if velho.get('schema_versao') == 1:
        sys.exit('Ja esta no formato novo (schema_versao 1).')
    novo, pend, erros = migrar_dado(velho, arq.parent)
    ev = {e: (v['status'] + (f' (longo={v["longo"]["status"]}, short={v["short"]["status"]})' if 'longo' in v and 'short' in v else ''))
          for e, v in novo['etapas'].items()}
    print(json.dumps(novo, ensure_ascii=False, indent=2) if a.mostrar else f'{arq}\n  formato={novo["formato"]} etapa_atual={novo["etapa_atual"]}')
    for e, s in ev.items():
        print(f'  {e}: {s}')
    print('PENDENCIAS (decisao humana):')
    print('\n'.join(f'  - {p}' for p in pend + ['validacao: ' + x for x in erros]) or '  nenhuma')
    if not a.aplicar:
        print('(dry-run: use --aplicar para gravar)')
        return
    bkp = arq.with_name('producao.v0.json')
    if bkp.exists():
        sys.exit(f'Erro: backup {bkp} ja existe; nada gravado.')
    bkp.write_text(arq.read_text(encoding='utf-8'), encoding='utf-8')
    gravar(arq, novo)
    print(f'Gravado {arq} (backup: {bkp.name}).')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    n = sp.add_parser('novo')
    n.add_argument('pasta')
    n.add_argument('--id', required=True)
    n.add_argument('--formato', choices=('longo', 'short', 'longo_e_short'), required=True)
    n.add_argument('--roteiro', action='append', required=True, help='path (ou longo=path / short=path)')
    v = sp.add_parser('validar')
    v.add_argument('alvo')
    e = sp.add_parser('etapa')
    e.add_argument('pasta')
    e.add_argument('etapa')
    e.add_argument('--status', choices=ESTADOS)
    e.add_argument('--sub', choices=('longo', 'short'))
    e.add_argument('--campo', action='append', default=[], help='chave=valor (aceita pontos: medicoes.lufs=-16)')
    m = sp.add_parser('migrar')
    m.add_argument('pasta')
    m.add_argument('--aplicar', action='store_true')
    m.add_argument('--mostrar', action='store_true', help='imprime o JSON migrado inteiro')
    a = ap.parse_args()
    sys.exit({'novo': cmd_novo, 'validar': cmd_validar, 'etapa': cmd_etapa, 'migrar': cmd_migrar}[a.cmd](a) or 0)


if __name__ == '__main__':
    main()
