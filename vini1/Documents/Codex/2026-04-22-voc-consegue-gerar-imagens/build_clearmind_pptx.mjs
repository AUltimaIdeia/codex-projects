import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = process.cwd();
const OUT = path.join(ROOT, "carrossel_clearmind_referencia");
const MEDIA = "C:\\Users\\vini1\\Downloads\\POST LENTE";

const W = 1080;
const H = 1350;
const C = {
  ink: "#111111",
  muted: "#5D6268",
  blue: "#0050A4",
  warm: "#F7F4EF",
  lightBlue: "#EAF3FF",
  brown: "#6F5545",
  line: "#D6D7D9",
  black: "#111111",
  white: "#FFFFFF",
};

const FONT = {
  title: "Arial",
  body: "Arial",
  serif: "Georgia",
};

async function readImageBlob(imagePath) {
  const bytes = await fs.readFile(imagePath);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function rect(slide, left, top, width, height, fill, line = { width: 0, fill }) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left, top, width, height },
    fill,
    line,
  });
}

function round(slide, left, top, width, height, fill, line = { width: 0, fill }) {
  return slide.shapes.add({
    geometry: "roundRect",
    position: { left, top, width, height },
    fill,
    line,
    adjustmentList: [{ name: "adj", formula: "val 10000" }],
  });
}

function text(slide, value, left, top, width, height, opts = {}) {
  const s = slide.shapes.add({
    geometry: "rect",
    position: { left, top, width, height },
    fill: "#FFFFFF00",
    line: { width: 0, fill: "#FFFFFF00" },
  });
  s.text = value;
  s.text.typeface = opts.typeface || FONT.body;
  s.text.fontSize = opts.size || 32;
  s.text.bold = Boolean(opts.bold);
  s.text.color = opts.color || C.ink;
  s.text.alignment = opts.align || "left";
  s.text.verticalAlignment = opts.valign || "top";
  s.text.insets = opts.insets || { left: 0, right: 0, top: 0, bottom: 0 };
  if (opts.autoFit) s.text.autoFit = opts.autoFit;
  return s;
}

function brandBar(slide, dark = false, page = "") {
  const color = dark ? C.white : C.ink;
  text(slide, "ÓPTICA REFERÊNCIA", 72, 58, 350, 40, { size: 28, bold: true, color });
  rect(slide, 720, 42, 110, 87, C.blue);
  text(slide, "ZEISS", 741, 67, 75, 35, {
    size: 28,
    bold: true,
    color: C.white,
    typeface: FONT.serif,
    align: "center",
  });
  text(slide, "ZVC", 852, 58, 130, 34, { size: 30, bold: true, color });
  text(slide, "by Óptica Referência", 852, 95, 190, 26, { size: 19, color });
  text(slide, page, 950, 1240, 65, 40, { size: 28, color: dark ? C.white : C.muted, align: "right" });
}

async function addImage(slide, imagePath, left, top, width, height, fit = "cover") {
  const img = slide.images.add({
    blob: await readImageBlob(imagePath),
    fit,
    alt: path.basename(imagePath),
  });
  img.position = { left, top, width, height };
  return img;
}

function slide1(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  brandBar(slide, false, "1/6");
  text(slide, "SAÚDE + TECNOLOGIA", 72, 232, 420, 36, { size: 26, bold: true, color: C.brown });
  text(slide, "Novas lentes ZEISS chegam ao Brasil para aliviar a rotina entre telas", 72, 292, 900, 210, {
    size: 62,
    bold: true,
    autoFit: "shrinkText",
  });
  rect(slide, 72, 515, 936, 2, C.line);
  text(slide, "A tecnologia ClearMind virou notícia na Veja e agora reforça uma exclusividade da Óptica Referência.", 72, 565, 880, 155, {
    size: 41,
    autoFit: "shrinkText",
  });
  round(slide, 72, 865, 936, 330, C.white, { width: 1.5, fill: C.line });
  return addImage(slide, path.join(MEDIA, "IMG_7090.JPEG"), 73, 866, 934, 328, "cover").then(() => {
    text(slide, "Arraste para entender o que muda na sua visão.", 72, 1235, 760, 42, { size: 28, bold: true });
  });
}

function slide2(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.warm;
  brandBar(slide, false, "2/6");
  text(slide, "O PROBLEMA", 72, 225, 300, 36, { size: 26, bold: true, color: C.brown });
  text(slide, "Sua mente também cansa quando seus olhos trabalham demais.", 72, 300, 900, 285, {
    size: 74,
    bold: true,
    autoFit: "shrinkText",
  });
  const items = [
    ["1", "Horas alternando celular, computador e ambientes diferentes."],
    ["2", "Foco constante em múltiplos estímulos digitais."],
    ["3", "Mais esforço para manter conforto, atenção e nitidez."],
  ];
  let y = 730;
  for (const [n, body] of items) {
    slide.shapes.add({ geometry: "ellipse", position: { left: 72, top: y + 12, width: 32, height: 32 }, fill: C.blue, line: { width: 0, fill: C.blue } });
    text(slide, n, 72, y + 11, 32, 32, { size: 22, bold: true, color: C.white, align: "center", valign: "middle" });
    text(slide, body, 128, y, 810, 72, { size: 41, autoFit: "shrinkText" });
    y += 146;
  }
  text(slide, "Não é só sobre enxergar. É sobre render melhor no dia a dia.", 72, 1215, 860, 45, { size: 28, bold: true });
}

async function slide3(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  brandBar(slide, false, "3/6");
  text(slide, "A TECNOLOGIA", 72, 215, 330, 36, { size: 26, bold: true, color: C.brown });
  text(slide, "ClearMind: lentes criadas para uma vida cada vez mais digital.", 72, 285, 900, 185, {
    size: 64,
    bold: true,
    autoFit: "shrinkText",
  });
  round(slide, 72, 610, 936, 420, C.white, { width: 1.5, fill: C.line });
  await addImage(slide, path.join(OUT, "03_card_video_lentes.png"), 73, 611, 934, 418, "cover");
  round(slide, 312, 798, 456, 70, C.blue);
  text(slide, "ENTRA VÍDEO DAS LENTES AQUI", 328, 817, 425, 34, { size: 28, bold: true, color: C.white, align: "center" });
  text(slide, "No Canva, substitua esta imagem pelo vídeo vertical ZEISS ClearMind.", 72, 1090, 890, 95, {
    size: 41,
    autoFit: "shrinkText",
  });
}

function slide4(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  brandBar(slide, false, "4/6");
  text(slide, "NA PRÁTICA", 72, 225, 300, 36, { size: 26, bold: true, color: C.brown });
  text(slide, "O benefício aparece na rotina, não só na armação.", 72, 292, 900, 265, {
    size: 74,
    bold: true,
    autoFit: "shrinkText",
  });
  const cards = [
    ["Conforto", "menos sensação de sobrecarga em dias intensos"],
    ["Foco", "mais facilidade para alternar entre telas e ambientes"],
    ["Qualidade de vida", "uma escolha visual pensada para o seu ritmo"],
  ];
  let y = 700;
  for (const [title, body] of cards) {
    round(slide, 72, y, 936, 150, C.lightBlue);
    text(slide, title, 112, y + 30, 250, 55, { size: 42, bold: true, color: C.blue });
    text(slide, body, 390, y + 28, 560, 92, { size: 41, autoFit: "shrinkText" });
    y += 185;
  }
}

function slide5(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.black;
  brandBar(slide, true, "5/6");
  text(slide, "EXCLUSIVIDADE", 72, 235, 340, 36, { size: 26, bold: true, color: "#CDBAAE" });
  text(slide, "Tecnologia alemã ZEISS com atendimento próximo da Referência.", 72, 310, 900, 245, {
    size: 70,
    bold: true,
    color: C.white,
    autoFit: "shrinkText",
  });
  rect(slide, 72, 742, 936, 2, "#404040");
  text(slide, "Aqui, você entende a lente certa para sua rotina antes de decidir.", 72, 810, 880, 190, {
    size: 58,
    bold: true,
    color: C.white,
    typeface: FONT.serif,
    autoFit: "shrinkText",
  });
  round(slide, 72, 1115, 590, 80, C.white);
  text(slide, "Agende sua avaliação", 108, 1137, 500, 45, { size: 40, bold: true, color: C.ink });
}

function slide6(presentation) {
  const slide = presentation.slides.add();
  slide.background.fill = C.warm;
  brandBar(slide, false, "6/6");
  rect(slide, 72, 265, 143, 108, C.blue);
  text(slide, "ZEISS", 88, 305, 110, 40, { size: 34, bold: true, color: C.white, typeface: FONT.serif, align: "center" });
  text(slide, "ClearMind", 72, 420, 700, 100, { size: 96, bold: true });
  text(slide, "Para quem vive entre telas, decisões e muitos estímulos.", 72, 535, 860, 145, {
    size: 58,
    bold: true,
    typeface: FONT.serif,
    autoFit: "shrinkText",
  });
  rect(slide, 72, 790, 936, 2, C.line);
  text(slide, "Conheça na Óptica Referência.", 72, 850, 850, 155, { size: 64, bold: true, autoFit: "shrinkText" });
  text(slide, "Post collab: ZEISS Vision Center by Óptica Referência + Óptica Referência", 72, 1080, 830, 82, {
    size: 28,
    color: C.muted,
    autoFit: "shrinkText",
  });
  text(slide, "CTA: chame no direct ou visite a loja.", 72, 1215, 760, 42, { size: 28, bold: true });
}

async function main() {
  await fs.mkdir(OUT, { recursive: true });
  const presentation = Presentation.create({ slideSize: { width: W, height: H } });
  await slide1(presentation);
  slide2(presentation);
  await slide3(presentation);
  slide4(presentation);
  slide5(presentation);
  slide6(presentation);

  const pptx = await PresentationFile.exportPptx(presentation);
  const output = path.join(OUT, "carrossel_clearmind_referencia_editavel.pptx");
  await pptx.save(output);
  console.log(output);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
