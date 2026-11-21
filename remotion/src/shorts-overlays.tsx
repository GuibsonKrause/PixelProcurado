import React from 'react';
import {AbsoluteFill, Composition, interpolate, registerRoot, useCurrentFrame} from 'remotion';
const gold='#FFD33D';
const Overlay:React.FC<{shot:any}>=({shot:s})=>{
 const f=useCurrentFrame();
 const ease=(delay=0)=>{const t=interpolate(f-delay,[0,17],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return 1-Math.pow(1-t,3)};
 const p=s.hook?.85+.15*ease():ease();
 const graphic=s.mode==='graphic';
 const titleSize=s.title.length>43?65:s.title.length>29?76:88;
 const ring=s.ring;
 return <AbsoluteFill style={{color:'#f8fafc',fontFamily:'Arial, sans-serif'}}>
  {s.mode==='portrait'&&<AbsoluteFill style={{background:'linear-gradient(180deg,rgba(5,9,16,.92) 0%,rgba(5,9,16,.75) 26%,transparent 47%,transparent 61%,rgba(5,9,16,.82) 78%,#090e17 100%)'}}/>}
  {graphic&&<AbsoluteFill style={{background:'radial-gradient(ellipse at 5% 35%,#253443 0%,#121c2b 42%,#090e17 78%)'}}/>}
  <div style={{position:'absolute',left:64,top:94,fontSize:23,fontWeight:700,letterSpacing:3}}>PIXEL <span style={{color:gold}}>/</span> PROCURADO</div>
  <div style={{position:'absolute',left:64,top:200,width:870,fontSize:25,color:gold,fontWeight:700,letterSpacing:1.6,lineHeight:1.35}}>{s.label}</div>
  <div style={{position:'absolute',left:64,top:280,width:870,opacity:p,transform:`translateY(${(1-p)*24}px)`}}>
   <div style={{height:6,width:110+80*ease(),background:gold,marginBottom:25}}/>
   <div style={{fontSize:titleSize,fontWeight:900,lineHeight:1.04,letterSpacing:-2.4,whiteSpace:'pre-line',textShadow:'0 3px 16px #090e17'}}>{s.title}</div>
  </div>
  {graphic&&<div style={{position:'absolute',left:68,top:650,width:866}}>
   {(s.items||[]).map((text:string,i:number)=>{const q=ease(i*8);return <div key={i} style={{position:'relative',marginBottom:22,padding:'34px 32px',borderLeft:`6px solid ${gold}`,background:'#ffffff0c',borderRadius:4,opacity:q,transform:`translateX(${(1-q)*45}px)`}}><div style={{fontSize:22,color:gold,letterSpacing:3,marginBottom:12}}>0{i+1}</div><div style={{fontSize:text.length>27?42:51,lineHeight:1.14,fontWeight:700}}>{text}</div></div>})}
  </div>}
  {s.radio&&<div style={{position:'absolute',top:1200,left:90,display:'flex',alignItems:'center',height:80,gap:13}}>{Array.from({length:31},(_,i)=><div key={i} style={{width:12,height:12+55*Math.abs(Math.sin(i*.7+Math.min(f,35)*.12)),background:i%3===0?gold:'#728394',borderRadius:3}}/>)}</div>}
  {ring&&<svg width={1080} height={1920} style={{position:'absolute'}}><rect x={54+ring[0]*972} y={651.625+ring[1]*546.75} width={ring[2]*972} height={ring[3]*546.75} rx={9} fill="none" stroke={gold} strokeWidth={5} pathLength={1} strokeDasharray={1} strokeDashoffset={1-ease()}/></svg>}
  {!graphic&&s.mode==='panel'&&<><div style={{position:'absolute',left:54,top:560,width:972,height:730,border:'1px solid #ffffff18'}}/><div style={{position:'absolute',left:64,top:1313,fontSize:21,color:'#a4b1c1'}}>ROCKSTAR GAMES <span style={{color:gold}}> / </span> {s.file?.includes('Artwork')?'ARTE OFICIAL':s.file?.endsWith('.mp4')?'TRECHO DO ACERVO':'IMAGEM DO ACERVO'}</div></>}
  <div style={{position:'absolute',left:64,top:1710,fontSize:20,color:'#8998aa',letterSpacing:1.5}}>DETALHES. HISTÓRIAS. EVIDÊNCIAS.</div>
 </AbsoluteFill>;
};
const Root:React.FC=()=> <Composition id="ShortsOverlay" component={Overlay} width={1080} height={1920} fps={30} durationInFrames={300} defaultProps={{shot:{title:'',label:'',mode:'panel'}}}/>;
registerRoot(Root);
