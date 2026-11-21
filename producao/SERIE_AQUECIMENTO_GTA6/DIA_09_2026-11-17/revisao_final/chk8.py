from PIL import Image
import glob,sys
fs=sorted(glob.glob(sys.argv[1]+'/revisao_final/frames_cartelas/rodape_*.jpg'))
ims=[Image.open(f) for f in fs]; h=sum(i.height for i in ims); pr=Image.new('RGB',(1920,h)); y=0
for i in ims: pr.paste(i,(0,y)); y+=i.height
pr.save(sys.argv[1]+'/revisao_final/prancha_rodapes.jpg'); print(fs)
