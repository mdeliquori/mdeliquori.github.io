// Mobile nav toggle
const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");

if (toggle && links) {
  toggle.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });

  // Close the menu after picking a link
  links.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      links.classList.remove("open");
      toggle.setAttribute("aria-expanded", false);
    })
  );
}

// Footer year
const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

// ===== Animations (GSAP) =====
// Everything here is an enhancement: without GSAP or with reduced motion the page is static.
const hasGsap = typeof window.gsap !== "undefined";
const canFlip = hasGsap && typeof window.Flip !== "undefined";

if (hasGsap) {
  gsap.registerPlugin(...[window.ScrollTrigger, window.SplitText, window.Flip].filter(Boolean));
}

const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Project filter: works without GSAP, animates with Flip when available
const filters = document.querySelectorAll(".filter");
const cards = document.querySelectorAll(".project-card");

filters.forEach((button) =>
  button.addEventListener("click", () => {
    const type = button.dataset.filter;
    filters.forEach((b) => b.setAttribute("aria-pressed", b === button));

    const state = canFlip && !reducedMotion() ? Flip.getState(cards) : null;
    cards.forEach((card) => {
      card.style.display = type === "all" || card.dataset.type === type ? "" : "none";
    });

    if (state) {
      Flip.from(state, {
        duration: 0.6,
        ease: "power2.inOut",
        absolute: true,
        onEnter: (els) => gsap.fromTo(els, { autoAlpha: 0, scale: 0.92 }, { autoAlpha: 1, scale: 1, duration: 0.5 }),
        onLeave: (els) => gsap.to(els, { autoAlpha: 0, scale: 0.92, duration: 0.4 })
      });
    }
  })
);

if (hasGsap) {
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    // Homepage intro: the drawing sheet sets up, then the name is lettered in
    const hero = document.querySelector(".hero");
    if (hero) {
      const name = hero.querySelector("h1");
      gsap.set(name, { autoAlpha: 0 });

      const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
      tl.from(".site-header", { yPercent: -100, duration: 0.6 })
        .fromTo(".sheet", { "--grid-alpha": 0 }, { "--grid-alpha": 1, duration: 1.2, ease: "none" }, 0)
        .from(".zones li", { autoAlpha: 0, duration: 0.3, stagger: 0.03 }, 0.2)
        .from(".title-block > div", { autoAlpha: 0, x: 12, duration: 0.4, stagger: 0.08 }, 0.5)
        .from([".hero-kicker", ".lead", ".hero-actions"], { autoAlpha: 0, y: 16, duration: 0.6, stagger: 0.12 }, 0.9);

      // Split once the web font is in, so the letters are measured correctly
      document.fonts.ready.then(() => {
        if (!window.SplitText) return gsap.set(name, { autoAlpha: 1 });
        const split = SplitText.create(name, { type: "chars", mask: "chars" });
        gsap.set(name, { autoAlpha: 1 });
        gsap.from(split.chars, { yPercent: 110, duration: 0.8, ease: "power3.out", stagger: 0.035, delay: Math.max(0, 0.4 - tl.time()) });
      });
    }

    // Project tiles arrive in a row as the grid scrolls in
    if (window.ScrollTrigger && cards.length) {
      gsap.set(cards, { autoAlpha: 0, y: 32 });
      ScrollTrigger.batch(cards, {
        start: "top 88%",
        once: true,
        onEnter: (batch) => gsap.to(batch, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power3.out", stagger: 0.1 })
      });
    }

    // Tile hover: the render drifts toward the pointer over its grid plate
    document.querySelectorAll(".card-plate").forEach((plate) => {
      const img = plate.querySelector("img");
      if (!img) return;
      const moveX = gsap.quickTo(img, "x", { duration: 0.5, ease: "power3.out" });
      const moveY = gsap.quickTo(img, "y", { duration: 0.5, ease: "power3.out" });
      const card = plate.closest(".project-card");

      card.addEventListener("pointerenter", () => gsap.to(img, { scale: 1.06, duration: 0.5, ease: "power3.out" }));
      card.addEventListener("pointermove", (e) => {
        const r = plate.getBoundingClientRect();
        moveX(((e.clientX - r.left) / r.width - 0.5) * 12);
        moveY(((e.clientY - r.top) / r.height - 0.5) * 12);
      });
      card.addEventListener("pointerleave", () => {
        moveX(0);
        moveY(0);
        gsap.to(img, { scale: 1, duration: 0.5, ease: "power3.out" });
      });
    });

    // Project page: title lettered in on load
    const projectTitle = document.querySelector(".model-title h1");
    if (projectTitle && window.SplitText) {
      gsap.set(projectTitle, { autoAlpha: 0 });
      document.fonts.ready.then(() => {
        const split = SplitText.create(projectTitle, { type: "chars", mask: "chars" });
        gsap.set(projectTitle, { autoAlpha: 1 });
        gsap.from(split.chars, { yPercent: 110, duration: 0.8, ease: "power3.out", stagger: 0.03 });
        gsap.from([".model-kicker", ".back-link"], { autoAlpha: 0, y: 12, duration: 0.6, stagger: 0.1 });
      });
    }

    // Project page: gallery figures and key figures reveal once
    if (window.ScrollTrigger) {
      gsap.utils.toArray(".gallery figure, .figures div").forEach((el) => {
        gsap.from(el, {
          autoAlpha: 0,
          y: 24,
          duration: 0.7,
          ease: "power3.out",
          scrollTrigger: { trigger: el, start: "top 90%", once: true }
        });
      });
    }
  });
}
