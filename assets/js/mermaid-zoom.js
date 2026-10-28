// Full-size viewer for Mermaid charts (layouts/shortcodes/mermaid.html). Mermaid renders each chart into its
// <pre> after load; once an SVG appears, the figure's "Open full size" button is shown. The viewer is a native
// <dialog> (Esc and a click outside close it) with zoom buttons, and a link that opens the SVG on its own.
(() => {
  const ZOOMS = [0.75, 1, 1.5, 2, 3];
  let dialog, stage, zoomLabel, svgLink, current, zoom = 1, blobUrl;

  function build() {
    dialog = document.createElement("dialog");
    dialog.className = "mz-dialog";
    dialog.innerHTML = `
      <div class="mz-bar">
        <button type="button" data-z="-1" aria-label="Zoom out">−</button>
        <span class="mz-zoom" aria-live="polite">100%</span>
        <button type="button" data-z="1" aria-label="Zoom in">+</button>
        <a class="mz-svg" target="_blank" rel="noopener">Open as SVG ↗</a>
        <button type="button" class="mz-close" aria-label="Close">✕</button>
      </div>
      <div class="mz-stage"></div>`;
    document.body.append(dialog);
    stage = dialog.querySelector(".mz-stage");
    zoomLabel = dialog.querySelector(".mz-zoom");
    svgLink = dialog.querySelector(".mz-svg");
    dialog.querySelector(".mz-close").addEventListener("click", () => dialog.close());
    dialog.querySelectorAll("[data-z]").forEach((b) => b.addEventListener("click", () => {
      const i = ZOOMS.indexOf(zoom) + Number(b.dataset.z);
      setZoom(ZOOMS[Math.max(0, Math.min(ZOOMS.length - 1, i))]);
    }));
    // A click on the backdrop lands on the dialog element itself, not on its contents.
    dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener("close", () => { stage.replaceChildren(); URL.revokeObjectURL(blobUrl); });
  }

  // Size the copy from its viewBox, so 100% means the chart's natural size, not the shrunken in-page one.
  function setZoom(z) {
    zoom = z;
    const [, , w, h] = current.getAttribute("viewBox").split(/[\s,]+/).map(Number);
    current.style.width = `${w * z}px`;
    current.style.height = `${h * z}px`;
    zoomLabel.textContent = `${Math.round(z * 100)}%`;
  }

  function open(svg) {
    if (!dialog) build();
    current = svg.cloneNode(true);
    current.removeAttribute("width");
    current.style.maxWidth = "none";
    stage.replaceChildren(current);

    // A standalone copy for the new tab. Charts are drawn for the page's theme, so paint the page background
    // behind it; otherwise light text from dark mode would sit on a white tab.
    const copy = svg.cloneNode(true);
    copy.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    copy.style.background = getComputedStyle(document.body).backgroundColor;
    copy.style.maxWidth = "none";
    blobUrl = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(copy)], { type: "image/svg+xml" }));
    svgLink.href = blobUrl;

    dialog.showModal();
    // Start at natural size, or smaller if that would not fit the screen.
    const [, , w] = current.getAttribute("viewBox").split(/[\s,]+/).map(Number);
    setZoom(w > stage.clientWidth ? 1 : ZOOMS.find((z) => w * z >= stage.clientWidth * 0.8) ?? 1.5);
  }

  function wire(fig) {
    const pre = fig.querySelector("pre.mermaid");
    const button = fig.querySelector(".mz-open");
    const ready = () => {
      const svg = pre.querySelector("svg[viewBox]");
      if (!svg) return false;
      button.hidden = false;
      button.addEventListener("click", () => open(svg));
      pre.addEventListener("click", () => open(svg));
      fig.classList.add("is-ready");
      return true;
    };
    if (ready()) return;
    const mo = new MutationObserver(() => { if (ready()) mo.disconnect(); });
    mo.observe(pre, { childList: true, subtree: true });
  }

  const start = () => document.querySelectorAll("figure.mz").forEach(wire);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
