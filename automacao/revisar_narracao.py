"""Correções locais de pronúncia do L01, preservando a primeira geração."""
import sys, os, json, wave
from pathlib import Path
import narrar_voicestudio as n
import producao
sys.path[:0]=[str(n.ROOT/'.production-tools/python'),str(n.ROOT/'.course-tools')]
from supertonic import TTS
folder=n.OUT/'revisao'
folder.mkdir(exist_ok=True)
model=Path(os.environ['LOCALAPPDATA'])/'OmniVoice/hf_cache/models--Supertone--supertonic-3/snapshots/724fb5abbf5502583fb520898d45929e62f02c0b'
n.SDK=TTS(model_dir=model,auto_download=False,intra_op_num_threads=4,inter_op_num_threads=1)
source=n.ROOT/'producao/L01/01_NARRACAO.txt'
paras=[x.strip() for x in source.read_text(encoding='utf-8').split('\n\n') if x.strip()]
changes={11:paras[10].replace('Port Gellhorn','Port Guél-hórn').replace('Grassrivers','Gráss Rívers'),
         14:paras[13].replace('An Extended Look','Um Olhar Estendido, em tradução livre')}
for idx,text in changes.items():
    n.generate(text,'M5',folder/f'{idx:02}.wav',1.0)
    out=folder/f'{idx:02}.srt'
    if not out.exists(): producao.transcribe(folder/f'{idx:02}.wav',out,'base')
    print(out.read_text(encoding='utf-8'),flush=True)
(folder/'adaptacoes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
