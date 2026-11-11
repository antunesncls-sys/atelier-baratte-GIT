/* =====================================================================
   RIZ DJONDJON — interactions & rendu dynamique
   Aucune dépendance. Les données viennent de assets/js/config.js
   ===================================================================== */
(() => {
  "use strict";

  const C = window.RDJ_CONFIG;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pad = (n) => String(n).padStart(2, "0");
  const DAYS = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"];
  const MONTHS_SHORT = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."];
  const MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];

  document.documentElement.classList.add("js");

  /* ------------------------------------------------------------------
     1. Liens issus de la config
     ------------------------------------------------------------------ */
  $$("[data-link]").forEach((a) => {
    const url = C.links[a.dataset.link];
    if (url) a.href = url;
  });
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

  /* ------------------------------------------------------------------
     2. Titre lettre par lettre + préchargement
     ------------------------------------------------------------------ */
  $$(".split").forEach((el, i) => {
    const txt = el.textContent;
    el.textContent = "";
    el.setAttribute("aria-hidden", "true");
    [...txt].forEach((ch, j) => {
      const s = document.createElement("span");
      s.className = "ch";
      s.textContent = ch;
      s.style.transitionDelay = `${0.35 + i * 0.18 + j * 0.045}s`;
      el.appendChild(s);
    });
  });

  let ready = false;
  const setReady = () => {
    if (ready) return;
    ready = true;
    document.body.classList.add("is-ready");
    document.body.classList.remove("is-loading");
    $$(".hero .reveal").forEach((el, i) => {
      el.style.setProperty("--d", `${0.7 + i * 0.12}s`);
      el.classList.add("is-in");
    });
  };
  window.addEventListener("load", () => setTimeout(setReady, reduceMotion ? 0 : 900));
  setTimeout(setReady, 2600); // filet de sécurité

  /* ------------------------------------------------------------------
     3. En-tête, progression, barre mobile
     ------------------------------------------------------------------ */
  const header = $(".header");
  const progress = $(".progress");
  const actionBar = $(".action-bar");
  const hero = $(".hero");
  let lastY = 0;
  let ticking = false;

  const onScroll = () => {
    const y = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    header.classList.toggle("is-scrolled", y > 40);
    const menuOpen = document.body.classList.contains("menu-open");
    header.classList.toggle("is-hidden", !menuOpen && y > lastY && y > 400);
    actionBar.classList.toggle("is-visible", y > hero.offsetHeight * 0.6);
    lastY = y;
    parallax();
    ticking = false;
  };
  window.addEventListener("scroll", () => {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });

  /* ------------------------------------------------------------------
     4. Parallaxe
     ------------------------------------------------------------------ */
  const parallaxEls = reduceMotion ? [] : $$("[data-parallax]");
  function parallax() {
    const vh = window.innerHeight;
    parallaxEls.forEach((el) => {
      const r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      const speed = parseFloat(el.dataset.parallax) || 0;
      const offset = (r.top + r.height / 2 - vh / 2) * speed;
      const base = el.dataset.baseTransform ?? (el.dataset.baseTransform = getComputedStyle(el).transform === "none" ? "" : getComputedStyle(el).transform);
      el.style.transform = `translate3d(0, ${(-offset).toFixed(1)}px, 0) ${base}`;
    });
  }
  onScroll();

  /* ------------------------------------------------------------------
     5. Menu mobile
     ------------------------------------------------------------------ */
  const burger = $(".burger");
  const overlay = $("#menu-overlay");
  const toggleMenu = (open) => {
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    document.body.classList.toggle("menu-open", open);
    document.body.style.overflow = open ? "hidden" : "";
    if (open) {
      overlay.hidden = false;
      requestAnimationFrame(() => overlay.classList.add("is-open"));
    } else {
      overlay.classList.remove("is-open");
      setTimeout(() => { if (!overlay.classList.contains("is-open")) overlay.hidden = true; }, 700);
    }
  };
  burger.addEventListener("click", () => toggleMenu(burger.getAttribute("aria-expanded") !== "true"));
  $$("a", overlay).forEach((a) => a.addEventListener("click", () => toggleMenu(false)));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && document.body.classList.contains("menu-open")) toggleMenu(false); });

  /* Lien actif dans la nav */
  const navLinks = $$(".nav a");
  const sectionObs = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      navLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === `#${en.target.id}`));
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  $$("main section[id]").forEach((s) => sectionObs.observe(s));

  /* ------------------------------------------------------------------
     6. Apparitions au scroll
     ------------------------------------------------------------------ */
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add("is-in");
      revealObs.unobserve(en.target);
      if (en.target.querySelector(".counter")) runCounters(en.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0 }); // seuil 0 : le clip-path initial rend le ratio visible nul

  function observeReveals(root = document) {
    // léger décalage entre éléments frères
    $$(".reveal, .reveal-img", root).forEach((el) => {
      if (el.closest(".hero")) return;
      const sib = [...el.parentElement.children].filter((c) => c.classList.contains("reveal") || c.classList.contains("reveal-img"));
      if (!el.style.getPropertyValue("--d")) el.style.setProperty("--d", `${Math.min(sib.indexOf(el), 6) * 0.08}s`);
      revealObs.observe(el);
    });
  }

  /* Compteurs */
  function runCounters(root) {
    $$(".counter", root).forEach((el) => {
      const target = parseFloat(el.dataset.count);
      const dec = parseInt(el.dataset.decimals || "0", 10);
      const suffix = el.dataset.suffix || "";
      if (reduceMotion) { el.textContent = target.toFixed(dec).replace(".", ",") + suffix; return; }
      const t0 = performance.now();
      const dur = 1600;
      const step = (t) => {
        const p = Math.min((t - t0) / dur, 1);
        const v = target * (1 - Math.pow(1 - p, 4));
        el.textContent = v.toFixed(dec).replace(".", ",") + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }

  /* ------------------------------------------------------------------
     7. Curseur personnalisé + boutons magnétiques (souris uniquement)
     ------------------------------------------------------------------ */
  if (finePointer && !reduceMotion) {
    document.body.classList.add("has-cursor");
    const cursor = $(".cursor");
    const label = $(".cursor__label");
    let cx = -100, cy = -100, tx = -100, ty = -100;
    window.addEventListener("mousemove", (e) => { tx = e.clientX; ty = e.clientY; }, { passive: true });
    const loop = () => {
      cx += (tx - cx) * 0.2;
      cy += (ty - cy) * 0.2;
      cursor.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      requestAnimationFrame(loop);
    };
    loop();
    document.addEventListener("mouseover", (e) => {
      const big = e.target.closest("[data-cursor]");
      const link = e.target.closest("a, button, .day--has, .post");
      cursor.classList.toggle("is-big", !!big);
      cursor.classList.toggle("is-link", !big && !!link);
      label.textContent = big ? big.dataset.cursor : "";
    });
    document.addEventListener("mouseleave", () => { tx = ty = -100; });

    $$(".magnetic").forEach((btn) => {
      btn.addEventListener("mousemove", (e) => {
        const r = btn.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.25;
        const y = (e.clientY - r.top - r.height / 2) * 0.35;
        btn.style.transform = `translate(${x}px, ${y}px)`;
      });
      btn.addEventListener("mouseleave", () => (btn.style.transform = ""));
    });
  }

  /* ------------------------------------------------------------------
     8. Horaires & statut "ouvert maintenant" (heure de Paris)
     ------------------------------------------------------------------ */
  const toMin = (hhmm) => { const [h, m] = hhmm.split(":").map(Number); return h * 60 + m; };
  const fmtH = (hhmm) => {
    if (hhmm === "24:00" || hhmm === "00:00") return "minuit";
    const [h, m] = hhmm.split(":");
    return `${parseInt(h, 10)}h${m === "00" ? "" : m}`;
  };

  function parisNow() {
    const parts = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Paris", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date());
    const get = (t) => parts.find((p) => p.type === t).value;
    const day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
    return { day, min: parseInt(get("hour"), 10) * 60 + parseInt(get("minute"), 10) };
  }

  function openStatus() {
    const { day, min } = parisNow();
    for (const [o, c] of C.hours[day] || []) {
      if (min >= toMin(o) && min < toMin(c)) {
        const left = toMin(c) - min;
        return left <= 45
          ? { cls: "is-soon", text: `Ferme bientôt · ${fmtH(c)}` }
          : { cls: "is-open", text: `Ouvert · jusqu'à ${fmtH(c)}` };
      }
    }
    const today = (C.hours[day] || []).find(([o]) => toMin(o) > min);
    if (today) return { cls: "", text: `Fermé · ouvre à ${fmtH(today[0])}` };
    for (let i = 1; i <= 7; i++) {
      const d = (day + i) % 7;
      if (C.hours[d] && C.hours[d].length) return { cls: "", text: `Fermé · ouvre ${i === 1 ? "demain" : DAYS[d]} à ${fmtH(C.hours[d][0][0])}` };
    }
    return { cls: "", text: "Fermé" };
  }

  function renderStatus() {
    const s = openStatus();
    $$("[data-status]").forEach((el) => {
      el.classList.remove("is-open", "is-soon");
      if (s.cls) el.classList.add(s.cls);
      $(".status__text", el).textContent = s.text;
    });
  }
  renderStatus();
  setInterval(renderStatus, 60_000);

  // Tableau des horaires (lundi → dimanche)
  const hoursTable = $("[data-hours]");
  const todayIdx = parisNow().day;
  const tbody = document.createElement("tbody");
  [1, 2, 3, 4, 5, 6, 0].forEach((d) => {
    const tr = document.createElement("tr");
    if (d === todayIdx) tr.className = "is-today";
    const slots = C.hours[d] || [];
    tr.innerHTML = `<th scope="row">${DAYS[d][0].toUpperCase() + DAYS[d].slice(1)}</th><td>${slots.length ? slots.map(([o, c]) => `${fmtH(o)} – ${fmtH(c)}`).join(", ") : "Fermé"}</td>`;
    tbody.appendChild(tr);
  });
  hoursTable.appendChild(tbody);

  // Accès métro
  $("[data-metro]").innerHTML = C.address.access.map((a) => `
    <li><span class="metro__m" aria-hidden="true">M</span>${a.lines.map((l) => `<span class="metro__line" data-l="${esc(l)}" aria-label="ligne ${esc(l)}">${esc(l)}</span>`).join("")}<span>${esc(a.label)}</span></li>`).join("");

  /* ------------------------------------------------------------------
     9. Carte (menu) avec onglets
     ------------------------------------------------------------------ */
  const tabsEl = $("[data-menu-tabs]");
  const panelsEl = $("[data-menu-panels]");
  const price = (p) => (typeof p === "number" ? `${p.toFixed(p % 1 ? 2 : 0).replace(".", ",")} €` : esc(p));

  C.menu.forEach((cat, i) => {
    const tab = document.createElement("button");
    tab.className = "tab";
    tab.type = "button";
    tab.setAttribute("role", "tab");
    tab.id = `tab-${cat.id}`;
    tab.setAttribute("aria-controls", `panel-${cat.id}`);
    tab.setAttribute("aria-selected", String(i === 0));
    tab.tabIndex = i === 0 ? 0 : -1;
    tab.textContent = cat.title;
    tabsEl.appendChild(tab);

    const panel = document.createElement("div");
    panel.className = "menu__panel";
    panel.id = `panel-${cat.id}`;
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", tab.id);
    panel.hidden = i !== 0;
    panel.innerHTML = (cat.note ? `<p class="menu__panel-note">${esc(cat.note)}</p>` : "") + cat.items.map((it, j) => `
      <article class="dish" style="animation-delay:${j * 0.06}s">
        <h3 class="dish__name">${esc(it.name)} ${(it.tags || []).map((t) => `<span class="tag tag--${esc(t)}">${esc(t)}</span>`).join("")}</h3>
        <span class="dish__price">${price(it.price)}</span>
        <p class="dish__desc">${esc(it.desc)}</p>
      </article>`).join("");
    panelsEl.appendChild(panel);
  });

  const tabs = $$(".tab", tabsEl);
  const selectTab = (tab) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      const panel = document.getElementById(t.getAttribute("aria-controls"));
      panel.hidden = !on;
      if (on) $$(".dish", panel).forEach((d) => { d.style.animation = "none"; void d.offsetWidth; d.style.animation = ""; });
    });
  };
  tabsEl.addEventListener("click", (e) => { const t = e.target.closest(".tab"); if (t) selectTab(t); });
  tabsEl.addEventListener("keydown", (e) => {
    const i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    let n = null;
    if (e.key === "ArrowRight") n = (i + 1) % tabs.length;
    if (e.key === "ArrowLeft") n = (i - 1 + tabs.length) % tabs.length;
    if (e.key === "Home") n = 0;
    if (e.key === "End") n = tabs.length - 1;
    if (n !== null) { e.preventDefault(); tabs[n].focus(); selectTab(tabs[n]); }
  });

  // Formules
  $("[data-formulas]").innerHTML = C.formulas.map((f) => `
    <article class="formula reveal${f.featured ? " formula--featured" : ""}">
      <p class="formula__when">${esc(f.when)}</p>
      <h3>${esc(f.title)}</h3>
      <p class="formula__price">${esc(f.price)}</p>
      <p>${esc(f.desc)}</p>
      ${f.contact
        ? `<a class="btn btn--sm ${f.featured ? "btn--mango" : "btn--line"}" href="#contact" data-subject="Privatisation / événement">${esc(f.cta)}</a>`
        : `<a class="btn btn--sm ${f.featured ? "btn--mango" : "btn--line"}" href="#reserver" data-reserve>${esc(f.cta)}</a>`}
    </article>`).join("");

  // Effet 3D léger sur les formules
  if (finePointer && !reduceMotion) {
    $$(".formula").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        const rx = ((e.clientY - r.top) / r.height - 0.5) * -8;
        const ry = ((e.clientX - r.left) / r.width - 0.5) * 8;
        card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-6px)`;
      });
      card.addEventListener("mouseleave", () => (card.style.transform = ""));
    });
  }

  /* ------------------------------------------------------------------
     10. Événements : calendrier, prochain événement, liste
     ------------------------------------------------------------------ */
  const TYPE_IMG = {
    "soirée": "assets/img/decor-jungle-2",
    brunch: "assets/img/plat-detail",
    concert: "assets/img/decor-jungle",
    atelier: "assets/img/sos-pwa",
    tradition: "assets/img/plat-signature",
  };
  const ymd = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const parseYmd = (s) => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const atTime = (date, hhmm) => { const d = new Date(date); const [h, m] = hhmm.split(":").map(Number); d.setHours(h, m, 0, 0); return d; };
  const longDate = (d) => `${DAYS[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`;

  // Toutes les occurrences entre deux dates
  function occurrences(from, to) {
    const out = [];
    C.events.forEach((ev) => {
      if (ev.recurring === "weekly") {
        const d = new Date(from);
        d.setDate(d.getDate() + ((ev.weekday - d.getDay() + 7) % 7));
        for (; d <= to; d.setDate(d.getDate() + 7)) out.push({ ...ev, day: new Date(d) });
      } else if (ev.date) {
        const d = parseYmd(ev.date);
        if (d >= from && d <= to) out.push({ ...ev, day: d });
      }
    });
    return out.sort((a, b) => atTime(a.day, a.start) - atTime(b.day, b.start));
  }

  const now = new Date();
  const today0 = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  let calMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  let selectedDay = null;

  const calGrid = $("[data-cal-grid]");
  const calTitle = $("[data-cal-title]");
  const listEl = $("[data-event-list]");

  function renderCalendar() {
    const y = calMonth.getFullYear();
    const m = calMonth.getMonth();
    const first = new Date(y, m, 1);
    const last = new Date(y, m + 1, 0);
    calTitle.textContent = `${MONTHS[m]} ${y}`;
    const evs = occurrences(first, last);
    const byDay = {};
    evs.forEach((e) => (byDay[ymd(e.day)] ||= []).push(e));

    const lead = (first.getDay() + 6) % 7; // lundi en premier
    let html = "";
    for (let i = 0; i < lead; i++) html += `<span class="day day--empty"></span>`;
    for (let d = 1; d <= last.getDate(); d++) {
      const date = new Date(y, m, d);
      const key = ymd(date);
      const list = byDay[key] || [];
      const cls = ["day"];
      if (date < today0) cls.push("day--past");
      if (key === ymd(today0)) cls.push("day--today");
      if (list.length) cls.push("day--has");
      const label = `${longDate(date)}${list.length ? ` : ${list.map((e) => e.title).join(", ")}` : ""}`;
      html += list.length
        ? `<button type="button" class="${cls.join(" ")}" data-day="${key}" aria-pressed="${selectedDay === key}" aria-label="${esc(label)}">${d}<span class="day__dots">${list.map((e) => `<i class="dot dot--${esc(e.type)}"></i>`).join("")}</span></button>`
        : `<span class="${cls.join(" ")}" aria-label="${esc(label)}">${d}<span class="day__dots"></span></span>`;
    }
    calGrid.innerHTML = html;
    $("[data-cal-prev]").disabled = y === now.getFullYear() && m === now.getMonth();
  }

  function eventItem(e) {
    return `<button type="button" class="event-item" data-ev="${esc(e.id)}" data-date="${ymd(e.day)}">
      <span class="event-item__date"><b>${e.day.getDate()}</b><small>${MONTHS_SHORT[e.day.getMonth()]}</small></span>
      <span><span class="event-item__title">${esc(e.title)}</span><span class="event-item__meta"><i class="dot dot--${esc(e.type)}"></i>${DAYS[e.day.getDay()]} · ${fmtH(e.start)} – ${fmtH(e.end)}</span></span>
      <svg class="ic" aria-hidden="true"><use href="#i-arrow"/></svg>
    </button>`;
  }

  function renderList() {
    let evs;
    let title;
    if (selectedDay) {
      const d = parseYmd(selectedDay);
      evs = occurrences(d, d);
      title = longDate(d);
    } else {
      const horizon = new Date(today0); horizon.setMonth(horizon.getMonth() + 4);
      // une seule occurrence pour les événements récurrents
      const seen = new Set();
      evs = occurrences(today0, horizon).filter((e) => eventRange(e)[1] > now)
        .filter((e) => (e.recurring ? (seen.has(e.id) ? false : seen.add(e.id)) : true)).slice(0, 5);
      title = "À venir";
    }
    listEl.innerHTML = `<p class="event-list__title">${esc(title)}${selectedDay ? ` · <button type="button" class="linkish" data-clear-day >voir tout</button>` : ""}</p>` + (evs.length ? evs.map(eventItem).join("") : `<p>Pas d'événement ce jour-là… mais la cuisine est ouverte !</p>`);
  }

  function renderNext() {
    const horizon = new Date(today0); horizon.setFullYear(horizon.getFullYear() + 1);
    // le prochain événement "spécial" (non récurrent) en priorité
    const all = occurrences(today0, horizon).filter((e) => atTime(e.day, e.start) > now);
    const next = all.find((e) => !e.recurring) || all[0];
    const box = $("[data-next-event]");
    if (!next) { box.hidden = true; return; }
    const img = TYPE_IMG[next.type] || TYPE_IMG.tradition;
    box.innerHTML = `
      <div class="next-event__bg" style="background-image:url('${img}.webp')"></div>
      <span class="next-event__badge">Prochain événement</span>
      <p class="next-event__date">${longDate(next.day)} · ${fmtH(next.start)}</p>
      <h3>${esc(next.title)}</h3>
      <div class="countdown" data-countdown="${atTime(next.day, next.start).getTime()}" aria-label="Compte à rebours">
        <div><b data-u="d">0</b><small>jours</small></div><div><b data-u="h">0</b><small>heures</small></div><div><b data-u="m">0</b><small>min</small></div><div><b data-u="s">0</b><small>sec</small></div>
      </div>
      <div class="next-event__ctas">
        <button type="button" class="btn btn--mango btn--sm" data-ev="${esc(next.id)}" data-date="${ymd(next.day)}">Voir le détail</button>
        <a class="btn btn--glass btn--sm" href="#reserver" data-reserve>Réserver ma place</a>
      </div>`;
    const cd = $("[data-countdown]", box);
    const target = +cd.dataset.countdown;
    const tick = () => {
      let s = Math.max(0, Math.floor((target - Date.now()) / 1000));
      const d = Math.floor(s / 86400); s -= d * 86400;
      const h = Math.floor(s / 3600); s -= h * 3600;
      const m = Math.floor(s / 60); s -= m * 60;
      $("[data-u=d]", cd).textContent = d;
      $("[data-u=h]", cd).textContent = pad(h);
      $("[data-u=m]", cd).textContent = pad(m);
      $("[data-u=s]", cd).textContent = pad(s);
    };
    tick();
    setInterval(tick, 1000);
  }

  // Ajout à l'agenda
  const stamp = (d) => `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}T${pad(d.getHours())}${pad(d.getMinutes())}00`;
  function eventRange(e) {
    const start = atTime(e.day, e.start);
    let end = atTime(e.day, e.end);
    if (end <= start) end.setDate(end.getDate() + 1);
    return [start, end];
  }
  const placeLabel = `${C.name}, ${C.address.street}, ${C.address.zip} ${C.address.city}`;
  function googleCalUrl(e) {
    const [s, en] = eventRange(e);
    const p = new URLSearchParams({ action: "TEMPLATE", text: `${e.title} — ${C.name}`, dates: `${stamp(s)}/${stamp(en)}`, ctz: "Europe/Paris", details: e.desc, location: placeLabel });
    return `https://calendar.google.com/calendar/render?${p}`;
  }
  function downloadIcs(e) {
    const [s, en] = eventRange(e);
    const icsEsc = (t) => t.replace(/[,;\\]/g, (c) => `\\${c}`);
    const ics = [
      "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Riz Djondjon//Agenda//FR", "CALSCALE:GREGORIAN",
      "BEGIN:VEVENT",
      `UID:${e.id}-${ymd(e.day)}@riz-djondjon`,
      `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").split(".")[0]}Z`,
      `DTSTART;TZID=Europe/Paris:${stamp(s)}`,
      `DTEND;TZID=Europe/Paris:${stamp(en)}`,
      `SUMMARY:${icsEsc(`${e.title} — ${C.name}`)}`,
      `DESCRIPTION:${icsEsc(e.desc)}`,
      `LOCATION:${icsEsc(placeLabel)}`,
      "END:VEVENT", "END:VCALENDAR",
    ].join("\r\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar;charset=utf-8" }));
    a.download = `riz-djondjon-${e.id}-${ymd(e.day)}.ics`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  const evModal = $("#modal-event");
  let currentEvent = null;
  function openEvent(id, date) {
    const ev = C.events.find((e) => e.id === id);
    if (!ev) return;
    currentEvent = { ...ev, day: parseYmd(date) };
    const img = TYPE_IMG[ev.type] || TYPE_IMG.tradition;
    $("#modal-event-title").textContent = ev.title;
    $("[data-event-body]").innerHTML = `
      <picture><source srcset="${img}.webp" type="image/webp"><img class="modal-event__img" src="${img}.jpg" alt=""></picture>
      <p class="modal-event__meta"><span>${longDate(currentEvent.day)}</span><span>${fmtH(ev.start)} – ${fmtH(ev.end)}</span><span>${esc(C.address.street)}</span></p>
      <p>${esc(ev.desc)}</p>
      <div class="modal-event__ctas">
        <button type="button" class="btn btn--mango btn--sm" data-reserve>Réserver ma place</button>
        <a class="btn btn--ghost btn--sm" href="${esc(googleCalUrl(currentEvent))}" target="_blank" rel="noopener">Google Agenda</a>
        <button type="button" class="btn btn--ghost btn--sm" data-ics>Apple / Outlook (.ics)</button>
      </div>`;
    showDialog(evModal);
  }

  document.addEventListener("click", (e) => {
    const day = e.target.closest("[data-day]");
    if (day) {
      selectedDay = selectedDay === day.dataset.day ? null : day.dataset.day;
      renderCalendar();
      renderList();
      if (window.innerWidth < 900) listEl.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "nearest" });
      return;
    }
    if (e.target.closest("[data-clear-day]")) { selectedDay = null; renderCalendar(); renderList(); return; }
    const ev = e.target.closest("[data-ev]");
    if (ev) { openEvent(ev.dataset.ev, ev.dataset.date); return; }
    if (e.target.closest("[data-ics]") && currentEvent) downloadIcs(currentEvent);
  });
  $("[data-cal-prev]").addEventListener("click", () => { calMonth.setMonth(calMonth.getMonth() - 1); renderCalendar(); });
  $("[data-cal-next]").addEventListener("click", () => { calMonth.setMonth(calMonth.getMonth() + 1); renderCalendar(); });

  renderCalendar();
  renderList();
  renderNext();

  /* ------------------------------------------------------------------
     11. Instagram
     ------------------------------------------------------------------ */
  const instaEl = $("[data-insta]");
  const IG_ICON = `<svg class="post__ic" aria-hidden="true"><use href="#i-insta"/></svg>`;

  function renderFallback() {
    instaEl.innerHTML = C.instagram.fallback.map((p) => `
      <a class="post reveal-img" href="${esc(C.links.instagram)}" target="_blank" rel="noopener" data-cursor="Voir">
        <picture><source srcset="${esc(p.img)}.webp" type="image/webp"><img src="${esc(p.img)}.jpg" alt="${esc(p.alt)}" loading="lazy"></picture>
        ${IG_ICON}<span class="post__cap">${esc(p.caption)}</span>
      </a>`).join("");
    observeReveals(instaEl);
  }

  function renderFeed(items) {
    instaEl.innerHTML = items.slice(0, 9).map((p) => {
      const type = (p.mediaType || p.media_type || "").toUpperCase();
      const src = (type === "VIDEO" ? (p.thumbnailUrl || p.thumbnail_url) : null) || p.sizes?.medium?.mediaUrl || p.mediaUrl || p.media_url;
      const cap = (p.prunedCaption || p.caption || "").slice(0, 120);
      const href = /^https:\/\/(www\.)?instagram\.com\//.test(p.permalink || "") ? p.permalink : C.links.instagram;
      if (!/^https:\/\//.test(src || "")) return "";
      return `<a class="post reveal-img${type === "VIDEO" ? " post--video" : ""}" href="${esc(href)}" target="_blank" rel="noopener" data-cursor="Voir">
        <img src="${esc(src)}" alt="${esc(cap || "Publication Instagram de Riz Djondjon")}" loading="lazy">
        ${IG_ICON}<span class="post__cap">${esc(cap)}</span>
      </a>`;
    }).join("");
    observeReveals(instaEl);
  }

  function renderEmbeds(urls) {
    instaEl.classList.add("is-embeds");
    instaEl.innerHTML = urls.map((u) => `<blockquote class="instagram-media" data-instgrm-permalink="${esc(u)}" data-instgrm-version="14"><a href="${esc(u)}" target="_blank" rel="noopener">Voir cette publication sur Instagram</a></blockquote>`).join("");
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.instagram.com/embed.js";
    document.body.appendChild(s);
  }

  (async () => {
    const ig = C.instagram;
    if (ig.feedUrl) {
      try {
        const res = await fetch(ig.feedUrl);
        if (!res.ok) throw new Error(res.status);
        const data = await res.json();
        const items = Array.isArray(data) ? data : data.posts || data.data || [];
        if (items.length) return renderFeed(items);
      } catch (err) { console.warn("Flux Instagram indisponible, affichage de secours.", err); }
    }
    if (ig.posts && ig.posts.length) return renderEmbeds(ig.posts);
    renderFallback();
  })();

  /* ------------------------------------------------------------------
     12. Avis (défilement à la souris)
     ------------------------------------------------------------------ */
  const track = $("[data-reviews]");
  track.innerHTML = C.reviews.map((r) => `
    <article class="review">
      <span class="stars" aria-label="5 sur 5"><svg class="ic"><use href="#i-star"/></svg><svg class="ic"><use href="#i-star"/></svg><svg class="ic"><use href="#i-star"/></svg><svg class="ic"><use href="#i-star"/></svg><svg class="ic"><use href="#i-star"/></svg></span>
      <p class="review__quote">${esc(r.text)}</p>
      <footer><b>${esc(r.name)}</b><span>${esc(r.date)}</span></footer>
    </article>`).join("");
  $$(".review .stars").forEach((s) => (s.style.fontSize = "1rem"));
  let drag = null;
  track.addEventListener("pointerdown", (e) => {
    if (e.pointerType !== "mouse") return;
    drag = { x: e.clientX, left: track.scrollLeft };
    track.classList.add("is-dragging");
  });
  window.addEventListener("pointermove", (e) => { if (drag) track.scrollLeft = drag.left - (e.clientX - drag.x); });
  window.addEventListener("pointerup", () => { drag = null; track.classList.remove("is-dragging"); });

  /* ------------------------------------------------------------------
     13. Plan Google Maps (chargé au clic : rapide & respectueux RGPD)
     ------------------------------------------------------------------ */
  $("[data-map-load]").addEventListener("click", () => {
    const frame = $("[data-map]");
    frame.innerHTML = `<iframe src="${esc(C.links.mapsEmbed)}" title="Plan d'accès : ${esc(placeLabel)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>`;
  });

  /* ------------------------------------------------------------------
     14. Fenêtres (réservation, événement)
     ------------------------------------------------------------------ */
  const supportsDialog = typeof HTMLDialogElement === "function";
  function showDialog(d) {
    if (supportsDialog) {
      if (!d.open) d.showModal();
    } else d.setAttribute("open", "");
  }
  $$(".modal").forEach((d) => {
    d.addEventListener("click", (e) => {
      if (e.target === d || e.target.closest("[data-close]")) d.close ? d.close() : d.removeAttribute("open");
    });
  });

  const reserveModal = $("#modal-reserve");
  document.addEventListener("click", (e) => {
    const r = e.target.closest("[data-reserve]");
    if (!r) return;
    e.preventDefault();
    if (document.body.classList.contains("menu-open")) toggleMenu(false);
    if (evModal.open) evModal.close();
    if (!supportsDialog) { window.open(C.links.reservation, "_blank", "noopener"); return; }
    const iframe = $("iframe", reserveModal);
    if (!iframe.src) iframe.src = C.links.reservation;
    showDialog(reserveModal);
  });

  // Les liens "Demander un devis" présélectionnent l'objet du formulaire
  document.addEventListener("click", (e) => {
    const s = e.target.closest("[data-subject]");
    if (!s) return;
    const radio = $(`input[name="subject"][value="${CSS.escape(s.dataset.subject)}"]`);
    if (radio) radio.checked = true;
  });

  /* ------------------------------------------------------------------
     15. Formulaire de contact
     ------------------------------------------------------------------ */
  const form = $("[data-contact-form]");
  const statusEl = $(".form__status", form);
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    statusEl.className = "form__status";
    let ok = true;
    $$("[required]", form).forEach((f) => {
      const valid = f.value.trim() && (f.type !== "email" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value));
      f.closest(".field").classList.toggle("is-invalid", !valid);
      if (!valid) ok = false;
    });
    if (!ok) {
      statusEl.textContent = "Merci de compléter votre nom, votre e-mail et votre message.";
      statusEl.classList.add("is-err");
      $(".is-invalid input, .is-invalid textarea", form)?.focus();
      return;
    }
    const data = new FormData(form);
    if (data.get("_gotcha")) return; // robot

    if (C.formEndpoint) {
      const btn = $("button[type=submit]", form);
      btn.disabled = true;
      statusEl.textContent = "Envoi en cours…";
      try {
        const res = await fetch(C.formEndpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error(res.status);
        form.reset();
        statusEl.textContent = "Merci ! Votre message est bien parti, on vous répond très vite. 🌿";
        statusEl.classList.add("is-ok");
      } catch {
        statusEl.textContent = "Oups, l'envoi a échoué. Appelez-nous au " + C.phoneDisplay + ".";
        statusEl.classList.add("is-err");
      } finally { btn.disabled = false; }
      return;
    }

    // Sans service d'envoi : on prépare l'e-mail dans la messagerie du visiteur
    const opt = (key, label) => (data.get(key) ? [`${label} : ${data.get(key)}`] : []);
    const lines = [
      `Objet : ${data.get("subject")}`,
      `Nom : ${data.get("name")}`,
      `E-mail : ${data.get("email")}`,
      ...opt("phone", "Téléphone"),
      ...opt("date", "Date souhaitée"),
      ...opt("guests", "Nombre de personnes"),
      "",
      data.get("message"),
    ];
    window.location.href = `mailto:${C.email}?subject=${encodeURIComponent(`[Site] ${data.get("subject")} — ${data.get("name")}`)}&body=${encodeURIComponent(lines.join("\n"))}`;
    statusEl.textContent = "Votre messagerie s'ouvre avec le message prêt à envoyer.";
    statusEl.classList.add("is-ok");
  });
  $$(".field input, .field textarea", form).forEach((f) => f.addEventListener("input", () => f.closest(".field").classList.remove("is-invalid")));

  /* Lancement des apparitions */
  observeReveals();
})();
