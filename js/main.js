/* ============================================================
   Renders publications & activities from data/*.js and wires up
   scroll-reveal + active-nav highlighting. No build step needed.
   ============================================================ */
(function () {
  "use strict";

  var esc = function (s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  };

  /* ---------- Publications ---------- */
  var pubs = (window.PUBLICATIONS || []).slice().sort(function (a, b) {
    return (b.year || 0) - (a.year || 0);
  });

  var pubList = document.getElementById("pub-list");
  var pubCount = document.getElementById("pub-count");
  if (pubCount) pubCount.textContent = pubs.length ? "(" + pubs.length + ")" : "";

  if (pubList) {
    pubList.innerHTML = pubs.map(function (p) {
      var meta = p.year ? esc(p.year) : "&mdash;";
      var venue = p.venue ? ' <span class="pub-venue">[' + esc(p.venue) + "]</span>" : "";
      var link = p.url
        ? ' <a class="ext" href="' + esc(p.url) + '" target="_blank" rel="noopener" aria-label="Open publication"></a>'
        : "";
      return (
        '<div class="row pub-row reveal">' +
          '<span class="meta">[<span class="meta-val">' + meta + "</span>]</span>" +
          '<div class="row-main"><span class="row-title">' + esc(p.title) + "</span>" + venue + link + "</div>" +
        "</div>"
      );
    }).join("");
  }

  var syncNote = document.getElementById("sync-note");
  if (syncNote) {
    var scholarSynced = pubs.some(function (p) { return p.source === "scholar"; });
    syncNote.textContent = scholarSynced
      ? "List synced with Google Scholar via the repository's automated workflow."
      : "List maintained from data/publications.js — automated Google Scholar sync available (see repository README).";
  }

  /* ---------- Activities ---------- */
  var acts = (window.ACTIVITIES || []).slice().sort(function (a, b) {
    return (b.year || 0) - (a.year || 0);
  });
  var actList = document.getElementById("act-list");
  if (actList) {
    actList.innerHTML = acts.map(function (a) {
      var meta = a.year ? esc(a.year) : "&mdash;";
      var text = esc(a.text);
      var inner = a.url
        ? '<a class="row-link" href="' + esc(a.url) + '" target="_blank" rel="noopener" style="border:none"><span class="row-title">' + text + "</span></a>"
        : '<span class="row-title">' + text + "</span>";
      return (
        '<div class="row reveal">' +
          '<span class="meta">[<span class="meta-val">' + meta + "</span>]</span>" +
          '<div class="row-main">' + inner + "</div>" +
        "</div>"
      );
    }).join("");
  }

  /* ---------- Scroll reveal ---------- */
  var rows = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    rows.forEach(function (r) { io.observe(r); });
  } else {
    rows.forEach(function (r) { r.classList.add("visible"); });
  }

  /* ---------- Active nav highlighting ---------- */
  var navLinks = document.querySelectorAll(".site-nav a");
  var sections = Array.prototype.map.call(navLinks, function (a) {
    return document.querySelector(a.getAttribute("href"));
  });
  var onScroll = function () {
    var pos = window.scrollY + 120;
    var current = -1;
    sections.forEach(function (sec, i) {
      if (sec && sec.offsetTop <= pos) current = i;
    });
    navLinks.forEach(function (a, i) { a.classList.toggle("active", i === current); });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Email reveal card ---------- */
  var emailBtn = document.querySelector(".email-reveal-btn");
  if (emailBtn) {
    var emailList = document.querySelector(".email-list");
    emailBtn.addEventListener("click", function () {
      var open = emailBtn.getAttribute("aria-expanded") === "true";
      emailBtn.setAttribute("aria-expanded", String(!open));
      emailBtn.textContent = open ? "Reveal emails" : "Hide emails";
      emailList.hidden = open;
    });
  }

  /* ---------- Gated contact cards ----------
     Numbers are stored reversed + base64 so they are not sitting in the
     markup as plain text for scrapers; they are only assembled after the
     visitor gives a name and a reason. */
  var decode = function (s) {
    try { return atob(s).split("").reverse().join(""); } catch (e) { return ""; }
  };
  var CHANNELS = {
    whatsapp: { n: "MjgxNzE4OTgxODQzMg==" },   // WhatsApp number, digits only
    call: { n: "ODQzMjA1MDYwODQzMis=" }        // direct line, E.164
  };

  var pretty = function (digits) {
    var d = digits.replace(/^\+/, "");
    return "+" + d.slice(0, 3) + " " + d.slice(3, 6) + " " + d.slice(6, 9) + " " + d.slice(9);
  };

  Array.prototype.forEach.call(document.querySelectorAll(".gate-card"), function (card) {
    var channel = card.getAttribute("data-channel");
    var form = card.querySelector(".gate-form");
    var errBox = card.querySelector(".gate-error");
    var result = card.querySelector(".gate-result");
    if (!form || !CHANNELS[channel]) return;

    var fail = function (msg) {
      errBox.textContent = msg;
      errBox.hidden = false;
    };

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      errBox.hidden = true;

      var name = (form.elements.name.value || "").trim();
      var reason = (form.elements.reason.value || "").trim();

      if (name.length < 2) { fail("Please enter your name."); form.elements.name.focus(); return; }
      if (reason.length < 10) { fail("Please add a short reason (at least 10 characters)."); form.elements.reason.focus(); return; }

      var number = decode(CHANNELS[channel].n);
      if (!number) { fail("Something went wrong — please use email instead."); return; }

      if (channel === "whatsapp") {
        var text = "Hello Dr. Zubair, my name is " + name + ". " + reason;
        var url = "https://wa.me/" + number + "?text=" + encodeURIComponent(text);
        result.innerHTML =
          '<p class="gate-ok">Thanks, ' + esc(name) + ". Your message is ready.</p>" +
          '<p class="gate-number"><a href="' + esc(url) + '" target="_blank" rel="noopener">Open WhatsApp chat &rarr;</a></p>' +
          '<p class="gate-fine">If the chat does not open, message ' + esc(pretty(number)) + " directly.</p>";
        form.hidden = true;
        result.hidden = false;
        window.open(url, "_blank", "noopener");
      } else {
        result.innerHTML =
          '<p class="gate-ok">Thanks, ' + esc(name) + ". Here is the line.</p>" +
          '<p class="gate-number"><a href="tel:' + esc(number) + '">' + esc(pretty(number)) + "</a></p>" +
          '<p class="gate-fine">Best reached during working hours, West Africa Time (UTC+1).</p>';
        form.hidden = true;
        result.hidden = false;
      }
    });
  });

  /* ---------- Footer year ---------- */
  var yr = document.getElementById("year");
  if (yr) yr.textContent = new Date().getFullYear();
})();
