import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import data from './edicao.json';

const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const gold='#ffd33d';
type Shot=typeof data.shots[number];
const Scene:React.FC<{shot:Shot}>=({shot})=>{
  const f=useCurrentFrame();
  const p=f/Math.max(1,shot.frames-1);
  const enter=interpolate(f,[0,16],[0,1],clamp);
  const titleOn=!!shot.title;
  const scale=shot.motion%2===0?1.035+p*.035:1.075-p*.035;
  const x=(p-.5)*(shot.motion===2?32:shot.motion===3?-32:12);
  const style:React.CSSProperties={width:'100%',height:'100%',objectFit:'cover'};
  return <AbsoluteFill style={{background:'#10121b',overflow:'hidden'}}>
    <AbsoluteFill style={{transform:shot.kind==='image'?`translateX(${x}px) scale(${scale})`:undefined}}>
      {shot.kind==='video'?<OffthreadVideo src={staticFile(shot.src)} startFrom={Math.round(shot.offset*30)} muted style={style}/>:<Img src={staticFile(shot.src)} style={style}/>}
    </AbsoluteFill>
    <AbsoluteFill style={{background:'linear-gradient(0deg,rgba(5,8,15,.68) 0%,transparent 35%,transparent 76%,rgba(5,8,15,.55) 100%)'}}/>
    {titleOn&&<AbsoluteFill style={{background:'linear-gradient(90deg,rgba(6,10,18,.84),rgba(6,10,18,.40) 57%,transparent)',opacity:enter}}/>}
    <div style={{position:'absolute',left:96,top:88,display:'flex',alignItems:'center',gap:14,transform:`translateY(${(1-enter)*12}px)`,opacity:enter}}>
      <div style={{width:7,height:25,background:gold}}/><span style={{fontSize:23,fontWeight:700,letterSpacing:3,color:'white',textShadow:'0 2px 8px #000'}}>{shot.label||'GTA VI / IMAGENS DE APOIO'}</span>
    </div>
    {titleOn&&<div style={{position:'absolute',left:96,top:295,maxWidth:1550,transform:`translateY(${(1-enter)*24}px)`,opacity:enter}}>
      <div style={{height:4,width:interpolate(f,[0,24],[0,90],clamp),background:gold,marginBottom:30}}/>
      <div style={{fontSize:shot.title.length>32?67:88,fontWeight:800,lineHeight:1.08,letterSpacing:-2,color:'#fff',whiteSpace:'pre-line',textShadow:'0 4px 30px #0008'}}>{shot.title}</div>
      {shot.sub&&<div style={{fontSize:29,color:'#e0e3ec',marginTop:32,lineHeight:1.4,maxWidth:1300}}>{shot.sub}</div>}
    </div>}
    {/* Only stills dissolve in; action footage keeps clean, rhythmic cuts. */}
    {shot.kind==='image'&&f<6&&<AbsoluteFill style={{background:'#10121b',opacity:interpolate(f,[0,6],[.22,0],clamp)}}/>}
  </AbsoluteFill>;
};

export const Edicao:React.FC=()=>{
 const frame=useCurrentFrame(),t=frame/30;
 const caption=data.captions.find(c=>t>=c.start&&t<c.end);
 const fade=interpolate(frame,[0,10,data.frames-12,data.frames-1],[0,1,1,0],clamp);
 const key=/^(Rockstar|Jason|Lucia|Leonida|fonte[.,]?|confirmado[.,]?|hipótese[.,]?|evidência[.,]?|PC[.,]?|confiança[.,]?)$/i;
 return <AbsoluteFill style={{background:'#080a10',fontFamily:'Arial, sans-serif'}}>
  <Audio src={staticFile('l01/narracao.wav')}/>
  <div style={{position:'absolute',width:1920,height:1080,transform:'scale(2)',transformOrigin:'top left',opacity:fade}}>
   {data.shots.map(s=><Sequence key={s.from} from={s.from} durationInFrames={s.frames}><Scene shot={s}/></Sequence>)}
   <div style={{position:'absolute',right:82,top:85,color:'#fff',fontSize:17,letterSpacing:2,fontWeight:700,textAlign:'right',opacity:.8}}>PIXEL<span style={{color:gold}}> / </span>PROCURADO</div>
   {caption&&<div style={{position:'absolute',bottom:91,left:220,right:220,display:'flex',justifyContent:'center',opacity:interpolate(t-caption.start,[0,.08],[0,1],clamp),transform:`translateY(${interpolate(t-caption.start,[0,.12],[5,0],clamp)}px)`}}>
    <div style={{background:'rgba(6,9,15,.88)',borderRadius:12,padding:'17px 28px',color:'#fff',fontSize:43,fontWeight:700,lineHeight:1.22,textAlign:'center',maxWidth:1420,boxShadow:'0 4px 20px #0004'}}>
      {caption.words.map((w,i)=><React.Fragment key={i}><span style={{color:key.test(w.word)&&t>=w.start?gold:'#fff'}}>{w.word}</span>{i<caption.words.length-1?' ':''}</React.Fragment>)}
    </div>
   </div>}
   <div style={{position:'absolute',bottom:0,left:0,height:4,width:`${frame/data.frames*100}%`,background:gold,opacity:.65}}/>
  </div>
 </AbsoluteFill>;
};
