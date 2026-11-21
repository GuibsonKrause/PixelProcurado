import {bundle} from '@remotion/bundler';
import {renderFrames,openBrowser} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const base=path.resolve('../producao/shorts');
const ids=process.argv.slice(2);
// A separately prefetched batch owns these IDs until its process exits.
const prefetchFile=path.join(base,'_acervo/prefetch.json');
if(fs.existsSync(prefetchFile)){
 const prefetch=JSON.parse(fs.readFileSync(prefetchFile,'utf8'));
 if(prefetch.pid!==process.pid&&ids.some(id=>prefetch.ids.includes(id))){
  let announced=false;
  while(true){
   try{process.kill(prefetch.pid,0)}catch{break}
   if(!announced){console.log('Waiting for the existing overlay batch');announced=true}
   await new Promise(resolve=>setTimeout(resolve,2000));
  }
 }
}
const component=fs.readFileSync('src/shorts-overlays.tsx','utf8');
fs.mkdirSync('out/empty-public',{recursive:true});
const url=await bundle({entryPoint:path.resolve('src/shorts-overlays.tsx'),publicDir:path.resolve('out/empty-public')});
const browser=await openBrowser('chrome');
try{
 for(const id of ids){
  const data=JSON.parse(fs.readFileSync(path.join(base,id,'projeto/timeline.json'),'utf8'));
  for(const s of data.shots){
   const out=path.join(base,id,'projeto/overlays',String(s.index).padStart(3,'0'));fs.mkdirSync(out,{recursive:true});
   const sig=crypto.createHash('sha256').update(JSON.stringify(s)+component).digest('hex');const marker=path.join(out,'complete.json');
   if(fs.existsSync(marker)&&JSON.parse(fs.readFileSync(marker,'utf8')).sig===sig)continue;
   const composition={id:'ShortsOverlay',width:1080,height:1920,fps:30,durationInFrames:Math.max(s.frames,60),defaultProps:{shot:s},props:{shot:s}};
   await renderFrames({serveUrl:url,composition,inputProps:{shot:s},outputDir:out,imageFormat:'png',frameRange:[0,s.animationFrames-1],omitBackground:true,concurrency:2,puppeteerInstance:browser,onStart:()=>{},onFrameUpdate:()=>{}});
   const frames=fs.readdirSync(out).filter(x=>/^element-.*\.png$/.test(x)).sort();
   if(frames.length!==s.animationFrames)throw Error(`Unexpected overlay count: ${id}/${s.index}`);
   frames.forEach((file,i)=>fs.renameSync(path.join(out,file),path.join(out,`frame-${String(i).padStart(4,'0')}.png`)));
   fs.writeFileSync(marker,JSON.stringify({sig,frames:s.animationFrames}));
   console.log(`OVERLAY ${id} ${s.index+1}/${data.shots.length}`);
  }
 }
}finally{await browser.close({silent:true});}
