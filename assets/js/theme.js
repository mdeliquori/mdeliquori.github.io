// Theme: follows the system until the visitor picks one with the toggle.
// Loaded in <head> so the saved theme applies before the first paint.
(() => {
  const root = document.documentElement;
  const system = window.matchMedia("(prefers-color-scheme: light)");

  let saved = null;
  try {
    saved = localStorage.getItem("theme");
  } catch (e) {
    // Storage blocked: the toggle still works for this page view
  }

  const apply = (theme) => {
    root.dataset.theme = theme;
    const button = document.querySelector(".theme-toggle");
    if (button) button.setAttribute("aria-label", theme === "light" ? "Switch to dark mode" : "Switch to light mode");
  };

  apply(saved === "light" || saved === "dark" ? saved : system.matches ? "light" : "dark");

  // Keep following the system while nothing is saved
  system.addEventListener("change", (e) => {
    if (!saved) apply(e.matches ? "light" : "dark");
  });

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".theme-toggle");
    if (!button) return;
    button.hidden = false;
    apply(root.dataset.theme);

    button.addEventListener("click", () => {
      saved = root.dataset.theme === "light" ? "dark" : "light";
      apply(saved);
      try {
        localStorage.setItem("theme", saved);
      } catch (e) {
        // Not remembered, but the switch still applies
      }
    });
  });
})();
