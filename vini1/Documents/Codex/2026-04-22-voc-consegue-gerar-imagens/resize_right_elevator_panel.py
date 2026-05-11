from pathlib import Path
from PIL import Image, ImageFilter


SRC = Path(r"C:\Users\vini1\.codex\generated_images\019dbc47-60f4-75e1-a08e-040c6de786e8\ig_0142c7c14683d0bc0169f116421f048197894d0f927ec96c2b.png")
OUT_DIR = Path(r"C:\Users\vini1\Documents\Codex\2026-04-22-voc-consegue-gerar-imagens\elevador_lateral_direita_56x234")

WIDTH_CM = 56
HEIGHT_CM = 234
DPI = 300


def cm_to_px(cm: float) -> int:
    return round(cm / 2.54 * DPI)


def cover_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    dst_ratio = target_w / target_h

    if src_ratio > dst_ratio:
        new_w = round(src_h * dst_ratio)
        # Keep slightly more of the right side for the right-panel composition.
        left = max(0, min(src_w - new_w, round((src_w - new_w) * 0.58)))
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = round(src_w / dst_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    target_w = cm_to_px(WIDTH_CM)
    target_h = cm_to_px(HEIGHT_CM)

    img = Image.open(SRC).convert("RGB")
    final = cover_crop(img, target_w, target_h)
    final = final.filter(ImageFilter.UnsharpMask(radius=1.1, percent=90, threshold=2))

    png = OUT_DIR / "lateral_direita_zeiss_56x234cm_300dpi.png"
    jpg = OUT_DIR / "lateral_direita_zeiss_56x234cm_300dpi.jpg"
    preview = OUT_DIR / "preview_lateral_direita_56x234cm.jpg"

    final.save(png, dpi=(DPI, DPI))
    final.save(jpg, "JPEG", quality=96, subsampling=0, dpi=(DPI, DPI))

    small = final.copy()
    small.thumbnail((900, 1700))
    small.save(preview, "JPEG", quality=90)

    print(f"{target_w}x{target_h}")
    print(png)
    print(jpg)
    print(preview)


if __name__ == "__main__":
    main()
