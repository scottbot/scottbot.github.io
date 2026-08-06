/* ────────────────────────────────────────────────────────────────
   The reading pane. On wide screens, clicking a link to one of the
   works or blog posts from a page marked `reader-enabled` opens the
   piece in an independently-scrolling right-hand pane, so the reader
   never loses their place. Plain JS, no dependencies; without it,
   every link is an ordinary link.
   ──────────────────────────────────────────────────────────────── */
(function () {
  "use strict";

  // The width threshold lives in hugo.toml ([params] readerMinWidth) and
  // reaches us via <body data-reader-min="…">.
  var MIN_WIDTH = parseInt(document.body.getAttribute("data-reader-min"), 10) || 1100;
  var pane = document.getElementById("reader");
  if (!pane) return;
  var titleEl = pane.querySelector(".reader-title");
  var contentEl = pane.querySelector(".reader-content");
  var permalinkEl = pane.querySelector(".reader-permalink");
  var closeBtn = pane.querySelector(".reader-close");
  var pageBody = document.querySelector(".page-body");
  var cache = {};
  var currentPath = null;
  var lastTrigger = null; // the link that opened the pane, for focus return

  function readerAllowed() {
    return document.body.classList.contains("reader-enabled") &&
           window.innerWidth >= MIN_WIDTH;
  }

  /* ── Reflow-proof scroll memory ──────────────────────────────
     Opening (or closing) the pane reflows the CV into a narrower
     (or wider) column, so a pixel offset carried across the change
     lands somewhere else entirely. Instead, remember which element
     sat at the top of the viewport and where its top edge was, then
     scroll the new container until it's back in that spot. */
  function captureAnchor() {
    var blocks = document.querySelectorAll(
      ".page-body main h2, .page-body main h3, .page-body main p, .page-body main li, .page-body main .cv-entry"
    );
    var fallback = null;
    for (var i = 0; i < blocks.length; i++) {
      var r = blocks[i].getBoundingClientRect();
      if (r.height === 0 || r.bottom <= 0) continue;
      if (!fallback) fallback = { el: blocks[i], top: r.top };
      // Prefer the first block whose top edge is actually on screen;
      // fall back to the one straddling the viewport's top.
      if (r.top >= 0) return { el: blocks[i], top: r.top };
    }
    return fallback;
  }
  function restoreAnchor(anchor, scroller) {
    if (!anchor || !document.contains(anchor.el)) return;
    var delta = anchor.el.getBoundingClientRect().top - anchor.top;
    if (scroller === window) {
      window.scrollBy({ top: delta, left: 0, behavior: "instant" });
    } else {
      scroller.scrollTo({ top: scroller.scrollTop + delta, behavior: "instant" });
    }
  }

  function absolutize(node, basePath) {
    // Fetched documents live at basePath; their relative srcs/hrefs
    // (images/fig-001.png) must be re-anchored or they'd resolve
    // against the page we're actually on.
    node.querySelectorAll("img[src], a[href], source[src]").forEach(function (el) {
      var attr = el.tagName === "A" ? "href" : "src";
      var val = el.getAttribute(attr);
      if (!val || /^([a-z]+:|\/|#)/i.test(val)) return;
      el.setAttribute(attr, basePath + val);
    });
  }

  function renderInto(path, doc) {
    var src = doc.querySelector("#reader-source");
    var docTitle = doc.querySelector("h1");
    titleEl.textContent = docTitle ? docTitle.textContent : (doc.title || "");
    contentEl.innerHTML = "";
    if (src) {
      var clone = src.cloneNode(true);
      absolutize(clone, path);
      contentEl.appendChild(clone);
      armorTables(contentEl);
    } else {
      var p = document.createElement("p");
      var a = document.createElement("a");
      a.href = path;
      a.textContent = "Read this piece on its own page →";
      p.appendChild(a);
      contentEl.appendChild(p);
    }
    permalinkEl.setAttribute("href", path);
    // Blog content sinks its white-background figures into the paper tint;
    // works remain true to their published form (see CSS).
    pane.classList.toggle("pane-blog", path.indexOf("/blog/") === 0);
    // Split view: the window stops scrolling and the left column takes
    // over as its own scroll container — hand it the reader's place by
    // element, not by pixel (the column narrows, so pixels don't map).
    if (!document.body.classList.contains("reader-open")) {
      var anchor = captureAnchor();
      document.body.classList.add("reader-open");
      restoreAnchor(anchor, pageBody);
    }
    pane.hidden = false;
    contentEl.scrollTop = 0;
    currentPath = path;
  }

  function openReader(path, push, focusPane) {
    var load = cache[path]
      ? Promise.resolve(cache[path])
      : fetch(path).then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.text();
        }).then(function (html) {
          cache[path] = html;
          return html;
        });
    load.then(function (html) {
      var doc = new DOMParser().parseFromString(html, "text/html");
      renderInto(path, doc);
      // Keyboard & screen-reader users follow their action into the pane;
      // the content region is the scroll container, so focusing it also
      // makes it scrollable by arrow keys.
      if (focusPane) contentEl.focus({ preventScroll: true });
      if (push) {
        var url = new URL(window.location);
        url.searchParams.set("read", path);
        history.pushState({ reader: path }, "", url);
      }
    }).catch(function () {
      window.location.href = path; // graceful surrender
    });
  }

  function closeReader(push) {
    // Hand the reader's place back from the left column to the window —
    // again by element, since the column widens back out on close.
    if (document.body.classList.contains("reader-open")) {
      var anchor = captureAnchor();
      document.body.classList.remove("reader-open");
      restoreAnchor(anchor, window);
    }
    // If focus was inside the pane, return it to the link that opened it,
    // so keyboard users are not dropped at the top of the document.
    if (pane.contains(document.activeElement)) {
      if (lastTrigger && document.contains(lastTrigger)) lastTrigger.focus();
      else if (pageBody) pageBody.querySelector("main") && pageBody.querySelector("main").focus();
    }
    pane.hidden = true;
    currentPath = null;
    if (push) {
      var url = new URL(window.location);
      url.searchParams.delete("read");
      history.pushState({}, "", url);
    }
  }

  document.addEventListener("click", function (e) {
    if (!readerAllowed()) return;
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    var a = e.target.closest("a");
    if (!a || a.origin !== window.location.origin) return;
    // Links that ask for another tab/window or a download are real
    // navigations — never intercept them.
    if (a.hasAttribute("download") || (a.target && a.target !== "_self")) return;
    if (a.closest("#reader")) {
      // The "open ↗" permalink is a real navigation — never intercept it.
      if (a.classList.contains("reader-permalink")) return;
      // Other links within the pane: internal works/posts swap the pane content.
      if (/^\/(works|blog)\/[^/]+\/$/.test(a.pathname)) {
        e.preventDefault();
        openReader(a.pathname, true, true);
      }
      return;
    }
    if (!/^\/(works|blog)\/[^/]+\/$/.test(a.pathname)) return;
    e.preventDefault();
    lastTrigger = a;
    openReader(a.pathname, true, true);
  });

  closeBtn.addEventListener("click", function () { closeReader(true); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && document.body.classList.contains("reader-open")) {
      closeReader(true);
    }
  });

  window.addEventListener("popstate", function () {
    var path = new URL(window.location).searchParams.get("read");
    var paneOpen = document.body.classList.contains("reader-open");
    if (path && /^\/(works|blog)\/[^/]+\/$/.test(path)) {
      // Hash-only traversals (footnote jumps within the pane) re-fire
      // popstate with the same ?read=; re-rendering would throw away the
      // reader's place, so leave the pane alone.
      if (paneOpen && path === currentPath) return;
      // Don't conjure the pane on a window too narrow for it — unless it
      // is already open (e.g. the user resized after opening).
      if (readerAllowed() || paneOpen) openReader(path, false, false);
    } else {
      closeReader(false);
    }
  });

  // Deep link: /cv/?read=/works/network-turn/
  var initial = new URL(window.location).searchParams.get("read");
  if (initial && /^\/(works|blog)\/[^/]+\/$/.test(initial)) {
    if (readerAllowed()) {
      openReader(initial, false, false);
    } else {
      // Too narrow for the pane (a shared link opened on a phone):
      // honor the link by going to the work itself.
      window.location.replace(initial);
    }
  }

  /* ── The still contents menu ─────────────────────────────────
     On pages with a .side-rail, quietly mark which section the
     reader is in as they scroll. Pure enhancement; the rail is
     ordinary anchor links without this. */
  var rail = document.querySelector(".side-rail");
  if (rail && "IntersectionObserver" in window) {
    var railLinks = {};
    rail.querySelectorAll('a[href^="#"]').forEach(function (a) {
      railLinks[a.getAttribute("href").slice(1)] = a;
    });
    var current = null;
    var mark = function (id) {
      if (current) current.classList.remove("active");
      current = railLinks[id] || null;
      if (current) current.classList.add("active");
    };
    var visible = [];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var id = e.target.id;
        if (e.isIntersecting) { if (visible.indexOf(id) < 0) visible.push(id); }
        else { visible = visible.filter(function (v) { return v !== id; }); }
      });
      // Mark the earliest heading on screen; when none is, keep the last
      // mark (the reader is inside that section's body).
      if (visible.length) {
        var order = Object.keys(railLinks);
        visible.sort(function (a, b) { return order.indexOf(a) - order.indexOf(b); });
        mark(visible[0]);
      }
    }, { rootMargin: "0px 0px -55% 0px" });
    Object.keys(railLinks).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  /* ── Overflow armor ──────────────────────────────────────────
     Wide tables (the software manuals have several) scroll within
     themselves rather than forcing the whole page sideways. Code
     blocks already behave; see `pre` in the CSS. */
  function armorTables(root) {
    root.querySelectorAll("table").forEach(function (t) {
      if (t.parentElement && t.parentElement.classList.contains("scrolls")) return;
      var wrap = document.createElement("div");
      wrap.className = "scrolls";
      t.parentNode.insertBefore(wrap, t);
      wrap.appendChild(t);
    });
  }
  armorTables(document);

  /* ── The rising manicule ─────────────────────────────────────
     After about a screen and a half of reading, a hand appears at
     the bottom corner, pointing the way back to the top. */
  var rise = document.querySelector(".rise");
  if (rise) {
    var riseCheck = function () {
      rise.classList.toggle("shown", window.scrollY > window.innerHeight * 1.5);
    };
    window.addEventListener("scroll", riseCheck, { passive: true });
    riseCheck();
  }

  /* ── The yielding running head (small screens) ───────────────
     On phones the frozen header would cost a strip of every screen,
     so it slides away while reading downward and returns on the
     first upward scroll (or near the top). Wide screens keep the
     always-frozen head. */
  var smallScreen = window.matchMedia("(max-width: 640px)");
  var lastY = window.scrollY;
  window.addEventListener("scroll", function () {
    if (!smallScreen.matches) {
      document.body.classList.remove("head-away");
      return;
    }
    var y = window.scrollY;
    if (y < 80) document.body.classList.remove("head-away");
    else if (y > lastY + 6) document.body.classList.add("head-away");
    else if (y < lastY - 6) document.body.classList.remove("head-away");
    lastY = y;
  }, { passive: true });
})();
