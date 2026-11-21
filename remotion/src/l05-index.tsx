import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {L05Overlay} from './l05-overlays';
registerRoot(()=> <Composition id="L05Overlay" component={L05Overlay} defaultProps={{shot:{}}} durationInFrames={1800} fps={30} width={3840} height={2160}/>);
