# Experiment D — Hypersonic Plasma-Sheath Cavitation, High Shear, and MHD Structures as Sources of SLW/SW

**Independent educational page.** This experiment is completely standalone and is not part of the SLW Hub.

Working title: Hypersonic Plasma-Sheath Cavitation, High Shear, and MHD Structures as Sources of Scalar-Longitudinal Waves (SLW) and Scalar Waves (SW)

One-sentence claim: A hypersonic vehicle in the ionosphere drives a dense, time-varying plasma sheath, density cavities, and high-shear MHD electric sheets. Those structures produce gradient-driven currents. In Hively MCE those gradients radiate SLW/SW — a longitudinal/scalar signature conventional RF sensors miss.

## Pages URL

When published via GitHub Pages:

**https://9wzg44nz44-glitch.github.io/Experiment-D-Hypersonic-Plasma-Shear-SLW/**

## Contents

- `index.html` — self-contained single-page educational app (CSS/JS inline; Google Fonts only). Toy sliders, uncalibrated.
- `slw-detectability.html` + `js/slw-detect.js` — **first quantitative SLW/SW detectability estimate** (`expt-d-detect-v0.1`). FACT sheath physics (RAM-C II, Drude blackout, ITU-R P.372 noise, TinySA Ultra floor) + HYP Hively EED (Hively & Loebl 2019 Eq. B5/37, US 9,306,527 Eq. 15, ledger □C). Every unknown coupling (η, χ, κ_C) is a swept slider. Cloud twin pending sync.
- `plots/` — Python reference figures (sim/run_analysis.py).
- `sim/` — Python reference model `expt_d_model.py`, the fixed cross-check grid `grid.json`, `dump_js_outputs.mjs` + `compare_outputs.mjs` (JS vs Python: PASS 105985 / FAIL 0 at rel tol 1e-9), and results tables.
- `wolfram/` — Mathematica twin `ExptDDetect.wl` (+ `_RunGrid.wl`, `_Publish.wl`). Not yet executed; JS-vs-WL compare owed.
- `.nojekyll` — allow GitHub Pages to serve without Jekyll processing

## Tone / caveats

Curious, technical, experiment-first. **Not flight data.** On `index.html`, the toy sliders and meters are pedagogical proxies, not calibrated predictions. `slw-detectability.html` gives calibrated FACT inputs, with the EED couplings left as explicit sweeps.

## Reproduce

```
cd sim && python3 expt_d_model.py           # baseline record
python3 run_analysis.py                     # plots + tables (needs numpy/matplotlib)
node dump_js_outputs.mjs && python3 -c "import json,expt_d_model as m;json.dump({'version':m.VERSION,'records':[m.model(p) for p in json.load(open('grid.json'))]},open('py_outputs.json','w'))" && node compare_outputs.mjs js_outputs.json py_outputs.json 1e-9
wolframscript -file ../wolfram/ExptDDetect_RunGrid.wl && node compare_outputs.mjs js_outputs.json wl_outputs.json 1e-9   # owed
```

## Citation

Hively, L. M. — US Patent 9,306,527 (2016), Maxwellian Circuit Equations / MCE framework.
Hively, L. M. & Loebl, A. S. — Classical and extended electrodynamics, Physics Essays 32, 112 (2019).
Grantham, W. L. — NASA TN D-6062 (1970); Jones, W. L. & Cross, A. E. — NASA TN D-6617 (1972) (RAM-C II plasma data).
