from pathlib import Path
from PIL import Image, ImageCms, ImageFilter


SRC = Path(r"C:\Users\vini1\.codex\generated_images\019db59c-7a64-7d83-8c93-f7b7cdb369fa\ig_0142c7c14683d0bc0169ea81e472d881978604327c0607dd8a.png")
OUT_DIR = Path(r"C:\Users\vini1\Documents\Codex\2026-04-22-voc-consegue-gerar-imagens\elevador_signature_print")
SRGB_PROFILE = Path(r"C:\Windows\System32\spool\drivers\color\sRGB Color Space Profile.icm")
CMYK_PROFILE = Path(r"C:\Windows\System32\spool\drivers\color\RSWOP.icm")

# Frontal: 1.31m x 2.34m
WIDTH_MM = 1310
HEIGHT_MM = 2340

# For large-format printing, 150 dpi is a strong practical target with manageable file size.
DPI = 150
MM_PER_INCH = 25.4


def mm_to_px(mm: float, dpi: int) -> int:
    return round(mm / MM_PER_INCH * dpi)


def main():
    OUT_DIR.mkdir(exist_ok=True)

    width_px = mm_to_px(WIDTH_MM, DPI)
    height_px = mm_to_px(HEIGHT_MM, DPI)

    img = Image.open(SRC).convert("RGB")
    img = img.resize((width_px, height_px), Image.Resampling.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=105, threshold=2))

    img = ImageCms.profileToProfile(
        img,
        str(SRGB_PROFILE),
        str(CMYK_PROFILE),
        outputMode="CMYK",
    )

    jpg_path = OUT_DIR / "zeiss_signature_elevador_frontal_cmyk_150dpi.jpg"
    pdf_path = OUT_DIR / "zeiss_signature_elevador_frontal_cmyk_150dpi.pdf"

    img.save(jpg_path, "JPEG", quality=95, subsampling=0, dpi=(DPI, DPI))
    img.save(pdf_path, "PDF", resolution=DPI)

    print(jpg_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
