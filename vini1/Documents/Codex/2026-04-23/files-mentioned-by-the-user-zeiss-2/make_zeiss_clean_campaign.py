from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


INPUT = Path(r"C:\Users\vini1\Downloads\ZEISS ClearMind Lenses Sales Folder _V2.pdf.png")
OUT_DIR = Path(r"C:\Users\vini1\Documents\Codex\2026-04-23\files-mentioned-by-the-user-zeiss-2")
DPI = 150


def cm_to_px(value_cm: float, dpi: int = DPI) -> int:
    return round(value_cm / 2.54 * dpi)


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def remove_horizontal_export_line(image: Image.Image) -> Image.Image:
    arr = np.array(image).astype(np.float32)
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    diff = np.mean(np.abs(np.diff(lum, axis=0)), axis=1)

    search_start = int(image.height * 0.45)
    search_end = int(image.height * 0.62)
    seam_y = int(np.argmax(diff[search_start:search_end]) + search_start)

    top = max(2, seam_y - 2)
    bottom = min(image.height - 3, seam_y + 6)
    before = arr[top - 2].copy()
    after = arr[bottom + 2].copy()
    span = bottom - top + 1

    for i, y in enumerate(range(top, bottom + 1), start=1):
        t = i / (span + 1)
        arr[y] = before * (1 - t) + after * t

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def fill_rect_from_edges(image: Image.Image, box, feather=42) -> Image.Image:
    """Remove simple sky-area marks by rebuilding the rectangle from its edge colors."""
    x0, y0, x1, y1 = box
    image = image.convert("RGB")
    arr = np.array(image).astype(np.float32)
    h = y1 - y0
    w = x1 - x0
    pad = 18

    left = arr[y0:y1, max(0, x0 - pad) : x0].mean(axis=1) if x0 - pad >= 0 else arr[y0:y1, x1 : x1 + pad].mean(axis=1)
    right = arr[y0:y1, x1 : min(arr.shape[1], x1 + pad)].mean(axis=1) if x1 + pad <= arr.shape[1] else arr[y0:y1, x0 - pad : x0].mean(axis=1)
    top = arr[max(0, y0 - pad) : y0, x0:x1].mean(axis=0) if y0 - pad >= 0 else arr[y1 : y1 + pad, x0:x1].mean(axis=0)
    bottom = arr[y1 : min(arr.shape[0], y1 + pad), x0:x1].mean(axis=0) if y1 + pad <= arr.shape[0] else arr[y0 - pad : y0, x0:x1].mean(axis=0)

    xx = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    horizontal = left[:, None, :] * (1 - xx) + right[:, None, :] * xx
    vertical = top[None, :, :] * (1 - yy) + bottom[None, :, :] * yy
    patch = np.clip((horizontal + vertical) * 0.5, 0, 255).astype(np.uint8)
    patch_img = Image.fromarray(patch, "RGB").filter(ImageFilter.GaussianBlur(10))

    mask = Image.new("L", image.size, 0)
    mask_crop = Image.new("L", (w, h), 255)
    mask_crop = mask_crop.filter(ImageFilter.GaussianBlur(feather))
    mask.paste(mask_crop, (x0, y0))
    replacement = image.copy()
    replacement.paste(patch_img, (x0, y0))
    return Image.composite(replacement, image, mask)


def clean_source(image: Image.Image) -> Image.Image:
    image = remove_horizontal_export_line(image)
    # Original campaign marks in the sky. These boxes are deliberately oversized
    # so no text or logo fragments survive after resizing and cropping.
    image = fill_rect_from_edges(image, (210, 255, 1320, 575))
    image = fill_rect_from_edges(image, (5350, 230, 6035, 805))
    return image


def build_background(src: Image.Image, target_w: int, target_h: int) -> Image.Image:
    arr = np.array(src).astype(np.float32)
    sky_samples = np.concatenate(
        [
            arr[120:560, 760:2100].reshape(-1, 3),
            arr[120:560, 4200:5350].reshape(-1, 3),
        ],
        axis=0,
    )
    mid_samples = np.concatenate(
        [
            arr[850:1450, 400:1450].reshape(-1, 3),
            arr[850:1450, 4550:6100].reshape(-1, 3),
        ],
        axis=0,
    )
    top_color = sky_samples.mean(axis=0)
    mid_color = mid_samples.mean(axis=0)
    navy = np.array([3, 18, 44], dtype=np.float32)

    y = np.linspace(0, 1, target_h, dtype=np.float32)[:, None]
    sky_t = smoothstep(y / 0.48)
    sky = top_color * (1 - sky_t) + mid_color * sky_t
    dark_t = smoothstep((y - 0.50) / 0.50)
    gradient = sky * (1 - dark_t) + navy * dark_t
    bg = np.repeat(gradient[:, None, :], target_w, axis=1)

    return Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB")


def paste_campaign_photo(canvas: Image.Image, src: Image.Image) -> Image.Image:
    target_w, target_h = canvas.size
    scale = 0.75
    paste_y = round(target_h * 0.165)
    subject_center_x = src.width * 0.515

    resized = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
    crop_x = round(subject_center_x * scale - target_w / 2)
    crop_x = max(0, min(crop_x, resized.width - target_w))
    visible = resized.crop((crop_x, 0, crop_x + target_w, resized.height))

    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.alpha_composite(visible.convert("RGBA"), (0, paste_y))

    # Blend the rectangular source into the built poster: sky fades at the top
    # while hair/skin remain solid, and the lower edge dissolves into the base.
    alpha = Image.new("L", visible.size, 255)
    alpha_arr = np.array(alpha, dtype=np.float32)
    visible_arr = np.array(visible.convert("RGB")).astype(np.float32)
    r = visible_arr[:, :, 0]
    g = visible_arr[:, :, 1]
    b = visible_arr[:, :, 2]
    sky_like = (b > 118) & (b > r + 16) & (g > r - 22)

    y = np.arange(visible.height, dtype=np.float32)
    top_len = max(1, round(visible.height * 0.13))
    top_fade = smoothstep(y / top_len)[:, None]
    alpha_arr = np.where(sky_like, alpha_arr * top_fade, alpha_arr)

    fade_start = round(visible.height * 0.92)
    bottom_fade = smoothstep((y - fade_start) / (visible.height - fade_start))[:, None]
    alpha_arr = alpha_arr * (1 - bottom_fade)
    alpha = Image.fromarray(np.clip(alpha_arr, 0, 255).astype(np.uint8), "L")
    visible_rgba = visible.convert("RGBA")
    visible_rgba.putalpha(alpha)

    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.alpha_composite(visible_rgba, (0, paste_y))
    return Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")


def add_campaign_shading(image: Image.Image) -> Image.Image:
    arr = np.array(image).astype(np.float32)
    h, w = arr.shape[:2]
    navy = np.array([2, 15, 39], dtype=np.float32)

    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    bottom_alpha = smoothstep((yy - 0.50) / 0.28) ** 1.04
    bottom_alpha = np.clip(bottom_alpha * 0.44, 0, 0.44)
    arr = arr * (1 - bottom_alpha[:, :, None]) + navy * bottom_alpha[:, :, None]

    xx = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
    side_alpha = smoothstep((np.abs(xx) - 0.70) / 0.30) * 0.11
    side_alpha = np.repeat(side_alpha, h, axis=0)
    arr = arr * (1 - side_alpha[:, :, None]) + navy * side_alpha[:, :, None]

    # Subtle blue lift through the middle like the reference poster.
    highlight_y = round(h * 0.68)
    highlight = np.exp(-((np.arange(h) - highlight_y) ** 2) / (2 * (h * 0.015) ** 2))[:, None]
    highlight = highlight * np.exp(-(xx**2) / (2 * 0.55**2))
    blue = np.array([35, 92, 155], dtype=np.float32)
    arr = arr * (1 - highlight[:, :, None] * 0.025) + blue * (highlight[:, :, None] * 0.025)

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def finish(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.UnsharpMask(radius=0.9, percent=55, threshold=2))


def save_outputs(image: Image.Image, stem: str):
    png = OUT_DIR / f"{stem}.png"
    jpg = OUT_DIR / f"{stem}.jpg"
    pdf = OUT_DIR / f"{stem}.pdf"
    preview = OUT_DIR / f"{stem}-preview.jpg"

    image.save(png, dpi=(DPI, DPI), optimize=True)
    image.save(jpg, quality=95, subsampling=0, dpi=(DPI, DPI), optimize=True)
    image.save(pdf, "PDF", resolution=DPI, quality=95, subsampling=0)

    preview_w = 1200
    preview_h = round(preview_w * image.height / image.width)
    image.resize((preview_w, preview_h), Image.Resampling.LANCZOS).save(preview, quality=90, optimize=True)
    return png, jpg, pdf, preview


def main():
    target_w = cm_to_px(65.5)
    target_h = cm_to_px(117)
    src = Image.open(INPUT).convert("RGB")
    src = clean_source(src)

    canvas = build_background(src, target_w, target_h)
    composed = paste_campaign_photo(canvas, src)
    composed = add_campaign_shading(composed)
    composed = finish(composed)

    paths = save_outputs(composed, "zeiss-clearmind-clean-campaign-v3-centered-small-65_5x117cm-150dpi")
    print("created:")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
