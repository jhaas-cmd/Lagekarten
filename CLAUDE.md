# ATLAS (vormals GIEAG Lagekarten) – Projektnotiz für Claude Code

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
- Export-Dialog (`#expDlg`): alle drei Karten vorgewählt, dpi, transparent, Dateinamen-Vorschau; mehrere Karten als ZIP (`#expZip`, `makeZip` ohne Kompression, `saveBlob`, `zipName`); `exportPng(kind, collect)` sammelt Blobs statt Download. PDF/SVG noch nicht gebaut (ausgeblendet).
- Reiterleiste: Format/Maßstab der aktiven Karte (`syncBar`), „⌖ Projekt“ (`centerBtn`, zentriert die aktive Karte), Rückgängig/Wiederholen, Zoom; Tasten 1/2/3, 0, +/−, Strg+Z/Y.
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
- Vegetation (`veg` + `wood`, `park`, `green` (Gärten, Bayern-CIR, sonst Wohngebiets-Tönung `garden`), `field`, `crowns`): Stimmungen `VEG_PRESETS` (baeume, halbton, flaeche, schwarzplan); Bäume ohne Stamm/Kontur mit Dichte `crowns.dens`, Größe `crowns.size`, Varianz `crowns.vari`, Bündeln zu Baumgruppen `crowns.grp` (`groupTrees`: Zufallsfeld ~75 m, nur in größeren Grünflächen); Landwirtschaft folgt öffentlichem Grün (`field.link`); Kronendach im Wald `crowns.forest` (`woodPolys`, ortsfestes Raster ~5 m), Tonvariation je Krone; Palette mit Sand · Braun; Farbpalette `PALROWS` (Blau, Grün, Signal) + Grau;
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

## Bedienung und Kennzahlen (Überarbeitung Nov. 2026)
- Projektzeile oben (`#projLine`, `syncProjLine`, `foldProject`): 01 Projekt klappt beim Kartenwechsel zu. Geführter Start (`#startCard`, `showStart`).
- Klick-Modi mit Leiste und Esc (`setMode`, `modeBar`, `endModes`); Rechtsklick-Menü (`openCtx`/`closeCtx`); Hilfe `#helpDlg` (Taste ?); `status()` blendet nach 7 s aus.
- Hintergrund-Aktivität oben rechts (`BUSY`, `paintBusy`, `track(label, fn)` um die Lade-/Rechenfunktionen); `paintBusy` aktualisiert auch die Berechnungsliste.
- Vorlagen: GIEAG-Vorlagen je Zielgruppe (`FAMS`, `FAM_VER`, `ensureFamilies`, Presets `gieag_<fam>_<kind>`, `fixed:true`), Schutz per `guardFixed` (Kopie vor erster Änderung), „Speichern unter …“, „Für alle Karten übernehmen“. Inaktive Ebenen: `LAYERS[].inact`.
- Gemeinsame Gestaltung `#sec_glob` hängt oben im Stil-Reiter jeder Karte.
- 01 Projekt → „Lagekennzahlen · Berechnungen“ (`#calcList`, `renderCalc`, `#calcAll`): Entfernungen/Fahrzeiten (`computeKpi`, Ort in `P.kpiAt`), Zensus im Radius, Stadtvergleich, Regionalatlas, Verkehr (optional); Status ✓ / veraltet / läuft.
- 05 Kennzahlen: rechnet beim Öffnen automatisch (`kzStale`, `runKz`); Spalten Radius | Stadt | Deutschland | Einschätzung.
  Stadt = Gemeindegrenze aus Overpass (`cityArea`: admin_level 8, sonst 6; gerade/ungerade-Regel je 100-m-Rasterzeile), Auswertung `zSum(bb, test, km2)` (allgemeine Form von `zAgg`), Ergebnis `P.kz.city = {name, kind, s, at}` bzw. `{err}`; `loadCity`.
  Bewertung: `KZPOL` (Richtung und Gewicht je Assetklasse), `devOf`, `evCell`, Lageindex `kzScore` (Stadt = 100; Regionalatlaswerte gegen Land), Kernwerte `KZKEY`. Nicht verfügbare Kennzahlen eingeklappt (`S.kz.showExt`).
  Radius in Makro-/Mikrolage per `S.kz.showR` (in `drawOverlay`, auch im Export).

## ATLAS (Nov. 2026)
- Name ATLAS, Untertitel „axperon site information“, Logo nach Julius' Skizze, ausgearbeitet: Kreis (1,5) mit kräftigem A (Schenkel 3, Winkel 210°/150°, am Kreis beschnitten, Spitze an der Kreislinie) und oranger Diagonale vom rechten Fußpunkt (Kreis bei 150°) zur Mitte des linken Schenkels – Pfeil im Kreis, als A lesbar, SVG inline in `.brand`; dieselbe Geometrie als Nordpfeil-Typ `atlas` (`drawAtlasMark`, Standard in `stDef`, `FAM_VER = 5`) und in der Dossier-Karte. Farben: Dunkelblau #14284B, Kontrast Orange #F0642D (keine Pinktöne). Schrift Archivo (Wortmarke/Überschriften, 800/900), sonst Inter. Backup-Kennung `app: 'gieag-lagekarten'` bleibt (Kompatibilität).
- Zentrieren-Knopf `#centerBtn` nur Fadenkreuz; `.zoom button` einheitlich 34 px hoch.
- Ladezeiten: `overpassQ` = Zwischenspeicher (20 min) + Zusammenlegen gleicher Anfragen + `overpassRace` (Server gestaffelt parallel, 2,5 s Versatz, schnellster zuerst, `ovBest`);
  `relayout` setzt den Stil nur neu, wenn sich `JSON.stringify(styleFor(...))` geändert hat (`v.sig`); Preconnect zu Kacheln/Overpass/Valhalla.
- `computeKpi`: Flughäfen nur aus Liste `AIRPORTS` (Verkehrsflughäfen, Drehkreuze markiert → Ziel `fhx`), Messen aus `MESSEN`; strukturiert in `P.kpiList` ({key,label,km,min,mode,luft}), Ort in `P.kpiAt`.
- Infrastruktur im Umgriff (`INFRA`, `loadInfra`, Ergebnis `P.kz.infra.items[id] = {n, d, nm}`): Lebensmittelmärkte, Einzelhandel gesamt (nur Anzahl), Ärzte, Apotheken, Kitas, Schulen, U-/Stadtbahn (nur städtisch, `urban`), S-Bahn/Bahnhalte. Eine Overpass-Abfrage mit `out count` als Trenner, zweite Abfrage im weiten Umkreis für fehlende.
- Kennzahlen-Gruppen `infra` und `anb` (Verkehrsanbindung aus `P.kpiList`), Bewertung nach Entfernung (`distEv`, Schwellen in `INFRA`/`ANB`, Gewichte je Assetklasse, ÖPNV über `ADW`), fließt in `kzScore`.
- Dossier: Kopf mit Logo (`.dhead`), Kartenausschnitt Mikrolage mit Radius (`mapShot`, `SHOT`, `shotPlan`: Maßstab so, dass der Radius passt), „Dossier drucken / als PDF“ (`#kzPrint`, `#printArea`, Druck-CSS A4).
- Dossier im Stil der GIEAG-Teaser (Hochformat): Kicker-Zeile, Logo rechts, große Versal-Überschrift „Standort / <Assetklasse in Orange> / <Stadt>“, Kernwerte mit Linie, Karte, Lageindex, Tabellen mit Gruppennamen im Tabellenkopf (`th.g`) und Quelle darunter (`.tsrc`); Bewertung als Ampel (Pillen `.ev.pos/.mid/.neg` = grün/gelb/rot, grau neutral); Orange nur als Markenakzent (Überschrift, Projektpunkt). Weiche Flächen (Kernwerte-Karten, Lageindex-Feld). Kurzbezeichnungen `SHORT`/`short()` und `KZGS` gegen Zeilenumbrüche; Kernwerte mit Ersatzliste `KEYFILL`.
- Dossier-Karte: Grundkarte einmal gerendert (`renderBase`, `BASE`, Vorlage `gieag_atlas_mk`, zusätzlich Graustufenfilter), darüber `composeShot` (Radius + halber Radius, Einrichtungen aus `infra.items[id].pts`, Projektpunkt orange, Legende, Maßstab, Nordpfeil); `dosProj` = Mercator ohne Karte.
- Neue GIEAG-Vorlage `atlas` („ATLAS · Graustufen“, Vegetation `grau` mit Schraffuren), `FAM_VER = 4`.
- Gastronomie (`gastro`, Wohnen/Büro) und Hotels (`hotel`, Büro) in `INFRA`; `infraStale()` erkennt alte Ergebnisse ohne neue Kategorien.
- Große Arbeitgeber (`loadEmployers`, Gruppe `arbg`, `P.kz.emp`): Wikidata-SPARQL (`wikibase:around`, P625 + P1128 ≥ 500) im Umkreis 10 km; Beschäftigte = Unternehmen gesamt, nur Organisationen mit eigener Koordinate.
- Projekteinstieg (Assistent `#startCard.wiz`, `showStart`, `WZ`, `wzShow`, `wzPlan`, `wzSummary`, `wzFinish`): 1 Ort (Nominatim, Titel aus Straße) · 2 Nutzung · 3 Zweck (Expo/Steckbrief/Dossier) + Kartenstil · 4 Zusammenfassung, optional „Alles berechnen“.
  Vorgaben zentral in `START_DEF` (Radius je Nutzung Stadt/Land, Vorlage je Nutzung, Maßstäbe, Formate je Zweck); Stadt/Land über `isUrban()` (Großstadt ≥ 100.000 EW in 8 bzw. 14 km). Nutzung/Zweck je Projekt in `P.asset`/`P.use`.
- Dossierkopf: ASSETKLASSE (orange) / PROJEKTTITEL / Straße (kleiner, `.hs2`, entfällt wenn gleich dem Titel); rechts Anschrift (fett), Stadtteil · Stadt, Hinweistext. Anschrift aus `P.addr` (`addrOf`, Nominatim mit addressdetails), sonst `addrLines()` aus `P.place`.
- Vorlagen nach Julius' Beispielkarten (`FAM_VER = 6`): `kontrast` (Dunkelblau/Orange), `gelb` (Dunkelblau/Gelb), `signal` (Grau + Signal, Wasser schwarz), `akzent` (Schwarzplan · Akzent), `pastell` (Vegetation `pastell`), `landschaft` (Vegetation `landschaft`). Keine Papierstruktur, keine Lage-Kaskade (abgelehnt).
- Signalfarbe je Vorlage `st.hi` (Projektpunkt, Baufeld, markierte Gebäude, Radius, solange keine eigene Farbe gesetzt; sonst `S.accent`).
- Gewässer: Schatten nach innen `water.inner` (0–80) in `drawWaterShadow` (Wassermaske aus `querySourceFeatures`, Land versetzt + weichgezeichnet, nur im Wasser; im Overlay, auch im Export). Gebäude: feine Kontur `bldg.line`/`bldg.lineCol`.
- Kartenstil unter 01 Projekt (`#famGrid`, `renderFamGrid`): Kacheln je sichtbarer GIEAG-Vorlage, setzt alle drei Karten. Ältere Vorlagen (`atlas`, `schwarz`, `investor`, `buero`, `wohnen`) mit `hide: true` ausgeblendet (bleiben erhalten, `gieag_atlas_mk` weiter für die Dossier-Karte). `FAM_VER = 7`. Assistent empfiehlt: Wohnen → pastell, Büro → kontrast, Light/Logistik → signal.
- Landschaft auf der Landkarte: keine Grünflächen, dafür Höhenstufen grün → ocker → braun (`hypso.ramp: 'gruenbraun'`, `HYPSO_GB`) und warme Schummerung (`hill.tone: 'braun'`).
- Ebenen neu gegliedert (`GRP`): Kartendarstellung (inkl. Luftbild) · Verkehr · Stadt (Orte, Stadtteile, Siedlung, Gebäude) · Landschaft (Gewässer, Vegetation) · Schummerung und Gelände (Schummerung, Höhenlinien); Gruppen einklappbar (`.lgrp`/`.lgb`, `LGC`, store `lgClosed`).
- Höhenstufen entfallen (kein Zeichnen, keine Ebene; `hypso`-Werte bleiben nur als Altbestand). Schummerung mit Farbton `hill.tone` grau/braun/grün (`HTONE`).
- Städte-/Ortsnamen je Kategorie (`ct.big/mid/small`: col, w, caps; Größen weiter in `ts`), leere Farbe = aus Schriftfarbe abgeleitet; `tierRows`.
- Stadtteile (`dist`, `drawDistricts`): place suburb/quarter/borough aus den Kacheln, nur nahe Großstädten ≥ 100.000 EW, Makro/Mikro ab 1:50.000.
- Straßennamen: Hintergrund als Rechteck (`box`), zu lange Namen zuerst bis 70 % kleiner (`fit`, `fontAt`), dann zweizeilig an Leerzeichen/Bindestrich, sonst weggelassen. `FAM_VER = 8`.
- Namen zentral: Ebene „Städtenamen“ (Stadt, `names`; ersetzt Ortsnamen- und Stadtteil-Zeile) mit Kategorien Groß-/Mittel-/Kleinstadt (`ct.*.on`, Stil) und Stadtteile (`dist`); Ebene „Straßennamen“ (Verkehr, `rn`): Schilder Autobahn (`rn.mwRef`) und Bundesstraße (`rn.bRef`) mit Größe/Schildfarbe in allen Karten, Straßennamen (`road.lbl*`, Makro/Mikro).
- Hintergrund hinter Namen (`bgRow`): an/aus, Farbe, Deckung voll/50 % (`names.bg/bgCol/bgA`, `nameBg`; Straßen `road.lblBg/lblBgCol` + `rn.bgA`). `FAM_VER = 9`.
- Regionalatlas: Sonderwerte (|v| ≥ 1e7, z. B. 5555555555) werden übersprungen. Neue Kennzahl „Wohnfläche je Haushalt“ (Zensus s × h, abgeleitet).
- Bodenrichtwert: manueller Eintrag in 05 Kennzahlen (`P.brw` = {v, d, art, src}, Felder `#brwV/#brwD/#brwA`, „BORIS öffnen“ → bodenrichtwerte-boris.de). Kein automatischer Abruf: BORIS-BW-Endpunkt nicht bekannt (Nutzungsbedingungen: keine kommerzielle Nutzung), Bayern meist kostenpflichtig (WMS geoservices.bayern.de/wms/v1/ogc_bodenrichtwerte.cgi ungeprüft).
- Auswahl und Schrift getrennt: „Städte“ (`cities`, Landkarte/Makro: Schwellenwert, welche Kategorien `ct.*.on`, Stadtteile `dist.on`; Mikro: Zeile „Stadtteile“ `distsel`) wählt, „Städtenamen“ (`names`) nur Schrift + Hintergrund. Straßen: Autobahnen „Nummern zeigen“ (`rn.mwRef.on`), Haupt-/Nebenstraßen „Nummern“ (`rn.bRef.on`) + „Straßennamen zeigen“ (`road.lbl`), Wohnstraßen „Straßennamen zeigen“ (`rn.minor`); „Straßennamen“ (`rnames`) nur Schrift, Schilder, Hintergrund. `FAM_VER = 10`.
- Kartendarstellung: Ebenen „Projekttitel“ (`ptitle.on`, zusätzlich zu S.ovTitle/miTitle/mkTitle) und „Projektpunkt“ (`ppoint.on`). Gewässer: „Seen und Weiher beschriften“ (`water.lake`, `drawLakeNames` aus water_name, Schrift wie Flussnamen).
- Assetklasse `fue` (Forschung & Entwicklung): INFRA-Listenkategorien `uni` (Hochschulen) und `forsch` (Forschungseinrichtungen) mit `list` (je Name nur nächster Eintrag, `items[id].list`), Gruppe `wiss` (`thW`), Gewichte in KZPOL/ANB/ADW, `START_DEF` (Radius 3/5 km, Vorlage kontrast), Assistent-Kachel. `FAM_VER = 11`.
- Dossier-Karte: Einrichtungen als Kreise (statt Quadrate), auch in der Legende. Bodenrichtwert auch als Freitext (`P.brw.t`, Feld `#brwT`, Knopf `#brwNA` „nicht frei verfügbar – muss eingeholt werden“); ohne Zahl erscheint der Text in Tabelle, Dossier und Kopiertext.
