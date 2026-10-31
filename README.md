# Ferienwohnung Reese-Horstmann

Website der Ferienwohnung in Bad Harzburg: https://harz-zu-jeder-jahreszeit.de (ferienwohnungreesehorstmann.de leitet weiter)

Statische Seite ohne Build-Schritt, gehostet über GitHub Pages (Branch `main`, Ordner `/`).

- `build.py` – erzeugt die Startseite in drei Sprachen (`index.html`, `en/index.html`, `ru/index.html`). Texte nur dort ändern, dann `python3 build.py`
- `site.js` – Anfrage-Helfer und Fotoansicht, Kontaktdaten oben
- `impressum.html`, `datenschutz.html` – Rechtstexte
- `style.css` – Gestaltung
- `fotos/` – Bilder (Platzhalter in der Seite: `<figure class="ph">`; Foto mit `<img src="fotos/…" alt="…">` in die figure setzen)
- `CNAME` – eigene Domain

## Vor dem Livegang

- [x] Fotos der Wohnung (31.10.)
- [x] Fotos von Hallenbad, Bad, Grundriss und Ausflügen aus dem Booking-Inserat (31.10.)
- [x] Telefon, Mobil/WhatsApp und Mail (31.10.)
- [x] Anschrift und E-Mail (31.10.)
- [ ] Falls es eine USt-IdNr. gibt: ins Impressum
- [ ] Entwurfs-Hinweis und `noindex` entfernen (`DRAFT = False` in `build.py`, Hinweis in Impressum und Datenschutz löschen)
