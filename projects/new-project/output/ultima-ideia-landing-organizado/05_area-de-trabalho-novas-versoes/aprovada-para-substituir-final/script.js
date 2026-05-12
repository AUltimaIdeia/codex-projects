const hero = document.querySelector(".hero");
const diagnosis = document.querySelector(".diagnosis");
const method = document.querySelector(".method");
const form = document.querySelector(".submission-form");
const whatsappButton = document.querySelector(".whatsapp-button");

const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

function updateMotion() {
  const viewportHeight = window.innerHeight || 1;

  if (hero) {
    const rect = hero.getBoundingClientRect();
    const progress = clamp(-rect.top / Math.max(rect.height, 1), 0, 1);
    hero.style.setProperty("--hero-parallax", `${progress * 46}px`);
  }

  if (diagnosis) {
    const rect = diagnosis.getBoundingClientRect();
    const progress = clamp((viewportHeight - rect.top) / (viewportHeight + rect.height), 0, 1);
    diagnosis.style.setProperty("--diagnosis-parallax", `${(progress - 0.5) * 34}px`);
    diagnosis.style.setProperty("--diagnosis-card-y", `${(1 - progress) * 16}px`);
  }

  if (method) {
    const rect = method.getBoundingClientRect();
    const progress = clamp((viewportHeight - rect.top) / (viewportHeight + rect.height * 0.4), 0, 1);
    method.style.setProperty("--method-line-scale", progress.toFixed(3));
  }
}

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

if (!reducedMotion.matches) {
  updateMotion();
  window.addEventListener("scroll", updateMotion, { passive: true });
  window.addEventListener("resize", updateMotion);
} else if (method) {
  method.style.setProperty("--method-line-scale", "1");
}

function openWhatsapp() {
  if (!whatsappButton) {
    return;
  }

  const url = whatsappButton.dataset.whatsappUrl;

  if (url) {
    window.location.href = url;
  }
}

whatsappButton?.addEventListener("click", openWhatsapp);

form?.addEventListener("submit", (event) => {
  event.preventDefault();
  openWhatsapp();
});
