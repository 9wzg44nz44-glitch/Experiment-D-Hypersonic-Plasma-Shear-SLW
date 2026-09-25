# Experiment D v0.3 receiver chain: key results (expt-d-detect-v0.3)

Signal = SLW (and SW proxy), HYP, on the Hively-style receive sphere inside the Faraday cage. Floor = receiver-chain noise (+) outside TEM noise leaking through the cage (SE). 
Baseline: h 70 km, Mach 25, n_e 1e18 m^-3, r = 100 km, RBW 30 kHz, chi = 0. 241 kHz = Mack band, modulation tab matched filter, lambda^2/4pi antenna, tau = 1 s, d_th = 1. Other bands: main page single look (SNR 0 dB); 1 MHz lambda^2/4pi, UHF hub aperture.

## quiet_rural, Faraday cage SE 55 dB

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

## quiet_rural, Faraday cage SE 80 dB

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

## residential, Faraday cage SE 55 dB

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

## residential, Faraday cage SE 80 dB

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

## Secondary comparison (not the target): ordinary unshielded receiver, TEM from the same currents

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
