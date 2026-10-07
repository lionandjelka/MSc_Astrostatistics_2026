#!/usr/bin/env python3
"""Extract compact observable features from the large binary-SMBH Parquet file.

The script reads the file row-group by row-group and computes light-curve summary
features for u,g,r,i,z,y. It can retain simulation truth for instructor training
files; remove those columns before distributing blind-test features.
"""
from pathlib import Path
import argparse, ast, re
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

BANDS=['u','g','r','i','z','y']
INPUTS=[
"('id', '')", "('inputs', 'field')", "('inputs', 'RA')", "('inputs', 'dec')",
"('inputs', 'total mass')", "('inputs', 'mass ratio')", "('inputs', 'period')",
"('inputs', 'eccentricity')", "('inputs', 'inclination')",
"('inputs', 'arg of pericenter')", "('inputs', 'redshift')",
"('inputs', 'Eddington fraction')", "('inputs', 'retrograde')",
"('inputs', 'Doppler boosting')", "('inputs', 'lensing flare')",
"('inputs', 'accretion modulation')"]

def flatten(df):
    names=[]
    for c in df.columns:
        parts=list(c) if isinstance(c,tuple) else None
        if parts is None:
            try:
                v=ast.literal_eval(str(c)); parts=list(v) if isinstance(v,tuple) else [c]
            except Exception: parts=[c]
        parts=[str(p) for p in parts if str(p).strip()]
        names.append('__'.join(re.sub(r'[^0-9A-Za-z]+','_',p).strip('_') for p in parts))
    df=df.copy(); df.columns=names; return df

def features(t,m,e,prefix):
    t=np.asarray(t if t is not None else [],float)
    m=np.asarray(m if m is not None else [],float)
    e=np.asarray(e if e is not None else [],float)
    ok=np.isfinite(t)&np.isfinite(m)
    t,m=t[ok],m[ok]
    if e.size==ok.size: e=e[ok]
    else: e=np.full(m.size,np.nan)
    out={prefix+'n_obs':len(m)}
    if len(m)<2:
        for k in ['t_span','cadence_med','mag_mean','mag_median','mag_std','mag_mad','amp_p95_p05','err_median','chi2_const']:
            out[prefix+k]=np.nan
        return out
    med=np.nanmedian(m)
    out.update({
      prefix+'t_span':np.nanmax(t)-np.nanmin(t),
      prefix+'cadence_med':np.nanmedian(np.diff(np.sort(t))) if len(t)>2 else np.nan,
      prefix+'mag_mean':np.nanmean(m), prefix+'mag_median':med,
      prefix+'mag_std':np.nanstd(m,ddof=1),
      prefix+'mag_mad':np.nanmedian(np.abs(m-med)),
      prefix+'amp_p95_p05':np.nanpercentile(m,95)-np.nanpercentile(m,5),
      prefix+'err_median':np.nanmedian(e) if e.size else np.nan,
      prefix+'chi2_const':np.nanmean(((m-med)/e)**2) if np.isfinite(e).sum()>1 and np.nanmin(e)>0 else np.nan,
    })
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('output')
    ap.add_argument('--max-rows',type=int,default=None)
    ap.add_argument('--bands',nargs='*',default=BANDS)
    args=ap.parse_args()
    pf=pq.ParquetFile(args.input)
    available=set(pf.schema_arrow.names)
    cols=[c for c in INPUTS if c in available]
    for b in args.bands:
        for leaf in ['time','obs mag','mag err']:
            c=f"('{b} band', '{leaf}')"
            if c in available: cols.append(c)
    rows=[]; count=0
    for rg in range(pf.metadata.num_row_groups):
        d=flatten(pf.read_row_group(rg,columns=cols).to_pandas())
        for _,r in d.iterrows():
            rec={c:r[c] for c in d.columns if c.startswith('inputs__') or c=='id'}
            for b in args.bands:
                rec.update(features(r.get(f'{b}_band__time'), r.get(f'{b}_band__obs_mag'), r.get(f'{b}_band__mag_err'), f'{b}__'))
            rows.append(rec); count+=1
            if args.max_rows and count>=args.max_rows: break
        if args.max_rows and count>=args.max_rows: break
    out=pd.DataFrame(rows)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    out.to_parquet(args.output,index=False)
    print(out.shape); print(args.output)
if __name__=='__main__': main()
