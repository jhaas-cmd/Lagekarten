#!/usr/bin/env python3
"""INKAR-Export (BBSR-Angebotsmieten je Kreis, CSV oder XLSX) -> daten/mieten/bbsr_angebotsmieten.json

Aufruf:  python3 tools/inkar_bbsr.py <export.csv|export.xlsx> [Jahr]
Erwartet je Zeile: Kreisschlüssel (5-stellig), Name, eine oder mehrere Jahresspalten mit €/m².
Genommen wird das jüngste Jahr (oder das angegebene)."""
import csv, json, re, sys, io, os

def rows_of(path):
    if path.lower().endswith(('.xlsx', '.xlsm')):
        import openpyxl
        ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
        return [[('' if c is None else str(c)) for c in r] for r in ws.iter_rows(values_only=True)]
    raw = open(path, 'rb').read()
    for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
        try: txt = raw.decode(enc); break
        except UnicodeDecodeError: pass
    sep = ';' if txt.count(';') > txt.count(',') else ','
    return list(csv.reader(io.StringIO(txt), delimiter=sep))

def num(x):
    x = str(x).strip().replace(' ', '').replace(' ', '')
    if not x or x in ('-', '.', '–'): return None
    if ',' in x: x = x.replace('.', '').replace(',', '.')
    try: return float(x)
    except ValueError: return None

def main():
    src, want = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
    R = rows_of(src)
    # Kopfzeile = erste Zeile mit mindestens einer Jahreszahl
    hi = next(i for i, r in enumerate(R) if sum(bool(re.search(r'(19|20)\d\d', c)) for c in r) >= 1 and any(c.strip() for c in r))
    head = R[hi]
    years = {j: int(re.search(r'(19|20)\d\d', c).group(0)) for j, c in enumerate(head) if re.search(r'(19|20)\d\d', c)}
    kreise, de = {}, None
    for r in R[hi + 1:]:
        cells = [c.strip() for c in r]
        code = next((re.sub(r'\D', '', c) for c in cells if re.fullmatch(r'\d{4,5}(000)?', re.sub(r'\D', '', c) or 'x')), None)
        name = next((c for c in cells if re.search(r'[A-Za-zÄÖÜäöü]', c)), '')
        vals = {years[j]: num(cells[j]) for j in years if j < len(cells) and num(cells[j]) is not None}
        if not vals: continue
        y = int(want) if want and int(want) in vals else max(vals)
        if re.search(r'^deutschland|bundesgebiet', name, re.I) or code in ('0', '00000'):
            de = vals[y]; continue
        if not code: continue
        kreise[code.zfill(5)[:5]] = {'n': name, 'v': round(vals[y], 2), 'j': y}
    stand = max((k['j'] for k in kreise.values()), default=None)
    out = {'quelle': 'BBSR-Wohnungsmarktbeobachtung, IDN ImmoDaten GmbH (über INKAR)',
           'def': 'Erst- und Wiedervermietungsmieten inserierter Wohnungen, nettokalt, €/m², Kreisebene',
           'stand': stand, 'de': de, 'kreise': kreise}
    os.makedirs('daten/mieten', exist_ok=True)
    json.dump(out, open('daten/mieten/bbsr_angebotsmieten.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f'{len(kreise)} Kreise, Stand {stand}, Deutschland {de}')

if __name__ == '__main__':
    main()
