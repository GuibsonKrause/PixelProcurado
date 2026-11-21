import subprocess,sys,numpy as np
ep=sys.argv[1]
def dec(v,i,t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(i),'-t',str(t),'-i',v,'-vn','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
L=ep+'/exportacoes/Pixel_Procurado_DIA09_Longo_V2.mp4'; V=ep+'/_vertical/exportacoes/Pixel_Procurado_DIA09_Vertical_V2.mp4'; S=ep+'/_story/exportacoes/Pixel_Procurado_DIA09_Story_V2.mp4'
a,b=dec(L,0,6),dec(V,0,6)
best=max(range(-1600,1601,4),key=lambda k: float(np.dot(a[1600:80000],b[1600+k:80000+k])))
x=a[1600:80000]; y=b[1600+best:80000+best]; print('lag amostras',best,'corr',np.corrcoef(x,y)[0,1])
l=dec(L,404.6,1.2); print('longo 404.6+ rms 50ms', [round(float(np.sqrt(np.mean(l[i:i+800]**2))),3) for i in range(0,len(l),800)])
s=dec(S,0,0.4); print('story 0+ rms 25ms', [round(float(np.sqrt(np.mean(s[i:i+400]**2))),3) for i in range(0,len(s),400)])
