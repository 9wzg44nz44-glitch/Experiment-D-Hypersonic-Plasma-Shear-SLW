# Candidate detectors: literature check (Experiment D, UI v0.3.1)

Fri 25 Sep 2026 (ET). The candidates are the Rydberg-atom vapor cell E-field sensor and the hydrogen 2S metastable "tickled de-excitation" (Stark/RF quench) detector, both approved by Dan.

Tags: **FACT** = stated in the cited primary source (or NIST data). **HYP** = hypothesis. **ASSUMPTION** = modelling choice. "Ours" = arithmetic done by us using only the cited formula.

Every "ours" number is recomputed in `sim/detectors_check.py`, which writes `sim/detectors_numbers.json`. The same script checks that all 32 numbers quoted on the page match; it currently reports 32/32. No purchases were made and nobody was contacted.

Source PDFs and text copies are kept in `/workspace/sim-lab/expt-d/detectors/sources/`: Lamb & Retherford 1950 and 1951, Parthey et al. 2011 (arXiv), and Landhuis et al. (arXiv).

## 0. Where the 1S–2S concept lives on the hub

- **`experiment-c.html`** (Experiment C, "Faraday-caged SLW/SW → atomic 1S–2S optical readout", v1 draft) holds the 1S–2S / forbidden S–S detector concept:
  - 243 nm and 121.6 nm photomultiplier (PMT) channels
  - a quench-control discriminator (a DC field mixes 2S and 2P)
  - a **"Detector bank (co-located at the atom end)"** table (`#det`). This is the hub's existing candidate-detector list.
- Other pages that point to it:
  - `index.html`: the Experiment C and F tabs. Experiment F, "Pure Scalar Wave + hydrogen forbidden transition", is a separate repo.
  - Strip links on `kit.html` and `experiment-c-cart.html`.
  - `future-scalar-ab.html`: Dan's note on the forbidden S-to-S transition in Chiao et al. 2023.
- `sw-vs-slw.html`, `c-nuclei.html`, `lab.html` and `library.html` mention related topics but hold no detector list.

## 1. Hydrogen 2S quench detector

| # | Claim / value | Label | Source |
|---|---|---|---|
| H1 | 1S–2S two-photon frequency 2 466 061 413 187 035(10) Hz (hyperfine centroid) | FACT | Parthey et al., PRL 107, 203001 (2011), doi:10.1103/PhysRevLett.107.203001 |
| H2 | Excitation light: 972 nm ECDL, frequency-doubled twice to 243 nm (13 mW); 5.8 K beam | FACT | Parthey 2011 |
| H3 | 2S detected by quenching in a 10 V/cm field; the 121 nm photons are counted by a PMT | FACT | Parthey 2011 |
| H4 | 2S two-photon (2E1) decay rate 8.2283 s⁻¹, so τ(2S) = 0.1215 s (a later calculation gives 8.2284 s⁻¹) | FACT | Klarsfeld, Phys. Lett. 30A, 382 (1969); Tung et al. |
| H5 | Natural 2S decay gives a two-photon **continuum**: the two photon energies share 10.2 eV | FACT | Klarsfeld 1969; Spitzer & Greenstein, ApJ 114, 407 (1951) |
| H6 | Induced decay 2S → 2P → 1S gives **one Lyman-α line**, 121.567 nm | FACT | NIST ASD H I (Kramida et al., doi:10.18434/T4W30F) |
| H7 | A(2P1/2 → 1S) = 6.2648×10⁸ s⁻¹, so τ(2P) = 1.60 ns and natural width γ/2π = 99.7 MHz | FACT (width is ours) | NIST ASD |
| H8 | Lamb shift 2S1/2–2P1/2 = 1057.8 MHz (NIST level energies give 1057.847 MHz; Hagley & Pipkin infer 1057.839(12) MHz) | FACT | NIST ASD levels; Hagley & Pipkin, PRL 72, 1172 (1994) |
| H9 | 2S1/2–2P3/2 = 9911.200(12) MHz (NIST levels give 9911.20 MHz) | FACT | Hagley & Pipkin 1994, doi:10.1103/PhysRevLett.72.1172 |
| H10 | r-f quench rate, Eq. (25): 1/τ = (2πe²S₀/cħ²)·\|(e·r)\|²·γ/[(ω−ω₀)² + (γ/2)²]. On resonance, Eq. (26): 1/τ = (8πe²S₀/cħ²γ)\|(e·r)\|². Eq. (27): \|(e·r)\|² = 3a₀². Static field, Eq. (42): 1/τ = (V²/ħ²)·γ/[ω² + (γ/2)²] with V = ⟨eE·r⟩. The E² scaling and Lorentzian off-resonance suppression follow directly | FACT | Lamb & Retherford, Phys. Rev. 79, 549 (1950), §6, §13, §16 and App. II (from Bethe) |
| H11 | β–e crossing (2S1/2 mJ = −½ with 2P1/2 mJ = +½) at **H = 540 G**, using their early Lamb-shift value of about 1000 Mc/s. Motional field E = (v/c)×H; quenching extends over a range of fields. The α–c crossing is at 4700 G | FACT | Lamb & Retherford 1950, §16 |
| H12 | Trapped 2S clouds of ≥5×10⁷ atoms; 10 V/cm quenches them "in a few microseconds"; overall Lyman-α detection efficiency ≈2×10⁻⁶ | FACT | Landhuis et al., arXiv:physics/0210019 (MIT; journal version not checked) |
| H13 | Hydrogen beam flux about 10¹⁷ atoms/s (ground state) in the 1S–2S apparatus | FACT | Parthey 2011 |

**The formula in SI units (ours, step by step):**
- Take a plane wave with peak amplitude E₀. Its average energy flux is S₀ = cE₀²/8π in Gaussian units, which equals E₀²/(2η₀) in SI.
- Substituting into Eq. (25) gives 1/τ = γ·V²/ħ² / [(ω−ω₀)² + γ²/4], with V = √3·e·a₀·E₀/2. The factor ½ comes from the rotating-wave form.
- On resonance this becomes 1/τ = 3(e·a₀·E₀/ħ)²/γ.
- For ω ≪ ω₀ both rotating terms count equally, giving 1/τ = γ(3e²a₀²E₀²/4ħ²)·[1/((ω₀−ω)² + γ²/4) + 1/((ω₀+ω)² + γ²/4)]. This is the time average of the static Eq. (42).

**Checks of the normalization (ours):**
- Lamb & Retherford's own example, S₀ = 3.4 mW/cm², gives τ = 1.26 µs. The paper quotes 1.25 µs.
- The static formula at 10 V/cm (2P1/2 and 2P3/2 paths) gives τ = 3.6 µs, consistent with "a few µs" (H12).

**Results (ours; constants CODATA 2018; γ from H7, frequencies from H8/H9):**

| Quantity | Value |
|---|---|
| 1 µV/m, resonant (1057.8 MHz), E₀ = peak amplitude | **3.10×10⁻¹¹ s⁻¹ per atom** |
| same, if 1 µV/m is the rms value | 6.19×10⁻¹¹ s⁻¹ |
| 1 µV/m at 241 kHz, B = 0, both rotating terms, 2P1/2 only | 1.37×10⁻¹³ s⁻¹ (−23.5 dB) |
| same, plus the 2P3/2 path (\|⟨z⟩\|² = 6a₀²) | **1.40×10⁻¹³ s⁻¹ (−23.4 dB)** |
| rotating-wave single term only (the approach behind Dan's estimate) | −26.5 dB |
| atoms held in 2S for 1 quench/s at 1 µV/m | 3×10¹⁰ (resonant); 7×10¹² (241 kHz) |

Dan's rough estimates were ~10⁻¹⁰ s⁻¹ and −27 dB. The 10⁻¹⁰ figure matches our formula without the ½ from the rotating-wave form (which would give 1.24×10⁻¹⁰). The −27 dB matches the single-term rotating-wave estimate (26.5 dB). The proper low-frequency answer is −23.4 dB.

**Level crossing (ours; hyperfine ignored, ASSUMPTION):**
- Method: diagonalise the 2P fine structure plus Zeeman terms (mJ = +½ block), using NIST 2P3/2–2P1/2 = 10969.05 MHz and gs = 2.00232.
- Result: **573.5 G** with L = 1057.8 MHz.
- Check: with L = 1000 MHz the same code gives 542 G, which reproduces Lamb & Retherford's 540 G.
- The "~575 G" value quoted to us agrees with this recomputation. **We did not find a primary source that states 575 G.** Lamb & Retherford Parts I and II give 540 G (Part I) and a figure for it (Part II, Fig. 34).
- Slope: 1.82 MHz/G. So 150 / 241 / 800 kHz splittings sit 0.08 / 0.13 / 0.44 G from the crossing.

**Can the crossing make 150–800 kHz resonant?** Only formally, for four reasons:
- The 2P linewidth is 99.7 MHz, so everything within about ±27 G of the crossing behaves as "resonant".
- At the crossing, a 241 kHz field perpendicular to B (needed for ΔmJ = +1) quenches at 6.19×10⁻¹¹ s⁻¹ for 1 µV/m (quasi-static average). The same holds for DC and anything up to tens of MHz: broadband, not tuned.
- The motional field v×B at 573.5 G is 52 mV/m for 100 µK hydrogen (1-D rms velocity) and 90 V/m at 300 K. This swamps 1 µV/m, as Lamb & Retherford (H11) note.
- Our inference (not checked in a source): the β state is a high-field seeker, so it cannot be held in a static magnetic trap. The MIT trapped metastables are F = 1, mF = 1 (H12).

**Signal signature:** induced decay gives one Lyman-α line (H6); natural decay gives the broad two-photon continuum (H5). A 121.6 nm bandpass filter (for example on a solar-blind PMT) separates the two, as the hub's Experiment C already proposes.

**What it can and cannot tell apart:**
- It is an **E-field detector**. Ordinary TEM at the same frequency quenches it too (FACT, H10).
- So SLW-vs-TEM discrimination still depends on the Faraday cage, and on the HYP that the SLW passes the wall.
- A pure SW (E = B = 0, HYP) has no E1 coupling. It could couple only through potentials, which is an untested HYP.

Beam fluxes, count rates and detector dark rates are not quoted beyond H12–H13. **Lyman-α detector dark rates were not verified.**

## 2. Rydberg vapor cell

| # | Claim / value | Label | Source |
|---|---|---|---|
| R1 | Atomic superhet: sensitivity 55 nV cm⁻¹ Hz⁻¹ᐟ², limited by laser frequency noise; minimum detectable field 780 pV cm⁻¹; phase and frequency detection. Earlier atomic electrometers reached "a few μV cm⁻¹ Hz⁻¹ᐟ²" | FACT | Jing et al., Nature Physics 16, 911 (2020), doi:10.1038/s41567-020-0918-5 |
| R2 | Vector microwave electrometry: arbitrary polarization measured at 0.5° resolution in a Rb vapor cell (Rydberg EIT, 14.233 GHz, 53D5/2–54P3/2) | FACT | Sedlacek, Schwettmann, Kübler, Shaffer, PRL 111, 063001 (2013), doi:10.1103/PhysRevLett.111.063001 |
| R3 | Low-frequency screening: alkali atoms adsorbed on the cell walls screen slow external fields. Estimated cut-off ≳10⁴ Hz for typical glass cells. A sapphire cell achieved a noise floor ≈0.34 (mV/m)/√Hz with a 3-dB low cut-off ≈770 Hz (11 mm³ active volume); about 2× dielectric shielding by the sapphire wall | FACT | Jau & Carter, Phys. Rev. Applied 13, 054034 (2020), doi:10.1103/PhysRevApplied.13.054034; arXiv:2002.04145 |
| R4 | Cs cell with built-in electrodes: 5.7 / 2.2 / 0.95 µV cm⁻¹ Hz⁻¹ᐟ² at 1 / 10 / 100 kHz; minimum fields 18.0 / 6.9 / 3.0 µV/cm; linear dynamic range >50 dB | FACT (preprint; journal status not verified) | Lei & Shi, arXiv:2405.04761 (2024) |
| R5 | Wall-integrated Si electrodes: DC fields reduced about 3× by surface charges; polarization-dependent microwave transmission into the cell | FACT | Ma, Viray, Anderson, Raithel, arXiv:2106.01968 |
| R6 | A plain all-glass cell contains no metal, so it can sit inside the cage with lasers brought in by fibre | ours (design note) | — |
| R7 | Commercial systems | **not verified** | — |

**Comparison with the sphere chain** (ours; E-field equivalent per √Hz using the page's isotropic aperture λ²/4π, an optimistic ASSUMPTION for a small sphere):

| Case | E-field equivalent per √Hz |
|---|---|
| Sphere chain at 241 kHz (ZFL-500LN+ → Airspy, NF 2.9 dB) | 4.9 pV/m |
| Quiet-rural outside noise at 241 kHz (ITU-R P.372, F_a = 71.3 dB, extrapolated below 0.3 MHz) | 13 nV/m |
| Same, leaked inside an SE 55 dB cage | 23 pV/m |
| Sphere chain at 1296 MHz (NF 0.4 dB) | 20 nV/m |

How far the best published Rydberg figures sit above these (field ratio in dB):
- 100 kHz figure (R4) vs the chain's own noise at 241 kHz: **146 dB** above.
- Same vs the leaked floor: **132 dB** above.
- Same vs unshielded outdoor noise: **77 dB** above.
- The 55 nV/cm/√Hz superhet (R1) vs the 1296 MHz chain: **49 dB** above.

**Direction test:** Hively's SLW far field is claimed to be longitudinal (HYP); TEM is transverse (FACT). R2 shows a vapor cell can measure the field's polarization direction, which makes the Rydberg cell a natural **SLW-vs-TEM direction test** for Experiments A/B, where fields from a nearby launcher are strong. It is not a vehicle-band detector.

## 3. Selection rules and longitudinal/scalar waves

| # | Statement | Label | Source |
|---|---|---|---|
| S1 | Single-photon J = 0 → J = 0 is forbidden (the photon has spin 1). Nuclear E0 decay goes by internal conversion or pair formation instead | FACT | Kibédi, Garnsworthy & Wood, Prog. Part. Nucl. Phys. 123, 103930 (2022), doi:10.1016/j.ppnp.2021.103930 |
| S2 | H 1S → 2S (S → S, same parity) is E1-forbidden; the lab drives it with two 243 nm photons | FACT | Parthey 2011; Klarsfeld 1969 |
| S3 | A helicity-0 longitudinal/scalar quantum, if one existed, carries no angular momentum and could in principle drive a monopole S → S step. The monopole overlap ⟨1s\|r²\|2s⟩ = −2.98 a₀² (non-zero) | **HYP: our inference, not from the sources**; the integral is ours | — |
| S4 | Hively: "Exemplary implementations may facilitate a 1S to 2S atomic transition (mS to nS transition in general)". Also: "High frequencies (> 1 THz) may correspond, for example, to atomic transitions from a 1S to a 2S orbital, which are forbidden by quantum mechanics on the basis of classical electrodynamics" | FACT that the patent says it; no mechanism, selection-rule argument or data given | US 9,306,527 B1 (text from the hub copy `papers/Hively-US9306527B1-Scalar-Longitudinal-Waves.pdf`; exact column/line numbers not pinned down from the two-column OCR) |
| S5 | Monstein & Wesley, EPL 59, 514 (2002): no discussion of atomic transitions (text search of the hub PDF) | FACT (absence, by search) | hub `papers/` |
| S6 | Hively & Loebl, Physics Essays 32, 112 (2019), and Hively & Land, JPCS (2021): no discussion of atomic transitions found (text search) | FACT (absence, by search) | hub `papers/` |
| S7 | Chiao et al., PRA 107, 042209 (2023): a scalar-potential (Aharonov–Bohm) effect inside a Faraday shell, read out by EIT; uses "a selection rule forbids S-wave to S-wave transitions". Different mechanism from SLW; disputed by Gao, PRA 111, 066203 (2025) and defended in the reply, PRA 111, 066204 | FACT | doi:10.1103/PhysRevA.107.042209 |

## 4. Not verified / open items

- **Source for "575 G":** not found. Our recomputation gives 573.5 G, and the 1950 paper gives 540 G with the old Lamb shift.
- **Hyperfine structure** was not included in the crossing or quench numbers.
- **Lei & Shi 2024** is a preprint; its journal status was not checked.
- **Commercial Rydberg systems:** specs and prices not verified.
- **Lyman-α detector dark rates:** not verified.
- **Landhuis et al.:** the journal version was not checked.
- **Bezginov et al. 2019** (Science) Lamb-shift value: not verified, because the search failed. The NIST level values and Hagley & Pipkin 1994 were used instead.
- **Patent column/line numbers** for the S4 quotes were not pinned down.
