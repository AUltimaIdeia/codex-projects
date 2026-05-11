from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import json, math, subprocess, sys, re
import imageio_ffmpeg

ROOT = Path(r"C:\Users\vini1\Documents\Codex\B-LIVING-hyperframes")
OUT = ROOT / "B-LIVING-inauguracao-motion.mp4"
FPS = 24
W, H = 1080, 1920
DURATION = 278

colors = {
    "navy": "#132142",
    "taupe": "#695C50",
    "sand": "#B7AB9E",
    "beige": "#D7CCC0",
    "white": "#F7F4EF",
    "ink": "#3D342C",
}

scenes = [
  dict(id='s1', start=0, end=18, kicker='Inauguração', title='Não é apenas abrir portas.', support='É o início de uma nova fase.', marker='Nascimento', dark=False, align='left'),
  dict(id='s2', start=18, end=58, kicker='Florianópolis', title='Uma cidade de valor raro.', support='Geografia, atratividade, qualidade de vida e força econômica.', marker='Era da integração', dark=True, align='right'),
  dict(id='s3', start=58, end=92, kicker='Believe', title='Entregar mais. Conectar mais.', support='Um time que transforma orientação em prosperidade.', marker='Onda positiva', dark=False, align='left'),
  dict(id='s4', start=92, end=123, kicker='Confiança', title='O momento que se concretizou.', support='Equipe, parceiros e amigos celebrando uma construção real.', marker='Momento único', dark=True, align='center'),
  dict(id='s5', start=123, end=164, kicker='Família', title='Mais do que um time.', support='Uma casa aberta para relacionamento, negócios e cidade.', marker='Portas abertas', dark=False, align='right'),
  dict(id='s6', start=164, end=202, kicker='Mercado', title='Floripa vive uma ascensão.', support='A Believe nasce no momento em que o mercado esperava por ela.', marker='Inovação', dark=True, align='left'),
  dict(id='s7', start=202, end=244, kicker='Consultoria', title='Entender o passado. Interpretar o presente. Projetar o futuro.', support='Experiência somada a um método para decisões melhores.', marker='Curadoria', dark=False, align='center'),
  dict(id='s8', start=244, end=DURATION, kicker='Convite', title='Venha para a Believe Floripa.', support='Atendimento de qualidade, foco no cliente e metodologia própria.', marker='B. LIVING', dark=True, align='right'),
]

font_dir = Path(r"C:\Windows\Fonts")
def font(name, size):
    for candidate in [name, "georgia.ttf", "arial.ttf"]:
        p = font_dir / candidate
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

f_title = font("georgia.ttf", 82)
f_title_small = font("georgia.ttf", 68)
f_brand = font("georgia.ttf", 38)
f_kicker = font("arialbd.ttf", 28)
f_support = font("arial.ttf", 34)
f_marker = font("arialbd.ttf", 24)
f_meta = font("arial.ttf", 18)

kit = Image.open(ROOT / "Kit Visual — B. Living.jpeg").convert("RGB")
kit = kit.resize((W, int(W * kit.height / kit.width)))
if kit.height < H:
    kit = kit.resize((int(H * kit.width / kit.height), H))
left = (kit.width - W) // 2
top = (kit.height - H) // 2
kit = kit.crop((left, top, left + W, top + H)).filter(ImageFilter.GaussianBlur(0.8))

frames_dir = ROOT / "render_assets"
frames_dir.mkdir(exist_ok=True)

# simple deterministic texture
noise = Image.new("RGBA", (W, H), (0,0,0,0))
dn = ImageDraw.Draw(noise)
for y in range(0, H, 11):
    for x in range((y * 7) % 11, W, 11):
        dn.point((x,y), fill=(19,33,66,28))

def wrap(draw, text, font_obj, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0,0), test, font=font_obj)[2] <= max_width or not line:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def draw_text_block(draw, xy, text, font_obj, fill, max_width, line_gap=10, align='left'):
    x, y = xy
    lines = wrap(draw, text, font_obj, max_width)
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font_obj)
        lw = bbox[2] - bbox[0]
        dx = 0 if align == 'left' else (max_width - lw if align == 'right' else (max_width - lw)/2)
        draw.text((x + dx, y), line, font=font_obj, fill=fill)
        y += (bbox[3]-bbox[1]) + line_gap
    return y

for idx, s in enumerate(scenes):
    base = Image.new("RGB", (W,H), colors["navy"] if s['dark'] else colors["white"])
    bg = kit.copy().convert("RGBA")
    overlay = Image.new("RGBA", (W,H), (247,244,239,205) if not s['dark'] else (19,33,66,218))
    bg.alpha_composite(overlay)
    base = Image.alpha_composite(base.convert("RGBA"), bg).convert("RGBA")

    # warm glow
    glow = Image.new("RGBA", (W,H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((650, 170, 1350, 860), fill=(215,204,192,80 if s['dark'] else 55))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    base.alpha_composite(glow)
    base.alpha_composite(noise)

    draw = ImageDraw.Draw(base)
    # Keep the editorial frame clean; captions carry the lower-third region.

    text_main = colors['white'] if s['dark'] else colors['navy']
    text_support = colors['beige'] if s['dark'] else colors['ink']
    text_muted = colors['beige'] if s['dark'] else colors['taupe']

    draw.text((72,68), "B. LIVING", font=f_brand, fill=text_main)
    draw.text((760,76), "FLORIPA · INAUGURAÇÃO", font=f_meta, fill=text_muted)

    maxw = 850
    if s['align'] == 'left': x = 96
    elif s['align'] == 'right': x = W - 96 - maxw
    else: x = (W - maxw)//2
    align = s['align']
    y = 690
    draw_text_block(draw, (x, y), s['kicker'].upper(), f_kicker, text_muted, maxw, 12, align)
    y += 66
    title_font = f_title_small if len(s['title']) > 58 else f_title
    y = draw_text_block(draw, (x, y), s['title'], title_font, text_main, maxw, 16, align)
    y += 34
    if align == 'right': draw.line((x+maxw-620, y, x+maxw, y), fill=text_muted, width=2)
    elif align == 'center': draw.line((x+115, y, x+maxw-115, y), fill=text_muted, width=2)
    else: draw.line((x, y, x+620, y), fill=text_muted, width=2)
    y += 34
    y = draw_text_block(draw, (x, y), s['support'], f_support, text_support, 760 if align != 'center' else maxw, 10, align)
    y += 42
    draw_text_block(draw, (x, y), s['marker'].upper(), f_marker, text_main, maxw, 10, align)

    base.convert("RGB").save(frames_dir / f"scene_{idx+1:02d}.png", quality=95)

# ASS captions
srt_text = (ROOT / "0428.srt").read_text(encoding="utf8")
def ass_time(sec):
    h = int(sec//3600); sec -= h*3600
    m = int(sec//60); sec -= m*60
    s = int(sec); cs = int(round((sec-s)*100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def to_sec(t):
    m = re.match(r"(\d+):(\d+):(\d+),(\d+)", t)
    return int(m[1])*3600 + int(m[2])*60 + int(m[3]) + int(m[4])/1000

events=[]
for block in re.split(r"\r?\n\r?\n", srt_text.strip()):
    lines=block.strip().splitlines()
    if len(lines)>=3:
        mt=re.search(r"(.+?)\s+-->\s+(.+)", lines[1])
        if mt:
            text=' '.join(lines[2:]).replace('{','').replace('}','')
            events.append((to_sec(mt[1]), to_sec(mt[2]), text))
ass = """[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Arial,44,&H00F7F4EF,&H00D7CCC0,&H00132142,&D9132142,0,0,0,0,100,100,0,0,3,1,0,2,110,110,142,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""
for st,en,txt in events:
    ass += f"Dialogue: 0,{ass_time(st)},{ass_time(en)},Default,,0,0,0,,{txt}\n"
(ROOT / "captions.ass").write_text(ass, encoding="utf8")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
inputs=[]
for i,s in enumerate(scenes):
    dur = s['end']-s['start']
    inputs += ['-loop','1','-t',str(dur),'-i',str(frames_dir / f"scene_{i+1:02d}.png")]
inputs += ['-i', str(ROOT / 'audio inauguração.MP3')]

parts=[]
for i,s in enumerate(scenes):
    dur=s['end']-s['start']; frames=max(1, int(round(dur*FPS)))
    direction = 1 if i%2 else -1
    xexpr = "iw/2-(iw/zoom/2)"
    yexpr = "ih/2-(ih/zoom/2)"
    parts.append(f"[{i}:v]scale={W}:{H},zoompan=z='min(zoom+0.00009,1.025)':d={frames}:x='{xexpr}':y='{yexpr}':s={W}x{H}:fps={FPS},setsar=1[v{i}]")
concat_inputs=''.join(f"[v{i}]" for i in range(len(scenes)))
ass_path = str(ROOT / 'captions.ass').replace('\\','/').replace(':','\\:')
parts.append(f"{concat_inputs}concat=n={len(scenes)}:v=1:a=0[vcat]")
parts.append(f"[vcat]subtitles='{ass_path}'[vout]")
filter_complex=';'.join(parts)
cmd=[ffmpeg, '-y', *inputs, '-filter_complex', filter_complex, '-map', '[vout]', '-map', f'{len(scenes)}:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(OUT)]
print('RUNNING_FFMPEG')
print(' '.join(cmd[:8]), '...')
subprocess.run(cmd, check=True, cwd=str(ROOT))
print(f"OUTPUT={OUT}")
print(f"SIZE={OUT.stat().st_size}")


