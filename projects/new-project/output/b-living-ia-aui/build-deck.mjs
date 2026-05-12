import fs from "node:fs/promises";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const requireFromRuntime = createRequire(
  "file:///C:/Users/vini1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json",
);
const artifactPath = requireFromRuntime.resolve("@oai/artifact-tool");
const art = await import(pathToFileURL(artifactPath).href);

const {
  Presentation,
  PresentationFile,
  text,
  shape,
  rule,
  fill,
  hug,
  fixed,
} = art;

const OUT = "C:/Users/vini1/OneDrive/Documentos/New project/output/b-living-ia-aui";
const PREVIEWS = `${OUT}/previews`;
await fs.mkdir(PREVIEWS, { recursive: true });

const W = 1920;
const H = 1080;

const C = {
  obsidian: "#090909",
  graphite: "#202020",
  white: "#F7F3EA",
  concrete: "#8A8A84",
  red: "#D71920",
  gold: "#B8A66F",
  light: "#F1ECE2",
  ink: "#11131A",
  mutedInk: "#5E5A52",
  soft: "#DED7CA",
  deep: "#101010",
};

const FONT = {
  display: "Arial Narrow",
  text: "Arial",
};

const PT_BR = [
  ["A ULTIMA IDEIA", "A ÚLTIMA IDEIA"],
  ["Implementacao", "Implementação"],
  ["Florianopolis", "Florianópolis"],
  ["Inteligencia", "Inteligência"],
  ["inteligencia", "inteligência"],
  ["aplicada a venda", "aplicada à venda"],
  ["alto padrao", "alto padrão"],
  ["padrao", "padrão"],
  ["Relacao", "Relação"],
  ["relacao", "relação"],
  ["nao", "não"],
  ["Nao", "Não"],
  ["esta", "está"],
  ["Esta", "Está"],
  ["operacao", "operação"],
  ["Operacao", "Operação"],
  ["repertorio", "repertório"],
  ["execucao", "execução"],
  ["Execucao", "Execução"],
  ["cerebro", "cérebro"],
  ["Cerebro", "Cérebro"],
  ["producao", "produção"],
  ["Producao", "Produção"],
  ["Mudanca", "Mudança"],
  ["logica", "lógica"],
  ["Equacao", "Equação"],
  ["multiplicacao", "multiplicação"],
  ["varias", "várias"],
  ["variavel", "variável"],
  ["proxima", "próxima"],
  ["proximo", "próximo"],
  ["proximos", "próximos"],
  ["decisao", "decisão"],
  ["decisao patrimonial", "decisão patrimonial"],
  ["Diagnostico", "Diagnóstico"],
  ["reunioes", "reuniões"],
  ["reuniao", "reunião"],
  ["experiencia", "experiência"],
  ["lideranca", "liderança"],
  ["Informacoes", "Informações"],
  ["informacoes", "informações"],
  ["metodo", "método"],
  ["Metodo", "Método"],
  ["replicavel", "replicável"],
  ["sequencia", "sequência"],
  ["sensacao", "sensação"],
  ["publico", "público"],
  ["atencao", "atenção"],
  ["Atencao", "Atenção"],
  ["comunicacao", "comunicação"],
  ["Comunicacao", "Comunicação"],
  ["conteudo", "conteúdo"],
  ["Conteudo", "Conteúdo"],
  ["segmentacao", "segmentação"],
  ["Captacao", "Captação"],
  ["captacao", "captação"],
  ["lancamento", "lançamento"],
  ["Lancamento", "Lançamento"],
  ["imovel", "imóvel"],
  ["imoveis", "imóveis"],
  ["regiao", "região"],
  ["Regiao", "Região"],
  ["residencia", "residência"],
  ["seguranca", "segurança"],
  ["saida", "saída"],
  ["compativeis", "compatíveis"],
  ["frequencia", "frequência"],
  ["Objecoes", "Objeções"],
  ["objecoes", "objeções"],
  ["objecao", "objeção"],
  ["historico", "histórico"],
  ["Historico", "Histórico"],
  ["Validacao", "Validação"],
  ["validacao", "validação"],
  ["relatorios", "relatórios"],
  ["apresentacao", "apresentação"],
  ["Sofisticacao", "Sofisticação"],
  ["sofisticacao", "sofisticação"],
  ["generica", "genérica"],
  ["Latencia", "Latência"],
  ["latencia", "latência"],
  ["Metrica", "Métrica"],
  ["metrica", "métrica"],
  ["acao", "ação"],
  ["Acao", "Ação"],
  ["Distribuicao", "Distribuição"],
  ["distribuicao", "distribuição"],
  ["Aderencia", "Aderência"],
  ["aderencia", "aderência"],
  ["avancar", "avançar"],
  ["persuasao", "persuasão"],
  ["Persuasao", "Persuasão"],
  ["confianca", "confiança"],
  ["Duvidas", "Dúvidas"],
  ["duvidas", "dúvidas"],
  ["silencios", "silêncios"],
  ["comparacoes", "comparações"],
  ["simulacao", "simulação"],
  ["niveis", "níveis"],
  ["ja", "já"],
  ["preferencias", "preferências"],
  ["familia", "família"],
  ["noticias", "notícias"],
  ["permissao", "permissão"],
  ["permissoes", "permissões"],
  ["integracoes", "integrações"],
  ["revisao", "revisão"],
  ["inicio", "início"],
  ["Orquestracao", "Orquestração"],
  ["orquestracao", "orquestração"],
  ["aprovacao", "aprovação"],
  ["avaliacao", "avaliação"],
  ["discricao", "discrição"],
  ["Implantacao", "Implantação"],
  ["visivel", "visível"],
  ["Comecar", "Começar"],
  ["comecar", "começar"],
  ["Fundacao", "Fundação"],
  ["simulacoes", "simulações"],
  ["metricas", "métricas"],
  ["previsivel", "previsível"],
  ["Referencias", "Referências"],
  ["protecao", "proteção"],
  ["visao", "visão"],
  ["Visao", "Visão"],
  ["precisao", "precisão"],
  ["Precisao", "Precisão"],
  ["negocio", "negócio"],
  ["Negocio", "Negócio"],
  ["DIAGNOSTICO", "DIAGNÓSTICO"],
  ["MUDANCA DE LOGICA", "MUDANÇA DE LÓGICA"],
  ["EQUACAO DE VALOR", "EQUAÇÃO DE VALOR"],
  ["REUNIOES", "REUNIÕES"],
  ["CAPTACAO", "CAPTAÇÃO"],
  ["ARQUITETURA E GOVERNANCA", "ARQUITETURA E GOVERNANÇA"],
  ["IMPLANTACAO", "IMPLANTAÇÃO"],
  ["E transformar", "É transformar"],
  ["E uma resposta", "É uma resposta"],
  ["E quem organiza", "E quem organiza"],
  ["real estáte", "real estate"],
];

function localize(value) {
  return PT_BR.reduce((out, [from, to]) => out.replaceAll(from, to), value);
}

const p = Presentation.create({ slideSize: { width: W, height: H } });

function frame(left, top, width, height) {
  return { left, top, width, height };
}

function compose(slide, node, left, top, width, height) {
  slide.compose(node, {
    frame: frame(left, top, width, height),
    baseUnit: 8,
  });
}

function bg(slide, mode = "dark") {
  const color = mode === "dark" ? C.obsidian : C.light;
  compose(slide, shape({ width: fill, height: fill, fill: color }), 0, 0, W, H);
}

function tx(slide, value, x, y, w, h, opts = {}) {
  const displayValue = typeof value === "string" ? localize(value) : value;
  const mode = opts.mode ?? "dark";
  const color =
    opts.color ?? (mode === "dark" ? C.white : C.ink);
  compose(
    slide,
    text(displayValue, {
      name: opts.name,
      width: fill,
      height: hug,
      style: {
        fontFace: opts.font ?? FONT.text,
        fontSize: opts.size ?? 36,
        bold: opts.bold ?? false,
        color,
        lineSpacing: opts.lineSpacing ?? 1.08,
      },
    }),
    x,
    y,
    w,
    h,
  );
}

function line(slide, x, y, w, color = C.red, weight = 4) {
  compose(
    slide,
    rule({ width: fill, stroke: color, weight, height: fixed(weight) }),
    x,
    y,
    w,
    weight + 4,
  );
}

function rect(slide, x, y, w, h, color) {
  compose(slide, shape({ width: fill, height: fill, fill: color }), x, y, w, h);
}

function header(slide, label, index, mode = "dark") {
  const primary = mode === "dark" ? C.white : C.ink;
  const secondary = mode === "dark" ? C.concrete : C.mutedInk;
  tx(slide, "B. LIVING", 86, 66, 300, 38, {
    mode,
    color: mode === "dark" ? C.gold : C.ink,
    size: 22,
    bold: true,
    font: FONT.display,
  });
  tx(slide, label.toUpperCase(), 1540, 66, 290, 34, {
    mode,
    color: mode === "dark" ? C.gold : C.mutedInk,
    size: 16,
    bold: true,
    font: FONT.display,
  });
  tx(slide, "A ULTIMA IDEIA | Implementacao de IA", 86, 1014, 560, 24, {
    mode,
    color: secondary,
    size: 12,
  });
  tx(slide, String(index).padStart(2, "0"), 1802, 1014, 48, 24, {
    mode,
    color: secondary,
    size: 13,
  });
  rect(slide, 70, 998, 38, 3, mode === "dark" ? C.red : C.gold);
}

function title(slide, value, mode = "dark", y = 144, size = 70) {
  tx(slide, value, 86, y, 1270, 190, {
    mode,
    size,
    bold: false,
    lineSpacing: 1.04,
  });
}

function sub(slide, value, mode = "dark", x = 86, y = 330, w = 960) {
  tx(slide, value, x, y, w, 86, {
    mode,
    color: mode === "dark" ? C.concrete : C.mutedInk,
    size: 25,
    lineSpacing: 1.18,
  });
}

function big(slide, value, x, y, w, h, mode = "dark", size = 88, color) {
  tx(slide, value, x, y, w, h, {
    mode,
    color,
    size,
    bold: false,
    lineSpacing: 1.0,
    font: FONT.display,
  });
}

function bullet(slide, n, head, body, x, y, mode = "dark", width = 780) {
  const color = mode === "dark" ? C.white : C.ink;
  const muted = mode === "dark" ? C.concrete : C.mutedInk;
  tx(slide, String(n).padStart(2, "0"), x, y + 4, 46, 28, {
    mode,
    color: C.gold,
    size: 17,
    bold: true,
  });
  line(slide, x + 64, y + 20, 82, C.gold, 2);
  tx(slide, head, x + 170, y, width, 34, {
    mode,
    color,
    size: 27,
    bold: true,
  });
  tx(slide, body, x + 170, y + 40, width, 56, {
    mode,
    color: muted,
    size: 20,
    lineSpacing: 1.15,
  });
}

function chip(slide, label, x, y, w, mode = "dark", color = C.graphite) {
  rect(slide, x, y, w, 54, color);
  tx(slide, label, x + 18, y + 14, w - 36, 26, {
    mode,
    color: mode === "dark" ? C.white : C.ink,
    size: 17,
    bold: true,
  });
}

function section(slide, index, titleText, bodyText) {
  bg(slide, "dark");
  tx(slide, `BLOCO ${index}`, 86, 74, 260, 28, {
    mode: "dark",
    color: C.gold,
    size: 18,
    bold: true,
  });
  rect(slide, 86, 158, 14, 590, C.red);
  big(slide, titleText, 140, 318, 900, 180, "dark", 72);
  sub(slide, bodyText, "dark", 140, 534, 760);
  tx(slide, "A ULTIMA IDEIA", 1490, 996, 260, 24, {
    mode: "dark",
    color: C.concrete,
    size: 12,
  });
}

function addSlide(mode = "dark", label = "", index = 1) {
  const slide = p.slides.add();
  bg(slide, mode);
  header(slide, label, index, mode);
  return slide;
}

// 01 Cover
{
  const s = p.slides.add();
  bg(s, "dark");
  tx(s, "B. LIVING", 86, 74, 300, 36, {
    mode: "dark",
    color: C.gold,
    size: 24,
    bold: true,
    font: FONT.display,
  });
  tx(s, "Implementacao de IA | Maio 2026", 1480, 74, 330, 52, {
    mode: "dark",
    color: C.concrete,
    size: 19,
  });
  rect(s, 86, 660, 420, 9, C.red);
  big(
    s,
    "Inteligencia\naplicada a venda\nde alto padrao",
    86,
    380,
    1120,
    285,
    "dark",
    86,
  );
  sub(
    s,
    "Como transformar conhecimento, velocidade e relacionamento em vantagem comercial acumulada.",
    "dark",
    86,
    706,
    880,
  );
  tx(s, "Florianopolis como contexto. Dados como memoria. Relacao como diferencial.", 86, 986, 820, 24, {
    mode: "dark",
    color: C.concrete,
    size: 16,
  });
  tx(s, "A ULTIMA IDEIA", 1540, 986, 230, 24, {
    mode: "dark",
    color: C.white,
    size: 14,
    bold: true,
    font: FONT.display,
  });
  rect(s, 1516, 994, 14, 3, C.red);
}

// 02 Thesis
{
  const s = addSlide("dark", "Tese", 2);
  title(s, "A IA nao entra como ferramenta.\nEntra como sistema operacional.", "dark", 142, 70);
  sub(
    s,
    "O objetivo e transformar conhecimento, velocidade e relacionamento em resultado comercial.",
    "dark",
    86,
    342,
    900,
  );
  big(
    s,
    "A vantagem nao esta em usar IA.\nEsta em fazer a operacao aprender\ne agir melhor todos os dias.",
    86,
    560,
    1280,
    230,
    "dark",
    58,
  );
  tx(s, "marketing", 1290, 424, 180, 28, { mode: "dark", color: C.concrete, size: 18 });
  tx(s, "venda", 1450, 558, 110, 28, { mode: "dark", color: C.concrete, size: 18 });
  tx(s, "gestao", 1280, 690, 110, 28, { mode: "dark", color: C.concrete, size: 18 });
  tx(s, "treinamento", 1510, 790, 180, 28, { mode: "dark", color: C.concrete, size: 18 });
  rect(s, 1418, 512, 18, 200, C.red);
  rect(s, 1328, 602, 198, 18, C.red);
  tx(s, "cerebro\ncentral", 1370, 604, 220, 64, {
    mode: "dark",
    color: C.white,
    size: 25,
    bold: true,
    lineSpacing: 1.02,
  });
}

// 03 Problem
{
  const s = addSlide("light", "Diagnostico", 3);
  title(s, "A inteligencia existe.\nMas esta dispersa.", "light", 138, 78);
  sub(
    s,
    "Nas reunioes, no WhatsApp, na experiencia dos corretores, na memoria da lideranca e nos materiais de produto.",
    "light",
    86,
    340,
    1000,
  );
  bullet(s, 1, "Conhecimento fragmentado", "Informacoes valiosas nao viram metodo replicavel.", 86, 570, "light", 650);
  bullet(s, 2, "Canais ativados em sequencia", "A operacao executa um canal por vez.", 86, 686, "light", 650);
  bullet(s, 3, "Venda dependente de memoria", "O corretor decide com base no que lembra no momento.", 86, 802, "light", 650);
  big(
    s,
    "O gargalo nao e\nrepertorio.\nE transformar repertorio\nem execucao.",
    1030,
    572,
    690,
    250,
    "light",
    54,
  );
  rect(s, 1010, 558, 8, 288, C.red);
}

// 04 Shift
{
  const s = addSlide("dark", "Mudanca de logica", 4);
  title(s, "De producao manual\npara inteligencia em fluxo.", "dark", 142, 72);
  sub(s, "A IA precisa entrar nos workflows reais: reuniao, campanha, lead, oferta, atendimento e aprendizado.", "dark", 86, 352, 1120);
  const y = 606;
  const rows = [
    ["Antes", "cada tarefa nasce quase do zero"],
    ["Agora", "cada tarefa nasce do cerebro da operacao"],
    ["Depois", "cada execucao melhora a proxima"],
  ];
  rows.forEach(([a, b], i) => {
    const yy = y + i * 116;
    tx(s, a, 86, yy, 170, 36, { mode: "dark", color: C.white, size: 29, bold: true });
    line(s, 236, yy + 20, 130, C.gold, 2);
    tx(s, b, 396, yy - 2, 780, 42, { mode: "dark", color: C.white, size: 34 });
  });
  rect(s, 1370, 548, 12, 320, C.red);
  tx(s, "ciclo que aprende", 1418, 674, 300, 40, { mode: "dark", color: C.concrete, size: 25 });
}

// 05 Equation
{
  const s = addSlide("light", "Equacao de valor", 5);
  title(s, "Resultado vem da multiplicacao\nde pequenas melhorias.", "light", 132, 68);
  sub(s, "Se a IA melhora varias etapas da venda ao mesmo tempo, o impacto deixa de ser linear.", "light", 86, 342, 950);
  const formula = "Leads x velocidade x preparo x oferta x timing x persuasao x aprendizado";
  big(s, formula, 86, 580, 1500, 180, "light", 50, C.ink);
  line(s, 86, 742, 740, C.red, 6);
  tx(s, "Melhorar uma variavel muda o funil. Melhorar todas cria uma operacao que aprende enquanto vende.", 86, 805, 1120, 64, {
    mode: "light",
    color: C.mutedInk,
    size: 27,
  });
}

// 06 Section
{
  const s = p.slides.add();
  section(s, 1, "Impacto\ninstitucional", "A B. Living ganha velocidade de execucao, escala de comunicacao e inteligencia centralizada.");
}

// 07 Simultaneous
{
  const s = addSlide("light", "Velocidade", 7);
  title(s, "Da operacao linear\npara a operacao simultanea.", "light", 132, 74);
  sub(s, "O marketing deixa de ativar canais em fila e passa a operar em paralelo.", "light", 86, 340, 860);
  tx(s, "modelo tradicional", 86, 616, 260, 80, { mode: "light", size: 30, bold: true });
  line(s, 360, 650, 170, C.gold, 2);
  tx(s, "Instagram, depois LinkedIn,\ndepois landing page,\ndepois e-mail", 570, 598, 470, 110, { mode: "light", color: C.mutedInk, size: 28 });
  tx(s, "modelo com IA", 86, 776, 260, 80, { mode: "light", size: 30, bold: true });
  line(s, 360, 810, 170, C.red, 4);
  tx(s, "um conceito central desdobrado\nsimultaneamente em todos os canais", 570, 762, 560, 110, { mode: "light", color: C.ink, size: 30, bold: true });
  ["Instagram", "LinkedIn", "YouTube", "Landing pages", "WhatsApp", "E-mail"].forEach((name, i) => {
    chip(s, name, 1280, 410 + i * 76, 310, "light", i === 0 ? C.red : C.soft);
  });
}

// 08 Central brain
{
  const s = addSlide("dark", "Omnicanalidade", 8);
  title(s, "Um cerebro central.\nMuitas superficies de comunicacao.", "dark", 130, 66);
  sub(s, "A mesma tese vira conteudo institucional, argumento comercial e material de campanha.", "dark", 86, 334, 940);
  rect(s, 780, 506, 360, 170, C.graphite);
  tx(s, "B. Living", 838, 548, 240, 34, { mode: "dark", color: C.white, size: 34, bold: true });
  tx(s, "inteligencia editorial", 838, 596, 260, 26, { mode: "dark", color: C.gold, size: 17 });
  const items = [
    ["Narrativa", "o que a marca acredita"],
    ["Formato", "como aparece por canal"],
    ["Canal", "onde o publico presta atencao"],
    ["Contexto", "momento do lead e do produto"],
  ];
  items.forEach(([h, b], i) => {
    const left = i % 2 === 0 ? 170 : 1260;
    const top = i < 2 ? 468 : 710;
    bullet(s, i + 1, h, b, left, top, "dark", 360);
    line(s, left + (i % 2 === 0 ? 570 : -320), top + 38, 270, C.gold, 1);
  });
}

// 09 Landing pages
{
  const s = addSlide("light", "Infraestrutura", 9);
  title(s, "Landing pages deixam de ser\nprojeto especial.", "light", 130, 74);
  sub(s, "Elas viram infraestrutura de campanha, segmentacao e venda consultiva.", "light", 86, 340, 840);
  [
    ["Por projeto", "uma tese, uma narrativa e um CTA consultivo"],
    ["Por corretor", "autoridade individual conectada ao metodo da B. Living"],
    ["Por perfil", "morador, investidor, segunda residencia e alta renda de fora"],
    ["Por objetivo", "captacao, lancamento, evento, lista VIP ou oportunidade fora do radar"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 86 + (i % 2) * 820, 586 + Math.floor(i / 2) * 154, "light", 550));
}

// 10 Cohorts
{
  const s = addSlide("light", "Cohorts", 10);
  title(s, "A comunicacao passa a ser\ndesenhada por cohorts.", "light", 132, 72);
  sub(s, "Cada publico recebe narrativa, canal, oferta e cadencia compativeis com seu momento.", "light", 86, 340, 1060);
  const cohorts = [
    "25-35: primeira decisao patrimonial",
    "35-45: upgrade de vida",
    "45-60: seguranca e permanencia",
    "Investidor: tese, timing e saida",
    "Morador: cidade, rotina e pertencimento",
  ];
  cohorts.forEach((c, i) => {
    line(s, 86, 530 + i * 82, 90, C.gold, 2);
    tx(s, c, 205, 512 + i * 82, 680, 48, { mode: "light", color: C.ink, size: 27 });
  });
  rect(s, 1060, 566, 9, 260, C.red);
  big(s, "A IA identifica\nonde cada grupo\npresta atencao.", 1105, 584, 570, 170, "light", 52, C.ink);
  tx(s, "Depois ajusta canal, copy, profundidade, frequencia e CTA.", 1105, 794, 520, 66, { mode: "light", color: C.mutedInk, size: 24 });
}

// 11 Meetings
{
  const s = addSlide("dark", "Reunioes", 11);
  title(s, "Uma reuniao deixa de terminar\nquando acaba.", "dark", 126, 66);
  sub(s, "O que foi discutido vira linha editorial, treinamento, material comercial e memoria institucional.", "dark", 86, 334, 1030);
  big(s, "Segunda-feira,\n8h.", 86, 590, 460, 120, "dark", 70, C.white);
  tx(s, "treino. metodo. mercado real.", 90, 728, 400, 30, { mode: "dark", color: C.gold, size: 19 });
  [
    ["Pauta vira conteudo", "post, video, pauta para corretor"],
    ["Insight vira argumento", "objecoes, bairro, produto, timing"],
    ["Direcionamento vira metodo", "o feedback reaparece na rotina"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 1000, 538 + i * 118, "dark", 560));
}

// 12 Real-time reading
{
  const s = addSlide("light", "Leitura", 12);
  title(s, "A empresa passa a enxergar\no negocio em tempo real.", "light", 132, 72);
  sub(s, "Marketing, comercial e produto deixam de operar por sensacao e passam a operar por leitura.", "light", 86, 340, 1060);
  const blocks = [
    ["Comercial", "leads, follow-ups, propostas, resposta e fechamento"],
    ["Mercado", "bairros, projetos, construtoras e movimentos da cidade"],
    ["Conteudo", "canais, temas, formatos, cohorts e oportunidades"],
  ];
  blocks.forEach(([h, b], i) => {
    rect(s, 170 + i * 545, 610, 2, 210, i === 1 ? C.red : C.gold);
    tx(s, h, 200 + i * 545, 612, 360, 40, { mode: "light", size: 30, bold: true });
    tx(s, b, 200 + i * 545, 674, 380, 92, { mode: "light", color: C.mutedInk, size: 23, lineSpacing: 1.18 });
  });
}

// 13 Partners
{
  const s = addSlide("dark", "Construtoras", 13);
  title(s, "A B. Living pode virar\nfonte de inteligencia para parceiros.", "dark", 132, 70);
  sub(s, "Nao apenas vender unidades, mas devolver leitura qualificada de mercado.", "dark", 86, 340, 850);
  [
    ["Objecoes reais do comprador", "o que trava, desperta interesse e precisa ser melhor explicado"],
    ["Perfil de demanda por produto", "quem responde melhor a cada tese, regiao, vista ou estilo de vida"],
    ["Feedback para lancamento", "leitura de publico antes, durante e depois da campanha"],
    ["Validacao institucional", "relacao com parceiros ganha inteligencia registrada"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 900, 420 + i * 116, "dark", 640));
}

// 14 Capture
{
  const s = addSlide("light", "Captacao", 14);
  title(s, "IA tambem melhora\na captacao de imoveis.", "light", 132, 70);
  sub(s, "A operacao premium nao cresce apenas vendendo melhor. Cresce captando melhor.", "light", 86, 340, 880);
  [
    ["Mapear ativos estrategicos", "imoveis, regioes e proprietarios com aderencia ao posicionamento"],
    ["Preparar argumento de captacao", "por que a B. Living e a melhor leitura para aquele ativo"],
    ["Priorizar oportunidades", "potencial comercial, institucional e de relacionamento"],
    ["Criar materiais para proprietarios", "relatorios, tese de preco, demanda e plano de apresentacao"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 86 + (i % 2) * 820, 568 + Math.floor(i / 2) * 160, "light", 570));
}

// 15 Brand
{
  const s = addSlide("dark", "Marca", 15);
  title(s, "Escalar sem diluir\no posicionamento.", "dark", 126, 76);
  sub(s, "A IA precisa proteger o tom premium da B. Living em cada conteudo, resposta e material.", "dark", 86, 342, 1030);
  big(s, "A sofisticacao nao esta\nno adjetivo.", 86, 640, 640, 120, "dark", 54, C.white);
  tx(s, "Esta na leitura, no contexto, no silencio certo e na forma de conduzir a decisao.", 86, 784, 690, 60, {
    mode: "dark",
    color: C.concrete,
    size: 25,
  });
  [
    "evitar copy generica de corretor",
    "padronizar linguagem sem engessar pessoas",
    "corrigir exageros comerciais",
    "preservar quiet luxury em escala",
  ].forEach((t, i) => {
    line(s, 1030, 534 + i * 110, 90, i === 0 ? C.red : C.gold, i === 0 ? 4 : 2);
    tx(s, t, 1148, 512 + i * 110, 560, 60, { mode: "dark", color: C.white, size: 27 });
  });
}

// 16 Section
{
  const s = p.slides.add();
  section(s, 2, "Impacto\ncomercial", "O corretor ganha repertorio, timing, clareza de prioridade e precisao na conversa.");
}

// 17 Funnel
{
  const s = addSlide("light", "Funil", 17);
  title(s, "A IA interfere em todos os fatores\nque movem a venda.", "light", 132, 70);
  sub(s, "Nao so gera mais lead. Aumenta a qualidade do trabalho sobre cada oportunidade.", "light", 86, 340, 980);
  const steps = ["Atrair", "Trabalhar", "Preparar", "Ofertar", "Negociar", "Aprender"];
  steps.forEach((step, i) => {
    const x = 150 + i * 270;
    rect(s, x, 620, 178, 56, i === 5 ? C.red : C.soft);
    tx(s, step, x + 24, 637, 140, 24, {
      mode: "light",
      color: i === 5 ? C.white : C.ink,
      size: 18,
      bold: true,
    });
    if (i < steps.length - 1) line(s, x + 188, 648, 72, C.gold, 2);
  });
  big(s, "Cada etapa gera dados.\nCada dado melhora a proxima decisao.", 220, 790, 1120, 110, "light", 48, C.ink);
}

// 18 Latency
{
  const s = addSlide("dark", "Lead response", 18);
  title(s, "Reduzir a latencia comercial\nvira metrica central.", "dark", 126, 70);
  sub(s, "Tempo entre sinal e acao: lead entrou, sistema entendeu, priorizou e sugeriu o proximo passo.", "dark", 86, 340, 1050);
  big(s, "Latencia", 86, 610, 400, 90, "dark", 72, C.white);
  tx(s, "e o tempo que separa oportunidade de acao.", 90, 712, 500, 54, { mode: "dark", color: C.concrete, size: 25 });
  [
    ["Classificar", "origem, perfil e temperatura"],
    ["Responder", "com contexto e tom correto"],
    ["Acionar", "corretor certo e proximo passo"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 1000, 514 + i * 120, "dark", 560));
  tx(s, "McKinsey, 2026: fluxos agentivos em home builders melhoraram tempo de resposta a leads em mais de 90%.", 86, 964, 960, 28, {
    mode: "dark",
    color: C.concrete,
    size: 12,
  });
}

// 19 Routing
{
  const s = addSlide("light", "Roteamento", 19);
  title(s, "O lead certo\npara o corretor certo.", "light", 132, 70);
  sub(s, "A IA cruza perfil do cliente, historico do corretor, tipo de imovel e chance de avanco.", "light", 86, 340, 1000);
  const cols = [
    ["Lead", "investidor, morador, cliente de fora, segunda residencia"],
    ["Produto", "bairro, ticket, construtora, tese, liquidez, estilo de vida"],
    ["Corretor", "historico, regiao, resposta, relacionamento"],
    ["Distribuicao", "quem tem mais chance de trabalhar com qualidade"],
  ];
  cols.forEach(([h, b], i) => {
    rect(s, 120 + i * 430, 596, 4, 210, i === 3 ? C.red : C.gold);
    tx(s, h, 150 + i * 430, 594, 280, 36, { mode: "light", size: 30, bold: true });
    tx(s, b, 150 + i * 430, 656, 300, 92, { mode: "light", color: C.mutedInk, size: 22, lineSpacing: 1.15 });
  });
}

// 20 WhatsApp
{
  const s = addSlide("dark", "WhatsApp", 20);
  title(s, "A resposta no WhatsApp passa\na carregar o cerebro da empresa.", "dark", 126, 66);
  sub(s, "Cliente, imovel, cidade, marca, historico e timing entram na mesma sugestao.", "dark", 86, 338, 990);
  big(s, "Nao e uma\nresposta bonita.", 86, 592, 720, 150, "dark", 68, C.white);
  tx(s, "E uma resposta com contexto comercial,\nleitura de mercado e padrao de marca.", 86, 786, 900, 80, {
    mode: "dark",
    color: C.white,
    size: 33,
    lineSpacing: 1.08,
  });
  ["tom do corretor", "visao da lideranca", "perfil do cliente", "tese do imovel"].forEach((c, i) => {
    chip(s, c, 1050, 548 + i * 78, 350, "dark", i === 1 ? C.red : C.graphite);
  });
}

// 21 Offer
{
  const s = addSlide("light", "Oferta", 21);
  title(s, "A oferta deixa de ser\nenvio de imovel.", "light", 132, 70);
  sub(s, "Ela passa a ser construcao de tese: por que esse produto, para essa pessoa, neste momento.", "light", 86, 340, 1060);
  [
    ["Contexto", "o que acontece na cidade, na regiao e no mercado"],
    ["Aderencia", "por que o imovel faz sentido para aquele cliente"],
    ["Timing", "quando abordar, nutrir e avancar para proposta"],
    ["Persuasao", "qual argumento usar sem perder confianca"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 86 + (i % 2) * 820, 582 + Math.floor(i / 2) * 154, "light", 580));
}

// 22 Voice of customer
{
  const s = addSlide("dark", "Voice of customer", 22);
  title(s, "Cada objecao\nvira inteligencia.", "dark", 126, 70);
  sub(s, "A voz do cliente retroalimenta conteudo, oferta, treinamento, produto e argumento comercial.", "dark", 86, 342, 950);
  big(s, "Duvidas, silencios,\nobjecoes e comparacoes\ndeixam rastros.", 86, 608, 640, 160, "dark", 52, C.white);
  [
    ["liquidez", "vira conteudo, script e material de apoio"],
    ["preco", "vira tese comparativa e defesa de valor"],
    ["bairro", "vira inteligencia urbana e regua de nutricao"],
  ].forEach(([h, b], i) => bullet(s, i + 1, `Se muitos perguntam sobre ${h}`, b, 1000, 540 + i * 120, "dark", 620));
}

// 23 Training
{
  const s = addSlide("light", "Treinamento", 23);
  title(s, "A empresa vira escola.\nMas uma escola alimentada pelo mercado.", "light", 132, 70);
  sub(s, "Feedback, onboarding e simulacao deixam de ser eventos e passam a operar dentro do fluxo.", "light", 86, 340, 1080);
  [
    ["Simular clientes por projeto", "perfis, objecoes e niveis de consciencia diferentes"],
    ["Dar nota e orientar", "tom, clareza, contexto, pergunta, oferta e fechamento"],
    ["Usar historico real", "treinar com padroes ja vistos em conversas e vendas"],
    ["Aplicar feedback", "o ajuste aparece no momento em que o corretor precisa usar"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 86 + (i % 2) * 820, 582 + Math.floor(i / 2) * 154, "light", 570));
}

// 24 Relationship
{
  const s = addSlide("dark", "Relacionamento", 24);
  title(s, "A experiencia premium continua\ndepois do lead.", "dark", 126, 70);
  sub(s, "A IA trabalha nos bastidores para a relacao parecer mais humana, nao menos.", "dark", 86, 340, 1050);
  [
    ["Memoria de relacionamento", "preferencias, familia, interesses, datas, historico e estilo de vida"],
    ["Reabordagem com sentido", "contexto certo, no momento certo, pelo motivo certo"],
    ["Curadoria individual", "noticias, teses, oportunidades e conteudos compativeis com o perfil"],
    ["Presenca sem ansiedade", "a marca permanece proxima sem parecer popular ou agressiva"],
  ].forEach(([h, b], i) => bullet(s, i + 1, h, b, 86 + (i % 2) * 820, 582 + Math.floor(i / 2) * 154, "dark", 570));
}

// 25 Architecture and governance
{
  const s = addSlide("dark", "Arquitetura e governanca", 25);
  title(s, "Para gerar resultado,\na IA precisa de controle.", "dark", 126, 70);
  sub(s, "Dados, metodo, integracoes, permissoes e revisao humana entram no desenho desde o inicio.", "dark", 86, 340, 1100);
  const layersData = [
    ["Factual", "fonte de verdade: imoveis, clientes, historico e contexto"],
    ["Orquestracao", "planeja prioridade, gatilhos, escalonamento e proximos passos"],
    ["Acao", "executa tarefas com aprovacao humana"],
    ["Controle", "permissao, auditoria, seguranca e avaliacao"],
    ["Blocos", "rotinas reutilizaveis para reuniao, lead, oferta e objecao"],
  ];
  layersData.forEach(([h, b], i) => {
    const y = 520 + i * 75;
    rect(s, 86, y + 10, 12 + i * 12, 12, i === 3 ? C.red : C.gold);
    tx(s, h, 150, y, 310, 32, { mode: "dark", color: C.white, size: 27, bold: true });
    tx(s, b, 500, y + 2, 850, 32, { mode: "dark", color: C.concrete, size: 21 });
  });
  tx(s, "No alto padrao, inteligencia sem discricao vira risco.", 1240, 840, 480, 80, {
    mode: "dark",
    color: C.white,
    size: 34,
    lineSpacing: 1.05,
  });
}

// 26 Roadmap and future
{
  const s = addSlide("light", "Implantacao", 26);
  title(s, "Implementar por fases,\ncom resultado visivel em cada etapa.", "light", 132, 70);
  sub(s, "Comecar simples, gerar confianca e aumentar profundidade com dados reais.", "light", 86, 340, 900);
  const phases = [
    ["1. Fundacao", "materiais, tom, imoveis, base inicial e regras"],
    ["2. Piloto comercial", "WhatsApp, leads, simulacoes, reunioes e ofertas"],
    ["3. Marketing omnicanal", "landing pages, cohorts, conteudos e campanhas"],
    ["4. Performance", "dashboards, metricas, feedback e melhoria continua"],
  ];
  phases.forEach(([h, b], i) => {
    const x = 120 + i * 430;
    rect(s, x, 600, 4, 220, i === 0 ? C.red : C.gold);
    tx(s, h, x + 34, 602, 310, 36, { mode: "light", color: C.ink, size: 28, bold: true });
    tx(s, b, x + 34, 664, 300, 96, { mode: "light", color: C.mutedInk, size: 22, lineSpacing: 1.15 });
  });
  tx(s, "Em 3 meses: prioridade no dia do corretor. Em 1 ano: venda mais previsivel.", 86, 914, 980, 40, {
    mode: "light",
    color: C.ink,
    size: 28,
    bold: true,
  });
}

// 27 Close and sources
{
  const s = addSlide("dark", "Fechamento", 27);
  big(s, "A IA nao substitui\na relacao.", 86, 188, 760, 150, "dark", 82, C.white);
  big(s, "Ela prepara melhor\ncada relacao.", 86, 390, 760, 150, "dark", 74, C.gold);
  rect(s, 86, 594, 380, 8, C.red);
  tx(s, "No alto padrao, quem entende antes decide melhor.", 86, 668, 850, 50, {
    mode: "dark",
    color: C.white,
    size: 34,
  });
  tx(s, "E quem organiza melhor sua inteligencia vende com mais precisao.", 86, 728, 880, 50, {
    mode: "dark",
    color: C.concrete,
    size: 28,
  });
  tx(s, "Referencias verificadas", 1160, 250, 420, 30, {
    mode: "dark",
    color: C.gold,
    size: 20,
    bold: true,
  });
  [
    "McKinsey, 2026: agentic AI in real estate",
    "McKinsey, 2023: generative AI in real estate",
    "Salesforce, 2026: State of Sales, 7th Edition",
    "NAR, 2025: REALTORS Technology Survey",
    "ANPD, 2026: sandbox de IA e protecao de dados",
  ].forEach((src, i) => {
    bullet(s, i + 1, src, "", 1160, 318 + i * 80, "dark", 560);
  });
}

const pptxBlob = await PresentationFile.exportPptx(p);
await pptxBlob.save(`${OUT}/B-Living-IA-AUltimaIdeia.pptx`);

for (let i = 0; i < p.slides.count; i += 1) {
  const slide = p.slides.getItem(i);
  const png = await p.export({ format: "png", slide });
  await fs.writeFile(
    `${PREVIEWS}/slide-${String(i + 1).padStart(2, "0")}.png`,
    Buffer.from(await png.arrayBuffer()),
  );
}

console.log(`PPTX ${OUT}/B-Living-IA-AUltimaIdeia.pptx`);
console.log(`PREVIEWS ${PREVIEWS}`);
console.log(`SLIDES ${p.slides.count}`);
