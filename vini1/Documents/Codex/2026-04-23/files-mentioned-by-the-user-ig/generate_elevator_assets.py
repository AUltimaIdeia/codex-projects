from PIL import Image, ImageDraw, ImageFilter
import numpy as np


SOURCE = "reference_layout.png"

# Source crop boxes after removing white separator bars and outside borders.
# Coordinates are (left, top, right, bottom), with right/bottom exclusive.
PANEL_CROPS = {
    "left": (3, 0, 194, 895),
    "front": (211, 0, 1187, 895),
    "right": (1204, 0, 1395, 895),
}

# 50% scale dimensions, using 5 px/mm.
# These preserve the exact requested ratios:
# front 3275:5850 == 655:1170, lateral 1400:5850 == 280:1170.
TARGET_SIZES = {
    "front": (3275, 5850),
    "left": (1400, 5850),
    "right": (1400, 5850),
}

DPI = 127.0
BACKGROUND_MASK_DILATION = {
    "left": 7,
    "front": 9,
    "right": 9,
}


# Source-panel-relative boxes for graphic extraction. Modes:
# full  - keep the whole rectangle, used for ZEISS logo blue blocks.
# white - keep white/silver typography and linework.
# fg    - keep white/silver plus gold/copper linework.
# blue  - keep electric-blue glow/flare accents.
OVERLAY_BOXES = {
    "left": [
        ((65, 40, 125, 98), "full"),
        ((40, 96, 150, 125), "white"),
        ((18, 180, 175, 352), "white"),
        ((0, 385, 191, 410), "fg"),
        ((54, 432, 136, 511), "white"),
        ((20, 528, 176, 674), "white"),
        ((0, 780, 191, 815), "white"),
        ((20, 822, 174, 868), "white"),
    ],
    "front": [
        ((30, 45, 170, 75), "white"),
        ((862, 38, 923, 99), "full"),
        ((832, 100, 950, 130), "white"),
        ((30, 405, 365, 550), "white"),
        ((28, 590, 438, 660), "fg"),
        ((28, 667, 610, 785), "white"),
        ((0, 717, 600, 744), "blue"),
        ((30, 790, 225, 815), "white"),
        ((30, 825, 920, 880), "fg"),
    ],
    "right": [
        ((65, 40, 125, 98), "full"),
        ((40, 96, 150, 125), "white"),
        ((38, 220, 158, 345), "white"),
        ((30, 337, 164, 358), "fg"),
        ((16, 365, 179, 535), "white"),
        ((0, 468, 191, 498), "blue"),
        ((20, 560, 170, 585), "white"),
        ((50, 590, 140, 680), "white"),
        ((35, 682, 160, 775), "white"),
        ((0, 780, 191, 815), "white"),
        ((20, 822, 174, 868), "white"),
    ],
}

BACKGROUND_FULL_BOXES = {
    "left": [
        (55, 38, 135, 130),
        (14, 176, 178, 360),
        (0, 382, 191, 416),
        (48, 428, 144, 516),
        (12, 522, 180, 686),
        (0, 774, 191, 822),
        (12, 818, 180, 875),
    ],
    "front": [
        (24, 38, 180, 82),
        (850, 34, 955, 134),
        (20, 505, 380, 542),
        (18, 630, 455, 660),
        (0, 710, 625, 752),
        (22, 780, 238, 823),
        (22, 816, 930, 890),
    ],
    "right": [
        (55, 38, 135, 130),
        (30, 210, 165, 365),
        (4, 350, 188, 555),
        (16, 552, 174, 590),
        (44, 584, 146, 684),
        (28, 676, 166, 782),
        (0, 774, 191, 822),
        (12, 818, 180, 875),
    ],
}


def classify_pixels(image):
    arr = np.asarray(image.convert("RGB")).astype(np.int16)
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    mx = arr.max(axis=2)
    mn = arr.min(axis=2)
    sat = mx - mn
    lum = 0.299 * r + 0.587 * g + 0.114 * b

    white = ((lum > 135) & (sat < 95)) | ((lum > 185) & (sat < 145))
    gold = (
        ((r > 105) & (g > 70) & (b < 120) & (r >= g - 8) & (g >= b + 10))
        | ((r > 130) & (g > 100) & (b < 155) & (r > b + 20) & (g > b + 5))
    )
    blue = (b > 125) & (g > 70) & (r < 95) & ((b - r) > 45)
    return white, gold, blue


def build_overlay_mask(image, panel_name):
    white, gold, blue = classify_pixels(image)
    h, w = white.shape
    mask = np.zeros((h, w), dtype=bool)

    for (x0, y0, x1, y1), mode in OVERLAY_BOXES[panel_name]:
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(w, x1)
        y1 = min(h, y1)
        if mode == "full":
            mask[y0:y1, x0:x1] = True
        elif mode == "white":
            mask[y0:y1, x0:x1] |= white[y0:y1, x0:x1]
        elif mode == "fg":
            mask[y0:y1, x0:x1] |= (white | gold)[y0:y1, x0:x1]
        elif mode == "blue":
            mask[y0:y1, x0:x1] |= blue[y0:y1, x0:x1]

    return Image.fromarray((mask * 255).astype(np.uint8), "L")


def build_background_mask(overlay_mask, panel_name):
    arr = np.asarray(overlay_mask).copy()
    for x0, y0, x1, y1 in BACKGROUND_FULL_BOXES[panel_name]:
        arr[y0:y1, x0:x1] = 255
    return Image.fromarray(arr, "L")


def dilate(mask, radius):
    if radius <= 0:
        return mask
    return mask.filter(ImageFilter.MaxFilter(radius * 2 + 1))


def diffuse_inpaint(image, mask):
    arr = np.asarray(image.convert("RGB")).astype(np.float32)
    unknown = np.asarray(mask) > 0
    known = ~unknown
    out = arr.copy()

    # Seed stubborn masked areas with a broad blur so very large marks still
    # have plausible local color if the diffusion front does not fully meet.
    blur_seed = np.asarray(image.convert("RGB").filter(ImageFilter.GaussianBlur(18))).astype(
        np.float32
    )
    out[unknown] = blur_seed[unknown]

    h, w = unknown.shape
    max_iters = h + w
    for _ in range(max_iters):
        if not unknown.any():
            break

        sum_rgb = np.zeros_like(out)
        count = np.zeros((h, w), dtype=np.float32)

        # Eight-neighbor diffusion from known pixels into the current boundary.
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                ys = slice(max(0, dy), h + min(0, dy))
                xs = slice(max(0, dx), w + min(0, dx))
                yd = slice(max(0, -dy), h - max(0, dy))
                xd = slice(max(0, -dx), w - max(0, dx))

                src_known = known[ys, xs]
                sum_rgb[yd, xd] += out[ys, xs] * src_known[:, :, None]
                count[yd, xd] += src_known

        fillable = unknown & (count > 0)
        if not fillable.any():
            break

        out[fillable] = sum_rgb[fillable] / count[fillable, None]
        known[fillable] = True
        unknown[fillable] = False

    filled = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")
    smoothed = filled.filter(ImageFilter.GaussianBlur(10.0))
    feather = mask.filter(ImageFilter.GaussianBlur(8.0))
    return Image.composite(smoothed, image.convert("RGB"), feather)


def make_overlay(image, mask):
    rgba = np.asarray(image.convert("RGBA")).copy()
    rgba[:, :, 3] = np.asarray(mask)
    return Image.fromarray(rgba, "RGBA")


def make_lateral_background(image):
    blurred = image.convert("RGB").filter(ImageFilter.GaussianBlur(22.0))
    w, h = blurred.size
    arr = np.asarray(blurred).astype(np.float32)
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    x = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
    edge_vignette = 0.80 + 0.18 * (1 - np.abs(x))
    vertical_depth = 0.94 - 0.12 * y
    factor = edge_vignette * vertical_depth
    navy = np.array([0, 27, 70], dtype=np.float32)
    arr = arr * factor[:, :, None] + navy * (1 - factor[:, :, None]) * 0.45
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def smoothstep(edge0, edge1, value):
    value = np.clip((value - edge0) / (edge1 - edge0), 0, 1)
    return value * value * (3 - 2 * value)


def soft_rect(x, y, x0, y0, x1, y1, feather):
    left = smoothstep(x0, x0 + feather, x)
    right = 1 - smoothstep(x1 - feather, x1, x)
    top = smoothstep(y0, y0 + feather, y)
    bottom = 1 - smoothstep(y1 - feather, y1, y)
    return left * right * top * bottom


def make_front_background(image, overlay_mask):
    top_mask = np.zeros(image.size[::-1], dtype=np.uint8)
    raw_overlay = np.asarray(overlay_mask)
    top_mask[:150, :] = raw_overlay[:150, :]
    top_mask[:, 850:960] = np.maximum(top_mask[:, 850:960], raw_overlay[:, 850:960])
    top_mask[30:90, 20:190] = 255
    top_mask[30:140, 840:965] = 255
    top_mask_image = dilate(Image.fromarray(top_mask, "L"), 7)
    cleaned = diffuse_inpaint(image, top_mask_image)

    arr = np.asarray(cleaned).astype(np.float32)
    h, w = arr.shape[:2]
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    xx = np.linspace(0, 1, w, dtype=np.float32)[None, :]

    lower_left = smoothstep(0.54, 0.78, yy) * (1 - smoothstep(0.58, 0.86, xx))
    title_zone = soft_rect(xx, yy, -0.10, 0.36, 0.45, 0.70, 0.04)
    offer_zone = soft_rect(xx, yy, -0.10, 0.59, 0.56, 0.82, 0.04)
    big_offer_zone = soft_rect(xx, yy, -0.10, 0.64, 0.74, 0.97, 0.04)
    bottom_zone = np.broadcast_to(smoothstep(0.80, 0.90, yy), (h, w))

    alpha = np.maximum.reduce(
        [
            lower_left * 0.86,
            title_zone,
            offer_zone,
            big_offer_zone,
            bottom_zone,
        ]
    )
    alpha_blur = Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8), "L")
    alpha_blur = alpha_blur.filter(ImageFilter.GaussianBlur(18.0))
    alpha = np.asarray(alpha_blur).astype(np.float32) / 255.0

    fill = np.zeros_like(arr)
    fill[:, :, 0] = 1 + 4 * (1 - yy)
    fill[:, :, 1] = 19 + 26 * (1 - yy) + 8 * xx
    fill[:, :, 2] = 56 + 54 * (1 - yy) + 20 * (1 - xx)

    # Preserve the original right-side photographic body as much as possible.
    alpha *= 1 - 0.22 * smoothstep(0.90, 1.00, xx)
    out = arr * (1 - alpha[:, :, None]) + fill * alpha[:, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def checker_preview(overlay):
    w, h = overlay.size
    checker = Image.new("RGBA", (w, h), (48, 48, 48, 255))
    draw = ImageDraw.Draw(checker)
    step = max(12, min(w, h) // 12)
    for y in range(0, h, step):
        for x in range(0, w, step):
            if ((x // step) + (y // step)) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=(96, 96, 96, 255))
    checker.alpha_composite(overlay)
    return checker


def save_png(image, path):
    image.save(path, dpi=(DPI, DPI), compress_level=6)


def main():
    source = Image.open(SOURCE).convert("RGBA")

    outputs = {
        "front": (
            "frontal_background.png",
            "frontal_overlay_transparent.png",
        ),
        "left": (
            "left_lateral_background.png",
            "left_lateral_overlay_transparent.png",
        ),
        "right": (
            "right_lateral_background.png",
            "right_lateral_overlay_transparent.png",
        ),
    }

    for panel_name, crop_box in PANEL_CROPS.items():
        crop = source.crop(crop_box)
        overlay_mask = build_overlay_mask(crop, panel_name)
        background_mask = build_background_mask(overlay_mask, panel_name)
        background_mask = dilate(background_mask, BACKGROUND_MASK_DILATION[panel_name])

        if panel_name in ("left", "right"):
            background = make_lateral_background(crop)
        elif panel_name == "front":
            background = make_front_background(crop, overlay_mask)
        else:
            background = diffuse_inpaint(crop, background_mask)
        overlay = make_overlay(crop, overlay_mask)

        target_size = TARGET_SIZES[panel_name]
        background = background.resize(target_size, Image.Resampling.LANCZOS)
        overlay = overlay.resize(target_size, Image.Resampling.LANCZOS)

        background_path, overlay_path = outputs[panel_name]
        save_png(background, background_path)
        save_png(overlay, overlay_path)

        # Small QA previews are intentionally separate from the production files.
        preview_bg = background.resize((target_size[0] // 5, target_size[1] // 5), Image.Resampling.LANCZOS)
        preview_ov = overlay.resize((target_size[0] // 5, target_size[1] // 5), Image.Resampling.LANCZOS)
        preview_bg.save(f"qa_{panel_name}_background_preview.png")
        checker_preview(preview_ov).save(f"qa_{panel_name}_overlay_preview.png")

        print(
            f"{panel_name}: {background_path}, {overlay_path} "
            f"({target_size[0]}x{target_size[1]}, dpi={DPI})"
        )


if __name__ == "__main__":
    main()
