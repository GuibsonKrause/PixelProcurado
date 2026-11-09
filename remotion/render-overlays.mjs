import {bundle} from '@remotion/bundler';
import {renderStill,openBrowser} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const data=JSON.parse(fs.readFileSync('src/edicao.json','utf8'));
fs.mkdirSync('out/overlays',{recursive:true});
fs.mkdirSync('out/empty-public',{recursive:true});
const url=await bundle({entryPoint:path.resolve('src/overlay-index.tsx'),publicDir:path.resolve('out/empty-public')});
const browser=await openBrowser('chrome');
try {
 for(let i=0;i<data.shots.length;i++){
  const output=path.resolve(`out/overlays/${String(i).padStart(3,'0')}.png`);
  if(fs.existsSync(output))continue;
  await renderStill({serveUrl:url,composition:{id:'Overlay',width:3840,height:2160,fps:30,durationInFrames:30,defaultProps:{},props:{}},output,inputProps:{index:i},imageFormat:'png',omitBackground:true,puppeteerInstance:browser});
  console.log(`Overlay ${i+1}/${data.shots.length}`);
 }
} finally {await browser.close({silent:true});}
