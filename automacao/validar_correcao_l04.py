"""QA pontual da correção P03 de L04; não renderiza nem promove arquivos."""
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'automacao'))
import verificar_l04 as qa
qa.FINAL=qa.P/'exportacoes/Pixel_Procurado_L04_4K_revisao_P03.mp4'
qa.Q=qa.W/'qa_revisao_P03'
qa.Q.mkdir(parents=True,exist_ok=True)
before=qa.FINAL.stat()
sha=hashlib.sha256(qa.FINAL.read_bytes()).hexdigest()
print(json.dumps(dict(file=str(qa.FINAL),bytes=before.st_size,sha256=sha)),flush=True)
for t in [17.6,18.5,20,21,22,23,24.3]:
 qa.run(['-v','error','-ss',t,'-i',qa.FINAL,'-frames:v','1','-update','1','-vf','scale=1280:720',qa.Q/f'P03_{t:.1f}s.jpg'])
print('P03 real frames extracted',flush=True)
qa.validate()
after=qa.FINAL.stat()
assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns),'File changed during QA'
assert sha==hashlib.sha256(qa.FINAL.read_bytes()).hexdigest()
(qa.Q/'assinatura_candidato.json').write_text(json.dumps(dict(file=str(qa.FINAL),bytes=after.st_size,sha256=sha,stable_during_full_qa=True),indent=2),encoding='utf8')
print('QA completed on stable candidate',flush=True)
