import React from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame,interpolate} from 'remotion';

const gold='#ffd33d';
const cl={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const Overlay:React.FC<{shot:any}>=({shot:s})=>{
 const f=useCurrentFrame();
 const ease=(delay=0)=>{const p=interpolate(f-delay,[0,23],[0,1],cl);return 1-Math.pow(1-p,3)};
 const p=ease();
 const full=s.kind==='graphic';
 const cue=(i:number)=>ease(s.cues?.[i]??i*5);
 const left=s.graphic==='questions'||s.graphic==='checklist';
 const lower=s.graphic==='headline'&&(s.file.includes('/Lucia Caminos/')||s.file.endsWith('Jason_and_Lucia_03.jpg'));
 const card:React.CSSProperties={position:'absolute',left:left?96:990,top:lower?570:330,width:800,opacity:p,transform:`translateY(${(1-p)*32}px)`};
 const ring=(x:number,y:number,w:number,h:number,delay=0)=>{
  const q=ease(delay);return <rect x={x} y={y} width={w} height={h} rx={28} fill="none" stroke={gold} strokeWidth={4} pathLength={1} strokeDasharray={1} strokeDashoffset={1-q} opacity={q}/>;
 };
 return <AbsoluteFill style={{color:'white',fontFamily:'Arial, sans-serif'}}>
  <div style={{width:1920,height:1080,position:'absolute',transform:'scale(2)',transformOrigin:'top left'}}>
   <AbsoluteFill style={{background:full?'radial-gradient(ellipse at 25% 30%,#23303d 0%,#0d1420 48%,#070b12 100%)':'linear-gradient(0deg,rgba(5,8,15,.54),transparent 28%,transparent 76%,rgba(5,8,15,.46))'}}/>
   {s.title&&!full&&<AbsoluteFill style={{opacity:p,background:`linear-gradient(${left?270:90}deg,transparent 24%,rgba(7,11,18,.35) 48%,rgba(7,11,18,.90) 100%)`}}/>}
   {full&&<svg width="1920" height="1080" style={{position:'absolute',opacity:.08}}>{Array.from({length:17},(_,i)=><line key={i} x1={i*120} y1={0} x2={i*120} y2={1080} stroke="white"/>)}{Array.from({length:10},(_,i)=><line key={i} x1={0} y1={i*120} x2={1920} y2={i*120} stroke="white"/>)}</svg>}
   <div style={{position:'absolute',left:96,top:77,display:'flex',gap:16,alignItems:'center',textShadow:'0 2px 12px #000'}}><span style={{background:gold,width:6,height:26}}/><span style={{fontSize:22,fontWeight:700,letterSpacing:2}}>{s.label||'GTA VI / IMAGENS DE APOIO'}</span></div>
   <div style={{position:'absolute',right:84,top:80,fontSize:17,fontWeight:700,letterSpacing:2,textShadow:'0 2px 12px #000'}}>PIXEL <span style={{color:gold}}>/</span> PROCURADO</div>
   {s.graphic==='headline'&&<div style={card}><div style={{height:5,width:100*p,background:gold,marginBottom:28}}/><div style={{fontSize:s.title.length>28?68:80,fontWeight:800,lineHeight:1.08,letterSpacing:-2,whiteSpace:'pre-line'}}>{s.title}</div>{s.sub&&<div style={{fontSize:28,lineHeight:1.4,color:'#d6dce5',marginTop:25}}>{s.sub}</div>}</div>}
   {(s.graphic==='questions'||s.graphic==='checklist')&&<div style={{...card,opacity:1,transform:undefined,top:280}}>{(s.graphic==='questions'?['Dinheiro?','Autonomia?','Um futuro juntos?']:['Quem propõe?','Quem hesita?','O que teme perder?']).map((t,i)=><div key={t} style={{opacity:cue(i),transform:`translateX(${(1-cue(i))*40}px)`,marginBottom:30,display:'flex',alignItems:'center',gap:22}}><span style={{fontSize:23,color:gold,fontWeight:700}}>0{i+1}</span><span style={{fontSize:58,fontWeight:700,letterSpacing:-1}}>{t}</span></div>)}</div>}
   {s.graphic==='dilemma'&&<>
    <div style={{position:'absolute',left:160,top:230,opacity:p,transform:`translateY(${(1-p)*25}px)`}}><div style={{fontSize:22,color:gold,letterSpacing:4,fontWeight:700}}>A MESMA OPORTUNIDADE</div><div style={{fontSize:72,fontWeight:800,marginTop:20,letterSpacing:-2}}>{s.title}</div><div style={{fontSize:29,color:'#c0cad6',marginTop:18}}>{s.sub}</div></div>
    {['RECOMPENSA','RISCO'].map((t,i)=>{const active=s.stage===0||s.stage>=3||s.stage===i+1;const q=ease(i*3);return <div key={t} style={{position:'absolute',left:160+i*820,top:480,width:740,height:250,border:`2px solid ${active?gold:'#4b5565'}`,borderRadius:22,background:active?'#ffd33d0e':'#ffffff05',opacity:q*(active?1:.48),transform:`translateY(${(1-q)*26}px)`,padding:38,boxSizing:'border-box'}}><div style={{fontSize:24,color:active?gold:'#b0bccb',letterSpacing:4,fontWeight:700}}>{t}</div><div style={{fontSize:46,fontWeight:700,marginTop:24}}>{i===0?'Finalmente parar.':'Perder o que ainda tem.'}</div></div>})}
    <div style={{position:'absolute',left:930,top:570,fontSize:42,color:gold,opacity:p}}>↔</div>
    <div style={{position:'absolute',left:160,top:780,fontSize:23,color:'#b9c3ce'}}>Hipótese ilustrativa • Não representa uma cena anunciada do jogo</div>
   </>}
   {s.graphic==='focus'&&<svg width="1920" height="1080" style={{position:'absolute',left:0,top:0,filter:'drop-shadow(0 2px 5px #0008)'}}>
    {s.focusType==='couple'&&ring(505,140,860,690)}
    {(s.focusType==='boats'||s.focusType==='surround')&&<>{ring(145,610,270,340)}{ring(1470,410,410,450)}{ring(1430,8,290,235,s.heliCue||0)}</>}
   </svg>}
   <div style={{position:'absolute',left:96,bottom:37,fontSize:17,letterSpacing:.5,color:'#d6dce5',textShadow:'0 2px 6px #000'}}>{s.source||(full?'PIXEL PROCURADO • GRÁFICO EDITORIAL':'GTA VI • Imagens: Rockstar Games • Análise: Pixel Procurado')}</div>
  </div>
 </AbsoluteFill>;
};
registerRoot(()=> <Composition id="L02Overlay" component={Overlay} defaultProps={{shot:{}}} durationInFrames={300} fps={30} width={3840} height={2160}/>);
