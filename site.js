// Gemeinsames Skript für alle Sprachfassungen. Texte kommen aus window.FEWO (je Seite gesetzt).

// Kontaktdaten für die Anfrage-Knöpfe
var WHATSAPP = "491744283147"; // Mobilnummer international ohne +
var EMAIL = "harz.fewo@web.de";

(function () {
  var T = window.FEWO;

  // Anfrage-Helfer: baut eine fertige Nachricht für WhatsApp oder E-Mail
  function val(id) { return document.getElementById(id).value; }
  function date(v) { return v ? v.split("-").reverse().join(".") : "?"; }
  function text() {
    var t = T.hello + "\n\n" + T.interest + "\n" +
      T.period + ": " + date(val("von")) + " – " + date(val("bis")) + "\n" +
      T.guests + ": " + val("erw") + " " + T.adults + ", " + val("kind") + " " + T.children + "\n";
    if (val("msg")) t += "\n" + val("msg") + "\n";
    t += "\n" + T.regards + "\n" + (val("name") || "");
    return t;
  }
  document.querySelectorAll("[data-send]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (b.dataset.send === "wa") {
        if (!WHATSAPP) return;
        location.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text());
      } else {
        location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(T.subject) + "&body=" + encodeURIComponent(text());
      }
    });
  });

  if (!WHATSAPP) {
    // Ohne Nummer nur per E-Mail anfragen
    document.querySelectorAll('[data-send="wa"], .mbar .btn-wa').forEach(function (e) { e.style.display = "none"; });
    document.querySelector('[data-send="mail"]').className = "btn btn-primary";
  }

  var von = document.getElementById("von"), bis = document.getElementById("bis");
  von.min = new Date().toISOString().slice(0, 10);
  von.addEventListener("change", function () { bis.min = von.value; if (bis.value && bis.value <= von.value) bis.value = ""; });

  // Fotos groß ansehen: Klick öffnet, Klick aufs Bild zoomt, Pfeile/Wischen blättern, Esc schließt
  var imgs = [].slice.call(document.querySelectorAll(".ph img"));
  var lb = document.getElementById("lb"), big = lb.querySelector("img"), cap = lb.querySelector(".cap"), box = lb.querySelector(".lb-scroll");
  var i = 0, x0 = null;
  function show(n) {
    i = (n + imgs.length) % imgs.length;
    lb.classList.remove("zoom");
    big.src = imgs[i].src; big.alt = imgs[i].alt;
    cap.textContent = imgs[i].alt + "  ·  " + (i + 1) + " / " + imgs.length;
  }
  function close() { lb.classList.remove("open"); document.body.style.overflow = ""; }
  imgs.forEach(function (im, n) {
    im.addEventListener("click", function () { show(n); lb.classList.add("open"); document.body.style.overflow = "hidden"; });
  });
  big.addEventListener("click", function (e) {
    var r = big.getBoundingClientRect(), fx = (e.clientX - r.left) / r.width, fy = (e.clientY - r.top) / r.height;
    lb.classList.toggle("zoom");
    if (lb.classList.contains("zoom")) {
      box.scrollLeft = fx * box.scrollWidth - box.clientWidth / 2;
      box.scrollTop = fy * box.scrollHeight - box.clientHeight / 2;
    }
  });
  box.addEventListener("click", function (e) { if (e.target === box) close(); });
  lb.querySelector(".x").addEventListener("click", close);
  lb.querySelector(".prev").addEventListener("click", function () { show(i - 1); });
  lb.querySelector(".next").addEventListener("click", function () { show(i + 1); });
  document.addEventListener("keydown", function (e) {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") show(i - 1);
    if (e.key === "ArrowRight") show(i + 1);
  });
  box.addEventListener("touchstart", function (e) { x0 = e.touches.length === 1 ? e.touches[0].clientX : null; }, { passive: true });
  box.addEventListener("touchend", function (e) {
    if (x0 === null || lb.classList.contains("zoom")) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });
})();

// Besucherzahl unten im Fuß (GoatCounter; in den GoatCounter-Einstellungen muss
// „Allow adding visitor counts on your website“ aktiv sein, sonst bleibt die Zeile unsichtbar)
(function () {
  var el = document.getElementById("visits");
  if (!el || !el.dataset.gc || !window.fetch) return;
  fetch("https://" + el.dataset.gc + ".goatcounter.com/counter/TOTAL.json")
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (d) { if (!d || !d.count || d.count === "0") return; el.querySelector("span").textContent = d.count; el.hidden = false; })
    .catch(function () {});
})();
