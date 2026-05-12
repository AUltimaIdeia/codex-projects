from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


OUT_DIR = Path(r"C:\Users\vini1\OneDrive\Documentos\New project\output\pdf\b-living-ia-roteiro-apresentacao")
PDF_PATH = OUT_DIR / "B-Living-IA-Roteiro-de-Apresentacao.pdf"


COLORS = {
    "obsidian": colors.HexColor("#090909"),
    "white": colors.HexColor("#F7F3EA"),
    "red": colors.HexColor("#D71920"),
    "gold": colors.HexColor("#B8A66F"),
    "ink": colors.HexColor("#11131A"),
    "muted": colors.HexColor("#66615A"),
    "light": colors.HexColor("#F1ECE2"),
}


SLIDES = [
    {
        "n": "01",
        "title": "Inteligencia aplicada a venda de alto padrao",
        "objective": "Abrir a apresentacao deixando claro que a IA sera tratada como alavanca comercial, nao como moda tecnologica.",
        "talk": [
            "Antes de falar de ferramenta, precisamos alinhar a intencao. Esta implementacao nasce para aproximar marketing, relacionamento e venda. O objetivo nao e produzir mais coisas. E fazer a B. Living vender com mais inteligencia, mais consistencia e mais controle sobre a experiencia premium.",
            "Quando falamos de inteligencia aplicada a venda de alto padrao, estamos falando de transformar conhecimento, velocidade e relacionamento em vantagem comercial acumulada. Cada conversa, cada lead, cada reuniao e cada conteudo passam a alimentar um sistema que aprende.",
        ],
        "transition": "Com essa premissa, a IA deixa de ser um recurso isolado e passa a ser parte da operacao.",
    },
    {
        "n": "02",
        "title": "A IA entra como sistema operacional",
        "objective": "Reformular a percepcao do cliente: IA nao e ferramenta de produtividade, e camada de operacao.",
        "talk": [
            "A grande mudanca aqui e entender que a IA nao deve entrar como uma ferramenta a mais na rotina. Ela entra como sistema operacional comercial. Ou seja: uma camada que conecta marketing, atendimento, gestao, treinamento e venda.",
            "O ganho real nao esta em usar IA. Esta em fazer a operacao aprender e agir melhor todos os dias. Isso significa menos dependencia de memoria individual, menos improviso e mais consistencia na tomada de decisao.",
        ],
        "transition": "Para entender por que isso importa, precisamos olhar para o gargalo atual.",
    },
    {
        "n": "03",
        "title": "A inteligencia existe, mas esta dispersa",
        "objective": "Mostrar que o problema nao e falta de conhecimento, e falta de organizacao e transformacao desse conhecimento em acao.",
        "talk": [
            "A B. Living ja possui inteligencia. Ela esta nas reunioes, na experiencia dos corretores, nos atendimentos, no WhatsApp, na memoria da lideranca e no repertorio sobre produto e cidade.",
            "O ponto e que essa inteligencia ainda aparece de forma fragmentada. Ela depende de quem estava na conversa, de quem lembra do detalhe certo e de quem consegue transformar aquilo em acao no momento certo.",
            "O gargalo, portanto, nao e repertorio. O gargalo e transformar repertorio em execucao replicavel.",
        ],
        "transition": "A partir daqui, a mudanca que propomos e sair da producao manual para um fluxo de inteligencia.",
    },
    {
        "n": "04",
        "title": "Da producao manual para inteligencia em fluxo",
        "objective": "Explicar a mudanca operacional: cada tarefa passa a nascer de uma base comum de conhecimento.",
        "talk": [
            "Hoje, muitas iniciativas nascem quase do zero: uma campanha, uma pauta, uma resposta, uma oferta, uma abordagem para proprietario. O que estamos propondo e que cada tarefa passe a nascer do cerebro da operacao.",
            "A IA deve entrar nos workflows reais: reuniao, campanha, lead, oferta, atendimento, treinamento e aprendizado. O que antes era esforco manual passa a virar um ciclo que aprende.",
        ],
        "transition": "Quando varias pequenas melhorias acontecem ao mesmo tempo, o impacto deixa de ser linear.",
    },
    {
        "n": "05",
        "title": "Resultado vem da multiplicacao de pequenas melhorias",
        "objective": "Apresentar a logica economica da implementacao.",
        "talk": [
            "O resultado nao vem de um unico grande gesto. Ele vem da multiplicacao de melhorias pequenas em pontos criticos: mais qualidade de lead, mais velocidade de resposta, mais preparo comercial, melhor oferta, melhor timing, mais persuasao e mais aprendizado.",
            "Esse e um principio importante de marketing e vendas: o funil nao melhora apenas no topo. Ele melhora quando cada etapa passa a tomar decisoes melhores. Marketing e venda porque marketing so cumpre seu papel quando aproxima demanda, valor e decisao.",
            "Philip Kotler define marketing como a criacao, comunicacao e entrega de valor para satisfazer necessidades de um mercado com resultado para o negocio. Esta implementacao segue exatamente essa logica: criar mais valor percebido e converter melhor esse valor em decisao.",
        ],
        "transition": "O primeiro bloco mostra o impacto institucional dessa mudanca.",
    },
    {
        "n": "06",
        "title": "Impacto institucional",
        "objective": "Abrir o bloco sobre ganhos de marca, comunicacao e gestao.",
        "talk": [
            "O primeiro impacto e institucional. A B. Living ganha velocidade de execucao, escala de comunicacao e uma inteligencia centralizada que preserva o padrao da marca.",
            "Aqui nao estamos falando apenas de marketing de performance. Estamos falando de uma empresa que passa a se comunicar, aprender e se posicionar com mais consistencia.",
        ],
        "transition": "O primeiro ganho pratico aparece na forma como os canais passam a operar.",
    },
    {
        "n": "07",
        "title": "Da operacao linear para a operacao simultanea",
        "objective": "Mostrar que a IA permite desdobrar uma mesma tese em varios canais ao mesmo tempo.",
        "talk": [
            "No modelo tradicional, a comunicacao acontece em fila: primeiro Instagram, depois LinkedIn, depois landing page, depois e-mail. Cada canal exige um novo esforco.",
            "Com IA, a logica muda. Um conceito central pode ser desdobrado simultaneamente em diferentes canais, respeitando formato, publico e contexto de cada um. A operacao fica mais rapida sem perder coerencia.",
        ],
        "transition": "Para isso funcionar, a empresa precisa de um cerebro central de comunicacao.",
    },
    {
        "n": "08",
        "title": "Um cerebro central, muitas superficies",
        "objective": "Explicar o papel da inteligencia central na consistencia omnicanal.",
        "talk": [
            "A ideia e criar uma camada central de inteligencia editorial e comercial. Dela saem narrativas, argumentos, formatos, materiais e respostas para diferentes canais.",
            "A mesma tese pode virar conteudo institucional, argumento de venda, pagina de campanha, roteiro de video, abordagem para WhatsApp ou material para corretor. O canal muda, mas a inteligencia por tras permanece conectada.",
        ],
        "transition": "Um exemplo direto dessa logica aparece nas landing pages.",
    },
    {
        "n": "09",
        "title": "Landing pages deixam de ser projeto especial",
        "objective": "Reposicionar landing pages como infraestrutura de venda e segmentacao.",
        "talk": [
            "Landing page nao precisa ser tratada como uma grande producao pontual. Ela pode virar infraestrutura comercial.",
            "Isso permite criar paginas por projeto, por perfil de comprador, por corretor ou por objetivo comercial. Cada pagina deixa de ser apenas uma vitrine e passa a ser uma tese de venda estruturada para um contexto especifico.",
        ],
        "transition": "A mesma logica vale para os diferentes publicos da B. Living.",
    },
    {
        "n": "10",
        "title": "Comunicacao desenhada por cohorts",
        "objective": "Mostrar segmentacao inteligente por perfis de cliente.",
        "talk": [
            "A comunicacao premium nao pode tratar todos os clientes como se tivessem o mesmo desejo. Um investidor, um morador local, um comprador de segunda residencia e alguem em upgrade de vida respondem a argumentos diferentes.",
            "A IA ajuda a identificar onde cada grupo presta atencao, qual narrativa faz sentido, qual canal usar, com que profundidade falar e qual CTA apresentar.",
        ],
        "transition": "Essa inteligencia tambem nasce de momentos internos, como as reunioes comerciais.",
    },
    {
        "n": "11",
        "title": "Uma reuniao deixa de terminar quando acaba",
        "objective": "Mostrar que reunioes viram insumo de conteudo, venda e treinamento.",
        "talk": [
            "Uma reuniao comercial nao deve terminar quando a reuniao acaba. Tudo que aparece ali - duvidas, oportunidades, objecoes, leitura de mercado, percepcoes dos corretores - pode virar ativo.",
            "A pauta pode virar conteudo. Um insight pode virar argumento comercial. Um direcionamento pode virar metodo de treinamento. A IA transforma a rotina em memoria institucional.",
        ],
        "transition": "Com isso, a empresa passa a enxergar melhor o proprio negocio.",
    },
    {
        "n": "12",
        "title": "O negocio em tempo real",
        "objective": "Defender a passagem de sensacao para leitura.",
        "talk": [
            "Hoje muitas decisoes de marketing e venda sao tomadas por percepcao. A proposta e fazer a B. Living operar com leitura mais clara do que esta acontecendo.",
            "Comercial, mercado e conteudo passam a alimentar o mesmo sistema. A empresa consegue enxergar quais temas aparecem, quais bairros geram duvida, quais produtos travam, quais perfis respondem melhor e onde existe oportunidade.",
        ],
        "transition": "Essa leitura tambem fortalece a relacao com parceiros e construtoras.",
    },
    {
        "n": "13",
        "title": "Fonte de inteligencia para parceiros",
        "objective": "Ampliar o valor da B. Living para construtoras e parceiros.",
        "talk": [
            "A B. Living pode deixar de ser vista apenas como canal de venda e passar a ser fonte qualificada de inteligencia de mercado.",
            "A empresa pode devolver para parceiros leituras sobre objecoes reais, perfil de demanda, feedback de lancamento e validacao institucional. Isso aumenta relevancia e fortalece relacionamento estrategico.",
        ],
        "transition": "O mesmo raciocinio tambem se aplica a captacao de imoveis.",
    },
    {
        "n": "14",
        "title": "IA tambem melhora a captacao",
        "objective": "Mostrar que a IA atua antes da venda, tambem na geracao de oferta.",
        "talk": [
            "A operacao premium nao cresce apenas vendendo melhor. Ela cresce captando melhor.",
            "A IA pode apoiar o mapeamento de ativos estrategicos, a priorizacao de oportunidades, a preparacao de argumento para proprietarios e a criacao de materiais de captacao mais inteligentes.",
        ],
        "transition": "Mas todo esse ganho precisa proteger uma coisa central: o posicionamento da marca.",
    },
    {
        "n": "15",
        "title": "Escalar sem diluir o posicionamento",
        "objective": "Mostrar que automacao sem criterio pode danificar marca premium.",
        "talk": [
            "No alto padrao, escala sem controle vira risco. A sofisticacao nao esta no adjetivo. Ela esta na leitura, no contexto, no silencio certo e na forma de conduzir a decisao.",
            "Por isso a IA precisa proteger o tom da B. Living. Ela deve evitar copy generica, padronizar linguagem sem engessar pessoas, corrigir exageros comerciais e preservar quiet luxury em escala.",
        ],
        "transition": "Depois do impacto institucional, entramos no impacto diretamente comercial.",
    },
    {
        "n": "16",
        "title": "Impacto comercial",
        "objective": "Abrir o bloco sobre ganhos para corretor, lead, oferta e fechamento.",
        "talk": [
            "O segundo impacto e comercial. Aqui a IA entra para melhorar o trabalho do corretor: prioridade, repertorio, timing, resposta, preparacao e precisao na conversa.",
            "A tecnologia nao substitui a relacao. Ela prepara melhor a relacao.",
        ],
        "transition": "Vamos olhar primeiro para o funil inteiro.",
    },
    {
        "n": "17",
        "title": "A IA interfere em todos os fatores da venda",
        "objective": "Mostrar que a IA nao atua so em captacao de lead.",
        "talk": [
            "A IA nao deve ser medida apenas por gerar mais leads. Ela interfere em todos os fatores que movem a venda: atrair, trabalhar, preparar, ofertar, negociar e aprender.",
            "Cada etapa gera dados. E cada dado pode melhorar a proxima decisao. Esse e o ponto: a venda passa a ficar menos dependente de improviso e mais sustentada por aprendizado.",
        ],
        "transition": "Um dos primeiros indicadores a melhorar e a latencia comercial.",
    },
    {
        "n": "18",
        "title": "Reduzir a latencia comercial",
        "objective": "Transformar velocidade de resposta em metrica estrategica.",
        "talk": [
            "Latencia e o tempo que separa oportunidade de acao. No comercial, esse tempo importa muito: lead entrou, alguem precisa entender, priorizar, responder e acionar o proximo passo.",
            "A IA pode ajudar a classificar o lead, sugerir resposta com contexto e acionar o corretor certo. Em mercados competitivos, isso muda a chance de conversao.",
        ],
        "transition": "Depois da velocidade, vem a qualidade do direcionamento.",
    },
    {
        "n": "19",
        "title": "O lead certo para o corretor certo",
        "objective": "Explicar roteamento inteligente de oportunidades.",
        "talk": [
            "Nem todo lead deve ser tratado da mesma forma, e nem todo corretor e o melhor caminho para toda oportunidade.",
            "A IA pode cruzar perfil do cliente, tipo de produto, historico do corretor, regiao, relacionamento e chance de avanco. O objetivo e distribuir melhor as oportunidades, nao apenas distribuir mais rapido.",
        ],
        "transition": "Essa mesma inteligencia precisa aparecer na conversa mais importante do dia a dia: o WhatsApp.",
    },
    {
        "n": "20",
        "title": "WhatsApp com cerebro da empresa",
        "objective": "Mostrar que resposta boa nao e texto bonito, e contexto certo.",
        "talk": [
            "No WhatsApp, a diferenca nao esta em escrever uma resposta mais bonita. Esta em responder com contexto comercial, leitura de mercado e padrao de marca.",
            "A resposta ideal carrega tom do corretor, visao da lideranca, perfil do cliente e tese do imovel. Isso permite atender rapido sem parecer automatico e manter a sofisticacao da B. Living.",
        ],
        "transition": "Essa mesma profundidade muda a forma de apresentar uma oferta.",
    },
    {
        "n": "21",
        "title": "A oferta deixa de ser envio de imovel",
        "objective": "Reposicionar oferta como construcao de tese.",
        "talk": [
            "No alto padrao, oferta nao e simplesmente mandar um imovel. Oferta e construir uma tese: por que esse produto, para essa pessoa, neste momento.",
            "A IA ajuda a organizar contexto, aderencia, timing e persuasao. Isso torna a abordagem mais consultiva e menos transacional.",
        ],
        "transition": "E cada reacao do cliente passa a alimentar o sistema.",
    },
    {
        "n": "22",
        "title": "Cada objecao vira inteligencia",
        "objective": "Mostrar como a voz do cliente vira ativo comercial.",
        "talk": [
            "Duvidas, silencios, objecoes e comparacoes deixam rastros. Se muitos clientes perguntam sobre liquidez, preco ou bairro, isso nao deve se perder em conversas soltas.",
            "Esses sinais podem virar conteudo, script, material de apoio, defesa de valor e pauta de treinamento. A voz do cliente retroalimenta marketing e venda.",
        ],
        "transition": "Com isso, a empresa tambem melhora a formacao do time.",
    },
    {
        "n": "23",
        "title": "A empresa vira escola alimentada pelo mercado",
        "objective": "Mostrar treinamento continuo e aplicado.",
        "talk": [
            "Treinamento nao precisa ser um evento isolado. A empresa pode virar uma escola em fluxo, alimentada pelo que o mercado realmente pergunta, trava e compara.",
            "A IA pode simular clientes, orientar abordagens, dar feedback e usar historico real para preparar melhor o corretor. O aprendizado aparece no momento em que ele precisa ser usado.",
        ],
        "transition": "Esse cuidado tambem se estende ao relacionamento depois do lead.",
    },
    {
        "n": "24",
        "title": "A experiencia premium continua depois do lead",
        "objective": "Mostrar IA como bastidor de relacionamento humano.",
        "talk": [
            "Relacionamento premium exige memoria, contexto e presenca bem dosada. A IA trabalha nos bastidores para a relacao parecer mais humana, nao menos.",
            "Ela ajuda a lembrar preferencias, datas, historico, interesses, momentos de reabordagem e oportunidades de curadoria individual. A marca permanece proxima sem parecer ansiosa ou agressiva.",
        ],
        "transition": "Para tudo isso funcionar, existe uma condicao: controle.",
    },
    {
        "n": "25",
        "title": "Para gerar resultado, a IA precisa de controle",
        "objective": "Mostrar governanca como requisito de qualidade e seguranca.",
        "talk": [
            "IA sem controle nao e estrategia. E risco. Principalmente em uma marca premium, onde linguagem, dados, permissao e criterio comercial precisam ser bem desenhados.",
            "A arquitetura precisa separar fonte factual, orquestracao, acao, controle e blocos reutilizaveis. Isso garante que a IA execute com aprovacao humana, seguranca, auditoria e padrao de marca.",
        ],
        "transition": "Por isso a implementacao deve acontecer por fases, com resultado visivel em cada etapa.",
    },
    {
        "n": "26",
        "title": "Implementar por fases",
        "objective": "Dar clareza sobre o caminho de execucao.",
        "talk": [
            "A recomendacao e comecar simples, gerar confianca e aumentar profundidade com dados reais.",
            "Primeiro, fundacao: materiais, tom, imoveis, base e regras. Depois, piloto comercial: WhatsApp, leads, simulacoes, reunioes e ofertas. Em seguida, marketing omnicanal: landing pages, cohorts, conteudos e campanhas. Por fim, performance: dashboards, metricas, feedback e melhoria continua.",
            "Em tres meses, a IA ja deve melhorar a prioridade no dia do corretor. Em um ano, o objetivo e tornar a venda mais previsivel.",
        ],
        "transition": "A conclusao e simples: IA nao substitui a relacao, ela prepara melhor cada relacao.",
    },
    {
        "n": "27",
        "title": "A IA nao substitui a relacao",
        "objective": "Fechar com a tese central e reforcar a razao comercial da implementacao.",
        "talk": [
            "A mensagem final e esta: a IA nao substitui a relacao. Ela prepara melhor cada relacao.",
            "No alto padrao, quem entende antes decide melhor. E quem organiza melhor sua inteligencia vende com mais precisao. Essa implementacao existe porque marketing e venda. Marketing cria demanda, organiza valor e conduz decisao. A IA entra para tornar esse processo mais claro, mais rapido e mais inteligente.",
            "A partir daqui, o trabalho e desenhar a operacao para que cada lead, cada conteudo, cada reuniao e cada atendimento ajude a B. Living a aprender e vender melhor.",
        ],
        "transition": "Encerrar abrindo para perguntas e validando proximos passos de implementacao.",
    },
]


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "CoverTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=32,
            leading=36,
            textColor=COLORS["white"],
            alignment=TA_LEFT,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            "CoverSub",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#BEB8AE"),
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            "SlideKicker",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=COLORS["gold"],
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "SlideTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=22,
            leading=26,
            textColor=COLORS["ink"],
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            "SectionLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=COLORS["red"],
            spaceBefore=8,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10.4,
            leading=15.2,
            textColor=COLORS["ink"],
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "Muted",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13.5,
            textColor=COLORS["muted"],
            spaceAfter=8,
        )
    )
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(COLORS["light"])
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(COLORS["red"])
    canvas.rect(1.55 * cm, height - 1.45 * cm, 1.0 * cm, 0.06 * cm, fill=1, stroke=0)
    canvas.setFillColor(COLORS["muted"])
    canvas.setFont("Helvetica", 7)
    canvas.drawString(1.55 * cm, 0.9 * cm, "A ULTIMA IDEIA | B. Living | Roteiro de apresentacao")
    page = str(canvas.getPageNumber())
    canvas.drawRightString(width - 1.55 * cm, 0.9 * cm, page)
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(COLORS["obsidian"])
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(COLORS["gold"])
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(1.7 * cm, height - 1.8 * cm, "B. LIVING")
    canvas.setFillColor(COLORS["red"])
    canvas.rect(1.7 * cm, height - 12.0 * cm, 5.4 * cm, 0.09 * cm, fill=1, stroke=0)
    canvas.setFillColor(COLORS["white"])
    canvas.setFont("Helvetica", 31)
    canvas.drawString(1.7 * cm, height - 8.0 * cm, "Roteiro de")
    canvas.drawString(1.7 * cm, height - 9.35 * cm, "apresentacao")
    canvas.setFont("Helvetica", 15)
    canvas.setFillColor(colors.HexColor("#BEB8AE"))
    canvas.drawString(1.7 * cm, height - 10.45 * cm, "Implementacao de IA")
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.7 * cm, 1.7 * cm, "Guia de fala slide a slide | Maio 2026")
    canvas.setFont("Helvetica-Bold", 8)
    label = "A ULTIMA IDEIA"
    label_width = stringWidth(label, "Helvetica-Bold", 8)
    canvas.setFillColor(COLORS["red"])
    canvas.rect(width - 1.9 * cm - label_width - 0.55 * cm, 1.72 * cm, 0.35 * cm, 0.04 * cm, fill=1, stroke=0)
    canvas.setFillColor(COLORS["white"])
    canvas.drawString(width - 1.7 * cm - label_width, 1.62 * cm, label)
    canvas.restoreState()


def build_pdf():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    doc = BaseDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=1.65 * cm,
        leftMargin=1.65 * cm,
        topMargin=1.9 * cm,
        bottomMargin=1.35 * cm,
        title="B. Living - Roteiro de Apresentacao",
        author="A Ultima Ideia",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[frame], onPage=cover_page),
            PageTemplate(id="content", frames=[frame], onPage=header_footer),
        ]
    )

    story = [Spacer(1, 1), PageBreak()]
    doc.handle_nextPageTemplate("content")

    intro = (
        "Use este roteiro como base de conducao. A fala foi escrita para soar natural em uma reuniao com cliente: "
        "afirmativa, consultiva e comercial. A ideia nao e ler palavra por palavra, mas manter o raciocinio, os pontos "
        "de enfase e as transicoes."
    )
    story.append(Paragraph("Como usar este roteiro", styles["SlideTitle"]))
    story.append(Paragraph(intro, styles["Body"]))
    story.append(Spacer(1, 0.2 * cm))

    for slide in SLIDES:
        story.append(PageBreak())
        story.append(Paragraph(f"SLIDE {slide['n']}", styles["SlideKicker"]))
        story.append(Paragraph(slide["title"], styles["SlideTitle"]))
        story.append(Paragraph("OBJETIVO DO SLIDE", styles["SectionLabel"]))
        story.append(Paragraph(slide["objective"], styles["Muted"]))
        story.append(Paragraph("FALA SUGERIDA", styles["SectionLabel"]))
        for paragraph in slide["talk"]:
            story.append(Paragraph(paragraph, styles["Body"]))
        story.append(Paragraph("TRANSICAO", styles["SectionLabel"]))
        story.append(Paragraph(slide["transition"], styles["Muted"]))

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(PDF_PATH)
