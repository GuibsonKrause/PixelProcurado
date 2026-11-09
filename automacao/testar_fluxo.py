"""Smoke test com sinais e arte próprios; não gera episódio publicável."""
import json
from pathlib import Path
import time
import producao as p

out=p.ROOT/'producao/L01/testes'/time.strftime('%Y%m%d-%H%M%S')
out.mkdir(parents=True)
raw=out/'sinal.wav'
p.run(['-f','lavfi','-i','sine=frequency=440:duration=3','-c:a','pcm_s16le',raw])
voice=out/'normalizado.wav'
p.normalize(raw,voice)
image=p.ROOT/'producao/L01/arte/cartela_confirmado.png'
manifest=out/'montagem.json'
manifest.write_text(json.dumps({'voice':str(voice),'clips':[{'file':str(image),'kind':'image','duration':3,
    'source':'Cartela tipográfica original criada no projeto','use_reviewed':True}]}),encoding='utf-8')
horizontal=out/'teste_horizontal.mp4'
p.assemble(manifest,horizontal)
vertical=out/'teste_vertical.mp4'
p.clip(horizontal,vertical,0,2,True)
assert abs(p.probe(horizontal)['duration']-3)<0.15
assert abs(p.probe(vertical)['duration']-2)<0.15
try: p.clip(horizontal,out/'invalido.mp4',0,8,True)
except ValueError: pass
else: raise AssertionError('Deveria rejeitar intervalo inválido')
try: p.output(horizontal)
except ValueError: pass
else: raise AssertionError('Deveria rejeitar sobrescrita')
data=json.loads(manifest.read_text())
data['clips'][0]['use_reviewed']=False
manifest.write_text(json.dumps(data),encoding='utf-8')
try: p.assemble(manifest,out/'sem_revisao.mp4')
except ValueError: pass
else: raise AssertionError('Deveria rejeitar mídia sem revisão')
data['clips'][0]['use_reviewed']=True
data['clips'][0]['duration']=1
manifest.write_text(json.dumps(data),encoding='utf-8')
try: p.assemble(manifest,out/'duracao_errada.mp4')
except ValueError: pass
else: raise AssertionError('Deveria rejeitar divergência de duração')
(out/'resultado.json').write_text(json.dumps({'status':'pass','tests':[
    'normalizacao duas passagens','montagem voz+imagem','vertical preserva quadro',
    'duracoes verificadas','intervalo invalido rejeitado','overwrite rejeitado',
    'midia sem revisao rejeitada','cobertura incorreta da voz rejeitada'],
    'horizontal':p.probe(horizontal),'vertical':p.probe(vertical)},indent=2),encoding='utf-8')
print(out)
