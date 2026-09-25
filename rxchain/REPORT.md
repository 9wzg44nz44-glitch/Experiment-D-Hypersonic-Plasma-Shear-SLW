# Experiment D v0.3: Receiver chain tab. Report

Physics `expt-d-detect-v0.3`, UI v0.3.0, 25 Sep 2026 (ET). Page: https://9wzg44nz44-glitch.github.io/Experiment-D-Hypersonic-Plasma-Shear-SLW/slw-detectability.html (tab "Receiver chain").

## 1. What is being detected (read first)

- **The signal is the SLW (and its SW proxy), HYP**, picked up by the Hively-style receive sphere.
- **TEM is only background**: outside radio noise leaking through the Faraday cage, plus the receiver's own thermal noise (FACT).
- LNAs, a narrower bandwidth and longer averaging only lower the noise side of the ratio. They improve the SLW result only under the HYP that the sphere turns the SLW into a voltage at its terminals.
- The results table gives the smallest detectable **η (SLW)** and **η√κ_C (SW proxy, `etakap_th0_sw`)** for each receiver option. Ordinary-receiver/TEM numbers appear only in a labelled secondary table.

## 2. The Faraday cage, cables and self-noise

- **The receive sphere sits inside a Faraday cage.**
  - The cage does the TEM noise reduction, by its shielding effectiveness (SE). The SLW is assumed to pass the cage wall (HYP).
  - The SE control is labelled "Faraday cage shielding around the receive sphere (SE)".
  - When leaked TEM dominates, the tab says: "TEM noise leaking through the Faraday cage sets the floor; a better cage (solid sheet, bonded seams, no cables through the wall) helps more than more amps."
- **No cable crosses the cage wall.** Receive electronics inside run on battery. Data leaves over all-dielectric optical fibre through a waveguide-below-cutoff tube soldered 360° to the cage wall.
  - FACT: a circular tube of inner diameter d has TE11 cutoff f_c = 1.841·c/(π·d), about 176/d GHz with d in mm. Well below cutoff it attenuates about 32 dB per tube diameter of length (H. W. Ott, *Electromagnetic Compatibility Engineering*, Wiley 2009).
  - Noted only, not modelled.
- **Self-noise.** The electronics inside the cage make their own RF.
  - They sit in a separate small shielded box, away from the sphere.
  - Measure their self-noise with the sphere replaced by a 50 Ω load. That measured floor is the N_rx this tab predicts.

## 3. New equations (v0.3), with sources

| # | Tag | Equation | Source |
|---|---|---|---|
| R1 | FACT | Friis cascade: F_sys = F1 + (F2−1)/G1 + (F3−1)/(G1G2) + …; stage order [cable] → LNA1 → LNA2 → LNA3 → instrument | H. T. Friis, "Noise figures of radio receivers", Proc. IRE 32, 419 (1944), doi:10.1109/JRPROC.1944.232049 |
| R2 | FACT | N_rx = k_B·T0·B·F_sys, i.e. N_rx(dBm) = kT0B(dBm) + NF_sys | Friis 1944; Pozar, *Microwave Engineering* 4e, §10.1 |
| R3 | FACT | passive loss L at T0: F = L, G = 1/L (ASSUMPTION cable at 290 K) | Friis 1944; Pozar §10.1 |
| R4 | FACT | F_inst = N_inst/(k_B T0 B), with N_inst = quoted level + 10·log10(B/quoted bandwidth) | definition of noise factor (Friis 1944) + maker's quoted floors |
| R5 | FACT | floor on the SLW sphere: N = N_rx ⊕ (kT0B + F_a − SE) (⊕ = add powers); unshielded ordinary receiver (secondary only): N = N_rx ⊕ (kT0B + F_a) | v0.2 form; F_a from ITU-R P.372 |
| R6 | FACT | radiometer equation d = (S/N)·√(B·τ); used only in the Sheath modulation tab (its detector reduces to R6 in a flat band), so nothing is counted twice | R. H. Dicke, Rev. Sci. Instrum. 17, 268 (1946) |
| R7 | FACT | derived readouts: ideal-receiver headroom = N − [kT0B ⊕ leak] (F_sys → 1); more-gain headroom = N − [kT0B·F_front ⊕ leak] (F_front = R1 without the instrument term). Coded with log1p to avoid cancellation | derived from R1–R5 |
| (v0.1) | HYP | SW proxy P_SW = κ_C·½·P_SLW, so min η√κ_C = √2 × min η | unchanged v0.1 |

With no chain in front of the instrument, N_rx is the quoted instrument floor itself. So the default (TinySA alone) reproduces v0.2 bit for bit.

**Instrument presets (FACT, quoted from the maker):**
- TinySA Ultra: −102 dBm @ 30 kHz without LNA, and −145 dBm @ 200 Hz with LNA, both at 30 MHz (tinysa.org TinySA4 Specification). This gives NF 27.2 dB and 6.0 dB.
- Airspy HF+ Discovery: MDS −140.0 dBm @ 500 Hz at 15 MHz (airspy.com), which gives NF 7.0 dB.
- Keysight N9040B UXA, DANL spec with preamp on (data sheet 5992-0090EN p.9), in dBm/Hz: −152 (100–200 kHz), −155 (200–500 kHz), −159 (0.5–1 MHz), −161 (1–10 MHz), −165 (10 MHz–2.1 GHz), −163 (2.1–3.6 GHz). Below 100 kHz the preamp-off rows are used.
- Ideal (F = 1): a limit, not a product.

## 4. Results


Signal = SLW (and SW proxy), HYP, on the Hively-style receive sphere inside the Faraday cage. Floor = receiver-chain noise (+) outside TEM noise leaking through the cage (SE). 
Baseline: h 70 km, Mach 25, n_e 1e18 m^-3, r = 100 km, RBW 30 kHz, chi = 0. 241 kHz = Mack band, modulation tab matched filter, lambda^2/4pi antenna, tau = 1 s, d_th = 1. Other bands: main page single look (SNR 0 dB); 1 MHz lambda^2/4pi, UHF hub aperture.

### quiet_rural, Faraday cage SE 55 dB

| band | chain | NF_sys (dB) | floor (dBm / 30 kHz) | floor set by | min eta, SLW | min eta*sqrt(kappa), SW proxy | ideal-receiver headroom (dB) |
|---|---|---|---|---|---|---|---|
| 241 kHz (Mack, 1 s) | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -101.7 | your receiver | 1.18e-04 | 1.68e-04 | 11.2 |
| 241 kHz (Mack, 1 s) | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -112.4 | TEM leaking through cage | 3.47e-05 | 4.90e-05 | 0.5 |
| 241 kHz (Mack, 1 s) | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -112.7 | TEM leaking through cage | 3.31e-05 | 4.68e-05 | 0.1 |
| 241 kHz (Mack, 1 s) | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -112.8 | TEM leaking through cage | 3.31e-05 | 4.68e-05 | 0.1 |
| 241 kHz (Mack, 1 s) | (u) Keysight UXA N9040B, preamp on (reference) | 19.0 | -108.4 | your receiver | 5.50e-05 | 7.77e-05 | 4.5 |
| 241 kHz (Mack, 1 s) | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -112.8 | TEM leaking through cage | 3.27e-05 | 4.63e-05 | 0.0 |
| 1 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 0.0248 | 0.0351 | 24.8 |
| 1 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -120.8 | your receiver | 2.84e-03 | 4.01e-03 | 6.0 |
| 1 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -124.8 | your receiver | 1.80e-03 | 2.54e-03 | 2.0 |
| 1 MHz | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -124.9 | your receiver | 1.77e-03 | 2.51e-03 | 1.9 |
| 1 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 15.0 | -114.1 | your receiver | 6.13e-03 | 8.67e-03 | 12.7 |
| 1 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -126.8 | your receiver | 1.42e-03 | 2.01e-03 | 0.0 |
| 433.92 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 5.27e+03 | 7.46e+03 | 27.2 |
| 433.92 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 571 | 807 | 7.9 |
| 433.92 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 328 | 464 | 3.1 |
| 433.92 MHz | (d) ZX60-P33ULN+ -> TinySA Ultra (LNA on) | 0.5 | -128.7 | your receiver | 243 | 344 | 0.5 |
| 433.92 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 646 | 914 | 9.0 |
| 433.92 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 230 | 325 | 0.0 |
| 1296 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 1.31e+04 | 1.86e+04 | 27.2 |
| 1296 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 1.42e+03 | 2.01e+03 | 7.9 |
| 1296 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 817 | 1.16e+03 | 3.1 |
| 1296 MHz | (d) Kuhne MKU LNA 132 AH -> TinySA Ultra (LNA on) | 0.4 | -128.8 | your receiver | 600 | 848 | 0.4 |
| 1296 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 1.61e+03 | 2.28e+03 | 9.0 |
| 1296 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 572 | 810 | 0.0 |

### quiet_rural, Faraday cage SE 80 dB

| band | chain | NF_sys (dB) | floor (dBm / 30 kHz) | floor set by | min eta, SLW | min eta*sqrt(kappa), SW proxy | ideal-receiver headroom (dB) |
|---|---|---|---|---|---|---|---|
| 241 kHz (Mack, 1 s) | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 1.14e-04 | 1.61e-04 | 26.7 |
| 241 kHz (Mack, 1 s) | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.2 | your receiver | 1.25e-05 | 1.76e-05 | 7.4 |
| 241 kHz (Mack, 1 s) | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -125.8 | your receiver | 7.32e-06 | 1.04e-05 | 2.8 |
| 241 kHz (Mack, 1 s) | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -126.0 | your receiver | 7.20e-06 | 1.02e-05 | 2.7 |
| 241 kHz (Mack, 1 s) | (u) Keysight UXA N9040B, preamp on (reference) | 19.0 | -110.2 | your receiver | 4.42e-05 | 6.25e-05 | 18.4 |
| 241 kHz (Mack, 1 s) | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -128.7 | your receiver | 5.30e-06 | 7.49e-06 | 0.0 |
| 1 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 0.0248 | 0.035 | 27.2 |
| 1 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 2.68e-03 | 3.79e-03 | 7.9 |
| 1 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 1.54e-03 | 2.18e-03 | 3.1 |
| 1 MHz | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -126.3 | your receiver | 1.52e-03 | 2.14e-03 | 2.9 |
| 1 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 15.0 | -114.2 | your receiver | 6.06e-03 | 8.57e-03 | 15.0 |
| 1 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 1.08e-03 | 1.53e-03 | 0.0 |
| 433.92 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 5.27e+03 | 7.46e+03 | 27.2 |
| 433.92 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 571 | 807 | 7.9 |
| 433.92 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 328 | 464 | 3.1 |
| 433.92 MHz | (d) ZX60-P33ULN+ -> TinySA Ultra (LNA on) | 0.5 | -128.7 | your receiver | 243 | 344 | 0.5 |
| 433.92 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 646 | 914 | 9.0 |
| 433.92 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 230 | 325 | 0.0 |
| 1296 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 1.31e+04 | 1.86e+04 | 27.2 |
| 1296 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 1.42e+03 | 2.01e+03 | 7.9 |
| 1296 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 817 | 1.16e+03 | 3.1 |
| 1296 MHz | (d) Kuhne MKU LNA 132 AH -> TinySA Ultra (LNA on) | 0.4 | -128.8 | your receiver | 600 | 848 | 0.4 |
| 1296 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 1.61e+03 | 2.28e+03 | 9.0 |
| 1296 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 572 | 810 | 0.0 |

### residential, Faraday cage SE 55 dB

| band | chain | NF_sys (dB) | floor (dBm / 30 kHz) | floor set by | min eta, SLW | min eta*sqrt(kappa), SW proxy | ideal-receiver headroom (dB) |
|---|---|---|---|---|---|---|---|
| 241 kHz (Mack, 1 s) | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -93.9 | TEM leaking through cage | 2.91e-04 | 4.12e-04 | 0.7 |
| 241 kHz (Mack, 1 s) | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -94.6 | TEM leaking through cage | 2.68e-04 | 3.78e-04 | 0.0 |
| 241 kHz (Mack, 1 s) | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -94.6 | TEM leaking through cage | 2.67e-04 | 3.78e-04 | 0.0 |
| 241 kHz (Mack, 1 s) | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -94.6 | TEM leaking through cage | 2.67e-04 | 3.78e-04 | 0.0 |
| 241 kHz (Mack, 1 s) | (u) Keysight UXA N9040B, preamp on (reference) | 19.0 | -94.5 | TEM leaking through cage | 2.71e-04 | 3.83e-04 | 0.1 |
| 241 kHz (Mack, 1 s) | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -94.6 | TEM leaking through cage | 2.67e-04 | 3.78e-04 | 0.0 |
| 1 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -101.6 | your receiver | 0.0261 | 0.0369 | 10.1 |
| 1 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -111.3 | TEM leaking through cage | 8.54e-03 | 0.0121 | 0.4 |
| 1 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -111.5 | TEM leaking through cage | 8.25e-03 | 0.0117 | 0.1 |
| 1 MHz | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -111.6 | TEM leaking through cage | 8.24e-03 | 0.0117 | 0.1 |
| 1 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 15.0 | -109.8 | TEM leaking through cage | 0.0101 | 0.0143 | 1.9 |
| 1 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -111.6 | TEM leaking through cage | 8.18e-03 | 0.0116 | 0.0 |
| 433.92 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 5.27e+03 | 7.46e+03 | 27.2 |
| 433.92 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 571 | 807 | 7.9 |
| 433.92 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 328 | 464 | 3.1 |
| 433.92 MHz | (d) ZX60-P33ULN+ -> TinySA Ultra (LNA on) | 0.5 | -128.7 | your receiver | 243 | 344 | 0.5 |
| 433.92 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 646 | 914 | 9.0 |
| 433.92 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 230 | 325 | 0.0 |
| 1296 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 1.31e+04 | 1.86e+04 | 27.2 |
| 1296 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 1.42e+03 | 2.01e+03 | 7.9 |
| 1296 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 817 | 1.16e+03 | 3.1 |
| 1296 MHz | (d) Kuhne MKU LNA 132 AH -> TinySA Ultra (LNA on) | 0.4 | -128.8 | your receiver | 600 | 848 | 0.4 |
| 1296 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 1.61e+03 | 2.28e+03 | 9.0 |
| 1296 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 572 | 810 | 0.0 |

### residential, Faraday cage SE 80 dB

| band | chain | NF_sys (dB) | floor (dBm / 30 kHz) | floor set by | min eta, SLW | min eta*sqrt(kappa), SW proxy | ideal-receiver headroom (dB) |
|---|---|---|---|---|---|---|---|
| 241 kHz (Mack, 1 s) | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -101.9 | your receiver | 1.15e-04 | 1.62e-04 | 17.2 |
| 241 kHz (Mack, 1 s) | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -117.4 | TEM leaking through cage | 1.95e-05 | 2.76e-05 | 1.8 |
| 241 kHz (Mack, 1 s) | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -118.7 | TEM leaking through cage | 1.67e-05 | 2.36e-05 | 0.4 |
| 241 kHz (Mack, 1 s) | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -118.8 | TEM leaking through cage | 1.66e-05 | 2.35e-05 | 0.4 |
| 241 kHz (Mack, 1 s) | (u) Keysight UXA N9040B, preamp on (reference) | 19.0 | -109.8 | your receiver | 4.67e-05 | 6.60e-05 | 9.4 |
| 241 kHz (Mack, 1 s) | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -119.2 | TEM leaking through cage | 1.59e-05 | 2.24e-05 | 0.0 |
| 1 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 0.0248 | 0.035 | 26.5 |
| 1 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.2 | your receiver | 2.72e-03 | 3.85e-03 | 7.3 |
| 1 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -125.8 | your receiver | 1.61e-03 | 2.27e-03 | 2.7 |
| 1 MHz | (d) ZFL-500LN+ -> Airspy HF+ Discovery | 2.9 | -125.9 | your receiver | 1.58e-03 | 2.24e-03 | 2.6 |
| 1 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 15.0 | -114.2 | your receiver | 6.08e-03 | 8.59e-03 | 14.3 |
| 1 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -128.5 | your receiver | 1.17e-03 | 1.66e-03 | 0.0 |
| 433.92 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 5.27e+03 | 7.46e+03 | 27.2 |
| 433.92 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 571 | 807 | 7.9 |
| 433.92 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 328 | 464 | 3.1 |
| 433.92 MHz | (d) ZX60-P33ULN+ -> TinySA Ultra (LNA on) | 0.5 | -128.7 | your receiver | 243 | 344 | 0.5 |
| 433.92 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 646 | 914 | 9.0 |
| 433.92 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 230 | 325 | 0.0 |
| 1296 MHz | (a) TinySA Ultra alone (v0.2 default) | 27.2 | -102.0 | your receiver | 1.31e+04 | 1.86e+04 | 27.2 |
| 1296 MHz | (b) TinySA + 1 LNA 21 dB / 3 dB (PLACEHOLDER) | 7.9 | -121.3 | your receiver | 1.42e+03 | 2.01e+03 | 7.9 |
| 1296 MHz | (c) TinySA + 2 LNAs 21 dB / 3 dB (PLACEHOLDER) | 3.1 | -126.1 | your receiver | 817 | 1.16e+03 | 3.1 |
| 1296 MHz | (d) Kuhne MKU LNA 132 AH -> TinySA Ultra (LNA on) | 0.4 | -128.8 | your receiver | 600 | 848 | 0.4 |
| 1296 MHz | (u) Keysight UXA N9040B, preamp on (reference) | 9.0 | -120.2 | your receiver | 1.61e+03 | 2.28e+03 | 9.0 |
| 1296 MHz | (e) ideal receiver, NF 0 dB (bound) | 0.0 | -129.2 | your receiver | 572 | 810 | 0.0 |

### Secondary comparison (not the target): ordinary unshielded receiver, TEM from the same currents

| site | band | chain | ordinary-receiver floor (dBm) | classical TEM SNR (dB) |
|---|---|---|---|---|
| quiet_rural | 1 MHz | (a) | -75.6 | -113.7 |
| quiet_rural | 1 MHz | (d) | -75.6 | -113.7 |
| quiet_rural | 1 MHz | (e) | -75.6 | -113.7 |
| quiet_rural | 433.92 MHz | (a) | -102.0 | -194.0 |
| quiet_rural | 433.92 MHz | (d) | -128.7 | -167.3 |
| quiet_rural | 433.92 MHz | (e) | -129.2 | -166.8 |
| quiet_rural | 1296 MHz | (a) | -102.0 | -201.1 |
| quiet_rural | 1296 MHz | (d) | -128.8 | -174.3 |
| quiet_rural | 1296 MHz | (e) | -129.2 | -173.9 |
| residential | 1 MHz | (a) | -56.7 | -132.6 |
| residential | 1 MHz | (d) | -56.7 | -132.6 |
| residential | 1 MHz | (e) | -56.7 | -132.6 |
| residential | 433.92 MHz | (a) | -102.0 | -194.0 |
| residential | 433.92 MHz | (d) | -126.2 | -169.8 |
| residential | 433.92 MHz | (e) | -126.5 | -169.5 |
| residential | 1296 MHz | (a) | -102.0 | -201.1 |
| residential | 1296 MHz | (d) | -128.6 | -174.5 |
| residential | 1296 MHz | (e) | -129.0 | -174.1 |


Sanity checks against the brief: one placeholder LNA (21 dB / 3 dB) in front of the TinySA lowers the receiver floor by 19.3 dB at 1, 30, 433.92 and 1296 MHz. At 241 kHz (quiet rural, SE 55) it lowers it by only 10.7 dB, because leaked TEM takes over. Two LNAs lower it by about 24 dB.

**Bottom line.**
- At the Mack band (241 kHz, 1 s) one good LNA takes min η from 1.18e-4 to 3.3e-5. After that, TEM leaking through the cage sets the floor, so improving the cage (SE 55 → 80 dB) gives a further 4.6×, while more amplifiers give < 0.5 dB.
- At 433.92 and 1296 MHz the SLW HYP is not detectable with any receiver (min η 230 and 572 even with an ideal receiver).

## 5. Cross-checks

| Check | Values compared | Result | Worst relative error |
|---|---|---|---|
| v0.3 default reproduces v0.2 (JS engines vs origin/main v0.2) | 308,448 | all bit-identical | 0 |
| JS vs Python, receiver-chain grid (`grid_rx.json`, 10,800 points) | 583,201 | PASS / 0 FAIL | 1.35e-14 |
| JS vs Python, rx modulation grid (`grid_rxmod.json`, 80 points) | 19,041 | PASS / 0 FAIL | 2.15e-14 |
| Old main grid re-run at v0.3 | 124,417 | PASS / 0 FAIL | 2.3e-15 |
| Old modulation grid re-run at v0.3 | 205,633 | PASS / 0 FAIL | 2.4e-12 |
| Wolfram twin (`wolfram/ExptDDetect.wl` v0.3 + `ExptDRx_RunGrid.wl`) | not run | **pending**: no Wolfram kernel on the box; syntax lint OK | — |

Grid coverage:
- 5 instrument presets.
- 0 LNAs, or 1–3 LNAs at {21/3, 10/1, 30/6} dB. Stage k has G − 3(k−1) and NF + 0.5(k−1).
- Cable 0 or 2 dB.
- f = 241 kHz, 1 MHz, 30 MHz, 433.59 MHz, 433.92 MHz and 1296 MHz.
- Sites: quiet rural, residential, none.
- SE 0, 55 and 80 dB; RBW 30 kHz and 1 kHz.

## 6. Assumptions and limits

- **ASSUMPTION:** each instrument's spot noise figure is applied at every frequency. The TinySA figure is specified at 30 MHz and the Airspy figure at 15 MHz.
- **ASSUMPTION:** UXA DANL is taken at face value. Keysight notes true noise density ≈ DANL + 2.25 dB, so the UXA line is about 2 dB optimistic. At a table edge the worse value is used; the table is clamped outside 3 Hz–3.6 GHz.
- **ASSUMPTION:** cable at 290 K; LNA gain and NF flat with frequency.
- **ASSUMPTION:** ZFL-500LN+ NF 2.9 dB holds at 241 kHz (typical curves start at 53 MHz).
- **ASSUMPTION:** nearest datasheet points. ZX60-P33ULN+ uses its 400 MHz point for 433.92 MHz. At 1296 MHz the Kuhne MKU LNA 132 AH is used instead.
- **ASSUMPTION:** the brief's "433.59 MHz" is treated as the page's 433.92 MHz band; both are in the grid.
- **ASSUMPTION:** the unshielded conventional-receiver form counts kT0 once in F plus F_a (v0.2 form, kept for continuity).
- **ASSUMPTION:** the 241 kHz "floor set by" diagnosis is made at the band centre only. ITU-R P.372 F_a is extrapolated below 0.3 MHz.
- **Not modelled:** overload and intermodulation; the fibre/waveguide feedthrough; self-noise of electronics inside the cage; the Wolfram twin (written but not run).
- **Placeholders:** the generic LNA sliders (21 dB / 3 dB) are placeholders and are tagged as such on the page.
