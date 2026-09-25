"""Experiment D v0.2 - 'Sheath modulation' study (physics id expt-d-detect-v0.2). Python reference.

Mirrors js/slw-modulation.js (browser/node) and the ExptDMod* section of wolfram/ExptDDetect.wl formula-for-formula.
Builds on the UNCHANGED v0.1 engine (../expt_d_model.py): same sheath current J, same random-phase current
I_src = (dn/n) J delta sqrt(A_s), same Hively & Loebl 2019 Eq. B5 SLW flux, same receiver/noise model.

Labels: FACT = published / standard physics (cited in REPORT.md); HYP = Hively EED as printed;
ASSUMPTION = modelling choice made here (user-adjustable); SWEEP = unknown coupling (never a single value).
"""
import math
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_here, os.path.join(_here, "..")]  # repo sim/ layout | sim-lab layout
import expt_d_model as B  # v0.1 engine

VERSION = "expt-d-detect-v0.2"
AMU = 1.66053906660e-27
M_AIR = 28.9644 * AMU            # FACT USSA-1976 sea-level mean molecular mass (constant below 86 km)
X_O2, X_N2 = 0.209476, 0.780840  # FACT USSA-1976 volume fractions
A_LF75 = B.c ** 2 / (4 * math.pi * 1e6 ** 2)  # v0.1 '1 MHz resonant antenna' aperture lambda^2/4pi at 1 MHz

MOD_DEFAULTS = dict(
    C_mack=0.65,   # FACT Parziale et al. 2015 Table 3: 2 f delta/U_E = 0.63-0.69 (Demetriades: 0.6-0.9)
    b2=0.2,        # ASSUMPTION: Mack band full width / f2 (read by eye from Parziale 2015 Fig. 6 & Fig. 9 FWHM bars)
    m2=0.01,       # ASSUMPTION: rms dn_e/n_e in the Mack band (anchored on FLDI rms drho/rho ~0.1-1 %, Parziale 2015 Fig. 6)
    D_m=1.0,       # vehicle base diameter D (m)
    St=0.2,        # FACT-range: Strouhal fD/U, 0.2 (hydrodynamic mode) ... 0.3-0.5 (aeroacoustic mode)
    bsh=0.2,       # ASSUMPTION: shedding band full width / fsh (no measured value used)
    msh=0.1,       # ASSUMPTION: rms dn_e/n_e of the wake current at the shedding frequency (no source found)
    Tw_K=3000.0,   # ASSUMPTION: near-wake gas = electron temperature for the chemistry rates (K)
    xs_D=1.0,      # ASSUMPTION: shedding site distance behind the base, in diameters
    tau_s=1.0,     # dwell (integration) time, s
    d_th=1.0,      # detection threshold on the deflection d (1 = v0.1's 'SNR 0 dB' convention)
    listen="lf75",  # plot/verdict antenna: 'lf75' (v0.1 1 MHz antenna, fixed aperture) | 'hub' (Dan's small antenna)
)
NQ_BAND = 200      # midpoint quadrature points across a matched band
NQ_ALL = 1200      # log-midpoint points for the all-band Eckart detector, 1 Hz .. 10 MHz
F_ALL = (1.0, 1e7)


# ---------------- FACT chemistry (rates in SI: m^3/s, m^6/s) ----------------
def alpha_dr(T):
    """Dissociative recombination e + NO+ -> N + O. Torr, St-Maurice & Torr 1977: 4.2e-7 (Te/300)^-0.85 cm^3/s."""
    return 4.2e-13 * (T / 300.0) ** -0.85


def k_att_o2(T):
    """e + O2 + O2 -> O2- + O2, Kossyi et al. 1992 R45 with Te = Tg = T: 1.4e-29 (300/T) exp(-600/T) cm^6/s."""
    return 1.4e-41 * (300.0 / T) * math.exp(-600.0 / T)


def k_att_n2(T):
    """e + O2 + N2 -> O2- + N2, Kossyi 1992 R46 with Te = Tg = T: 1.07e-31 (300/T)^2 exp(-70/T) cm^6/s."""
    return 1.07e-43 * (300.0 / T) ** 2 * math.exp(-70.0 / T)


def k_det_o2(T):
    """O2- + O2 -> e + 2 O2, Kossyi 1992 R57: 2.7e-10 (T/300)^0.5 exp(-5590/T) cm^3/s."""
    return 2.7e-16 * (T / 300.0) ** 0.5 * math.exp(-5590.0 / T)


def n_air(h):
    return B.rho_air(h) / M_AIR


# ---------------- v0.1 pieces re-used (identical formulas) ----------------
def sheath_loss_db(f, p):
    """v0.1 Drude slab one-way attenuation A_sh (dB) and interface transmission Tint (linear) at frequency f."""
    ne = 10 ** p["log10_ne"]
    wp = math.sqrt(ne * B.qe * B.qe / (B.eps0 * B.me))
    nu = p["nu_scale"] * B.NU_REF * B.rho_air(p["h_km"]) / B.rho_air(B.H_REF)
    w = 2 * math.pi * f
    den = w * w + nu * nu
    er = 1 - wp * wp / den
    ei = wp * wp * nu / (w * den)
    n_re, n_im = B.csqrt(er, ei)
    A = B.DB_PER_NP2 * (w / B.c) * n_im * p["d_sh"]
    T = 4 * n_re / ((n_re + 1) ** 2 + n_im ** 2)
    return A, T, n_re


def noise_density(f, p):
    """v0.1 shielded Hively receiver floor divided by RBW (W/Hz): TinySA spec density (+) (kT0 F_a - SE)."""
    Nts = -102 + 10 * math.log10(p["rbw"] / 30e3)
    env = B.NOISE_ENV[p["noise_env"]]
    if env:
        kT0B = B.dbm(B.kB * B.T0 * p["rbw"])
        Fa = env[0] - env[1] * math.log10(f / 1e6)
        N = B.sum_dbm(Nts, kT0B + Fa - p["SE_dB"])
    else:
        N = Nts
    return 10 ** (N / 10) * 1e-3 / p["rbw"]


def ap_area(kind, f):
    if kind == "hub":
        return B.HUB_AEFF * B.HUB_ETA
    if kind == "lf75":
        return A_LF75
    return (B.c / f) ** 2 / (4 * math.pi)  # 'recip': lambda^2/4pi (HL2019 Sec. VI reciprocity, HYP)


def setup(pin=None):
    p = dict(B.DEFAULTS)
    p.update(MOD_DEFAULTS)
    if pin:
        p.update(pin)
    b = B.model(p)  # v0.1 base quantities at the v0.1 f_rx (only f-independent ones are used here)
    ne = 10 ** p["log10_ne"]
    U = b["U_ms"]
    s = dict(p=p, b=b, ne=ne, U=U)
    # FACT (a): Mack second mode, f2 = C U_E / (2 delta); ASSUMPTION U_E = U (slender body), delta = v0.1 shear-layer delta
    s["f2"] = p["C_mack"] * U / (2 * p["delta_m"])
    s["f2_lo"], s["f2_hi"] = s["f2"] * (1 - p["b2"] / 2), s["f2"] * (1 + p["b2"] / 2)
    # FACT (c): wake oscillation, fsh = St U / D
    s["fsh"] = p["St"] * U / p["D_m"]
    s["fsh_lo"], s["fsh_hi"] = s["fsh"] * (1 - p["bsh"] / 2), s["fsh"] * (1 + p["bsh"] / 2)
    # FACT (d): wake chemistry. dn/dt = -alpha n^2  ->  n(t)/n0 = 1/(1 + alpha n0 t)
    al = alpha_dr(p["Tw_K"])
    s["alpha"] = al
    s["t_s"] = p["xs_D"] * p["D_m"] / U
    s["surv"] = 1.0 / (1.0 + al * ne * s["t_s"])
    s["tau_dr"] = 1.0 / (al * ne)
    s["f_chem"] = 1.0 / (2 * math.pi * s["tau_dr"])
    na = n_air(p["h_km"])
    nO2, nN2 = X_O2 * na, X_N2 * na
    s["nu_att"] = k_att_o2(p["Tw_K"]) * nO2 * nO2 + k_att_n2(p["Tw_K"]) * nO2 * nN2
    s["nu_det"] = k_det_o2(p["Tw_K"]) * nO2
    s["L_wake_m"] = U * s["tau_dr"]
    # currents (v0.1 form I = m J delta sqrt(A_s) for every component)
    I0 = b["J_Am2"] * p["delta_m"] * math.sqrt(p["A_s"])
    s["I0"] = I0
    s["It"] = b["Isrc_A"]  # = m_t I0 (v0.1, broadband turbulence)
    s["I2"] = p["m2"] * I0
    s["Ish"] = p["msh"] * s["surv"] * I0
    s["fc"] = b["fc_Hz"]
    s["r"] = p["r_km"] * 1e3
    return s


def psd_I(s, f):
    """One-sided current PSD (A^2/Hz): v0.1 broadband + Mack top-hat + shedding top-hat."""
    p = s["p"]
    g = 1.0 if f <= s["fc"] else (f / s["fc"]) ** (-5.0 / 3.0)
    S = s["It"] ** 2 * g / (2.5 * s["fc"])
    if s["f2_lo"] <= f < s["f2_hi"]:
        S += s["I2"] ** 2 / (p["b2"] * s["f2"])
    if s["fsh_lo"] <= f < s["fsh_hi"]:
        S += s["Ish"] ** 2 / (p["bsh"] * s["fsh"])
    return S


def s1(s, f, A):
    """Received SLW PSD at eta = 1 (W/Hz): 2 Z0 S_I(f) A / (4 pi r)^2 x 10^(-chi A_sh(f)/10)  (HL2019 Eq. B5, v0.1 I_pk = sqrt2 I_rms)."""
    p = s["p"]
    loss = p["chi"] * sheath_loss_db(f, p)[0] if p["chi"] else 0.0
    return 2 * B.Z0 * psd_I(s, f) * A / (4 * math.pi * s["r"]) ** 2 * 10 ** (-loss / 10)


def q_band(s, fa, fb, A):
    """Q = integral (s1/n)^2 df over [fa, fb], NQ_BAND midpoints."""
    df = (fb - fa) / NQ_BAND
    q = 0.0
    for i in range(NQ_BAND):
        f = fa + (i + 0.5) * df
        q += (s1(s, f, A) / noise_density(f, s["p"])) ** 2 * df
    return q


def q_all(s, A):
    """All-band Eckart detector over 1 Hz..10 MHz (log midpoints), far-field part only (k r >= 1)."""
    la, lb = math.log(F_ALL[0]), math.log(F_ALL[1])
    dl = (lb - la) / NQ_ALL
    fmin = B.c / (2 * math.pi * s["r"])
    q = 0.0
    for i in range(NQ_ALL):
        f = math.exp(la + (i + 0.5) * dl)
        if f < fmin:
            continue
        q += (s1(s, f, A) / noise_density(f, s["p"])) ** 2 * f * dl
    return q


def eta_from_q(q, tau, d_th):
    return (d_th * d_th / (tau * q)) ** 0.25 if q > 0 else math.inf


def tuned(s, f, ap):
    """A v0.1-style tuned receiver (centre frequency f, bandwidth RBW): exact v0.1 in-band power + band top-hats."""
    p = s["p"]
    A = ap_area(ap, f)
    g = 1.0 if f <= s["fc"] else (f / s["fc"]) ** (-5.0 / 3.0)
    F = min(1.0, p["rbw"] * g / (2.5 * s["fc"]))
    Iband2 = s["It"] ** 2 * F + p["rbw"] * (psd_I(s, f) - s["It"] ** 2 * g / (2.5 * s["fc"]))
    loss = p["chi"] * sheath_loss_db(f, p)[0]
    P1 = 2 * B.Z0 * Iband2 * A / (4 * math.pi * s["r"]) ** 2 * 10 ** (-loss / 10)
    N = noise_density(f, p) * p["rbw"]
    q = p["rbw"] * (P1 / N) ** 2
    tau = max(p["tau_s"], 1.0 / p["rbw"])
    return dict(P1_dBm=B.dbm(P1), N_dBm=B.dbm(N), eta1=math.sqrt(N / P1), eta=eta_from_q(q, tau, p["d_th"]),
                gain_dB=5 * math.log10(tau * p["rbw"]) - 10 * math.log10(p["d_th"]))


def matched(s, fa, fb, fcen):
    p = s["p"]
    A = ap_area("recip", fcen)
    q = q_band(s, fa, fb, A)
    tau = max(p["tau_s"], 1.0 / (fb - fa))
    return dict(A=A, q=q, eta=eta_from_q(q, tau, p["d_th"]), kr=2 * math.pi * s["r"] * fcen / B.c,
                quarter_wave_m=B.c / fcen / 4)


def am_fingerprint(p, f, m):
    """FACT-side: peak-to-peak one-way loss swing (dB) and phase swing (rad) on a carrier f crossing the sheath
    when n_e -> n_e (1 +/- m); evaluates the unchanged v0.1 Drude slab."""
    q = dict(p)
    out = []
    for sgn in (1, -1):
        q["log10_ne"] = p["log10_ne"] + math.log10(1 + sgn * m)
        A, T, nre = sheath_loss_db(f, q)
        out.append((A - 10 * math.log10(T), 2 * math.pi * f / B.c * nre * p["d_sh"]))
    A0, T0, _ = sheath_loss_db(f, p)
    return dict(dL_dB=out[0][0] - out[1][0], dphi_rad=out[0][1] - out[1][1], L0_dB=A0 - 10 * math.log10(T0))


AM_F = [433.92e6, 1296e6, 2.25e9, 10e9]


def model(pin=None):
    s = setup(pin)
    p = s["p"]
    o = dict(version=VERSION)
    for k in ["U", "f2", "f2_lo", "f2_hi", "fsh", "fsh_lo", "fsh_hi", "alpha", "t_s", "surv", "tau_dr", "f_chem",
              "nu_att", "nu_det", "L_wake_m", "I0", "It", "I2", "Ish"]:
        o[k] = s[k]
    for key, f, ap in [("r433", 433.92e6, "hub"), ("r1296", 1296e6, "hub"), ("r1M", 1e6, "recip")]:
        t = tuned(s, f, ap)
        for kk, vv in t.items():
            o[key + "_" + kk] = vv
    m2 = matched(s, s["f2_lo"], s["f2_hi"], s["f2"])
    msh = matched(s, s["fsh_lo"], s["fsh_hi"], s["fsh"])
    for kk, vv in m2.items():
        o["rMack_" + kk] = vv
    for kk, vv in msh.items():
        o["rShed_" + kk] = vv
    # plot / verdict antenna
    A = ap_area(p["listen"], 1e6)
    o["A_listen"] = A
    qa = q_all(s, A)
    q2 = q_band(s, s["f2_lo"], s["f2_hi"], A)
    qs = q_band(s, s["fsh_lo"], s["fsh_hi"], A)
    o["q_all"], o["q_mack"], o["q_shed"] = qa, q2, qs
    o["eta_all"] = eta_from_q(qa, p["tau_s"], p["d_th"])
    o["eta_mack"] = eta_from_q(q2, max(p["tau_s"], 1 / (s["f2_hi"] - s["f2_lo"])), p["d_th"])
    o["eta_shed"] = eta_from_q(qs, max(p["tau_s"], 1 / (s["fsh_hi"] - s["fsh_lo"])), p["d_th"])
    o["kr_shed"] = 2 * math.pi * s["r"] * s["fsh"] / B.c
    # hypothetical pure-tone bound for the Mack power (NOT physical: measured band ~20 % wide)
    P2 = 2 * B.Z0 * s["I2"] ** 2 * A / (4 * math.pi * s["r"]) ** 2
    o["eta_tone_mack"] = math.sqrt(p["d_th"] * noise_density(s["f2"], p) / (P2 * p["tau_s"])) if P2 > 0 else math.inf
    eta = 10 ** p["log10_eta"]
    o["dev_all"] = eta ** 4 / o["eta_all"] ** 4 * p["d_th"] if math.isfinite(o["eta_all"]) else 0.0  # deflection at your eta
    # spectrum samples (for plots and the cross-check)
    fs = [10 ** (k / 8) for k in range(0, 57)]  # 1 Hz .. 10 MHz
    o["spec_f"] = fs
    o["spec_S_dBmHz"] = [B.dbm(max(eta * eta * s1(s, f, A), 1e-300)) for f in fs]
    o["spec_N_dBmHz"] = [B.dbm(noise_density(f, p)) for f in fs]
    for f in AM_F:
        a = am_fingerprint(p, f, p["m2"])
        o["am_%d_dL_dB" % round(f / 1e6)] = a["dL_dB"]
        o["am_%d_dphi" % round(f / 1e6)] = a["dphi_rad"]
        o["am_%d_L0_dB" % round(f / 1e6)] = a["L0_dB"]
    return o


def grid():
    G = []
    for mach in [10, 15, 20, 25]:
        for h in [30, 45, 60, 70]:
            for r in [10, 100, 1000]:
                for ne in [16, 18, 20]:
                    for listen in ["lf75", "hub"]:
                        for tau in [0.01, 1.0, 100.0]:
                            G.append(dict(mach=mach, h_km=h, r_km=r, log10_ne=ne, listen=listen, tau_s=tau,
                                          log10_eta=-3 if tau == 1.0 else -6,
                                          chi=0.5 if (ne == 18 and r == 100) else 0.0,
                                          D_m=1.0 if mach < 20 else 5.0,
                                          delta_m=0.01 if h >= 45 else 0.003,
                                          m2=0.01 if r != 1000 else 0.1))
    return G


if __name__ == "__main__":
    import json
    json.dump(model(), sys.stdout, indent=1, default=str)
