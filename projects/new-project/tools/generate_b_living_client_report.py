from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\vini1\OneDrive\Documentos\New project")
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT_DIR / "Relatorio_Cliente_B_Living_Abril_2026.pdf"

DOWNLOADS = Path(r"C:\Users\vini1\Downloads")
LOGO_WHITE = DOWNLOADS / "B. LIVING LOGO - BRANCA.png"

FONT_DIR = Path(r"C:\Windows\Fonts")
ARIAL = FONT_DIR / "arial.ttf"
ARIAL_BOLD = FONT_DIR / "arialbd.ttf"

if ARIAL.exists() and ARIAL_BOLD.exists():
    pdfmetrics.registerFont(TTFont("ReportRegular", str(ARIAL)))
    pdfmetrics.registerFont(TTFont("ReportBold", str(ARIAL_BOLD)))
else:
    # Built-in fallback. Accented text is safer with Arial, but this keeps generation usable.
    "ReportRegular"
    "ReportBold"


PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#111927")
INK = colors.HexColor("#1E252F")
MUTED = colors.HexColor("#667085")
GOLD = colors.HexColor("#B89B63")
BEIGE = colors.HexColor("#F4EFE6")
LINE = colors.HexColor("#E4E7EC")
SOFT = colors.HexColor("#F7F4EF")
GREEN = colors.HexColor("#287A5C")


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="ReportBold",
        fontSize=31,
        leading=36,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        fontName="ReportRegular",
        fontSize=11.5,
        leading=16.5,
        textColor=colors.HexColor("#E7E0D5"),
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverMeta",
        fontName="ReportRegular",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#D8C8A7"),
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="H1",
        fontName="ReportBold",
        fontSize=18,
        leading=23,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="H2",
        fontName="ReportBold",
        fontSize=12.5,
        leading=16,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyClient",
        fontName="ReportRegular",
        fontSize=9.2,
        leading=13.2,
        textColor=INK,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        fontName="ReportRegular",
        fontSize=7.6,
        leading=10.2,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHead",
        fontName="ReportBold",
        fontSize=7.6,
        leading=9.5,
        textColor=colors.white,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="TableCell",
        fontName="ReportRegular",
        fontSize=7.4,
        leading=9.3,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="MetricNum",
        fontName="ReportBold",
        fontSize=17,
        leading=20,
        textColor=NAVY,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="MetricLabel",
        fontName="ReportRegular",
        fontSize=7.3,
        leading=9,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="Footer",
        fontName="ReportRegular",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#98A2B3"),
        alignment=TA_RIGHT,
    )
)


def p(text, style="BodyClient"):
    return Paragraph(text, styles[style])


def bullet(items):
    return ListFlowable(
        [ListItem(p(item), leftIndent=2 * mm) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=5 * mm,
        bulletFontName="ReportRegular",
        bulletFontSize=6,
        bulletColor=GOLD,
    )


def section(title):
    return p(title, "H1")


def subsection(title):
    return p(title, "H2")


def metric_cards(items):
    cells = []
    for num, label in items:
        cells.append([p(num, "MetricNum"), p(label, "MetricLabel")])
    tbl = Table([cells], colWidths=[(PAGE_W - 36 * mm) / len(items)] * len(items))
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E7DDCC")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E7DDCC")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return tbl


def simple_table(headers, rows, widths):
    data = [[p(h, "TableHead") for h in headers]]
    for row in rows:
        data.append([p(str(cell), "TableCell") for cell in row])
    tbl = Table(data, colWidths=widths, repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFAF7")]),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return tbl


class ClientReport(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=17 * mm,
            bottomMargin=15 * mm,
            title="Relatório de Entregas - B. Living - Abril 2026",
            author="A Última Ideia",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(
            [
                PageTemplate(id="cover", frames=frame, onPage=draw_cover_bg),
                PageTemplate(id="normal", frames=frame, onPage=draw_page),
            ]
        )


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, PAGE_H - 12 * mm, PAGE_W - 18 * mm, PAGE_H - 12 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("ReportRegular", 7.2)
    canvas.drawString(18 * mm, PAGE_H - 9 * mm, "B. Living - Relatório de entregas | Abril 2026")
    canvas.setFont("ReportRegular", 7)
    canvas.drawRightString(PAGE_W - 18 * mm, 9 * mm, f"Página {doc.page}")
    canvas.restoreState()


def draw_cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 7 * mm, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#172233"))
    canvas.rect(7 * mm, 0, 10 * mm, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#182231"))
    canvas.rect(0, 0, PAGE_W, 44 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(colors.HexColor("#334155"))
    canvas.setLineWidth(0.7)
    canvas.line(24 * mm, 82 * mm, PAGE_W - 24 * mm, 82 * mm)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.1)
    canvas.line(24 * mm, 96 * mm, 74 * mm, 96 * mm)
    canvas.restoreState()


def cover_story():
    flow = []
    flow.append(Spacer(1, 18 * mm))
    if LOGO_WHITE.exists():
        img = Image(str(LOGO_WHITE), width=55 * mm, height=22 * mm, kind="proportional")
        flow.append(img)
        flow.append(Spacer(1, 44 * mm))
    else:
        flow.append(p("B. LIVING", "CoverTitle"))
        flow.append(Spacer(1, 40 * mm))
    flow.append(p("Relatório de Entregas", "CoverTitle"))
    flow.append(p("Abril de 2026", "CoverSub"))
    flow.append(Spacer(1, 10 * mm))
    flow.append(
        p(
            "Consolidação executiva das frentes desenvolvidas no mês: inauguração, conteúdo, relacionamento, "
            "materiais comerciais, suporte operacional e organização das próximas entregas.",
            "CoverSub",
        )
    )
    flow.append(Spacer(1, 71 * mm))
    flow.append(p("Preparado para apresentação à B. Living", "CoverMeta"))
    flow.append(p("A Última Ideia", "CoverMeta"))
    flow.append(NextPageTemplate("normal"))
    flow.append(PageBreak())
    return flow


executive_points = [
    "Abril concentrou a virada de implantação da presença da B. Living, com foco em inauguração, geração de percepção de marca, suporte comercial, captação audiovisual e organização da comunicação digital.",
    "As entregas foram além de posts: incluíram convite físico e digital, página de confirmação, textos comerciais, roteiros, listas, suporte de evento, captação de foto, vídeo e drone, carrosséis, stories, apoio técnico e materiais estratégicos.",
    "O mês também consolidou uma linha editorial mais madura para o ciclo seguinte, conectando inauguração, eventos proprietários, autoridade institucional, empreendimentos, materiais de apoio para reuniões comerciais e implementação de workspace no ChatGPT.",
]

fronts = [
    ("Inauguração B. Living", "Convite, página de RSVP, dashboard, textos de disparo, checklist, discurso, lista de convidados, vídeo final e materiais pós-evento."),
    ("Captação audiovisual", "Foto, vídeo e drone nos eventos Casa Dimas e Cacupé - GND; foto e vídeo na cobertura no João Paulo e no Pátio Milano."),
    ("Conteúdo e redes sociais", "Grid aprovado, post institucional aprovado, stories, vídeos rápidos, carrossel Wine & Living e organização de próximos conteúdos."),
    ("Materiais comerciais", "Apresentações, copy, edição e criação da apresentação de resultados de vendas, roteiros, voice overs e PDF estratégico sobre Florianópolis."),
    ("Suporte técnico e operação", "Diagnóstico e relatório técnico de e-mail/domínio, webmail, restabelecimento dos e-mails, organização de ativos em Drive e Workspace no ChatGPT em andamento."),
]

deliveries = [
    ("Convite de inauguração", "PDF, imagens, versões ajustadas e arquivos de apoio para impressão/divulgação.", "Entregue"),
    ("Convite virtual / RSVP", "Landing page, link final, domínio da marca, dashboard interno e textos de envio.", "Entregue"),
    ("Textos de disparo", "Copies para clientes, parceiros e convite institucional com CTA de confirmação.", "Entregue"),
    ("Checklist de inauguração", "Estrutura operacional de som, iluminação, recepção, equipe, produção e contingências.", "Entregue"),
    ("Roteiros e discurso", "Voice over Rafael, roteiros B. Living, discurso e estrutura de fala para a inauguração.", "Entregue"),
    ("Listas de convidados", "Guest list e lista de confirmados, com consolidação aproximada de 115 confirmações.", "Entregue"),
    ("Vídeo da inauguração", "Versões, prévias, refinamentos de trilha/imagens/legendas e entrega final em 30/04.", "Entregue"),
    ("Captação Casa Dimas", "Captação de foto, vídeo e drone no evento Casa Dimas.", "Entregue"),
    ("Captação Cacupé - GND", "Captação de foto, vídeo e drone no evento Cacupé - GND.", "Entregue"),
    ("Cobertura João Paulo", "Captação de foto e vídeo de cobertura no João Paulo.", "Entregue"),
    ("Pátio Milano", "Captação de foto e vídeo no Pátio Milano, com entrega por iCloud e WeTransfer.", "Entregue"),
    ("Material institucional Rafael", "Captação de vídeo para material institucional do Rafael.", "Entregue"),
    ("Grid de feed", "Três divisões para posts fixados, aprovadas por Rafael.", "Entregue e aprovado"),
    ("Post Frente Parlamentar / REURB", "Sequência de imagens, legenda institucional e ajuste de marcações.", "Entregue e aprovado"),
    ("Wine & Living / Casa Dimas", "Convite, lembrete, Drive, carrossel, legenda estratégica e vídeos de apoio.", "Entregue"),
    ("Stories e vídeos rápidos", "Conteúdo do dia, Casa Dimas e materiais publicados em stories.", "Publicado"),
    ("Material estratégico Florianópolis", "PDF de 16 páginas com narrativa de território, escassez, infraestrutura e futuro.", "Base entregue"),
    ("Apresentação resultados de vendas", "Copy, edição e criação da apresentação de resultados de vendas usada no evento de inauguração.", "Entregue"),
    ("E-mail e domínio", "Relatório técnico de incidente e restabelecimento dos e-mails.", "Resolvido"),
    ("Workspace no ChatGPT", "Implementação de Workspace no ChatGPT para organização e uso operacional da B. Living.", "Em andamento"),
]

timeline = [
    ("01/04", "Convite de inauguração em PDF/imagens, link do convite virtual, dashboard e ajustes de arte."),
    ("02/04", "Textos de disparo para clientes/parceiros e CTA para confirmação de presença."),
    ("06-09/04", "Orçamento gráfico, voice over, roteiros, checklist, discurso e materiais de inauguração."),
    ("10-14/04", "Primeiros materiais pós-evento, contratos/fornecedores, grid de feed e convite Casa Dimas."),
    ("15-17/04", "Post institucional aprovado, lembrete Wine & Living, relatório técnico e e-mails restabelecidos."),
    ("20-24/04", "Vídeos da inauguração, carrossel Wine & Living, lista de confirmados, voice overs, stories e captações de eventos."),
    ("29-30/04", "Prévia avançada e entrega final do vídeo da inauguração, PDF estratégico, Pátio Milano e Workspace no ChatGPT em andamento."),
]

next_steps = [
    ("Max Studios / Empreende Brasil", "Transformar o material recebido em uma apresentação mais forte e orientada à venda."),
    ("Mercado imobiliário vs. mercado financeiro", "Definir cronograma, estrutura narrativa e formato visual da apresentação."),
    ("História da ilha", "Converter a base estratégica já entregue em apresentação oficial visual, com mapas, dados e imagens."),
    ("Circuito imobiliário", "Organizar construtoras e empreendimentos em mapa da ilha para uso comercial."),
    ("Calendário editorial", "Estruturar agenda semanal com mais equilíbrio entre eventos, autoridade e empreendimentos."),
    ("Workspace no ChatGPT", "Concluir implementação, organizar bases de conhecimento, documentos, prompts e fluxos de uso do time."),
]


def build_story():
    flow = []
    flow.extend(cover_story())
    flow.append(section("Visão Executiva"))
    flow.extend([p(item) for item in executive_points])
    flow.append(Spacer(1, 6 * mm))
    flow.append(subsection("Frentes de trabalho"))
    flow.append(simple_table(["Frente", "Valor entregue"], fronts, [46 * mm, 128 * mm]))
    flow.append(Spacer(1, 5 * mm))
    flow.append(
        p(
            "Metodologia: este relatório consolida registros de conversas, arquivos compartilhados e materiais encontrados no ciclo de abril. "
            "A leitura foi adaptada para apresentação executiva ao cliente, agrupando evidências por entrega e por frente de trabalho.",
            "Small",
        )
    )

    flow.append(PageBreak())
    flow.append(section("Entregas Consolidadas"))
    flow.append(
        p(
            "A tabela abaixo resume as principais entregas realizadas no mês, com uma descrição objetiva do que foi disponibilizado e o status registrado no ciclo.",
        )
    )
    flow.append(simple_table(["Entrega", "Descrição", "Status"], deliveries, [42 * mm, 96 * mm, 36 * mm]))

    flow.append(PageBreak())
    flow.append(section("Destaques do Mês"))
    highlights = [
        (
            "Lançamento e inauguração",
            [
                "Desenvolvimento do convite físico e digital, incluindo versões ajustadas, textos de disparo e CTA de confirmação.",
                "Estruturação de página de RSVP, domínio da marca e dashboard interno de acompanhamento.",
                "Checklist operacional, listas de convidados, discurso e materiais de apoio para o evento.",
            ],
        ),
        (
            "Conteúdo e autoridade",
            [
                "Entrega de grid de feed aprovado e post institucional aprovado sobre Frente Parlamentar / REURB.",
                "Produção de carrossel Wine & Living com legenda estratégica, voltado a reforçar posicionamento e percepção de valor.",
                "Vídeos, stories e materiais rápidos para sustentar presença digital ao longo do mês.",
            ],
        ),
        (
            "Captação audiovisual",
            [
                "Captação de foto, vídeo e drone no evento Casa Dimas.",
                "Captação de foto, vídeo e drone no evento Cacupé - GND.",
                "Captação de foto e vídeo na cobertura no João Paulo e no Pátio Milano.",
                "Captação de vídeo para material institucional do Rafael.",
            ],
        ),
        (
            "Materiais comerciais e estratégia",
            [
                "Entrega de roteiros e voice overs para Rafael, incluindo estrutura de fala para inauguração.",
                "Copy, edição e criação da apresentação de resultados de vendas usada no evento de inauguração.",
                "Desenvolvimento de material estratégico sobre Florianópolis e B. Living, com narrativa de passado, presente e futuro.",
                "Organização de próximos passos editoriais para conectar inauguração, Casa Dimas, cortes institucionais e empreendimentos.",
            ],
        ),
        (
            "Operação e suporte",
            [
                "Acompanhamento de fornecedores, contratos, orçamentos e comprovantes ligados aos eventos.",
                "Diagnóstico técnico de e-mail/domínio, relatório de incidente e restabelecimento dos e-mails.",
                "Organização e envio de fotos/vídeos por Drive, iCloud e WeTransfer conforme demanda dos corretores.",
                "Implementação de Workspace no ChatGPT em andamento para organizar bases, prompts e fluxos de uso.",
            ],
        ),
    ]
    for title, items in highlights:
        flow.append(KeepTogether([subsection(title), bullet(items), Spacer(1, 3 * mm)]))

    flow.append(PageBreak())
    flow.append(
        KeepTogether(
            [
                section("Linha do Tempo"),
                simple_table(["Período", "Principais entregas"], timeline, [25 * mm, 149 * mm]),
            ]
        )
    )
    flow.append(Spacer(1, 7 * mm))
    flow.append(section("Próximas Frentes Recomendadas"))
    flow.append(
        p(
            "Além do que foi entregue em abril, algumas demandas ficaram mapeadas para continuidade. A recomendação é tratá-las como pauta estruturada do próximo ciclo, com escopo, prazo e prioridade definidos."
        )
    )
    flow.append(simple_table(["Frente", "Encaminhamento sugerido"], next_steps, [48 * mm, 126 * mm]))
    flow.append(Spacer(1, 7 * mm))
    flow.append(section("Conclusão"))
    flow.append(
        p(
            "Abril consolidou a B. Living em uma fase de presença ativa: inauguração, relacionamento, conteúdo, suporte comercial e organização institucional. "
            "O volume de entregas mostra um mês de implantação, com foco em sustentar o lançamento da marca e preparar materiais que ampliam autoridade nas próximas reuniões e campanhas."
        )
    )
    flow.append(
        p(
            "Para o próximo ciclo, o maior ganho está em transformar as frentes já iniciadas em um sistema recorrente: calendário editorial, materiais comerciais visuais, vídeos institucionais e apoio direto aos empreendimentos estratégicos."
        )
    )
    return flow


def main():
    doc = ClientReport(str(PDF_PATH))
    story = build_story()
    doc.build(story)
    print(PDF_PATH)


if __name__ == "__main__":
    main()
