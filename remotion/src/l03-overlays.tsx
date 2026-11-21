import React from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';

const gold='#ffd33d';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
export const L03Overlay:React.FC<{shot:any}>=({shot:s})=>{
 const frame=useCurrentFrame();
 const reveal=(cue=0)=>{if(cue<0)return 1;const p=interpolate(frame-cue,[0,19],[0,1],clamp);return 1-Math.pow(1-p,3)};
 const p=s.animate?reveal():1;
 const full=s.presentation==='graphic', classic=s.presentation==='classic-card';
 const side=s.layout?.side||s.panelSide||'left';
 const width=s.layout?.width||760, x=side==='right'?1920-100-width:96;
 const rows=(left:number,top:number,rowWidth:number,size=54)=>(s.items||[]).slice(0,s.stage??s.items?.length).map((text:string,i:number)=>{
  const q=reveal(s.cues?.[i]??0);
  return <div key={i} style={{position:'absolute',left,top:top+i*124,width:rowWidth,display:'flex',gap:22,alignItems:'baseline',opacity:q,transform:`translateX(${(1-q)*26}px)`}}><span style={{color:gold,fontSize:23,fontWeight:800}}>0{i+1}</span><span style={{fontSize:size,fontWeight:700,letterSpacing:-1,lineHeight:1.16}}>{text}</span></div>;
 });
 return <AbsoluteFill style={{color:'#fff',fontFamily:'Arial, sans-serif'}}>
  <div style={{width:1920,height:1080,position:'absolute',transform:'scale(2)',transformOrigin:'top left'}}>
   {full&&<AbsoluteFill style={{background:'radial-gradient(ellipse at 25% 25%,#253441 0%,#101824 52%,#080d15 100%)'}}/>}
   {!full&&!classic&&<AbsoluteFill style={{background:'linear-gradient(0deg,rgba(5,8,15,.55),transparent 26%,transparent 75%,rgba(5,8,15,.52))'}}/>}
   {full&&<svg width="1920" height="1080" style={{position:'absolute',opacity:.055}}>{Array.from({length:17},(_,i)=><line key={i} x1={i*120} y1="0" x2={i*120} y2="1080" stroke="white"/>)}</svg>}
   <div style={{position:'absolute',left:96,top:77,display:'flex',gap:16,alignItems:'center',textShadow:'0 2px 12px #000'}}><span style={{background:gold,width:6,height:26}}/><span style={{fontSize:22,fontWeight:700,letterSpacing:2}}>{s.label}</span></div>
   <div style={{position:'absolute',right:84,top:80,fontSize:17,fontWeight:700,letterSpacing:2,textShadow:'0 2px 12px #000'}}>PIXEL <span style={{color:gold}}>/</span> PROCURADO</div>
   {s.graphic==='headline'&&<div style={{position:'absolute',left:x,top:s.layout?.top||280,width,opacity:p,transform:`translateY(${(1-p)*26}px)`}}><div style={{height:5,width:100,background:gold,marginBottom:30}}/><div style={{fontSize:classic?60:72,fontWeight:800,letterSpacing:-2,lineHeight:1.1,whiteSpace:'pre-line'}}>{s.title}</div>{s.sub&&<div style={{fontSize:27,lineHeight:1.4,color:'#cbd4df',marginTop:28}}>{s.sub}</div>}</div>}
   {s.graphic==='list'&&<><div style={{position:'absolute',left:150,top:220,fontSize:70,fontWeight:800,letterSpacing:-2}}>{s.title}</div>{rows(160,390,1590,54)}</>}
   {s.graphic==='dates'&&(s.items||[]).slice(0,s.stage||0).map((text:string,i:number)=>{const q=reveal(s.cues?.[i]??0);const [name,year]=text.split('\n');return <div key={i} style={{position:'absolute',left:160+i*820,top:340,width:740,height:360,boxSizing:'border-box',border:'2px solid #ffd33d',borderRadius:22,padding:48,background:'#ffd33d09',opacity:q,transform:`translateY(${(1-q)*30}px)`}}><div style={{fontSize:28,color:gold,fontWeight:700,letterSpacing:4}}>{name}</div><div style={{fontSize:142,fontWeight:800,letterSpacing:-6,marginTop:22}}>{year}</div></div>})}
   {s.graphic==='radio'&&<>
    <div style={{position:'absolute',left:150,top:205,fontSize:67,fontWeight:800,letterSpacing:-2}}>{s.title}</div>
    <div style={{position:'absolute',left:154,top:292,fontSize:27,color:'#cbd4df'}}>{s.sub}</div>
    <svg width="880" height="440" viewBox="0 0 880 440" style={{position:'absolute',left:150,top:380}}><rect x="10" y="20" width="840" height="370" rx="34" fill="#182332" stroke="#697583" strokeWidth="3"/><rect x="50" y="65" width="410" height="240" rx="16" fill="#090f17"/>{Array.from({length:11},(_,i)=><line key={i} x1="75" y1={85+i*19} x2="435" y2={85+i*19} stroke="#445263" strokeWidth="5"/>)}<rect x="500" y="65" width="300" height="92" rx="8" fill="#ffd33d13" stroke={gold}/><text x="525" y="122" fontSize="30" fill={gold} fontFamily="Arial" fontWeight="bold">RÁDIO / 1986</text><circle cx="570" cy="240" r="44" fill="#0a111b" stroke="#8793a2" strokeWidth="4"/><circle cx="735" cy="240" r="44" fill="#0a111b" stroke="#8793a2" strokeWidth="4"/><line x1="570" y1="240" x2="585" y2="210" stroke={gold} strokeWidth="5"/><line x1="735" y1="240" x2="720" y2="210" stroke={gold} strokeWidth="5"/><text x="515" y="345" fontSize="20" fill="#9ba9ba" fontFamily="Arial">GRÁFICO EDITORIAL</text></svg>
    {rows(1110,395,660,54)}
   </>}
   {s.graphic==='focus'&&<svg width="1920" height="1080" style={{position:'absolute',filter:'drop-shadow(0 2px 5px #000b)'}}>{(s.focusRects||[]).map((r:any)=>{const q=reveal(r.cue||0);return <g key={r.id} opacity={q}><rect x={r.x} y={r.y} width={r.width} height={r.height} rx="14" fill="none" stroke={gold} strokeWidth="4" pathLength="1" strokeDasharray="1" strokeDashoffset={1-q}/>{r.label&&<g><rect x={Math.max(12,r.x)} y={Math.max(118,r.y-45)} width={Math.min(480,r.label.length*14+32)} height="36" rx="5" fill="#080d15e8"/><text x={Math.max(12,r.x)+16} y={Math.max(118,r.y-45)+26} fontSize="22" fontWeight="bold" fill={gold}>{r.label}</text></g>}</g>})}</svg>}
   <div style={{position:'absolute',left:96,bottom:37,fontSize:16,letterSpacing:.3,color:'#d6dce5',textShadow:'0 2px 6px #000'}}>{s.source}</div>
  </div>
 </AbsoluteFill>;
};
