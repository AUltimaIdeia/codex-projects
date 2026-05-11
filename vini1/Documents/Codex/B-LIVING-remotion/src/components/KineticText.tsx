import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SrtCue} from '../utils/parseSrt';

type KineticTextProps = {
  cue: SrtCue;
  durationInFrames: number;
  index: number;
  totalCues: number;
  serifFamily: string;
  sansFamily: string;
};

const colors = {
  beige: '#D8CFC4',
  navy: '#071A3D',
  offWhite: '#F7F4EF',
  sand: '#9B9086',
  taupe: '#6F6258',
};

const keywords = [
  'Florianópolis',
  'mercado imobiliário',
  'sofisticada',
  'integração',
  'confiança',
  'família',
  'inovação',
  'qualidade',
  'propósito',
  'futuro',
  'cidade',
  'evolução',
  'raro',
  'believe',
  'believing',
];

const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const keywordPattern = new RegExp(`(${keywords.sort((a, b) => b.length - a.length).map(escapeRegExp).join('|')})`, 'gi');

const splitIntoLines = (text: string): string[] => {
  const cleaned = text.replace(/\s+/g, ' ').trim();

  if (cleaned.length <= 30) {
    return [cleaned];
  }

  const targetLines = cleaned.length > 68 ? 3 : 2;
  const words = cleaned.split(' ');
  const targetLength = Math.ceil(cleaned.length / targetLines);
  const lines: string[] = [];
  let current = '';

  for (const word of words) {
    const proposed = current ? `${current} ${word}` : word;
    const shouldBreak = proposed.length > targetLength && lines.length < targetLines - 1;

    if (shouldBreak && current.length > 0) {
      lines.push(current);
      current = word;
    } else {
      current = proposed;
    }
  }

  if (current.length > 0) {
    lines.push(current);
  }

  return lines;
};

const getVariant = (text: string, index: number) => {
  const short = text.length <= 28;
  const impact = /evolução|confiança|família|raro|inovação|believe|believing/i.test(text);

  if (short && impact) {
    return 'impact';
  }

  if (short) {
    return 'manifesto';
  }

  if (index % 5 === 1) {
    return 'dark';
  }

  if (index % 5 === 3) {
    return 'institutional';
  }

  return 'editorial';
};

const renderRichText = (
  line: string,
  highlightColor: string,
  serifFamily: string,
  frame: number,
  inFrames: number,
) => {
  let wordIndex = 0;

  return line.split(keywordPattern).flatMap((part, partIndex) => {
    const isKeyword = keywords.some((keyword) => keyword.toLocaleLowerCase('pt-BR') === part.toLocaleLowerCase('pt-BR'));

    return part.split(/(\s+)/).map((token, tokenIndex) => {
      if (/^\s+$/.test(token)) {
        return <React.Fragment key={`${part}-${partIndex}-${tokenIndex}`}>{token}</React.Fragment>;
      }

      const delay = Math.min(wordIndex, 8) * 2;
      const reveal = interpolate(frame, [delay, inFrames + delay], [0, 1], {
        easing: Easing.bezier(0.16, 1, 0.3, 1),
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      });

      wordIndex += 1;

      return (
        <span
          key={`${part}-${partIndex}-${tokenIndex}`}
          style={{
            color: isKeyword ? highlightColor : undefined,
            display: 'inline-block',
            fontFamily: isKeyword ? serifFamily : undefined,
            fontWeight: isKeyword ? 700 : undefined,
            opacity: reveal,
            transform: `translateY(${(1 - reveal) * 12}px)`,
          }}
        >
          {token}
        </span>
      );
    });
  });
};

export const KineticText: React.FC<KineticTextProps> = ({
  cue,
  durationInFrames,
  index,
  totalCues,
  serifFamily,
  sansFamily,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const variant = getVariant(cue.text, index);
  const lines = splitIntoLines(cue.text);

  const inFrames = Math.min(durationInFrames * 0.45, fps * 0.75);
  const outStart = Math.max(inFrames + 1, durationInFrames - Math.min(fps * 0.35, durationInFrames * 0.3));
  const ease = Easing.bezier(0.16, 1, 0.3, 1);

  const opacity = interpolate(frame, [0, inFrames, outStart, durationInFrames], [0, 1, 1, 0], {
    easing: ease,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = interpolate(frame, [0, inFrames], [34, 0], {
    easing: ease,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const blur = interpolate(frame, [0, inFrames], [8, 0], {
    easing: ease,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const tracking = interpolate(frame, [0, inFrames], [1.8, 0], {
    easing: ease,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const scale = interpolate(frame, [0, Math.max(1, durationInFrames - 1)], [0.985, 1.012], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const lineProgress = interpolate(frame, [0, inFrames], [0, 1], {
    easing: ease,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const isDark = variant === 'dark' || variant === 'impact';
  const background = isDark ? colors.navy : colors.offWhite;
  const primary = isDark ? colors.offWhite : colors.navy;
  const secondary = isDark ? colors.beige : colors.taupe;
  const highlight = isDark ? colors.beige : colors.navy;
  const longTextFactor = cue.text.length > 86 ? 0.74 : cue.text.length > 58 ? 0.86 : 1;
  const baseSize =
    variant === 'impact' ? 132 : variant === 'manifesto' ? 90 : variant === 'institutional' ? 66 : variant === 'dark' ? 82 : 76;
  const fontSize = Math.round(baseSize * longTextFactor);
  const textAlign = variant === 'institutional' || variant === 'editorial' ? 'left' : 'center';
  const justifyContent = variant === 'institutional' || variant === 'editorial' ? 'flex-start' : 'center';
  const topOffset = variant === 'institutional' || variant === 'editorial' ? 560 : 0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: background,
        color: primary,
        fontFamily: sansFamily,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          borderColor: isDark ? 'rgba(216,207,196,0.24)' : 'rgba(7,26,61,0.16)',
          borderStyle: 'solid',
          borderWidth: 1,
          bottom: 70,
          left: 70,
          position: 'absolute',
          right: 70,
          top: 70,
        }}
      />
      <div
        style={{
          color: secondary,
          fontFamily: sansFamily,
          fontSize: 18,
          fontWeight: 500,
          left: 96,
          letterSpacing: '0.18em',
          position: 'absolute',
          right: 96,
          textAlign: 'left',
          textTransform: 'uppercase',
          top: 104,
        }}
      >
        B. LIVING
      </div>
      <div
        style={{
          backgroundColor: secondary,
          height: 1,
          left: 96,
          opacity: 0.45,
          position: 'absolute',
          right: 96,
          top: 152,
          transform: `scaleX(${lineProgress})`,
          transformOrigin: 'left center',
        }}
      />
      <div
        style={{
          bottom: 104,
          color: secondary,
          fontFamily: sansFamily,
          fontSize: 16,
          fontWeight: 400,
          left: 96,
          letterSpacing: '0.12em',
          opacity: 0.82,
          position: 'absolute',
          textTransform: 'uppercase',
        }}
      >
        {String(index + 1).padStart(2, '0')} / {String(totalCues).padStart(2, '0')}
      </div>
      <div
        style={{
          alignItems: textAlign === 'center' ? 'center' : 'flex-start',
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          justifyContent,
          opacity,
          padding: textAlign === 'center' ? '0 126px' : `0 116px 0 116px`,
          paddingTop: topOffset,
          transform: `translateY(${y}px) scale(${scale})`,
          filter: `blur(${blur}px)`,
        }}
      >
        <div
          style={{
            maxWidth: textAlign === 'center' ? 850 : 780,
            textAlign,
          }}
        >
          {lines.map((line, lineIndex) => {
            const stagger = interpolate(frame, [lineIndex * 3, inFrames + lineIndex * 3], [0, 1], {
              easing: ease,
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });

            return (
              <div
                key={`${cue.id}-${lineIndex}`}
                style={{
                  fontFamily: variant === 'institutional' ? sansFamily : serifFamily,
                  fontSize,
                  fontWeight: variant === 'institutional' ? 500 : 600,
                  letterSpacing: `${tracking}px`,
                  lineHeight: variant === 'impact' ? 0.92 : 1.03,
                  marginTop: lineIndex === 0 ? 0 : 10,
                  opacity: stagger,
                  transform: `translateY(${(1 - stagger) * 24}px)`,
                }}
              >
                {renderRichText(line, highlight, serifFamily, frame, inFrames)}
              </div>
            );
          })}
        </div>
      </div>
      {variant === 'dark' ? (
        <div
          style={{
            borderBottom: `1px solid rgba(216,207,196,${0.18 + lineProgress * 0.22})`,
            bottom: 320,
            left: 116,
            position: 'absolute',
            right: 116,
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};
