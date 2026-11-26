# GIEAG Lagekarten – Projektnotiz für Claude Code

## Was das ist
Ein eigenes Browser-Tool von Julius (Projektentwickler/Architekt, GIEAG München) zum Erzeugen von
Übersichtskarten und Lageplänen für Präsentationen (Expo Real, Projektsteckbriefe).
Eine einzige HTML-Datei, kein Build. Läuft über GitHub Pages (siehe unten), funktioniert aber auch lokal per Doppelklick.

## Arbeitsweise (GitHub Pages, Live + Entwurf)
- Live:    `index.html`          → https://jhaas-cmd.github.io/lagekarten/
- Entwurf: `entwurf/index.html`  → https://jhaas-cmd.github.io/lagekarten/entwurf/
- Julius äußert Änderungswünsche im Chat. Änderungen **nur im Entwurf**, gezielt an der betroffenen Stelle,
  nie die Datei neu aufbauen. Commit + Push auf `main`; Julius lädt den Entwurf nach ~1 Min. mit F5 neu.
- „Übernehmen“: Entwurf nach `index.html` kopieren, dabei die rote ENTWURF-Kennung im Kopf entfernen.
- „Verwerfen“: `entwurf/index.html` wieder aus `index.html` herstellen (ENTWURF-Kennung wieder einsetzen).
- Live und Entwurf liegen auf derselben Domain und teilen sich die gespeicherten Projekte (localStorage).
- Git-Historie ersetzt Versionsnummern; keine Dateien wie `_27`, `_28` anlegen.
- Sprache der Oberfläche und der Kommentare: Deutsch.
- Julius ist Architekt, kein Programmierer: Rückfragen und Erklärungen fachlich, nicht technisch formulieren.

## Aufbau der Datei
- Zeile ~8–10: MapLibre-GL-CSS (Version 4.7.1, eingebettet)
- Zeile ~11–72: MapLibre GL JS 4.7.1, minifiziert eingebettet – **nicht anfassen**
- danach: eigenes CSS der App
- `<body>`: Seitenleiste (`<aside>`, feste Breite 320 px); rechts Reiterleiste (Registerlaschen) + Bühne mit je einer Karte
  - 01 Projekt: *Übersicht* (Projekt verwalten, Ort finden, Lagekennzahlen) · *Stil* (Stilvorlagen, Gestaltung für alle Karten)
  - 02 Landkarte (`ov`), 03 Makrolage (`mi`), 04 Mikrolage (`mk`): je Karte aus der Vorlage `mapUI(kind)` erzeugt,
    gegliedert in *Übersicht* (Ausgabegröße, Maßstab, Markierung, Projektpunkt/-titel) · *Stil* (Gestaltung übernehmen,
    Schrift, Städte, Straßen/Bahn/Grenzen, Gewässer, Topographie, Landschaft) · *Mapping* (Fahrzeiten, Funktionen, POIs, freie Texte)
  - Nur die Gruppe der aktiven Karte ist sichtbar. Gemeinsame Abschnitte (`#sec_mark`, `#sec_funk`, `#sec_poi`, `#sec_note`)
    liegen in `#shared` und werden von `setTab` in die Platzhalter (`.slot[data-slot]`) der aktiven Karte gehängt.
  - Maßstäbe: Landkarte 1:500.000–1:10 Mio. (500.000er), Makrolage 1:25.000–1:100.000 (25.000er), Mikrolage 1:5.000–1:25.000 (5.000er)
- Einstellungen je Karte: `S.st[kind]` (Stil; wirksam über `ST(kind)`, das „Gestaltung übernehmen“ auflöst), `S.ppk[kind]` (Projektpunkt),
  `S.zone[kind]` (Fahrzeiten: mode drive/bike/walk), `S.mapIn[kind]` (Nutzungsmapping). Alte Schlüssel (S.walk, S.drive, S.hill …)
  dienen nur noch der einmaligen Übernahme.
- Ansichts-Zoom (`vzoom`): Mausrad vergrößert sofort per CSS (`previewZoom`), scharf neu gezeichnet nach 260 ms Ruhe (`commitZoom`);
  Knöpfe −/100 %/+ (`setZoom`); Leertaste + Ziehen verschiebt das Blatt. Maßstab bleibt fix.
- `relayout` arbeitet nur auf der aktiven Karte und setzt `v.relayouting`, damit Größenänderungen den gespeicherten Ausschnitt nicht überschreiben.
- Projekt-Sektion: „Sichern (Export)“ / „Einlesen (Import)“ – alle Projekte, Stilvorlagen, Einstellungen als JSON
- Letztes `<script>`: die eigentliche App-Logik (ca. 1.700 Zeilen)

## Wichtige Stellen im App-Script
- `DPI = { ov: 192, mi: 384, mk: 384 }` – interne Render-dpi (Makro/Mikro 384 → Zoom 14 mit Einzelgebäuden)
- `scaleOf(kind)`, `centerOf(kind)`, `KNAME` – Maßstab, Ausschnittsmitte und Name je Karte
- `PRESETS` – Ausgabeformate in cm, abgestimmt auf die GIEAG-Folienlayouts (A1, A2, B1–B3, K1 …)
- `store` / `S` / `saveS()` – Einstellungen; gespeichert im localStorage mit Präfix `gieag-lk-`
- `styleFor(kind, k)` / `styleBase` – Kartenstil (OpenFreeMap-Vektorkacheln)
- `drawOverlay`, `drawSettlements`, `drawZones`, `drawPois`, `drawNotes`, `scaleBar` – Canvas-Zeichnungen über der Karte
- `computeKpi`, `matrix` – Lagekennzahlen (Entfernungen/Fahrzeiten)
- `fetchIso`, `isoWait` – Erreichbarkeitszonen
- `overpassQ`, `loadMapping`, `loadCities` – OSM-Daten
- `exportPng(kind)` – PNG-Export: rendert die Karte unsichtbar in Druckauflösung neu, zeichnet Overlays darüber,
  Dateiname automatisch (`…_Lageplan_M25000_…cm_300dpi.png`); fehlende Kacheln → nach 60 s wird exportiert, was da ist

## Externe Dienste (alle ohne API-Key)
- Kacheln: https://tiles.openfreemap.org/planet
- Ortssuche: Nominatim (nominatim.openstreetmap.org)
- POIs/Städte/Mapping: Overpass-API mit Ausweichservern (overpass-api.de, kumi.systems, private.coffee, mail.ru)
- Routing/Isochronen/Matrix: Valhalla (valhalla1.openstreetmap.de)
- Gelände: AWS Terrarium-Höhenkacheln

## Gestaltung
GIEAG-Akzentfarbe #255AA8. Haltung: schlicht, wenig Text, präzise – die Karten landen in Präsentationen.

## Beim Ändern beachten
- Gespeicherte Projekte und Vorlagen der Nutzer nicht brechen: neue Einstellungen mit Standardwert ergänzen,
  bestehende localStorage-Schlüssel nicht umbenennen.
- Nach einer Änderung kurz prüfen, dass das Script fehlerfrei bleibt (z. B. `node --check` auf den extrahierten Script-Block).
