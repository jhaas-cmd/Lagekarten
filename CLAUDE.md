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
    Stadt und Landschaft – Orte, Siedlung, Gebäude (Schatten), Gewässer (Flussnamen), Wald, Wiesen & Felder, Grün aus Luftbild, Luftbild · Topographie – Schummerung, Höhenlinien, Höhenstufen)
    · *Mapping* (Fahrzeiten, Funktionen, Hervorheben, POIs, freie Texte).
    Hervorheben (`#sec_hl`, `P.hl`, `drawHl`, `pickHl`, `loadLine`): Klick wählt Straße (ganze Straße gleichen Namens, zusammenhängend, per Overpass),
    Gleis (Auswahl der dort fahrenden Linien → Linienverlauf aus Route-Relationen) oder Gebäude (Kachelgeometrie); Bahnlinie auch per Name (z. B. S7) im Ausschnitt.
    Je Element Farbe, Strich, Deckkraft, weißer Rand, gestrichelt, Beschriftung als Schild/Text (verschiebbar), Sichtbarkeit je Karte. Bäume sind vorerst ausgeblendet (OSM-Daten zu lückenhaft).
  - Abschnitte als Akkordeon (nur einer offen je Bereich); statische Hinweise hinter (i)
  - Nur die Gruppe der aktiven Karte ist sichtbar. Gemeinsame Abschnitte (`#sec_mark`, `#sec_funk`, `#sec_poi`, `#sec_note`)
    (+ `#sec_hl`) liegen in `#shared` und werden von `setTab` in die Platzhalter (`.slot[data-slot]`) der aktiven Karte gehängt.
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
- Luftbild (`st.photo`, `photoLayers` in `styleFor`): Rasterebene unter allem; Quelle auto = amtliches DOP20 des Bundeslands (`DOP.BY`/`DOP.BW`, WMS mit {bbox-epsg-3857}),
  sonst Sentinel-2 cloudless 2016 (`SAT`); Bundesland per Nominatim-Reverse in `P.region`/`P.regionAt`; Ebenennamen aus GetCapabilities in `store 'photoL'`.
  Grün aus Luftbild (`st.green`, `ensureGreen`, `greenMask`, `drawGreen` in `drawBase`): Vegetationsindex aus Bayern-CIR, Maske unter der Karte; Export lädt Maske in Druckauflösung (`GREEN_EXP`). Quellenvermerk über `photoLic`.
- Projekt-Sektion „Luftbild & Satellit · Test“ (`SRC_TESTS`, `testSource`): prüft im Browser Bayern DOP20 (RGB/CIR), BW DOP20, ESA WorldCover, Sentinel-2 cloudless 2016 auf Erreichbarkeit und Export-Freigabe (CORS). Vorstufe für eine Ebene „Luftbild“ und „Grün aus Infrarot“.
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

## Stand Etappe 1 (umgesetzt)
- Luftbild unter Kartendarstellung. Straßen: `mw` Autobahnen · `road` Haupt-/Nebenstraßen (sec/pri) · `minor` Wohn-/Anliegerstraßen (min; Migration aus road).
- Vegetation (`veg` + `wood`, `park`, `green` (Gärten, Bayern-CIR, sonst Wohngebiets-Tönung `garden`), `field`, `crowns`): Stimmungen `VEG_PRESETS` (baeume, halbton, flaeche, schwarzplan); Bäume ohne Stamm/Kontur mit Dichte `crowns.dens`, Größe `crowns.size`, Varianz `crowns.vari`, Bündeln zu Baumgruppen `crowns.grp` (`groupTrees`: Zufallsfeld ~75 m, nur in größeren Grünflächen); Kronendach im Wald `crowns.forest` (`woodPolys`, ortsfestes Raster ~5 m), Tonvariation je Krone; Palette mit Sand · Braun; Farbpalette `PALROWS` (Blau, Grün, Signal) + Grau;
  Halbtonmuster `half-s/m/l`; Baumkronen `drawCrowns` aus CIR (`findCrowns`, experimentell) oder OSM (`loadTrees`).
- Hervorheben und POIs je Karte (`inK`, `hidK`, `takeOver`, `dropK`): Liste zeigt nur Elemente der aktiven Karte; „Aus anderen Karten übernehmen“.

## Etappen 2–4 (umgesetzt)
- Reiter **05 Kennzahlen** (`kzOn`, `showKz`, Gruppe `data-tab="kz"`, Panel `#kzRep`; nicht Teil von `KINDS`, die zuletzt aktive Karte bleibt `active`):
  Zensus-Kacheln `daten/zensus/{tx}_{ty}.json` (EPSG:3035, 10-km-Kacheln, Spalten siehe LIESMICH), `index.json`, `de.json` (Bundeswerte);
  `laea()` (ETRS89-LAEA), `zTile`, `zAgg` (Radius, gewichtete Mittel), Definitionen `KZK`/`KZG`/`KZORDER` je Assetklasse (wohnen/buero/light/logistik),
  Ergebnis in `P.kz` (res, umland 15 km, r25, ra, traffic), Text kopieren, PNG-Kachel. Einstellungen `S.kz`.
- Regionalatlas (`RA_URL`, `RA_IND`, `raQuery`, `loadRA`): Einkommen (Kreis), Einkünfte/Steuerpflichtige, Fertigstellungen, Bevölkerungsentwicklung (Gemeinde), Arbeitslosenquote, Arbeitsplatzdichte (Kreis); Landeswert zum Vergleich.
- Verkehr auf Knopfdruck (`loadTraffic`): Bayern über BAYSIS ArcGIS REST (DTV-Zählstellen im Umkreis); BW nur Hinweis (Verkehrsmonitoring als PDF).
- **Zensus-Raster als Kartenebene** (Mapping, `#sec_zg`, `S.zg[kind]`, `ensureZg`, `drawZg` in `drawBase`, `zgLegend`): 10 Merkmale (`ZATTR`), Halbtonraster/Farbstufen, 5 Quantilstufen, Legende oben links.
- Nicht frei verfügbar / offen: Pendler (BA), Baulandpreise, Bodenrichtwerte als Dienst (BW nur Portal, Bayern kostenpflichtig), Kaufkraft (GfK). CORS der externen Dienste im Browser von Julius prüfen.
