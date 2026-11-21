import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {L03Overlay} from './l03-overlays';
registerRoot(()=> <Composition id="L03Overlay" component={L03Overlay} defaultProps={{shot:{}}} durationInFrames={1800} fps={30} width={3840} height={2160}/>);
