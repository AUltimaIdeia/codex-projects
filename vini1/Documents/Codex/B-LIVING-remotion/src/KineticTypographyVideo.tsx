import React, {useCallback, useEffect, useMemo, useState} from 'react';
import {
  AbsoluteFill,
  Sequence,
  cancelRender,
  continueRender,
  delayRender,
  staticFile,
  useVideoConfig,
} from 'remotion';
import {Audio} from '@remotion/media';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadCormorant} from '@remotion/google-fonts/CormorantGaramond';
import {KineticText} from './components/KineticText';
import {parseSrt, type SrtCue} from './utils/parseSrt';

const inter = loadInter('normal', {
  subsets: ['latin'],
  weights: ['300', '400', '500', '600', '700'],
});

const cormorant = loadCormorant('normal', {
  subsets: ['latin'],
  weights: ['400', '500', '600', '700'],
});

export type KineticTypographyVideoProps = {
  srtFile: string;
  audioFile?: string;
  cues?: SrtCue[];
};

const useSrtCues = (srtFile: string, providedCues?: SrtCue[]) => {
  const [handle] = useState(() => delayRender('Loading B. LIVING typography assets'));
  const [cues, setCues] = useState<SrtCue[] | null>(providedCues ?? null);

  const loadCues = useCallback(async () => {
    try {
      await Promise.all([inter.waitUntilDone(), cormorant.waitUntilDone()]);

      if (providedCues) {
        setCues(providedCues);
        continueRender(handle);
        return;
      }

      const response = await fetch(staticFile(srtFile));

      if (!response.ok) {
        throw new Error(`Could not load ${srtFile}`);
      }

      const text = await response.text();
      setCues(parseSrt(text));
      continueRender(handle);
    } catch (error) {
      cancelRender(error as Error);
    }
  }, [handle, providedCues, srtFile]);

  useEffect(() => {
    loadCues();
  }, [loadCues]);

  return cues;
};

export const KineticTypographyVideo: React.FC<KineticTypographyVideoProps> = ({
  srtFile,
  audioFile,
  cues: providedCues,
}) => {
  const cues = useSrtCues(srtFile, providedCues);
  const {fps} = useVideoConfig();

  const timedCues = useMemo(() => {
    return (cues ?? []).map((cue) => ({
      ...cue,
      from: Math.max(0, Math.round((cue.startMs / 1000) * fps)),
      duration: Math.max(1, Math.ceil(((cue.endMs - cue.startMs) / 1000) * fps)),
    }));
  }, [cues, fps]);

  if (!cues) {
    return null;
  }

  return (
    <AbsoluteFill style={{backgroundColor: '#F7F4EF'}}>
      {audioFile ? <Audio src={staticFile(audioFile)} /> : null}
      {timedCues.map((cue, index) => (
        <Sequence key={`${cue.id}-${cue.startMs}`} from={cue.from} durationInFrames={cue.duration}>
          <KineticText
            cue={cue}
            durationInFrames={cue.duration}
            index={index}
            totalCues={timedCues.length}
            serifFamily={cormorant.fontFamily}
            sansFamily={inter.fontFamily}
          />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
