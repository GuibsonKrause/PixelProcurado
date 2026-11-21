import sys
from pathlib import Path
from PIL import Image
ep=Path(sys.argv[1]); out=ep/'revisao_final'/'capas'; out.mkdir(parents=True,exist_ok=True)
fs=[ep/'publicacao/capas'/f for f in ('capa_longo_A.jpg','capa_longo_B.jpg','capa_vertical_A.jpg','capa_vertical_B.jpg')]+[ep/'publicacao/carrossel'/f'0{i}.jpg' for i in range(1,5)]
ims=[]
for f in fs:
    im=Image.open(f).convert('RGB'); print(f.name, im.size)
    w=640 if im.width>im.height else 320
    p=im.resize((w, round(im.height*w/im.width)), Image.LANCZOS); p.save(out/f'preview_{f.parent.name}_{f.stem}.jpg', quality=88); ims.append(p)
# prancha horizontal (2 longos) e vertical (2 verticais + 4 carrossel)
pr=Image.new('RGB',(1280,ims[0].height),'black'); pr.paste(ims[0],(0,0)); pr.paste(ims[1],(640,0)); pr.save(ep/'revisao_final'/'prancha_capas_longo.jpg')
vs=ims[2:]; H=max(i.height for i in vs); pr=Image.new('RGB',(sum(i.width for i in vs),H),'black'); x=0
for i in vs: pr.paste(i,(x,0)); x+=i.width
pr.save(ep/'revisao_final'/'prancha_capas_vert_carrossel.jpg')
