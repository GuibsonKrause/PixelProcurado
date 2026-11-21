import React from 'react';
import {AbsoluteFill,Composition,registerRoot} from 'remotion';
import {L05Overlay} from './l05-overlays';

const L06Overlay: React.FC<{shot:any}> = ({shot}) => (
  <AbsoluteFill>
    {shot.graphic === 'headline' && shot.presentation === 'full' && (
      <AbsoluteFill style={{background:'linear-gradient(90deg, rgba(5,9,18,.76) 0%, rgba(5,9,18,.48) 34%, transparent 66%)'}}/>
    )}
    <L05Overlay shot={shot}/>
  </AbsoluteFill>
);
registerRoot(()=> <Composition id="L06Overlay" component={L06Overlay} defaultProps={{shot:{}}} durationInFrames={1800} fps={30} width={3840} height={2160}/>);
