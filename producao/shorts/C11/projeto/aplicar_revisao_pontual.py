import json
from pathlib import Path
root=Path('producao/shorts')
p=root/'C11/voz'
base=json.loads((p/'palavras_revisadas.json').read_text(encoding='utf8'))
part1=json.loads((p/'revisao_palavras_17.json').read_text(encoding='utf8'))
part2=json.loads((p/'revisao_palavras_16.json').read_text(encoding='utf8'))
part2[0].update(start=24.7,end=24.85)
part2[1].update(start=24.85)
last=json.loads((p/'revisao_palavras_83.json').read_text(encoding='utf8'))[-1:]
combined=[w for w in base if w['end']<=17 or w['start']>=31]+part1+part2+last
combined.sort(key=lambda w:w['start'])
(p/'palavras_asr.json').write_text(json.dumps(combined,ensure_ascii=False,indent=2),encoding='utf8')
(p/'DECISOES_REVISAO_PONTUAL.md').write_text('ASR beam1 perdeu uma frase em 20–24s. Janela 17–24s beam5 reconheceu a frase integral; janela 16–31s recuperou a relação seguinte com boa confiança após 25,4s. Primeiras duas marcações dessa segunda janela tinham alinhamento inválido (relação 17,04–25,4s), ajustadas para 24,70–25,40s, entre a frase anterior e fica 25,40s. Essa âncora merece escuta amostral. Porque recuperado na janela final. Voz não regenerada.',encoding='utf8')
p=root/'C12/voz'
base=json.loads((p/'palavras_revisadas.json').read_text(encoding='utf8'))
last=json.loads((p/'revisao_palavras_81.json').read_text(encoding='utf8'))[-1:]
assert last and 'final' in last[0]['word'].lower()
base+=last
(p/'palavras_asr.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf8')
