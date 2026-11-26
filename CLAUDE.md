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
  - Seitenleiste per Ziehgriff (`#resizer`) 260–560 px breit, gespeichert unter `sidebarW`
  - 01 Projekt: *Übersicht* (Projekt verwalten mit automatischem Speichern, Ort finden, Lagekennzahlen) · *Stil* (Gestaltung für alle Karten)
  - 02 Landkarte (`ov`), 03 Makrolage (`mi`), 04 Mikrolage (`mk`): je Karte aus der Vorlage `mapUI(kind)` erzeugt,
    mit Unterreitern (Registerlaschen-Optik) *Übersicht* (Ausgabegröße, Maßstab, Markierung, Projektpunkt/-titel) ·
    *Stil* (Preset + kompakte Ebenenliste `LAYERS` + Attribut-Board `.inspector` mit `boardOf()`: je Ebene immer Farbe/Deckkraft · Strich · Darstellung · Beschriftung;
    gegliedert nach `GRP`: Kartendarstellung – Schrift, Fokus, Nordpfeil (Typen kreis/pfeil/nadel/kompass), Maßstabsleiste, Raster, Grenzen ·
    Verkehr – Autobahnen, Straßen (Darstellung Linie/Fläche/Kontur/beides, Straßennamen mit eigener Schrift), Bahn ·
    Stadt und Landschaft – Orte, Siedlung, Gebäude (Schatten), Gewässer (Flussnamen), Wald, Wiesen & Felder · Topographie – Schummerung, Höhenlinien, Höhenstufen)
    · *Mapping* (Fahrzeiten, Funktionen, POIs, freie Texte). Bäume sind vorerst ausgeblendet (OSM-Daten zu lückenhaft).
  - Abschnitte als Akkordeon (nur einer offen je Bereich); statische Hinweise hinter (i)
  - Nur die Gruppe der aktiven Karte ist sichtbar. Gemeinsame Abschnitte (`#sec_mark`, `#sec_funk`, `#sec_poi`, `#sec_note`)
    liegen in `#shared` und werden von `setTab` in die Platzhalter (`.slot[data-slot]`) der aktiven Karte gehängt.
  - Maßstäbe: Landkarte 1:500.000–1:10 Mio. (500.000er), Makrolage 1:25.000–1:100.000 (25.000er), Mikrolage 1:5.000–1:25.000 (5.000er)
- Kartenebenen außerhalb des Vektorstils (Overlay-Canvas bzw. Grundfläche `${kind}Sc` unter der Karte):
  `drawBase` (Weiß, Höhenstufen, Siedlungsflächen der Landkarte), `drawContours`/`drawHypso` aus `DEMS` (Terrarium-Kacheln, `ensureDem`),
  `drawGrid` (Meterraster und Blattraster achsparallel zur Blattkante, Gradnetz), `drawCities` (Landkarte: CITIES; Makrolage: `PLACES` per Overpass, ab 500 EW), `drawTrees` (`TREES`, Mikrolage ≤ 1:15.000),
  `drawLineLabels` (Fluss-/Straßennamen), `drawRoadRefs`, `drawStations`. Fokus: im Preset (`st.focus`), Vorschau per CSS (`.focus`), Export per Canvas-Filter.
- Webschriften (Inter, Source Sans 3, IBM Plex Sans) über Google Fonts; `loadFonts()` vor dem Zeichnen/Export. Strichstärken in Stufen `WSTEPS`.
- Presets: `S.presets[id] = { name, base, st }`, `S.use[kind]` = Preset der Karte; `ST(kind)` liefert den wirksamen Stil.
  Änderungen in der Ebenenliste wirken in allen Karten mit demselben Preset. (`S.st` nur noch Altbestand.)
- Weitere Einstellungen je Karte: `S.ppk[kind]` (Projektpunkt),
  `S.zone[kind]` (Fahrzeiten: mode drive/bike/walk), `S.mapIn[kind]` (Nutzungsmapping). Alte Schlüssel (S.walk, S.drive, S.hill …)
  dienen nur noch der einmaligen Übernahme.
- Ansichts-Zoom (`vzoom`): Mausrad vergrößert sofort per CSS (`previewZoom`), scharf neu gezeichnet nach 260 ms Ruhe (`commitZoom`);
  Knöpfe −/100 %/+ (`setZoom`); Leertaste + Ziehen verschiebt das Blatt. Maßstab bleibt fix.
- `relayout` arbeitet nur auf der aktiven Karte und setzt `v.relayouting`, damit Größenänderungen den gespeicherten Ausschnitt nicht überschreiben.
- Rückgängig/Wiederholen (`hist`, `snap`, `undo`, `redo`): Momentaufnahmen von `{S, P}` nach jeder Änderung (`saveS`, `repaint`);
  `syncAllUI()` setzt danach alle Bedienelemente neu. `snap` speichert das Projekt zugleich automatisch (`autosave`).
- Export-Dialog (`#expDlg`): Karten wählen, dpi, transparent, Dateinamen-Vorschau; PDF/SVG vorgesehen, noch nicht gebaut.
- Reiterleiste: Format/Maßstab der aktiven Karte (`syncBar`), Rückgängig/Wiederholen, Zoom; Tasten 1/2/3, 0, +/−, Strg+Z/Y.
- Projekt-Sektion: „Sichern (Export)“ / „Einlesen (Import)“ – alle Projekte, Presets, Einstellungen als JSON
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
