from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


INPUT = Path(r"C:\Users\vini1\Downloads\ZEISS ClearMind Lenses Sales Folder _V2.pdf.png")
OUT_DIR = Path(r"C:\Users\vini1\Documents\Codex\2026-04-23\files-mentioned-by-the-user-zeiss-2")
DPI = 150


def cm_to_px(value_cm: float, dpi: int = DPI) -> int:
    return round(value_cm / 2.54 * dpi)


def remove_horizontal_export_line(image: Image.Image) -> Image.Image:
    """Blend out the full-width PDF export seam visible across the original art."""
    arr = np.array(image).astype(np.float32)
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    diff = np.mean(np.abs(np.diff(lum, axis=0)), axis=1)

    search_start = int(image.height * 0.45)
    search_end = int(image.height * 0.62)
    seam_y = int(np.argmax(diff[search_start:search_end]) + search_start)

    top = max(0, seam_y - 2)
    bottom = min(image.height - 1, seam_y + 6)
    before = arr[top - 2].copy()
    after = arr[bottom + 2].copy()
    span = bottom - top + 1

    for i, y in enumerate(range(top, bottom + 1), start=1):
        t = i / (span + 1)
        arr[y] = before * (1 - t) + after * t

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def finish(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=2))


def save_set(image: Image.Image, stem: str):
    png = OUT_DIR / f"{stem}.png"
    jpg = OUT_DIR / f"{stem}.jpg"
    pdf = OUT_DIR / f"{stem}.pdf"

    image.save(png, dpi=(DPI, DPI), optimize=True)
    image.save(jpg, quality=95, subsampling=0, dpi=(DPI, DPI), optimize=True)
    image.save(pdf, "PDF", resolution=DPI, quality=95, subsampling=0)
    return png, jpg, pdf


def landscape_layout(src: Image.Image) -> Image.Image:
    target_w = cm_to_px(117)
    target_h = cm_to_px(65.5)
    target_aspect = target_w / target_h
    crop_h = round(src.width / target_aspect)

    # Keep the brand marks and sky at the top; crop excess from the lower body.
    crop = src.crop((0, 0, src.width, crop_h))
    return finish(crop.resize((target_w, target_h), Image.Resampling.LANCZOS))


def find_logo(src: Image.Image) -> Image.Image:
    arr = np.array(src.convert("RGB"))
    roi = arr[: int(src.height * 0.25), int(src.width * 0.72) :, :]
    blue_mask = (roi[:, :, 2] > 95) & (roi[:, :, 1] < 120) & (roi[:, :, 0] < 55)
    ys, xs = np.where(blue_mask)
    if len(xs) == 0:
        raise RuntimeError("Could not locate ZEISS logo.")

    x0 = max(0, int(xs.min()) - 8)
    x1 = min(roi.shape[1] - 1, int(xs.max()) + 8)
    y0 = max(0, int(ys.min()) - 8)
    y1 = min(roi.shape[0] - 1, int(ys.max()) + 8)

    crop = src.crop((int(src.width * 0.72) + x0, y0, int(src.width * 0.72) + x1 + 1, y1 + 1)).convert("RGBA")
    crop_arr = np.array(crop.convert("RGB"))
    shape_blue = (crop_arr[:, :, 2] > 95) & (crop_arr[:, :, 1] < 130) & (crop_arr[:, :, 0] < 70)

    alpha = np.zeros(shape_blue.shape, dtype=np.uint8)
    for y in range(shape_blue.shape[0]):
        cols = np.where(shape_blue[y])[0]
        if len(cols) > 4:
            alpha[y, int(cols.min()) : int(cols.max()) + 1] = 255

    alpha = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(0.35))
    crop.putalpha(alpha)
    return crop


def load_font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.truetype("arial.ttf", size=size)


def draw_slogan(canvas: Image.Image, x: int, y: int):
    draw = ImageDraw.Draw(canvas)
    light = load_font(
        [
            r"C:\Windows\Fonts\segoeuil.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ],
        132,
    )
    bold = load_font(
        [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ],
        132,
    )
    fill = (255, 255, 255, 240)
    draw.text((x, y), "Seeing ", font=light, fill=fill)
    offset = round(draw.textlength("Seeing ", font=light))
    draw.text((x + offset, y), "beyond", font=bold, fill=fill)


def vertical_layout(src: Image.Image) -> Image.Image:
    target_w = cm_to_px(65.5)
    target_h = cm_to_px(117)

    scale = target_h / src.height
    resized = src.resize((round(src.width * scale), target_h), Image.Resampling.LANCZOS)

    subject_center_x = round(src.width * 0.515 * scale)
    crop_x = min(max(0, subject_center_x - target_w // 2), resized.width - target_w)
    canvas = resized.crop((crop_x, 0, crop_x + target_w, target_h)).convert("RGBA")

    # Gentle top lift for readable white text without changing the campaign look.
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gradient = Image.new("L", (1, target_h), 0)
    g = np.zeros((target_h, 1), dtype=np.uint8)
    fade_h = round(target_h * 0.18)
    for y in range(fade_h):
        g[y, 0] = round(50 * (1 - y / fade_h))
    gradient = Image.fromarray(g, "L").resize(canvas.size)
    overlay.putalpha(gradient)
    canvas = Image.alpha_composite(canvas, overlay)

    margin = cm_to_px(3.4)
    draw_slogan(canvas, margin, cm_to_px(3.3))

    logo = find_logo(src)
    target_logo_w = cm_to_px(8.8)
    logo = logo.resize((target_logo_w, round(target_logo_w * logo.height / logo.width)), Image.Resampling.LANCZOS)
    canvas.alpha_composite(logo, (target_w - margin - logo.width, cm_to_px(3.0)))

    return finish(canvas.convert("RGB"))


def make_previews(images):
    for path in images:
        im = Image.open(path)
        preview_w = 1400
        preview_h = round(preview_w * im.height / im.width)
        preview = im.resize((preview_w, preview_h), Image.Resampling.LANCZOS)
        preview.save(path.with_name(f"{path.stem}-preview.jpg"), quality=88, optimize=True)


def main():
    src = Image.open(INPUT).convert("RGB")
    cleaned = remove_horizontal_export_line(src)

    landscape = landscape_layout(cleaned)
    vertical = vertical_layout(cleaned)

    landscape_paths = save_set(landscape, "zeiss-clearmind-117x65_5cm-150dpi")
    vertical_paths = save_set(vertical, "zeiss-clearmind-65_5x117cm-150dpi")
    make_previews([landscape_paths[0], vertical_paths[0]])

    print("created:")
    for path in (*landscape_paths, *vertical_paths):
        print(path)


if __name__ == "__main__":
    main()
