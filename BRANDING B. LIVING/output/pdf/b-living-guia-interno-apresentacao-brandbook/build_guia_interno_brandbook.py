from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import fitz
from PIL import Image as PILImage
from PIL import ImageDraw
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path.cwd()
OUT_DIR = ROOT / "output" / "pdf" / "b-living-guia-interno-apresentacao-brandbook"
TMP_DIR = ROOT / "tmp" / "pdfs" / "b-living-guia-interno-apresentacao-brandbook"

COPY_PATH = ROOT / "brandbook-toolkit" / "01-Brandbook" / "brandbook-b-living-editorial-copy.md"
ARCH_PATH = ROOT / "brandbook-toolkit" / "01-Brandbook" / "brandbook-b-living-arquitetura-editorial.md"
MASTER_PATH = ROOT / "brandbook-toolkit" / "01-Brandbook" / "brandbook-b-living-master.md"
DESIGN_PATH = ROOT / "DESIGN.md"
INDEX_PATH = (
    ROOT
    / "brandbook-toolkit"
    / "01-Brandbook"
    / "paginas-curadas"
    / "00-controle"
    / "INDICE-PAGINAS-CURADAS.md"
)

MD_OUT = OUT_DIR / "B-Living-Guia-Interno-Apresentacao-Brandbook.md"
PDF_OUT = OUT_DIR / "B-Living-Guia-Interno-Apresentacao-Brandbook.pdf"
PREVIEW_OUT = OUT_DIR / "preview-guia-interno-contact-sheet.png"


@dataclass
class PageEntry:
    number: int
    title: str
    chapter_num: int
    chapter_title: str
    chapter_objective: str = ""
    sections: Dict[str, str] = field(default_factory=dict)
    arch_function: str = ""
    arch_visual: str = ""
    selected_visual: bool = False


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def clean_md(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = text.replace(">", "")
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def first_words(text: str, limit: int = 34) -> str:
    text = clean_md(text)
    if not text:
        return ""
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(" ,.;:") + "..."


def extract_section(block: str, name: str) -> str:
    pattern = re.compile(
        rf"^### {re.escape(name)}\s*$([\s\S]*?)(?=^### |\Z)",
        flags=re.MULTILINE,
    )
    match = pattern.search(block)
    return match.group(1).strip() if match else ""


def parse_architecture(text: str) -> Dict[int, Dict[str, str]]:
    pages: Dict[int, Dict[str, str]] = {}
    for raw in text.splitlines():
        match = re.match(r"^\|\s*(\d{1,3})\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", raw)
        if not match:
            continue
        num = int(match.group(1))
        if 1 <= num <= 104:
            pages[num] = {
                "title": clean_md(match.group(2)),
                "function": clean_md(match.group(3)),
                "visual": clean_md(match.group(4)),
            }
    return pages


def parse_selected_pages(text: str) -> set[int]:
    selected: set[int] = set()
    for raw in text.splitlines():
        match = re.match(r"^\|\s*(\d{1,3})\s*\|", raw)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 104:
                selected.add(num)
    return selected


def parse_copy(text: str, arch: Dict[int, Dict[str, str]], selected: set[int]) -> List[PageEntry]:
    entries: List[PageEntry] = []
    current_chapter_num = 0
    current_chapter_title = ""
    chapter_objective = ""
    pending_objective = False
    current_page: Optional[PageEntry] = None
    page_lines: List[str] = []

    def flush_page() -> None:
        nonlocal current_page, page_lines
        if not current_page:
            return
        block = "\n".join(page_lines).strip()
        sections: Dict[str, str] = {}
        for match in re.finditer(r"^### ([^\n]+)\n([\s\S]*?)(?=^### |\Z)", block, flags=re.MULTILINE):
            sections[clean_md(match.group(1))] = match.group(2).strip()
        current_page.sections = sections
        current_page.chapter_objective = chapter_objective
        if current_page.number in arch:
            current_page.arch_function = arch[current_page.number].get("function", "")
            current_page.arch_visual = arch[current_page.number].get("visual", "")
        current_page.selected_visual = current_page.number in selected
        entries.append(current_page)
        current_page = None
        page_lines = []

    for line in text.splitlines():
        chapter_match = re.match(r"^# Capitulo\s+(\d+)\s+-\s+(.+)$", line)
        page_match = re.match(r"^## Pagina\s+(\d{1,3})\s+-\s+(.+)$", line)

        if chapter_match:
            flush_page()
            current_chapter_num = int(chapter_match.group(1))
            current_chapter_title = clean_md(chapter_match.group(2))
            chapter_objective = ""
            pending_objective = False
            continue

        if line.startswith("Objetivo do capitulo:"):
            chapter_objective = clean_md(line.replace("Objetivo do capitulo:", "", 1))
            pending_objective = False
            continue

        if line.strip() == "## Objetivo do capitulo":
            pending_objective = True
            chapter_objective = ""
            continue

        if pending_objective and not page_match and not line.startswith("#"):
            if line.strip():
                chapter_objective = clean_md((chapter_objective + " " + line.strip()).strip())
            continue

        if page_match:
            flush_page()
            pending_objective = False
            num = int(page_match.group(1))
            current_page = PageEntry(
                number=num,
                title=clean_md(page_match.group(2)),
                chapter_num=current_chapter_num,
                chapter_title=current_chapter_title,
            )
            page_lines = []
            continue

        if current_page:
            page_lines.append(line)

    flush_page()
    return sorted(entries, key=lambda item: item.number)


def chapter_decision(chapter_num: int) -> str:
    decisions = {
        1: "abrir a reunião mostrando que o brandbook é uma construção estratégica, não uma coleção de peças bonitas",
        2: "provar que o desafio real era percepção, codificação de autoridade e clareza de valor",
        3: "mostrar cedo que a estratégia já ganhou atmosfera visual, sem cair em luxo óbvio",
        4: "transformar o diagnóstico em plataforma de marca defensável e aplicável",
        5: "demonstrar que a promessa da marca precisa aparecer na experiência, não apenas no discurso",
        6: "proteger a percepção da marca pela linguagem, pelo vocabulário e pela forma de conduzir",
        7: "converter o conceito visual em regras repetíveis para equipe, designers e fornecedores",
        8: "reposicionar os canais sociais como plataforma de autoridade, prova e relacionamento",
        9: "tirar o brandbook do plano conceitual e mostrar como ele vira material comercial, atendimento e presença",
        10: "garantir continuidade, aprovação correta e evolução sem descaracterizar a marca",
    }
    return decisions.get(chapter_num, "manter a narrativa do brandbook conectada ao posicionamento")


def page_status(entry: PageEntry) -> str:
    if entry.selected_visual:
        return "Página já curada visualmente na sequência selecionada do brandbook."
    return "Página prevista na arquitetura completa e explicada a partir da copy editorial."


def page_title(entry: PageEntry) -> str:
    principal = clean_md(entry.sections.get("Titulo principal", ""))
    if principal and principal.lower() != entry.title.lower():
        return principal
    return entry.title


def what_it_shows(entry: PageEntry) -> str:
    principal = page_title(entry)
    support = first_words(entry.sections.get("Texto de apoio", ""), 28)
    if support:
        return f"Mostra a ideia '{principal}' e usa o apoio textual para enquadrar: {support}"
    if entry.arch_function:
        return f"Mostra a ideia '{principal}' com a função de {entry.arch_function.lower()}."
    return f"Mostra a ideia '{principal}' dentro da narrativa do capítulo."


def why_it_exists(entry: PageEntry) -> str:
    function = entry.arch_function or "organizar a passagem narrativa desta etapa"
    return (
        f"Existe para {function.lower()} e impedir que a apresentação seja lida como uma sequência solta. "
        f"Ela amarra esta etapa à decisão de {chapter_decision(entry.chapter_num)}."
    )


def how_built(entry: PageEntry) -> str:
    visual = entry.arch_visual or clean_md(entry.sections.get("Orientacao visual", ""))
    if visual:
        return (
            f"Foi construída com direção de {first_words(visual, 28)}. "
            "A forma visual deve sustentar a tese antes de decorar a página."
        )
    return (
        "Foi construída como página de transição estratégica, com hierarquia clara, texto controlado e foco na decisão que precisa ser defendida."
    )


def strategic_decision(entry: PageEntry) -> str:
    phrase = clean_md(entry.sections.get("Frase final", ""))
    if phrase:
        return f"A decisão é usar esta página para fixar a lógica: {first_words(phrase, 24)}"
    return f"A decisão é reforçar que a B. Living deve ser percebida por critério, leitura e confiança antes de produto."


def speaker_note(entry: PageEntry) -> str:
    title = page_title(entry)
    function = entry.arch_function.lower() if entry.arch_function else "organizar esta parte da narrativa"
    return (
        f"Fala sugerida: 'Nesta página, eu mostro {title.lower()}. "
        f"O ponto não é só apresentar uma informação: é deixar claro que {function} faz parte da construção de marca. "
        f"Por isso, esta escolha precisa ser lida como estratégia antes de ser lida como estética.'"
    )


def bridge_note(entry: PageEntry, next_entry: Optional[PageEntry]) -> str:
    if not next_entry:
        return "Ponte: fechar dizendo que o brandbook termina como sistema vivo, pronto para orientar aplicação, aprovação e evolução."
    if next_entry.chapter_num != entry.chapter_num:
        return (
            f"Ponte: depois desta página, a apresentação muda para o capítulo {next_entry.chapter_num}, "
            f"'{next_entry.chapter_title}', mostrando o próximo nível da construção."
        )
    return f"Ponte: a próxima página aprofunda essa lógica em '{next_entry.title}'."


def portuguese_cleanup(text: str) -> str:
    replacements = {
        r"\bnao\b": "não",
        r"\bNao\b": "Não",
        r"\bso\b": "só",
        r"\bSo\b": "Só",
        r"\bpagina\b": "página",
        r"\bPagina\b": "Página",
        r"\bpaginas\b": "páginas",
        r"\bPaginas\b": "Páginas",
        r"\bfuncao\b": "função",
        r"\bFuncao\b": "Função",
        r"\bfuncoes\b": "funções",
        r"\bdecisao\b": "decisão",
        r"\bDecisao\b": "Decisão",
        r"\bdecisoes\b": "decisões",
        r"\bDecisoes\b": "Decisões",
        r"\bimovel\b": "imóvel",
        r"\bImovel\b": "Imóvel",
        r"\bimoveis\b": "imóveis",
        r"\bImoveis\b": "Imóveis",
        r"\bpercepcao\b": "percepção",
        r"\bPercepcao\b": "Percepção",
        r"\bpercepcoes\b": "percepções",
        r"\bestrategia\b": "estratégia",
        r"\bEstrategia\b": "Estratégia",
        r"\bestrategico\b": "estratégico",
        r"\bEstrategico\b": "Estratégico",
        r"\bestrategica\b": "estratégica",
        r"\bEstrategica\b": "Estratégica",
        r"\bestrategicas\b": "estratégicas",
        r"\bconstrucao\b": "construção",
        r"\bConstrucao\b": "Construção",
        r"\bcodificacao\b": "codificação",
        r"\bCodificacao\b": "Codificação",
        r"\bcriterio\b": "critério",
        r"\bCriterio\b": "Critério",
        r"\bcriterios\b": "critérios",
        r"\bconfianca\b": "confiança",
        r"\bConfianca\b": "Confiança",
        r"\bexperiencia\b": "experiência",
        r"\bExperiencia\b": "Experiência",
        r"\bexperiencias\b": "experiências",
        r"\bmetodo\b": "método",
        r"\bMetodo\b": "Método",
        r"\bFlorianopolis\b": "Florianópolis",
        r"\bterritorio\b": "território",
        r"\bTerritorio\b": "Território",
        r"\bessencia\b": "essência",
        r"\bEssencia\b": "Essência",
        r"\bimobiliaria\b": "imobiliária",
        r"\bImobiliaria\b": "Imobiliária",
        r"\bimobiliarias\b": "imobiliárias",
        r"\bimobiliario\b": "imobiliário",
        r"\bimobiliarios\b": "imobiliários",
        r"\bpadrao\b": "padrão",
        r"\bPadrao\b": "Padrão",
        r"\baplicacao\b": "aplicação",
        r"\bAplicacao\b": "Aplicação",
        r"\baplicacoes\b": "aplicações",
        r"\bAplicacoes\b": "Aplicações",
        r"\baprovacao\b": "aprovação",
        r"\bAprovacao\b": "Aprovação",
        r"\bgovernanca\b": "governança",
        r"\bGovernanca\b": "Governança",
        r"\bapresentacao\b": "apresentação",
        r"\bApresentacao\b": "Apresentação",
        r"\breuniao\b": "reunião",
        r"\bReuniao\b": "Reunião",
        r"\bselecao\b": "seleção",
        r"\borientacao\b": "orientação",
        r"\bOrientacao\b": "Orientação",
        r"\bconducao\b": "condução",
        r"\bConducao\b": "Condução",
        r"\boperacao\b": "operação",
        r"\bOperacao\b": "Operação",
        r"\blideranca\b": "liderança",
        r"\bvisao\b": "visão",
        r"\brelacao\b": "relação",
        r"\bcomunicacao\b": "comunicação",
        r"\bComunicacao\b": "Comunicação",
        r"\bsintese\b": "síntese",
        r"\bSintese\b": "Síntese",
        r"\bdiagnostico\b": "diagnóstico",
        r"\bDiagnostico\b": "Diagnóstico",
        r"\bestetica\b": "estética",
        r"\bEstetica\b": "Estética",
        r"\bobvio\b": "óbvio",
        r"\bóbvia\b": "óbvia",
        r"\bhistorico\b": "histórico",
        r"\bfamilia\b": "família",
        r"\bpatrimonio\b": "patrimônio",
        r"\banalitico\b": "analítico",
        r"\banalitica\b": "analítica",
        r"\btecnico\b": "técnico",
        r"\blegivel\b": "legível",
        r"\bpossivel\b": "possível",
        r"\bnecessario\b": "necessário",
        r"\bsensiveis\b": "sensíveis",
        r"\bpratica\b": "prática",
        r"\bPratica\b": "Prática",
        r"\bpraticos\b": "práticos",
        r"\bdirecao\b": "direção",
        r"\bDirecao\b": "Direção",
        r"\bopcoes\b": "opções",
        r"\bopcao\b": "opção",
        r"\bavaliacao\b": "avaliação",
        r"\bindicacao\b": "indicação",
        r"\bpos-venda\b": "pós-venda",
        r"\bultimas\b": "últimas",
        r"\bunica\b": "única",
        r"\bdossie\b": "dossiê",
        r"\bDossie\b": "Dossiê",
        r"\bconteudo\b": "conteúdo",
        r"\bConteudo\b": "Conteúdo",
        r"\bconteudos\b": "conteúdos",
        r"\bmensuracao\b": "mensuração",
        r"\bmetricas\b": "métricas",
        r"\bMetricas\b": "Métricas",
        r"\bnumeros\b": "números",
        r"\btitulo\b": "título",
        r"\bTitulo\b": "Título",
        r"\bproximos\b": "próximos",
        r"\bProximos\b": "Próximos",
        r"\bproximo\b": "próximo",
    }
    for pattern, value in replacements.items():
        text = re.sub(pattern, value, text)
    return text


def md_escape(text: str) -> str:
    return text.replace("\u2011", "-")


def build_markdown(entries: List[PageEntry]) -> str:
    lines: List[str] = []
    lines.extend(
        [
            "# Guia Interno de Apresentação do Brandbook B. Living",
            "",
            "Material de apoio interno para conduzir a apresentação do brandbook completo de 104 páginas.",
            "",
            "Este documento não substitui o brandbook. Ele funciona como roteiro de preparação: explica a lógica de construção, a função de cada página, a decisão por trás das escolhas e a fala sugerida para apresentar ao cliente.",
            "",
            "## Como usar este guia",
            "",
            "- Use como roteiro de bastidor antes e durante a apresentação.",
            "- Não leia todas as notas em voz alta. Use cada bloco para lembrar o motivo estratégico da página.",
            "- Mantenha a narrativa principal: o projeto começa no pedido visual, revela um problema de percepção, organiza a autoridade real da B. Living e transforma isso em sistema verbal, visual e operacional.",
            "- Quando houver dúvida, volte aos critérios: decisão antes do imóvel, Rafael e equipe antes do produto, curadoria antes de vitrine, Florianópolis como território e visual como consequência da tese.",
            "",
            "## Síntese estratégica para abrir a reunião",
            "",
            "**Pedido declarado.** Organizar Instagram, destaques, linguagem e percepção visual da B. Living.",
            "",
            "**Problema real.** A marca entregava mais valor do que comunicava. O desafio era transformar autoridade, experiência e método em percepção clara.",
            "",
            "**Tese diagnóstica.** A B. Living não precisava inventar sofisticação. Precisava codificar a sofisticação que já existia em Rafael, equipe, preparo, leitura de Florianópolis, relacionamento com construtoras e condução comercial.",
            "",
            "**Ideia central.** Antes do imóvel, vem a decisão.",
            "",
            "**Posicionamento.** Curadoria imobiliária de alto padrão que orienta decisões com critério, leitura de mercado e confiança.",
            "",
            "**Essência.** Escolha bem conduzida.",
            "",
            "**Conceito visual.** Quiet authority: sobriedade, profundidade, editorialidade e alto padrão sem ostentação.",
            "",
            "## Mapa rápido dos capítulos",
            "",
        ]
    )

    chapters: Dict[int, List[PageEntry]] = {}
    for entry in entries:
        chapters.setdefault(entry.chapter_num, []).append(entry)

    for chapter_num, chapter_entries in chapters.items():
        first = chapter_entries[0].number
        last = chapter_entries[-1].number
        lines.append(
            f"- Capítulo {chapter_num}: {chapter_entries[0].chapter_title} - páginas {first:03d} a {last:03d}. Função: {chapter_decision(chapter_num)}."
        )
    lines.append("")

    for chapter_num, chapter_entries in chapters.items():
        chapter_title = chapter_entries[0].chapter_title
        objective = chapter_entries[0].chapter_objective
        lines.append(f"## Capítulo {chapter_num} - {chapter_title}")
        lines.append("")
        if objective:
            lines.append(f"**Objetivo do capítulo.** {objective}")
            lines.append("")
        lines.append(f"**Decisão de apresentação.** Este bloco serve para {chapter_decision(chapter_num)}.")
        lines.append("")

        for idx, entry in enumerate(chapter_entries):
            next_entry = entries[entries.index(entry) + 1] if entries.index(entry) + 1 < len(entries) else None
            lines.append(f"### Página {entry.number:03d} - {entry.title}")
            lines.append("")
            lines.append(f"**Status.** {page_status(entry)}")
            lines.append("")
            lines.append(f"**O que a página mostra.** {what_it_shows(entry)}")
            lines.append("")
            lines.append(f"**Função na narrativa.** {entry.arch_function or 'Organizar a continuidade da apresentação.'}")
            lines.append("")
            lines.append(f"**Por que existe.** {why_it_exists(entry)}")
            lines.append("")
            lines.append(f"**Como foi construída.** {how_built(entry)}")
            lines.append("")
            lines.append(f"**Decisão estratégica.** {strategic_decision(entry)}")
            lines.append("")
            lines.append(f"**Como apresentar.** {speaker_note(entry)}")
            lines.append("")
            lines.append(f"**Ponte para a próxima página.** {bridge_note(entry, next_entry)}")
            lines.append("")

    lines.extend(
        [
            "## Fechamento da apresentação",
            "",
            "Ao encerrar, retome que o brandbook não é um arquivo estático. Ele é uma ferramenta para decidir, aprovar, comunicar e proteger a marca.",
            "",
            "A mensagem final para sustentar é simples: a B. Living já tinha substância. O projeto organizou essa substância em narrativa, experiência, linguagem, visual e aplicação.",
            "",
            "## Objeções prováveis e respostas de condução",
            "",
            "**Se o cliente disser que ficou muito estratégico:** explique que isso é intencional. A estética só sustenta valor quando nasce de uma tese clara.",
            "",
            "**Se o cliente pedir mais imóveis nas primeiras páginas:** explique que o imóvel aparece como consequência. Antes dele, a marca precisa provar critério, autoridade e confiança.",
            "",
            "**Se houver dúvida sobre o tom sóbrio:** explique que alto padrão aqui não é brilho ou ostentação. É profundidade, silêncio, precisão e segurança.",
            "",
            "**Se a equipe quiser usar o brandbook como manual operacional:** direcione para os checklists finais de estratégia, visual, linguagem, governança e próximos passos.",
            "",
            "## Próximos passos para apresentar",
            "",
            "1. Validar a narrativa central com Rafael.",
            "2. Usar o brandbook como referência de aprovação para Instagram, WhatsApp, apresentações, proposta, eventos e fornecedores.",
            "3. Transformar os capítulos finais em toolkit aplicado: templates, modelos de atendimento, dossiês, posts, destaques e materiais comerciais.",
            "4. Medir se a percepção da marca está migrando de imobiliária-vitrine para curadoria imobiliária de alto padrão.",
            "",
        ]
    )
    return portuguese_cleanup(md_escape("\n".join(lines)))


def pdf_styles():
    base = getSampleStyleSheet()
    navy = colors.HexColor("#102033")
    brass = colors.HexColor("#9E8755")
    paper = colors.HexColor("#F3EEE2")

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="Times-Roman",
            fontSize=28,
            leading=33,
            alignment=TA_CENTER,
            textColor=paper,
            spaceAfter=16,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=17,
            alignment=TA_CENTER,
            textColor=paper,
            spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Times-Roman",
            fontSize=20,
            leading=24,
            textColor=navy,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Times-Roman",
            fontSize=16,
            leading=20,
            textColor=navy,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=navy,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=12.4,
            textColor=colors.HexColor("#202833"),
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.7,
            leading=10.5,
            textColor=colors.HexColor("#354052"),
            spaceAfter=3,
        ),
        "label": ParagraphStyle(
            "label",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9,
            textColor=brass,
            spaceAfter=2,
        ),
    }
    return styles, navy, brass, paper


def escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


def make_para(text: str, style: ParagraphStyle) -> Paragraph:
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = escape_xml(text)
    text = text.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    return Paragraph(text, style)


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#58606C"))
    canvas.drawString(1.5 * cm, 0.8 * cm, "Guia interno - Brandbook B. Living")
    canvas.drawRightString(A4[0] - 1.5 * cm, 0.8 * cm, f"Página {doc.page}")
    canvas.restoreState()


def add_cover(story: List, styles, navy, paper):
    data = [[make_para("Guia Interno de Apresentação do Brandbook B. Living", styles["cover_title"])]]
    cover = Table(data, colWidths=[17.0 * cm], rowHeights=[20.5 * cm])
    cover.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), navy),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 1.2 * cm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1.2 * cm),
                ("TOPPADDING", (0, 0), (-1, -1), 1.2 * cm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2 * cm),
            ]
        )
    )
    story.append(cover)
    story.append(PageBreak())


def build_pdf(markdown: str, pdf_path: Path) -> None:
    styles, navy, brass, paper = pdf_styles()
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=1.45 * cm,
        leftMargin=1.45 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.35 * cm,
        title="Guia Interno de Apresentação do Brandbook B. Living",
        author="A Última Ideia",
    )
    story: List = []
    add_cover(story, styles, navy, paper)

    lines = markdown.splitlines()
    in_pages = False
    bullet_buffer: List[str] = []

    def flush_bullets():
        nonlocal bullet_buffer
        if not bullet_buffer:
            return
        for bullet in bullet_buffer:
            story.append(make_para("• " + bullet, styles["small"]))
        bullet_buffer = []

    for raw in lines[1:]:
        line = raw.strip()
        if not line:
            flush_bullets()
            story.append(Spacer(1, 0.07 * cm))
            continue

        if line.startswith("## Capítulo "):
            flush_bullets()
            if in_pages:
                story.append(PageBreak())
            in_pages = True
            story.append(make_para(line.replace("## ", ""), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.7, color=brass, spaceAfter=0.18 * cm))
            continue

        if line.startswith("# "):
            flush_bullets()
            story.append(make_para(line.replace("# ", ""), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.7, color=brass, spaceAfter=0.18 * cm))
            continue

        if line.startswith("## "):
            flush_bullets()
            story.append(make_para(line.replace("## ", ""), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.6, color=brass, spaceAfter=0.16 * cm))
            continue

        if line.startswith("### Página "):
            flush_bullets()
            story.append(Spacer(1, 0.08 * cm))
            story.append(make_para(line.replace("### ", ""), styles["h2"]))
            continue

        if line.startswith("- "):
            bullet_buffer.append(line[2:])
            continue

        if re.match(r"^\d+\.\s+", line):
            bullet_buffer.append(line)
            continue

        flush_bullets()
        style = styles["body"]
        if line.startswith("**") and ".**" in line[:40]:
            style = styles["small"]
        story.append(make_para(line, style))

    flush_bullets()
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


def render_preview(pdf_path: Path, preview_path: Path) -> None:
    doc = fitz.open(str(pdf_path))
    pages = [0, 1, 2, 3, max(0, len(doc) - 1)]
    thumbs: List[PILImage.Image] = []
    for pageno in pages:
        page = doc[pageno]
        pix = page.get_pixmap(matrix=fitz.Matrix(0.70, 0.70), alpha=False)
        image = PILImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_path = OUT_DIR / f"preview-page-{pageno + 1:03d}.png"
        image.save(image_path)
        thumbs.append(image)

    thumb_w = max(p.width for p in thumbs)
    thumb_h = max(p.height for p in thumbs)
    margin = 24
    cols = 3
    rows = 2
    width = cols * thumb_w + (cols + 1) * margin
    height = rows * thumb_h + (rows + 1) * margin

    sheet = PILImage.new("RGB", (width, height), (238, 238, 238))
    draw = ImageDraw.Draw(sheet)
    for idx, image in enumerate(thumbs):
        col = idx % cols
        row = idx // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + margin)
        sheet.paste(image, (x, y))
        draw.rectangle([x, y, x + image.width, y + image.height], outline=(180, 180, 180), width=2)
        draw.text((x + 10, y + 10), f"PDF page {pages[idx] + 1}", fill=(90, 90, 90))
    sheet.save(preview_path)
    doc.close()


def validate(entries: List[PageEntry], markdown: str, pdf_path: Path) -> Dict[str, object]:
    reader = PdfReader(str(pdf_path))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    result = {
        "entry_count": len(entries),
        "missing_pages": [n for n in range(1, 105) if n not in {entry.number for entry in entries}],
        "has_ana_couto": bool(re.search(r"Ana\s+Couto", markdown + "\n" + text, flags=re.I)),
        "has_page_001": "Página 001" in markdown,
        "has_page_104": "Página 104" in markdown,
        "pdf_pages": len(reader.pages),
        "pdf_has_title": "Guia Interno de Apresentação" in text,
    }
    missing_required = []
    for entry in entries:
        block_match = re.search(
            rf"### Página {entry.number:03d}[\s\S]*?(?=### Página|\Z)",
            markdown,
        )
        block = block_match.group(0) if block_match else ""
        for label in [
            "O que a página mostra",
            "Função na narrativa",
            "Por que existe",
            "Como foi construída",
            "Decisão estratégica",
            "Como apresentar",
            "Ponte para a próxima página",
        ]:
            if label not in block:
                missing_required.append(f"{entry.number:03d}:{label}")
    result["missing_required_notes"] = missing_required
    return result


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    copy_text = read_text(COPY_PATH)
    arch_text = read_text(ARCH_PATH)
    selected_text = read_text(INDEX_PATH)

    arch = parse_architecture(arch_text)
    selected = parse_selected_pages(selected_text)
    entries = parse_copy(copy_text, arch, selected)

    markdown = build_markdown(entries)
    MD_OUT.write_text(markdown, encoding="utf-8")
    build_pdf(markdown, PDF_OUT)
    render_preview(PDF_OUT, PREVIEW_OUT)
    validation = validate(entries, markdown, PDF_OUT)

    validation_path = OUT_DIR / "validacao-guia-interno.txt"
    validation_path.write_text(
        "\n".join(f"{key}: {value}" for key, value in validation.items()),
        encoding="utf-8",
    )

    if validation["entry_count"] != 104:
        raise SystemExit(f"Expected 104 entries, got {validation['entry_count']}")
    if validation["missing_pages"]:
        raise SystemExit(f"Missing pages: {validation['missing_pages']}")
    if validation["has_ana_couto"]:
        raise SystemExit("Forbidden attribution found: Ana Couto")
    if validation["missing_required_notes"]:
        raise SystemExit(f"Missing required notes: {validation['missing_required_notes'][:10]}")

    print(f"MD: {MD_OUT}")
    print(f"PDF: {PDF_OUT}")
    print(f"PREVIEW: {PREVIEW_OUT}")
    print(f"VALIDATION: {validation_path}")
    print(validation)


if __name__ == "__main__":
    main()
