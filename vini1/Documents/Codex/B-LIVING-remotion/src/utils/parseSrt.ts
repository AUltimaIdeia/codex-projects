export type SrtCue = {
  id: number;
  startMs: number;
  endMs: number;
  text: string;
};

const timestampPattern = /(\d{2}):(\d{2}):(\d{2}),(\d{1,3})/;

const parseTimestamp = (value: string): number => {
  const match = value.match(timestampPattern);

  if (!match) {
    throw new Error(`Invalid SRT timestamp: ${value}`);
  }

  const [, hours, minutes, seconds, milliseconds] = match;
  const normalizedMs = milliseconds.padEnd(3, '0');

  return (
    Number(hours) * 60 * 60 * 1000 +
    Number(minutes) * 60 * 1000 +
    Number(seconds) * 1000 +
    Number(normalizedMs)
  );
};

export const parseSrt = (input: string): SrtCue[] => {
  const normalized = input.replace(/\uFEFF/g, '').replace(/\r\n/g, '\n').trim();

  if (normalized.length === 0) {
    return [];
  }

  return normalized
    .split(/\n{2,}/)
    .map((block, blockIndex) => {
      const lines = block.split('\n').map((line) => line.trimEnd());
      const timingLineIndex = lines.findIndex((line) => line.includes('-->'));

      if (timingLineIndex === -1) {
        throw new Error(`Invalid SRT block without timing line: ${block}`);
      }

      const [startRaw, endRaw] = lines[timingLineIndex].split('-->');
      const text = lines
        .slice(timingLineIndex + 1)
        .join('\n')
        .trim();

      return {
        id: Number(lines[0]) || blockIndex + 1,
        startMs: parseTimestamp(startRaw.trim()),
        endMs: parseTimestamp(endRaw.trim()),
        text,
      };
    })
    .filter((cue) => cue.text.length > 0 && cue.endMs > cue.startMs);
};

export const getDurationInFramesFromSrt = (cues: SrtCue[], fps: number): number => {
  const lastEndMs = cues.reduce((max, cue) => Math.max(max, cue.endMs), 0);
  return Math.max(1, Math.ceil((lastEndMs / 1000) * fps) + Math.round(fps * 0.45));
};
