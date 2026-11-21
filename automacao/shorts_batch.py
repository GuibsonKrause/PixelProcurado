"""Resumable sequential render; every final is validated before advancing."""
import subprocess,sys,json
from shorts_vertical import ROOT,BASE,PLANS,render,qa,write_json
for rid in sys.argv[1:] or PLANS:
    subprocess.run([r'C:\Program Files\nodejs\node.exe','render-shorts-overlays.mjs',rid],cwd=ROOT/'remotion',check=True)
    render(rid)
    qa(rid)
    print('VALIDATED '+rid,flush=True)
