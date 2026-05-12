from pathlib import Path
import sys
import math

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".video_deps"))

import imageio.v3 as iio
import numpy as np
from PIL import Image, ImageFilter, ImageChops


INPUT = Path(r"C:\Users\vini1\Downloads\IMG_5684.PNG")
OUT_DIR = ROOT / "output"
OUTPUT = OUT_DIR / "ultima-ideia-cinematic-5s.mp4"
FPS = 24
DURATION = 5
FRAMES = FPS * DURATION


def smoothstep(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def make_vignette(size):
    w, h = size
    y, x = np.mgrid[0:h, 0:w]
    nx = (x - w * 0.52) / (w * 0.62)
    ny = (y - h * 0.46) / (h * 0.70)
    d = np.sqrt(nx * nx + ny * ny)
    v = 1.0 - np.clip((d - 0.45) / 0.65, 0, 1) * 0.30
    return v[..., None]


def crop_zoom(img: Image.Image, scale: float, center):
    w, h = img.size
    cw = int(round(w / scale))
    ch = int(round(h / scale))
    cx, cy = center
    left = int(round(cx - cw / 2))
    top = int(round(cy - ch / 2))
    left = max(0, min(w - cw, left))
    top = max(0, min(h - ch, top))
    return img.crop((left, top, left + cw, top + ch)).resize((w, h), Image.Resampling.LANCZOS)


def paste_region_shift(base, src, box, dx, dy, blur=9, opacity=0.45):
    x1, y1, x2, y2 = box
    region = src.crop(box)
    shifted = Image.new("RGB", src.size, (0, 0, 0))
    shifted.paste(region, (int(x1 + dx), int(y1 + dy)))
    mask = Image.new("L", src.size, 0)
    m = Image.new("L", (x2 - x1, y2 - y1), int(255 * opacity))
    m = m.filter(ImageFilter.GaussianBlur(blur))
    mask.paste(m, (x1, y1))
    return Image.composite(shifted, base, mask)


def make_glow_layer(img):
    # Central poster hand symbol: select bright editorial linework, not the text.
    w, h = img.size
    arr = np.asarray(img.convert("L")).astype(np.float32)
    mask = np.zeros((h, w), dtype=np.float32)
    x1, y1, x2, y2 = 342, 455, 520, 680
    roi = arr[y1:y2, x1:x2]
    selected = np.clip((roi - 135) / 80, 0, 1)
    yy, xx = np.mgrid[0 : y2 - y1, 0 : x2 - x1]
    oval = (((xx - 82) / 92) ** 2 + ((yy - 102) / 125) ** 2) < 1.0
    selected *= oval.astype(np.float32)
    mask[y1:y2, x1:x2] = selected
    mask_img = Image.fromarray(np.uint8(mask * 255), "L").filter(ImageFilter.GaussianBlur(8))
    glow = Image.new("RGB", img.size, (232, 232, 220))
    return glow, mask_img


def apply_light_shift(img, t):
    w, h = img.size
    arr = np.asarray(img).astype(np.float32)
    y, x = np.mgrid[0:h, 0:w]
    # Diagonal sunlight boundary, drifting almost imperceptibly across five seconds.
    boundary = 328 + 0.405 * x + 18 * (t - 0.5)
    band = np.clip((boundary - y) / 145, 0, 1)
    natural = 1.0 + 0.045 * band - 0.025 * (1 - band)
    arr *= natural[..., None]
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")


def preserve_red_note(original, frame):
    arr = np.asarray(original.convert("RGB"))
    red = (arr[..., 0] > 110) & (arr[..., 1] < 80) & (arr[..., 2] < 80)
    red = Image.fromarray(np.uint8(red) * 255, "L").filter(ImageFilter.GaussianBlur(0.7))
    return Image.composite(original.convert("RGB"), frame, red)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    original = Image.open(INPUT).convert("RGB")
    w, h = original.size
    vignette = make_vignette((w, h))
    glow_layer, glow_mask = make_glow_layer(original)

    frames = []
    for i in range(FRAMES):
        p = i / (FRAMES - 1)
        s = smoothstep(p)
        # Dolly toward the poster while keeping the silhouetted man in frame.
        scale = 1.0 + 0.038 * s
        center = (w * (0.515 - 0.018 * s), h * (0.505 - 0.006 * s))
        frame = crop_zoom(original, scale, center)

        breeze = math.sin(p * math.tau * 1.25) * 1.2
        frame = paste_region_shift(frame, frame, (315, 915, 785, 1075), breeze, -0.35, blur=12, opacity=0.18)
        frame = paste_region_shift(frame, frame, (200, 840, 355, 1015), -breeze * 0.45, 0.25, blur=13, opacity=0.12)
        frame = paste_region_shift(frame, frame, (210, 705, 315, 980), math.sin(p * math.tau) * 0.75, 0, blur=18, opacity=0.10)

        frame = apply_light_shift(frame, p)

        pulse = 0.10 + 0.055 * math.sin((p * math.tau * 1.15) - 0.45)
        soft_mask = glow_mask.point(lambda v: int(v * max(0, pulse)))
        frame = Image.composite(glow_layer, frame, soft_mask)

        frame = preserve_red_note(original, frame)

        arr = np.asarray(frame).astype(np.float32)
        arr *= vignette
        # Fine monochrome film grain, restrained and stable enough to avoid artifacts.
        rng = np.random.default_rng(1200 + i)
        grain = rng.normal(0, 2.2, arr.shape[:2])[..., None]
        arr = arr + grain
        frame = Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")
        frames.append(np.asarray(frame))

    iio.imwrite(
        OUTPUT,
        np.stack(frames),
        fps=FPS,
        codec="libx264",
        quality=9,
        pixelformat="yuv420p",
        macro_block_size=1,
    )
    print(str(OUTPUT))


if __name__ == "__main__":
    main()
