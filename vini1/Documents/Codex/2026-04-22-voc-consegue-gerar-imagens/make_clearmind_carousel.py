from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "carrossel_clearmind_referencia"
MEDIA = Path(r"C:\Users\vini1\Downloads\POST LENTE")

W, H = 1080, 1350
INK = "#111111"
MUTED = "#5d6268"
BLUE = "#0050A4"
LIGHT_BLUE = "#EAF3FF"
BROWN = "#6F5545"
WARM = "#F7F4EF"
LINE = "#D6D7D9"


def font(size, bold=False, serif=False):
    candidates = []
    if serif:
        candidates = [
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
    return ImageFont.load_default(size=size)


F = {
    "eyebrow": font(26, bold=True),
    "small": font(28),
    "small_b": font(28, bold=True),
    "body": font(42),
    "body_b": font(42, bold=True),
    "title": font(74, bold=True),
    "title2": font(64, bold=True),
    "serif": font(44, serif=True),
    "serif_b": font(58, bold=True, serif=True),
    "logo": font(38, bold=True, serif=True),
}


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=fnt) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, text, xy, fnt, fill=INK, max_width=900, line_gap=12, align="left"):
    x, y = xy
    lines = wrap(draw, text, fnt, max_width)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        lw = bbox[2] - bbox[0]
        tx = x
        if align == "center":
            tx = x + (max_width - lw) / 2
        draw.text((tx, y), line, font=fnt, fill=fill)
        y += bbox[3] - bbox[1] + line_gap
    return y


def cover_crop(img, box, radius=0):
    x, y, w, h = box
    src = img.copy()
    src_ratio = src.width / src.height
    dst_ratio = w / h
    if src_ratio > dst_ratio:
        nw = int(src.height * dst_ratio)
        left = (src.width - nw) // 2
        src = src.crop((left, 0, left + nw, src.height))
    else:
        nh = int(src.width / dst_ratio)
        top = (src.height - nh) // 2
        src = src.crop((0, top, src.width, top + nh))
    src = src.resize((w, h), Image.Resampling.LANCZOS)
    if radius:
        mask = Image.new("L", (w, h), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
        out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        out.paste(src.convert("RGBA"), (0, 0), mask)
        return out
    return src


def base(bg="#FFFFFF"):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    return im, d


def brand_bar(d, dark=False, page=None):
    color = "#FFFFFF" if dark else INK
    d.text((72, 58), "ÓPTICA REFERÊNCIA", font=F["small_b"], fill=color)
    d.rectangle((720, 42, 830, 129), fill=BLUE)
    d.text((743, 70), "ZEISS", font=font(28, bold=True, serif=True), fill="#FFFFFF")
    d.text((852, 59), "ZVC", font=font(30, bold=True), fill=color)
    d.text((852, 96), "by Óptica Referência", font=font(19), fill=color)
    if page:
        d.text((950, 1245), page, font=F["small"], fill=color if dark else MUTED)


def zeiss_flag(d, x, y, scale=1):
    w, h = int(124 * scale), int(94 * scale)
    d.rectangle((x, y, x + w, y + h), fill=BLUE)
    fnt = font(int(32 * scale), bold=True, serif=True)
    bbox = d.textbbox((0, 0), "ZEISS", font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((x + (w - tw) / 2, y + (h - th) / 2 - int(2 * scale)), "ZEISS", font=fnt, fill="#FFFFFF")


def save(im, name):
    OUT.mkdir(exist_ok=True)
    path = OUT / name
    im.save(path, quality=95)
    return path


def slide_1(article):
    im, d = base("#FFFFFF")
    brand_bar(d, page="1/6")
    d.text((72, 230), "SAÚDE + TECNOLOGIA", font=F["eyebrow"], fill=BROWN)
    y = draw_wrapped(
        d,
        "Novas lentes ZEISS chegam ao Brasil para aliviar a rotina entre telas",
        (72, 285),
        F["title2"],
        max_width=910,
        line_gap=12,
    )
    y += 26
    d.rectangle((72, y, 1008, y + 2), fill=LINE)
    y += 42
    draw_wrapped(
        d,
        "A tecnologia ClearMind virou notícia na Veja e agora reforça uma exclusividade da Óptica Referência.",
        (72, y),
        F["body"],
        max_width=890,
        line_gap=10,
    )
    crop = article.crop((0, 470, article.width, min(article.height, 1500)))
    thumb = cover_crop(crop, (72, 865, 936, 330), radius=8)
    im.paste(thumb, (72, 865), thumb if thumb.mode == "RGBA" else None)
    d.rounded_rectangle((72, 865, 1008, 1195), radius=8, outline=LINE, width=2)
    d.text((72, 1238), "Arraste para entender o que muda na sua visão.", font=F["small_b"], fill=INK)
    return save(im, "01_capa_noticia.png")


def slide_2():
    im, d = base(WARM)
    brand_bar(d, page="2/6")
    d.text((72, 225), "O PROBLEMA", font=F["eyebrow"], fill=BROWN)
    draw_wrapped(d, "Sua mente também cansa quando seus olhos trabalham demais.", (72, 300), F["title"], max_width=900, line_gap=10)
    items = [
        "Horas alternando celular, computador e ambientes diferentes.",
        "Foco constante em múltiplos estímulos digitais.",
        "Mais esforço para manter conforto, atenção e nitidez.",
    ]
    y = 730
    for i, item in enumerate(items, 1):
        d.ellipse((72, y + 12, 102, y + 42), fill=BLUE)
        d.text((81, y + 8), str(i), font=font(24, bold=True), fill="#FFFFFF")
        y = draw_wrapped(d, item, (128, y), F["body"], max_width=790, line_gap=8) + 34
    d.text((72, 1215), "Não é só sobre enxergar. É sobre render melhor no dia a dia.", font=F["small_b"], fill=INK)
    return save(im, "02_problema_telas.png")


def slide_3(lens):
    im, d = base("#FFFFFF")
    brand_bar(d, page="3/6")
    d.text((72, 210), "A TECNOLOGIA", font=F["eyebrow"], fill=BROWN)
    draw_wrapped(d, "ClearMind: lentes criadas para uma vida cada vez mais digital.", (72, 275), F["title2"], max_width=930, line_gap=10)
    photo = cover_crop(lens, (72, 610, 936, 420), radius=8)
    im.paste(photo, (72, 610), photo if photo.mode == "RGBA" else None)
    d.rounded_rectangle((72, 610, 1008, 1030), radius=8, outline=LINE, width=2)
    d.rounded_rectangle((312, 830, 768, 900), radius=6, fill=(0, 80, 164))
    d.text((344, 849), "ENTRA VÍDEO DAS LENTES AQUI", font=F["small_b"], fill="#FFFFFF")
    draw_wrapped(
        d,
        "Use o vídeo vertical ZEISS ClearMind neste card para dar movimento ao carrossel.",
        (72, 1085),
        F["body"],
        max_width=910,
        line_gap=8,
    )
    return save(im, "03_card_video_lentes.png")


def slide_4():
    im, d = base("#FFFFFF")
    brand_bar(d, page="4/6")
    d.text((72, 225), "NA PRÁTICA", font=F["eyebrow"], fill=BROWN)
    draw_wrapped(d, "O benefício aparece na rotina, não só na armação.", (72, 292), F["title"], max_width=910, line_gap=10)
    cards = [
        ("Conforto", "menos sensação de sobrecarga em dias intensos"),
        ("Foco", "mais facilidade para alternar entre telas e ambientes"),
        ("Qualidade de vida", "uma escolha visual pensada para o seu ritmo"),
    ]
    y = 700
    for title, body in cards:
        d.rounded_rectangle((72, y, 1008, y + 150), radius=8, fill=LIGHT_BLUE)
        d.text((112, y + 28), title, font=F["body_b"], fill=BLUE)
        draw_wrapped(d, body, (390, y + 31), F["body"], max_width=560, line_gap=8)
        y += 185
    return save(im, "04_beneficios_rotina.png")


def slide_5():
    im, d = base("#111111")
    brand_bar(d, dark=True, page="5/6")
    d.text((72, 230), "EXCLUSIVIDADE", font=F["eyebrow"], fill="#CDBAAE")
    draw_wrapped(d, "Tecnologia alemã ZEISS com atendimento próximo da Referência.", (72, 300), F["title"], fill="#FFFFFF", max_width=900, line_gap=10)
    d.rectangle((72, 742, 1008, 744), fill="#404040")
    draw_wrapped(
        d,
        "Aqui, você entende a lente certa para sua rotina antes de decidir.",
        (72, 805),
        F["serif_b"],
        fill="#FFFFFF",
        max_width=895,
        line_gap=12,
    )
    d.rounded_rectangle((72, 1115, 662, 1195), radius=8, fill="#FFFFFF")
    d.text((108, 1137), "Agende sua avaliação", font=F["body_b"], fill=INK)
    return save(im, "05_exclusividade_referencia.png")


def slide_6():
    im, d = base(WARM)
    brand_bar(d, page="6/6")
    zeiss_flag(d, 72, 265, scale=1.15)
    d.text((72, 405), "ClearMind", font=font(96, bold=True), fill=INK)
    draw_wrapped(d, "Para quem vive entre telas, decisões e muitos estímulos.", (72, 525), F["serif_b"], max_width=860, line_gap=14)
    d.rectangle((72, 790, 1008, 792), fill=LINE)
    draw_wrapped(d, "Conheça na Óptica Referência.", (72, 850), F["title2"], max_width=890, line_gap=10)
    draw_wrapped(d, "Post collab: ZEISS Vision Center by Óptica Referência + Óptica Referência", (72, 1080), F["small"], fill=MUTED, max_width=820, line_gap=8)
    d.text((72, 1215), "CTA: chame no direct ou visite a loja.", font=F["small_b"], fill=INK)
    return save(im, "06_cta_final.png")


def make_preview(paths):
    html = f"""<!doctype html>
<html lang="pt-BR">
<meta charset="utf-8">
<title>Preview Carrossel ClearMind</title>
<style>
  body {{ margin: 0; background: #ececec; font-family: Arial, sans-serif; }}
  main {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; padding: 24px; }}
  figure {{ margin: 0; background: white; padding: 12px; border-radius: 8px; }}
  img, video {{ width: 100%; border-radius: 4px; display: block; }}
  figcaption {{ font-size: 14px; color: #555; margin-top: 8px; }}
</style>
<main>
  {''.join(f'<figure><img src="{p.name}"><figcaption>{p.name}</figcaption></figure>' for p in paths[:2])}
  <figure>
    <video src="C:/Users/vini1/Downloads/POST LENTE/VERTICAL_ZEISS_ClearMind_9x16_OP1_15s.mp4" controls muted loop playsinline></video>
    <figcaption>Slide 3 em vídeo: usar VERTICAL_ZEISS_ClearMind_9x16_OP1_15s.mp4</figcaption>
  </figure>
  {''.join(f'<figure><img src="{p.name}"><figcaption>{p.name}</figcaption></figure>' for p in paths[3:])}
</main>
</html>
"""
    (OUT / "preview_carrossel.html").write_text(html, encoding="utf-8")


def make_caption():
    text = """# Carrossel ClearMind - Referência + ZEISS Vision Center

## Ordem sugerida do carrossel
1. 01_capa_noticia.png
2. 02_problema_telas.png
3. VERTICAL_ZEISS_ClearMind_9x16_OP1_15s.mp4
4. 04_beneficios_rotina.png
5. 05_exclusividade_referencia.png
6. 06_cta_final.png

Use o arquivo 03_card_video_lentes.png apenas como referência visual do slide-vídeo.

## Legenda sugerida
Você sente que sua rotina entre telas exige cada vez mais da sua visão?

As novas lentes ZEISS ClearMind foram destaque na Veja por uma proposta muito atual: ajudar a reduzir o esforço mental em meio aos estímulos digitais do dia a dia.

Na Óptica Referência, essa tecnologia chega com o que mais importa na hora de escolher suas lentes: orientação, confiança e atendimento próximo.

Conheça as lentes ClearMind e descubra se elas fazem sentido para a sua rotina.

Chame no direct ou visite a Óptica Referência.

## Observações de publicação
- Publicar no perfil da Óptica Referência.
- Marcar como collab com ZEISS Vision Center by Óptica Referência se fizer sentido na estratégia do dia.
- Inserir o link da reportagem nos stories no mesmo dia do post.
- Evitar mencionar promoção de aniversário neste post, para manter o foco editorial/exclusividade.
"""
    (OUT / "legenda_e_orientacoes.md").write_text(text, encoding="utf-8")


def main():
    article = Image.open(MEDIA / "IMG_7090.JPEG").convert("RGB")
    lens_source = article.crop((0, int(article.height * 0.72), article.width, article.height))
    paths = [
        slide_1(article),
        slide_2(),
        slide_3(lens_source),
        slide_4(),
        slide_5(),
        slide_6(),
    ]
    make_preview(paths)
    make_caption()
    print(f"Created {len(paths)} PNGs in {OUT}")


if __name__ == "__main__":
    main()
