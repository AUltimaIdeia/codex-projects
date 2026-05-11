const directions = {
  manifesto: {
    series: "LIGHT 01",
    small: "A luz não decora.",
    title: "Ela conduz a visão.",
    line: "No ZEISS Vision Center, cada reflexo existe para aproximar precisão, conforto e escolha.",
    footer: "ZEISS / VISION CENTER",
    notesTitle: "Arquitetura Da Luz",
    notesCopy:
      "Uma peça vertical com atmosfera premium, luz recortando a loja e azul óptico entrando como assinatura. A mensagem posiciona o espaço como parte da tecnologia, não só como ponto de venda.",
    tone: "Tom: cinematográfico, preciso, premium",
    format: "Formato: story vertical ou feed 4:5",
    move: "Movimento: feixe de luz revelando a frase"
  },
  sistema: {
    series: "OPTICS 02",
    small: "Não é só uma armação.",
    title: "É precisão vestida no rosto.",
    line: "Lentes, medidas e design trabalham juntos para transformar escolha em performance visual.",
    footer: "ZEISS / PERSONAL OPTICS",
    notesTitle: "Precisão Que Veste",
    notesCopy:
      "A direção mais orientada a produto. O post torna os óculos desejáveis sem perder a autoridade técnica: forma, ajuste, lente e precisão aparecem como uma única experiência.",
    tone: "Tom: técnico, elegante, sensorial",
    format: "Formato: carrossel editorial de 4 telas",
    move: "Movimento: foco passando da lente para o rosto"
  },
  ruptura: {
    series: "CENTER 03",
    small: "Você não compra visão.",
    title: "Você passa por um ritual de precisão.",
    line: "Do primeiro teste ao ajuste final, a experiência ZEISS transforma atendimento em alta tecnologia humana.",
    footer: "ZEISS / PRECISION RITUAL",
    notesTitle: "Vision Center Ritual",
    notesCopy:
      "A opção mais experiencial e memorável. Em vez de vender produto, vende travessia: entrar em um ambiente de precisão, ser guiado e sair com uma visão calibrada.",
    tone: "Tom: imersivo, premium, humano",
    format: "Formato: reels + capa estática",
    move: "Movimento: câmera atravessando a loja"
  }
};

const cards = document.querySelectorAll(".direction-card");
const fields = {
  series: document.querySelector("#post-series"),
  small: document.querySelector("#post-small"),
  title: document.querySelector("#post-title"),
  line: document.querySelector("#post-line"),
  footer: document.querySelector("#post-footer-left"),
  notesTitle: document.querySelector("#notes-title"),
  notesCopy: document.querySelector("#notes-copy"),
  tone: document.querySelector("#brief-tone"),
  format: document.querySelector("#brief-format"),
  move: document.querySelector("#brief-move")
};

function setDirection(key) {
  const direction = directions[key];
  document.body.dataset.direction = key;

  cards.forEach((card) => {
    card.classList.toggle("selected", card.dataset.direction === key);
  });

  fields.series.textContent = direction.series;
  fields.small.textContent = direction.small;
  fields.title.textContent = direction.title;
  fields.line.textContent = direction.line;
  fields.footer.textContent = direction.footer;
  fields.notesTitle.textContent = direction.notesTitle;
  fields.notesCopy.textContent = direction.notesCopy;
  fields.tone.textContent = direction.tone;
  fields.format.textContent = direction.format;
  fields.move.textContent = direction.move;
}

cards.forEach((card) => {
  card.addEventListener("click", () => setDirection(card.dataset.direction));
});

setDirection("manifesto");
