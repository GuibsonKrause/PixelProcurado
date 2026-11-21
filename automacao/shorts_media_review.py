"""Visual contact sheets of the exact source ranges used by the edits."""
from shorts_vertical import *
out=BASE/'_acervo/revisao_fontes';out.mkdir(exist_ok=True)
videos={};pictures={}
for rid in PLANS:
    data=json.loads((BASE/rid/'projeto/timeline.json').read_text(encoding='utf8'))
    for s in data['shots']:
        if not s['file']:continue
        if s['file'].endswith('.mp4'):
            length=min(s['frames']/FPS,s.get('motion',999))
            key=(s['file'],round(s['offset'],2),round(length,2))
            videos.setdefault(key,[]).append(rid)
        else:pictures.setdefault(s['file'],[]).append(rid)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for page in range(math.ceil(len(videos)/7)):
    sheet=Image.new('RGB',(960,7*220),'#151c28');draw=ImageDraw.Draw(sheet)
    for j,((file,offset,length),ids) in enumerate(list(videos.items())[page*7:page*7+7]):
        for k,t in enumerate([offset+.05,offset+length/2,offset+max(0,length-.1)]):
            dest=out/f'v{page}-{j}-{k}.jpg';run(['-ss',t,'-i',ROOT/file,'-frames:v',1,dest],out/'extract.log')
            im=Image.open(dest);im.thumbnail((320,180));sheet.paste(im,(k*320,j*220))
        draw.text((5,j*220+181),f'{",".join(sorted(set(ids)))} | {Path(file).stem[:30]} | {offset:.2f}–{offset+length:.2f}',font=font,fill='white')
    sheet.save(out/f'videos_{page:02}.jpg',quality=90)
for page in range(math.ceil(len(pictures)/12)):
    sheet=Image.new('RGB',(1200,4*255),'#151c28');draw=ImageDraw.Draw(sheet)
    for j,(file,ids) in enumerate(list(pictures.items())[page*12:page*12+12]):
        im=Image.open(ROOT/file);im.thumbnail((400,225));x=j%3*400;y=j//3*255;sheet.paste(im,(x,y));draw.text((x+5,y+228),Path(file).stem,font=font,fill='white')
    sheet.save(out/f'imagens_{page:02}.jpg',quality=90)
print(f'CONTACTS {len(videos)} video ranges, {len(pictures)} images',flush=True)
