from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(r"C:\Users\vini1\OneDrive\Documentos\New project")
OUT_DIR = ROOT / "output" / "pdf" / "oceana-jurere-locucao-corrida"
PDF_PATH = OUT_DIR / "Oceana-Jurere-Versao-Corrida-da-Locucao.pdf"

PALETTE = {
    "ink": colors.HexColor("#070707"),
    "paper": colors.HexColor("#F4F0E8"),
    "red": colors.HexColor("#E11920"),
}


def register_fonts():
    fonts = {
        "AUI-Display": r"C:\Windows\Fonts\ARIALNB.TTF",
        "AUI-Text": r"C:\Windows\Fonts\arial.ttf",
    }
    for name, path in fonts.items():
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))


register_fonts()

DISPLAY = "AUI-Display" if "AUI-Display" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
TEXT = "AUI-Text" if "AUI-Text" in pdfmetrics.getRegisteredFontNames() else "Helvetica"

W, H = A4
M = 52

SCRIPT = """Tem um momento da vida em que morar deixa de ser sobre necessidade.

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


def draw_wrapped(c, text, x, y, max_width, font, size, leading, color):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in text_lines(text, font, size, max_width):
        if line:
            c.drawString(x, y, line)
        y -= leading
    return y


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    c.setTitle("Oceana Jurerê - Versão Corrida da Locução")
    c.setAuthor("A Última Ideia")

    c.setFillColor(PALETTE["paper"])
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(PALETTE["ink"])
    c.rect(0, 0, 15, H, fill=1, stroke=0)
    c.setFillColor(PALETTE["red"])
    c.rect(15, 0, 3, H, fill=1, stroke=0)

    c.setFont(TEXT, 7.5)
    c.setFillColor(PALETTE["red"])
    c.drawString(M, H - 58, "TELEPROMPTER")
    c.rect(M, H - 68, 38, 1.4, fill=1, stroke=0)

    c.setFont(DISPLAY, 31)
    c.setFillColor(PALETTE["ink"])
    c.drawString(M, H - 112, "VERSÃO CORRIDA DA LOCUÇÃO")

    draw_wrapped(
        c,
        SCRIPT,
        M,
        H - 154,
        W - (M * 2),
        font=TEXT,
        size=11.3,
        leading=16.2,
        color=PALETTE["ink"],
    )

    c.showPage()
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build()
