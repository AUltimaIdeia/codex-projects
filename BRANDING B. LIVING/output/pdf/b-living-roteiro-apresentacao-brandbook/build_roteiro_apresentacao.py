from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


OUT_DIR = Path(__file__).resolve().parent
PDF_PATH = OUT_DIR / "B-Living-Roteiro-Completo-Apresentacao-Brandbook.pdf"
MD_PATH = OUT_DIR / "B-Living-Roteiro-Completo-Apresentacao-Brandbook.md"


sections = [
    {
        "title": "Antes De Começar",
        "body": [
            "Este roteiro foi escrito para uma apresentação em que a B. Living é protagonista desde a primeira frase. A Última Ideia aparece como intérprete, organizadora e tradutora de uma força que já existia na operação.",
            "A condução deve ser segura, emocional na medida certa e sem parecer uma justificativa de esforço. O ponto não é dizer quanto trabalho deu. O ponto é mostrar que o trabalho precisava ser profundo porque a B. Living já tinha substância suficiente para merecer uma construção desse nível.",
        ],
        "talk": [
            "Antes de abrir o material, eu quero alinhar como esta apresentação deve ser lida. O que vocês vão ver aqui não é uma coleção de peças bonitas. É uma construção de marca.",
            "A B. Living não começa neste brandbook. Ela já existia na prática: na forma como Rafael conduz, na qualidade da equipe, na leitura de Florianópolis, na relação com construtoras, no preparo interno e na confiança construída com cada cliente.",
            "O que este trabalho faz é organizar essa força em linguagem, imagem, método e direção. Não estamos apresentando uma marca inventada. Estamos apresentando uma marca revelada.",
        ],
    },
    {
        "title": "Abertura Da Reunião",
        "body": [
            "Objetivo: criar clima, assumir o comando da reunião e posicionar o brandbook como uma virada estratégica para a B. Living.",
        ],
        "talk": [
            "A B. Living chegou até aqui com ativos muito fortes: liderança, equipe, relacionamento, repertório comercial, leitura de cidade, acesso a oportunidades e capacidade real de conduzir decisões importantes.",
            "Mas existia uma diferença entre aquilo que a operação entregava e aquilo que a marca comunicava. E essa diferença era o ponto mais importante do projeto.",
            "Quando começamos, o pedido parecia visual: organizar Instagram, destaques, comunicação, estética e percepção premium. Mas quanto mais a gente olhava para a B. Living, mais ficava claro que o desafio real não era deixar a marca mais bonita. Era fazer a marca ser percebida na mesma altura do valor que ela já entregava.",
            "Por isso, este brandbook não é um manual de estética. Ele é um sistema para que a B. Living seja entendida, aplicada e defendida com clareza.",
        ],
    },
    {
        "title": "Frase De Entrada No Brandbook",
        "body": [
            "Use esta fala imediatamente antes de abrir a primeira página do PDF ou antes de mostrar a capa.",
        ],
        "talk": [
            "Apresento a vocês a B. Living organizada como ela merece ser percebida: uma curadoria para decisões imobiliárias de alto padrão.",
        ],
    },
    {
        "title": "Capítulo 1 - Abertura Premium",
        "body": [
            "Páginas 001 a 006. Função: mostrar que o brandbook tem peso estratégico e estabelecer o norte da marca.",
        ],
        "talk": [
            "A abertura existe para colocar a B. Living em outro lugar de percepção. Ela não começa pelo imóvel, pela oferta ou pelo catálogo. Ela começa pela decisão.",
            "A frase 'curadoria para decisões imobiliárias de alto padrão' resume a virada principal: a B. Living não existe para mostrar mais opções. Ela existe para ajudar o cliente a entender melhor o que escolher, quando escolher e por que escolher.",
            "A ideia 'antes do imóvel, vem a decisão' é o centro do raciocínio. No alto padrão, a escolha não é só sobre planta, vista, metragem ou preço. É sobre cidade, patrimônio, momento de vida, liquidez, timing, construtora e futuro.",
            "Por isso, a essência da marca foi sintetizada em 'escolha bem conduzida'. Essa frase é curta, mas carrega o que a B. Living precisa sustentar em todos os pontos de contato.",
        ],
    },
    {
        "title": "Capítulo 2 - Diagnóstico E Desafio Real",
        "body": [
            "Páginas 007 a 016. Função: provar que o projeto resolveu um problema de percepção, não apenas de visual.",
        ],
        "talk": [
            "Aqui a gente volta ao ponto de partida. O pedido parecia visual. Mas o Instagram era só o sintoma mais visível.",
            "O problema real era percepção. A B. Living entregava mais valor do que comunicava. E quando uma marca entrega mais do que comunica, o mercado enxerga menos valor do que ela realmente tem.",
            "A B. Living não precisava inventar sofisticação. Ela precisava codificar a sofisticação que já existia na operação: Rafael como liderança, a equipe como inteligência em movimento, as construtoras como acesso, Florianópolis como território estratégico, os resultados como prova e a relação com o cliente como condução.",
            "A tese diagnóstica é simples: a B. Living não deve parecer uma imobiliária comum. Ela deve ser reconhecida como curadoria imobiliária de alto padrão.",
        ],
    },
    {
        "title": "Capítulo 3 - Virada Visual Inicial",
        "body": [
            "Páginas 017 a 026. Função: mostrar cedo a potência visual da nova marca e explicar o conceito de quiet authority.",
        ],
        "talk": [
            "Depois de estabelecer a estratégia, o brandbook mostra a virada visual. E essa virada não nasce de gosto pessoal. Ela nasce da tese.",
            "O conceito visual é quiet authority: autoridade silenciosa, sobriedade, profundidade, editorialidade e alto padrão sem ostentação.",
            "A B. Living não precisava parecer resort, clube náutico, construtora ou vitrine de luxo óbvio. Ela precisava parecer critério, confiança e leitura.",
            "Por isso o azul profundo ganha força como território. A tipografia ganha peso editorial. A fotografia deixa de ser decorativa e passa a mostrar cidade, equipe, arquitetura, atendimento e contexto.",
            "O visual aqui não é enfeite. É consequência da estratégia.",
        ],
    },
    {
        "title": "Capítulo 4 - Plataforma De Marca",
        "body": [
            "Páginas 027 a 040. Função: transformar o diagnóstico em posicionamento, promessa, essência, pilares e critérios de decisão.",
        ],
        "talk": [
            "Este é o núcleo estratégico do brandbook. Aqui a marca deixa de ser apenas percebida e passa a ser definida.",
            "O posicionamento coloca a B. Living como uma curadoria imobiliária que orienta decisões com critério, leitura de mercado e confiança.",
            "A proposta de valor é ajudar clientes de alto padrão a tomar decisões imobiliárias mais seguras e bem orientadas, conectando momento de vida, patrimônio, produto, cidade e timing.",
            "Os pilares existem para impedir que a comunicação fique genérica. Rafael aparece como autoridade. A equipe aparece como método em operação. A curadoria aparece como critério. Florianópolis aparece como território estratégico. O preparo aparece como cultura. A performance aparece como prova. E a humanidade aparece como condução.",
            "A partir daqui, qualquer peça, post, atendimento ou apresentação precisa responder a uma pergunta: isso ajuda a B. Living a ser percebida como curadoria ou faz a marca voltar a parecer uma imobiliária comum?",
        ],
    },
    {
        "title": "Capítulo 5 - Experiência E Jornada",
        "body": [
            "Páginas 041 a 050. Função: mostrar que a promessa da marca precisa aparecer na experiência real do cliente.",
        ],
        "talk": [
            "Uma marca só é forte quando a experiência confirma a promessa. Por isso, este capítulo mostra como a B. Living deve ser percebida em cada ponto de contato.",
            "A experiência precisa seguir alguns princípios: ler antes de oferecer, orientar antes de vender, selecionar com critério, transformar preparo em prova e continuar depois da compra.",
            "A jornada não começa quando o cliente pede um imóvel. Ela começa quando ele descobre a marca, observa Rafael, percebe a equipe, entende a leitura da cidade e sente confiança suficiente para conversar.",
            "Depois vêm o diagnóstico, a curadoria, a decisão, o fechamento, o pós-venda e a indicação. Em todos esses momentos, a B. Living precisa provar que conduz melhor, não apenas que tem boas opções.",
        ],
    },
    {
        "title": "Capítulo 6 - Identidade Verbal",
        "body": [
            "Páginas 051 a 060. Função: proteger a percepção da marca pela linguagem.",
        ],
        "talk": [
            "A linguagem é uma das formas mais rápidas de elevar ou derrubar a percepção de uma marca.",
            "A B. Living deve falar de forma consultiva, segura, sofisticada, analítica, próxima e humana. Ela não precisa gritar. Ela precisa conduzir.",
            "Por isso, o brandbook define palavras, frases, vocabulário, tom de voz e exemplos de comunicação para Rafael, equipe, imóveis, WhatsApp e chamadas comerciais.",
            "Também define o que evitar: termos como imperdível, luxo absoluto, sonho de consumo, últimas unidades, chame agora e qualquer promessa sem prova. Essas expressões colocam a marca no mesmo território de comunicação de todo mundo.",
            "A linguagem da B. Living precisa reforçar uma ideia: cada imóvel deve ser apresentado com tese, não como uma oferta solta.",
        ],
    },
    {
        "title": "Capítulo 7 - Identidade Visual Completa",
        "body": [
            "Páginas 061 a 076. Função: converter o conceito visual em regras repetíveis para equipe, designers e fornecedores.",
        ],
        "talk": [
            "Aqui o brandbook deixa de ser só estratégico e vira ferramenta prática.",
            "A identidade visual organiza logo principal, logo compacta, área de proteção, usos incorretos, paleta, tipografia, composição, fotografia, texturas, grafismos, posts, capas e apresentações.",
            "O ponto mais importante é que a identidade visual não deve ser usada como decoração. Ela deve proteger o território da marca.",
            "Toda aplicação precisa parecer B. Living: sóbria, editorial, precisa, criteriosa e premium sem ostentação.",
            "Esse capítulo também existe para dar independência à operação. Designers, social media, equipe interna e fornecedores passam a ter critério para aplicar a marca sem descaracterizá-la.",
        ],
    },
    {
        "title": "Capítulo 8 - Comunicação E Redes Sociais",
        "body": [
            "Páginas 077 a 086. Função: reposicionar Instagram e redes sociais como plataforma de autoridade, prova e relacionamento.",
        ],
        "talk": [
            "O Instagram da B. Living não deve ser um catálogo. Ele precisa ser uma jornada de confiança.",
            "Isso muda completamente a lógica de conteúdo. O imóvel continua importante, mas ele deixa de ser o começo da conversa. Antes dele vêm Rafael, equipe, cidade, leitura, método, prova e contexto.",
            "A linha editorial organiza os territórios principais: Rafael lê o mercado, equipe em método, Florianópolis em movimento, imóveis com tese, provas e resultados, construtoras, eventos e bastidores de preparo.",
            "Os destaques também deixam de ser apenas arquivos. Eles passam a funcionar como percurso de entendimento: quem é a B. Living, como ela pensa, como conduz, que provas tem, como atende e como o cliente pode avançar.",
            "A rede social precisa fazer o cliente pensar: aqui existe alguém capaz de me orientar antes de tentar me vender.",
        ],
    },
    {
        "title": "Capítulo 9 - Aplicações Prioritárias",
        "body": [
            "Páginas 087 a 096. Função: tirar o brandbook do plano conceitual e mostrar como ele vira operação.",
        ],
        "talk": [
            "Este capítulo mostra que o brandbook não termina no PDF. Ele começa a ganhar valor quando vira aplicação.",
            "A marca precisa aparecer no dossiê de decisão, no WhatsApp consultivo, nas apresentações comerciais, nos eventos, no ponto físico, nos materiais da equipe, nos conteúdos de Rafael, nas fichas de imóveis e nos briefs para fornecedores.",
            "O objetivo é que cada ponto de contato pareça fazer parte do mesmo sistema.",
            "A B. Living não precisa depender de improviso toda vez que for se comunicar. Ela passa a ter um padrão de decisão, linguagem, imagem e aplicação.",
            "Isso é o que transforma branding em ferramenta comercial.",
        ],
    },
    {
        "title": "Capítulo 10 - Governança E Fechamento",
        "body": [
            "Páginas 097 a 104. Função: garantir continuidade, aprovação correta e evolução sem descaracterizar a marca.",
        ],
        "talk": [
            "A última parte do brandbook existe para proteger o que foi construído.",
            "Uma marca forte não depende só de uma boa apresentação. Ela depende de critério de uso, aprovação, repetição e evolução.",
            "Por isso, o brandbook define governança: quem aprova o quê, quais perguntas precisam ser feitas antes de aprovar uma peça, quais critérios visuais e verbais devem ser respeitados e quais métricas podem indicar evolução de percepção.",
            "A partir daqui, o desafio não é apenas gostar do material. O desafio é aplicar o sistema com consistência.",
        ],
    },
    {
        "title": "Fechamento Da Apresentação",
        "body": [
            "Objetivo: encerrar com síntese estratégica, emoção controlada e convite para aplicação.",
        ],
        "talk": [
            "O que está sendo apresentado aqui é mais do que uma nova forma de comunicar a B. Living.",
            "É uma forma de organizar aquilo que a marca já tinha de mais forte: liderança, equipe, preparo, leitura de cidade, relação com o mercado, qualidade de condução e confiança.",
            "A B. Living não precisa competir por volume de postagem, por estética genérica ou por promessa de luxo. Ela precisa ocupar com clareza o território que já era dela: curadoria para decisões imobiliárias de alto padrão.",
            "Este brandbook é o sistema que permite fazer isso com consistência. Ele orienta como a marca fala, como aparece, como atende, como apresenta, como vende, como prova e como evolui.",
            "A nova B. Living não é uma ruptura com a essência da marca. É a essência da marca organizada para ser percebida.",
        ],
    },
    {
        "title": "Frase Final",
        "body": [
            "Use se quiser terminar com assinatura emocional de A Última Ideia, sem tirar protagonismo da B. Living.",
        ],
        "talk": [
            "A última ideia da B. Living não é trocar quem a marca é. É revelar, com clareza, a força que ela já tinha.",
        ],
    },
    {
        "title": "Versão Curta Para Caso O Tempo Aperte",
        "body": [
            "Use esta versão se precisar abrir a apresentação em até dois minutos antes de passar pelas páginas.",
        ],
        "talk": [
            "A B. Living não começa neste brandbook. Ela já existia na prática: na liderança do Rafael, na qualidade da equipe, no relacionamento com construtoras, na leitura de Florianópolis, no preparo interno e na confiança construída com cada cliente.",
            "O pedido inicial parecia visual: organizar Instagram, destaques, comunicação e percepção premium. Mas o diagnóstico mostrou que o desafio real era maior. A B. Living entregava mais valor do que comunicava.",
            "Por isso, este trabalho não inventa uma nova marca. Ele organiza uma força que já existia. Transforma autoridade em percepção, experiência em método, estética em sistema e comunicação em direção.",
            "A partir daqui, a B. Living deixa de ser apresentada como uma vitrine de imóveis e passa a ser reconhecida como curadoria para decisões imobiliárias de alto padrão.",
            "Esse é o norte do brandbook: antes do imóvel, vem a decisão. E a essência da marca é conduzir essa escolha da forma certa.",
        ],
    },
]


def build_markdown():
    lines = [
        "# Roteiro Completo Para Apresentar O Brandbook B. Living",
        "",
        "Documento de apoio para apresentação do brandbook master completo.",
        "",
        "Tese de condução: B. Living como protagonista; A Última Ideia como intérprete da essência, da operação e da força já existente na marca.",
        "",
    ]
    for section in sections:
        lines.append(f"## {section['title']}")
        lines.append("")
        for paragraph in section["body"]:
            lines.append(paragraph)
            lines.append("")
        lines.append("### Fala sugerida")
        lines.append("")
        for paragraph in section["talk"]:
            lines.append(paragraph)
            lines.append("")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#667085"))
    canvas.drawString(2 * cm, 1.15 * cm, "B. Living - roteiro interno de apresentação")
    canvas.drawRightString(A4[0] - 2 * cm, 1.15 * cm, f"{doc.page}")
    canvas.restoreState()


def build_pdf():
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#102A43"),
        spaceAfter=16,
    )
    subtitle = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#475467"),
        spaceAfter=18,
    )
    h1 = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15.5,
        leading=20,
        textColor=colors.HexColor("#102A43"),
        spaceBefore=4,
        spaceAfter=8,
    )
    label = ParagraphStyle(
        "LabelCustom",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#9A6A20"),
        spaceBefore=8,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=7,
    )
    talk = ParagraphStyle(
        "TalkCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.6,
        leading=16,
        leftIndent=0.35 * cm,
        rightIndent=0.15 * cm,
        borderColor=colors.HexColor("#D6C7A1"),
        borderWidth=0.7,
        borderPadding=7,
        textColor=colors.HexColor("#111827"),
        spaceAfter=7,
    )

    doc = BaseDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.75 * cm,
        bottomMargin=1.85 * cm,
        title="Roteiro Completo Para Apresentar O Brandbook B. Living",
        author="A Última Ideia",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])

    story = [
        Spacer(1, 2.2 * cm),
        Paragraph("Roteiro Completo Para Apresentar O Brandbook B. Living", title),
        Paragraph("Documento de apoio interno para conduzir a apresentação do brandbook master completo.", subtitle),
        Paragraph("Tese de condução: B. Living como protagonista; A Última Ideia como intérprete da essência, da operação e da força já existente na marca.", subtitle),
        PageBreak(),
    ]

    for section in sections:
        story.append(Paragraph(section["title"], h1))
        for paragraph in section["body"]:
            story.append(Paragraph(paragraph, body))
        story.append(Paragraph("FALA SUGERIDA", label))
        for paragraph in section["talk"]:
            story.append(Paragraph(paragraph, talk))
        story.append(Spacer(1, 0.25 * cm))

    doc.build(story)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_markdown()
    build_pdf()
    print(PDF_PATH)
    print(MD_PATH)
