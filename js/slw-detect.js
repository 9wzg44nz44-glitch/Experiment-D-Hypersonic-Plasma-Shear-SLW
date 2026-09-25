/* Experiment D — SLW/SW detectability engine (expt-d-detect-v0.2; v0.1 formulas unchanged, v0.2 adds js/slw-modulation.js)
 * Pure functions, no DOM. Used by slw-detectability.html and by node (cross-check vs Python/WL).
 * Labels: FACT = published/standard physics (cited); HYP = Hively EED (as printed in the cited papers / hub ledger);
 *         ASSUMPTION = modelling choice made here; SWEEP = unknown coupling, never given a single value.
 * Mirrors: /workspace/sim-lab/expt-d/expt_d_model.py (Python reference) and wolfram/ExptDDetect.wl (Mathematica twin).
 */
(function (root) {
  "use strict";
  const VERSION = "expt-d-detect-v0.2";
  // FACT: CODATA 2018 exact / recommended values
  const K = {
    c: 299792458,
    mu0: 1.25663706212e-6,
    eps0: 8.8541878128e-12,
    qe: 1.602176634e-19,
    me: 9.1093837015e-31,
    kB: 1.380649e-23,
    T0: 290,
  };
  K.Z0 = K.mu0 * K.c; // 376.730313668 ohm
  // FACT: US Standard Atmosphere 1976 (NOAA/NASA/USAF, NASA-TM-X-74335) mass density kg/m^3 and sound speed m/s
  const USSA_H = [30, 40, 50, 60, 70, 80, 90];
  const USSA_RHO = [1.8410e-2, 3.9957e-3, 1.0269e-3, 3.0968e-4, 8.2829e-5, 1.8458e-5, 3.416e-6];
  const USSA_A = [301.71, 317.19, 329.80, 314.07, 297.14, 282.54, 274.10];
  // FACT: Grantham, NASA TN D-6062 (1970) p.12: nu = 2.51e9 s^-1 typical at 150 000 ft (45.72 km), stations 2-4 (RAM C-II flow field)
  const NU_REF = 2.51e9, H_REF = 45.72;
  // FACT: ITU-R P.372 Table 1, Fam = c - d log10(f_MHz), valid 0.3-250 MHz (outside: extrapolated = ASSUMPTION)
  const NOISE_ENV = { none: null, quiet_rural: [53.6, 28.6], rural: [67.2, 27.7], residential: [72.5, 27.7], city: [76.8, 27.7] };
  // HYP carry-over: hub SleeveBalunSNR receive convention (A_EFF = pi*0.05^2, ETA = 0.5), js/sleeve-balun-snr.js
  const HUB_AEFF = Math.PI * 0.05 * 0.05, HUB_ETA = 0.5;

  function interp(xs, ys, x, logy) {
    const n = xs.length;
    let i = 0;
    if (x <= xs[0]) i = 0; else if (x >= xs[n - 1]) i = n - 2; else { while (x > xs[i + 1]) i++; }
    const t = (x - xs[i]) / (xs[i + 1] - xs[i]);
    if (logy) return Math.exp(Math.log(ys[i]) + t * (Math.log(ys[i + 1]) - Math.log(ys[i])));
    return ys[i] + t * (ys[i + 1] - ys[i]);
  }
  function rhoAir(hkm) { return interp(USSA_H, USSA_RHO, hkm, true); }
  function soundSpeed(hkm) { return interp(USSA_H, USSA_A, hkm, false); }
  // numerically stable principal sqrt of (a + i b), b >= 0 -> Im >= 0
  function csqrt(a, b) {
    const r = Math.hypot(a, b);
    if (a >= 0) { const re = Math.sqrt((r + a) / 2); return [re, re > 0 ? b / (2 * re) : 0]; }
    const im = Math.sqrt((r - a) / 2); return [b / (2 * im), im];
  }
  function dbm(W) { return 10 * Math.log10(W / 1e-3); }
  function sumDbm(a, b) { return 10 * Math.log10(Math.pow(10, a / 10) + Math.pow(10, b / 10)); }

  const DEFAULTS = {
    h_km: 70, mach: 25, log10_ne: 18, nu_scale: 1, log10_S: 6, delta_m: 0.01, B_uT: 50, theta_deg: 90,
    mech: "vxB", Te_K: 6000, f_close: 1, m_t: 0.1, A_s: 1, d_sh: 0.05,
    f_rx: 30e6, rbw: 30e3, aperture: "hub", SE_dB: 55, noise_env: "quiet_rural",
    log10_eta: -3, chi: 0, log10_kappa: 0, r_km: 100,
  };

  function model(pin) {
    const p = Object.assign({}, DEFAULTS, pin || {});
    const o = { version: VERSION };
    // ---- FACT side: flow + sheath ----
    const a = soundSpeed(p.h_km);
    const U = p.mach * a;                                   // m/s
    const ne = Math.pow(10, p.log10_ne);                    // m^-3
    const wp = Math.sqrt(ne * K.qe * K.qe / (K.eps0 * K.me)); // FACT plasma frequency
    const fp = wp / (2 * Math.PI);                          // = 8.98 sqrt(ne) Hz (NRL Plasma Formulary)
    const nu = p.nu_scale * NU_REF * rhoAir(p.h_km) / rhoAir(H_REF); // FACT anchor x ASSUMPTION nu ∝ rho
    const sigma = ne * K.qe * K.qe / (K.me * nu);          // FACT Drude DC conductivity (S/m)
    const S = Math.pow(10, p.log10_S);                     // shear rate du/dy (s^-1)
    const du = Math.min(S * p.delta_m, U);                  // ASSUMPTION: velocity jump across layer, capped at U
    const B = p.B_uT * 1e-6;
    const De = K.kB * p.Te_K / (K.me * nu);                 // FACT electron diffusivity
    let J;
    if (p.mech === "diff") J = p.f_close * K.qe * De * ne / p.delta_m;          // unbalanced e- diffusion (upper bound)
    else J = p.f_close * sigma * du * B * Math.sin(p.theta_deg * Math.PI / 180); // Ohm's law, motional du x B (upper bound)
    const Nc = p.A_s / (p.delta_m * p.delta_m);            // ASSUMPTION correlation cells, l_c = delta
    const Isrc = p.m_t * J * p.delta_m * Math.sqrt(p.A_s); // rms, random-phase sum of Nc cells
    const fc = S / (2 * Math.PI);                           // ASSUMPTION eddy frequency
    const g = p.f_rx <= fc ? 1 : Math.pow(p.f_rx / fc, -5 / 3); // FACT-form Kolmogorov -5/3 + Taylor (applicability ASSUMPTION)
    const Fspec = Math.min(1, p.rbw * g / (2.5 * fc));
    const Iband = Isrc * Math.sqrt(Fspec);
    const Ipk = Math.SQRT2 * Iband;                          // ASSUMPTION equivalent-sinusoid peak
    // sheath at f_rx (FACT Drude slab, e^{-i w t})
    const w = 2 * Math.PI * p.f_rx;
    const den = w * w + nu * nu;
    const er = 1 - wp * wp / den, ei = wp * wp * nu / (w * den);
    const n = csqrt(er, ei);
    const k0 = w / K.c;
    const alpha = k0 * n[1];                                // Np/m
    const Ash_dB = 8.685889638065035 * alpha * p.d_sh;       // one-way attenuation, dB
    const Tint = 4 * n[0] / ((n[0] + 1) * (n[0] + 1) + n[1] * n[1]); // 1-|Gamma|^2 (normal incidence)
    const Tint_dB = 10 * Math.log10(Tint);
    const lam = K.c / p.f_rx;
    const r = p.r_km * 1e3;
    // ---- receiver + noise (FACT) ----
    const Arx = p.aperture === "recip" ? lam * lam / (4 * Math.PI) : HUB_AEFF * HUB_ETA; // HYP carry-over / HYP reciprocity
    const Atem = 1.5 * lam * lam / (4 * Math.PI);           // FACT short dipole, Balanis
    const Nts = -102 + 10 * Math.log10(p.rbw / 30e3);        // FACT tinysa.org TinySA4 spec, no LNA
    const kT0B = dbm(K.kB * K.T0 * p.rbw);
    const env = NOISE_ENV[p.noise_env];
    const fMHz = p.f_rx / 1e6;
    const Fa = env ? env[0] - env[1] * Math.log10(fMHz) : -Infinity;
    const Next_conv = env ? kT0B + Fa : -Infinity;
    const Nconv = env ? sumDbm(Nts, Next_conv) : Nts;          // conventional (TEM) receiver
    const Nhiv = env ? sumDbm(Nts, Next_conv - p.SE_dB) : Nts;  // Hively RX with Faraday/sleeve TEM rejection SE
    // ---- HYP: SLW (Hively & Loebl 2019 Eq. B5; US 9,306,527 Eq. 15) ----
    const eta = Math.pow(10, p.log10_eta), kappa = Math.pow(10, p.log10_kappa);
    const Sslw1 = K.Z0 * Ipk * Ipk / Math.pow(4 * Math.PI * r, 2);  // W/m^2 at eta = 1
    const slwLoss_dB = p.chi * Ash_dB;                       // SWEEP chi: 0 (HL2019 App. A) ... 1 (hub Joule reading)
    const Pslw1 = Sslw1 * Arx * Math.pow(10, -slwLoss_dB / 10);
    const Pslw = eta * eta * Pslw1;
    const Cpk = K.mu0 * eta * Ipk / (4 * Math.PI * r);       // ledger box C = -mu0 (d_t rho + div J), T (=V s/m^2)
    const ELpk = K.Z0 * Cpk / K.mu0;                         // HL2019 Eq. 37 far field |E_r| = Z0 |C/mu0|
    // ---- HYP: SW proxy (E = B = 0, Ohmic-off) ----
    const Ssw1 = 0.5 * K.Z0 * Ipk * Ipk / Math.pow(4 * Math.PI * r, 2); // c C^2/(2 mu0) at eta = 1
    const Psw = kappa * eta * eta * Ssw1 * Arx;
    // ---- FACT-form classical TEM from the same fluctuating currents ----
    const IcellPk = Math.SQRT2 * p.m_t * J * p.delta_m * p.delta_m * Math.sqrt(Fspec);
    const PtemEmit = Nc * K.Z0 * (Math.PI / 3) * Math.pow(IcellPk * p.delta_m / lam, 2); // Balanis 4-16, incoherent
    const Ptem_dBm = dbm(PtemEmit * Atem / (4 * Math.PI * r * r)) + Tint_dB - Ash_dB;
    const PtemHiv_dBm = Ptem_dBm - p.SE_dB;
    const Tb = p.Te_K * Tint;                                // FACT Kirchhoff, optically thick slab
    const Pth_dBm = dbm(K.kB * Tb * p.rbw * 1.5 * p.A_s / (4 * Math.PI * r * r));
    // ---- outputs ----
    const Pslw_dBm = dbm(Pslw), Psw_dBm = dbm(Psw), Pslw1_dBm = dbm(Pslw1), Psw1_dBm = dbm(Ssw1 * Arx);
    const NhivW = Math.pow(10, Nhiv / 10) * 1e-3;
    Object.assign(o, {
      a_ms: a, U_ms: U, fp_Hz: fp, nu_s: nu, sigma_Sm: sigma, du_ms: du, De_m2s: De, J_Am2: J, Nc: Nc,
      Isrc_A: Isrc, fc_Hz: fc, Fspec: Fspec, Iband_A: Iband, eps_r: er, eps_i: ei, n_re: n[0], n_im: n[1],
      alpha_Npm: alpha, Ash_dB: Ash_dB, Tint_dB: Tint_dB, Arx_m2: Arx, Atem_m2: Atem,
      Nts_dBm: Nts, Fa_dB: env ? Fa : null, Nconv_dBm: Nconv, Nhiv_dBm: Nhiv,
      Pslw1_dBm: Pslw1_dBm, Pslw_dBm: Pslw_dBm, SNR_slw_dB: Pslw_dBm - Nhiv,
      Cpk_T: Cpk, ELpk_Vm: ELpk,
      Psw1_dBm: Psw1_dBm, Psw_dBm: Psw_dBm, SNR_sw_dB: Psw_dBm - Nhiv,
      Ptem_dBm: Ptem_dBm, SNR_tem_dB: Ptem_dBm - Nconv, PtemHiv_dBm: PtemHiv_dBm,
      Tb_K: Tb, Pth_dBm: Pth_dBm, SNR_th_dB: Pth_dBm - Nconv,
      eta_th0: Math.sqrt(NhivW / Pslw1), eta_th10: Math.sqrt(10 * NhivW / Pslw1),
      etakap_th0_sw: Math.sqrt(NhivW / (Ssw1 * Arx)),
      rmax_km: p.r_km * Math.sqrt(Pslw / NhivW),
      kr: 2 * Math.PI * r / lam,
    });
    return o;
  }

  const api = { VERSION, K, DEFAULTS, model, rhoAir, soundSpeed, csqrt, NOISE_ENV };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ExptDDetect = api;
})(typeof window !== "undefined" ? window : globalThis);
