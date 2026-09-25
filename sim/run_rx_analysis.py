"""python3 run_rx_analysis.py -> results_rx.md + results_rx.json : v0.3 receiver-chain key results (Python reference engines).
Baseline flight/plasma defaults (h 70 km, Mach 25, n_e 1e18, 100 km, RBW 30 kHz, chi 0).  241 kHz = Mack band, modulation tab
(matched filter, lambda^2/4pi antenna, tau 1 s, d_th 1); other bands = main page single look (SNR 0 dB).
SW proxy: P_SW = kappa * eta^2 * P_SLW(eta=1)/2 (v0.1 HYP relation), so eta*sqrt(kappa)_th = sqrt(2) * eta_th in every detector."""
import json, math
import expt_d_model as X
import expt_d_mod as M

PLACE = dict(lna1_G_dB=21, lna1_NF_dB=3, lna2_G_dB=21, lna2_NF_dB=3)
# verified datasheet values (see rxchain/SHOPPING_LIST.md)
ZFL500 = dict(lna1_G_dB=24, lna1_NF_dB=2.9)      # Mini-Circuits ZFL-500LN+: 0.1-500 MHz, gain 24 dB min, NF 2.9 dB typ
P33ULN = dict(lna1_G_dB=24.06, lna1_NF_dB=0.43)  # Mini-Circuits ZX60-P33ULN+: typical data at 400 MHz
MKU132 = dict(lna1_G_dB=33, lna1_NF_dB=0.4)      # Kuhne MKU LNA 132 AH: 1246-1346 MHz, 33 dB typ, NF 0.4 dB @18 C


def best(band):
    if band in ("241k", "1M"):
        return dict(rx_preset="airspy_hfd", n_lna=1, **ZFL500), "ZFL-500LN+ -> Airspy HF+ Discovery"
    if band == "433":
        return dict(rx_preset="tinysa_lna", n_lna=1, **P33ULN), "ZX60-P33ULN+ -> TinySA Ultra (LNA on)"
    return dict(rx_preset="tinysa_lna", n_lna=1, **MKU132), "Kuhne MKU LNA 132 AH -> TinySA Ultra (LNA on)"


CHAINS = [("a", "TinySA Ultra alone (v0.2 default)", lambda b: dict(rx_preset="tinysa", n_lna=0)),
          ("b", "TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER)", lambda b: dict(rx_preset="tinysa", n_lna=1, **PLACE)),
          ("c", "TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER)", lambda b: dict(rx_preset="tinysa", n_lna=2, **PLACE)),
          ("d", "best verified real chain", lambda b: best(b)[0]),
          ("u", "Keysight UXA N9040B, preamp on (reference)", lambda b: dict(rx_preset="uxa_preamp", n_lna=0)),
          ("e", "ideal receiver, NF 0 dB (bound)", lambda b: dict(rx_preset="ideal", n_lna=0))]
BANDS = [("241k", None), ("1M", 1e6), ("433", 433.92e6), ("1296", 1296e6)]
rows = []
for site in ("quiet_rural", "residential"):
    for se in (55, 80):
        for bk, f in BANDS:
            for key, name, fn in CHAINS:
                ch = fn(bk)
                p = dict(noise_env=site, SE_dB=se, **ch)
                if f is None:
                    s = M.setup(p)
                    o = M.model(p)
                    f2 = o["f2"]
                    pq = s["p"]
                    N = M.noise_density(f2, pq) * pq["rbw"]
                    q = X.model(dict(pq, f_rx=f2, aperture="recip"))  # chain diagnostics at f2 (same noise terms)
                    eta = o["rMack_eta"]
                    rows.append(dict(site=site, SE=se, band="241 kHz (Mack, 1 s)", f=f2, chain=key, chain_name=name if key != "d" else best(bk)[1],
                                     floor_dBm=10 * math.log10(N / 1e-3), NFsys=q["NFsys_dB"], eta_slw=eta, etak_sw=math.sqrt(2) * eta,
                                     dom=q["rx_dom"], head_ideal=q["head_ideal_dB"], Nconv=q["Nconv_dBm"], snr_tem=None))
                else:
                    q = X.model(dict(p, f_rx=f, aperture="recip" if f <= 1e6 else "hub"))
                    rows.append(dict(site=site, SE=se, band={"1M": "1 MHz", "433": "433.92 MHz", "1296": "1296 MHz"}[bk], f=f, chain=key,
                                     chain_name=name if key != "d" else best(bk)[1], floor_dBm=q["Nhiv_dBm"], NFsys=q["NFsys_dB"],
                                     eta_slw=q["eta_th0"], etak_sw=q["etakap_th0_sw"], dom=q["rx_dom"], head_ideal=q["head_ideal_dB"],
                                     Nconv=q["Nconv_dBm"], snr_tem=q["SNR_tem_dB"]))
json.dump(dict(version=X.VERSION, rows=rows), open("results_rx.json", "w"), indent=1)


def g(x):
    return "%.2e" % x if (x < 0.01 or x >= 1e4) else "%.3g" % x


L = ["# Experiment D v0.3 receiver chain: key results (" + X.VERSION + ")", "",
     "Signal = SLW (and SW proxy), HYP, on the Hively-style receive sphere inside the Faraday cage. Floor = receiver-chain noise (+) outside TEM noise leaking through the cage (SE). ",
     "Baseline: h 70 km, Mach 25, n_e 1e18 m^-3, r = 100 km, RBW 30 kHz, chi = 0. 241 kHz = Mack band, modulation tab matched filter, lambda^2/4pi antenna, tau = 1 s, d_th = 1. Other bands: main page single look (SNR 0 dB); 1 MHz lambda^2/4pi, UHF hub aperture.", ""]
for site in ("quiet_rural", "residential"):
    for se in (55, 80):
        L += ["## %s, Faraday cage SE %d dB" % (site, se), "",
              "| band | chain | NF_sys (dB) | floor (dBm / 30 kHz) | floor set by | min eta, SLW | min eta*sqrt(kappa), SW proxy | ideal-receiver headroom (dB) |",
              "|---|---|---|---|---|---|---|---|"]
        for r in rows:
            if r["site"] == site and r["SE"] == se:
                L.append("| %s | (%s) %s | %.1f | %.1f | %s | %s | %s | %.1f |" % (r["band"], r["chain"], r["chain_name"], r["NFsys"], r["floor_dBm"],
                         "your receiver" if r["dom"] == "receiver" else "TEM leaking through cage", g(r["eta_slw"]), g(r["etak_sw"]), r["head_ideal"]))
        L.append("")
L += ["## Secondary comparison (not the target): ordinary unshielded receiver, TEM from the same currents", "",
      "| site | band | chain | ordinary-receiver floor (dBm) | classical TEM SNR (dB) |", "|---|---|---|---|---|"]
for r in rows:
    if r["SE"] == 55 and r["snr_tem"] is not None and r["chain"] in ("a", "d", "e"):
        L.append("| %s | %s | (%s) | %.1f | %.1f |" % (r["site"], r["band"], r["chain"], r["Nconv"], r["snr_tem"]))
open("results_rx.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[:40]))
