# Experiment D receiver chain: verified gear shopping list (v0.3)

Compiled Fri 25 Sep 2026 (ET). **Nothing has been bought and nobody has been contacted.** Specs are quoted from the maker's datasheet or product page unless marked otherwise. Prices are the web prices seen on 25 Sep 2026, before tax and shipping unless stated; they change often. "Not published" means I looked and the maker does not state it.

**What this gear is for.** The target is the SLW (and the SW proxy), HYP, received by the Hively-style receive sphere **inside a Faraday cage**. An LNA, a narrower bandwidth or longer averaging only lowers the *noise* side. They help only under the HYP that the sphere turns the SLW into a voltage at its terminals. TEM is background only: outside noise leaking through the cage, plus the receiver's own thermal noise (FACT). When leaked TEM sets the floor, a better cage helps more than more amplifiers.

**Build rules** (see the tab's section 5):
- No cable crosses the cage wall. The receive electronics run on battery.
- Data leaves on all-dielectric optical fibre through a waveguide-below-cutoff tube, soldered 360° to the wall. FACT: TE11 cutoff f_c = 1.841c/(πd), about 176/d GHz with d in mm; well below cutoff the tube attenuates about 32 dB per tube diameter of length (Ott, *Electromagnetic Compatibility Engineering*, Wiley 2009).
- Put the LNA and receiver in their own small shielded box, away from the sphere.
- Measure their self-noise with the sphere replaced by a 50 Ω load.

## Recommendation (one good LNA per band; a 2nd LNA is rarely worth it)

| Band | Chain | NF_sys (model) | Parts cost | Min η, SLW (quiet rural, SE 55) | vs TinySA alone |
|---|---|---|---|---|---|
| 241 kHz (Mack) to 30 MHz | Mini-Circuits **ZFL-500LN+** → **Airspy HF+ Discovery** | 2.9 dB | $116.81 + $169 ≈ **$286** | 3.31e-5 (241 kHz, 1 s); 1.77e-3 (1 MHz) | 3.6× better at 241 kHz, 14× at 1 MHz |
| 433.92 MHz | Mini-Circuits **ZX60-P33ULN+** → TinySA Ultra (LNA on) | 0.5 dB | $152.68 (TinySA already in use) | 243 (not detectable, η > 1) | 22× |
| 1296 MHz | Kuhne **MKU LNA 132 AH** → TinySA Ultra (LNA on) | 0.4 dB | €259 incl. VAT (€217.65 net) | 600 (not detectable) | 22× |

Main conclusions:
- **241 kHz** is the only band where the SLW HYP is detectable at plausible η. With one LNA, the floor is set by TEM leaking through the cage (SE 55), not by the receiver. A second LNA buys < 0.5 dB there. Improving the cage from SE 55 to SE 80 buys 4.6× in η.
- **433.92 and 1296 MHz** are not detectable with any receiver, even an ideal NF 0 dB one (min η 230 and 572). The UHF LNAs are listed only so the chain can be tested end to end.
- **2nd and 3rd LNAs:** a second LNA (placeholder 21 dB / 3 dB) gains 4–5 dB at 1 MHz and UHF over one placeholder LNA. With a 0.4–0.5 dB first stage it gains < 0.5 dB. A third LNA gains almost nothing and raises overload risk.

## (a) Low-noise amplifiers (LNAs)

| Part | Range | Gain | NF | P1dB / OIP3 (output) | Supply | Price | Source |
|---|---|---|---|---|---|---|---|
| Mini-Circuits ZFL-500LN+ | 0.1–500 MHz | 24 dB min | 2.9 dB typ. **ASSUMPTION** it holds at 241 kHz: typical curves start at 53 MHz | +5 dBm / +14 dBm | 15 V, 60 mA | $116.81 | minicircuits.com datasheet ZFL-500LN+ |
| Mini-Circuits ZFL-1000LN+ | 0.1–1000 MHz | 20 dB min | 2.9 dB typ | +3 / +14 dBm | 15 V, 60 mA | $131.43 | minicircuits.com |
| Mini-Circuits ZX60-P33ULN+ | 0.4–3 GHz | 24.06 dB @ 400 MHz, 18.71 @ 900, 14.52 @ 1500 (typical data) | 0.43 dB @ 400 MHz, 0.38 @ 900, 0.46 @ 1500 | +17.3 / +30.3 dBm @ 400 MHz | 3 V, 56 mA | $152.68 | minicircuits.com datasheet + typical-performance table |
| Mini-Circuits ZX60-P103LN+ | 50–3000 MHz | 15.6 dB @ 1 GHz | 0.5 dB @ 1 GHz, 0.4 @ 500 MHz | P1dB 22.4 / OIP3 39.4 dBm | 5 V, 95 mA | $119.47 | minicircuits.com |
| Mini-Circuits ZX60-100VH+ | 0.3–100 MHz | 36 dB typ | 4 dB | OIP3 +43 dBm | 12 V, 320 mA (heavy on battery) | $325.35 | minicircuits.com |
| Mini-Circuits ZX60-33LN+ | 50–3000 MHz | see datasheet | 1.1 dB typ | see datasheet | | price not checked | minicircuits.com |
| Mini-Circuits ZFL-500HLN+ | 10–500 MHz | see datasheet | 3.8 dB | IP3 +30 dBm | | price not checked | minicircuits.com |
| Kuhne MKU LNA 132 AH (23 cm) | 1246–1346 MHz | 33 dB typ | 0.4 ± 0.05 dB (18 °C) | OIP3 +27 dBm; max input 1 mW | 9–15 V, 80 mA | €259 incl. VAT (€217.65 net) | kuhne-electronic.com |
| Kuhne MKU LNA 131 AH (23 cm) | 1246–1346 MHz | 20 dB | not captured | not captured | 15 mA | €309 SMA / €344 N | kuhne-electronic.com |
| **Zeenko ZK06-UM** | 10 MHz–6 GHz | 5 dB @ 100 kHz, 23.5 @ 5 MHz, 27 @ 10 MHz, 25.5 @ 100 MHz, 22.5 @ 1 GHz | 2.3 dB @ 10 MHz, 0.8 @ 100 MHz, 0.6 @ 1 GHz; **no NF published below 10 MHz** | OP1dB 18 dBm, OIP3 34 dBm @ 1 GHz | USB-C 5 V, 80 mA | $18–32 (resellers) | image-PDF datasheet from resellers (eleshop, Kamami, WITS, RunBit); zeenko.tech publishes no table |
| Zeenko ZK05-UM | 100 kHz–6 GHz | 28 dB @ 100 kHz | 1.9 dB @ 10 MHz; none published lower | not captured | USB-C | not captured | same reseller datasheet |

Notes:
- The Zeenko ZK06-UM has almost no gain at 241 kHz (5 dB at 100 kHz), so it is **not suitable for the Mack band**. It is a cheap, good option for 30–1300 MHz.
- USB-C 5 V is convenient on a battery pack inside the cage, but a USB supply line is a noise path. Keep the battery and the LNA inside the shielded electronics box.

## (b) Receivers and analysers

| Item | Range | Noise spec (maker) | Model NF | Other | Price | Source |
|---|---|---|---|---|---|---|
| TinySA Ultra (already in use; v0.2 default) | 100 kHz–800 MHz (6 GHz Ultra mode) | LDS −102 dBm @ 30 kHz RBW, 30 MHz, no LNA; −145 dBm @ 200 Hz with LNA; **internal LNA: "Built-in optional 20dB LNA with Noise Figure of 5dB up to 4GHz"** | 27.2 dB (LNA off); 6.0 dB (LNA on) | IIP3 +15 dBm, P1dB −1 dBm; battery ≥ 2 h | not rechecked | tinysa.org/wiki/pmwiki.php?n=TinySA4.Specification |
| Airspy HF+ Discovery | 0.5 kHz–31 MHz, 64–260 MHz | MDS −140.0 dBm @ 500 Hz, 15 MHz | 7.0 dB | IIP3 +15 dBm (HF); 110 dB BDR; 768 ksps IQ (660 kHz alias-free); +10 dBm max input | $169 (Itead, official US seller; airspy.com lists no price) | airspy.com/airspy-hf-discovery/ |
| SDRplay RSPdx-R2 | 1 kHz–2 GHz | NF 19 dB @ 300 kHz, 18 @ 2 MHz, 17 @ 12 MHz (typical) | not a preset | 14-bit ADC | $235 SRP | sdrplay.com (RSPdx-R2 datasheet / announcement) |
| Keysight N9040B UXA (reference only) | to 3.6 GHz used here | DANL, preamp on (1 Hz): −152 (100–200 kHz) … −165 dBm (10 MHz–2.1 GHz) | 15–19 dB at LF, 9 dB at UHF | lab instrument | not published | Keysight data sheet 5992-0090EN p.9 |

With a good LNA in front, the Airspy's own noise hardly matters: NF_sys is 2.9 dB with the ZFL-500LN+. So the Airspy is chosen for its LF coverage, its IQ recording (needed for the matched filter in the Sheath modulation tab) and its linearity, not for its NF.

## (c) Test gear and reference antennas (not receivers for the SLW)

| Item | What it's for | Key specs | Price | Source |
|---|---|---|---|---|
| LibreVNA | measuring cage SE, cable loss, LNA gain (Experiments A/B) | 100 kHz–6 GHz; IFBW 10 Hz–50 kHz; dynamic range 60 dB < 1 MHz, 80 dB 1–5 MHz, 85–105 dB (S21) 5–2940 MHz | not published by the project | github.com/jankae/LibreVNA spec sheet |
| NanoRFE VNA6000-A | same; **Dan already owns one** | not re-verified | owned | |
| Bonito MegActiv MA305FT | outside-noise reference channel *outside* the cage | 9 kHz–300 MHz; gain 3 dB nominal; IP3 > +30 dBm @ 7 MHz; IP2 > +50 dBm; 5–15 V, typ 10 mA; **NF not published** | not captured | bonito.net |
| Wellbrook ALA1530LNP | (same role) | 50 kHz–30 MHz; NF ≈ 0.2 dB; OIP3 +55 dBm | **treat as unavailable**: the maker reportedly ceased operations | wellbrook.uk.com (archived) |
| 50 Ω terminations (SMA) | self-noise test: replace the sphere with a load | | cheap; price not checked | |

Active antennas are TEM E-field antennas. They are useful only for logging outside noise alongside the caged sphere, so a "signal" that also appears on them can be rejected. They are **not** a substitute for the sphere inside the cage.

## Not verified / gaps
- Below 53 MHz the ZFL-500LN+ NF is taken from its single typical spec value (no curve).
- No Zeenko NF is published below 10 MHz. The ZK05-UM spec is partial.
- Not captured: TinySA Ultra current price, Bonito price, and the prices of the ZX60-33LN+ and ZFL-500HLN+.
- LibreVNA has no official price.
- The NanoRFE VNA6000-A specs were not re-verified.
- The Kuhne MKU LNA 131 AH NF was not captured.
- Wellbrook availability comes from secondary reports.
- UXA price is not published.
