"""Valida as quatro exportações finais e prepara evidência para revisão."""
import json
import subprocess
import sys
from pathlib import Path

from dia01_validar import BASE, FF
from PIL import Image, ImageDraw, ImageFont

def main():
    exports=BASE/'exportacoes'
    qa=BASE/'qa'
    checker=Path(__file__).with_name('dia01_validar.py')
    vertical=['--width','1080','--height','1920']
    jobs=[('DIA01_Master_4K',[]),('DIA01_Instagram_Integral',vertical),
          ('DIA01_Reel_HUD',vertical+['--reference',str(qa/'audio/referencia_reel_concatenada.wav')]),
          ('DIA01_Story_HUD',vertical+['--reference',str(qa/'audio/referencia_story_concatenada.wav')])]
    for name,args in jobs:
        log=BASE/f'EXEC_QA_FINAL_{name}.log'
        print(f'QA START {name}',flush=True)
        with log.open('w',encoding='utf-8') as out:
            p=subprocess.run([sys.executable,str(checker),str(exports/f'{name}.mp4'),*args],stdout=out,stderr=subprocess.STDOUT)
        if p.returncode:
            print(log.read_text(encoding='utf-8',errors='replace')[-4000:],flush=True)
            raise SystemExit(p.returncode)
        print(f'QA DONE {name}: {log}',flush=True)
    master=exports/'DIA01_Master_4K.mp4'
    q=qa/'DIA01_Master_4K'
    frame_dir=q/'quadros_representativos'
    frame_dir.mkdir(exist_ok=True)
    points=[(.6,'Entrada'),(5,'Leitura'),(10,'Saida'),(15,'Pre-load'),(27,'HUD'),(65,'Predio'),(125,'Laboratorio'),(151,'Inventario'),(190,'Combate'),(220,'Cena escura'),(250,'Escritorio'),(265,'Luta'),(300,'HUD'),(339,'Regra'),(360,'CTA'),(371,'Fim')]
    sheet=Image.new('RGB',(1920,1200),(10,12,18))
    draw=ImageDraw.Draw(sheet)
    font_path=Path('C:/Windows/Fonts/arial.ttf')
    font=ImageFont.truetype(str(font_path),20) if font_path.is_file() else ImageFont.load_default()
    rows=[]
    for i,(t,label) in enumerate(points):
        dst=frame_dir/f'{i+1:02}_{t:07.3f}_{label.replace(" ","_")}.jpg'
        p=subprocess.run([FF,'-v','error','-nostdin','-y','-ss',str(t),'-i',str(master),'-frames:v','1','-q:v','2','-update','1',str(dst)],capture_output=True)
        assert p.returncode==0 and dst.stat().st_size>1000,p.stderr.decode('utf-8',errors='replace')
        x=(i%4)*480;y=(i//4)*300
        with Image.open(dst) as im:
            assert im.size==(3840,2160)
            sheet.paste(im.resize((480,270),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+9,y+273),f'{t:07.3f} s | {label}',font=font,fill='white')
        rows.append({'time':t,'label':label,'file':str(dst.resolve())})
    contact=q/'contato_representativo.jpg'
    sheet.save(contact,quality=93)
    report=json.loads((q/'RELATORIO_QA.json').read_text(encoding='utf-8'))
    (q/'QUADROS_REPRESENTATIVOS.json').write_text(json.dumps({'master':str(master.resolve()),'sha256':report['sha256'],'contact':str(contact.resolve()),'frames':rows},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'QUADROS DONE {contact}',flush=True)

if __name__=='__main__':
    main()
