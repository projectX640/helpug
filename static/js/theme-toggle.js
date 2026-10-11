(function () {
  const toggle = document.querySelector("[data-theme-toggle]");
  if (!toggle) return;

  const root = document.documentElement;
  const storageKey = "rapid-response-theme";

  function applyTheme(theme) {
    const dark = theme === "dark";
    root.dataset.theme = dark ? "dark" : "light";
    toggle.setAttribute("aria-pressed", String(dark));
    toggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    toggle.querySelector(".theme-toggle-icon").textContent = dark ? "☀" : "☾";
    toggle.querySelector(".theme-toggle-label").textContent = dark ? "Light mode" : "Dark mode";
  }

  let savedTheme = "light";
  try {
    savedTheme = window.localStorage.getItem(storageKey) || "light";
  } catch (error) {}

  applyTheme(savedTheme);
  toggle.addEventListener("click", function () {
    const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    try {
      window.localStorage.setItem(storageKey, nextTheme);
    } catch (error) {}
  });
}());
