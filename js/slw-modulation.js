/* Experiment D v0.2 — "Sheath modulation" engine (expt-d-detect-v0.2)
 * Pure functions, no DOM. Needs js/slw-detect.js (the unchanged v0.1 engine) loaded first (browser) or require()d (node).
 * Mirrors sim/expt_d_mod.py (Python reference) and the ExptDMod section of wolfram/ExptDDetect.wl formula-for-formula.
 * Labels: FACT = published physics (cited on the page); HYP = Hively EED as printed; ASSUMPTION = modelling choice (slider);
 *         SWEEP = unknown coupling, never a single value.
 */
(function (root) {
  "use strict";
  const X = (typeof module !== "undefined" && module.exports) ? require("./slw-detect.js") : root.ExptDDetect;
  const VERSION = "expt-d-detect-v0.2";
  const K = X.K;
  const AMU = 1.66053906660e-27, M_AIR = 28.9644 * AMU;          // FACT USSA-1976 mean molecular mass
  const X_O2 = 0.209476, X_N2 = 0.780840;                          // FACT USSA-1976 volume fractions
  const NU_REF = 2.51e9, H_REF = 45.72;                            // FACT Grantham TN D-6062 (as v0.1)
  const DB_PER_NP2 = 8.685889638065035;
  const HUB_A = Math.PI * 0.05 * 0.05 * 0.5;                       // HYP carry-over hub convention (as v0.1)
  const A_LF75 = K.c * K.c / (4 * Math.PI * 1e6 * 1e6);            // v0.1 1 MHz resonant antenna, lambda^2/4pi at 1 MHz
  const MOD_DEFAULTS = {
    C_mack: 0.65, b2: 0.2, m2: 0.01, D_m: 1.0, St: 0.2, bsh: 0.2, msh: 0.1,
    Tw_K: 3000, xs_D: 1.0, tau_s: 1.0, d_th: 1.0, listen: "lf75",
  };
  const NQ_BAND = 200, NQ_ALL = 1200, F_ALL = [1.0, 1e7];
  const AM_F = [433.92e6, 1296e6, 2.25e9, 10e9];

  // ---- FACT chemistry (SI) ----
  const alphaDR = (T) => 4.2e-13 * Math.pow(T / 300.0, -0.85);                       // Torr, St-Maurice & Torr 1977, NO+
  const kAttO2 = (T) => 1.4e-41 * (300.0 / T) * Math.exp(-600.0 / T);                // Kossyi 1992 R45 (Te = Tg)
  const kAttN2 = (T) => 1.07e-43 * Math.pow(300.0 / T, 2) * Math.exp(-70.0 / T);     // Kossyi 1992 R46 (Te = Tg)
  const kDetO2 = (T) => 2.7e-16 * Math.pow(T / 300.0, 0.5) * Math.exp(-5590.0 / T);  // Kossyi 1992 R57
  const nAir = (h) => X.rhoAir(h) / M_AIR;
  const dbm = (W) => 10 * Math.log10(W / 1e-3);
  const sumDbm = (a, b) => 10 * Math.log10(Math.pow(10, a / 10) + Math.pow(10, b / 10));

  function sheathLoss(f, p) { // v0.1 Drude slab at frequency f -> [A_sh dB, Tint linear, Re n]
    const ne = Math.pow(10, p.log10_ne);
    const wp = Math.sqrt(ne * K.qe * K.qe / (K.eps0 * K.me));
    const nu = p.nu_scale * NU_REF * X.rhoAir(p.h_km) / X.rhoAir(H_REF);
    const w = 2 * Math.PI * f, den = w * w + nu * nu;
    const er = 1 - wp * wp / den, ei = wp * wp * nu / (w * den);
    const n = X.csqrt(er, ei);
    const A = DB_PER_NP2 * (w / K.c) * n[1] * p.d_sh;
    const T = 4 * n[0] / (Math.pow(n[0] + 1, 2) + Math.pow(n[1], 2));
    return [A, T, n[0]];
  }
  function noiseDensity(f, p) { // v0.1 shielded-receiver floor / RBW, W/Hz
    const Nts = -102 + 10 * Math.log10(p.rbw / 30e3);
    const env = X.NOISE_ENV[p.noise_env];
    let N;
    if (env) { const kT0B = dbm(K.kB * K.T0 * p.rbw); const Fa = env[0] - env[1] * Math.log10(f / 1e6); N = sumDbm(Nts, kT0B + Fa - p.SE_dB); }
    else N = Nts;
    return Math.pow(10, N / 10) * 1e-3 / p.rbw;
  }
  function apArea(kind, f) {
    if (kind === "hub") return HUB_A;
    if (kind === "lf75") return A_LF75;
    return Math.pow(K.c / f, 2) / (4 * Math.PI); // recip: lambda^2/4pi (HYP, HL2019 Sec. VI)
  }
  function setup(pin) {
    const p = Object.assign({}, X.DEFAULTS, MOD_DEFAULTS, pin || {});
    const b = X.model(p);
    const ne = Math.pow(10, p.log10_ne), U = b.U_ms;
    const s = { p, b, ne, U };
    s.f2 = p.C_mack * U / (2 * p.delta_m);                       // FACT Mack 2nd mode f = C U_E/(2 delta)
    s.f2_lo = s.f2 * (1 - p.b2 / 2); s.f2_hi = s.f2 * (1 + p.b2 / 2);
    s.fsh = p.St * U / p.D_m;                                    // FACT wake Strouhal f = St U/D
    s.fsh_lo = s.fsh * (1 - p.bsh / 2); s.fsh_hi = s.fsh * (1 + p.bsh / 2);
    const al = alphaDR(p.Tw_K);
    s.alpha = al;
    s.t_s = p.xs_D * p.D_m / U;
    s.surv = 1.0 / (1.0 + al * ne * s.t_s);                      // dn/dt = -alpha n^2
    s.tau_dr = 1.0 / (al * ne);
    s.f_chem = 1.0 / (2 * Math.PI * s.tau_dr);
    const na = nAir(p.h_km), nO2 = X_O2 * na, nN2 = X_N2 * na;
    s.nu_att = kAttO2(p.Tw_K) * nO2 * nO2 + kAttN2(p.Tw_K) * nO2 * nN2;
    s.nu_det = kDetO2(p.Tw_K) * nO2;
    s.L_wake_m = U * s.tau_dr;
    const I0 = b.J_Am2 * p.delta_m * Math.sqrt(p.A_s);
    s.I0 = I0; s.It = b.Isrc_A; s.I2 = p.m2 * I0; s.Ish = p.msh * s.surv * I0;
    s.fc = b.fc_Hz; s.r = p.r_km * 1e3;
    return s;
  }
  function psdI(s, f) {
    const p = s.p;
    const g = f <= s.fc ? 1.0 : Math.pow(f / s.fc, -5.0 / 3.0);
    let S = s.It * s.It * g / (2.5 * s.fc);
    if (s.f2_lo <= f && f < s.f2_hi) S += s.I2 * s.I2 / (p.b2 * s.f2);
    if (s.fsh_lo <= f && f < s.fsh_hi) S += s.Ish * s.Ish / (p.bsh * s.fsh);
    return S;
  }
  function s1(s, f, A) {
    const p = s.p;
    const loss = p.chi ? p.chi * sheathLoss(f, p)[0] : 0.0;
    return 2 * K.Z0 * psdI(s, f) * A / Math.pow(4 * Math.PI * s.r, 2) * Math.pow(10, -loss / 10);
  }
  function qBand(s, fa, fb, A) {
    const df = (fb - fa) / NQ_BAND; let q = 0.0;
    for (let i = 0; i < NQ_BAND; i++) { const f = fa + (i + 0.5) * df; q += Math.pow(s1(s, f, A) / noiseDensity(f, s.p), 2) * df; }
    return q;
  }
  function qAll(s, A) {
    const la = Math.log(F_ALL[0]), lb = Math.log(F_ALL[1]), dl = (lb - la) / NQ_ALL;
    const fmin = K.c / (2 * Math.PI * s.r); let q = 0.0;
    for (let i = 0; i < NQ_ALL; i++) { const f = Math.exp(la + (i + 0.5) * dl); if (f < fmin) continue; q += Math.pow(s1(s, f, A) / noiseDensity(f, s.p), 2) * f * dl; }
    return q;
  }
  const etaFromQ = (q, tau, d) => q > 0 ? Math.pow(d * d / (tau * q), 0.25) : Infinity;
  function tuned(s, f, ap) {
    const p = s.p, A = apArea(ap, f);
    const g = f <= s.fc ? 1.0 : Math.pow(f / s.fc, -5.0 / 3.0);
    const F = Math.min(1.0, p.rbw * g / (2.5 * s.fc));
    const Iband2 = s.It * s.It * F + p.rbw * (psdI(s, f) - s.It * s.It * g / (2.5 * s.fc));
    const loss = p.chi * sheathLoss(f, p)[0];
    const P1 = 2 * K.Z0 * Iband2 * A / Math.pow(4 * Math.PI * s.r, 2) * Math.pow(10, -loss / 10);
    const N = noiseDensity(f, p) * p.rbw;
    const q = p.rbw * Math.pow(P1 / N, 2);
    const tau = Math.max(p.tau_s, 1.0 / p.rbw);
    return { P1_dBm: dbm(P1), N_dBm: dbm(N), eta1: Math.sqrt(N / P1), eta: etaFromQ(q, tau, p.d_th),
             gain_dB: 5 * Math.log10(tau * p.rbw) - 10 * Math.log10(p.d_th) };
  }
  function matched(s, fa, fb, fcen) {
    const p = s.p, A = apArea("recip", fcen), q = qBand(s, fa, fb, A), tau = Math.max(p.tau_s, 1.0 / (fb - fa));
    return { A, q, eta: etaFromQ(q, tau, p.d_th), kr: 2 * Math.PI * s.r * fcen / K.c, quarter_wave_m: K.c / fcen / 4 };
  }
  function amFingerprint(p, f, m) {
    const out = [];
    [1, -1].forEach((sg) => {
      const q = Object.assign({}, p, { log10_ne: p.log10_ne + Math.log10(1 + sg * m) });
      const r = sheathLoss(f, q);
      out.push([r[0] - 10 * Math.log10(r[1]), 2 * Math.PI * f / K.c * r[2] * p.d_sh]);
    });
    const r0 = sheathLoss(f, p);
    return { dL_dB: out[0][0] - out[1][0], dphi_rad: out[0][1] - out[1][1], L0_dB: r0[0] - 10 * Math.log10(r0[1]) };
  }
  function model(pin) {
    const s = setup(pin), p = s.p, o = { version: VERSION };
    ["U", "f2", "f2_lo", "f2_hi", "fsh", "fsh_lo", "fsh_hi", "alpha", "t_s", "surv", "tau_dr", "f_chem",
     "nu_att", "nu_det", "L_wake_m", "I0", "It", "I2", "Ish"].forEach((k) => { o[k] = s[k]; });
    [["r433", 433.92e6, "hub"], ["r1296", 1296e6, "hub"], ["r1M", 1e6, "recip"]].forEach(([key, f, ap]) => {
      const t = tuned(s, f, ap); for (const k in t) o[key + "_" + k] = t[k];
    });
    const m2 = matched(s, s.f2_lo, s.f2_hi, s.f2), msh = matched(s, s.fsh_lo, s.fsh_hi, s.fsh);
    for (const k in m2) o["rMack_" + k] = m2[k];
    for (const k in msh) o["rShed_" + k] = msh[k];
    const A = apArea(p.listen, 1e6);
    o.A_listen = A;
    const qa = qAll(s, A), q2 = qBand(s, s.f2_lo, s.f2_hi, A), qs = qBand(s, s.fsh_lo, s.fsh_hi, A);
    o.q_all = qa; o.q_mack = q2; o.q_shed = qs;
    o.eta_all = etaFromQ(qa, p.tau_s, p.d_th);
    o.eta_mack = etaFromQ(q2, Math.max(p.tau_s, 1 / (s.f2_hi - s.f2_lo)), p.d_th);
    o.eta_shed = etaFromQ(qs, Math.max(p.tau_s, 1 / (s.fsh_hi - s.fsh_lo)), p.d_th);
    o.kr_shed = 2 * Math.PI * s.r * s.fsh / K.c;
    const P2 = 2 * K.Z0 * s.I2 * s.I2 * A / Math.pow(4 * Math.PI * s.r, 2);
    o.eta_tone_mack = P2 > 0 ? Math.sqrt(p.d_th * noiseDensity(s.f2, p) / (P2 * p.tau_s)) : Infinity;
    const eta = Math.pow(10, p.log10_eta);
    o.dev_all = isFinite(o.eta_all) ? Math.pow(eta, 4) / Math.pow(o.eta_all, 4) * p.d_th : 0.0;
    const fs = []; for (let k = 0; k <= 56; k++) fs.push(Math.pow(10, k / 8));
    o.spec_f = fs;
    o.spec_S_dBmHz = fs.map((f) => dbm(Math.max(eta * eta * s1(s, f, A), 1e-300)));
    o.spec_N_dBmHz = fs.map((f) => dbm(noiseDensity(f, p)));
    AM_F.forEach((f) => { const a = amFingerprint(p, f, p.m2), k = Math.round(f / 1e6); o["am_" + k + "_dL_dB"] = a.dL_dB; o["am_" + k + "_dphi"] = a.dphi_rad; o["am_" + k + "_L0_dB"] = a.L0_dB; });
    return o;
  }
  // spectrum helper for the page plot (not part of the cross-check record)
  function spectrum(pin, fs) {
    const s = setup(pin), p = s.p, A = apArea(p.listen, 1e6), eta = Math.pow(10, p.log10_eta);
    return fs.map((f) => ({ f, S: eta * eta * s1(s, f, A), N: noiseDensity(f, p),
      St: 2 * K.Z0 * (s.It * s.It * (f <= s.fc ? 1 : Math.pow(f / s.fc, -5 / 3)) / (2.5 * s.fc)) * A / Math.pow(4 * Math.PI * s.r, 2) * eta * eta }));
  }
  const api = { VERSION, MOD_DEFAULTS, model, setup, psdI, s1, noiseDensity, apArea, spectrum, alphaDR, kAttO2, kAttN2, kDetO2, A_LF75 };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ExptDMod = api;
})(typeof window !== "undefined" ? window : globalThis);
