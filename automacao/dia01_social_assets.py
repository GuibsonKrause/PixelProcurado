"""Peças estáticas de apoio: evidência real do HUD, sem inventar captura."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.course-tools'),str(ROOT/'.production-tools/python')]
from PIL import Image, ImageDraw, ImageFont, ImageOps

P=ROOT/'producao/SERIE_AQUECIMENTO_GTA6/DIA_01_2026-11-09'
OUT=P/'social'
YELLOW='#FFD33D'
WHITE='#F8FAFC'

def font(n,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('impact.ttf' if bold else 'arial.ttf'),n)

def main():
    OUT.mkdir(exist_ok=True)
    hud=Image.open(P/'evidencia_hud_botoes.png').convert('RGB')
    frame=Image.open(P/'referencia_seek_pyav370.png').convert('RGB')
    texts=[('ANTES DE FUGIR','LEIA O HUD',['Duas opções aparecem na porta do carro.','O detalhe está nas imagens oficiais.']),
      ('CÍRCULO','SMASH WINDOW',['A opção mostrada é quebrar a janela.','Observe o símbolo real do comando.']),
      ('TRIÂNGULO','SLIM JIM',['A ferramenta aparece como outra opção.','A comparação parte desse HUD.']),
      ('O QUE É FATO?','O QUE É ANÁLISE?',['Fato: o HUD apresenta as duas opções.','As consequências discutidas no vídeo','são interpretação editorial das imagens.'])]
    paths=[]
    for i,(a,b,lines) in enumerate(texts,1):
        canvas=Image.new('RGB',(1080,1350),'#080A10'); draw=ImageDraw.Draw(canvas)
        draw.text((65,55),'PIXEL / PROCURADO',font=font(30),fill=WHITE)
        draw.text((65,130),a,font=font(70,True),fill=WHITE)
        draw.text((65,220),b,font=font(70,True),fill=YELLOW)
        scene=ImageOps.fit(frame,(950,430),method=Image.Resampling.LANCZOS)
        canvas.paste(scene,(65,340))
        crop=ImageOps.contain(hud,(950,410),method=Image.Resampling.LANCZOS)
        canvas.paste(crop,((1080-crop.width)//2,790))
        for j,line in enumerate(lines):draw.text((65,1190+j*39),line,font=font(28),fill=WHITE)
        draw.text((65,1310),'Rockstar Games · GTA VI · análise do gameplay',font=font(19),fill='#ADB3BE')
        path=OUT/f'carrossel_{i:02}.jpg';canvas.save(path,quality=95,optimize=True);paths.append(str(path))
    thumb=Image.new('RGB',(1080,1920),'#080A10');draw=ImageDraw.Draw(thumb)
    draw.text((70,100),'PIXEL / PROCURADO',font=font(40),fill=WHITE)
    draw.text((70,230),'QUAL',font=font(155,True),fill=WHITE)
    draw.text((70,410),'BOTÃO?',font=font(155,True),fill=YELLOW)
    thumb.paste(ImageOps.fit(frame,(1080,608)),(0,720))
    thumb.paste(ImageOps.contain(hud,(980,430)),(50,1370))
    draw.text((70,1825),'ANÁLISE DO GAMEPLAY OFICIAL',font=font(30),fill=WHITE)
    thumb.save(OUT/'capa_vertical_hud.png')
    for path in paths:
        with Image.open(path) as im:assert im.size==(1080,1350)
    (OUT/'PECAS_ESTATICAS.json').write_text(json.dumps({'status':'preparadas_aguardando_QA','carrossel':paths,'capa_vertical':str(OUT/'capa_vertical_hud.png'),'fonte_frame_segundos':364.9,'captura_autentica':True,'envio_confirmado':False},ensure_ascii=False,indent=2),encoding='utf8')
    print('Criados4slides1080x1350 e capa vertical1080x1920 com HUD autêntico.')

if __name__=='__main__':main()
