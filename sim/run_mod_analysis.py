"""Experiment D v0.2 sheath-modulation analysis: tables + plots.  python3 run_mod_analysis.py"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import expt_d_mod as M
import expt_d_model as B

OUT = os.path.dirname(os.path.abspath(__file__))
PL = os.path.join(OUT, "..", "plots")
os.makedirs(PL, exist_ok=True)
plt.rcParams.update({"figure.dpi": 110, "font.size": 9})
TAG = "expt-d-detect-v0.2 · FACT sheath modulation + HYP (Hively EED) SLW · not flight data"
res = {}

# ---- regression: v0.2 tuned receiver with no bands, single shot == v0.1 eta_th0 ----
worst = 0.0; n = 0
for p in B.grid():
    q = dict(p); q.update(m2=0.0, msh=0.0, tau_s=0.0, d_th=1.0)
    s = M.setup(q)
    t = M.tuned(s, p["f_rx"], p["aperture"])
    ref = B.model(p)["eta_th0"]
    worst = max(worst, abs(t["eta"] - ref) / ref); n += 1
res["regression_v01"] = dict(points=n, worst_rel=worst)
print("regression vs v0.1 eta_th0:", n, "points, worst rel", worst)

# ---- Table A: modulation bands for representative cases ----
rows = []
for mach, h in [(10, 30), (10, 45), (15, 45), (15, 60), (20, 45), (20, 60), (25, 70)]:
    for dl in [0.003, 0.01]:
        for D in [1.0, 5.0]:
            o = M.model(dict(mach=mach, h_km=h, delta_m=dl, D_m=D))
            rows.append(dict(mach=mach, h=h, delta_mm=dl * 1e3, D=D, U=o["U"], f2=o["f2"], f2_C09=0.9 / 0.65 * o["f2"],
                             fsh=o["fsh"], fsh_045=0.45 / 0.2 * o["fsh"], t_s=o["t_s"]))
res["bands"] = rows
chem = []
for h in [30, 45, 60, 70]:
    for T in [1000, 3000, 6000]:
        for ne in [16, 18, 20]:
            o = M.model(dict(h_km=h, Tw_K=T, log10_ne=ne, mach=15, D_m=1.0))
            chem.append(dict(h=h, T=T, ne=ne, alpha=o["alpha"], tau_dr=o["tau_dr"], f_chem=o["f_chem"], nu_att=o["nu_att"],
                             nu_det=o["nu_det"], surv=o["surv"], t_s=o["t_s"], L_wake=o["L_wake_m"]))
res["chem"] = chem

# ---- Table B: minimum detectable eta, v0.1 vs v0.2 ----
def etas(base, r, tau):
    q = dict(base); q.update(r_km=r, tau_s=tau)
    o = M.model(q)
    return o
cases = {"baseline (70 km, M25, n_e 1e18, delta 1 cm, D 1 m)": dict(),
         "representative (45 km, M15, n_e 1e18, delta 1 cm, D 2.5 m)": dict(h_km=45, mach=15, D_m=2.5),
         "extreme n_e 1e20 (70 km, M25)": dict(log10_ne=20)}
tabB = []
for cname, base in cases.items():
    for r in [10, 100]:
        o0 = etas(base, r, 1e-9)   # tau -> 1/B : single shot (v0.1 convention)
        o1 = etas(base, r, 1.0)
        o100 = etas(base, r, 100.0)
        for key, lab in [("r433", "433.92 MHz, Dan's small antenna (hub)"), ("r1296", "1296 MHz, Dan's sleeve balun (hub)"),
                         ("r1M", "1 MHz, 75 m resonant (lambda^2/4pi)")]:
            tabB.append(dict(case=cname, r=r, rx=lab, v01=o0[key + "_eta1"], v02_1s=o1[key + "_eta"], v02_100s=o100[key + "_eta"]))
        tabB.append(dict(case=cname, r=r, rx="Mack-band matched LF (lambda^2/4pi at f2=%.0f kHz, %.0f m quarter-wave)" % (o1["f2"] / 1e3, o1["rMack_quarter_wave_m"]),
                         v01=None, v02_1s=o1["rMack_eta"], v02_100s=o100["rMack_eta"]))
        tabB.append(dict(case=cname, r=r, rx="Shedding-band matched VLF (lambda^2/4pi at fsh=%.0f Hz, %.0f km quarter-wave; kr=%.2g)" % (o1["fsh"], o1["rShed_quarter_wave_m"] / 1e3, o1["rShed_kr"]),
                         v01=None, v02_1s=o1["rShed_eta"], v02_100s=o100["rShed_eta"]))
        tabB.append(dict(case=cname, r=r, rx="All-band Eckart, fixed 75 m-class antenna (A=7.2e3 m^2), far field only",
                         v01=None, v02_1s=o1["eta_all"], v02_100s=o100["eta_all"]))
        tabB.append(dict(case=cname, r=r, rx="  of which Mack band only (same antenna)", v01=None, v02_1s=o1["eta_mack"], v02_100s=o100["eta_mack"]))
        tabB.append(dict(case=cname, r=r, rx="  pure-tone bound for Mack power (NOT physical)", v01=None, v02_1s=o1["eta_tone_mack"], v02_100s=o100["eta_tone_mack"]))
res["etas"] = tabB
f = lambda x: "—" if x is None else ("%.2g" % x)
with open(os.path.join(OUT, "results_mod.md"), "w") as fh:
    fh.write("# Experiment D v0.2 — minimum detectable η (deflection d ≥ 1, v0.1 convention)\n\n")
    fh.write("v0.1 = single look in the 30 kHz RBW (no integration). v0.2 = same receiver plus integration over the dwell time (radiometer / Eckart detector).\n\n")
    for cname in cases:
        fh.write("## " + cname + "\n\n| range | receiver | v0.1 | v0.2, 1 s | v0.2, 100 s |\n|---|---|---|---|---|\n")
        for t in tabB:
            if t["case"] == cname:
                fh.write("| %d km | %s | %s | %s | %s |\n" % (t["r"], t["rx"], f(t["v01"]), f(t["v02_1s"]), f(t["v02_100s"])))
        fh.write("\n")
    fh.write("## Modulation bands (FACT frequencies; U from Mach × USSA-1976 sound speed)\n\n| Mach | h km | δ mm | D m | U m/s | f2 (C=0.65) kHz | f2 (C=0.9) kHz | f_sh (St 0.2) Hz | f_sh (St 0.45) Hz |\n|---|---|---|---|---|---|---|---|---|\n")
    for r_ in rows:
        fh.write("| %g | %g | %g | %g | %.0f | %.0f | %.0f | %.0f | %.0f |\n" % (r_["mach"], r_["h"], r_["delta_mm"], r_["D"], r_["U"], r_["f2"] / 1e3, r_["f2_C09"] / 1e3, r_["fsh"], r_["fsh_045"]))
    fh.write("\n## Wake chemistry time scales (FACT rates; Mach 15, D = 1 m, shedding site 1 D behind base)\n\n| h km | T K | n_e m⁻³ | α_DR m³/s | τ_DR = 1/(α n_e) | f_chem = 1/(2π τ_DR) | wake length U τ_DR | survival at t_s | ν_att s⁻¹ | ν_det s⁻¹ |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for c in chem:
        fh.write("| %g | %g | 1e%d | %.2e | %.2e s | %.2e Hz | %.3g m | %.3g | %.2e | %.2e |\n" % (c["h"], c["T"], c["ne"], c["alpha"], c["tau_dr"], c["f_chem"], c["L_wake"], c["surv"], c["nu_att"], c["nu_det"]))
    fh.write("\nRegression: v0.2 tuned receiver with bands off and single-shot integration reproduces v0.1 η_th0 on %d v0.1 grid points, worst rel %.2e.\n" % (n, worst))
json.dump(res, open(os.path.join(OUT, "analysis_mod.json"), "w"), indent=1, default=str)

# ---------- Fig M1: source current PSD components ----------
fs = np.logspace(0, 7.3, 900)
fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.2), sharey=True)
for ax, (lab, pin) in zip(axs, [("Mach 10, 30 km, δ 3 mm, D 1 m", dict(mach=10, h_km=30, delta_m=0.003, D_m=1.0)),
                                ("Mach 15, 45 km, δ 1 cm, D 2.5 m", dict(mach=15, h_km=45, delta_m=0.01, D_m=2.5)),
                                ("Mach 20, 60 km, δ 1 cm, D 5 m", dict(mach=20, h_km=60, delta_m=0.01, D_m=5.0))]):
    s = M.setup(pin)
    tot = [M.psd_I(s, x) for x in fs]
    turb = [s["It"] ** 2 * (1 if x <= s["fc"] else (x / s["fc"]) ** (-5 / 3)) / (2.5 * s["fc"]) for x in fs]
    ax.loglog(fs, tot, color="k", lw=1.6, label="total (sum of independent parts)")
    ax.loglog(fs, turb, color="#1f78b4", ls="--", label="(b) broadband turbulence (v0.1 model)")
    ax.axvspan(s["f2_lo"], s["f2_hi"], color="#33a02c", alpha=.25, label="(a) Mack 2nd-mode band  f₂ = C·U/(2δ)")
    ax.axvspan(s["fsh_lo"], s["fsh_hi"], color="#ff7f00", alpha=.3, label="(c) wake oscillation band  f = St·U/D")
    ax.axvline(s["f_chem"], color="#6a3d9a", ls=":", label="(d) chemistry corner 1/(2π τ_DR) at n_e=1e18, 3000 K")
    ax.set_title(lab + "\nU = %.0f m/s, f₂ = %.0f kHz, f_sh = %.0f Hz, wake survival %.2f" % (s["U"], s["f2"] / 1e3, s["fsh"], s["surv"]), fontsize=8.5)
    ax.set_xlabel("frequency (Hz)"); ax.grid(alpha=.3, which="both")
axs[0].set_ylabel("sheath current PSD S_I(f)  (A²/Hz)"); axs[0].legend(fontsize=6.8, loc="lower left")
axs[0].set_ylim(1e-18, 1e-2)
fig.suptitle("Fig M1 — FACT-based sheath modulation spectrum (frequencies cited; amplitudes m₂=1 %, m_sh=10 %, m_t=10 % are ASSUMPTIONS)\nnarrowband = Mack band (~20 % wide) and wake band; broadband = turbulence · " + TAG, fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(PL, "figM1_source_spectrum.png")); plt.close(fig)

# ---------- Fig M2: received spectrum vs noise (key plot) ----------
def spec_plot(pin, fname, title):
    s = M.setup(pin); p = s["p"]; A = M.ap_area(p["listen"], 1e6); eta = 10 ** p["log10_eta"]
    fs2 = np.logspace(0, 7, 1400)
    S = np.array([B.dbm(max(eta * eta * M.s1(s, x, A), 1e-300)) for x in fs2])
    N = np.array([B.dbm(M.noise_density(x, p)) for x in fs2])
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    fmin = B.c / (2 * math.pi * s["r"])
    ax.axvspan(1, fmin, color="#999", alpha=.18, label="near field (k·r < 1): far-field formula not valid")
    ax.semilogx(fs2, S, color="#1b9e77", lw=2, label="HYP SLW at η = %g (received power per Hz)" % eta)
    ax.axvspan(s["f2_lo"], s["f2_hi"], color="#33a02c", alpha=.18, label="(a) Mack 2nd-mode band (FACT frequency)")
    ax.axvspan(s["fsh_lo"], s["fsh_hi"], color="#ff7f00", alpha=.25, label="(c) wake oscillation band (FACT frequency)")
    ax.semilogx(fs2, N, color="k", lw=1.4, label="noise floor per Hz (shielded receiver; ITU-R P.372 quiet rural, extrapolated < 0.3 MHz)")
    tau = p["tau_s"]
    for lo, hi, col, lab in [(s["f2_lo"], s["f2_hi"], "#33a02c", "Mack band"), (s["fsh_lo"], s["fsh_hi"], "#ff7f00", "wake band")]:
        fm = math.sqrt(lo * hi)
        thr = B.dbm(M.noise_density(fm, p)) + 10 * math.log10(p["d_th"] / math.sqrt(max(tau, 1 / (hi - lo)) * (hi - lo)))
        ax.plot([lo, hi], [thr, thr], color=col, lw=3, ls="--")
        ax.text(hi * 1.1, thr, "detect line, %s\n(%g s averaging)" % (lab, tau), color=col, fontsize=7, va="center")
    ax.set_xlabel("frequency (Hz)"); ax.set_ylabel("dBm per Hz at the receiver")
    ax.set_ylim(min(N.min(), S.max()) - 80, max(N.max(), S.max()) + 15); ax.grid(alpha=.3, which="both")
    ax.legend(fontsize=7, loc="upper right")
    ax.set_title(title, fontsize=8.5)
    fig.tight_layout(); fig.savefig(os.path.join(PL, fname)); plt.close(fig)
    return s

spec_plot(dict(log10_eta=-3, r_km=100), "modulation_spectrum.png",
          "Fig M2 — received modulation spectrum vs noise: baseline (70 km, Mach 25, n_e 1e18, δ 1 cm, D 1 m), r = 100 km,\n75 m-class LF antenna (A = 7.2×10³ m²), 1 s averaging. SLW part is HYP: this page does not claim SLW emission strength.\n" + TAG)
spec_plot(dict(log10_eta=-3, r_km=100, h_km=45, mach=15, D_m=2.5), "figM2b_spectrum_M15_45km.png",
          "Fig M2b — as Fig M2 at Mach 15, 45 km, D 2.5 m\n" + TAG)

# ---------- Fig M3: chemistry time scales ----------
hs = np.linspace(30, 90, 61)
fig, axs = plt.subplots(1, 2, figsize=(12, 4.3))
ax = axs[0]
for T, ls in [(1000, ":"), (3000, "-"), (6000, "--")]:
    for ne, col in [(16, "#66a61e"), (18, "#1f78b4"), (20, "#e31a1c")]:
        ax.semilogy(hs, [1 / (M.alpha_dr(T) * 10 ** ne)] * len(hs), color=col, ls=ls, lw=1)
    ax.semilogy(hs, [1 / (M.k_att_o2(T) * (M.X_O2 * M.n_air(h)) ** 2 + M.k_att_n2(T) * M.X_O2 * M.X_N2 * M.n_air(h) ** 2) for h in hs], color="#6a3d9a", ls=ls, lw=2)
    ax.semilogy(hs, [1 / (M.k_det_o2(T) * M.X_O2 * M.n_air(h)) for h in hs], color="#b15928", ls=ls, lw=2)
ax.set_xlabel("altitude (km)"); ax.set_ylabel("time scale (s)")
ax.set_title("time scales: thin = recombination 1/(α n_e) for n_e 1e16/1e18/1e20 (green/blue/red);\nthick purple = 3-body attachment; thick brown = O₂⁻ detachment; line style = T 1000/3000/6000 K", fontsize=7.5)
ax.grid(alpha=.3, which="both")
ax = axs[1]
t = np.logspace(-7, -1, 300)
for ne, col in [(16, "#66a61e"), (18, "#1f78b4"), (20, "#e31a1c")]:
    for T, ls in [(1000, ":"), (3000, "-"), (6000, "--")]:
        ax.semilogx(t, 1 / (1 + M.alpha_dr(T) * 10 ** ne * t), color=col, ls=ls)
for U, D in [(3000, 1), (7400, 1), (7400, 5)]:
    ax.axvline(D / U, color="gray", lw=.8); ax.text(D / U, 1.02, "D/U\n%g m @ %g km/s" % (D, U / 1e3), fontsize=6.5, ha="center")
ax.set_xlabel("time after leaving the body t (s)"); ax.set_ylabel("electron survival n(t)/n₀ = 1/(1+α n₀ t)")
ax.set_ylim(0, 1.15); ax.grid(alpha=.3, which="both")
ax.set_title("recombination 'peel-off' envelope (FACT rate, Torr et al. 1977 NO⁺)", fontsize=8)
fig.suptitle("Fig M3 — wake plasma chemistry (FACT rates; freestream air density; T_e = T_gas ASSUMPTION) · " + TAG, fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(PL, "figM3_chemistry_timescales.png")); plt.close(fig)

# ---------- Fig M4: eta threshold vs dwell ----------
taus = np.logspace(-4, 3, 60)
fig, axs = plt.subplots(1, 2, figsize=(12, 4.3), sharey=True)
for ax, r in zip(axs, [10, 100]):
    series = {k: [] for k in ["r433", "r1296", "r1M", "rMack", "all"]}
    for tau in taus:
        o = M.model(dict(r_km=r, tau_s=tau))
        series["r433"].append(o["r433_eta"]); series["r1296"].append(o["r1296_eta"]); series["r1M"].append(o["r1M_eta"])
        series["rMack"].append(o["rMack_eta"]); series["all"].append(o["eta_all"])
    for k, col, lab in [("r433", "#e0a060", "433.92 MHz, hub antenna"), ("r1296", "#e07060", "1296 MHz, hub antenna"),
                        ("r1M", "#7ec8ff", "1 MHz, 75 m resonant (30 kHz RBW)"), ("rMack", "#33a02c", "Mack-band matched LF (λ²/4π at f₂)"),
                        ("all", "#1b9e77", "all-band Eckart, fixed 75 m-class antenna")]:
        ax.loglog(taus, series[k], color=col, lw=2, label=lab)
    o0 = M.model(dict(r_km=r, tau_s=1e-9))
    for k, col in [("r433", "#e0a060"), ("r1296", "#e07060"), ("r1M", "#7ec8ff")]:
        ax.plot([taus[0]], [o0[k + "_eta1"]], "o", color=col)
    ax.axhline(1, color="k", lw=1.5); ax.set_title("r = %d km (dots: v0.1 single-look values)" % r)
    ax.set_xlabel("dwell / integration time τ (s)"); ax.grid(alpha=.3, which="both")
axs[0].set_ylabel("minimum detectable η (d = 1)"); axs[0].legend(fontsize=7)
fig.suptitle("Fig M4 — integration gain: η_th ∝ τ^(-1/4) for noise-like signals (radiometer/Eckart); baseline sheath · " + TAG, fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(PL, "figM4_eta_vs_dwell.png")); plt.close(fig)

# ---------- Fig M5: conventional (FACT) fingerprint on carriers crossing the sheath ----------
nes = np.linspace(15, 20.5, 111)
fig, axs = plt.subplots(1, 2, figsize=(12, 4.3))
for fc, col, lab in [(433.92e6, "#e0a060", "433.92 MHz"), (1296e6, "#e07060", "1296 MHz"), (2.25e9, "#7570b3", "2.25 GHz (S-band telemetry)"), (10e9, "#1b9e77", "10 GHz (X-band radar)")]:
    a = [M.am_fingerprint(dict(M.setup(dict(log10_ne=x))["p"]), fc, 0.01) for x in nes]
    axs[0].semilogy(nes, [max(abs(z["dL_dB"]), 1e-6) for z in a], color=col, label=lab)
    axs[1].semilogy(nes, [max(abs(z["dphi_rad"]), 1e-8) for z in a], color=col, label=lab)
    axs[0].semilogy(nes, [max(z["L0_dB"], 1e-6) for z in a], color=col, ls=":", lw=1)
axs[0].set_xlabel("log₁₀ n_e (m⁻³)"); axs[0].set_ylabel("dB"); axs[0].set_title("solid: peak-to-peak AM swing for ±1 % n_e (Mack-band level)\ndotted: mean one-way loss (blackout when large)", fontsize=8)
axs[1].set_xlabel("log₁₀ n_e (m⁻³)"); axs[1].set_ylabel("rad"); axs[1].set_title("peak-to-peak phase swing for ±1 % n_e", fontsize=8)
for ax in axs: ax.grid(alpha=.3, which="both"); ax.legend(fontsize=7)
fig.suptitle("Fig M5 — FACT conventional fingerprint: any carrier crossing the sheath picks up AM/PM sidebands at f₂, f_sh (v0.1 Drude slab, 70 km, d 5 cm) · " + TAG, fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(PL, "figM5_conventional_fingerprint.png")); plt.close(fig)
print("done")
