import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), "..");
const ffmpeg = "C:\\Users\\vini1\\AppData\\Local\\CapCut\\Apps\\8.3.0.3497\\ffmpeg.exe";
const duration = 276.000;

function filterPath(filePath) {
  return filePath.replace(/\\/g, "/").replace(/^([A-Za-z]):/, "$1\\:");
}

const sourceVideo = path.join(root, "assets", "source-video.mp4");
const kit = path.join(root, "assets", "kit-visual-b-living.jpeg");
const audio = path.join(root, "assets", "audio-inauguracao.mp3");
const ass = path.join(root, "data", "captions.ass");
const output = path.join(root, "renders", "believe-inauguracao-motion.mp4");
const georgia = "C:/Windows/Fonts/georgia.ttf";

const subtitle = filterPath(ass).replace(/'/g, "\\'");
const filters = [
  "[0:v]scale=1920:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:1,eq=brightness=-0.20:contrast=1.08:saturation=0.58,setsar=1[bg]",
  "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=rgba,colorchannelmixer=aa=0.16[kit]",
  "[0:v]scale=920:920:force_original_aspect_ratio=increase,crop=920:920,setsar=1,drawbox=x=0:y=0:w=iw:h=ih:color=0xF7F3EC@0.78:t=4[clip]",
  "[bg][kit]overlay=0:0[base1]",
  "[base1][clip]overlay=80:326[base2]",
  "[base2]drawbox=x=70:y=1314:w=940:h=372:color=0x101C3D@0.74:t=fill,drawbox=x=70:y=1314:w=940:h=372:color=0xCBBBAA@0.42:t=2,drawbox=x=250:y=273:w=580:h=1:color=0xCBBBAA@0.72:t=fill[panel]",
  "[panel]drawtext=fontfile='C\\:/Windows/Fonts/georgia.ttf':text='B. LIVING':fontcolor=0xF7F3EC:fontsize=76:x=(w-text_w)/2:y=116:shadowcolor=0x101C3D@0.55:shadowx=0:shadowy=2,drawtext=fontfile='C\\:/Windows/Fonts/georgia.ttf':text='INAUGURAÇÃO FLORIPA':fontcolor=0xCBBBAA:fontsize=28:x=(w-text_w)/2:y=218:shadowcolor=0x101C3D@0.45:shadowx=0:shadowy=1[subbase]",
  "[subbase]subtitles=filename='" + subtitle + "':fontsdir='C\\:/Windows/Fonts'[v]"
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
