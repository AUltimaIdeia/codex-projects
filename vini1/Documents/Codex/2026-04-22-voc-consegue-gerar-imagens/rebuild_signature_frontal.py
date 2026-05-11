from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageCms


SRC = Path(r"C:\Users\vini1\Downloads\ZEISS ClearMind Lenses Sales Folder _V2.pdf.png")
OUT_DIR = Path(r"C:\Users\vini1\Documents\Codex\2026-04-22-voc-consegue-gerar-imagens\elevador_signature_fixed")
SRGB_PROFILE = Path(r"C:\Windows\System32\spool\drivers\color\sRGB Color Space Profile.icm")
CMYK_PROFILE = Path(r"C:\Windows\System32\spool\drivers\color\RSWOP.icm")

WIDTH_MM = 1310
HEIGHT_MM = 2340
DPI = 150
MM_PER_INCH = 25.4


def mm_to_px(mm: float, dpi: int) -> int:
    return round(mm / MM_PER_INCH * dpi)


def load_font(size: int, bold: bool = False, serif: bool = False):
    candidates = []
    if serif:
        candidates = [
            r"C:\Windows\Fonts\BOD_R.TTF",
            r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
            r"C:\Windows\Fonts\timesbd.ttf" if bold else r"C:\Windows\Fonts\times.ttf",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        ]
    for c in candidates:
        p = Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def draw_text(draw, text, box, font, fill, line_gap=1.15, align="left"):
    left, top, width, height = box
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textlength(test, font=font) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    bbox = draw.textbbox((0, 0), "Ag", font=font)
    lh = int((bbox[3] - bbox[1]) * line_gap)
    y = top
    for line in lines:
        if y + lh > top + height:
            break
        line_bbox = draw.textbbox((0, 0), line, font=font)
        lw = line_bbox[2] - line_bbox[0]
        x = left
        if align == "center":
            x = left + (width - lw) / 2
        elif align == "right":
            x = left + width - lw
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def build_front():
    target_w = mm_to_px(WIDTH_MM, DPI)
    target_h = mm_to_px(HEIGHT_MM, DPI)
    img = Image.open(SRC).convert("RGB")

    # Preserve aspect ratio: scale to full height and crop overflow from the left, keeping the talent intact.
    scaled_w = round(img.width * target_h / img.height)
    hero = img.resize((scaled_w, target_h), Image.Resampling.LANCZOS)
    x = max(0, scaled_w - target_w)
    hero = hero.crop((x, 0, x + target_w, target_h))

    # Left-to-right premium dark overlay for legibility.
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    panel_w = int(target_w * 0.53)
    for i in range(panel_w):
        alpha = int(220 - (i / panel_w) * 170)
        od.line((i, 0, i, target_h), fill=(8, 16, 42, alpha), width=1)
    for j in range(target_h):
        alpha = int(36 + (j / target_h) * 58)
        od.line((0, j, target_w, j), fill=(4, 9, 26, alpha), width=1)

    # Soft vignette on bottom.
    for j in range(int(target_h * 0.28)):
        alpha = int((j / (target_h * 0.28)) * 120)
        y = target_h - int(target_h * 0.28) + j
        od.line((0, y, target_w, y), fill=(0, 0, 0, alpha), width=1)

    base = hero.convert("RGBA")
    base.alpha_composite(overlay)
    canvas = base.convert("RGB")
    draw = ImageDraw.Draw(canvas)

    # Logo block
    logo_w = int(target_w * 0.16)
    logo_h = int(logo_w * 1.18)
    logo_x = target_w - logo_w - int(target_w * 0.055)
    logo_y = int(target_h * 0.06)
    draw.rectangle((logo_x, logo_y, logo_x + logo_w, logo_y + logo_h), fill="#0050A4")
    logo_font = load_font(int(logo_w * 0.28), bold=True, serif=True)
    draw.text((logo_x + logo_w * 0.12, logo_y + logo_h * 0.18), "ZEISS", font=logo_font, fill="white")

    white = "#FFFFFF"
    blue = "#4DB3FF"
    gold = "#D8B36A"

    left = int(target_w * 0.08)
    maxw = int(target_w * 0.42)

    draw_text(draw, "ZEISS", (left, int(target_h * 0.13), maxw, 180), load_font(int(target_h * 0.05), bold=False, serif=True), white)
    draw_text(draw, "SIGNATURE", (left, int(target_h * 0.18), maxw, 130), load_font(int(target_h * 0.023), bold=False), white)
    draw.line((left, int(target_h * 0.235), left + maxw * 0.62, int(target_h * 0.235)), fill=(255, 255, 255, 150), width=2)
    draw_text(draw, "EXCLUSIVIDADE ZEISS VISION CENTER", (left, int(target_h * 0.255), maxw, 220), load_font(int(target_h * 0.022), bold=True), white)

    draw_text(draw, "COMPRE 01 PAR DE LENTES", (left, int(target_h * 0.61), maxw, 160), load_font(int(target_h * 0.027), bold=True), white)
    draw_text(draw, "INDIVIDUAL E", (left, int(target_h * 0.665), maxw, 180), load_font(int(target_h * 0.042), bold=False), white)

    # emphasis lines
    line_y = int(target_h * 0.703)
    draw.line((left, line_y, left + int(maxw * 0.08), line_y), fill=gold, width=5)
    draw.line((left + int(maxw * 0.46), line_y, left + int(maxw * 0.58), line_y), fill=gold, width=5)

    draw_text(draw, "LEVE", (left, int(target_h * 0.71), int(maxw * 0.6), 430), load_font(int(target_h * 0.09), bold=True), white)
    draw_text(draw, "03", (left + int(maxw * 0.58), int(target_h * 0.71), int(maxw * 0.42), 430), load_font(int(target_h * 0.09), bold=True), white, align="left")
    flare_y = int(target_h * 0.825)
    draw.line((left, flare_y, left + int(maxw * 0.92), flare_y), fill=blue, width=8)
    draw.ellipse((left + int(maxw * 0.35) - 18, flare_y - 18, left + int(maxw * 0.35) + 18, flare_y + 18), fill="#9DE5FF")

    # footer tags
    footer_y = int(target_h * 0.91)
    footer_font = load_font(int(target_h * 0.018), bold=False)
    items = ["TECNOLOGIA ALEMÃ", "PRECISÃO E PROTEÇÃO", "QUALIDADE ZEISS"]
    col_w = int(maxw / 3)
    for i, item in enumerate(items):
        box_left = left + i * col_w
        draw_text(draw, item, (box_left, footer_y, col_w - 24, 120), footer_font, white)
        if i < 2:
            draw.line((box_left + col_w - 18, footer_y + 6, box_left + col_w - 18, footer_y + 78), fill=(255, 255, 255, 140), width=2)

    rgb_jpg = OUT_DIR / "zeiss_signature_elevador_frontal_rgb_150dpi.jpg"
    rgb_pdf = OUT_DIR / "zeiss_signature_elevador_frontal_rgb_150dpi.pdf"
    cmyk_jpg = OUT_DIR / "zeiss_signature_elevador_frontal_cmyk_150dpi_v2.jpg"
    cmyk_pdf = OUT_DIR / "zeiss_signature_elevador_frontal_cmyk_150dpi_v2.pdf"

    OUT_DIR.mkdir(exist_ok=True)
    canvas.save(rgb_jpg, "JPEG", quality=97, subsampling=0, dpi=(DPI, DPI))
    canvas.save(rgb_pdf, "PDF", resolution=DPI)

    cmyk = ImageCms.profileToProfile(
        canvas,
        str(SRGB_PROFILE),
        str(CMYK_PROFILE),
        outputMode="CMYK",
        renderingIntent=ImageCms.Intent.PERCEPTUAL,
    )
    cmyk.save(cmyk_jpg, "JPEG", quality=95, subsampling=0, dpi=(DPI, DPI))
    cmyk.save(cmyk_pdf, "PDF", resolution=DPI)

    print(rgb_jpg)
    print(rgb_pdf)
    print(cmyk_jpg)
    print(cmyk_pdf)


if __name__ == "__main__":
    build_front()
