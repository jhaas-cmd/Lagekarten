#!/usr/bin/env python3
"""INKAR-Tabellenexport (Kreise, breit: Zeile 1 Indikatoren, Zeile 2 Jahre) -> daten/inkar/kreise.json,
daten/inkar/meta.json und daten/mieten/bbsr_angebotsmieten.json.

Aufruf (aus dem Repo-Stamm): python3 tools/inkar_kreise.py <export1.csv> [<export2.csv> ...]
Mehrere Exporte werden zusammengeführt; kommt ein Indikator mehrfach (mehrere Jahre) vor,
wird das jüngste Jahr als Wert genommen und die Reihe als Zeitreihe gespeichert."""
import csv, json, sys, os, datetime

# Auswahl für ATLAS: INKAR-Name -> (Kennung, Einheit, Nachkommastellen)
SEL = {
    'Baulandpreise': ('baul', '€/m²', 0),
    'Baugenehmigungen für Wohnungenje Einwohner': ('bgen', 'je 1.000 EW', 1),
    'Prognostizierte Bevölkerungsentwicklung (2022-2030)': ('prog30', '%', 1),
    'Prognostizierte Bevölkerungsentwicklung (2022-2045)': ('prog45', '%', 1),
    'Bevölkerungsentwicklung (10 Jahre)': ('bev10', '%', 1),
    'Gesamtwanderungssaldo': ('wans', 'je 1.000 EW', 1),
    'Einpersonenhaushalte': ('ein1', '%', 1),
    'Durchschnittsalter der Bevölkerung': ('alt', 'Jahre', 1),
    'Kaufkraft': ('kauf', '€ je EW', 0),
    'Einzelhandelsrelevante Kaufkraft': ('ekk', '€ je EW', 0),
    'Medianeinkommen': ('med', '€', 0),
    'Medianeinkommen akademischer Berufsabschluss': ('medak', '€', 0),
    'Monatliches Haushaltseinkommen': ('hhek', '€', 0),
    'Haushalte mit hohem Einkommen': ('hhhoch', '%', 1),
    'Bruttoverdienst im Produzierenden Gewerbe': ('bvpg', '€', 0),
    'Gewerbesteuer': ('gewst', '€ je EW', 0),
    'Studierende': ('stud', 'je 1.000 EW', 1),
    'Angebotsmietpreise': ('amiete', '€/m²', 2),
}
ZERO_IS_MISSING = {'baul', 'amiete', 'kauf', 'med', 'medak', 'hhek'}

def num(x):
    x = (x or '').strip()
    if not x or x in ('-', '.', '–'): return None
    try: return float(x.replace('.', '').replace(',', '.'))
    except ValueError: return None

ind, names, vals = {}, {}, {}          # ind[id] = {n,u,d,j,years}; vals[id][ags] = {jahr: wert}
for path in sys.argv[1:]:
    R = list(csv.reader(open(path, encoding='utf-8-sig'), delimiter=';'))
    head, years = R[0], R[1]
    for r in R[2:]:
        if len(r) < 4 or r[2].strip() != 'Kreise': continue
        ags = r[0].strip().zfill(5)[:5]; names[ags] = r[1].strip()
        for j in range(3, min(len(head), len(r))):
            s = SEL.get(head[j].strip())
            if not s: continue
            i, u, d = s; y = int(years[j]) if years[j].strip().isdigit() else 0; v = num(r[j])
            if v is None or (v == 0 and i in ZERO_IS_MISSING): continue
            ind.setdefault(i, {'n': head[j].strip(), 'u': u, 'd': d, 'years': set()})['years'].add(y)
            vals.setdefault(i, {}).setdefault(ags, {})[y] = v

out = {'quelle': 'INKAR, BBSR Bonn (dl-de/by-2-0)', 'abruf': datetime.date.today().isoformat(), 'ind': {}, 'n': names, 'v': {}}
for i, m in ind.items():
    ys = sorted(m['years']); out['ind'][i] = {'n': m['n'], 'u': m['u'], 'd': m['d'], 'j': ys[-1], 'jahre': ys}
    out['v'][i] = {a: ({str(y): w for y, w in s.items()} if len(ys) > 1 else s[max(s)]) for a, s in vals[i].items()}
os.makedirs('daten/inkar', exist_ok=True); os.makedirs('daten/mieten', exist_ok=True)
json.dump(out, open('daten/inkar/kreise.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump({'abruf': out['abruf'], 'datenjahre': sorted({y for m in ind.values() for y in m['years']}), 'indikatoren': len(ind)},
          open('daten/inkar/meta.json', 'w'), ensure_ascii=False, indent=1)
if 'amiete' in vals:
    am = vals['amiete']; j = max(ind['amiete']['years'])
    json.dump({'quelle': 'BBSR-Wohnungsmarktbeobachtung, IDN ImmoDaten GmbH (über INKAR)',
               'def': 'Angebotsmieten (Erst- und Wiedervermietung) inserierter Wohnungen, nettokalt, €/m², Kreisebene',
               'stand': j, 'de': None,
               'kreise': {a: {'n': names[a], 'v': s[max(s)], 'j': max(s), 'reihe': ({str(y): w for y, w in sorted(s.items())} if len(s) > 1 else None)} for a, s in am.items()}},
              open('daten/mieten/bbsr_angebotsmieten.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(names), 'Kreise;', ', '.join(f"{i} {m['j']}" for i, m in out['ind'].items()))
