// Hardware project stage (ORYZO-style): the stage pins, the model turns a full
// 360 degrees as you scroll, and the text beside it steps through .model-step items.
// Without GSAP, or with reduced motion, the steps stay a static list and the
// model can be orbited by hand.
(() => {
  const stage = document.querySelector(".model-stage");
  const viewer = stage && stage.querySelector("model-viewer");
  if (!stage || !viewer || typeof window.gsap === "undefined" || typeof window.ScrollTrigger === "undefined") {
    if (viewer) viewer.setAttribute("camera-controls", "");
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  const root = document.documentElement;
  const steps = gsap.utils.toArray(".model-step", stage);
  const count = stage.querySelector(".model-count");
  const bar = stage.querySelector(".model-bar span");
  const header = document.querySelector(".site-header");
  const pad = (n) => String(n).padStart(2, "0");

  // Camera pitch: near top-down at the start, settling to a 3/4 view
  const PITCH_START = 8;
  const PITCH_END = 64;

  const mm = gsap.matchMedia();

  mm.add({ motion: "(prefers-reduced-motion: no-preference)", small: "(max-width: 720px)" }, (context) => {
    const { motion, small } = context.conditions;

    if (!motion) {
      viewer.setAttribute("camera-controls", "");
      return () => viewer.removeAttribute("camera-controls");
    }

    root.classList.add("has-model-motion");
    viewer.removeAttribute("camera-controls");

    const view = { yaw: 0, pitch: PITCH_START };
    const render = () => {
      viewer.orientation = `0deg 0deg ${view.yaw}deg`;
      viewer.cameraOrbit = `0deg ${view.pitch}deg auto`;
    };
    render();

    let current = 0;
    const setCount = (i) => {
      if (count && i !== current) count.textContent = `${pad(i + 1)} / ${pad(steps.length)}`;
      current = i;
    };
    if (count) count.textContent = `${pad(1)} / ${pad(steps.length)}`;

    gsap.set(steps, { autoAlpha: 0 });
    gsap.set(steps[0], { autoAlpha: 1 });

    // One unit of timeline per step; the scroll distance scales with the step count
    const tl = gsap.timeline({
      defaults: { ease: "none" },
      scrollTrigger: {
        trigger: stage,
        start: () => `top ${header ? header.offsetHeight : 0}px`,
        end: () => `+=${window.innerHeight * steps.length * (small ? 0.75 : 1)}`,
        pin: true,
        scrub: 1,
        invalidateOnRefresh: true,
        onUpdate: (self) => setCount(Math.min(steps.length - 1, Math.floor(self.progress * steps.length)))
      }
    });

    tl.to(view, { yaw: 360, duration: steps.length, onUpdate: render }, 0)
      .to(view, { pitch: PITCH_END, duration: 1, ease: "power2.inOut", onUpdate: render }, 0);

    if (bar) tl.to(bar, { scaleX: 1, duration: steps.length }, 0);

    // Text swap centred on each step boundary
    steps.forEach((step, i) => {
      if (i === 0) return;
      tl.to(steps[i - 1], { autoAlpha: 0, y: -24, duration: 0.18, ease: "power2.in" }, i - 0.2)
        .fromTo(step, { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 0.2, ease: "power2.out" }, i);
    });

    return () => {
      root.classList.remove("has-model-motion");
      gsap.set(steps, { clearProps: "all" });
      viewer.orientation = "0deg 0deg 0deg";
      viewer.cameraOrbit = `0deg ${PITCH_END}deg auto`;
    };
  });
})();
