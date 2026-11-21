import json,subprocess,sys,numpy as np
ep=sys.argv[1]
r=json.load(open(ep+'/revisao_final/asr_trechos.json',encoding='utf-8'))
for x in r:
    if 'Reel' in x['video'] or 'Story' in x['video'] or 'Vertical' in x['video'] or x['inicio']==0:
        print(x['video'][-28:], x['inicio'], x['palavras'][:3], x['palavras'][-2:])
def dec(v,i,t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(i),'-t',str(t),'-i',v,'-vn','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
L=ep+'/exportacoes/Pixel_Procurado_DIA09_Longo_V2.mp4'; V=ep+'/_vertical/exportacoes/Pixel_Procurado_DIA09_Vertical_V2.mp4'
R=ep+'/_reel/exportacoes/Pixel_Procurado_DIA09_Reel_V2.mp4'; S=ep+'/_story/exportacoes/Pixel_Procurado_DIA09_Story_V2.mp4'
a,b=dec(L,0,4),dec(V,0,4); n=min(len(a),len(b)); print('corr longo x vertical 0-4s', np.corrcoef(a[:n],b[:n])[0,1])
for nome,v,d in (('reel',R,64.3),('story',S,15.12)):
    x=dec(v,0,d)
    for k in (0,0.1,0.2,0.3):
        s=x[int(k*16000):int((k+0.1)*16000)]; print(nome,'ini',k,round(float(np.sqrt(np.mean(s**2))),4))
    for k in (1.2,0.8,0.5,0.3,0.15):
        s=x[-int(k*16000):]; print(nome,'ultimos',k,'s rms',round(float(np.sqrt(np.mean(s[:1600]**2))),4))
