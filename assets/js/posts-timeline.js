// /posts/ timeline (layouts/posts/list.html): show cards in batches as the reader scrolls, keep the year rail in
// step with the year being read, and jump straight to a year when one is picked. Without this script every card
// is simply visible, so nothing here is required to read the page.
(() => {
  const BATCH = 12; // cards added per step; four rows of three on desktop
  const feed = document.querySelector(".pt-feed");
  const more = document.querySelector(".pt-more");
  if (!feed || !more) return;

  const items = [...feed.querySelectorAll(".pt-item")];
  const sections = [...feed.querySelectorAll(".pt-section")];
  const links = new Map([...document.querySelectorAll(".pt-year")].map((a) => [a.dataset.year, a]));
  const status = more.querySelector(".pt-status");
  const button = more.querySelector(".pt-button");
  const rail = document.querySelector(".pt-years");
  const smooth = matchMedia("(prefers-reduced-motion: no-preference)").matches ? "smooth" : "auto";
  let shown = 0;

  document.documentElement.classList.add("pt-js");
  items.forEach((el) => el.classList.add("is-pending"));

  // Reveal every card up to index `upTo` (exclusive), and any year section that now has a visible card.
  function reveal(upTo) {
    upTo = Math.min(upTo, items.length);
    for (let i = shown; i < upTo; i++) {
      items[i].classList.remove("is-pending");
      items[i].style.setProperty("--d", `${(i - shown) * 35}ms`); // stagger the fade-in within a batch
      items[i].classList.add("is-in");
    }
    shown = Math.max(shown, upTo);
    sections.forEach((s) => (s.hidden = s.querySelector(".pt-item.is-pending:first-child") !== null));
    const done = shown >= items.length;
    status.textContent = done ? `All ${items.length} posts shown.` : `Showing ${shown} of ${items.length} posts`;
    button.hidden = done;
    if (done) io.disconnect();
  }

  // Index just past the last card of a year, so jumping to 2019 also shows everything newer than it.
  const endOfYear = (section) => items.indexOf([...section.querySelectorAll(".pt-item")].pop()) + 1;

  function jumpTo(year, push) {
    const section = document.getElementById(`y${year}`);
    if (!section) return;
    reveal(endOfYear(section));
    section.scrollIntoView({ behavior: push ? smooth : "auto", block: "start" });
    if (push) history.replaceState(null, "", `#y${year}`);
  }

  // Load the next batch a little before the reader reaches the bottom.
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) reveal(shown + BATCH);
  }, { rootMargin: "800px 0px" });

  // Scroll spy: the section crossing the upper part of the screen is the "current" year.
  const spy = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      links.forEach((a) => a.removeAttribute("aria-current"));
      const a = links.get(e.target.dataset.year);
      if (!a) continue;
      a.setAttribute("aria-current", "true");
      // Keep the active year visible in the rail when it scrolls sideways on small screens.
      rail.scrollTo({ left: a.offsetLeft - rail.clientWidth / 2 + a.clientWidth / 2, behavior: smooth });
    }
  }, { rootMargin: "-25% 0px -70% 0px" });

  links.forEach((a, year) => a.addEventListener("click", (ev) => { ev.preventDefault(); jumpTo(year, true); }));
  button.addEventListener("click", () => reveal(shown + BATCH));

  more.hidden = false;
  const fromHash = location.hash.match(/^#y(\d{4})$/);
  if (fromHash) jumpTo(fromHash[1], false); else reveal(BATCH);
  // At the very top no section has reached the spy's band yet, so start with the newest year highlighted.
  if (!fromHash) links.values().next().value?.setAttribute("aria-current", "true");
  io.observe(more);
  sections.forEach((s) => spy.observe(s));
})();
