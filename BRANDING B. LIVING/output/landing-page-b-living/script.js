const header = document.querySelector(".site-header");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const setHeaderState = () => {
  if (!header) return;
  header.classList.toggle("is-scrolled", window.scrollY > 24);
};

setHeaderState();
window.addEventListener("scroll", setHeaderState, { passive: true });

const heroVideo = document.querySelector(".hero-video");

if (heroVideo) {
  if (reduceMotion) {
    heroVideo.removeAttribute("autoplay");
    heroVideo.pause();
  } else {
    heroVideo.play().catch(() => {
      heroVideo.classList.add("is-unavailable");
    });

    heroVideo.addEventListener("error", () => heroVideo.classList.add("is-unavailable"));

    window.setTimeout(() => {
      if (heroVideo.readyState === 0) {
        heroVideo.classList.add("is-unavailable");
      }
    }, 2800);
  }
}

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (event) => {
    const target = document.querySelector(anchor.getAttribute("href"));
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
  });
});

const revealTargets = document.querySelectorAll(
  "main > section:not(.hero), .method-list article, .audience-grid article, .proof-list div",
);

if (reduceMotion || !("IntersectionObserver" in window)) {
  revealTargets.forEach((element) => element.classList.add("is-visible"));
} else {
  revealTargets.forEach((element) => element.classList.add("reveal"));

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -12% 0px", threshold: 0.12 },
  );

  revealTargets.forEach((element) => revealObserver.observe(element));
}

const parallaxTargets = document.querySelectorAll(
  ".hero-video, .hero-fallback, .guided-image img, .final-bg img, .image-rail img",
);

parallaxTargets.forEach((element) => element.classList.add("parallax-media"));

let ticking = false;

const updateParallax = () => {
  ticking = false;
  if (reduceMotion) return;

  parallaxTargets.forEach((element) => {
    const rect = element.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > window.innerHeight) return;

    const progress = (rect.top + rect.height / 2 - window.innerHeight / 2) / window.innerHeight;
    const offset = Math.max(-18, Math.min(18, progress * -22));
    element.style.transform = `scale(1.03) translate3d(0, ${offset}px, 0)`;
  });
};

const requestParallaxUpdate = () => {
  if (ticking) return;
  ticking = true;
  window.requestAnimationFrame(updateParallax);
};

if (!reduceMotion) {
  updateParallax();
  window.addEventListener("scroll", requestParallaxUpdate, { passive: true });
  window.addEventListener("resize", requestParallaxUpdate);
}
