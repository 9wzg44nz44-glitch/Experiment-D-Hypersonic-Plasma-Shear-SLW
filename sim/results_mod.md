# Experiment D v0.2 — minimum detectable η (deflection d ≥ 1, v0.1 convention)

v0.1 = single look in the 30 kHz RBW (no integration). v0.2 = same receiver plus integration over the dwell time (radiometer / Eckart detector).

## baseline (70 km, M25, n_e 1e18, delta 1 cm, D 1 m)

| range | receiver | v0.1 | v0.2, 1 s | v0.2, 100 s |
|---|---|---|---|---|
| 10 km | 433.92 MHz, Dan's small antenna (hub) | 5.3e+02 | 40 | 13 |
| 10 km | 1296 MHz, Dan's sleeve balun (hub) | 1.3e+03 | 1e+02 | 32 |
| 10 km | 1 MHz, 75 m resonant (lambda^2/4pi) | 0.0025 | 0.00019 | 6e-05 |
| 10 km | Mack-band matched LF (lambda^2/4pi at f2=241 kHz, 310 m quarter-wave) | — | 1.2e-05 | 3.7e-06 |
| 10 km | Shedding-band matched VLF (lambda^2/4pi at fsh=1486 Hz, 50 km quarter-wave; kr=0.31) | — | 1.9e-05 | 5.9e-06 |
| 10 km | All-band Eckart, fixed 75 m-class antenna (A=7.2e3 m^2), far field only | — | 3.1e-05 | 9.7e-06 |
| 10 km |   of which Mack band only (same antenna) | — | 4.9e-05 | 1.6e-05 |
| 10 km |   pure-tone bound for Mack power (NOT physical) | — | 8.8e-06 | 8.8e-07 |
| 100 km | 433.92 MHz, Dan's small antenna (hub) | 5.3e+03 | 4e+02 | 1.3e+02 |
| 100 km | 1296 MHz, Dan's sleeve balun (hub) | 1.3e+04 | 1e+03 | 3.2e+02 |
| 100 km | 1 MHz, 75 m resonant (lambda^2/4pi) | 0.025 | 0.0019 | 0.0006 |
| 100 km | Mack-band matched LF (lambda^2/4pi at f2=241 kHz, 310 m quarter-wave) | — | 0.00012 | 3.7e-05 |
| 100 km | Shedding-band matched VLF (lambda^2/4pi at fsh=1486 Hz, 50 km quarter-wave; kr=3.1) | — | 0.00019 | 5.9e-05 |
| 100 km | All-band Eckart, fixed 75 m-class antenna (A=7.2e3 m^2), far field only | — | 0.00031 | 9.7e-05 |
| 100 km |   of which Mack band only (same antenna) | — | 0.00049 | 0.00016 |
| 100 km |   pure-tone bound for Mack power (NOT physical) | — | 8.8e-05 | 8.8e-06 |

## representative (45 km, M15, n_e 1e18, delta 1 cm, D 2.5 m)

| range | receiver | v0.1 | v0.2, 1 s | v0.2, 100 s |
|---|---|---|---|---|
| 10 km | 433.92 MHz, Dan's small antenna (hub) | 2e+04 | 1.5e+03 | 4.7e+02 |
| 10 km | 1296 MHz, Dan's sleeve balun (hub) | 4.9e+04 | 3.7e+03 | 1.2e+03 |
| 10 km | 1 MHz, 75 m resonant (lambda^2/4pi) | 0.093 | 0.0071 | 0.0022 |
| 10 km | Mack-band matched LF (lambda^2/4pi at f2=158 kHz, 475 m quarter-wave) | — | 0.00026 | 8.1e-05 |
| 10 km | Shedding-band matched VLF (lambda^2/4pi at fsh=388 Hz, 193 km quarter-wave; kr=0.081) | — | 0.0029 | 0.00093 |
| 10 km | All-band Eckart, fixed 75 m-class antenna (A=7.2e3 m^2), far field only | — | 0.0011 | 0.00036 |
| 10 km |   of which Mack band only (same antenna) | — | 0.0016 | 0.00051 |
| 10 km |   pure-tone bound for Mack power (NOT physical) | — | 0.00036 | 3.6e-05 |
| 100 km | 433.92 MHz, Dan's small antenna (hub) | 2e+05 | 1.5e+04 | 4.7e+03 |
| 100 km | 1296 MHz, Dan's sleeve balun (hub) | 4.9e+05 | 3.7e+04 | 1.2e+04 |
| 100 km | 1 MHz, 75 m resonant (lambda^2/4pi) | 0.93 | 0.071 | 0.022 |
| 100 km | Mack-band matched LF (lambda^2/4pi at f2=158 kHz, 475 m quarter-wave) | — | 0.0026 | 0.00081 |
| 100 km | Shedding-band matched VLF (lambda^2/4pi at fsh=388 Hz, 193 km quarter-wave; kr=0.81) | — | 0.029 | 0.0093 |
| 100 km | All-band Eckart, fixed 75 m-class antenna (A=7.2e3 m^2), far field only | — | 0.011 | 0.0036 |
| 100 km |   of which Mack band only (same antenna) | — | 0.016 | 0.0051 |
| 100 km |   pure-tone bound for Mack power (NOT physical) | — | 0.0036 | 0.00036 |

## extreme n_e 1e20 (70 km, M25)

| range | receiver | v0.1 | v0.2, 1 s | v0.2, 100 s |
|---|---|---|---|---|
| 10 km | 433.92 MHz, Dan's small antenna (hub) | 5.3 | 0.4 | 0.13 |
| 10 km | 1296 MHz, Dan's sleeve balun (hub) | 13 | 1 | 0.32 |
| 10 km | 1 MHz, 75 m resonant (lambda^2/4pi) | 2.5e-05 | 1.9e-06 | 6e-07 |
| 10 km | Mack-band matched LF (lambda^2/4pi at f2=241 kHz, 310 m quarter-wave) | — | 1.2e-07 | 3.7e-08 |
| 10 km | Shedding-band matched VLF (lambda^2/4pi at fsh=1486 Hz, 50 km quarter-wave; kr=0.31) | — | 7.8e-07 | 2.5e-07 |
| 10 km | All-band Eckart, fixed 75 m-class antenna (A=7.2e3 m^2), far field only | — | 3.1e-07 | 9.7e-08 |
| 10 km |   of which Mack band only (same antenna) | — | 4.9e-07 | 1.6e-07 |
| 10 km |   pure-tone bound for Mack power (NOT physical) | — | 8.8e-08 | 8.8e-09 |
| 100 km | 433.92 MHz, Dan's small antenna (hub) | 53 | 4 | 1.3 |
| 100 km | 1296 MHz, Dan's sleeve balun (hub) | 1.3e+02 | 10 | 3.2 |
| 100 km | 1 MHz, 75 m resonant (lambda^2/4pi) | 0.00025 | 1.9e-05 | 6e-06 |
| 100 km | Mack-band matched LF (lambda^2/4pi at f2=241 kHz, 310 m quarter-wave) | — | 1.2e-06 | 3.7e-07 |
| 100 km | Shedding-band matched VLF (lambda^2/4pi at fsh=1486 Hz, 50 km quarter-wave; kr=3.1) | — | 7.8e-06 | 2.5e-06 |
| 100 km | All-band Eckart, fixed 75 m-class antenna (A=7.2e3 m^2), far field only | — | 3.1e-06 | 9.7e-07 |
| 100 km |   of which Mack band only (same antenna) | — | 4.9e-06 | 1.6e-06 |
| 100 km |   pure-tone bound for Mack power (NOT physical) | — | 8.8e-07 | 8.8e-08 |

## Modulation bands (FACT frequencies; U from Mach × USSA-1976 sound speed)

| Mach | h km | δ mm | D m | U m/s | f2 (C=0.65) kHz | f2 (C=0.9) kHz | f_sh (St 0.2) Hz | f_sh (St 0.45) Hz |
|---|---|---|---|---|---|---|---|---|
| 10 | 30 | 3 | 1 | 3017 | 327 | 453 | 603 | 1358 |
| 10 | 30 | 3 | 5 | 3017 | 327 | 453 | 121 | 272 |
| 10 | 30 | 10 | 1 | 3017 | 98 | 136 | 603 | 1358 |
| 10 | 30 | 10 | 5 | 3017 | 98 | 136 | 121 | 272 |
| 10 | 45 | 3 | 1 | 3235 | 350 | 485 | 647 | 1456 |
| 10 | 45 | 3 | 5 | 3235 | 350 | 485 | 129 | 291 |
| 10 | 45 | 10 | 1 | 3235 | 105 | 146 | 647 | 1456 |
| 10 | 45 | 10 | 5 | 3235 | 105 | 146 | 129 | 291 |
| 15 | 45 | 3 | 1 | 4852 | 526 | 728 | 970 | 2184 |
| 15 | 45 | 3 | 5 | 4852 | 526 | 728 | 194 | 437 |
| 15 | 45 | 10 | 1 | 4852 | 158 | 218 | 970 | 2184 |
| 15 | 45 | 10 | 5 | 4852 | 158 | 218 | 194 | 437 |
| 15 | 60 | 3 | 1 | 4711 | 510 | 707 | 942 | 2120 |
| 15 | 60 | 3 | 5 | 4711 | 510 | 707 | 188 | 424 |
| 15 | 60 | 10 | 1 | 4711 | 153 | 212 | 942 | 2120 |
| 15 | 60 | 10 | 5 | 4711 | 153 | 212 | 188 | 424 |
| 20 | 45 | 3 | 1 | 6470 | 701 | 970 | 1294 | 2911 |
| 20 | 45 | 3 | 5 | 6470 | 701 | 970 | 259 | 582 |
| 20 | 45 | 10 | 1 | 6470 | 210 | 291 | 1294 | 2911 |
| 20 | 45 | 10 | 5 | 6470 | 210 | 291 | 259 | 582 |
| 20 | 60 | 3 | 1 | 6281 | 680 | 942 | 1256 | 2827 |
| 20 | 60 | 3 | 5 | 6281 | 680 | 942 | 251 | 565 |
| 20 | 60 | 10 | 1 | 6281 | 204 | 283 | 1256 | 2827 |
| 20 | 60 | 10 | 5 | 6281 | 204 | 283 | 251 | 565 |
| 25 | 70 | 3 | 1 | 7428 | 805 | 1114 | 1486 | 3343 |
| 25 | 70 | 3 | 5 | 7428 | 805 | 1114 | 297 | 669 |
| 25 | 70 | 10 | 1 | 7428 | 241 | 334 | 1486 | 3343 |
| 25 | 70 | 10 | 5 | 7428 | 241 | 334 | 297 | 669 |

## Wake chemistry time scales (FACT rates; Mach 15, D = 1 m, shedding site 1 D behind base)

| h km | T K | n_e m⁻³ | α_DR m³/s | τ_DR = 1/(α n_e) | f_chem = 1/(2π τ_DR) | wake length U τ_DR | survival at t_s | ν_att s⁻¹ | ν_det s⁻¹ |
|---|---|---|---|---|---|---|---|---|---|
| 30 | 1000 | 1e16 | 1.51e-13 | 6.63e-04 s | 2.40e+02 Hz | 3 m | 0.75 | 1.50e+04 | 1.48e+05 |
| 30 | 1000 | 1e18 | 1.51e-13 | 6.63e-06 s | 2.40e+04 Hz | 0.03 m | 0.0291 | 1.50e+04 | 1.48e+05 |
| 30 | 1000 | 1e20 | 1.51e-13 | 6.63e-08 s | 2.40e+06 Hz | 0.0003 m | 0.0003 | 1.50e+04 | 1.48e+05 |
| 30 | 3000 | 1e16 | 5.93e-14 | 1.69e-03 s | 9.44e+01 Hz | 7.63 m | 0.884 | 7.39e+03 | 1.06e+07 |
| 30 | 3000 | 1e18 | 5.93e-14 | 1.69e-05 s | 9.44e+03 Hz | 0.0763 m | 0.0709 | 7.39e+03 | 1.06e+07 |
| 30 | 3000 | 1e20 | 5.93e-14 | 1.69e-07 s | 9.44e+05 Hz | 0.000763 m | 0.000762 | 7.39e+03 | 1.06e+07 |
| 30 | 6000 | 1e16 | 3.29e-14 | 3.04e-03 s | 5.24e+01 Hz | 13.8 m | 0.932 | 4.08e+03 | 3.81e+07 |
| 30 | 6000 | 1e18 | 3.29e-14 | 3.04e-05 s | 5.24e+03 Hz | 0.138 m | 0.121 | 4.08e+03 | 3.81e+07 |
| 30 | 6000 | 1e20 | 3.29e-14 | 3.04e-07 s | 5.24e+05 Hz | 0.00138 m | 0.00137 | 4.08e+03 | 3.81e+07 |
| 45 | 1000 | 1e16 | 1.51e-13 | 6.63e-04 s | 2.40e+02 Hz | 3.21 m | 0.763 | 1.82e+02 | 1.62e+04 |
| 45 | 1000 | 1e18 | 1.51e-13 | 6.63e-06 s | 2.40e+04 Hz | 0.0321 m | 0.0311 | 1.82e+02 | 1.62e+04 |
| 45 | 1000 | 1e20 | 1.51e-13 | 6.63e-08 s | 2.40e+06 Hz | 0.000321 m | 0.000321 | 1.82e+02 | 1.62e+04 |
| 45 | 3000 | 1e16 | 5.93e-14 | 1.69e-03 s | 9.44e+01 Hz | 8.18 m | 0.891 | 8.95e+01 | 1.17e+06 |
| 45 | 3000 | 1e18 | 5.93e-14 | 1.69e-05 s | 9.44e+03 Hz | 0.0818 m | 0.0756 | 8.95e+01 | 1.17e+06 |
| 45 | 3000 | 1e20 | 5.93e-14 | 1.69e-07 s | 9.44e+05 Hz | 0.000818 m | 0.000817 | 8.95e+01 | 1.17e+06 |
| 45 | 6000 | 1e16 | 3.29e-14 | 3.04e-03 s | 5.24e+01 Hz | 14.7 m | 0.936 | 4.94e+01 | 4.20e+06 |
| 45 | 6000 | 1e18 | 3.29e-14 | 3.04e-05 s | 5.24e+03 Hz | 0.147 m | 0.128 | 4.94e+01 | 4.20e+06 |
| 45 | 6000 | 1e20 | 3.29e-14 | 3.04e-07 s | 5.24e+05 Hz | 0.00147 m | 0.00147 | 4.94e+01 | 4.20e+06 |
| 60 | 1000 | 1e16 | 1.51e-13 | 6.63e-04 s | 2.40e+02 Hz | 3.12 m | 0.757 | 4.25e+00 | 2.48e+03 |
| 60 | 1000 | 1e18 | 1.51e-13 | 6.63e-06 s | 2.40e+04 Hz | 0.0312 m | 0.0303 | 4.25e+00 | 2.48e+03 |
| 60 | 1000 | 1e20 | 1.51e-13 | 6.63e-08 s | 2.40e+06 Hz | 0.000312 m | 0.000312 | 4.25e+00 | 2.48e+03 |
| 60 | 3000 | 1e16 | 5.93e-14 | 1.69e-03 s | 9.44e+01 Hz | 7.94 m | 0.888 | 2.09e+00 | 1.79e+05 |
| 60 | 3000 | 1e18 | 5.93e-14 | 1.69e-05 s | 9.44e+03 Hz | 0.0794 m | 0.0736 | 2.09e+00 | 1.79e+05 |
| 60 | 3000 | 1e20 | 5.93e-14 | 1.69e-07 s | 9.44e+05 Hz | 0.000794 m | 0.000793 | 2.09e+00 | 1.79e+05 |
| 60 | 6000 | 1e16 | 3.29e-14 | 3.04e-03 s | 5.24e+01 Hz | 14.3 m | 0.935 | 1.15e+00 | 6.41e+05 |
| 60 | 6000 | 1e18 | 3.29e-14 | 3.04e-05 s | 5.24e+03 Hz | 0.143 m | 0.125 | 1.15e+00 | 6.41e+05 |
| 60 | 6000 | 1e20 | 3.29e-14 | 3.04e-07 s | 5.24e+05 Hz | 0.00143 m | 0.00143 | 1.15e+00 | 6.41e+05 |
| 70 | 1000 | 1e16 | 1.51e-13 | 6.63e-04 s | 2.40e+02 Hz | 2.95 m | 0.747 | 3.04e-01 | 6.64e+02 |
| 70 | 1000 | 1e18 | 1.51e-13 | 6.63e-06 s | 2.40e+04 Hz | 0.0295 m | 0.0287 | 3.04e-01 | 6.64e+02 |
| 70 | 1000 | 1e20 | 1.51e-13 | 6.63e-08 s | 2.40e+06 Hz | 0.000295 m | 0.000295 | 3.04e-01 | 6.64e+02 |
| 70 | 3000 | 1e16 | 5.93e-14 | 1.69e-03 s | 9.44e+01 Hz | 7.51 m | 0.883 | 1.50e-01 | 4.78e+04 |
| 70 | 3000 | 1e18 | 5.93e-14 | 1.69e-05 s | 9.44e+03 Hz | 0.0751 m | 0.0699 | 1.50e-01 | 4.78e+04 |
| 70 | 3000 | 1e20 | 5.93e-14 | 1.69e-07 s | 9.44e+05 Hz | 0.000751 m | 0.000751 | 1.50e-01 | 4.78e+04 |
| 70 | 6000 | 1e16 | 3.29e-14 | 3.04e-03 s | 5.24e+01 Hz | 13.5 m | 0.931 | 8.26e-02 | 1.72e+05 |
| 70 | 6000 | 1e18 | 3.29e-14 | 3.04e-05 s | 5.24e+03 Hz | 0.135 m | 0.119 | 8.26e-02 | 1.72e+05 |
| 70 | 6000 | 1e20 | 3.29e-14 | 3.04e-07 s | 5.24e+05 Hz | 0.00135 m | 0.00135 | 8.26e-02 | 1.72e+05 |

Regression: v0.2 tuned receiver with bands off and single-shot integration reproduces v0.1 η_th0 on 2304 v0.1 grid points, worst rel 1.22e-15.
