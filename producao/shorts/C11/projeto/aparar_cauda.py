import wave,shutil,json
from pathlib import Path
folder=Path('producao/shorts/C11');p=folder/'voz/narracao.wav';backup=folder/'historico/antes_revisao_20261031/narracao_revisada_antes_aparo.wav'
if not backup.exists():shutil.copy2(p,backup)
with wave.open(str(backup),'rb') as r:
 params=r.getparams();before=r.getnframes()/r.getframerate();samples=r.readframes(round(85.65*r.getframerate()))
with wave.open(str(folder/'voz/narracao_aparada.wav'),'wb') as w:
 w.setparams(params);w.writeframes(samples)
with wave.open(str(folder/'voz/narracao_aparada.wav'),'rb') as r:assert abs(r.getnframes()/r.getframerate()-85.65)<.0001
(folder/'voz/narracao_aparada.wav').replace(p)
(folder/'voz/APARO_SILENCIO.json').write_text(json.dumps(dict(before=before,after=85.65,method='PCM sample trim, no resynthesis or renormalization',authorization='Coordinator: independent review found 3.3s silent tail after Porque; preserve whole word and short breath',backup=str(backup)),ensure_ascii=False,indent=2),encoding='utf8')
