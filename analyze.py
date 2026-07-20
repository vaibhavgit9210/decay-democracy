import csv, json

FILES = {
 'libdem':'liberal-democracy-index.csv',
 'electdem':'electoral-democracy-index.csv',
 'expression':'freedom-of-expression-index.csv',
 'judicial':'judicial-constraints-on-the-executive-index.csv',
 'civlib':'civil-liberties-index-vdem.csv',
 'assoc':'freedom-of-association-index.csv',
}
COUNTRIES = ['Hungary','Turkey','Venezuela','India','Switzerland']
data = {c:{k:{} for k in FILES} for c in COUNTRIES}
for key,fn in FILES.items():
    with open(fn) as f:
        for row in csv.DictReader(f):
            if row['entity'] in COUNTRIES:
                vc=[k for k in row if k.endswith('estimate_best')][0]
                try: data[row['entity']][key][int(row['year'])]=float(row[vc])
                except ValueError: pass

# Decay detector, calibrated on known backsliders then applied to India + control.
# Episode fires when, from the country's modern-era (post-1990) peak, the index
# has fallen >= 0.10 (V-Dem ERT threshold) and stayed below peak-0.05 for >= 5 years.
# Onset = start of the steepest 10-year decline window after the peak.
def detect(s):
    yrs=[y for y in sorted(s) if y>=1990]
    peak_y=max(yrs,key=lambda y:(s[y],y)); peak=s[peak_y]
    last=yrs[-1]; cur=s[last]
    drop=peak-cur
    # steepest 10-year window after peak
    onset=None; steep=0
    for y in yrs:
        if y<peak_y or y+10>last+1: continue
        d=s[y]-s[min(y+10,last)]
        if d>steep: steep=d; onset=y
    # years below peak-0.05
    below=[y for y in yrs if y>peak_y and s[y]<peak-0.05]
    sustained=(last-below[0]+1) if below else 0
    fires = drop>=0.10 and sustained>=5
    return {'peak_year':peak_y,'peak':round(peak,3),'latest_year':last,'latest':round(cur,3),
            'drop':round(drop,3),'onset':onset,'sustained_years':sustained,'fires':fires}

out={'series':{},'verdicts':{},'sequence':{}}
for c in COUNTRIES:
    out['verdicts'][c]={'libdem':detect(data[c]['libdem'])}
    # sequencing: for each sub-index, first year (>= onset-3) it fell >=0.05 below its post-1990 peak
    ep=out['verdicts'][c]['libdem']; seq={}
    if ep['fires']:
        for k in ['expression','civlib','assoc','judicial','electdem']:
            s=data[c][k]; yrs=[y for y in sorted(s) if y>=1990]
            pk=max(s[y] for y in yrs if y<=ep['onset'])
            first=None
            for y in yrs:
                if y>=ep['onset']-3 and pk-s[y]>=0.05: first=y; break
            seq[k]={'pre_peak':round(pk,3),'first_fall':first,'latest':round(s[yrs[-1]],3),
                    'drop':round(pk-s[yrs[-1]],3)}
    out['sequence'][c]=seq
    out['series'][c]={k:{y:round(v,3) for y,v in sorted(data[c][k].items()) if y>=1975} for k in FILES}

json.dump(out,open('analysis.json','w'))
print(json.dumps({'verdicts':out['verdicts'],'sequence':out['sequence']},indent=1))
