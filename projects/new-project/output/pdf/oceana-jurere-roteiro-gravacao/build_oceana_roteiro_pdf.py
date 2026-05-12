from pathlib import Path
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


ROOT = Path(r"C:\Users\vini1\OneDrive\Documentos\New project")
OUT_DIR = ROOT / "output" / "pdf" / "oceana-jurere-roteiro-gravacao"
TMP_DIR = ROOT / "tmp" / "pdfs" / "oceana-jurere-roteiro-gravacao"
PDF_PATH = OUT_DIR / "Oceana-Jurere-Roteiro-de-Gravacao-A-Ultima-Ideia.pdf"
LANDING_ASSETS = ROOT / "output" / "ultima-ideia-landing-organizado" / "05_area-de-trabalho-novas-versoes" / "aprovada-para-substituir-final" / "assets"
HERO_IMAGE = LANDING_ASSETS / "hero-wall-v2.png"
HAND_IMAGE = LANDING_ASSETS / "crop-method-hand.png"
PAPER_IMAGE = LANDING_ASSETS / "crop-deliverables-paper.png"
LOGO_IMAGE = LANDING_ASSETS / "logo-mao-estalo.jpeg"


PALETTE = {
    "obsidian": colors.HexColor("#070707"),
    "graphite": colors.HexColor("#171717"),
    "ritual": colors.HexColor("#F4F0E8"),
    "concrete": colors.HexColor("#A7A29A"),
    "red": colors.HexColor("#E11920"),
    "paper": colors.HexColor("#F4F0E8"),
    "paper2": colors.HexColor("#EBE6DC"),
}


def register_fonts():
    fonts = {
        "AUI-Display": r"C:\Windows\Fonts\ARIALNB.TTF",
        "AUI-Text": r"C:\Windows\Fonts\arial.ttf",
        "AUI-TextBold": r"C:\Windows\Fonts\arialbd.ttf",
    }
    for name, path in fonts.items():
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))


register_fonts()

DISPLAY = "AUI-Display" if "AUI-Display" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
TEXT = "AUI-Text" if "AUI-Text" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
BOLD = "AUI-TextBold" if "AUI-TextBold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"

W, H = A4
M = 42


def draw_wordmark(c, x, y, dark=True):
    c.setFont(DISPLAY, 14)
    c.setFillColor(PALETTE["ritual"] if dark else PALETTE["obsidian"])
    c.drawString(x, y, "A ÚLTIMA IDEIA")
    c.setFillColor(PALETTE["red"])
    c.circle(x + 122, y + 5, 2.4, fill=1, stroke=0)


def image_cover_path(src, name, target_w, target_h):
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out = TMP_DIR / name
    with Image.open(src) as im:
        im = im.convert("RGB")
        src_ratio = im.width / im.height
        target_ratio = target_w / target_h
        if src_ratio > target_ratio:
            new_w = int(im.height * target_ratio)
            left = (im.width - new_w) // 2
            box = (left, 0, left + new_w, im.height)
        else:
            new_h = int(im.width / target_ratio)
            top = (im.height - new_h) // 2
            box = (0, top, im.width, top + new_h)
        im.crop(box).resize((int(target_w * 2), int(target_h * 2)), Image.Resampling.LANCZOS).save(out)
    return out


def draw_cover_image(c, src, x, y, w, h, name):
    if not src.exists():
        return
    cropped = image_cover_path(src, name, w, h)
    c.drawImage(ImageReader(str(cropped)), x, y, width=w, height=h, mask="auto")
    c.setFillColor(colors.Color(0, 0, 0, alpha=0.28))
    c.rect(x, y, w, h, fill=1, stroke=0)


def draw_grain(c, dark=True):
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.05 if dark else 0.08))
    for x in range(22, int(W), 34):
        for y in range(28, int(H), 43):
            if (x + y) % 3 == 0:
                c.circle(x, y, 0.45, fill=1, stroke=0)


def footer(c, page, dark=True):
    c.setStrokeColor(PALETTE["graphite"] if dark else PALETTE["concrete"])
    c.setLineWidth(0.35)
    c.line(M, 32, W - M, 32)
    draw_wordmark(c, M, 17, dark=dark)
    c.setFont(TEXT, 7.5)
    c.setFillColor(PALETTE["concrete"])
    c.drawRightString(W - M - 46, 17, f"OCEANA JURERÊ / ROTEIRO DE GRAVAÇÃO / {page:02d}")


def text_lines(text, font, size, max_width):
    lines = []
    for raw in text.split("\n"):
        raw = raw.strip()
        if not raw:
            lines.append("")
            continue
        words = raw.split()
        line = ""
        for word in words:
            trial = word if not line else f"{line} {word}"
            if pdfmetrics.stringWidth(trial, font, size) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_wrapped(c, text, x, y, max_width, font=TEXT, size=10, leading=14, color=None, max_lines=None):
    c.setFont(font, size)
    c.setFillColor(color or PALETTE["ritual"])
    lines = text_lines(text, font, size, max_width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        if line:
            c.drawString(x, y, line)
        y -= leading
    return y


def label(c, text, x, y, dark=True):
    c.setFont(BOLD, 7.2)
    c.setFillColor(PALETTE["red"])
    c.drawString(x, y, text.upper())
    c.setStrokeColor(PALETTE["red"])
    c.setLineWidth(1.2)
    c.line(x, y - 5, x + 34, y - 5)


def page_title(c, kicker, title, page):
    c.setFillColor(PALETTE["obsidian"])
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_grain(c, dark=True)
    c.setFillColor(PALETTE["graphite"])
    c.rect(W - 64, 0, 64, H, fill=1, stroke=0)
    c.setFillColor(PALETTE["red"])
    c.rect(W - 64, 0, 3, H, fill=1, stroke=0)
    label(c, kicker, M, H - 58)
    c.setFont(DISPLAY, 35)
    c.setFillColor(PALETTE["ritual"])
    for i, line in enumerate(textwrap.wrap(title.upper(), 24)):
        c.drawString(M, H - 100 - (i * 38), line)
    footer(c, page, dark=True)


def light_page(c, page):
    c.setFillColor(PALETTE["paper"])
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_grain(c, dark=False)
    c.setFillColor(PALETTE["obsidian"])
    c.rect(0, 0, 14, H, fill=1, stroke=0)
    c.setFillColor(PALETTE["red"])
    c.rect(14, 0, 3, H, fill=1, stroke=0)
    footer(c, page, dark=False)


ROTEIRO = [
    {
        "n": "01",
        "title": "Morar deixa de ser necessidade",
        "time": "0s - 10s",
        "voice": "Tem um momento da vida em que morar deixa de ser sobre necessidade.",
        "intent": "Abrir com maturidade. A fala precisa tirar o espectador do modo compra e colocar a decisão dentro de uma fase de vida.",
        "visual": "Plano lento. Mar, luz entrando por vidro, textura de fachada, detalhe de mão abrindo uma cortina. Nada apressado.",
        "screen": "Morar deixa de ser necessidade.",
        "rhythm": "Pausa longa depois de 'vida'. Voz baixa, segura, sem tom promocional.",
    },
    {
        "n": "02",
        "title": "A vida que você construiu",
        "time": "10s - 25s",
        "voice": "Você já morou onde precisava. Já comprou o que fazia sentido. Já escolheu pelo preço, pelo prazo, pela lógica, pela oportunidade. Mas existe uma fase em que a escolha muda.",
        "intent": "Criar identificação com alguém que já venceu etapas racionais. O público precisa se reconhecer como quem não está mais no mesmo momento.",
        "visual": "Cortes curtos de cidade, chegada de carro, elevador, detalhe de arquitetura, mesa posta. A sensação é de vida organizada.",
        "screen": "Existe uma fase em que a escolha muda.",
        "rhythm": "Cadência de lista. Cada frase deve parecer uma etapa superada.",
    },
    {
        "n": "03",
        "title": "Não é apenas um apartamento",
        "time": "25s - 38s",
        "voice": "Você não procura mais apenas um apartamento. Você procura um lugar que acompanhe o tamanho da vida que você construiu. E talvez seja por isso que Jurerê continue sendo Jurerê.",
        "intent": "Virar de produto para símbolo. A decisão deixa de ser metragem e passa a ser permanência, território e reconhecimento.",
        "visual": "Mostrar proximidade com o mar, paisagem de Jurerê, caminhada tranquila, fachada em composição limpa.",
        "screen": "Um lugar do tamanho da vida que você construiu.",
        "rhythm": "A frase 'Jurerê continue sendo Jurerê' deve entrar como conclusão, não como slogan.",
    },
    {
        "n": "04",
        "title": "A pergunta certa",
        "time": "38s - 52s",
        "voice": "Por que alguém que pode morar em qualquer lugar escolheria o Oceana? Não porque ele está em Jurerê. Isso, sozinho, não basta. A pergunta certa é: o que ainda existe em Jurerê que realmente pode ser chamado de oportunidade?",
        "intent": "Aumentar critério. O roteiro não deve defender o óbvio. Ele precisa mostrar que localização só tem valor quando encontra produto e momento.",
        "visual": "Corte seco. Tela escura por meio segundo. Depois, detalhes do empreendimento e mapa/território de forma elegante.",
        "screen": "O que ainda pode ser chamado de oportunidade?",
        "rhythm": "Mais firme. A pergunta deve funcionar como ponto de tensão do vídeo.",
    },
    {
        "n": "05",
        "title": "Três camadas de decisão",
        "time": "52s - 70s",
        "voice": "Um imóvel de alto padrão precisa responder a três coisas: localização, produto e momento. No Oceana, essas três camadas se encontram. Jurerê Internacional é um endereço consolidado, com baixa disponibilidade, alta procura e uma dinâmica própria de valorização.",
        "intent": "Entrar no argumento racional sem perder a aura. Aqui o vídeo prova critério.",
        "visual": "Sequência com três palavras em tela: localização, produto, momento. Intercalar com imagens de entorno, planta e mar.",
        "screen": "Localização. Produto. Momento.",
        "rhythm": "Mais objetivo. A fala deve soar como diagnóstico de mercado.",
    },
    {
        "n": "06",
        "title": "Conforto, mar e privacidade",
        "time": "70s - 88s",
        "voice": "O projeto entrega uma proposta rara: morar com conforto, receber bem, estar perto do mar e manter a privacidade que esse perfil de cliente valoriza. Não é um imóvel para quem está apenas procurando metragem.",
        "intent": "Traduzir produto em vida. A planta e o alto padrão precisam aparecer como consequência de um jeito de viver.",
        "visual": "Ambientes internos, varanda, circulação, mesa, área social, luz natural. Evitar excesso de pessoas; usar presença discreta.",
        "screen": "Conforto. Mar. Privacidade.",
        "rhythm": "Suave, mas com precisão. A frase final deve cortar a lógica de compra comum.",
    },
    {
        "n": "07",
        "title": "A decisão está no conjunto",
        "time": "88s - 108s",
        "voice": "É para quem entende que, em certos endereços, a decisão está no conjunto. Localização. Planta. Liquidez. Estilo de vida. Permanência. Oceana Jurerê. Uma curadoria B. Living para quem quer decidir com critério.",
        "intent": "Fechar com autoridade e sem pressa. A assinatura deve parecer curadoria, não chamada agressiva.",
        "visual": "Montagem final em cortes lentos: fachada, mar, interior, detalhe de acabamento, horizonte. Encerrar com logo/nome do projeto.",
        "screen": "Oceana Jurerê. Decidir com critério.",
        "rhythm": "Pausas claras entre as palavras finais. Não acelerar o fechamento.",
    },
]


FULL_SCRIPT = """Tem um momento da vida em que morar deixa de ser sobre necessidade.

Você já morou onde precisava. Já comprou o que fazia sentido. Já escolheu pelo preço, pelo prazo, pela lógica, pela oportunidade.

Mas existe uma fase em que a escolha muda.

Você não procura mais apenas um apartamento. Você procura um lugar que acompanhe o tamanho da vida que você construiu.

E talvez seja por isso que Jurerê continue sendo Jurerê.

Por que alguém que pode morar em qualquer lugar escolheria o Oceana?

Não porque ele está em Jurerê. Isso, sozinho, não basta.

A pergunta certa é: o que ainda existe em Jurerê que realmente pode ser chamado de oportunidade?

Um imóvel de alto padrão precisa responder a três coisas: localização, produto e momento.

No Oceana, essas três camadas se encontram.

Jurerê Internacional é um endereço consolidado, com baixa disponibilidade, alta procura e uma dinâmica própria de valorização.

O projeto entrega uma proposta rara: morar com conforto, receber bem, estar perto do mar e manter a privacidade que esse perfil de cliente valoriza.

Não é um imóvel para quem está apenas procurando metragem.

É para quem entende que, em certos endereços, a decisão está no conjunto.

Localização. Planta. Liquidez. Estilo de vida. Permanência.

Oceana Jurerê.

Uma curadoria B. Living para quem quer decidir com critério."""


def cover(c):
    c.setFillColor(PALETTE["obsidian"])
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_grain(c, dark=True)
    c.setFillColor(PALETTE["graphite"])
    c.rect(W - 64, 0, 64, H, fill=1, stroke=0)
    c.setFillColor(PALETTE["red"])
    c.rect(W - 64, 0, 3, H, fill=1, stroke=0)
    c.rect(M, H - 93, 112, 2, fill=1, stroke=0)
    c.circle(M + 126, H - 92, 3, fill=1, stroke=0)
    c.setStrokeColor(colors.Color(0.956, 0.941, 0.91, alpha=0.11))
    c.setLineWidth(0.5)
    for yy in (H - 155, H - 312, H - 515):
        c.line(M, yy, W - 184, yy)
    draw_wordmark(c, M, H - 55, dark=True)
    c.setFont(DISPLAY, 54)
    c.setFillColor(PALETTE["ritual"])
    c.drawString(M, H - 185, "OCEANA")
    c.drawString(M, H - 238, "JURERÊ")
    c.setFont(BOLD, 12)
    c.setFillColor(PALETTE["concrete"])
    c.drawString(M, H - 278, "ROTEIRO DE GRAVAÇÃO / NARRATIVA DE ALTO PADRÃO")
    c.setFont(TEXT, 10)
    c.setFillColor(PALETTE["ritual"])
    draw_wrapped(
        c,
        "Uma peça para vender critério, não urgência. O imóvel aparece como consequência de localização, produto, momento e vida construída.",
        M,
        H - 330,
        360,
        font=TEXT,
        size=12,
        leading=17,
        color=PALETTE["ritual"],
    )
    c.setFont(TEXT, 8.5)
    c.setFillColor(PALETTE["concrete"])
    c.drawString(M, 66, "Formato sugerido: filme vertical ou horizontal curto / 90 a 110 segundos")
    footer(c, 1, dark=True)
    c.showPage()


def direction_page(c):
    page_title(c, "direção", "O vídeo não vende metragem. Ele vende critério.", 2)
    y = H - 205
    columns = [
        ("TOM", "Baixo, adulto, consultivo. Sem euforia, sem promessa facil, sem linguagem de corretagem comum."),
        ("PÚBLICO", "Cliente que já comprou por lógica e agora decide por conjunto: vida, liquidez, privacidade e permanência."),
        ("RITMO", "Começo contemplativo, meio analítico, fechamento autoral. Pausas são parte da percepção de alto valor."),
        ("REGRA", "Jurerê não entra como argumento suficiente. Entra como território que precisa ser provado pelo produto e pelo momento."),
    ]
    for i, (name, body) in enumerate(columns):
        x = M if i % 2 == 0 else W / 2 + 8
        yy = y - (i // 2) * 145
        label(c, name, x, yy)
        draw_wrapped(c, body, x, yy - 28, 218, size=11, leading=16, color=PALETTE["ritual"])
    c.showPage()


def structure_page(c):
    light_page(c, 3)
    c.setFillColor(PALETTE["paper2"])
    c.rect(W - 56, 0, 56, H, fill=1, stroke=0)
    c.setFillColor(PALETTE["red"])
    c.rect(W - 56, 0, 3, H, fill=1, stroke=0)
    label(c, "estrutura narrativa", M + 8, H - 58, dark=False)
    c.setFont(DISPLAY, 31)
    c.setFillColor(PALETTE["obsidian"])
    c.drawString(M + 8, H - 103, "4 ATOS PARA CONDUZIR A DECISÃO")
    acts = [
        ("01", "Fase de vida", "Morar deixa de ser necessidade e passa a ser expressão de uma vida construída."),
        ("02", "Tensão", "Se alguém pode morar em qualquer lugar, Jurerê sozinho não basta como resposta."),
        ("03", "Critério", "A oportunidade aparece quando localização, produto e momento se encontram."),
        ("04", "Curadoria", "Oceana entra como conjunto: planta, liquidez, estilo de vida e permanência."),
    ]
    y = H - 158
    for n, title, body in acts:
        c.setFillColor(PALETTE["red"])
        c.rect(M + 8, y - 4, 28, 4, fill=1, stroke=0)
        c.setFont(DISPLAY, 21)
        c.setFillColor(PALETTE["obsidian"])
        c.drawString(M + 48, y - 7, f"{n} / {title.upper()}")
        draw_wrapped(c, body, M + 48, y - 32, 420, font=TEXT, size=10.5, leading=15, color=PALETTE["obsidian"])
        y -= 104
    footer(c, 3, dark=False)
    c.showPage()


def scene_page(c, scene, page):
    c.setFillColor(PALETTE["obsidian"])
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_grain(c, dark=True)
    c.setFillColor(PALETTE["graphite"])
    c.rect(W - 112, 96, 70, H - 198, fill=1, stroke=0)
    c.setStrokeColor(colors.Color(0.956, 0.941, 0.91, alpha=0.12))
    c.setLineWidth(0.5)
    c.rect(W - 112, 96, 70, H - 198, fill=0, stroke=1)
    c.setFillColor(PALETTE["red"])
    c.rect(0, 0, 8, H, fill=1, stroke=0)
    c.setFont(DISPLAY, 42)
    c.setFillColor(PALETTE["red"])
    c.drawString(M, H - 76, scene["n"])
    c.setFont(DISPLAY, 26)
    c.setFillColor(PALETTE["ritual"])
    c.drawString(M + 72, H - 72, scene["title"].upper())
    c.setFont(BOLD, 8)
    c.setFillColor(PALETTE["concrete"])
    c.drawString(M + 72, H - 93, scene["time"].upper())

    y = H - 132
    label(c, "fala principal", M, y)
    y = draw_wrapped(c, scene["voice"], M, y - 29, W - 2 * M, font=DISPLAY, size=18, leading=23, color=PALETTE["ritual"])
    y -= 18

    x1 = M
    x2 = W / 2 + 9
    label(c, "intenção", x1, y)
    label(c, "imagem", x2, y)
    y1 = draw_wrapped(c, scene["intent"], x1, y - 27, 230, font=TEXT, size=9.8, leading=14, color=PALETTE["ritual"])
    y2 = draw_wrapped(c, scene["visual"], x2, y - 27, 230, font=TEXT, size=9.8, leading=14, color=PALETTE["ritual"])
    y = min(y1, y2) - 20

    c.setStrokeColor(PALETTE["graphite"])
    c.setLineWidth(0.5)
    c.line(M, y + 10, W - M, y + 10)
    label(c, "texto na tela", x1, y)
    label(c, "ritmo de locução", x2, y)
    draw_wrapped(c, scene["screen"], x1, y - 27, 230, font=BOLD, size=11.5, leading=16, color=PALETTE["ritual"])
    draw_wrapped(c, scene["rhythm"], x2, y - 27, 230, font=TEXT, size=9.8, leading=14, color=PALETTE["ritual"])
    footer(c, page, dark=True)
    c.showPage()


def teleprompter_pages(c, start_page):
    light_page(c, start_page)
    label(c, "teleprompter", M + 8, H - 58, dark=False)
    c.setFont(DISPLAY, 31)
    c.setFillColor(PALETTE["obsidian"])
    c.drawString(M + 8, H - 103, "VERSÃO CORRIDA DA LOCUÇÃO")
    y = H - 143
    page = start_page
    for paragraph in FULL_SCRIPT.split("\n\n"):
        lines = text_lines(paragraph, TEXT, 11.5, W - 2 * M - 16)
        needed = len(lines) * 16 + 15
        if y - needed < 68:
            c.showPage()
            page += 1
            light_page(c, page)
            y = H - 58
        y = draw_wrapped(c, paragraph, M + 8, y, W - 2 * M - 16, font=TEXT, size=11.5, leading=16, color=PALETTE["obsidian"])
        y -= 13
    c.showPage()
    return page + 1


def checklist_page(c, page):
    page_title(c, "checklist", "Antes de gravar, proteger a percepção.", page)
    items = [
        "A locução está mais próxima de curadoria do que de anúncio.",
        "As imagens mostram silêncio, espaço, textura, mar e privacidade.",
        "O vídeo não depende de adjetivos genéricos de luxo.",
        "Jurerê aparece como endereço consolidado, não como clichê turístico.",
        "Oceana é apresentado pelo conjunto: localização, planta, liquidez, estilo de vida e permanência.",
        "O fechamento não pede atenção. Ele sustenta critério.",
    ]
    y = H - 205
    for item in items:
        c.setFillColor(PALETTE["red"])
        c.rect(M, y - 2, 10, 10, fill=1, stroke=0)
        draw_wrapped(c, item, M + 28, y + 2, W - 2 * M - 28, font=TEXT, size=12, leading=16, color=PALETTE["ritual"])
        y -= 52
    c.showPage()


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    c.setTitle("Oceana Jurerê - Roteiro de Gravação")
    c.setAuthor("A Ultima Ideia")
    c.setSubject("Roteiro de gravação para campanha Oceana Jurerê")

    cover(c)
    direction_page(c)
    structure_page(c)
    page = 4
    for scene in ROTEIRO:
        scene_page(c, scene, page)
        page += 1
    page = teleprompter_pages(c, page)
    checklist_page(c, page)
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build()
