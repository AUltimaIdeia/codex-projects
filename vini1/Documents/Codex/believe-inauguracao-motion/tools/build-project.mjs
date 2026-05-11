import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), "..");
const srtPath = path.join(root, "data", "0428.srt");
const captionJsonPath = path.join(root, "data", "captions.json");
const assPath = path.join(root, "data", "captions.ass");
const outputPath = path.join(root, "renders", "believe-inauguracao-motion.mp4");
const ffmpegPath = "C:\\Users\\vini1\\AppData\\Local\\CapCut\\Apps\\8.3.0.3497\\ffmpeg.exe";

const palette = {
  deepNavy: "#101C3D",
  warmTaupe: "#5F554C",
  softSand: "#AFA69C",
  elegantBeige: "#D8CEC3",
  pureWhite: "#F7F3EC",
  accent: "#CBBBAA",
};

function toSeconds(stamp) {
  const match = stamp.match(/(\d+):(\d+):(\d+),(\d+)/);
  if (!match) throw new Error(`Invalid SRT timestamp: ${stamp}`);
  const [, hh, mm, ss, ms] = match.map(Number);
  return hh * 3600 + mm * 60 + ss + ms / 1000;
}

function parseSrt(raw) {
  return raw
    .replace(/^\uFEFF/, "")
    .trim()
    .split(/\r?\n\r?\n/)
    .map((block) => {
      const lines = block.split(/\r?\n/).filter(Boolean);
      const index = Number(lines[0]);
      const [startRaw, endRaw] = lines[1].split(/\s+-->\s+/);
      return {
        index,
        start: toSeconds(startRaw),
        end: toSeconds(endRaw),
        text: polishText(lines.slice(2).join(" ")),
      };
    });
}

function polishText(text) {
  let out = text.replace(/\s+/g, " ").trim();
  const feminine = "cidade|fase|família|palavra|empresa|equipe|noite|pessoa|bagagem|metodologia";
  out = out.replace(new RegExp(`\\b1\\s+(${feminine})\\b`, "gi"), "uma $1");
  out = out.replace(/\b1\s+Marco\b/g, "um marco");
  out = out.replace(/\b1\s+marco\b/g, "um marco");
  out = out.replace(/\b1\s+/g, "um ");
  return out.charAt(0).toUpperCase() + out.slice(1);
}

function wrapText(text, maxChars = 29) {
  const words = text.split(/\s+/);
  const lines = [];
  let current = "";
  for (const word of words) {
    if ((current + " " + word).trim().length > maxChars && current) {
      lines.push(current);
      current = word;
    } else {
      current = (current + " " + word).trim();
    }
  }
  if (current) lines.push(current);
  if (lines.length <= 2) return lines;
  return [lines[0], lines.slice(1).join(" ")];
}

const highlightTerms = [
  "B. Living",
  "Believe",
  "Florianópolis",
  "Floripa",
  "inauguração",
  "nascimento",
  "nova fase",
  "mercado",
  "sofisticada",
  "integrada",
  "impacto",
  "valor raro",
  "evolução",
  "confiança",
  "família",
  "negócios",
  "cliente",
  "método",
  "Rafael",
  "prosperidade",
  "parceiros",
];

function htmlHighlight(text) {
  let out = escapeHtml(text);
  for (const term of highlightTerms) {
    const safe = escapeRegExp(escapeHtml(term));
    out = out.replace(new RegExp(`(${safe})`, "gi"), '<span class="accent">$1</span>');
  }
  return out;
}

function assHighlight(text) {
  let out = assEscape(text);
  for (const term of highlightTerms) {
    const safe = escapeRegExp(assEscape(term));
    out = out.replace(
      new RegExp(`(${safe})`, "gi"),
      "{\\c&H00AABBCB&}$1{\\c&H00ECF3F7&}",
    );
  }
  return out;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function assEscape(text) {
  return text.replace(/[{}]/g, "");
}

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function assTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const cs = Math.round((seconds - Math.floor(seconds)) * 100);
  return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}.${String(cs).padStart(2, "0")}`;
}

function filterPath(filePath) {
  return filePath.replace(/\\/g, "/").replace(/^([A-Za-z]):/, "$1\\:");
}

function writeDocs(cues, duration) {
  const beatRows = cues
    .map(
      (cue) =>
        `| ${String(cue.index).padStart(3, "0")} | ${assTime(cue.start)} - ${assTime(cue.end)} | ${cue.text.replace(/\|/g, "\\|")} | Soft fade up, accent nouns, lower safe area |`,
    )
    .join("\n");

  fs.writeFileSync(
    path.join(root, "DESIGN.md"),
    `# B. Living Motion Visual System

## Style Position
Premium real-estate inauguration film for Florianopolis: institutional, refined, coastal, celebratory, and editorial. The visual system follows the supplied B. Living kit visual.

## Colors
- Deep Navy: ${palette.deepNavy} for authority, logo lockups, lower-panel overlays.
- Warm Taupe: ${palette.warmTaupe} for secondary editorial text and subtle dividers.
- Soft Sand: ${palette.softSand} for supporting lines and quiet UI details.
- Elegant Beige: ${palette.elegantBeige} for panel fills and atmospheric wash.
- Pure White: ${palette.pureWhite} for main caption text.
- Accent Beige: ${palette.accent} for highlighted nouns only.

## Typography
- Titles: Suisse Works when available, with Georgia/Cambria as local fallbacks.
- Text: refined serif for main captions; compact uppercase sans/serif tracking for metadata.

## Layout System
- Master format: 1080 x 1920 vertical, 30fps.
- Top safe area: brand lockup and event label.
- Middle zone: source event video, looped as premium background/footage texture.
- Bottom safe area: caption panel with max two lines per SRT cue.

## Motion Language
- Text uses soft fade-up, slight vertical travel, and short dissolve exits.
- Footage uses slow editorial push through FFmpeg scaling and looped motion.
- Transitions stay restrained: no flashy wipes, no neon, no generic tech gradients.

## Components
- Logo/title: centered B. LIVING wordmark treatment.
- Captions: burned-in, sentence case, two-line maximum where possible.
- Emphasis: key nouns in accent beige only.
- CTA: final cue resolves to Believe Floripa invitation.

## Anti-Patterns
- No loud social-media stickers.
- No single-color blue/purple gradient treatment.
- No oversized type that covers the event footage.
- No unverified public claims beyond the SRT narration.
- No illegible captions outside mobile safe areas.
`,
    "utf8",
  );

  fs.writeFileSync(
    path.join(root, "CREATIVE_STRATEGY.md"),
    `# Creative Strategy

## Objective
- Business goal: turn the inauguration into a premium brand moment for a high-end real-estate operation in Florianopolis.
- Platform goal: vertical motion video for Instagram Reels/Stories and client-facing social distribution.
- Primary metric: full-watch retention and qualified brand interest.
- Approval gate: confirm final MP4, captions, audio sync, and brand tone before publishing.

## Audience
- ICP: high-income buyers, property owners, investors, builders, brokers, and partners in the Florianopolis luxury market.
- Awareness stage: warm to market-aware; the viewer understands real estate value but needs a stronger reason to trust the brand.
- Desired outcome: perceive the opening as a new, more mature and integrated way to do premium real estate.
- Objection: another real-estate office opening may feel ordinary without a clear strategic frame.

## Offer
- Promise: a more sophisticated, connected, client-focused experience in the Florianopolis real-estate market.
- Proof: inauguration, team, partner confidence, method, 18-year leadership background, and local market reading from the narration.
- Differentiator: integration between construction, connection, coordination, and consultative service.
- CTA: "Venha para a Believe Floripa."
- Forbidden claims: do not imply guaranteed returns or unsupported investment performance.

## Angle Set
1. New era of the Florianopolis market.
2. Trust, family, and partnership behind the brand.
3. Premium method and client-focused service.

## Production Decision
- Master: 1080x1920, ${duration.toFixed(3)}s, 30fps, 136 text screens from SRT.
- Captions: burned-in with high-end editorial treatment.
- Variants: master plus shorter hook/crop variants planned in VARIANT_MATRIX.md.
`,
    "utf8",
  );

  fs.writeFileSync(
    path.join(root, "SCRIPT_SHOT_PLAN.md"),
    `# Script And Shot Plan

## Master Specs
- Composition ID: believe-inauguracao-video
- Format: 1080x1920 vertical
- Duration: ${duration.toFixed(3)} seconds
- FPS: 30
- Audio: assets/audio-inauguracao.mp3
- Footage: assets/source-video.mp4, looped as event texture
- Visual source: assets/kit-visual-b-living.jpeg
- Caption source: data/0428.srt, parsed into data/captions.json and data/captions.ass

## Beat Map
| # | Time | Copy | Visual Action |
|---|---:|---|---|
${beatRows}

## Implementation Notes
- Each SRT cue becomes one screen/caption event.
- The HyperFrames source keeps all cue elements as timed clips.
- The render path burns the ASS caption track into the final video using FFmpeg because the local HyperFrames CLI is not available in PATH.
- The WhatsApp source is intentionally looped because the narration is longer than the 14.282s source footage.
`,
    "utf8",
  );

  fs.writeFileSync(
    path.join(root, "VARIANT_MATRIX.md"),
    `# Variant Matrix

## Master Definition
- File: renders/believe-inauguracao-motion.mp4
- Ratio: 9:16
- Duration: ${duration.toFixed(3)}s
- Hook: "Toda grande inauguração simboliza um nascimento."
- Constant elements: B. Living palette, source event footage, burned-in captions, MP3 narration.

## Variant Table
| Variant | Platform | Hypothesis | Angle | Duration | Production Delta | Metric |
|---|---|---|---|---:|---|---|
| Master | Reels/Stories | Full institutional piece builds authority | Nova fase do mercado | ${duration.toFixed(1)}s | None | Completion rate |
| Hook A | Reels | Market-frame hook lifts retention | Mercado mais sofisticado | 45s | First 20 cues + CTA | 3s hold |
| Hook B | Reels | Trust/family angle warms partner audience | Confiança e time | 45s | Middle testimonial cues + CTA | Saves/shares |
| Proof A | Feed | Method and leadership proof drives inquiry | Método/Rafael | 60s | Final proof cues | Qualified DMs |
| Crop A | Feed | Square crop improves feed use | Premium brand recap | 60s | 1080x1080 layout | Watch rate |

## Test Rules
- Use the master as the control.
- Change one primary variable per variant: hook, proof, or crop.
- Keep CTA, palette, and audio source constant.
`,
    "utf8",
  );
}

function writeCaptionFiles(cues, duration) {
  const json = {
    schema: "hyren.hyperframes.caption-track.v1",
    composition_id: "believe-inauguracao-video",
    duration_seconds: duration,
    fps: 30,
    total_screens: cues.length,
    style: {
      mode: "burned_in",
      language: "pt-BR",
      placement: "bottom_safe_area",
      max_lines: 2,
      animation: "soft_fade_up",
      emphasis: "highlight key nouns only",
    },
    cues: cues.map((cue) => ({
      ...cue,
      duration: Number((cue.end - cue.start).toFixed(3)),
      lines: wrapText(cue.text),
    })),
  };

  fs.writeFileSync(captionJsonPath, `${JSON.stringify(json, null, 2)}\n`, "utf8");

  const assEvents = cues
    .map((cue) => {
      const line = wrapText(cue.text)
        .map((part) => assHighlight(part))
        .join("\\N");
      return `Dialogue: 0,${assTime(cue.start)},${assTime(cue.end)},Caption,,0,0,0,,{\\fad(240,220)\\an2\\pos(540,1506)\\blur0.45}${line}`;
    })
    .join("\n");

  fs.writeFileSync(
    assPath,
    `[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption, Georgia, 62, &H00ECF3F7, &H00AABBCB, &H7A101C3D, &HBB101C3D, 0, 0, 0, 0, 100, 100, 0, 0, 1, 2.2, 0.8, 2, 92, 92, 380, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
${assEvents}
`,
    "utf8",
  );
}

function writeIndex(cues, duration) {
  const loopCount = Math.ceil(duration / 14.282);
  const videoClips = Array.from({ length: loopCount }, (_, i) => {
    const start = Number((i * 14.282).toFixed(3));
    const clipDuration = Math.min(14.282, duration - start);
    return `<video id="source-video-${i + 1}" class="event-video" data-start="${start}" data-duration="${clipDuration.toFixed(3)}" data-track-index="0" src="assets/source-video.mp4" muted playsinline></video>`;
  }).join("\n      ");

  const cueClips = cues
    .map((cue) => {
      const lines = wrapText(cue.text).map((line) => `<span>${htmlHighlight(line)}</span>`).join("");
      return `<div id="cue-${String(cue.index).padStart(3, "0")}" class="cue clip" data-start="${cue.start.toFixed(3)}" data-duration="${(cue.end - cue.start).toFixed(3)}" data-track-index="4">${lines}</div>`;
    })
    .join("\n      ");

  fs.writeFileSync(
    path.join(root, "index.html"),
    `<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>B. Living Inauguracao Motion</title>
  </head>
  <body>
    <div data-composition-id="believe-inauguracao-video" data-width="1080" data-height="1920" data-duration="${duration.toFixed(3)}">
      <div class="background-wash" data-layout-ignore></div>
      <img class="visual-kit-texture" src="assets/kit-visual-b-living.jpeg" alt="" data-layout-ignore />
      <div class="video-stage" data-layout-allow-overflow>
        ${videoClips}
      </div>
      <audio id="source-audio" data-start="0" data-duration="${duration.toFixed(3)}" data-track-index="2" src="assets/audio-inauguracao.mp3" data-volume="1"></audio>
      <div class="brand-lockup">
        <div class="brand">B. LIVING</div>
        <div class="rule"></div>
        <div class="eyebrow">INAUGURAÇÃO FLORIPA</div>
      </div>
      <div class="caption-panel" data-layout-ignore></div>
      ${cueClips}
      <style>
        [data-composition-id="believe-inauguracao-video"] {
          position: relative;
          overflow: hidden;
          width: 1080px;
          height: 1920px;
          background: ${palette.deepNavy};
          color: ${palette.pureWhite};
          font-family: "Suisse Works", Georgia, Cambria, serif;
        }
        .background-wash {
          position: absolute;
          inset: 0;
          background:
            linear-gradient(180deg, rgba(16, 28, 61, 0.62), rgba(16, 28, 61, 0.92)),
            radial-gradient(circle at 50% 30%, rgba(216, 206, 195, 0.2), transparent 48%);
          z-index: 1;
        }
        .visual-kit-texture {
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
          opacity: 0.11;
          mix-blend-mode: screen;
          z-index: 2;
        }
        .video-stage {
          position: absolute;
          left: 80px;
          top: 326px;
          width: 920px;
          height: 920px;
          overflow: hidden;
          border: 4px solid rgba(247, 243, 236, 0.72);
          box-shadow: 0 34px 90px rgba(0, 0, 0, 0.34);
          z-index: 4;
        }
        .event-video {
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
          filter: saturate(0.78) contrast(1.05);
        }
        .brand-lockup {
          position: absolute;
          top: 118px;
          left: 0;
          width: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 24px;
          z-index: 8;
          letter-spacing: 0.08em;
        }
        .brand {
          font-size: 76px;
          line-height: 0.95;
          color: ${palette.pureWhite};
        }
        .rule {
          width: 520px;
          height: 1px;
          background: rgba(203, 187, 170, 0.72);
        }
        .eyebrow {
          font-family: Georgia, Cambria, serif;
          font-size: 27px;
          color: ${palette.accent};
        }
        .caption-panel {
          position: absolute;
          left: 70px;
          bottom: 236px;
          width: 940px;
          height: 370px;
          background: rgba(16, 28, 61, 0.74);
          border: 1px solid rgba(203, 187, 170, 0.42);
          z-index: 6;
        }
        .cue {
          position: absolute;
          left: 96px;
          bottom: 318px;
          width: 888px;
          min-height: 188px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 12px;
          text-align: center;
          font-size: 62px;
          line-height: 1.08;
          z-index: 9;
          opacity: 0;
          text-wrap: balance;
        }
        .cue span {
          display: block;
        }
        .accent {
          color: ${palette.accent};
        }
      </style>
      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        window.__timelines = window.__timelines || {};
        const tl = gsap.timeline({ paused: true });
        document.querySelectorAll(".cue").forEach((el) => {
          const start = Number(el.dataset.start);
          const duration = Number(el.dataset.duration);
          tl.fromTo(el, { y: 28, opacity: 0 }, { y: 0, opacity: 1, duration: 0.24, ease: "power2.out" }, start);
          tl.to(el, { y: -18, opacity: 0, duration: 0.22, ease: "power2.in" }, Math.max(start, start + duration - 0.22));
        });
        window.__timelines["believe-inauguracao-video"] = tl;
      </script>
    </div>
  </body>
</html>
`,
    "utf8",
  );
}

function writeRenderScript(duration) {
  fs.writeFileSync(
    path.join(root, "tools", "render-video.mjs"),
    `import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), "..");
const ffmpeg = ${JSON.stringify(ffmpegPath)};
const duration = ${duration.toFixed(3)};

function filterPath(filePath) {
  return filePath.replace(/\\\\/g, "/").replace(/^([A-Za-z]):/, "$1\\\\:");
}

const sourceVideo = path.join(root, "assets", "source-video.mp4");
const kit = path.join(root, "assets", "kit-visual-b-living.jpeg");
const audio = path.join(root, "assets", "audio-inauguracao.mp3");
const ass = path.join(root, "data", "captions.ass");
const output = path.join(root, "renders", "believe-inauguracao-motion.mp4");
const georgia = "C:/Windows/Fonts/georgia.ttf";

const subtitle = filterPath(ass).replace(/'/g, "\\\\'");
const filters = [
  "[0:v]scale=1920:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:1,eq=brightness=-0.20:contrast=1.08:saturation=0.58,setsar=1[bg]",
  "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=rgba,colorchannelmixer=aa=0.16[kit]",
  "[0:v]scale=920:920:force_original_aspect_ratio=increase,crop=920:920,setsar=1,drawbox=x=0:y=0:w=iw:h=ih:color=0xF7F3EC@0.78:t=4[clip]",
  "[bg][kit]overlay=0:0[base1]",
  "[base1][clip]overlay=80:326[base2]",
  "[base2]drawbox=x=70:y=1314:w=940:h=372:color=0x101C3D@0.74:t=fill,drawbox=x=70:y=1314:w=940:h=372:color=0xCBBBAA@0.42:t=2,drawbox=x=250:y=273:w=580:h=1:color=0xCBBBAA@0.72:t=fill[panel]",
  "[panel]drawtext=fontfile='C\\\\:/Windows/Fonts/georgia.ttf':text='B. LIVING':fontcolor=0xF7F3EC:fontsize=76:x=(w-text_w)/2:y=116:shadowcolor=0x101C3D@0.55:shadowx=0:shadowy=2,drawtext=fontfile='C\\\\:/Windows/Fonts/georgia.ttf':text='INAUGURAÇÃO FLORIPA':fontcolor=0xCBBBAA:fontsize=28:x=(w-text_w)/2:y=218:shadowcolor=0x101C3D@0.45:shadowx=0:shadowy=1[subbase]",
  "[subbase]subtitles=filename='" + subtitle + "':fontsdir='C\\\\:/Windows/Fonts'[v]"
].join(";");

const args = [
  "-y",
  "-stream_loop", "-1",
  "-t", String(duration),
  "-i", sourceVideo,
  "-loop", "1",
  "-t", String(duration),
  "-i", kit,
  "-i", audio,
  "-filter_complex", filters,
  "-map", "[v]",
  "-map", "2:a",
  "-t", String(duration),
  "-r", "30",
  "-c:v", "h264_mf",
  "-b:v", "6500k",
  "-pix_fmt", "yuv420p",
  "-c:a", "aac",
  "-b:a", "192k",
  "-movflags", "+faststart",
  output,
];

const result = spawnSync(ffmpeg, args, { stdio: "inherit" });
process.exit(result.status ?? 1);
`,
    "utf8",
  );
}

function maybeRender() {
  if (!fs.existsSync(ffmpegPath)) {
    console.warn(`FFmpeg not found at ${ffmpegPath}`);
    return;
  }
  const result = spawnSync(process.execPath, [path.join(root, "tools", "render-video.mjs")], {
    stdio: "inherit",
  });
  if ((result.status ?? 1) !== 0) {
    process.exit(result.status ?? 1);
  }
}

const raw = fs.readFileSync(srtPath, "utf8");
const cues = parseSrt(raw);
const duration = Number((cues.at(-1).end + 0.334).toFixed(3));

writeCaptionFiles(cues, duration);
writeDocs(cues, duration);
writeIndex(cues, duration);
writeRenderScript(duration);

fs.writeFileSync(
  path.join(root, "QA_REPORT.md"),
  `# QA Report

## Scope
- Master vertical video for B. Living inauguration.
- 136 SRT-derived text screens.
- Duration: ${duration.toFixed(3)}s.

## Generated Assets
- data/captions.json
- data/captions.ass
- index.html
- tools/render-video.mjs

## Verification Status
- Project generation: passed.
- Caption count: ${cues.length === 136 ? "passed" : "failed"} (${cues.length} screens).
- MP4 render: pending.
- Visual/audio inspection: pending after render.

## Known Environment Notes
- Local workspace path C:\\Users\\MEU CODEX\\PROJECTS\\B. LIVING is read-only for this user; production files were created in C:\\Users\\vini1\\Documents\\Codex\\believe-inauguracao-motion.
- HyperFrames CLI was not available through npm/npx in PATH. The source follows the HyperFrames HTML contract, and final MP4 rendering uses local FFmpeg.
`,
  "utf8",
);

console.log(JSON.stringify({ root, cues: cues.length, duration, outputPath }, null, 2));

if (process.argv.includes("--render")) {
  maybeRender();
}
