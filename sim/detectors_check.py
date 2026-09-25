#!/usr/bin/env python3
"""Candidate-detectors cross-check (UI v0.3.1). Recomputes every number quoted in the
'Candidate detectors' section of slw-detectability.html from cited formulas and checks the
page text contains each formatted value.  Usage:  python3 detectors_check.py [../slw-detectability.html]
Sources (see detectors/LIT_CHECK.md):
  Lamb & Retherford, Phys. Rev. 79, 549 (1950), Eqs. (25)-(27) r-f quench rate, Eq. (42) static-field quench,
    Sec. 16 (beta-e crossing, 540 G with their ~1000 Mc/s shift);  NIST ASD H I (A(2P1/2)=6.2648e8 s^-1, level energies);
  Klarsfeld, Phys. Lett. 30A, 382 (1969): 2S two-photon rate 8.2283 s^-1;  CODATA 2018 constants.
"""
import json, math, sys
import numpy as np

e = 1.602176634e-19; hbar = 1.054571817e-34; a0 = 5.29177210903e-11; c = 299792458.0
kB = 1.380649e-23; T0 = 290.0; eta0 = 376.730313668; mH = 1.6735575e-27
muB_MHz_G = 1.39962449361; gs = 2.00231930436
gam = 6.2648e8                      # FACT NIST ASD A(2p 2P1/2 -> 1s), s^-1
G2S = 8.2283                        # FACT Klarsfeld 1969, s^-1
cm1 = 29979.2458                    # MHz per cm^-1
E2S, E2P12, E2P32 = 82258.9543992821, 82258.9191133, 82259.2850014   # FACT NIST ASD H I levels, cm^-1
L_MHz = (E2S - E2P12) * cm1         # Lamb shift 2S1/2-2P1/2
S2P32_MHz = (E2P32 - E2S) * cm1     # 2S1/2-2P3/2
FS_MHz = (E2P32 - E2P12) * cm1      # 2P3/2-2P1/2
wL = 2 * math.pi * L_MHz * 1e6; w32 = 2 * math.pi * S2P32_MHz * 1e6
x = lambda E: e * a0 * E / hbar     # e a0 E / hbar  [s^-1]

def rate_resonant(E0):               # Lamb Eq.(26) in SI with plane-wave S0 = E0^2/(2 eta0): 1/tau = |<e.r>|^2 (eE0/hbar)^2/gamma, |<e.r>|^2 = 3 a0^2 (Eq. 27)
    return 3 * x(E0) ** 2 / gam
def rate_ac(E0, f, p32=True):         # Eq.(25) with BOTH rotating terms (needed for f << resonance); V = sqrt(3) e a0 E0 / 2
    w = 2 * math.pi * f
    r = gam * 3 * x(E0) ** 2 / 4 * (1 / ((wL - w) ** 2 + gam ** 2 / 4) + 1 / ((wL + w) ** 2 + gam ** 2 / 4))
    if p32:                           # 2S1/2 -> 2P3/2, |<z>|^2 = 6 a0^2, detuning 2S-2P3/2 (ASSUMPTION same gamma)
        r += gam * 6 * x(E0) ** 2 / 4 * (1 / ((w32 + w) ** 2 + gam ** 2 / 4) + 1 / ((w32 - w) ** 2 + gam ** 2 / 4))
    return r
def rate_static(E):                   # Lamb Eq.(42): gamma V^2/hbar^2 / (w^2 + gamma^2/4), V = sqrt(3) e a0 E (+ 2P3/2 term, V^2 = 6 e^2 a0^2 E^2)
    return gam * x(E) ** 2 * (3 / (wL ** 2 + gam ** 2 / 4) + 6 / (w32 ** 2 + gam ** 2 / 4))

# ---- level crossing beta (2S1/2 mJ=-1/2) with e (2P1/2 mJ=+1/2), hyperfine ignored (ASSUMPTION)
def e_level(B, L=L_MHz):
    xi = FS_MHz / 1.5; gL = 1 - 5.446e-4
    st = [(ml, ms) for ml in (-1, 0, 1) for ms in (-.5, .5) if abs(ml + ms - .5) < 1e-9]
    H = np.zeros((2, 2))
    for i, (ml, ms) in enumerate(st):
        H[i, i] = xi * ml * ms + muB_MHz_G * B * (gL * ml + gs * ms)
    H[0, 1] = H[1, 0] = 0.5 * xi * math.sqrt(2)          # L+S- between |0,+1/2> and |1,-1/2>
    return np.linalg.eigvalsh(H)[0] + xi
def split(B, L=L_MHz): return (L - gs * 0.5 * muB_MHz_G * B) - e_level(B, L)
def bisect(fn, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if fn(lo) * fn(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2
Bc = bisect(split, 300, 900); Bc1950 = bisect(lambda B: split(B, 1000.0), 300, 900)
slope = abs(split(Bc + 0.01) - split(Bc - 0.01)) / 0.02    # MHz/G
fwhm_MHz = gam / (2 * math.pi) / 1e6

# ---- E-field equivalents per sqrt(Hz), isotropic matched aperture lambda^2/4pi (page ASSUMPTION)
def e_equiv(f, F_lin):                # E_rms such that (E^2/eta0) * lambda^2/(4 pi) = kT0 F  (per Hz)
    lam = c / f; return math.sqrt(kB * T0 * F_lin * 4 * math.pi * eta0 / lam ** 2)
f241 = 241e3; Fa_qr = 53.6 - 28.6 * math.log10(f241 / 1e6)   # ITU-R P.372 quiet rural (extrapolated below 0.3 MHz, ASSUMPTION)
En_rx241 = e_equiv(f241, 10 ** (2.9 / 10))                    # ZFL-500LN+ -> Airspy, NF_sys 2.9 dB
En_out241 = e_equiv(f241, 10 ** (Fa_qr / 10))
En_leak241 = En_out241 * 10 ** (-55 / 20)
En_rx1296 = e_equiv(1296e6, 10 ** (0.4 / 10))                 # Kuhne MKU LNA 132 AH -> TinySA LNA on, NF_sys 0.4 dB
ryd = {"jing2020_GHz": 55e-9 * 100, "lei2024_100k": 0.95e-6 * 100, "lei2024_10k": 2.2e-6 * 100,
       "lei2024_1k": 5.7e-6 * 100, "jau2020_sub_kHz": 0.34e-3}             # V/m/sqrt(Hz)
db = lambda r: 20 * math.log10(r)
vth = lambda T: math.sqrt(kB * T / mH)
N = {
  "tau2S_s": 1 / G2S, "tau2P_ns": 1e9 / gam, "fwhm_MHz": fwhm_MHz, "L_MHz": L_MHz, "S2P32_MHz": S2P32_MHz,
  "rate_res_1uV": rate_resonant(1e-6), "rate_res_1uVrms": rate_resonant(math.sqrt(2) * 1e-6),
  "rate_241k_1uV": rate_ac(1e-6, f241), "rate_241k_1uV_P12only": rate_ac(1e-6, f241, False),
  "offres_dB": 10 * math.log10(rate_ac(1e-6, f241) / rate_resonant(1e-6)),
  "offres_dB_P12only": 10 * math.log10(rate_ac(1e-6, f241, False) / rate_resonant(1e-6)),
  "offres_dB_RWA": 10 * math.log10((gam ** 2 / 4) / ((wL - 2 * math.pi * f241) ** 2 + gam ** 2 / 4)),
  "check_lamb_eq26_tau_us": 1e6 / rate_resonant(math.sqrt(2 * eta0 * 34.0)),   # S0 = 3.4 mW/cm^2; paper: 1.25e-6 s
  "check_10Vcm_tau_us": 1e6 / rate_static(1000.0),                            # quench field used by Parthey 2011 / Landhuis 2002
  "Bcross_G": Bc, "Bcross_1950_G": Bc1950, "slope_MHz_per_G": slope,
  "dB_150k_G": 0.150 / slope, "dB_241k_G": 0.241 / slope, "dB_800k_G": 0.800 / slope, "dB_halfwidth_G": fwhm_MHz / 2 / slope,
  "rate_cross_1uV": 6 * x(1e-6) ** 2 / gam,
  "Emot_100uK_Vm": vth(100e-6) * Bc * 1e-4, "Emot_300K_Vm": vth(300.0) * Bc * 1e-4,
  "N_1ps_res": 1 / rate_resonant(1e-6), "N_1ps_241k": 1 / rate_ac(1e-6, f241),
  "Fa_qr_241k_dB": Fa_qr, "En_rx241": En_rx241, "En_out241": En_out241, "En_leak241": En_leak241, "En_rx1296": En_rx1296,
  "ryd": ryd, "r2_1s2s_a02": (1/math.sqrt(2))*(2*24/1.5**5 - 120/1.5**6),   # <1s|r^2|2s> radial integral in a0^2 (R10=2e^-r, R20=(2-r)e^(-r/2)/(2 sqrt2))
  "ryd100k_vs_rx241_dB": db(ryd["lei2024_100k"] / En_rx241), "ryd100k_vs_leak241_dB": db(ryd["lei2024_100k"] / En_leak241),
  "ryd100k_vs_out241_dB": db(ryd["lei2024_100k"] / En_out241), "jing_vs_rx1296_dB": db(ryd["jing2020_GHz"] / En_rx1296),
}
def sci(v, d=2):
    m, ex = f"{v:.{d-1}e}".split("e"); ex = int(ex)
    sup = str(ex).replace("-", "⁻").translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"{m}×10{sup}"
EXPECT = {   # formatted strings that must appear verbatim in the page section
  "tau2S": f"{N['tau2S_s']:.3f} s", "tau2P": f"{N['tau2P_ns']:.2f} ns", "fwhm": f"{N['fwhm_MHz']:.1f} MHz",
  "L": f"{N['L_MHz']:.1f} MHz", "S32": f"{N['S2P32_MHz']:.0f} MHz",
  "res": sci(N["rate_res_1uV"]), "resrms": sci(N["rate_res_1uVrms"]), "off": sci(N["rate_241k_1uV"]),
  "offdB": f"{abs(N['offres_dB']):.1f} dB", "rwadB": f"{abs(N['offres_dB_RWA']):.1f} dB",
  "Bc": f"{N['Bcross_G']:.1f} G", "Bc50": f"{N['Bcross_1950_G']:.0f} G", "slope": f"{N['slope_MHz_per_G']:.2f} MHz/G",
  "w150": f"{N['dB_150k_G']:.2f}", "w800": f"{N['dB_800k_G']:.2f} G", "hw": f"{N['dB_halfwidth_G']:.0f} G",
  "cross": sci(N["rate_cross_1uV"]), "Emot": f"{N['Emot_100uK_Vm']*1e3:.0f} mV/m",
  "Nres": sci(N["N_1ps_res"], 1), "Noff": sci(N["N_1ps_241k"], 1),
  "Enrx": f"{N['En_rx241']*1e12:.0f} pV/m", "Enleak": f"{N['En_leak241']*1e12:.0f} pV/m", "Emot300": f"{N['Emot_300K_Vm']:.0f} V/m", "r2": f"{abs(N['r2_1s2s_a02']):.2f} a₀²", "Enout": f"{N['En_out241']*1e9:.0f} nV/m",
  "En1296": f"{N['En_rx1296']*1e9:.0f} nV/m",
  "r1": f"{N['ryd100k_vs_rx241_dB']:.0f} dB", "rl": f"{N['ryd100k_vs_leak241_dB']:.0f} dB", "ro": f"{N['ryd100k_vs_out241_dB']:.0f} dB", "r3": f"{N['jing_vs_rx1296_dB']:.0f} dB",
  "chk26": f"{N['check_lamb_eq26_tau_us']:.2f} µs", "chk10": f"{N['check_10Vcm_tau_us']:.1f} µs",
}
if __name__ == "__main__":
    json.dump({"numbers": N, "expect": EXPECT}, open("detectors_numbers.json", "w"), indent=1, ensure_ascii=False)
    for k, v in EXPECT.items(): print(f"{k:8s} {v}")
    if len(sys.argv) > 1:
        html = open(sys.argv[1], encoding="utf-8").read()
        i = html.find('id="candDet"'); sec = html[i:html.find("</details>", i)] if i >= 0 else ""
        miss = [f"{k}: {v}" for k, v in EXPECT.items() if v not in sec]
        print(f"page check: {len(EXPECT) - len(miss)}/{len(EXPECT)} quoted numbers found in #candDet")
        for m in miss: print("  MISSING", m)
        sys.exit(1 if miss else 0)
