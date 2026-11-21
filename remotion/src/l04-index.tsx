import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {L04Overlay} from './l04-overlays';
registerRoot(()=> <Composition id="L04Overlay" component={L04Overlay} defaultProps={{shot:{}}} durationInFrames={1800} fps={30} width={3840} height={2160}/>);
