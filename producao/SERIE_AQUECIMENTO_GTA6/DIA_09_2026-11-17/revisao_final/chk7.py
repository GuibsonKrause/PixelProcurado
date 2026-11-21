import sys,re,difflib
sys.path.insert(0,'automacao')
from validar_revisao import ler_srt
ep=sys.argv[1]
srt=' '.join(t.replace('\n',' ') for _,_,t in ler_srt(ep+'/exportacoes/Pixel_Procurado_DIA09_Longo_V2.srt'))
nar=open(ep+'/01_NARRACAO.txt',encoding='utf-8').read()
n=lambda s: re.sub(r'\W+',' ',s.lower()).split()
a,b=n(nar),n(srt); print(len(a),len(b))
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if op!='equal': print(op,' '.join(a[i1:i2]),'->',' '.join(b[j1:j2]))
