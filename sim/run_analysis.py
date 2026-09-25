"""Experiment D detectability analysis (expt-d-detect-v0.1): plots + results tables.
Run:  source /workspace/sim-lab/env.sh && python run_analysis.py
"""
import csv, json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import expt_d_model as M

OUT = os.path.dirname(os.path.abspath(__file__))
PL = os.path.join(OUT, "plots")
os.makedirs(PL, exist_ok=True)
FR = [(1e6, "1 MHz"), (30e6, "30 MHz"), (433.92e6, "433.92 MHz"), (1296e6, "1296 MHz")]
NE = [16, 18, 20]
R = np.logspace(0, 3, 121)
BASE = dict(M.DEFAULTS)
plt.rcParams.update({"figure.dpi": 110, "font.size": 9})
TAG = "expt-d-detect-v0.1 · FACT sheath + HYP (Hively EED) SLW/SW · not flight data"


def m(**kw):
    p = dict(BASE); p.update(kw); return M.model(p)

# ---------- fig1: received power vs range ----------
fig, axs = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
for i, (f, fl) in enumerate([(1e6, "1 MHz"), (433.92e6, "433.92 MHz")]):
    for j, ap in enumerate(["hub", "recip"]):
        ax = axs[i][j]
        for le, ls in [(0, "-"), (-1, "--"), (-2, "-."), (-3, ":")]:
            ax.semilogx(R, [m(f_rx=f, aperture=ap, r_km=r, log10_eta=le)["Pslw_dBm"] for r in R], ls, color="#1b9e77",
                        label=f"HYP SLW, η=1e{le}" if le else "HYP SLW, η=1")
        ax.semilogx(R, [m(f_rx=f, aperture=ap, r_km=r, log10_eta=0, log10_kappa=0)["Psw_dBm"] for r in R], color="#7570b3",
                    label="HYP SW proxy, η=1, κ_C=1")
        ax.semilogx(R, [m(f_rx=f, r_km=r)["Ptem_dBm"] for r in R], color="#d95f02", label="FACT-form TEM from same currents (conv. dipole)")
        ax.semilogx(R, [m(f_rx=f, r_km=r)["Pth_dBm"] for r in R], color="#e7298a", label="FACT sheath thermal emission (conv. dipole)")
        q = m(f_rx=f, aperture=ap)
        ax.axhline(q["Nhiv_dBm"], color="k", lw=1.2, label=f"floor, Hively RX (TinySA + ext·10^(-SE/10)) {q['Nhiv_dBm']:.1f} dBm")
        ax.axhline(q["Nconv_dBm"], color="gray", lw=1, ls="--", label=f"floor, conventional RX {q['Nconv_dBm']:.1f} dBm")
        ax.set_ylim(-320, -40); ax.grid(alpha=.3)
        ax.set_title(f"f_rx = {fl}, SLW aperture = {'hub π(5 cm)²×0.5' if ap=='hub' else 'reciprocal λ²/4π'}")
        if i == 1: ax.set_xlabel("range r (km)")
        if j == 0: ax.set_ylabel("received power in 30 kHz RBW (dBm)")
axs[0][0].legend(fontsize=6.5, loc="lower left")
fig.suptitle("Fig 1 — received power vs range, baseline (70 km, M25, n_e=1e18 m⁻³, S=1e6 s⁻¹, δ=1 cm, vxB upper bound)\n" + TAG, fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(PL, "fig1_power_vs_range.png")); plt.close(fig)

# ---------- fig2: eta threshold vs range ----------
fig, axs = plt.subplots(1, 4, figsize=(14, 4.2), sharey=True)
cols = {16: "#66a61e", 18: "#1f78b4", 20: "#e31a1c"}
for k, (f, fl) in enumerate(FR):
    ax = axs[k]
    for ne in NE:
        for ap, ls in [("hub", "-"), ("recip", "--")]:
            ax.loglog(R, [m(f_rx=f, aperture=ap, r_km=r, log10_ne=ne)["eta_th0"] for r in R], ls, color=cols[ne],
                      label=f"n_e=1e{ne}, {ap}")
    ax.axhline(1, color="k", lw=1.5); ax.text(0.98, 0.03, "black line: η = 1\n(sheath as SLW-efficient as\nHively's own balun antenna)", fontsize=6.5, transform=ax.transAxes, ha="right", va="bottom", bbox=dict(fc="w", ec="none", alpha=.8))
    ax.set_title(f"f_rx = {fl}"); ax.set_xlabel("range r (km)"); ax.grid(alpha=.3, which="both")
axs[0].set_ylabel("η needed for SNR = 0 dB (TinySA, 30 kHz)"); axs[0].legend(fontsize=6.5)
fig.suptitle("Fig 2 — HYP SLW: minimum SLW-active fraction η vs range (solid: hub aperture, dashed: reciprocal λ²/4π); below the black line = detectable for some η ≤ 1\n" + TAG, fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(PL, "fig2_eta_threshold_vs_range.png")); plt.close(fig)

# ---------- fig3: heatmap eta_th vs n_e and shear ----------
lne = np.linspace(14, 20, 61); lS = np.linspace(4, 8, 41)
fig, axs = plt.subplots(1, 3, figsize=(14, 4.2))
for ax, (f, ap, ttl) in zip(axs, [(1e6, "recip", "1 MHz, reciprocal aperture"), (30e6, "hub", "30 MHz, hub aperture"), (433.92e6, "hub", "433.92 MHz, hub aperture")]):
    Z = np.array([[math.log10(m(f_rx=f, aperture=ap, log10_ne=a, log10_S=b)["eta_th0"]) for a in lne] for b in lS])
    im = ax.pcolormesh(lne, lS, Z, shading="auto", cmap="viridis_r", vmin=-6, vmax=6)
    cs = ax.contour(lne, lS, Z, levels=[0], colors="w", linewidths=2)
    ax.clabel(cs, fmt={0: "η=1"}, fontsize=7)
    if Z.min() > 0:
        ax.text(0.5, 0.5, f"η_th > 1 everywhere\n(min η_th = {10**Z.min():.2g})", transform=ax.transAxes, ha="center", color="w", fontsize=9, weight="bold")
    ax.set_title(ttl + ", r = 100 km"); ax.set_xlabel("log10 n_e (m⁻³)"); ax.set_ylabel("log10 shear rate S (s⁻¹)")
    fig.colorbar(im, ax=ax, label="log10 η_th (SNR=0 dB)")
fig.suptitle("Fig 3 — HYP SLW threshold η over n_e × shear (δ = 1 cm, Δu = min(Sδ, U)); white contour η = 1\n" + TAG, fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(PL, "fig3_eta_threshold_ne_shear.png")); plt.close(fig)

# ---------- fig4: FACT sheath blackout ----------
F = np.logspace(5, 11, 300)
fig, axs = plt.subplots(1, 2, figsize=(11, 4))
for ne in [16, 17, 18, 19, 20]:
    A = [m(f_rx=f, log10_ne=ne)["Ash_dB"] for f in F]
    T = [m(f_rx=f, log10_ne=ne)["Tint_dB"] for f in F]
    l, = axs[0].loglog(F, np.maximum(A, 1e-3), label=f"n_e=1e{ne} m⁻³ (f_p={8.98*math.sqrt(10**ne)/1e9:.2f} GHz)")
    axs[1].semilogx(F, T, color=l.get_color())
for ax in axs:
    ax.axvline(433.92e6, color="gray", ls=":"); ax.axvline(1296e6, color="gray", ls=":"); ax.axvline(30e6, color="gray", ls=":"); ax.grid(alpha=.3, which="both")
    ax.set_xlabel("frequency (Hz)")
axs[0].set_ylabel("Drude slab attenuation over d = 5 cm (dB)"); axs[0].legend(fontsize=7)
axs[1].set_ylabel("interface power transmission 1-|Γ|² (dB)")
fig.suptitle(f"Fig 4 — FACT: collisional-plasma (Drude/Appleton) sheath loss at 70 km (ν = {m()['nu_s']:.2e} s⁻¹, Grantham-anchored) — classical blackout picture\n" + TAG, fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(PL, "fig4_sheath_blackout.png")); plt.close(fig)

# ---------- fig5: spectral fraction ----------
fig, ax = plt.subplots(figsize=(6.5, 4))
for s in [4, 5, 6, 7, 8]:
    ax.loglog(F, [m(f_rx=f, log10_S=s)["Fspec"] for f in F], label=f"S = 1e{s} s⁻¹ (f_c = {10**s/2/math.pi:.3g} Hz)")
ax.set_xlabel("receiver frequency f_rx (Hz)"); ax.set_ylabel("fraction of fluctuation power in 30 kHz RBW")
ax.grid(alpha=.3, which="both"); ax.legend(fontsize=7)
ax.set_title("Fig 5 — ASSUMPTION: flat to f_c = S/2π, then Kolmogorov f^-5/3 (optimistic: no dissipation cutoff)", fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(PL, "fig5_spectral_fraction.png")); plt.close(fig)

# ---------- fig6: tornado (FACT-side uncertainties) at a reference case ----------
REF = dict(f_rx=1e6, aperture="recip")
ref = m(**REF)["eta_th0"]
knobs = [("log10_ne", 16, 20, "n_e 1e16…1e20 m⁻³"), ("nu_scale", 0.1, 10, "ν ×0.1…×10"), ("log10_S", 4, 8, "shear 1e4…1e8 s⁻¹"),
         ("delta_m", 0.001, 0.1, "δ 1 mm…10 cm"), ("B_uT", 25, 65, "B 25…65 µT"), ("m_t", 0.01, 0.5, "δn/n 0.01…0.5"),
         ("A_s", 0.1, 10, "sheet area 0.1…10 m²"), ("f_close", 1e-3, 1, "J closure 1e-3…1"), ("mach", 10, 25, "Mach 10…25"),
         ("chi", 0, 1, "χ SLW sheath loss 0…1")]
rows = []
for key, lo, hi, lab in knobs:
    a = math.log10(m(**REF, **{key: lo})["eta_th0"] / ref); b = math.log10(m(**REF, **{key: hi})["eta_th0"] / ref)
    rows.append((lab, a, b))
rows.sort(key=lambda t: max(abs(t[1]), abs(t[2])))
fig, ax = plt.subplots(figsize=(7.5, 4.5))
for i, (lab, a, b) in enumerate(rows):
    ax.barh(i, a, color="#1f78b4"); ax.barh(i, b, color="#e31a1c", alpha=.7)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=7.5)
ax.axvline(0, color="k"); ax.set_xlabel(f"Δ log10 η_th vs reference (η_th,ref = {ref:.3g}); blue = low end, red = high end")
ax.set_title("Fig 6 — sensitivity of the η threshold (1 MHz, reciprocal aperture, 100 km, n_e=1e18)", fontsize=8)
ax.grid(alpha=.3, axis="x"); fig.tight_layout(); fig.savefig(os.path.join(PL, "fig6_sensitivity_tornado.png")); plt.close(fig)
tornado = [dict(knob=l, dlog_lo=a, dlog_hi=b) for l, a, b in rows]

# ---------- results tables ----------
res = []
for mech in ["vxB", "diff"]:
    for ne in NE:
        for f, fl in FR:
            for ap in ["hub", "recip"]:
                row = dict(mech=mech, log10_ne=ne, f_rx_MHz=f / 1e6, aperture=ap)
                for r in [10, 100, 1000]:
                    q = m(mech=mech, log10_ne=ne, f_rx=f, aperture=ap, r_km=r)
                    row[f"eta_th0_r{r}"] = q["eta_th0"]
                    row[f"Pslw1_dBm_r{r}"] = q["Pslw1_dBm"]
                q = m(mech=mech, log10_ne=ne, f_rx=f, aperture=ap, r_km=100)
                row.update(J_Am2=q["J_Am2"], Isrc_A=q["Isrc_A"], Fspec=q["Fspec"], fp_GHz=q["fp_Hz"] / 1e9, Ash_dB=q["Ash_dB"],
                           Nhiv_dBm=q["Nhiv_dBm"], Nconv_dBm=q["Nconv_dBm"], SNR_tem_dB_r100=q["SNR_tem_dB"], SNR_th_dB_r100=q["SNR_th_dB"],
                           etakap_sw_r100=q["etakap_th0_sw"])
                res.append(row)
with open(os.path.join(OUT, "results_table.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(res[0].keys())); w.writeheader(); [w.writerow(r) for r in res]

def g(x):
    return f"{x:.2g}" if x < 1e4 else f"{x:.1e}"
lines = ["| J mech | n_e (m⁻³) | f_rx | aperture | η_th @10 km | η_th @100 km | η_th @1000 km | P_SLW(η=1) @100 km (dBm) | floor (dBm) | TEM SNR @100 km | thermal SNR @100 km |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
for r in res:
    lines.append(f"| {r['mech']} | 1e{r['log10_ne']} | {r['f_rx_MHz']:g} MHz | {r['aperture']} | {g(r['eta_th0_r10'])} | **{g(r['eta_th0_r100'])}** | {g(r['eta_th0_r1000'])} | "
                 f"{r['Pslw1_dBm_r100']:.1f} | {r['Nhiv_dBm']:.1f} | {r['SNR_tem_dB_r100']:.0f} dB | {r['SNR_th_dB_r100']:.0f} dB |")
open(os.path.join(OUT, "results_table.md"), "w").write("\n".join(lines) + "\n")

# shear sweep table (fixed delta and fixed du)
sh = ["| S (s⁻¹) | δ | Δu (m/s) | J (A/m²) | f_c (Hz) | η_th 1 MHz recip | η_th 30 MHz hub | η_th 433.92 MHz hub |", "|---|---|---|---|---|---|---|---|"]
for s in [4, 5, 6, 7, 8]:
    for d in [0.01, 0.001]:
        q1 = m(log10_S=s, delta_m=d, f_rx=1e6, aperture="recip"); q2 = m(log10_S=s, delta_m=d); q3 = m(log10_S=s, delta_m=d, f_rx=433.92e6)
        sh.append(f"| 1e{s} | {d*100:g} cm | {q1['du_ms']:.3g} | {q1['J_Am2']:.3g} | {q1['fc_Hz']:.3g} | {g(q1['eta_th0'])} | {g(q2['eta_th0'])} | {g(q3['eta_th0'])} |")
open(os.path.join(OUT, "shear_table.md"), "w").write("\n".join(sh) + "\n")
json.dump(dict(version=M.VERSION, baseline=m(), tornado=tornado, ref_eta=ref), open(os.path.join(OUT, "analysis_summary.json"), "w"), indent=1, default=str)
print("done", len(res))
