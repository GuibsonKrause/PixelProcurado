import React from 'react';
import {AbsoluteFill,Composition,registerRoot,getInputProps} from 'remotion';
import data from './edicao.json';
const Overlay:React.FC=()=>{
 const {index}=getInputProps() as {index:number};const s=data.shots[index];
 return <AbsoluteFill style={{fontFamily:'Arial, sans-serif',color:'white'}}>
  <div style={{position:'absolute',width:1920,height:1080,transform:'scale(2)',transformOrigin:'top left'}}>
   <AbsoluteFill style={{background:'linear-gradient(0deg,rgba(5,8,15,.5),transparent 28%,transparent 80%,rgba(5,8,15,.5))'}}/>
   {s.title&&<AbsoluteFill style={{background:'linear-gradient(90deg,rgba(6,10,18,.80),rgba(6,10,18,.3) 60%,transparent)'}}/>}
   <div style={{position:'absolute',left:96,top:88,display:'flex',alignItems:'center',gap:14}}><div style={{width:7,height:25,background:'#ffd33d'}}/><span style={{fontSize:23,fontWeight:700,letterSpacing:3,textShadow:'0 2px 8px #000'}}>{s.label||'GTA VI / IMAGENS DE APOIO'}</span></div>
   <div style={{position:'absolute',right:82,top:85,fontSize:17,letterSpacing:2,fontWeight:700,opacity:.8}}>PIXEL<span style={{color:'#ffd33d'}}> / </span>PROCURADO</div>
   {s.title&&<div style={{position:'absolute',left:96,top:295,maxWidth:1550}}>
    <div style={{height:4,width:90,background:'#ffd33d',marginBottom:30}}/>
    <div style={{fontSize:s.title.length>32?67:88,fontWeight:800,lineHeight:1.08,letterSpacing:-2,whiteSpace:'pre-line',textShadow:'0 4px 30px #0008'}}>{s.title}</div>
    {s.sub&&<div style={{fontSize:29,color:'#e0e3ec',marginTop:32,lineHeight:1.4,maxWidth:1300}}>{s.sub}</div>}
   </div>}
  </div>
 </AbsoluteFill>;
};
registerRoot(()=> <Composition id="Overlay" component={Overlay} durationInFrames={30} fps={30} width={3840} height={2160}/>);
