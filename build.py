#!/usr/bin/env python3
"""Erzeugt die Startseite in drei Sprachen aus einer Vorlage.

    python3 build.py

Schreibt index.html (Deutsch), en/index.html und ru/index.html.
Texte nur hier ändern, nicht in den erzeugten Dateien.
Impressum und Datenschutz sind bewusst nur auf Deutsch (impressum.html, datenschutz.html).
"""
import html
import json
import os

SITE = "https://harz-zu-jeder-jahreszeit.de/"
DRAFT = False  # Entwurf: gelber Hinweis und noindex. Auf False setzen, wenn die Seite fertig ist.

# Fotos: Datei, Breite, Höhe, Bildunterschrift je Sprache (dient auch als Alt-Text in der Großansicht)
GALLERY = [
    ("hallenbad.jpg", 1024, 768, "wide", {"de": "Hallenbad im Haus", "en": "Indoor pool in the building", "ru": "Крытый бассейн в доме"}),
    ("wohnzimmer.jpg", 1050, 1400, "", {"de": "Wohnzimmer", "en": "Living room", "ru": "Гостиная"}),
    ("schlafzimmer.jpg", 1400, 1050, "", {"de": "Schlafzimmer", "en": "Bedroom", "ru": "Спальня"}),
    ("kueche.jpg", 1050, 1400, "", {"de": "Küche", "en": "Kitchen", "ru": "Кухня"}),
    ("essecke.jpg", 1050, 1400, "", {"de": "Essecke", "en": "Dining area", "ru": "Обеденный уголок"}),
    ("wohnzimmer-tv.jpg", 1050, 1400, "", {"de": "Wohnzimmer", "en": "Living room", "ru": "Гостиная"}),
    ("mini-backofen.jpg", 576, 768, "", {"de": "Kommode mit Mini-Backofen", "en": "Sideboard with mini oven", "ru": "Комод с мини-духовкой"}),
    ("bad.jpg", 576, 768, "", {"de": "Duschbad", "en": "Shower room", "ru": "Ванная с душем"}),
    ("balkon-sitzplatz.jpg", 1400, 933, "", {"de": "Balkon mit Sitzplatz", "en": "Balcony with seating", "ru": "Балкон со столиком"}),
    ("balkon.jpg", 1050, 1400, "", {"de": "Balkon am Waldrand", "en": "Balcony by the forest", "ru": "Балкон у леса"}),
    ("hallenbad-abends.jpg", 576, 768, "", {"de": "Hallenbad am Abend", "en": "Indoor pool in the evening", "ru": "Бассейн вечером"}),
    ("haus.jpg", 1400, 933, "", {"de": "Apartmenthaus Kurhausstraße 18", "en": "Apartment building, Kurhausstraße 18", "ru": "Дом на Kurhausstraße 18"}),
    ("grundriss.jpg", 502, 480, "plan", {"de": "Grundriss der Wohnung", "en": "Floor plan", "ru": "План квартиры"}),
]
TRIPS = [
    ("seilbahn.jpg", 828, 621, {"de": "Burgberg-Seilbahn", "en": "Burgberg cable car", "ru": "Канатная дорога на Бургберг"}),
    ("baumwipfelpfad.jpg", 1024, 683, {"de": "Baumwipfelpfad", "en": "Treetop walk", "ru": "Тропа по верхушкам деревьев"}),
    ("radau-wasserfall.jpg", 584, 768, {"de": "Radau-Wasserfall", "en": "Radau waterfall", "ru": "Водопад Радау"}),
    ("burgruine.jpg", 1050, 1400, {"de": "Alter Baum auf der Burgruine", "en": "Old tree on the castle ruins", "ru": "Старое дерево на руинах замка"}),
    ("see.jpg", 1400, 1050, {"de": "Baden und Spazieren am See", "en": "Lakeside walks", "ru": "Прогулки у озера"}),
    ("wald.jpg", 1050, 1400, {"de": "Wandern im Wald", "en": "Hiking in the forest", "ru": "Прогулки по лесу"}),
    ("walderdbeeren.jpg", 1050, 1400, {"de": "Walderdbeeren am Wegesrand", "en": "Wild strawberries along the trail", "ru": "Земляника у тропы"}),
    ("todtenrode.jpg", 1050, 1400, {"de": "Herz in Todtenrode", "en": "Heart sculpture in Todtenrode", "ru": "Сердце в Тодтенроде"}),
]
WINTER = [
    ("winter.jpg", 768, 768, {"de": "Verschneiter Harz", "en": "The Harz in snow", "ru": "Заснеженный Гарц"}),
    ("lichterbogen.jpg", 1050, 1400, {"de": "Bad Harzburger Wintertreff", "en": "Bad Harzburg winter market", "ru": "Зимняя ярмарка в Бад-Харцбурге"}),
    ("eisbahn.jpg", 1050, 1400, {"de": "Eisbahn", "en": "Ice rink", "ru": "Каток"}),
    ("feuerzangenbowle.jpg", 1400, 933, {"de": "Feuerzangenbowle an der Eisbahn", "en": "Hot punch by the ice rink", "ru": "Пунш у катка"}),
    ("wintertreff.jpg", 1050, 1400, {"de": "Glühwein vom Wintertreff", "en": "Mulled wine at the winter market", "ru": "Глинтвейн на ярмарке"}),
    ("weihnachtsmarkt-getraenke.jpg", 1050, 1400, {"de": "Heiße Getränke am Weihnachtsmarkt", "en": "Hot drinks at the Christmas market", "ru": "Горячие напитки на рождественской ярмарке"}),
]
DIST = ["400 m", "550 m", "600 m", "900 m", "2 km", "2,1 km", "12 km", "16 km"]

T = {}

T["de"] = dict(
    lang="de", path="", up="",
    title="Ferienwohnung Reese-Horstmann · Bad Harzburg mit Hallenbad und Saunen",
    desc="Gemütliche Ferienwohnung für bis zu 4 Personen in Bad Harzburg: am Waldrand, mit Hallenbad und zwei Saunen im Haus, großem Balkon und kostenlosem Parkplatz. Direkt bei den Gastgebern anfragen.",
    draft="Entwurf – noch nicht freigegeben.",
    brand="Ferienwohnung Reese-Horstmann", brand_sub="Bad Harzburg · Harz zu jeder Jahreszeit",
    nav=["Wohnung", "Lage", "Preise", "Anfrage"], ask="Anfragen",
    hero_eyebrow="Ferienwohnung in Bad Harzburg",
    hero_h1="Harz zu jeder Jahreszeit – mit Hallenbad und Saunen im Haus",
    hero_lead="Ruhige, renovierte Wohnung für bis zu 4 Personen, direkt am Waldrand am Ende einer Sackgasse. Morgens Frühstück auf dem großen Balkon, tagsüber wandern im Nationalpark, abends schwimmen und saunieren.",
    btn_direct="Direkt anfragen", btn_view="Wohnung ansehen",
    rating="Hervorragend · 38 Bewertungen auf Booking.com",
    hero_cap="Aussicht im Harz bei Bad Harzburg",
    hl=[("Hallenbad und 2 Saunen", "Im Haus, kostenlos für Gäste"),
        ("Am Waldrand", "Ruhig am Ende einer Sackgasse, Nationalpark 2 km"),
        ("Großer Balkon", "Süd-West mit Blick in den Garten"),
        ("Parkplatz und WLAN", "Beides kostenlos")],
    w_eyebrow="Die Wohnung", w_h2="Gemütlich, komplett ausgestattet, für bis zu 4 Gäste",
    w_lead="Alle Räume sind renoviert, ein Großteil der Möbel ist neu. Nur die ganz gemütlichen sind geblieben.",
    rooms_h="Räume",
    rooms=["52 m² in der 3. Etage, mit Fahrstuhl",
           "Schlafzimmer mit Doppelbett 180 × 200 cm und eigenem Fernseher",
           "Wohnzimmer mit Schlafsofa für zwei weitere Gäste, Flachbild-TV, DVD- und CD-Player",
           "Essecke, die zum Sitzenbleiben einlädt",
           "Helle Küchenzeile mit Mini-Backofen, Mikrowelle, Kühlschrank mit Gefrierfach, Kaffeemaschine, Wasserkocher, Toaster und Eierkocher",
           "Duschbad mit Haartrockner",
           "Großer Süd-West-Balkon"],
    extras_h="Extras",
    extras=["Hallenbad und zwei Saunen im Haus, kostenlos",
            "Sole-Therme nur 400 m entfernt",
            "Bücher und Gesellschaftsspiele",
            "Ausflugstipps und Material zum Harz im Schrank",
            "Kostenloser Parkplatz und WLAN",
            "Kissen, Decken, Spülmittel, Seife und Reinigungsmittel sind da",
            "Waschmaschine im Haus (gegen Gebühr)",
            "Gästekarte: kostenlos Bus fahren, vergünstigter Eintritt"],
    pool_h="Hallenbad und Saunen",
    pool=["Hallenbad täglich von 7 bis 21 Uhr (mit Mittagspause)",
          "Ohne Anmeldung, so oft Sie möchten",
          "Zugang mit eigenem Transponder",
          "Zwei Saunen, an bestimmten Tagen geöffnet, ebenfalls ohne Anmeldung",
          "Saunatuch bitte selbst mitbringen"],
    plan="Grundriss der Wohnung ansehen",
    l_eyebrow="Lage und Ausflüge", l_h2="Mitten im Grünen, trotzdem zentral",
    l_lead="Die Wohnung liegt in der Kurhausstraße in Bad Harzburg, direkt am Waldrand. Restaurants sind zu Fuß erreichbar, der Nationalpark Harz beginnt gleich hinter dem Haus.",
    season=["Frühling bis Herbst", "Winter"],
    trips_h="Ausflüge",
    trips=["Burgberg mit Seilbahn", "Baumwipfelpfad und Baumschwebebahn", "Radau-Wasserfall und Rabenklippen",
           "Sole-Therme und Kurpark", "Goslar mit Kaiserpfalz und Altstadt", "Wandern und im Winter Skifahren"],
    dist_h="Entfernungen",
    dist=["Sole-Therme (Solebad)", "Restaurant Hexenklause", "Restaurant Salz &amp; Seele", "Restaurant Tauts",
          "Nationalpark Harz", "Bahnhof Bad Harzburg", "Goslar, Altstadt", "Bergwerk Rammelsberg (Welterbe)"],
    approx="ca.", map="Auf der Karte ansehen (OpenStreetMap)",
    s_eyebrow="Was Gäste sagen", s_h2="9,0 von 10 aus 38 Bewertungen",
    quotes=["„Der unkomplizierte Zugang zu dem Schwimmbad war für uns alle eine große Bereicherung.“",
            "„Zentral gelegen, sehr guter Ausgangspunkt für Ausflüge. Sauber, gut ausgestattet.“",
            "„Die Wohnung war durchweg sauber und super eingerichtet. Der Kontakt zum Vermieter war freundlich und kompetent.“"],
    scores=["Gastgeber", "Preis-Leistung", "Komfort", "Ausstattung", "Sauberkeit", "Lage"],
    s_src="Gästebewertungen auf Booking.com, Stand Oktober 2026. Ausgezeichnet mit dem Traveller Review Award 2023 von Booking.com.",
    p_eyebrow="Preise und Ablauf", p_h2="Direkt bei uns buchen",
    p_text="Schreiben Sie uns einfach, wann Sie kommen möchten. Wir melden uns persönlich mit Preis und Verfügbarkeit. Wer direkt bucht, zahlt keine Portalgebühr.",
    steps=[("Anfrage", "per E-Mail oder WhatsApp"), ("Bestätigung", "mit Preis von uns"),
           ("Anzahlung", "von 100 € innerhalb einer Woche"), ("Restzahlung", "30 Tage vor Anreise, per Überweisung oder PayPal"),
           ("Anreiseinfos", "und Gästekarte per Post, sobald alles bezahlt ist"),
           ("Schlüsselsafe", "Code einen Tag vor Anreise per WhatsApp")],
    info_h="Gut zu wissen",
    info=[("Preis pro Nacht", "50–70 € für 2 Personen, je nach Saison"),
          ("Jede weitere Person", "Erwachsene 10 €, Kinder 8 € pro Nacht"),
          ("Bearbeitungsgebühr inkl. Endreinigung", "einmalig 60 € pro Aufenthalt"),
          ("Mindestaufenthalt", "2 Nächte"),
          ("Gästebeitrag (Kurtaxe) Bad Harzburg", "3 € pro Erwachsenem und Nacht, Kinder frei"),
          ("Bettwäsche und Handtücher", "bitte mitbringen oder als Wäschepaket buchen: 20 € pro Person für Bettwäsche, Handtuch und Badetuch (ohne Saunatuch)"),
          ("Parken", "kostenlos auf dem Parkplatz oder Parkdeck direkt am Haus"),
          ("Spülmaschine", "nicht vorhanden"),
          ("Stornierung", "bis 30 Tage vor Anreise kostenlos"),
          ("Anreise", "14:00 bis 19:00 Uhr"),
          ("Abreise", "08:30 bis 10:00 Uhr"),
          ("Kinder", "ab 3 Jahren willkommen"),
          ("Rauchen", "nur auf dem Balkon"),
          ("Haustiere, Grillen, Partys", "leider nicht möglich"),
          ("Ruhezeiten", "13:00 bis 15:00 und 22:00 bis 07:00 Uhr")],
    a_eyebrow="Anfrage", a_h2="Wir freuen uns auf Sie",
    a_text="Ihre Gastgeber, Familie Reese. Wir wohnen in Bramsche bei Osnabrück; Bad Harzburg ist unser Ausgleich zu Job und Alltag geworden. Wir sprechen Deutsch, Englisch und Russisch.",
    mobile_label="Mobil und WhatsApp", mobile_no="0174 4283147", phone_no="05468 8068890", phone_label="Telefon", mail_label="E-Mail",
    booking_hint='Auch auf <a href="https://www.booking.com/hotel/de/ferienwohnung-reese-horstmann.de.html" rel="noopener">Booking.com</a> buchbar.',
    f_von="Anreise", f_bis="Abreise", f_erw="Erwachsene", f_kind="Kinder (ab 3 J.)", f_name="Ihr Name",
    f_msg="Nachricht (optional)", f_msg_ph="z. B. Wäschepaket gewünscht",
    btn_wa="Per WhatsApp anfragen", btn_mail="Per E-Mail anfragen",
    f_hint="Ihre Angaben werden nicht auf dieser Website gespeichert. Die Knöpfe öffnen Ihr E-Mail-Programm oder WhatsApp mit einer fertigen Nachricht.",
    legal=["Impressum", "Datenschutz"],
    lb=["Fotoansicht", "Schließen", "Vorheriges Foto", "Nächstes Foto"],
    js=dict(hello="Hallo Familie Reese,", interest="wir interessieren uns für Ihre Ferienwohnung in Bad Harzburg.",
            period="Zeitraum", guests="Gäste", adults="Erwachsene", children="Kinder",
            regards="Viele Grüße", subject="Anfrage Ferienwohnung Bad Harzburg"),
)

T["en"] = dict(
    lang="en", path="en/", up="../",
    title="Holiday apartment Reese-Horstmann · Bad Harzburg with indoor pool and saunas",
    desc="Cosy holiday apartment for up to 4 guests in Bad Harzburg, Germany: by the forest, with an indoor pool and two saunas in the building, a large balcony and free parking. Contact the hosts directly.",
    draft="Draft – not yet published.",
    brand="Holiday apartment Reese-Horstmann", brand_sub="Bad Harzburg · The Harz in every season",
    nav=["Apartment", "Location", "Prices", "Enquiry"], ask="Enquire",
    hero_eyebrow="Holiday apartment in Bad Harzburg, Germany",
    hero_h1="The Harz in every season – with indoor pool and saunas in the building",
    hero_lead="Quiet, renovated apartment for up to 4 guests, right at the edge of the forest at the end of a cul-de-sac. Breakfast on the large balcony, hiking in the national park by day, swimming and saunas in the evening.",
    btn_direct="Enquire directly", btn_view="See the apartment",
    rating="Excellent · 38 reviews on Booking.com",
    hero_cap="View over the Harz near Bad Harzburg",
    hl=[("Indoor pool and 2 saunas", "In the building, free for guests"),
        ("By the forest", "Quiet, at the end of a cul-de-sac, national park 2 km"),
        ("Large balcony", "South-west facing, overlooking the garden"),
        ("Parking and Wi-Fi", "Both free of charge")],
    w_eyebrow="The apartment", w_h2="Cosy and fully equipped for up to 4 guests",
    w_lead="All rooms have been renovated and most of the furniture is new. Only the really comfortable pieces stayed.",
    rooms_h="Rooms",
    rooms=["52 m² on the 3rd floor, with lift",
           "Bedroom with a 180 × 200 cm double bed and its own TV",
           "Living room with a sofa bed for two more guests, flat-screen TV, DVD and CD player",
           "Dining area that invites you to linger",
           "Bright kitchenette with mini oven, microwave, fridge with freezer compartment, coffee maker, kettle, toaster and egg cooker",
           "Shower room with hairdryer",
           "Large south-west balcony"],
    extras_h="Extras",
    extras=["Indoor pool and two saunas in the building, free of charge",
            "Brine spa (Sole-Therme) only 400 m away",
            "Books and board games",
            "Tips and guides for trips in the Harz",
            "Free parking and Wi-Fi",
            "Pillows, blankets, washing-up liquid, soap and cleaning supplies provided",
            "Washing machine in the building (for a fee)",
            "Guest card: free buses, reduced admission"],
    pool_h="Indoor pool and saunas",
    pool=["Indoor pool open daily 7 am to 9 pm (with a midday break)",
          "No booking needed, use it as often as you like",
          "Access with your own transponder",
          "Two saunas, open on certain days, also no booking needed",
          "Please bring your own sauna towel"],
    plan="View the floor plan",
    l_eyebrow="Location and trips", l_h2="Surrounded by nature, yet central",
    l_lead="The apartment is on Kurhausstraße in Bad Harzburg, right at the edge of the forest. Restaurants are within walking distance and the Harz National Park starts just behind the house.",
    season=["Spring to autumn", "Winter"],
    trips_h="Things to do",
    trips=["Burgberg hill with cable car", "Treetop walk and suspended forest railway", "Radau waterfall and Rabenklippen cliffs",
           "Brine spa and spa park", "Goslar with its imperial palace and old town", "Hiking, and skiing in winter"],
    dist_h="Distances",
    dist=["Brine spa (Sole-Therme)", "Restaurant Hexenklause", "Restaurant Salz &amp; Seele", "Restaurant Tauts",
          "Harz National Park", "Bad Harzburg station", "Goslar old town", "Rammelsberg mine (UNESCO World Heritage)"],
    approx="approx.", map="View on the map (OpenStreetMap)",
    s_eyebrow="What guests say", s_h2="9.0 out of 10 from 38 reviews",
    quotes=["“The easy access to the swimming pool was a real highlight for all of us.”",
            "“Central location, a great base for trips. Clean and well equipped.”",
            "“The apartment was spotless and beautifully furnished. The hosts were friendly and helpful.”"],
    scores=["Host", "Value for money", "Comfort", "Facilities", "Cleanliness", "Location"],
    s_src="Guest reviews on Booking.com, translated from German, as of October 2026. Winner of the Booking.com Traveller Review Award 2023.",
    p_eyebrow="Prices and booking", p_h2="Book directly with us",
    p_text="Just tell us when you would like to come. We will reply personally with the price and availability. Booking directly means no platform fees.",
    steps=[("Enquiry", "by email or WhatsApp"), ("Confirmation", "with the price from us"),
           ("Deposit", "of €100 within one week"), ("Balance", "30 days before arrival, by bank transfer or PayPal"),
           ("Arrival details", "and guest card by post once payment is complete"),
           ("Key safe", "code via WhatsApp one day before arrival")],
    info_h="Good to know",
    info=[("Price per night", "€50–70 for 2 guests, depending on the season"),
          ("Each additional guest", "adults €10, children €8 per night"),
          ("Service fee incl. final cleaning", "€60 once per stay"),
          ("Minimum stay", "2 nights"),
          ("Visitor tax (Kurtaxe) Bad Harzburg", "€3 per adult per night, children free"),
          ("Bed linen and towels", "please bring your own or book the linen package: €20 per person for bed linen, hand towel and bath towel (no sauna towel)"),
          ("Parking", "free, in the car park or parking deck right by the building"),
          ("Dishwasher", "not available"),
          ("Cancellation", "free up to 30 days before arrival"),
          ("Check-in", "2 pm to 7 pm"),
          ("Check-out", "8:30 am to 10 am"),
          ("Children", "welcome from age 3"),
          ("Smoking", "on the balcony only"),
          ("Pets, barbecues, parties", "not allowed"),
          ("Quiet hours", "1 pm to 3 pm and 10 pm to 7 am")],
    a_eyebrow="Enquiry", a_h2="We look forward to welcoming you",
    a_text="Your hosts, the Reese family. We live in Bramsche near Osnabrück; Bad Harzburg has become our place to unwind. We speak German, English and Russian.",
    mobile_label="Mobile and WhatsApp", mobile_no="+49 174 4283147", phone_no="+49 5468 8068890", phone_label="Landline", mail_label="Email",
    booking_hint='Also bookable on <a href="https://www.booking.com/hotel/de/ferienwohnung-reese-horstmann.en-gb.html" rel="noopener">Booking.com</a>.',
    f_von="Arrival", f_bis="Departure", f_erw="Adults", f_kind="Children (age 3+)", f_name="Your name",
    f_msg="Message (optional)", f_msg_ph="e.g. linen package wanted",
    btn_wa="Enquire via WhatsApp", btn_mail="Enquire by email",
    f_hint="Your details are not stored on this website. The buttons open your email app or WhatsApp with a ready-made message.",
    legal=["Impressum (legal notice)", "Datenschutz (privacy)"],
    lb=["Photo viewer", "Close", "Previous photo", "Next photo"],
    js=dict(hello="Dear Reese family,", interest="we are interested in your holiday apartment in Bad Harzburg.",
            period="Dates", guests="Guests", adults="adults", children="children",
            regards="Kind regards", subject="Enquiry holiday apartment Bad Harzburg"),
)

T["ru"] = dict(
    lang="ru", path="ru/", up="../",
    title="Апартаменты Reese-Horstmann · Бад-Харцбург, бассейн и сауны",
    desc="Уютные апартаменты для отдыха до 4 человек в Бад-Харцбурге (Германия): у леса, с крытым бассейном и двумя саунами в доме, большим балконом и бесплатной парковкой. Пишите хозяевам напрямую.",
    draft="Черновик – ещё не опубликовано.",
    brand="Апартаменты Reese-Horstmann", brand_sub="Бад-Харцбург · Гарц в любое время года",
    nav=["Квартира", "Расположение", "Цены", "Запрос"], ask="Запрос",
    hero_eyebrow="Апартаменты для отдыха в Бад-Харцбурге",
    hero_h1="Гарц в любое время года – с бассейном и саунами в доме",
    hero_lead="Тихая, отремонтированная квартира до 4 человек, прямо у леса, в конце тупиковой улицы. Утром завтрак на большом балконе, днём прогулки по национальному парку, вечером бассейн и сауны.",
    btn_direct="Написать напрямую", btn_view="Посмотреть квартиру",
    rating="Превосходно · 38 отзывов на Booking.com",
    hero_cap="Вид на горы Гарц у Бад-Харцбурга",
    hl=[("Бассейн и 2 сауны", "В доме, бесплатно для гостей"),
        ("У самого леса", "Тихо, в конце тупика, национальный парк в 2 км"),
        ("Большой балкон", "На юго-запад, с видом на сад"),
        ("Парковка и Wi-Fi", "Бесплатно")],
    w_eyebrow="Квартира", w_h2="Уютно, всё необходимое, до 4 гостей",
    w_lead="Все комнаты отремонтированы, большая часть мебели новая. Остались только самые уютные вещи.",
    rooms_h="Комнаты",
    rooms=["52 м² на 3-м этаже, есть лифт",
           "Спальня с двуспальной кроватью 180 × 200 см и отдельным телевизором",
           "Гостиная с диваном-кроватью ещё для двух гостей, плоский телевизор, DVD- и CD-плеер",
           "Обеденный уголок, где хочется посидеть подольше",
           "Светлая кухня: мини-духовка, микроволновка, холодильник с морозилкой, кофеварка, чайник, тостер и яйцеварка",
           "Ванная с душем и феном",
           "Большой балкон на юго-запад"],
    extras_h="Дополнительно",
    extras=["Крытый бассейн и две сауны в доме, бесплатно",
            "Соляные термы (Sole-Therme) всего в 400 м",
            "Книги и настольные игры",
            "Советы и материалы для поездок по Гарцу",
            "Бесплатная парковка и Wi-Fi",
            "Подушки, одеяла, средство для мытья посуды, мыло и чистящие средства есть",
            "Стиральная машина в доме (платно)",
            "Карта гостя: бесплатные автобусы, скидки на входные билеты"],
    pool_h="Бассейн и сауны",
    pool=["Бассейн открыт ежедневно с 7:00 до 21:00 (с обеденным перерывом)",
          "Без записи, сколько угодно",
          "Вход по собственному транспондеру",
          "Две сауны, открыты в определённые дни, тоже без записи",
          "Полотенце для сауны, пожалуйста, возьмите с собой"],
    plan="Посмотреть план квартиры",
    l_eyebrow="Расположение и экскурсии", l_h2="На природе, но в центре",
    l_lead="Квартира находится на улице Kurhausstraße в Бад-Харцбурге, прямо у леса. До ресторанов можно дойти пешком, национальный парк Гарц начинается сразу за домом.",
    season=["С весны до осени", "Зима"],
    trips_h="Куда сходить",
    trips=["Гора Бургберг с канатной дорогой", "Тропа по верхушкам деревьев и подвесная дорога", "Водопад Радау и скалы Рабенклиппен",
           "Соляные термы и курортный парк", "Гослар: императорский дворец и старый город", "Пешие прогулки, зимой лыжи"],
    dist_h="Расстояния",
    dist=["Соляные термы (Sole-Therme)", "Ресторан Hexenklause", "Ресторан Salz &amp; Seele", "Ресторан Tauts",
          "Национальный парк Гарц", "Вокзал Бад-Харцбург", "Гослар, старый город", "Рудник Раммельсберг (наследие ЮНЕСКО)"],
    approx="ок.", map="Посмотреть на карте (OpenStreetMap)",
    s_eyebrow="Отзывы гостей", s_h2="9,0 из 10 по 38 отзывам",
    quotes=["«Удобный доступ к бассейну очень порадовал всех нас.»",
            "«Центральное расположение, отличная отправная точка для поездок. Чисто, хорошо оборудовано.»",
            "«Квартира была очень чистой и прекрасно обставленной. Хозяева приветливые и компетентные.»"],
    scores=["Хозяева", "Цена/качество", "Комфорт", "Оснащение", "Чистота", "Расположение"],
    s_src="Отзывы гостей на Booking.com, перевод с немецкого, октябрь 2026. Награда Booking.com Traveller Review Award 2023.",
    p_eyebrow="Цены и бронирование", p_h2="Бронируйте напрямую у нас",
    p_text="Просто напишите, когда вы хотите приехать. Мы лично ответим с ценой и наличием свободных дат. При прямом бронировании нет комиссии платформы.",
    steps=[("Запрос", "по электронной почте или в WhatsApp"), ("Подтверждение", "с ценой от нас"),
           ("Предоплата", "100 € в течение недели"), ("Остаток", "за 30 дней до заезда, банковским переводом или через PayPal"),
           ("Информация о заезде", "и карта гостя по почте после полной оплаты"),
           ("Сейф для ключей", "код в WhatsApp за день до заезда")],
    info_h="Полезно знать",
    info=[("Цена за ночь", "50–70 € за 2 человек, в зависимости от сезона"),
          ("Каждый следующий гость", "взрослый 10 €, ребёнок 8 € за ночь"),
          ("Сервисный сбор, включая финальную уборку", "60 € единоразово за проживание"),
          ("Минимальный срок", "2 ночи"),
          ("Курортный сбор Бад-Харцбурга", "3 € со взрослого за ночь, дети бесплатно"),
          ("Постельное бельё и полотенца", "возьмите с собой или закажите комплект: 20 € на человека (постельное бельё, полотенце и банное полотенце, без полотенца для сауны)"),
          ("Парковка", "бесплатно, на стоянке или парковочной палубе рядом с домом"),
          ("Посудомоечная машина", "нет"),
          ("Отмена", "бесплатно до 30 дней до заезда"),
          ("Заезд", "с 14:00 до 19:00"),
          ("Выезд", "с 08:30 до 10:00"),
          ("Дети", "с 3 лет"),
          ("Курение", "только на балконе"),
          ("Животные, гриль, вечеринки", "к сожалению, нельзя"),
          ("Время тишины", "с 13:00 до 15:00 и с 22:00 до 07:00")],
    a_eyebrow="Запрос", a_h2="Будем рады вас видеть",
    a_text="Ваши хозяева, семья Reese. Мы живём в Брамше под Оснабрюком, а Бад-Харцбург стал для нас местом отдыха от работы и будней. Мы говорим по-немецки, по-английски и по-русски.",
    mobile_label="Мобильный и WhatsApp", mobile_no="+49 174 4283147", phone_no="+49 5468 8068890", phone_label="Телефон", mail_label="Эл. почта",
    booking_hint='Также можно забронировать на <a href="https://www.booking.com/hotel/de/ferienwohnung-reese-horstmann.ru.html" rel="noopener">Booking.com</a>.',
    f_von="Заезд", f_bis="Выезд", f_erw="Взрослые", f_kind="Дети (от 3 лет)", f_name="Ваше имя",
    f_msg="Сообщение (по желанию)", f_msg_ph="например, нужен комплект белья",
    btn_wa="Написать в WhatsApp", btn_mail="Написать на почту",
    f_hint="Ваши данные не сохраняются на этом сайте. Кнопки открывают почтовую программу или WhatsApp с готовым сообщением.",
    legal=["Impressum (выходные данные)", "Datenschutz (конфиденциальность)"],
    lb=["Просмотр фото", "Закрыть", "Предыдущее фото", "Следующее фото"],
    js=dict(hello="Здравствуйте, семья Reese!", interest="Нас интересуют ваши апартаменты в Бад-Харцбурге.",
            period="Даты", guests="Гости", adults="взр.", children="дет.",
            regards="С уважением", subject="Запрос: апартаменты в Бад-Харцбурге"),
)

ICONS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 18c2 0 2-1.5 4-1.5S8 18 10 18s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5M2 22c2 0 2-1.5 4-1.5S8 22 10 22s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5M8 15V5a2 2 0 0 1 4 0M16 15V5a2 2 0 0 0-4 0M8 9h8"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 5 12h4l-4 6h14l-4-6h4z"/><path d="M12 18v4"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M12 1v1M4.2 4.2l.7.7M1 12h1M22 12h1M19.1 4.9l.7-.7M3 21h18M6 21v-5h12v5"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>',
]
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2s.2-1.1.1-1.2l-.5-.3z"/></svg>'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%232f5d46'/%3E%3Cpath d='M12 46 26 24l8 12 6-8 12 18z' fill='%23f7f4ee'/%3E%3C/svg%3E"
LANGS = [("de", "DE"), ("en", "EN"), ("ru", "RU")]
OG_LOCALE = {"de": "de_DE", "en": "en_GB", "ru": "ru_RU"}
SCORES = ["9,7", "9,6", "9,5", "9,3", "9,2", "9,2"]


def a(s):
    """Text für HTML-Attribute."""
    return html.escape(s, quote=True)


def page(t):
    up = t["up"]
    dec = (lambda s: s.replace(",", ".")) if t["lang"] == "en" else (lambda s: s)
    li = lambda items: "\n".join(f"          <li>{x}</li>" for x in items)

    switch = " ".join(
        f'<a href="{up}{"" if code == "de" else code + "/"}" hreflang="{code}" lang="{code}"'
        + (' aria-current="true"' if code == t["lang"] else "") + f">{label}</a>"
        for code, label in LANGS)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="{SITE}{"" if code == "de" else code + "/"}">' for code, _ in LANGS)

    gallery = "\n".join(
        f'      <figure class="ph{" " + cls if cls else ""}"><img src="{up}fotos/{f}" alt="{a(cap[t["lang"]])}" loading="lazy" width="{w}" height="{h}"><figcaption>{cap[t["lang"]]}</figcaption></figure>'
        for f, w, h, cls, cap in GALLERY)
    trips_gal = "\n".join(
        f'      <figure class="ph"><img src="{up}fotos/{f}" alt="{a(cap[t["lang"]])}" loading="lazy" width="{w}" height="{h}"><figcaption>{cap[t["lang"]]}</figcaption></figure>'
        for f, w, h, cap in TRIPS)
    winter_gal = "\n".join(
        f'      <figure class="ph"><img src="{up}fotos/{f}" alt="{a(cap[t["lang"]])}" loading="lazy" width="{w}" height="{h}"><figcaption>{cap[t["lang"]]}</figcaption></figure>'
        for f, w, h, cap in WINTER)
    hl = "\n".join(f"    <div>\n      {ICONS[i]}\n      <h3>{h}</h3><p>{p}</p>\n    </div>" for i, (h, p) in enumerate(t["hl"]))
    dist = "\n".join(
        f'          <li><span>{n}</span><span>{(t["approx"] + " ") if d == "12 km" else ""}{dec(d)}</span></li>'
        for n, d in zip(t["dist"], DIST))
    quotes = "\n".join(f"      <blockquote>{q}</blockquote>" for q in t["quotes"])
    scores = "\n".join(f"      <span>{n} <b>{dec(v)}</b></span>" for n, v in zip(t["scores"], SCORES))
    steps = "\n".join(f"        <li><b>{b}</b> {r}</li>" for b, r in t["steps"])
    info = "\n".join(f"        <tr><td>{k}</td><td>{v}</td></tr>" for k, v in t["info"])
    erw = "".join(f"<option{' selected' if n == 2 else ''}>{n}</option>" for n in range(1, 5))
    kind = "".join(f"<option{' selected' if n == 0 else ''}>{n}</option>" for n in range(0, 4))

    ld = json.dumps({
        "@context": "https://schema.org", "@type": "VacationRental",
        "name": t["brand"], "description": t["desc"], "url": SITE + t["path"],
        "image": [SITE + "fotos/" + f for f in ("hallenbad.jpg", "wohnzimmer.jpg", "schlafzimmer.jpg", "bank-aussicht.jpg")],
        "telephone": "+49 174 4283147", "email": "harz.fewo@web.de",
        "address": {"@type": "PostalAddress", "streetAddress": "Kurhausstraße 18", "postalCode": "38667",
                    "addressLocality": "Bad Harzburg", "addressCountry": "DE"},
        "containsPlace": {"@type": "Accommodation", "occupancy": {"@type": "QuantitativeValue", "maxValue": 4},
                          "numberOfBedrooms": 1},
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True}
                           for n in ("Indoor pool", "Saunas", "Free parking", "Free Wi-Fi", "Balcony")],
        "checkinTime": "14:00", "checkoutTime": "10:00", "petsAllowed": False,
    }, ensure_ascii=False)
    draft_bar = f'<div class="draft">{t["draft"]}</div>\n\n' if DRAFT else ""
    robots = '<meta name="robots" content="noindex, nofollow">\n' if DRAFT else ""

    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{a(t['desc'])}">
{robots}<meta name="theme-color" content="#2f5d46">
<link rel="canonical" href="{SITE}{t['path']}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:title" content="{a(t['title'])}">
<meta property="og:description" content="{a(t['desc'])}">
<meta property="og:url" content="{SITE}{t['path']}">
<meta property="og:image" content="{SITE}fotos/hallenbad.jpg">
<meta property="og:locale" content="{OG_LOCALE[t['lang']]}">
<script type="application/ld+json">{ld}</script>
<link rel="stylesheet" href="{up}style.css">
<link rel="icon" href="{FAVICON}">
</head>
<body class="has-mbar">
<!-- Erzeugt mit build.py – Änderungen bitte dort machen. -->

{draft_bar}<header class="top">
  <div class="wrap">
    <a class="brand" href="#start">{t['brand']}<small>{t['brand_sub']}</small></a>
    <nav class="nav">
      <a href="#wohnung">{t['nav'][0]}</a>
      <a href="#lage">{t['nav'][1]}</a>
      <a href="#preise">{t['nav'][2]}</a>
      <a href="#anfrage">{t['nav'][3]}</a>
    </nav>
    <div class="head-right">
      <nav class="langs" aria-label="Sprache / Language / Язык">{switch}</nav>
      <a class="btn btn-primary btn-sm" href="#anfrage">{t['ask']}</a>
    </div>
  </div>
</header>

<main id="start">

<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow">{t['hero_eyebrow']}</div>
      <h1>{t['hero_h1']}</h1>
      <p class="lead">{t['hero_lead']}</p>
      <div class="actions">
        <a class="btn btn-primary" href="#anfrage">{t['btn_direct']}</a>
        <a class="btn btn-ghost" href="#wohnung">{t['btn_view']}</a>
      </div>
      <div class="rating"><b>{dec('9,0')}</b> {t['rating']}</div>
    </div>
    <figure class="ph tall"><img src="{up}fotos/bank-aussicht.jpg" alt="{a(t['hero_cap'])}" width="960" height="720"><figcaption>{t['hero_cap']}</figcaption></figure>
  </div>
</section>

<section class="wood" style="padding:32px 0">
  <div class="wrap hl">
{hl}
  </div>
</section>

<section id="wohnung">
  <div class="wrap">
    <div class="eyebrow">{t['w_eyebrow']}</div>
    <h2>{t['w_h2']}</h2>
    <p class="lead">{t['w_lead']}</p>

    <div class="gallery" style="margin:28px 0 36px">
{gallery}
    </div>

    <div class="cols">
      <div class="card">
        <h3>{t['rooms_h']}</h3>
        <ul class="ticks">
{li(t['rooms'])}
        </ul>
      </div>
      <div class="card">
        <h3>{t['extras_h']}</h3>
        <ul class="ticks">
{li(t['extras'])}
        </ul>
      </div>
    </div>
    <div class="card" style="margin-top:28px">
      <h3>{t['pool_h']}</h3>
      <ul class="ticks">
{li(t['pool'])}
      </ul>
    </div>
  </div>
</section>

<section id="lage" class="alt">
  <div class="wrap">
    <div class="eyebrow">{t['l_eyebrow']}</div>
    <h2>{t['l_h2']}</h2>
    <p class="lead">{t['l_lead']}</p>
    <h3 class="season">{t['season'][0]}</h3>
    <div class="gallery">
{trips_gal}
    </div>
    <h3 class="season">{t['season'][1]}</h3>
    <div class="gallery g3">
{winter_gal}
    </div>
    <div class="cols">
      <div class="card">
        <h3>{t['trips_h']}</h3>
        <ul class="ticks">
{li(t['trips'])}
        </ul>
      </div>
      <div class="card">
        <h3>{t['dist_h']}</h3>
        <ul class="dist">
{dist}
        </ul>
        <p class="src"><a href="https://www.openstreetmap.org/search?query=Kurhausstra%C3%9Fe%2018%2C%2038667%20Bad%20Harzburg" rel="noopener">{t['map']}</a></p>
      </div>
    </div>
  </div>
</section>

<section id="stimmen">
  <div class="wrap">
    <div class="eyebrow">{t['s_eyebrow']}</div>
    <h2>{t['s_h2']}</h2>
    <div class="quotes" style="margin-top:20px">
{quotes}
    </div>
    <div class="scores">
{scores}
    </div>
    <p class="src">{t['s_src']}</p>
  </div>
</section>

<section id="preise" class="wood">
  <div class="wrap cols">
    <div>
      <div class="eyebrow">{t['p_eyebrow']}</div>
      <h2>{t['p_h2']}</h2>
      <p>{t['p_text']}</p>
      <ol class="steps">
{steps}
      </ol>
    </div>
    <div class="card">
      <h3>{t['info_h']}</h3>
      <table class="prices">
{info}
      </table>
    </div>
  </div>
</section>

<section id="anfrage">
  <div class="wrap cols">
    <div>
      <div class="eyebrow">{t['a_eyebrow']}</div>
      <h2>{t['a_h2']}</h2>
      <p>{t['a_text']}</p>
      <ul class="contact-lines">
        <li>{t['mobile_label']}: <a href="tel:+491744283147">{t['mobile_no']}</a></li>
        <li>{t['phone_label']}: <a href="tel:+4954688068890">{t['phone_no']}</a></li>
        <li>{t['mail_label']}: <a href="mailto:harz.fewo@web.de">harz.fewo@web.de</a></li>
      </ul>
      <p class="hint">{t['booking_hint']}</p>
    </div>
    <form class="ask card" id="ask" novalidate>
      <div class="two">
        <div><label for="von">{t['f_von']}</label><input type="date" id="von" required></div>
        <div><label for="bis">{t['f_bis']}</label><input type="date" id="bis" required></div>
      </div>
      <div class="two">
        <div><label for="erw">{t['f_erw']}</label><select id="erw">{erw}</select></div>
        <div><label for="kind">{t['f_kind']}</label><select id="kind">{kind}</select></div>
      </div>
      <div><label for="name">{t['f_name']}</label><input id="name" autocomplete="name"></div>
      <div><label for="msg">{t['f_msg']}</label><textarea id="msg" placeholder="{a(t['f_msg_ph'])}"></textarea></div>
      <div class="actions">
        <button class="btn btn-wa" type="button" data-send="wa">
          {WA_ICON}
          {t['btn_wa']}
        </button>
        <button class="btn btn-ghost" type="button" data-send="mail">{t['btn_mail']}</button>
      </div>
      <p class="hint">{t['f_hint']}</p>
    </form>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <div>{t['brand']} · Kurhausstraße 18 · 38667 Bad Harzburg</div>
    <div><a href="{up}impressum.html">{t['legal'][0]}</a> · <a href="{up}datenschutz.html">{t['legal'][1]}</a></div>
  </div>
</footer>

<div class="mbar">
  <a class="btn btn-wa" href="https://wa.me/491744283147" rel="noopener">WhatsApp</a>
  <a class="btn btn-primary" href="#anfrage">{t['ask']}</a>
</div>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="{a(t['lb'][0])}">
  <div class="lb-scroll"><img alt=""></div>
  <button class="x" type="button" aria-label="{a(t['lb'][1])}">×</button>
  <button class="prev" type="button" aria-label="{a(t['lb'][2])}">‹</button>
  <button class="next" type="button" aria-label="{a(t['lb'][3])}">›</button>
  <div class="cap"></div>
</div>

<script>window.FEWO = {json.dumps(t['js'], ensure_ascii=False)};</script>
<script src="{up}site.js"></script>
</body>
</html>
"""


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    for code, t in T.items():
        out = os.path.join(root, t["path"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(page(t))
        print("geschrieben:", os.path.relpath(out, root))
