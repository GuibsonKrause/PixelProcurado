import {bundle} from '@remotion/bundler';
import {renderStill,renderFrames,openBrowser} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const data=JSON.parse(fs.readFileSync('../producao/L02/projeto/edicao_l02.json','utf8'));
const root=path.resolve('../producao/L02/projeto/overlays');
fs.mkdirSync(root,{recursive:true});fs.mkdirSync('out/empty-public',{recursive:true});
const component=fs.readFileSync('src/l02-overlays.tsx','utf8');
const url=await bundle({entryPoint:path.resolve('src/l02-overlays.tsx'),publicDir:path.resolve('out/empty-public')});
const browser=await openBrowser('chrome');
const selected=process.argv[2]?.split(',').map(Number);
try{
 for(let i=0;i<data.shots.length;i++){
  if(selected&&!selected.includes(i))continue;
  const s=data.shots[i],folder=path.join(root,String(i).padStart(3,'0'));
  fs.mkdirSync(folder,{recursive:true});
  const sig=crypto.createHash('sha256').update(JSON.stringify(s)+component).digest('hex');
  const done=path.join(folder,'complete.json');
  if(fs.existsSync(done)&&JSON.parse(fs.readFileSync(done,'utf8')).sig===sig){console.log(`Reuse overlay ${i+1}`);continue;}
  const composition={id:'L02Overlay',width:3840,height:2160,fps:30,durationInFrames:Math.max(300,s.frames),defaultProps:{shot:s},props:{shot:s}};
  if(s.animate){
   await renderFrames({serveUrl:url,composition,inputProps:{shot:s},outputDir:folder,imageFormat:'png',frameRange:[0,s.animationFrames-1],omitBackground:true,concurrency:2,puppeteerInstance:browser,onStart:()=>{},onFrameUpdate:()=>{}});
   const frames=fs.readdirSync(folder).filter(x=>/^element-.*\.png$/.test(x)).sort();
   if(frames.length!==s.animationFrames)throw Error(`Frame count ${i}: ${frames.length}`);
   // Explicit filenames allow FFmpeg to read the animation without assumptions about Remotion padding.
   frames.forEach((file,j)=>fs.copyFileSync(path.join(folder,file),path.join(folder,`frame-${String(j).padStart(4,'0')}.png`)));
  }else{
   await renderStill({serveUrl:url,composition,inputProps:{shot:s},frame:29,output:path.join(folder,'frame-0000.png'),imageFormat:'png',omitBackground:true,puppeteerInstance:browser});
  }
  fs.writeFileSync(done,JSON.stringify({sig,frames:s.animationFrames}));
  console.log(`Overlay ${i+1}/${data.shots.length} | ${s.animationFrames} frames`);
 }
}finally{await browser.close({silent:true});}
