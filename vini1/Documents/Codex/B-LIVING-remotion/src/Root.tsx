import React from 'react';
import {Composition, type CalculateMetadataFunction, staticFile} from 'remotion';
import {KineticTypographyVideo, type KineticTypographyVideoProps} from './KineticTypographyVideo';
import {getDurationInFramesFromSrt, parseSrt} from './utils/parseSrt';

const FPS = 30;
const WIDTH = 1080;
const HEIGHT = 1920;

const defaultProps: KineticTypographyVideoProps = {
  srtFile: '0428.srt',
  audioFile: 'audio-inauguracao.mp3',
};

const calculateMetadata: CalculateMetadataFunction<KineticTypographyVideoProps> = async ({props}) => {
  const response = await fetch(staticFile(props.srtFile));

  if (!response.ok) {
    throw new Error(`Could not load SRT file: ${props.srtFile}`);
  }

  const srt = await response.text();
  const cues = parseSrt(srt);

  return {
    durationInFrames: getDurationInFramesFromSrt(cues, FPS),
    fps: FPS,
    height: HEIGHT,
    props: {
      ...props,
      cues,
    },
    width: WIDTH,
  };
};

export const Root: React.FC = () => {
  return (
    <Composition
      id="KineticTypographyVideo"
      component={KineticTypographyVideo}
      durationInFrames={FPS * 10}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
      defaultProps={defaultProps}
      calculateMetadata={calculateMetadata}
    />
  );
};
