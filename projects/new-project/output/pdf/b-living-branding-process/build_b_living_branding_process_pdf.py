from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from pypdf import PdfReader


ROOT = Path(r"C:\Users\vini1\OneDrive\Documentos\New project")
OUT = ROOT / "output" / "pdf" / "b-living-branding-process"
OUT.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT / "B-Living-Processo-de-Branding-A-Ultima-Ideia.pdf"

FONT_DIR = Path(r"C:\Windows\Fonts")
REGULAR = FONT_DIR / "arial.ttf"
BOLD = FONT_DIR / "arialbd.ttf"
NARROW_BOLD = FONT_DIR / "ARIALNB.TTF"

pdfmetrics.registerFont(TTFont("AUI-Regular", str(REGULAR)))
pdfmetrics.registerFont(TTFont("AUI-Bold", str(BOLD)))
if NARROW_BOLD.exists():
    pdfmetrics.registerFont(TTFont("AUI-Display", str(NARROW_BOLD)))
else:
    pdfmetrics.registerFont(TTFont("AUI-Display", str(BOLD)))

PAGE_W, PAGE_H = landscape(A4)

C = {
    "obsidian": colors.HexColor("#090909"),
    "graphite": colors.HexColor("#202020"),
    "ritual": colors.HexColor("#F7F3EA"),
    "paper": colors.HexColor("#F1ECE2"),
    "muted": colors.HexColor("#8A8A84"),
    "line": colors.HexColor("#D8D0C2"),
    "red": colors.HexColor("#D71920"),
    "gold": colors.HexColor("#B8A66F"),
    "ink": colors.HexColor("#161616"),
    "soft": colors.HexColor("#E7E0D3"),
}

FIXES = {
    "nao e": "não é",
    "Nao e": "Não é",
    "objetivo e": "objetivo é",
    "funcao e": "função é",
    "Funcao e": "Função é",
    "pergunta e": "pergunta é",
    "Pergunta e": "Pergunta é",
    "Branding e": "Branding é",
    "marca e": "marca é",
    "Marca e": "Marca é",
    "ela e": "ela é",
    "Ele e": "Ele é",
    "Ele nao": "Ele não",
    "Isso nao": "Isso não",
    "o que e": "o que é",
    "O que e": "O que é",
    "A Ultima Ideia": "A Última Ideia",
    "Ultima": "Última",
    "inteligencia": "inteligência",
    "informacao": "informação",
    "Informacao": "Informação",
    "informacoes": "informações",
    "Informacoes": "Informações",
    "experiencia": "experiência",
    "Experiencia": "Experiência",
    "comunicacao": "comunicação",
    "Comunicacao": "Comunicação",
    "aplicavel": "aplicável",
    "replicavel": "replicável",
    "criterio": "critério",
    "criterios": "critérios",
    "estetica": "estética",
    "Estetica": "Estética",
    "aparencia": "aparência",
    "Aparencia": "Aparência",
    "peca": "peça",
    "Peca": "Peça",
    "estrategia": "estratégia",
    "Estrategia": "Estratégia",
    "estrategico": "estratégico",
    "Estrategico": "Estratégico",
    "estrategica": "estratégica",
    "Estrategica": "Estratégica",
    "decisao": "decisão",
    "Decisao": "Decisão",
    "decisoes": "decisões",
    "Decisoes": "Decisões",
    "funcao": "função",
    "Funcao": "Função",
    "aprovacao": "aprovação",
    "Aprovacao": "Aprovação",
    "aplicacao": "aplicação",
    "Aplicacao": "Aplicação",
    "apresentacao": "apresentação",
    "Apresentacao": "Apresentação",
    "gestao": "gestão",
    "Gestao": "Gestão",
    "mensuracao": "mensuração",
    "Mensuracao": "Mensuração",
    "imersao": "imersão",
    "Imersao": "Imersão",
    "diagnostico": "diagnóstico",
    "Diagnostico": "Diagnóstico",
    "hipoteses": "hipóteses",
    "Hipoteses": "Hipóteses",
    "publico": "público",
    "confianca": "confiança",
    "variacoes": "variações",
    "visao": "visão",
    "diferenciacao": "diferenciação",
    "percepcao": "percepção",
    "Percepcao": "Percepção",
    "posicao": "posição",
    "sequencia": "sequência",
    "operacao": "operação",
    "Operacao": "Operação",
    "pratica": "prática",
    "Pratica": "Prática",
    "negocio": "negócio",
    "Negocio": "Negócio",
    "paginas": "páginas",
    "pagina": "página",
    "nao": "não",
    "Nao": "Não",
    "esta": "está",
    "propria": "própria",
    "proprio": "próprio",
    "imovel": "imóvel",
    "imoveis": "imóveis",
    "referencias": "referências",
    "Referencias": "Referências",
    "categorias": "categorias",
    "analise": "análise",
    "Analise": "Análise",
    "sintese": "síntese",
    "Sintese": "Síntese",
    "lancamento": "lançamento",
    "Lancamento": "Lançamento",
    "anuncios": "anúncios",
    "conteudo": "conteúdo",
    "conteudos": "conteúdos",
    "area": "área",
    "areas": "áreas",
    "proximos": "próximos",
    "proximo": "próximo",
    "proxima": "próxima",
    "apos": "após",
    "basico": "básico",
    "rapido": "rápido",
    "videos": "vídeos",
    "midia": "mídia",
    "possivel": "possível",
    "possiveis": "possíveis",
    "varios": "vários",
    "varias": "várias",
    "limites": "limites",
    "raciocinio": "raciocínio",
    "tras": "trás",
    "construido": "construído",
    "construida": "construída",
    "construcao": "construção",
    "Construcao": "Construção",
    "forca": "força",
    "Forca": "Força",
    "util": "útil",
    "numero": "número",
    "volume": "volume",
    "proposito": "propósito",
    "Proposito": "Propósito",
    "autonomia": "autonomia",
    "codigo": "código",
    "Codigo": "Código",
    "improviso": "improviso",
    "relatorio": "relatório",
    "relatorios": "relatórios",
    "dificil": "difícil",
    "facil": "fácil",
    "Facil": "Fácil",
    "fisico": "físico",
    "Fisico": "Físico",
    "logica": "lógica",
    "Logica": "Lógica",
    "módulo": "módulo",
}


def fix_text(text):
    text = str(text)
    for src, dst in FIXES.items():
        text = re.sub(rf"\b{re.escape(src)}\b", dst, text)
    return text


def wrap_by_width(text, font, size, max_width):
    text = fix_text(text)
    words = str(text).split()
    lines = []
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c, text, x, y, width, font="AUI-Regular", size=13, leading=18, color=None, max_lines=None):
    text = fix_text(text)
    if color:
        c.setFillColor(color)
    c.setFont(font, size)
    lines = []
    for para in str(text).split("\n"):
        if not para.strip():
            lines.append("")
        else:
            lines.extend(wrap_by_width(para, font, size, width))
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def footer(c, page_no, total):
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.35)
    c.line(18 * mm, 13 * mm, PAGE_W - 18 * mm, 13 * mm)
    c.setFont("AUI-Regular", 7.5)
    c.setFillColor(C["muted"])
    c.drawString(18 * mm, 8.5 * mm, fix_text("A Ultima Ideia | Documento de processo e entrega de branding | B. Living"))
    c.drawRightString(PAGE_W - 18 * mm, 8.5 * mm, f"{page_no:02d}/{total:02d}")


def section_label(c, label):
    c.setFont("AUI-Bold", 8)
    c.setFillColor(C["red"])
    c.drawString(18 * mm, PAGE_H - 17 * mm, fix_text(label.upper()))
    c.setStrokeColor(C["red"])
    c.setLineWidth(1.2)
    c.line(18 * mm, PAGE_H - 20 * mm, 42 * mm, PAGE_H - 20 * mm)


def draw_bullets(c, bullets, x, y, width, size=13, leading=18):
    for item in bullets:
        c.setFillColor(C["red"])
        c.circle(x, y + 4, 2.2, fill=1, stroke=0)
        y = draw_wrapped(c, item, x + 8 * mm, y, width - 8 * mm, size=size, leading=leading, color=C["ink"])
        y -= 5
    return y


def draw_card(c, x, y, w, h, title, body, accent=C["gold"]):
    c.setFillColor(C["ritual"])
    c.roundRect(x, y - h, w, h, 4, fill=1, stroke=0)
    c.setStrokeColor(C["line"])
    c.roundRect(x, y - h, w, h, 4, fill=0, stroke=1)
    c.setFillColor(accent)
    c.rect(x, y - h, 4, h, fill=1, stroke=0)
    c.setFillColor(C["ink"])
    c.setFont("AUI-Bold", 11.5)
    c.drawString(x + 8 * mm, y - 11 * mm, fix_text(title))
    draw_wrapped(c, body, x + 8 * mm, y - 20 * mm, w - 15 * mm, size=9.5, leading=13, color=C["graphite"])


def cover(c):
    c.setFillColor(C["obsidian"])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(C["red"])
    c.rect(0, 0, 10 * mm, PAGE_H, fill=1, stroke=0)
    c.setFillColor(C["ritual"])
    c.setFont("AUI-Display", 47)
    c.drawString(24 * mm, PAGE_H - 43 * mm, "B. LIVING")
    c.setFont("AUI-Bold", 22)
    c.drawString(24 * mm, PAGE_H - 62 * mm, "Processo de Branding")
    c.setFont("AUI-Regular", 13.5)
    draw_wrapped(
        c,
        "Como a inteligencia do processo organiza informacao, valor, experiencia e comunicacao para construir uma marca aplicavel - e replicavel para o ecossistema de corretores.",
        24 * mm,
        PAGE_H - 82 * mm,
        175 * mm,
        size=13.5,
        leading=19,
        color=C["soft"],
    )
    c.setStrokeColor(C["gold"])
    c.setLineWidth(1)
    c.line(24 * mm, 37 * mm, 90 * mm, 37 * mm)
    c.setFont("AUI-Regular", 10)
    c.setFillColor(C["gold"])
    c.drawString(24 * mm, 28 * mm, fix_text("Documento preparado pela A Ultima Ideia para Rafael e B. Living"))


def content_page(c, page_no, total, section, title, intro="", bullets=None, cards=None, quote=None):
    c.setFillColor(C["paper"])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    section_label(c, section)
    c.setFillColor(C["ink"])
    c.setFont("AUI-Bold", 25)
    y = PAGE_H - 33 * mm
    y = draw_wrapped(c, title, 18 * mm, y, 168 * mm, font="AUI-Bold", size=25, leading=29, color=C["ink"])
    if intro:
        y -= 6
        y = draw_wrapped(c, intro, 18 * mm, y, 160 * mm, size=12.2, leading=17, color=C["graphite"])
    if quote:
        c.setFillColor(C["obsidian"])
        c.roundRect(196 * mm, PAGE_H - 76 * mm, 78 * mm, 38 * mm, 4, fill=1, stroke=0)
        draw_wrapped(c, quote, 203 * mm, PAGE_H - 48 * mm, 64 * mm, font="AUI-Bold", size=11.5, leading=15, color=C["ritual"])
    if bullets:
        y -= 8
        draw_bullets(c, bullets, 20 * mm, y, 148 * mm, size=11.4, leading=15.5)
    if cards:
        x = 186 * mm
        card_y = PAGE_H - 93 * mm
        for card in cards[:3]:
            draw_card(c, x, card_y, 90 * mm, 28 * mm, card[0], card[1], card[2] if len(card) > 2 else C["gold"])
            card_y -= 33 * mm
    footer(c, page_no, total)


PAGES = [
    ("abertura", "O papel deste PDF", "Este material explica o raciocinio por tras do projeto de branding da B. Living. Ele nao substitui o brandbook final; ele mostra como esse brandbook nasce.", ["Transforma bastidores em argumento de valor.", "Mostra que o trabalho nao e uma peca estetica isolada.", "Prepara Rafael para entender a profundidade da entrega final."], [("Funcao", "Explicar processo, investimento intelectual e aplicacao pratica."), ("Uso", "Pode ser enviado antes da apresentacao completa ou usado como apoio comercial.")], "O que parece simples no final precisa ser construido com criterio antes."),
    ("abertura", "O que a entrega final pode conter", "A entrega oficial de branding pode chegar a aproximadamente 90 paginas porque precisa consolidar estrategia, experiencia, linguagem, visual, comunicacao, exemplos e governanca.", ["Este PDF explica a logica da entrega.", "O brandbook final documenta a marca em profundidade.", "O toolkit transforma a estrategia em uso diario.", "A governanca evita que a marca se desorganize depois da aprovacao."], [("Importante", "O numero de paginas nao e o objetivo. A profundidade util e o objetivo.", C["red"])], None),
    ("abertura", "A tese da A Ultima Ideia", "Branding e gestao de valor. A marca precisa alinhar o que ela e, o que ela faz e o que ela fala, para que o mercado perceba mais valor, mais confianca e mais diferenciacao.", ["O E organiza estrategia e posicao.", "O Faz prova essa estrategia na experiencia.", "O Fala torna essa verdade percebida em linguagem, visual e comunicacao."], [("E", "Quem a marca e, qual valor sustenta e que lugar ocupa."), ("Faz", "Como a marca entrega, atende, vende e prova a promessa."), ("Fala", "Como a marca comunica, aparece, narra e cria memoria.")], "Antes de criar aparencia, encontramos a forca."),
    ("abertura", "Como informacao vira marca", "O processo nao parte de opiniao visual. Ele transforma informacoes soltas em leitura, leitura em decisao e decisao em sistema de marca.", ["Informacoes entram como sinais: negocio, mercado, clientes, equipe, vendas, canais e materiais.", "O diagnostico separa sintoma de causa.", "A plataforma transforma conclusoes em direcao.", "A identidade e a comunicacao traduzem a direcao em forma publica."], [("Entrada", "Dados, conversas, materiais, percepcao e contexto."), ("Processamento", "Pesquisa, diagnostico, tensoes, oportunidades e criterios."), ("Saida", "Brandbook, toolkit, narrativa, visual, canais e governanca.")], None),
    ("processo", "Mapa geral do processo", "O desenvolvimento segue uma sequencia de dez etapas. Cada etapa reduz subjetividade e aumenta clareza para a etapa seguinte.", ["1. Imersao", "2. Pesquisa", "3. Diagnostico", "4. Decodificador de Valor", "5. Plataforma de Branding", "6. Experiencia e Jornada", "7. Identidade Verbal", "8. Identidade Visual", "9. Comunicacao", "10. Implementacao, Gestao e Mensuracao"], [("Logica", "Da compreensao ao sistema aplicavel."), ("Resultado", "Uma marca que pode ser apresentada, usada, replicada e medida.")], None),
    ("etapa 1", "Imersao: entender antes de propor", "A imersao organiza o contexto real da B. Living: negocio, ambicao, momento, percepcao atual, equipe, clientes, objetivos comerciais e riscos de comunicacao.", ["O pedido inicial nao e tratado como conclusao.", "A conversa separa expectativa, problema real e hipoteses.", "A etapa define o que precisa ser investigado antes de virar identidade.", "Para a B. Living, isso inclui marca master, corretores, atendimento e alto valor percebido."], [("Entrega interna", "Briefing estrategico e matriz pedido versus problema."), ("Entrega ao cliente", "Leitura clara do desafio e do que sera investigado.")], None),
    ("etapa 1", "Pedido declarado versus problema real", "Muitas empresas pedem logo, post, site ou apresentacao. O processo pergunta o que existe por tras disso: percepcao fraca, falta de diferenciacao, inconsistencia de equipe ou dificuldade de vender valor.", ["Pedido declarado: o que o cliente acha que precisa.", "Problema real: o que impede a marca de ser percebida corretamente.", "Hipoteses: leituras iniciais que precisam de evidencia.", "Proximos passos: o que deve ser validado para nao criar no escuro."], [("Para Rafael", "A pergunta nao e apenas 'qual identidade usar?'. A pergunta e 'qual percepcao a B. Living precisa comandar?'.", C["red"])], None),
    ("etapa 2", "Pesquisa: transformar intuicao em evidencia", "A pesquisa organiza sinais de mercado, categoria, publico, concorrencia, comportamento, reputacao, vendas e comunicacao.", ["O objetivo nao e acumular informacao.", "O objetivo e descobrir o que sustenta decisao.", "Achados fortes viram criterios de branding.", "Achados fracos ficam como hipoteses, nao como verdades."], [("O que entra", "Materiais existentes, conversas, canais, concorrentes e referencias."), ("O que sai", "Achados, tensoes, oportunidades e nivel de confianca.")], None),
    ("etapa 2", "O que precisa ser observado na B. Living", "A B. Living opera em uma categoria em que confianca, repertorio, presenca, atendimento e percepcao de exclusividade influenciam diretamente a decisao.", ["Como a marca aparece no Instagram.", "Como os corretores se apresentam individualmente.", "Como o imovel e narrado.", "Como o atendimento prova ou enfraquece a promessa.", "Como a empresa pode parecer mais coordenada sem apagar a individualidade dos corretores."], [("Foco", "Imobiliaria de alto valor nao vende apenas metros quadrados. Vende leitura, seguranca, desejo e decisao patrimonial.")], None),
    ("etapa 3", "Diagnostico: separar sintoma de causa", "O diagnostico e a virada do processo. Ele interpreta o que foi encontrado e define quais problemas realmente precisam ser resolvidos pela marca.", ["Sintoma: a comunicacao parece inconsistente.", "Causa possivel: falta uma plataforma comum.", "Sintoma: cada corretor fala de um jeito.", "Causa possivel: nao existe um codigo de marca compartilhado.", "Sintoma: o valor existe, mas nao aparece com forca.", "Causa possivel: experiencia e narrativa nao estao alinhadas."], [("Entrega", "Problema central, tensoes, gaps, riscos e oportunidades."), ("Checkpoint", "Antes de criar, Rafael valida a leitura estrategica.")], None),
    ("etapa 3", "Mapa E, Faz e Fala", "A leitura da B. Living precisa mostrar se existe coerencia entre estrategia, experiencia e comunicacao.", ["E: posicionamento, proposta de valor, essencia e personalidade.", "Faz: atendimento, captacao, visita, pos-venda, materiais e relacionamento.", "Fala: Instagram, WhatsApp, apresentacoes, roteiros, argumentos comerciais e linguagem visual."], [("Pergunta-chave", "O que a B. Living promete esta sendo provado em cada ponto de contato?", C["red"])], None),
    ("etapa 4", "Decodificador de Valor", "Antes de definir a plataforma, o processo identifica quais ativos precisam ser preservados, fortalecidos, ressignificados ou abandonados.", ["Preservar: o que ja tem valor e nao deve ser perdido.", "Fortalecer: o que existe, mas precisa de mais presenca.", "Ressignificar: o que pode ganhar novo sentido.", "Abandonar: o que enfraquece percepcao, consistencia ou valor."], [("Para a B. Living", "Essa etapa evita que a marca jogue fora ativos importantes ou mantenha vicios que confundem o mercado.")], None),
    ("etapa 5", "Plataforma de Branding", "A plataforma e a base estrategica que organiza a marca. E o documento de decisao que orienta tudo o que vem depois.", ["Posicionamento.", "Proposta de valor.", "Essencia.", "Promessa.", "Pilares.", "Personalidade.", "Territorios de marca.", "Criterios de decisao."], [("Funcao", "Tirar a marca do campo do gosto pessoal e colocar em um sistema de criterios."), ("Aplicacao", "Toda peca futura deve conseguir responder a plataforma.")], None),
    ("etapa 5", "O que a plataforma resolve para Rafael", "A plataforma permite que a B. Living tenha uma direcao comum mesmo quando varias pessoas comunicam a marca.", ["Rafael passa a ter criterio para aprovar ou reprovar materiais.", "Corretores entendem o que podem e nao podem alterar.", "Fornecedores recebem direcao, nao apenas pedido.", "Conteudo passa a nascer de territorios, nao de improviso.", "A marca ganha consistencia sem ficar engessada."], [("Resultado", "Menos subjetividade. Mais decisao. Mais coerencia.")], None),
    ("etapa 6", "Experiencia e Jornada", "Uma marca imobiliaria precisa ser provada na experiencia. O cliente percebe valor no atendimento, na visita, no material, na forma como o corretor conduz e na seguranca que sente para decidir.", ["Mapear a jornada do cliente.", "Identificar momentos de alto impacto.", "Definir principios de atendimento e apresentacao.", "Conectar promessa de marca com entrega real.", "Criar padroes que ajudem todos os corretores."], [("Brand moments", "Pontos da jornada em que a marca precisa aparecer com mais forca.")], None),
    ("etapa 6", "Promessa versus entrega", "O branding nao pode prometer o que a operacao nao sustenta. Por isso, a experiencia precisa confirmar a narrativa.", ["Se a marca promete curadoria, o atendimento precisa demonstrar criterio.", "Se promete alto valor, a apresentacao precisa parecer alto valor.", "Se promete confianca, a comunicacao precisa ser clara, segura e consistente.", "Se promete exclusividade, o cliente precisa sentir tratamento e contexto."], [("Regra", "Toda promessa precisa encontrar uma prova na experiencia.", C["red"])], None),
    ("etapa 7", "Identidade Verbal", "A identidade verbal define como a B. Living fala, argumenta, conduz, vende, apresenta imoveis e se relaciona.", ["Narrativa central da marca.", "Tom de voz.", "Mensagens-chave.", "Vocabulario permitido e evitado.", "Argumentos comerciais.", "Exemplos de antes e depois.", "Roteiros para pontos de contato importantes."], [("Para corretores", "Ajuda cada profissional a se comunicar com personalidade sem sair do territorio da B. Living.")], None),
    ("etapa 7", "Linguagem para a marca e para os corretores", "O desafio e criar uma linguagem comum sem transformar todos os corretores em copias uns dos outros.", ["A B. Living tem voz institucional.", "Cada corretor pode ter uma assinatura individual.", "A base de valor precisa ser compartilhada.", "O argumento de venda precisa parecer parte do mesmo ecossistema.", "As diferencas individuais devem reforcar a marca, nao fragmenta-la."], [("Arquitetura", "Marca master forte + personal branding endossado para os corretores.")], None),
    ("etapa 8", "Identidade Visual", "A identidade visual traduz estrategia em reconhecimento. Ela nao deve nascer antes da plataforma, porque visual sem direcao vira gosto pessoal.", ["Paleta.", "Tipografia.", "Estilo de imagem.", "Composicao.", "Grafismos.", "Aplicacoes reais.", "Critérios de legibilidade, contraste e consistencia.", "Sistema para marca principal e variações de corretores."], [("Objetivo", "Fazer tudo parecer parte do mesmo universo, mesmo quando cada corretor aparece individualmente.")], None),
    ("etapa 8", "Ecossistema visual da B. Living", "A marca precisa ter uma aparencia reconhecivel em diferentes contextos: institucional, comercial, social, individual, digital e impresso.", ["Materiais institucionais.", "Apresentacoes de imoveis.", "Posts e stories.", "Assinaturas de corretores.", "Propostas comerciais.", "Convites e eventos.", "Capas de videos.", "Modelos de anuncios e comunicados."], [("Criterio", "Consistencia visual nao significa repeticao. Significa reconhecimento.")], None),
    ("etapa 9", "Comunicacao", "A comunicacao transforma a plataforma em narrativa publica. Ela define o que a B. Living fala, para quem fala, em qual canal e com qual funcao.", ["Territorios editoriais.", "Mensagens por etapa do funil.", "Plano de canais.", "Direcao de conteudo.", "Campanhas e grandes ideias, quando fizer sentido.", "Calendario, se houver capacidade operacional."], [("Papel", "Evitar conteudo solto e criar uma presenca publica que educa, diferencia e vende valor.")], None),
    ("etapa 9", "Conteudo como prova de posicionamento", "A comunicacao da B. Living deve mostrar criterio, repertorio e leitura de mercado. O conteudo nao deve existir apenas para manter frequencia.", ["Conteudos de autoridade imobiliaria.", "Leituras de regiao e oportunidade.", "Imoveis apresentados com narrativa, nao apenas ficha tecnica.", "Bastidores de curadoria.", "Provas de atendimento e relacionamento.", "Conteudos individuais dos corretores alinhados ao mesmo codigo."], [("Regra", "Todo conteudo deve reforcar uma percepcao desejada.")], None),
    ("etapa 10", "Implementacao, Gestao e Mensuracao", "A etapa final garante que o branding nao morra na apresentacao. O sistema precisa ser usado, revisado e compartilhado.", ["Brandbook.", "Toolkit.", "Guia rapido.", "Treinamento ou repasse.", "Checklist de consistencia.", "Rotina de aprovacao.", "Indicadores de marca, comunicacao e experiencia.", "Plano de evolucao."], [("Entrega viva", "Marca nao e arquivo final. Marca e sistema de gestao.")], None),
    ("aplicacao", "Como isso se aplica diretamente a B. Living", "O projeto deve consolidar a B. Living como marca principal e organizar a forma como corretores, materiais e comunicacao orbitam esse centro.", ["A marca master define o territorio.", "Os corretores ganham autonomia com limites claros.", "Os materiais passam a compartilhar linguagem e visual.", "O cliente percebe um ecossistema coordenado.", "Rafael ganha controle de consistencia e direcao."], [("Resultado esperado", "Uma imobiliaria com percepcao mais forte e uma equipe mais alinhada na forma de vender valor.")], None),
    ("aplicacao", "Marca master + branding individual dos corretores", "A replicacao para corretores nao deve criar marcas independentes desconectadas. Ela deve funcionar como arquitetura endossada.", ["A B. Living aparece como selo de confianca.", "O corretor aparece como especialista com estilo proprio.", "A narrativa individual respeita os pilares da marca.", "O visual individual usa variacoes controladas.", "A comunicacao individual amplia a presenca da B. Living."], [("Modelo", "Individualidade com pertencimento. Autonomia sem fragmentacao.", C["red"])], None),
    ("aplicacao", "O que pode variar e o que deve permanecer", "Para o ecossistema funcionar, cada corretor precisa ter espaco de expressao, mas dentro de um codigo comum.", ["Pode variar: foto, especialidade, tom pessoal dentro do limite, repertorio, nicho, forma de aparecer.", "Deve permanecer: marca B. Living, criterios visuais, promessa central, padrao de apresentacao, argumentos de valor, qualidade de linguagem.", "Nao pode acontecer: cada corretor parecer uma imobiliaria separada."], [("Objetivo", "Fazer o cliente reconhecer a B. Living mesmo quando o ponto de contato e individual.")], None),
    ("aplicacao", "Toolkit para corretores", "O toolkit transforma a estrategia em uso pratico para a equipe.", ["Modelos de post.", "Modelos de story.", "Assinatura visual.", "Bio orientada.", "Roteiros de WhatsApp.", "Mensagens de captacao.", "Apresentacao de imovel.", "Pitch pessoal.", "Checklist antes de publicar.", "Exemplos corretos e incorretos."], [("Beneficio", "Reduz improviso, acelera aplicacao e aumenta consistencia.")], None),
    ("entrega final", "Estrutura do brandbook oficial", "A entrega final pode ser um documento robusto, porque precisa registrar a marca como sistema completo. O volume pode variar, mas a profundidade deve cobrir estrategia, identidade, aplicacao e gestao.", ["Introducao e contexto.", "Diagnostico sintetico.", "Plataforma de Branding.", "Experiencia e jornada.", "Identidade verbal.", "Identidade visual.", "Comunicacao.", "Ecossistema de corretores.", "Aplicacoes.", "Toolkit.", "Governanca e metricas."], [("Observacao", "Por isso a entrega final pode chegar perto de 90 paginas quando o projeto exige muitas aplicacoes e exemplos.")], None),
    ("entrega final", "O que Rafael recebe no fim", "A entrega final deve permitir que Rafael entenda, apresente, aprove, cobre e replique a marca com mais clareza.", ["Um documento oficial de marca.", "Uma narrativa estrategica clara.", "Criterios de decisao.", "Sistema verbal e visual.", "Aplicacoes para canais prioritarios.", "Modelo de replicacao para corretores.", "Toolkit de uso.", "Rotina de governanca."], [("Valor", "O branding deixa de depender da memoria de quem criou e passa a viver em um sistema consultavel.")], None),
    ("entrega final", "Como mostrar o tempo investido", "O tempo do branding aparece no nivel de decisao que o documento permite tomar.", ["Tempo de escuta: entender contexto e expectativas.", "Tempo de leitura: separar problema real de pedido inicial.", "Tempo de analise: transformar sinais em diagnostico.", "Tempo de criacao: traduzir estrategia em linguagem e visual.", "Tempo de aplicacao: transformar marca em uso real.", "Tempo de governanca: preparar a marca para durar."], [("Mensagem para o cliente", "O valor nao esta apenas nas paginas finais. Esta nas decisoes que elas organizam.")], None),
    ("governanca", "Aprovacoes e checkpoints", "O processo deve ter pontos de validacao para evitar que uma decisao mal resolvida contamine as etapas seguintes.", ["Validar imersao e desafio.", "Validar diagnostico.", "Validar decodificador de valor.", "Validar plataforma.", "Validar experiencia e jornada.", "Validar verbal.", "Validar visual.", "Validar comunicacao.", "Validar brandbook e toolkit."], [("Por que importa", "Cada aprovacao reduz retrabalho e aumenta seguranca na proxima etapa.")], None),
    ("governanca", "Indicadores de marca e consistencia", "A marca precisa ser acompanhada por sinais que mostrem se a percepcao esta evoluindo.", ["Consistencia visual entre corretores.", "Clareza de mensagem nos canais.", "Qualidade dos materiais de imoveis.", "Aderencia dos corretores ao toolkit.", "Percepcao de valor em conversas comerciais.", "Engajamento qualificado.", "Conversao por etapa da jornada.", "Feedback de clientes e parceiros."], [("Medicao", "Nao medir apenas alcance. Medir clareza, consistencia, percepcao e valor.")], None),
    ("roadmap", "Caminho recomendado para a B. Living", "O projeto pode seguir em uma sequencia objetiva: consolidar a marca principal, criar o sistema de uso e depois replicar para corretores.", ["1. Fechar diagnostico e plataforma.", "2. Definir verbal e visual da marca master.", "3. Montar brandbook oficial.", "4. Criar toolkit de aplicacao.", "5. Construir modelo de branding individual para corretores.", "6. Testar com primeiros perfis.", "7. Ajustar regras.", "8. Treinar equipe.", "9. Implantar rotina de governanca."], [("Progresso", "Primeiro o centro. Depois as extensoes.")], None),
    ("fechamento", "Resultado esperado", "Ao final, a B. Living deve ter uma marca mais clara, mais forte e mais facil de aplicar. O cliente percebe unidade. Os corretores ganham direcao. Rafael ganha controle estrategico.", ["Mais consistencia entre marca, equipe e materiais.", "Mais clareza sobre o que a B. Living representa.", "Mais criterio para aprovar conteudo e identidade.", "Mais forca para os corretores se posicionarem sem fragmentar a marca.", "Mais capacidade de transformar branding em vantagem comercial."], [("Sintese", "O objetivo nao e criar um documento bonito. E criar um sistema de marca que organiza valor e pode ser usado todos os dias.", C["red"])], None),
]


def build():
    total = len(PAGES) + 1
    c = canvas.Canvas(str(PDF_PATH), pagesize=landscape(A4))
    cover(c)
    footer(c, 1, total)
    c.showPage()
    for index, page in enumerate(PAGES, start=2):
        content_page(c, index, total, *page)
        c.showPage()
    c.save()
    pages = len(PdfReader(str(PDF_PATH)).pages)
    print(f"PDF written: {PDF_PATH}")
    print(f"Pages: {pages}")


if __name__ == "__main__":
    build()
