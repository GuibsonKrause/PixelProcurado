"""Validador minimo de JSON Schema (sem dependencias). Suporta o subconjunto usado em automacao/schemas/."""
import re

_TIPOS = {'object': dict, 'array': list, 'string': str, 'boolean': bool, 'null': type(None)}


def _tipo_ok(v, t):
    if t == 'integer':
        return isinstance(v, int) and not isinstance(v, bool)
    if t == 'number':
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    return isinstance(v, _TIPOS[t])


def validar(dado, schema, raiz=None, caminho='$'):
    """Retorna lista de erros (strings). Vazia = valido."""
    raiz = raiz or schema
    if '$ref' in schema:
        alvo = raiz
        for p in schema['$ref'].lstrip('#/').split('/'):
            alvo = alvo[p]
        return validar(dado, alvo, raiz, caminho)
    if 'oneOf' in schema or 'anyOf' in schema:
        alts = schema.get('oneOf') or schema.get('anyOf')
        if not any(not validar(dado, s, raiz, caminho) for s in alts):
            return [f'{caminho}: nao corresponde a nenhuma alternativa permitida']
    erros = []
    t = schema.get('type')
    if t:
        tipos = t if isinstance(t, list) else [t]
        if not any(_tipo_ok(dado, x) for x in tipos):
            return [f'{caminho}: esperado {"/".join(tipos)}, recebido {type(dado).__name__}']
    if 'enum' in schema and dado not in schema['enum']:
        erros.append(f'{caminho}: valor {dado!r} fora de {schema["enum"]}')
    if 'const' in schema and dado != schema['const']:
        erros.append(f'{caminho}: deve ser {schema["const"]!r}')
    if isinstance(dado, str):
        if 'pattern' in schema and not re.search(schema['pattern'], dado):
            erros.append(f'{caminho}: {dado!r} nao casa com {schema["pattern"]}')
        if len(dado) < schema.get('minLength', 0):
            erros.append(f'{caminho}: texto vazio ou curto demais')
    if isinstance(dado, (int, float)) and not isinstance(dado, bool) and 'minimum' in schema and dado < schema['minimum']:
        erros.append(f'{caminho}: {dado} < minimo {schema["minimum"]}')
    if isinstance(dado, dict):
        for k in schema.get('required', []):
            if k not in dado:
                erros.append(f'{caminho}: campo obrigatorio ausente: {k}')
        props = schema.get('properties', {})
        for k, v in dado.items():
            if k in props:
                erros += validar(v, props[k], raiz, f'{caminho}.{k}')
            elif isinstance(schema.get('additionalProperties'), dict):
                erros += validar(v, schema['additionalProperties'], raiz, f'{caminho}.{k}')
            elif schema.get('additionalProperties') is False:
                erros.append(f'{caminho}: campo nao permitido: {k}')
    if isinstance(dado, list):
        if len(dado) < schema.get('minItems', 0):
            erros.append(f'{caminho}: minimo de {schema["minItems"]} itens (tem {len(dado)})')
        if 'items' in schema:
            for i, v in enumerate(dado):
                erros += validar(v, schema['items'], raiz, f'{caminho}[{i}]')
    return erros
