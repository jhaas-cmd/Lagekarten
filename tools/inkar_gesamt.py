#!/usr/bin/env python3
"""INKAR-Gesamtdatenbank (lange Form: Bereich;ID;Kuerzel;Indikator;Raumbezug;Kennziffer;Name;Zeitbezug;Wert)
-> daten/inkar/kreise.json, daten/inkar/gemeinden/<LL>.json, daten/inkar/meta.json, daten/mieten/bbsr_angebotsmieten.json

Aufruf (aus dem Repo-Stamm): python3 tools/inkar_gesamt.py <INKAR_Auswahl.csv[.gz]>
Die Datei darf gepackt (.gz) sein. Zeitreihen werden mitgenommen (Kreise ab 2005, Gemeinden ab 2013).
Vergleichswerte Land und Bund kommen direkt aus INKAR (Raumbezug „Bundesländer“ / „Bund“)."""
import gzip, json, sys, os, datetime, collections

# Kürzel -> (Kennung in ATLAS, Einheit, Nachkommastellen, auch Gemeinde)
SEL = {
    'm_mietpr': ('amiete', '€/m²', 2, False),
    'd_KW_BL': ('baul', '€/m²', 0, False),
    'q_kaufkraft': ('kauf', '€ je EW', 0, True),
    'q_einzelhandelskaufkraft': ('ekk', '€ je EW', 0, True),
    'm_ek': ('med', '€', 0, False),
    'm_ek_akad': ('medak', '€', 0, False),
    'd_Hausshaltseinkommen': ('hhek', '€', 0, False),
    'a_hheink_hoch': ('hhhoch', '%', 1, True),
    'd_Bruttoverdienst_Prod': ('bvpg', '€', 0, False),
    'q_einkst_bev': ('einkst', '€ je EW', 0, True),
    'q_gewst_bev': ('gewst', '€ je EW', 0, True),
    'q_gest_bev': ('stkraft', '€ je EW', 0, True),
    'q_bip_ew': ('bipew', 'Tsd. € je EW', 1, False),
    'q_bip_et': ('bipet', 'Tsd. € je Erwerbst.', 1, False),
    'q_gen_wo_ew': ('bgen', 'je 1.000 EW', 1, True),
    'q_fert_wo_bev': ('fert', 'je 1.000 EW', 1, True),
    'q_fert_wo3um_bev': ('fertmfh', 'je 1.000 EW', 1, True),
    'e_bev2230_rop45': ('prog30', '%', 1, False),
    'e_bev2245_rop45': ('prog45', '%', 1, False),
    'xbev': ('bev', 'EW', 0, True),
    'e10_bev': ('bev10', '%', 1, True),
    'i_wans': ('wans', 'je 1.000 EW', 1, True),
    'q_bev_fl': ('dichte', 'EW/km²', 0, True),
    'm_bev_alter': ('alt', 'Jahre', 1, True),
    'q_HH1': ('ein1', '%', 1, True),
    'q_HH': ('hhgr', 'Personen', 2, True),
    'a_hh_kind': ('hhkind', '%', 1, True),
    'q_wofl_bev': ('wofl', 'm² je EW', 1, False),
    'q_pendlersaldo': ('pend', 'je 100 Besch.', 1, True),
    's_SvbAO_SvbWO': ('zentral', 'Verhältnis', 2, True),
    'sva': ('sva', 'Beschäftigte', 0, True),
    'q_sva_bev': ('svadi', 'je 1.000 EW', 0, True),
    'a_sva_akadem': ('akad', '%', 1, False),
    'a_svb_wissen': ('wissind', '%', 1, False),
    'a_svb_unternehmensdienstlstg': ('udl', '%', 1, False),
    'a_svb_IT': ('it', '%', 1, False),
    'a_bb_1000Mbits': ('gbit', '%', 1, True),
    'q_stud': ('stud', 'je 1.000 EW', 1, True),
    'q_übern_bev': ('uebern', 'je EW', 1, True),
}
ZERO_IS_MISSING = {'amiete', 'baul', 'kauf', 'ekk', 'med', 'medak', 'hhek', 'bvpg', 'dichte', 'alt', 'hhgr', 'bev', 'sva', 'zentral', 'svadi', 'bipew', 'bipet', 'wofl'}
Y_KRE, Y_GEM = 2005, 2013

def num(x):
    x = (x or '').strip()
    if not x or x in ('-', '.', '–'): return None
    try: return float(x.replace('.', '').replace(',', '.')) if ',' in x else float(x)
    except ValueError: return None

src = sys.argv[1]
f = gzip.open(src, 'rt', encoding='utf-8-sig') if src.endswith('.gz') else open(src, encoding='utf-8-sig')
next(f)
KR = collections.defaultdict(dict); GE = collections.defaultdict(dict); LA = collections.defaultdict(dict); BU = collections.defaultdict(dict)
nK, nG, title = {}, {}, {}
for line in f:
    c = line.rstrip('\n').split(';')
    if len(c) < 9: continue
    s = SEL.get(c[2])
    if not s: continue
    rb = c[4]
    if rb not in ('Kreise', 'Gemeinden', 'Bundesländer', 'Bund'): continue
    try: y = int(c[7])
    except ValueError: continue
    v = num(c[8]); i = s[0]
    if v is None or (v == 0 and i in ZERO_IS_MISSING): continue
    if i not in title or title[i].startswith('('): title[i] = c[3].split(') ', 1)[1] if c[3].startswith('(SDG') else c[3]
    k = c[5].strip()
    if rb == 'Kreise':
        if y < Y_KRE: continue
        a = k.zfill(8)[:5]; nK[a] = c[6]; KR[(i, a)][y] = v
    elif rb == 'Gemeinden':
        if not s[3] or y < Y_GEM: continue
        a = k.zfill(8); nG[a] = c[6]; GE[(i, a)][y] = v
    elif rb == 'Bundesländer':
        if y < Y_KRE: continue
        LA[(i, k.zfill(2)[:2])][y] = v
    else:
        if y < Y_KRE: continue
        BU[i][y] = v

def rnd(v, d): return round(v, d) if d else int(round(v))
def series(dct, d): return {str(y): rnd(w, d) for y, w in sorted(dct.items())}

meta = {k[0]: k for k in SEL.values()}
ind = {}
for (i, a), s in KR.items(): ind.setdefault(i, set()).update(s)
out = {'quelle': 'INKAR, BBSR Bonn (dl-de/by-2-0)', 'abruf': datetime.date.today().isoformat(), 'ind': {}, 'n': nK, 'v': {}, 'land': {}, 'de': {}}
gemInd = {}
for (i, a), s in GE.items(): gemInd.setdefault(i, set()).update(s)
for i in sorted(set(ind) | set(gemInd)):
    _, u, d, g = meta[i]; ys = sorted(ind.get(i, set()) | gemInd.get(i, set()))
    out['ind'][i] = {'n': title[i], 'u': u, 'd': d, 'j': ys[-1], 'jahre': ys, 'gem': i in gemInd}
for (i, a), s in KR.items(): out['v'].setdefault(i, {})[a] = series(s, meta[i][2])
for (i, l), s in LA.items(): out['land'].setdefault(i, {})[l] = series(s, meta[i][2])
for i, s in BU.items(): out['de'][i] = series(s, meta[i][2])
os.makedirs('daten/inkar/gemeinden', exist_ok=True); os.makedirs('daten/mieten', exist_ok=True)
json.dump(out, open('daten/inkar/kreise.json', 'w'), ensure_ascii=False, separators=(',', ':'))
byL = collections.defaultdict(lambda: {'n': {}, 'v': {}})
for (i, a), s in GE.items():
    L = byL[a[:2]]; L['n'][a] = nG[a]; L['v'].setdefault(i, {})[a] = series(s, meta[i][2])
for l, L in byL.items():
    json.dump({'quelle': out['quelle'], 'abruf': out['abruf'], 'land': l, **L}, open(f'daten/inkar/gemeinden/{l}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump({'abruf': out['abruf'], 'datenjahre': sorted({y for s in ind.values() for y in s}), 'indikatoren': len(out['ind']),
           'gemeinden': sorted(byL), 'jahrgang': max(out['ind'][i]['j'] for i in out['ind'] if i not in ('prog30', 'prog45'))},
          open('daten/inkar/meta.json', 'w'), ensure_ascii=False, indent=1)
am = {a: s for (i, a), s in KR.items() if i == 'amiete'}
if am:
    j = max(max(s) for s in am.values())
    de = BU.get('amiete'); de = de[max(de)] if de else None
    json.dump({'quelle': 'BBSR-Wohnungsmarktbeobachtung, IDN ImmoDaten GmbH (über INKAR)',
               'def': 'Angebotsmieten (Erst- und Wiedervermietung) inserierter Wohnungen, nettokalt, €/m², Kreisebene', 'stand': j, 'de': de,
               'kreise': {a: {'n': nK[a], 'v': s[max(s)], 'j': max(s), 'reihe': series(s, 2)} for a, s in am.items()}},
              open('daten/mieten/bbsr_angebotsmieten.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(nK), 'Kreise,', len(nG), 'Gemeinden,', len(out['ind']), 'Indikatoren')
for i, m in out['ind'].items(): print(f"  {i:8} {m['jahre'][0]}–{m['j']}  {'G' if m['gem'] else ' '}  {m['n']}")
