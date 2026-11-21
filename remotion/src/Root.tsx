import React from 'react';
import {Edicao} from './Edicao';
import data from './edicao.json';
import {
  AbsoluteFill,
  Composition,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const PixelProcuradoBase: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entrance = spring({frame, fps, config: {damping: 14}});
  const opacity = interpolate(frame, [0, 12, 130, 149], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0c0d13',
        color: '#f8f8fa',
        fontFamily: 'Arial, sans-serif',
        justifyContent: 'center',
        padding: 110,
        opacity,
      }}
    >
      <div
        style={{
          width: 14,
          height: 650,
          backgroundColor: '#ffd33d',
          position: 'absolute',
          left: 100,
          transform: `scaleY(${entrance})`,
        }}
      />
      <div style={{fontSize: 38, color: '#a7abb8', fontWeight: 700}}>
        PIXEL PROCURADO / DOSSIÊ 01
      </div>
      <div
        style={{
          fontSize: 126,
          color: '#ffd33d',
          fontWeight: 900,
          marginTop: 130,
          transform: `translateX(${interpolate(entrance, [0, 1], [-100, 0])}px)`,
        }}
      >
        REMOTION INSTALADO
      </div>
      <div style={{fontSize: 54, fontWeight: 700, marginTop: 55}}>
        Template automatizado do canal
      </div>
    </AbsoluteFill>
  );
};

export const Root: React.FC = () => (
  <>
  <Composition id="Video1Final4K" component={Edicao} durationInFrames={data.frames} fps={30} width={3840} height={2160}/>
  <Composition
    id="PixelProcuradoBase"
    component={PixelProcuradoBase}
    durationInFrames={150}
    fps={30}
    width={1920}
    height={1080}
  />
  </>
);
