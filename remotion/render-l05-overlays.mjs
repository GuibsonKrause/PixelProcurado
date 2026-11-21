import {bundle} from '@remotion/bundler';
import {renderStill,renderFrames,openBrowser} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const here=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1'));
process.chdir(decodeURIComponent(here));
const data=JSON.parse(fs.readFileSync('../producao/L05/projeto/edicao_l05.json','utf8'));
if(data.status!=='final-direction')throw Error('L05 timeline must be final-direction');
const selected=process.argv[2]?.split(',').map(Number);
if(!selected?.length)throw Error('Pass explicit shot indices; renderizar_l05.py owns sequential production');
const root=path.resolve('../producao/L05/projeto/overlays');
const component=fs.readFileSync('src/l05-overlays.tsx','utf8')+fs.readFileSync('src/l05-index.tsx','utf8');
fs.mkdirSync('out/empty-public',{recursive:true});
const url=await bundle({entryPoint:path.resolve('src/l05-index.tsx'),publicDir:path.resolve('out/empty-public')});
const browser=await openBrowser('chrome');
try{
 for(const i of selected){
  const s=data.shots[i];if(!s)throw Error(`Unknown shot ${i}`);
  const folder=path.join(root,String(i).padStart(3,'0'));fs.mkdirSync(folder,{recursive:true});
  const sig=crypto.createHash('sha256').update(JSON.stringify(s)+component).digest('hex');
  const done=path.join(folder,'complete.json'), count=s.animate?s.animationFrames:1;
  if(fs.existsSync(done)){const d=JSON.parse(fs.readFileSync(done,'utf8'));if(d.sig===sig&&Array.from({length:count},(_,j)=>path.join(folder,`frame-${String(j).padStart(4,'0')}.png`)).every(f=>fs.existsSync(f)&&fs.statSync(f).size>0)){console.log(`Reuse overlay ${i}`);continue;}}
  if(fs.existsSync(done))fs.unlinkSync(done);
  // Only regenerated L05 PNGs in this verified shot folder are replaced.
  for(const f of fs.readdirSync(folder))if(/^(frame-\d+|element-.*)\.png$/.test(f))fs.unlinkSync(path.join(folder,f));
  const composition={id:'L05Overlay',width:3840,height:2160,fps:30,durationInFrames:Math.max(s.frames,count),defaultProps:{shot:s},props:{shot:s}};
  if(s.animate){
   // Rasterize every moving frame. Holds are exact hardlinks of the last
   // rendered frame, avoiding repeated screenshots of unchanged list states.
   const active=new Set([0]);
   const cues=s.graphic==='list'?(s.cues||[0]):s.graphic==='focus'?(s.focusRects||[]).map(r=>r.cue||0):[0];
   for(const cue of cues)if(cue>=0)for(let f=cue;f<=cue+19&&f<count;f++)active.add(f);
   const frames=[...active].sort((a,b)=>a-b),ranges=[];
   for(const f of frames){const r=ranges.at(-1);if(r&&r[1]===f-1)r[1]=f;else ranges.push([f,f]);}
   for(const [from,to] of ranges){
    const tmp=path.join(folder,`range-${from}`);fs.mkdirSync(tmp,{recursive:true});
    await renderFrames({serveUrl:url,composition,inputProps:{shot:s},outputDir:tmp,imageFormat:'png',frameRange:[from,to],omitBackground:true,concurrency:1,puppeteerInstance:browser,onStart:()=>{},onFrameUpdate:()=>{}});
    const made=fs.readdirSync(tmp).filter(f=>/^element-.*\.png$/.test(f)).sort();
    if(made.length!==to-from+1)throw Error(`Overlay ${i}: sparse range incomplete`);
    made.forEach((f,j)=>fs.renameSync(path.join(tmp,f),path.join(folder,`frame-${String(from+j).padStart(4,'0')}.png`)));
    fs.rmdirSync(tmp);
   }
   let last=0;
   for(let f=0;f<count;f++){const file=path.join(folder,`frame-${String(f).padStart(4,'0')}.png`);if(fs.existsSync(file))last=f;else fs.linkSync(path.join(folder,`frame-${String(last).padStart(4,'0')}.png`),file);}
  }else await renderStill({serveUrl:url,composition,inputProps:{shot:s},frame:0,output:path.join(folder,'frame-0000.png'),imageFormat:'png',omitBackground:true,puppeteerInstance:browser});
  fs.writeFileSync(done,JSON.stringify({sig,frames:count,width:3840,height:2160}));console.log(`Overlay ${i}: ${count} frames`);
 }
}finally{await browser.close({silent:true});}
