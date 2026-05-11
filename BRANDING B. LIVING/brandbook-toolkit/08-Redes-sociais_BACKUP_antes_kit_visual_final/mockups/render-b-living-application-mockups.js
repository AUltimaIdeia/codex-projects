const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const OUT = __dirname;
const logoMainDark = "../../02-Logos/LOGO%20PRINCIPAL/SVG/B.%20LIVING%20LOGO%20-%20BEGE%20CLARO.svg";
const logoMainLight = "../../02-Logos/LOGO%20PRINCIPAL/SVG/B.%20LIVING%20LOGO%20-%20AZUL%20ESCURO.svg";
const logoCompactDark = "../../02-Logos/LOGO%20COMPACTA/SVG/Logo%20B.%20LIVING%20COMPACTA%20-%20BEGE%20CLARO.svg";
const logoCompactLight = "../../02-Logos/LOGO%20COMPACTA/SVG/Logo%20B.%20LIVING%20COMPACTA%20-%20AZUL%20ESCURO.svg";

const baseCss = `
  :root {
    --navy: oklch(16.5% 0.048 245);
    --navy-deep: oklch(12.5% 0.035 250);
    --navy-soft: oklch(22% 0.048 240);
    --paper: oklch(92% 0.015 82);
    --paper-soft: oklch(84% 0.018 82);
    --paper-dim: oklch(70% 0.018 82);
    --petrol: oklch(42% 0.055 205);
    --stone: oklch(37% 0.012 238);
    --brass: oklch(68% 0.055 78);
    --brass-soft: oklch(76% 0.045 80);
    --ink: oklch(15% 0.04 245);
    --line: oklch(92% 0.015 82 / 0.18);
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; width: 100%; min-height: 100%; background: var(--navy-deep); }
  body { display: grid; place-items: center; font-family: "Segoe UI", Arial, sans-serif; }
  .board {
    position: relative;
    width: 3840px;
    height: 2160px;
    overflow: hidden;
    color: var(--paper);
    background:
      radial-gradient(circle at 16% 14%, oklch(31% 0.07 225 / 0.48), transparent 30%),
      radial-gradient(circle at 88% 72%, oklch(36% 0.055 205 / 0.26), transparent 28%),
      linear-gradient(145deg, oklch(18% 0.052 242), oklch(10.8% 0.03 252) 70%);
  }
  .board::before {
    content: "";
    position: absolute;
    inset: 0;
    opacity: 0.38;
    background-image:
      linear-gradient(oklch(92% 0.015 82 / 0.035) 1px, transparent 1px),
      linear-gradient(90deg, oklch(92% 0.015 82 / 0.035) 1px, transparent 1px);
    background-size: 96px 96px;
  }
  .board::after {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.25;
    background: radial-gradient(circle at 50% 50%, transparent 0 62%, oklch(2% 0.02 250 / 0.42) 100%);
  }
  .frame { position: absolute; inset: 70px; z-index: 1; border: 1px solid var(--line); }
  .logo-main { position: absolute; z-index: 3; left: 150px; top: 128px; width: 520px; }
  .label {
    color: var(--brass-soft);
    font-size: 24px;
    font-weight: 650;
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  h1, h2, h3, p { margin: 0; }
  .display {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 400;
    line-height: 0.92;
    letter-spacing: 0;
  }
  .body-copy { color: var(--paper-soft); font-size: 34px; line-height: 1.32; font-weight: 350; }
  .paper { background: var(--paper); color: var(--ink); }
  .thin { border: 1px solid var(--line); }
  .rule { height: 1px; background: linear-gradient(90deg, var(--brass), transparent); }
  .logo-small { width: 120px; height: auto; }
`;

const mapSvg = `
  <svg class="map-svg" viewBox="0 0 720 560" aria-hidden="true">
    <path d="M72 142 H640 V480 H120 V222 H560 V420 H214 V302 H470" fill="none" stroke="oklch(92% 0.015 82 / 0.23)" stroke-width="2"/>
    <path d="M96 500 C178 382 218 310 340 250 C478 182 548 112 650 56" fill="none" stroke="oklch(68% 0.055 78 / 0.72)" stroke-width="3"/>
    <path d="M112 404 H610 M140 324 H542 M170 246 H610" fill="none" stroke="oklch(92% 0.015 82 / 0.11)" stroke-width="2"/>
    <circle cx="142" cy="432" r="9" fill="oklch(76% 0.045 80)"/>
    <circle cx="342" cy="250" r="9" fill="oklch(76% 0.045 80)"/>
    <circle cx="584" cy="98" r="9" fill="oklch(76% 0.045 80)"/>
  </svg>`;

const html = (title, body) => `<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"/><title>${title}</title><style>${baseCss}${body.css || ""}</style></head>
<body><main class="board">${body.html}</main></body></html>`;

const mockups = [
  {
    slug: "mockup-01-instagram-grid-autoridade",
    title: "Instagram - Autoridade Antes Do Produto",
    css: `
      .headline { position:absolute; z-index:3; left:150px; top:440px; width:1120px; font-size:132px; }
      .intro { position:absolute; z-index:3; left:154px; top:885px; width:920px; }
      .phone { position:absolute; z-index:3; right:180px; top:170px; width:1180px; height:1820px; border:1px solid var(--line); background:oklch(9% 0.03 250 / .45); padding:74px; }
      .profile { display:flex; align-items:center; gap:42px; padding-bottom:48px; border-bottom:1px solid var(--line); }
      .avatar { width:150px; height:150px; border:1px solid var(--line); display:grid; place-items:center; }
      .avatar img { width:94px; }
      .handle { font-size:38px; color:var(--paper); }
      .bio { color:var(--paper-soft); margin-top:10px; font-size:24px; line-height:1.35; }
      .highlights { display:grid; grid-template-columns:repeat(6, 1fr); gap:22px; margin:42px 0 54px; }
      .highlight { text-align:center; color:var(--paper-dim); font-size:18px; letter-spacing:.06em; }
      .dot { width:82px; height:82px; border:1px solid var(--brass); margin:0 auto 14px; display:grid; place-items:center; }
      .dot img { width:42px; }
      .grid { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }
      .post { aspect-ratio:1; border:1px solid var(--line); padding:32px; display:flex; flex-direction:column; justify-content:space-between; background:oklch(17% 0.035 245 / .74); }
      .post.paper { background:var(--paper); color:var(--ink); }
      .post .k { color:var(--brass-soft); font-size:17px; letter-spacing:.16em; text-transform:uppercase; font-weight:650; }
      .post .t { font-family:Georgia,serif; font-size:40px; line-height:.98; }
      .post.paper .k { color:var(--petrol); }
      .left-list { position:absolute; z-index:3; left:154px; bottom:190px; width:960px; display:grid; gap:24px; }
      .left-list div { border-top:1px solid var(--line); padding-top:24px; display:grid; grid-template-columns:140px 1fr; gap:26px; color:var(--paper-soft); font-size:28px; }
      .left-list strong { color:var(--brass-soft); font-size:20px; letter-spacing:.18em; }
    `,
    html: `
      <div class="frame"></div><img class="logo-main" src="${logoMainDark}" />
      <h1 class="display headline">Autoridade antes do produto.</h1>
      <p class="body-copy intro">Um perfil que conduz a percep&ccedil;&atilde;o: Rafael, equipe, m&eacute;todo, cidade e oportunidades com tese.</p>
      <section class="phone">
        <div class="profile"><div class="avatar"><img src="${logoCompactDark}"/></div><div><div class="handle">@b.livingfloripa</div><div class="bio">Curadoria para decis&otilde;es imobili&aacute;rias de alto padr&atilde;o.<br/>Rafael Bittencourt + equipe. Florian&oacute;polis com leitura, crit&eacute;rio e confian&ccedil;a.</div></div></div>
        <div class="highlights">${["Comece","Rafael","Equipe","Metodo","Floripa","Invest"].map(x=>`<div class="highlight"><div class="dot"><img src="${logoCompactDark}"/></div>${x}</div>`).join("")}</div>
        <div class="grid">
          ${[
            ["paper","Manifesto","Antes do imovel, vem a decisao."],["","Rafael","Le o mercado"],["","Equipe","Preparo em operacao"],
            ["","Floripa","A cidade como ativo"],["paper","Metodo","Criterio nao e detalhe"],["","Produto","Com tese"],
            ["","Construtoras","Acesso e relacao"],["","Prova","VGV autorizado"],["paper","Contato","Analise antes da oferta"]
          ].map(([c,k,t])=>`<article class="post ${c}"><div class="k">${k}</div><div class="t">${t}</div></article>`).join("")}
        </div>
      </section>
      <section class="left-list"><div><strong>01</strong><span>Instagram como jornada de confian&ccedil;a, n&atilde;o cat&aacute;logo.</span></div><div><strong>02</strong><span>Destaques ordenados para explicar, provar e conduzir.</span></div><div><strong>03</strong><span>Produto aparece como consequ&ecirc;ncia da curadoria.</span></div></section>`
  },
  {
    slug: "mockup-02-apresentacao-dossie-de-decisao",
    title: "Apresentacao Comercial - Dossie De Decisao",
    css: `
      .title { position:absolute; z-index:3; left:150px; top:420px; width:1040px; font-size:126px; }
      .copy { position:absolute; z-index:3; left:154px; top:820px; width:850px; }
      .deck { position:absolute; z-index:3; right:150px; top:170px; width:1900px; height:1680px; }
      .slide { position:absolute; border:1px solid var(--line); }
      .s1 { left:0; top:180px; width:920px; height:1220px; padding:84px; background:var(--paper); color:var(--ink); }
      .s2 { right:0; top:0; width:1060px; height:700px; padding:70px; background:oklch(15% 0.04 245 / .92); }
      .s3 { right:160px; bottom:0; width:1080px; height:780px; padding:70px; background:oklch(18% 0.042 242 / .88); }
      .s1 img { width:420px; }
      .s1 h2 { margin-top:420px; font-size:86px; }
      .s1 p { margin-top:34px; color:oklch(24% 0.04 245); font-size:31px; line-height:1.32; }
      .s2 h3,.s3 h3 { font-size:66px; }
      .s2 p,.s3 p { margin-top:36px; color:var(--paper-soft); font-size:31px; line-height:1.35; }
      .map-svg { position:absolute; right:64px; bottom:48px; width:520px; height:400px; opacity:.75; }
      .metrics { display:grid; grid-template-columns:repeat(3,1fr); gap:28px; margin-top:70px; }
      .metric { border-top:1px solid var(--brass); padding-top:22px; color:var(--paper-soft); font-size:24px; }
      .metric strong { display:block; color:var(--paper); font-family:Georgia,serif; font-size:48px; font-weight:400; }
    `,
    html: `
      <div class="frame"></div><img class="logo-main" src="${logoMainDark}" />
      <h1 class="display title">Dossi&ecirc; de decis&atilde;o.</h1>
      <p class="body-copy copy">Uma apresenta&ccedil;&atilde;o comercial que organiza tese, cidade, produto, timing e crit&eacute;rio. Menos PDF de venda. Mais material de orienta&ccedil;&atilde;o patrimonial.</p>
      <section class="deck">
        <article class="slide s1"><img src="${logoMainLight}"/><h2 class="display">Curadoria imobili&aacute;ria para quem decide com crit&eacute;rio.</h2><p>Apresenta&ccedil;&atilde;o para cliente/investidor. Florian&oacute;polis, tese, produto e pr&oacute;ximo passo.</p></article>
        <article class="slide s2"><div class="label">Leitura territorial</div><h3 class="display">Por que este movimento importa agora?</h3><p>Antes de apresentar uma unidade, a B. Living contextualiza bairro, liquidez, desenvolvimento e momento de vida.</p>${mapSvg}</article>
        <article class="slide s3"><div class="label">Produto com tese</div><h3 class="display">O im&oacute;vel como consequ&ecirc;ncia da an&aacute;lise.</h3><p>Crit&eacute;rios vis&iacute;veis, recomenda&ccedil;&atilde;o objetiva e fechamento consultivo.</p><div class="metrics"><div class="metric"><strong>01</strong>Contexto</div><div class="metric"><strong>02</strong>Timing</div><div class="metric"><strong>03</strong>Decis&atilde;o</div></div></article>
      </section>`
  },
  {
    slug: "mockup-03-whatsapp-atendimento-consultivo",
    title: "WhatsApp - Atendimento Consultivo",
    css: `
      .headline { position:absolute; z-index:3; left:150px; top:410px; width:1050px; font-size:118px; }
      .copy { position:absolute; z-index:3; left:154px; top:805px; width:860px; }
      .phone { position:absolute; z-index:3; right:290px; top:150px; width:980px; height:1840px; border:1px solid var(--line); background:oklch(92% 0.015 82); color:var(--ink); padding:54px; }
      .top { display:flex; align-items:center; gap:28px; border-bottom:1px solid oklch(17% 0.045 245 / .16); padding-bottom:38px; }
      .top img { width:90px; }
      .top strong { font-size:32px; }
      .top span { display:block; margin-top:6px; color:oklch(36% 0.018 245); font-size:20px; }
      .chat { display:grid; gap:26px; margin-top:60px; }
      .bubble { max-width:760px; padding:30px 34px; border:1px solid oklch(17% 0.045 245 / .15); font-size:30px; line-height:1.32; }
      .me { margin-left:auto; background:oklch(16.5% 0.048 245); color:var(--paper); }
      .client { background:oklch(88% 0.018 82); }
      .analysis { margin-top:46px; padding:42px; background:var(--navy); color:var(--paper); }
      .analysis .label { font-size:18px; }
      .analysis h3 { margin-top:130px; font-size:58px; }
      .analysis p { margin-top:22px; color:var(--paper-soft); font-size:24px; line-height:1.34; }
      .left-notes { position:absolute; z-index:3; left:154px; bottom:210px; width:980px; display:grid; grid-template-columns:1fr 1fr; gap:34px; }
      .note { border-top:1px solid var(--line); padding-top:28px; color:var(--paper-soft); font-size:30px; line-height:1.3; }
      .note strong { display:block; color:var(--paper); font-family:Georgia,serif; font-size:58px; font-weight:400; margin-bottom:14px; }
    `,
    html: `
      <div class="frame"></div><img class="logo-main" src="${logoMainDark}" />
      <h1 class="display headline">Antes de te enviar op&ccedil;&otilde;es.</h1>
      <p class="body-copy copy">O atendimento tamb&eacute;m precisa carregar a marca: escuta, qualifica&ccedil;&atilde;o e recomenda&ccedil;&atilde;o com crit&eacute;rio.</p>
      <section class="phone">
        <div class="top"><img src="${logoCompactLight}"/><div><strong>B. Living Floripa</strong><span>curadoria imobili&aacute;ria de alto padr&atilde;o</span></div></div>
        <div class="chat">
          <div class="bubble client">Tenho interesse em comprar em Florian&oacute;polis. Voc&ecirc;s t&ecirc;m op&ccedil;&otilde;es?</div>
          <div class="bubble me">Temos. Mas antes de te enviar op&ccedil;&otilde;es, quero entender seu objetivo: moradia, investimento ou uma combina&ccedil;&atilde;o dos dois?</div>
          <div class="bubble client">Investimento com possibilidade de uso familiar.</div>
          <div class="bubble me">Perfeito. Vamos olhar territ&oacute;rio, liquidez, timing e perfil de produto antes de selecionar as unidades.</div>
        </div>
        <div class="analysis"><div class="label">An&aacute;lise preliminar</div><h3 class="display">Produto certo para o momento certo.</h3><p>Sele&ccedil;&atilde;o enviada com contexto, n&atilde;o como cat&aacute;logo.</p></div>
      </section>
      <section class="left-notes"><article class="note"><strong>Tom</strong>Consultivo, seguro e humano.</article><article class="note"><strong>Fun&ccedil;&atilde;o</strong>Converter sem parecer venda comum.</article></section>`
  },
  {
    slug: "mockup-04-kit-rafael-equipe-autoridade",
    title: "Kit Rafael e Equipe - Autoridade Distribuida",
    css: `
      .headline { position:absolute; z-index:3; left:150px; top:430px; width:1160px; font-size:122px; }
      .copy { position:absolute; z-index:3; left:154px; top:835px; width:850px; }
      .cards { position:absolute; z-index:3; right:150px; top:150px; width:2000px; height:1800px; display:grid; grid-template-columns:1.1fr 1fr 1fr; grid-template-rows:1fr 1fr; gap:34px; }
      .person { border:1px solid var(--line); padding:56px; background:oklch(15% 0.038 245 / .78); display:flex; flex-direction:column; justify-content:space-between; }
      .rafael { grid-row:span 2; background:var(--paper); color:var(--ink); }
      .person .role { color:var(--brass-soft); font-size:20px; font-weight:650; letter-spacing:.16em; text-transform:uppercase; }
      .rafael .role { color:var(--petrol); }
      .person h3 { font-size:76px; }
      .rafael h3 { font-size:108px; }
      .person p { color:var(--paper-soft); font-size:29px; line-height:1.32; }
      .rafael p { color:oklch(28% 0.03 245); font-size:34px; }
      .portrait { height:420px; border:1px solid oklch(17% 0.045 245 / .16); background:linear-gradient(145deg, oklch(16% 0.04 245 / .12), transparent); display:grid; place-items:center; }
      .portrait img { width:140px; }
      .person:not(.rafael) .portrait { border-color:var(--line); background:linear-gradient(145deg, oklch(42% 0.055 205 / .16), transparent); }
      .system { position:absolute; z-index:3; left:154px; bottom:190px; width:980px; border-top:1px solid var(--line); padding-top:34px; color:var(--paper-soft); font-size:30px; line-height:1.35; }
      .system strong { color:var(--paper); }
    `,
    html: `
      <div class="frame"></div><img class="logo-main" src="${logoMainDark}" />
      <h1 class="display headline">Autoridade distribu&iacute;da.</h1>
      <p class="body-copy copy">Rafael puxa a tese. A equipe sustenta o m&eacute;todo. Cada especialista aparece com uma for&ccedil;a clara, sem linguagem de corretor gen&eacute;rico.</p>
      <section class="cards">
        <article class="person rafael"><div><div class="role">Fundador / leitura de mercado</div><h3 class="display">Rafael Bittencourt</h3></div><div class="portrait"><img src="${logoCompactLight}"/></div><p>18 anos de mercado, lideran&ccedil;a comercial e vis&atilde;o sobre Florian&oacute;polis.</p></article>
        ${[
          ["Marta","seguran&ccedil;a relacional e credibilidade"],["Juan","energia de execu&ccedil;&atilde;o e evolu&ccedil;&atilde;o"],["Uberdan","presen&ccedil;a comercial e conex&atilde;o pr&aacute;tica"],["Fabiano","vis&atilde;o de oportunidade e investimento"]
        ].map(([n,c])=>`<article class="person"><div><div class="role">Equipe B. Living</div><h3 class="display">${n}</h3></div><div class="portrait"><img src="${logoCompactDark}"/></div><p>${c}</p></article>`).join("")}
      </section>
      <div class="system"><strong>Sistema replic&aacute;vel:</strong> cada corretor ganha presen&ccedil;a sem romper a marca. A assinatura individual serve &agrave; autoridade coletiva.</div>`
  },
  {
    slug: "mockup-05-experiencia-presencial-mesa-de-decisao",
    title: "Experiencia Presencial - Mesa De Decisao",
    css: `
      .headline { position:absolute; z-index:3; left:150px; top:420px; width:1160px; font-size:126px; }
      .copy { position:absolute; z-index:3; left:154px; top:830px; width:880px; }
      .scene { position:absolute; z-index:3; right:150px; top:150px; width:2050px; height:1810px; }
      .wall { position:absolute; inset:0 0 560px 0; border:1px solid var(--line); background:linear-gradient(145deg, oklch(15% 0.04 245 / .9), oklch(9% 0.03 250 / .7)); display:grid; place-items:center; }
      .wall img { width:820px; }
      .table { position:absolute; left:80px; right:80px; bottom:80px; height:680px; border:1px solid var(--line); background:oklch(92% 0.015 82); color:var(--ink); }
      .folder { position:absolute; left:90px; top:80px; width:760px; height:500px; border:1px solid oklch(17% 0.045 245 / .16); padding:56px; }
      .folder img { width:330px; }
      .folder h3 { margin-top:96px; width:360px; font-size:44px; line-height:1.02; }
      .invite { position:absolute; right:90px; top:80px; width:720px; height:500px; background:var(--navy); color:var(--paper); padding:56px; border:1px solid oklch(17% 0.045 245 / .16); }
      .invite h3 { margin-top:150px; font-size:68px; }
      .invite p { margin-top:24px; color:var(--paper-soft); font-size:27px; line-height:1.32; }
      .plate { position:absolute; left:900px; bottom:90px; width:520px; height:140px; background:oklch(15% 0.04 245); color:var(--paper); display:flex; align-items:center; justify-content:center; font-size:26px; letter-spacing:.12em; text-transform:uppercase; }
      .notes { position:absolute; z-index:3; left:154px; bottom:190px; width:980px; display:grid; gap:24px; }
      .notes div { border-top:1px solid var(--line); padding-top:24px; color:var(--paper-soft); font-size:30px; line-height:1.32; }
      .notes strong { color:var(--paper); font-family:Georgia,serif; font-size:58px; font-weight:400; display:block; margin-bottom:12px; }
    `,
    html: `
      <div class="frame"></div><img class="logo-main" src="${logoMainDark}" />
      <h1 class="display headline">Mesa de decis&atilde;o B. Living.</h1>
      <p class="body-copy copy">O ponto f&iacute;sico e os eventos precisam parecer extens&atilde;o da curadoria: ambiente de leitura, rela&ccedil;&atilde;o e condu&ccedil;&atilde;o.</p>
      <section class="scene">
        <div class="wall"><img src="${logoMainDark}"/></div>
        <div class="table">
          <article class="folder"><img src="${logoMainLight}"/><h3 class="display">Dossi&ecirc; de decis&atilde;o</h3></article>
          <article class="invite"><div class="label">Wine & Living</div><h3 class="display">Cidade, mercado e patrim&ocirc;nio.</h3><p>Encontro para leitura de oportunidades com parceiros e clientes.</p></article>
          <div class="plate">A cidade &eacute; parte da decis&atilde;o</div>
        </div>
      </section>
      <section class="notes"><div><strong>Presen&ccedil;a</strong>Fachada, mesa, pasta e convite sem ostenta&ccedil;&atilde;o.</div><div><strong>Fun&ccedil;&atilde;o</strong>Transformar atendimento presencial em prova de marca.</div></section>`
  }
];

async function main() {
  const browser = await chromium.launch({ headless: true });
  for (const mockup of mockups) {
    const htmlPath = path.join(OUT, `${mockup.slug}.html`);
    const pngPath = path.join(OUT, `${mockup.slug}.png`);
    fs.writeFileSync(htmlPath, html(mockup.title, mockup), "utf8");
    const page = await browser.newPage({ viewport: { width: 3840, height: 2160 }, deviceScaleFactor: 1 });
    await page.goto(`file://${htmlPath.replace(/\\/g, "/")}`, { waitUntil: "networkidle" });
    await page.screenshot({ path: pngPath, fullPage: false, type: "png" });
    await page.close();
    console.log(pngPath);
  }
  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
