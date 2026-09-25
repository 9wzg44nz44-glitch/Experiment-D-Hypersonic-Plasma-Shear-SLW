"""Experiment D - SLW/SW detectability model (expt-d-detect-v0.1), Python reference implementation.

Mirrors web/js/slw-detect.js (browser/node) and wolfram/ExptDDetect.wl (Mathematica twin) formula-for-formula.
Labels: FACT = published / standard physics (cited in REPORT.md); HYP = Hively EED as printed (Hively & Loebl 2019,
US 9,306,527, hub ledger); ASSUMPTION = modelling choice made here; SWEEP = unknown coupling (never a single value).
"""
import math

VERSION = "expt-d-detect-v0.1"
# FACT: CODATA 2018
c = 299792458.0
mu0 = 1.25663706212e-6
eps0 = 8.8541878128e-12
qe = 1.602176634e-19
me = 9.1093837015e-31
kB = 1.380649e-23
T0 = 290.0
Z0 = mu0 * c
# FACT: US Standard Atmosphere 1976 (NASA-TM-X-74335)
USSA_H = [30, 40, 50, 60, 70, 80, 90]
USSA_RHO = [1.8410e-2, 3.9957e-3, 1.0269e-3, 3.0968e-4, 8.2829e-5, 1.8458e-5, 3.416e-6]
USSA_A = [301.71, 317.19, 329.80, 314.07, 297.14, 282.54, 274.10]
# FACT: Grantham NASA TN D-6062 (1970) p.12, nu = 2.51e9 s^-1 at 45.72 km, stations 2-4
NU_REF, H_REF = 2.51e9, 45.72
# FACT: ITU-R P.372 Table 1 (Fam = c - d log10 f_MHz; valid 0.3-250 MHz)
NOISE_ENV = {"none": None, "quiet_rural": (53.6, 28.6), "rural": (67.2, 27.7),
             "residential": (72.5, 27.7), "city": (76.8, 27.7)}
# HYP carry-over: hub SleeveBalunSNR receive convention
HUB_AEFF, HUB_ETA = math.pi * 0.05 * 0.05, 0.5
DB_PER_NP2 = 8.685889638065035  # 20/ln(10)

DEFAULTS = dict(h_km=70, mach=25, log10_ne=18, nu_scale=1, log10_S=6, delta_m=0.01, B_uT=50, theta_deg=90,
                mech="vxB", Te_K=6000, f_close=1, m_t=0.1, A_s=1, d_sh=0.05,
                f_rx=30e6, rbw=30e3, aperture="hub", SE_dB=55, noise_env="quiet_rural",
                log10_eta=-3, chi=0, log10_kappa=0, r_km=100)


def interp(xs, ys, x, logy):
    n = len(xs)
    if x <= xs[0]:
        i = 0
    elif x >= xs[n - 1]:
        i = n - 2
    else:
        i = 0
        while x > xs[i + 1]:
            i += 1
    t = (x - xs[i]) / (xs[i + 1] - xs[i])
    if logy:
        return math.exp(math.log(ys[i]) + t * (math.log(ys[i + 1]) - math.log(ys[i])))
    return ys[i] + t * (ys[i + 1] - ys[i])


def rho_air(h):
    return interp(USSA_H, USSA_RHO, h, True)


def sound_speed(h):
    return interp(USSA_H, USSA_A, h, False)


def csqrt(a, b):
    r = math.hypot(a, b)
    if a >= 0:
        re = math.sqrt((r + a) / 2)
        return re, (b / (2 * re) if re > 0 else 0.0)
    im = math.sqrt((r - a) / 2)
    return b / (2 * im), im


def dbm(W):
    return 10 * math.log10(W / 1e-3)


def sum_dbm(a, b):
    return 10 * math.log10(10 ** (a / 10) + 10 ** (b / 10))


def model(pin=None):
    p = dict(DEFAULTS)
    if pin:
        p.update(pin)
    a = sound_speed(p["h_km"])
    U = p["mach"] * a
    ne = 10 ** p["log10_ne"]
    wp = math.sqrt(ne * qe * qe / (eps0 * me))
    fp = wp / (2 * math.pi)
    nu = p["nu_scale"] * NU_REF * rho_air(p["h_km"]) / rho_air(H_REF)
    sigma = ne * qe * qe / (me * nu)
    S = 10 ** p["log10_S"]
    du = min(S * p["delta_m"], U)
    B = p["B_uT"] * 1e-6
    De = kB * p["Te_K"] / (me * nu)
    if p["mech"] == "diff":
        J = p["f_close"] * qe * De * ne / p["delta_m"]
    else:
        J = p["f_close"] * sigma * du * B * math.sin(p["theta_deg"] * math.pi / 180)
    Nc = p["A_s"] / (p["delta_m"] * p["delta_m"])
    Isrc = p["m_t"] * J * p["delta_m"] * math.sqrt(p["A_s"])
    fc = S / (2 * math.pi)
    g = 1.0 if p["f_rx"] <= fc else (p["f_rx"] / fc) ** (-5 / 3)
    Fspec = min(1.0, p["rbw"] * g / (2.5 * fc))
    Iband = Isrc * math.sqrt(Fspec)
    Ipk = math.sqrt(2) * Iband
    w = 2 * math.pi * p["f_rx"]
    den = w * w + nu * nu
    er = 1 - wp * wp / den
    ei = wp * wp * nu / (w * den)
    n_re, n_im = csqrt(er, ei)
    k0 = w / c
    alpha = k0 * n_im
    Ash_dB = DB_PER_NP2 * alpha * p["d_sh"]
    Tint = 4 * n_re / ((n_re + 1) * (n_re + 1) + n_im * n_im)
    Tint_dB = 10 * math.log10(Tint)
    lam = c / p["f_rx"]
    r = p["r_km"] * 1e3
    Arx = lam * lam / (4 * math.pi) if p["aperture"] == "recip" else HUB_AEFF * HUB_ETA
    Atem = 1.5 * lam * lam / (4 * math.pi)
    Nts = -102 + 10 * math.log10(p["rbw"] / 30e3)
    kT0B = dbm(kB * T0 * p["rbw"])
    env = NOISE_ENV[p["noise_env"]]
    fMHz = p["f_rx"] / 1e6
    if env:
        Fa = env[0] - env[1] * math.log10(fMHz)
        Next_conv = kT0B + Fa
        Nconv = sum_dbm(Nts, Next_conv)
        Nhiv = sum_dbm(Nts, Next_conv - p["SE_dB"])
    else:
        Fa, Nconv, Nhiv = None, Nts, Nts
    eta = 10 ** p["log10_eta"]
    kappa = 10 ** p["log10_kappa"]
    Sslw1 = Z0 * Ipk * Ipk / (4 * math.pi * r) ** 2
    slwLoss_dB = p["chi"] * Ash_dB
    Pslw1 = Sslw1 * Arx * 10 ** (-slwLoss_dB / 10)
    Pslw = eta * eta * Pslw1
    Cpk = mu0 * eta * Ipk / (4 * math.pi * r)
    ELpk = Z0 * Cpk / mu0
    Ssw1 = 0.5 * Z0 * Ipk * Ipk / (4 * math.pi * r) ** 2
    Psw = kappa * eta * eta * Ssw1 * Arx
    IcellPk = math.sqrt(2) * p["m_t"] * J * p["delta_m"] * p["delta_m"] * math.sqrt(Fspec)
    PtemEmit = Nc * Z0 * (math.pi / 3) * (IcellPk * p["delta_m"] / lam) ** 2
    Ptem_dBm = dbm(PtemEmit * Atem / (4 * math.pi * r * r)) + Tint_dB - Ash_dB
    Tb = p["Te_K"] * Tint
    Pth_dBm = dbm(kB * Tb * p["rbw"] * 1.5 * p["A_s"] / (4 * math.pi * r * r))
    Pslw_dBm, Psw_dBm = dbm(Pslw), dbm(Psw)
    NhivW = 10 ** (Nhiv / 10) * 1e-3
    return dict(
        version=VERSION, a_ms=a, U_ms=U, fp_Hz=fp, nu_s=nu, sigma_Sm=sigma, du_ms=du, De_m2s=De, J_Am2=J, Nc=Nc,
        Isrc_A=Isrc, fc_Hz=fc, Fspec=Fspec, Iband_A=Iband, eps_r=er, eps_i=ei, n_re=n_re, n_im=n_im,
        alpha_Npm=alpha, Ash_dB=Ash_dB, Tint_dB=Tint_dB, Arx_m2=Arx, Atem_m2=Atem,
        Nts_dBm=Nts, Fa_dB=Fa, Nconv_dBm=Nconv, Nhiv_dBm=Nhiv,
        Pslw1_dBm=dbm(Pslw1), Pslw_dBm=Pslw_dBm, SNR_slw_dB=Pslw_dBm - Nhiv,
        Cpk_T=Cpk, ELpk_Vm=ELpk,
        Psw1_dBm=dbm(Ssw1 * Arx), Psw_dBm=Psw_dBm, SNR_sw_dB=Psw_dBm - Nhiv,
        Ptem_dBm=Ptem_dBm, SNR_tem_dB=Ptem_dBm - Nconv, PtemHiv_dBm=Ptem_dBm - p["SE_dB"],
        Tb_K=Tb, Pth_dBm=Pth_dBm, SNR_th_dB=Pth_dBm - Nconv,
        eta_th0=math.sqrt(NhivW / Pslw1), eta_th10=math.sqrt(10 * NhivW / Pslw1),
        etakap_th0_sw=math.sqrt(NhivW / (Ssw1 * Arx)),
        rmax_km=p["r_km"] * math.sqrt(Pslw / NhivW),
        kr=2 * math.pi * r / lam,
    )


def grid():
    """Fixed cross-check grid (shared with node + WL via grid.json)."""
    G = []
    for mech in ["vxB", "diff"]:
        for ne in [16, 18, 20]:
            for lS in [4, 6, 8]:
                for f in [1e6, 30e6, 433.92e6, 1296e6]:
                    for ap in ["hub", "recip"]:
                        for r in [1, 10, 100, 1000]:
                            for h in [40, 70]:
                                for env in ["quiet_rural", "none"]:
                                    G.append(dict(mech=mech, log10_ne=ne, log10_S=lS, f_rx=f, aperture=ap,
                                                  r_km=r, h_km=h, noise_env=env,
                                                  chi=(0.5 if (ne == 18 and r == 100) else 0),
                                                  delta_m=(0.003 if lS == 8 else 0.01)))
    return G


if __name__ == "__main__":
    import json
    import sys
    o = model()
    json.dump(o, sys.stdout, indent=1)
