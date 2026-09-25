(* ::Package:: *)
(* Experiment D - SLW/SW detectability engine, Mathematica twin of web/js/slw-detect.js and expt_d_model.py.
   PhysicsVersion: expt-d-detect-v0.2 (v0.1 engine unchanged + v0.2 sheath-modulation section at the end)   (NOT yet executed: no Wolfram kernel on the build box; syntax checked by eye + wl_lint.mjs)
   Labels: FACT = published/standard physics; HYP = Hively EED as printed (Hively & Loebl 2019 Eq. B5/37;
   US 9,306,527 Eq. 15; hub ledger box C = -mu0 (d_t rho + div J)); ASSUMPTION = modelling choice; SWEEP = unknown coupling.
   Symbols avoid the protected single letters C, D, E, I, K, N, O. *)

exptDVersion = "expt-d-detect-v0.2";

(* FACT: CODATA 2018 *)
cLight = 299792458.;
mu0 = 1.25663706212*^-6;
eps0 = 8.8541878128*^-12;
qe = 1.602176634*^-19;
me = 9.1093837015*^-31;
kB = 1.380649*^-23;
tRef = 290.;
z0 = mu0 cLight;

(* FACT: US Standard Atmosphere 1976 *)
ussaH = {30., 40., 50., 60., 70., 80., 90.};
ussaRho = {1.8410*^-2, 3.9957*^-3, 1.0269*^-3, 3.0968*^-4, 8.2829*^-5, 1.8458*^-5, 3.416*^-6};
ussaA = {301.71, 317.19, 329.80, 314.07, 297.14, 282.54, 274.10};
(* FACT: Grantham NASA TN D-6062 (1970) p.12 *)
nuRef = 2.51*^9; hRef = 45.72;
(* FACT: ITU-R P.372 Table 1 *)
noiseEnv = <|"none" -> None, "quiet_rural" -> {53.6, 28.6}, "rural" -> {67.2, 27.7},
   "residential" -> {72.5, 27.7}, "city" -> {76.8, 27.7}|>;
(* HYP carry-over: hub SleeveBalunSNR receive convention *)
hubAeff = N[Pi] 0.05 0.05; hubEta = 0.5;
dbPerNp2 = 8.685889638065035;

exptDDefaults = <|"h_km" -> 70., "mach" -> 25., "log10_ne" -> 18., "nu_scale" -> 1., "log10_S" -> 6.,
   "delta_m" -> 0.01, "B_uT" -> 50., "theta_deg" -> 90., "mech" -> "vxB", "Te_K" -> 6000., "f_close" -> 1.,
   "m_t" -> 0.1, "A_s" -> 1., "d_sh" -> 0.05, "f_rx" -> 30.*^6, "rbw" -> 30.*^3, "aperture" -> "hub",
   "SE_dB" -> 55., "noise_env" -> "quiet_rural", "log10_eta" -> -3., "chi" -> 0., "log10_kappa" -> 0., "r_km" -> 100.|>;

interpTab[xs_List, ys_List, x_, logy_] := Module[{n = Length[xs], i, t},
   i = Which[x <= xs[[1]], 1, x >= xs[[n]], n - 1, True, LengthWhile[Rest[xs], x > # &] + 1];
   t = (x - xs[[i]])/(xs[[i + 1]] - xs[[i]]);
   If[logy, Exp[Log[ys[[i]]] + t (Log[ys[[i + 1]]] - Log[ys[[i]]])], ys[[i]] + t (ys[[i + 1]] - ys[[i]])]];
rhoAir[h_] := interpTab[ussaH, ussaRho, h, True];
soundSpeed[h_] := interpTab[ussaH, ussaA, h, False];

(* stable principal sqrt of a + I b, b >= 0 *)
cSqrt[a_, b_] := Module[{r = Sqrt[a^2 + b^2], re, im},
   If[a >= 0, re = Sqrt[(r + a)/2]; {re, If[re > 0, b/(2 re), 0.]},
    im = Sqrt[(r - a)/2]; {b/(2 im), im}]];
dBm[w_] := 10. Log10[w/1.*^-3];
sumdBm[a_, b_] := 10. Log10[10.^(a/10.) + 10.^(b/10.)];

exptDModel[pin_Association] := Module[
   {p = Join[exptDDefaults, pin], a, uu, ne, wp, fp, nu, sigma, ss, du, bb, de, jj, nc, isrc, fc, g, fspec,
    iband, ipk, w, den, er, ei, nn, k0, alpha, ashdB, tint, tintdB, lam, r, arx, atem, nts, kt0b, env, fMHz,
    fa, nextConv, nconv, nhiv, eta, kappa, sslw1, slwLossdB, pslw1, pslw, cpk, elpk, ssw1, psw, icellpk,
    ptemEmit, ptemdBm, tb, pthdBm, pslwdBm, pswdBm, nhivW},
   a = soundSpeed[p["h_km"]];
   uu = p["mach"] a;
   ne = 10.^p["log10_ne"];
   wp = Sqrt[ne qe qe/(eps0 me)];                               (* FACT *)
   fp = wp/(2 N[Pi]);                                           (* = 8.98 Sqrt[ne] Hz *)
   nu = p["nu_scale"] nuRef rhoAir[p["h_km"]]/rhoAir[hRef];    (* FACT anchor x ASSUMPTION nu ~ rho *)
   sigma = ne qe qe/(me nu);                                    (* FACT Drude DC *)
   ss = 10.^p["log10_S"];
   du = Min[ss p["delta_m"], uu];                               (* ASSUMPTION *)
   bb = p["B_uT"] 1.*^-6;
   de = kB p["Te_K"]/(me nu);
   jj = If[p["mech"] === "diff",
     p["f_close"] qe de ne/p["delta_m"],
     p["f_close"] sigma du bb Sin[p["theta_deg"] N[Pi]/180]];
   nc = p["A_s"]/(p["delta_m"] p["delta_m"]);
   isrc = p["m_t"] jj p["delta_m"] Sqrt[p["A_s"]];
   fc = ss/(2 N[Pi]);
   g = If[p["f_rx"] <= fc, 1., (p["f_rx"]/fc)^(-5./3.)];
   fspec = Min[1., p["rbw"] g/(2.5 fc)];
   iband = isrc Sqrt[fspec];
   ipk = Sqrt[2.] iband;
   w = 2 N[Pi] p["f_rx"];
   den = w w + nu nu;
   er = 1 - wp wp/den; ei = wp wp nu/(w den);
   nn = cSqrt[er, ei];
   k0 = w/cLight;
   alpha = k0 nn[[2]];
   ashdB = dbPerNp2 alpha p["d_sh"];
   tint = 4 nn[[1]]/((nn[[1]] + 1)^2 + nn[[2]]^2);
   tintdB = 10. Log10[tint];
   lam = cLight/p["f_rx"];
   r = p["r_km"] 1.*^3;
   arx = If[p["aperture"] === "recip", lam lam/(4 N[Pi]), hubAeff hubEta];
   atem = 1.5 lam lam/(4 N[Pi]);
   nts = -102. + 10. Log10[p["rbw"]/30.*^3];
   kt0b = dBm[kB tRef p["rbw"]];
   env = noiseEnv[p["noise_env"]];
   fMHz = p["f_rx"]/1.*^6;
   If[env === None,
    fa = Null; nconv = nts; nhiv = nts,
    fa = env[[1]] - env[[2]] Log10[fMHz];
    nextConv = kt0b + fa;
    nconv = sumdBm[nts, nextConv];
    nhiv = sumdBm[nts, nextConv - p["SE_dB"]]];
   eta = 10.^p["log10_eta"]; kappa = 10.^p["log10_kappa"];
   (* HYP: Hively & Loebl 2019 Eq. B5 / US 9,306,527 Eq. 15 *)
   sslw1 = z0 ipk ipk/(4 N[Pi] r)^2;
   slwLossdB = p["chi"] ashdB;
   pslw1 = sslw1 arx 10.^(-slwLossdB/10.);
   pslw = eta eta pslw1;
   cpk = mu0 eta ipk/(4 N[Pi] r);                              (* HYP ledger box C source, retarded Green fn *)
   elpk = z0 cpk/mu0;                                            (* HYP HL2019 Eq. 37 far field *)
   ssw1 = 0.5 z0 ipk ipk/(4 N[Pi] r)^2;                          (* HYP SW proxy c C^2/(2 mu0) *)
   psw = kappa eta eta ssw1 arx;
   (* FACT-form classical TEM, Balanis 4-16, incoherent cells *)
   icellpk = Sqrt[2.] p["m_t"] jj p["delta_m"] p["delta_m"] Sqrt[fspec];
   ptemEmit = nc z0 (N[Pi]/3) (icellpk p["delta_m"]/lam)^2;
   ptemdBm = dBm[ptemEmit atem/(4 N[Pi] r r)] + tintdB - ashdB;
   tb = p["Te_K"] tint;
   pthdBm = dBm[kB tb p["rbw"] 1.5 p["A_s"]/(4 N[Pi] r r)];
   pslwdBm = dBm[pslw]; pswdBm = dBm[psw];
   nhivW = 10.^(nhiv/10.) 1.*^-3;
   <|"version" -> exptDVersion, "a_ms" -> a, "U_ms" -> uu, "fp_Hz" -> fp, "nu_s" -> nu, "sigma_Sm" -> sigma,
    "du_ms" -> du, "De_m2s" -> de, "J_Am2" -> jj, "Nc" -> nc, "Isrc_A" -> isrc, "fc_Hz" -> fc, "Fspec" -> fspec,
    "Iband_A" -> iband, "eps_r" -> er, "eps_i" -> ei, "n_re" -> nn[[1]], "n_im" -> nn[[2]], "alpha_Npm" -> alpha,
    "Ash_dB" -> ashdB, "Tint_dB" -> tintdB, "Arx_m2" -> arx, "Atem_m2" -> atem, "Nts_dBm" -> nts, "Fa_dB" -> fa,
    "Nconv_dBm" -> nconv, "Nhiv_dBm" -> nhiv, "Pslw1_dBm" -> dBm[pslw1], "Pslw_dBm" -> pslwdBm,
    "SNR_slw_dB" -> pslwdBm - nhiv, "Cpk_T" -> cpk, "ELpk_Vm" -> elpk, "Psw1_dBm" -> dBm[ssw1 arx],
    "Psw_dBm" -> pswdBm, "SNR_sw_dB" -> pswdBm - nhiv, "Ptem_dBm" -> ptemdBm, "SNR_tem_dB" -> ptemdBm - nconv,
    "PtemHiv_dBm" -> ptemdBm - p["SE_dB"], "Tb_K" -> tb, "Pth_dBm" -> pthdBm, "SNR_th_dB" -> pthdBm - nconv,
    "eta_th0" -> Sqrt[nhivW/pslw1], "eta_th10" -> Sqrt[10 nhivW/pslw1], "etakap_th0_sw" -> Sqrt[nhivW/(ssw1 arx)],
    "rmax_km" -> p["r_km"] Sqrt[pslw/nhivW], "kr" -> 2 N[Pi] r/lam|>];

(* Interactive twin of slw-detectability.html (sliders mirror the page). *)
exptDManipulate[] := Manipulate[
   Module[{apEff = If[ap === "auto", If[frx == 1.*^6, "recip", "hub"], ap], q, pars, rr = 10.^Range[0., 3., 0.05]},
    pars = <|"h_km" -> h, "mach" -> mach, "log10_ne" -> lne, "log10_S" -> lS, "delta_m" -> dl,
        "B_uT" -> bt, "mech" -> mech, "f_close" -> fcl, "m_t" -> mt, "A_s" -> as, "f_rx" -> frx, "aperture" -> apEff,
        "SE_dB" -> se, "noise_env" -> env, "log10_eta" -> le, "chi" -> chi, "log10_kappa" -> lk, "r_km" -> rk|>;
    q = exptDModel[pars];
    Column[{
      Style["Experiment D: could a receiver hear it?  physics " <> exptDVersion <> " \[CenterDot] UI v0.2.0 (HYP estimate, not flight data)", Bold],
      Style[If[q["eta_th0"] <= 1.,
        "Detectable? Only if \[Eta] > " <> ToString[NumberForm[q["eta_th0"], 3]],
        "Detectable? No, not for any \[Eta] \[LessEqual] 1 (would need \[Eta] = " <> ToString[NumberForm[q["eta_th0"], 3]] <> ")"] <>
        "  \[CenterDot]  SNR " <> ToString[NumberForm[q["SNR_slw_dB"], {4, 1}]] <> " dB", 16, Bold],
      Style["SNR = signal-to-noise ratio: how far the signal sits above the receiver's own noise (0 dB = equal).", Italic, Gray],
      OpenerView[{"Detailed readouts",
      Grid[{{"plasma frequency f_p (GHz)", q["fp_Hz"]/1.*^9}, {"collision rate \[Nu] (1/s)", q["nu_s"]}, {"current density J, upper limit (A/m^2)", q["J_Am2"]},
        {"flickering current rms (A)", q["Isrc_A"]}, {"plasma loss, ordinary radio (dB)", q["Ash_dB"]}, {"noise floor, shielded Hively receiver (dBm)", q["Nhiv_dBm"]},
        {"SLW received power, HYP (dBm)", q["Pslw_dBm"]}, {"SLW SNR, HYP (dB)", q["SNR_slw_dB"]}, {"smallest \[Eta] for SNR 0 dB", q["eta_th0"]},
        {"scalar-wave proxy power, HYP (dBm)", q["Psw_dBm"]}, {"ordinary radio power, FACT form (dBm)", q["Ptem_dBm"]}, {"plasma glow power, FACT (dBm)", q["Pth_dBm"]}},
       Frame -> All, Alignment -> Left]}],
      ListLogLinearPlot[{
        Table[{x, exptDModel[Append[pars, "r_km" -> x]]["Pslw_dBm"]}, {x, rr}],
        Table[{x, q["Nhiv_dBm"]}, {x, rr}]}, Joined -> True, PlotLegends -> {"SLW at your \[Eta] (HYP)", "noise floor"},
       AxesLabel -> {"distance (km)", "received power (dBm)"}, ImageSize -> 480],
      Style["Cloud twin pending sync (" <> exptDVersion <> ")", Italic]}]],
   Style["Main controls", Bold],
   {{rk, 100., "distance to the vehicle (km)"}, 1., 1000.},
   {{lne, 18., "plasma density: log10 of n_e, free electrons per cubic metre"}, 14., 20.},
   {{frx, 30.*^6, "receiver band"}, {433.92*^6 -> "433.92 MHz: Dan's ball antenna", 1296.*^6 -> "1296 MHz: Dan's sleeve-balun",
      30.*^6 -> "30 MHz: reference", 1.*^6 -> "1 MHz: hypothetical ~75 m antenna"}},
   {{le, -3., "unknown coupling: log10 \[Eta], fraction of plasma current launching an SLW if Hively is right (SWEEP)"}, -12., 0.},
   Delimiter, Style["Full controls", Bold],
   {{h, 70., "altitude (km)"}, 30., 90.}, {{mach, 25., "Mach number (speed / speed of sound)"}, 5., 26.},
   {{lS, 6., "log10 shear rate S (1/s)"}, 4., 8.}, {{dl, 0.01, "shear-layer thickness \[Delta] (m)"}, 0.001, 0.1},
   {{bt, 50., "Earth's magnetic field B (\[Micro]T)"}, 25., 65.}, {{mech, "vxB", "how the current is driven"}, {"vxB" -> "motion through Earth's field", "diff" -> "electron diffusion (extreme bound)"}},
   {{fcl, 1., "current closure f_close (1 = upper limit)"}, 0.001, 1.},
   {{mt, 0.1, "turbulence level \[Delta]n/n"}, 0.01, 0.5}, {{as, 1., "turbulent sheet area (m^2)"}, 0.1, 10.},
   {{ap, "auto", "antenna collecting-area model"}, {"auto" -> "auto (from band)", "hub" -> "small Hively antenna (hub)", "recip" -> "full-size resonant \[Lambda]^2/4\[Pi]"}},
   {{se, 55., "shielding SE: Faraday + sleeve-balun cut of ordinary radio (dB)"}, 0., 80.},
   {{env, "quiet_rural", "local radio noise (ITU-R P.372)"}, {"quiet_rural", "rural", "residential", "city", "none"}},
   {{chi, 0., "\[Chi]: SLW loss in plasma relative to radio (SWEEP)"}, 0., 1.},
   {{lk, 0., "log10 \[Kappa]_C: receiver response to a pure scalar wave (SWEEP)"}, -12., 0.},
   SaveDefinitions -> True];

(* ===================== v0.2 "Sheath modulation" (mirror of js/slw-modulation.js and sim/expt_d_mod.py) =====================
   NOT yet executed (no Wolfram kernel on the build box). FACT: Mack 2nd mode f2 = C U_E/(2 delta) (Parziale, Shepherd & Hornung 2015,
   JFM 781:87, Table 3: C = 0.63-0.69); wake oscillation f = St U/D (Schmidt & Shepherd 2015 JFM 785:R3; Awasthi et al. 2022;
   Thasu & Duvvuri 2022); NO+ recombination 4.2e-7 (Te/300)^-0.85 cm^3/s (Torr, St-Maurice & Torr 1977); Kossyi et al. 1992 R45, R46, R57.
   Detection: Eckart filter + square law + smoothing (Rudnick 1961), flat-band limit = radiometer equation (Dicke 1946).
   ASSUMPTIONS (sliders): U_E = U, top-hat bands, m2, msh, Tw, xs_D. HYP: the SLW itself (HL2019 Eq. B5, eta SWEEP). *)
amu = 1.66053906660*^-27; mAir = 28.9644 amu; xO2 = 0.209476; xN2 = 0.780840;
aLF75 = cLight cLight/(4 N[Pi] 1.*^6 1.*^6);
modDefaults = <|"C_mack" -> 0.65, "b2" -> 0.2, "m2" -> 0.01, "D_m" -> 1., "St" -> 0.2, "bsh" -> 0.2, "msh" -> 0.1,
   "Tw_K" -> 3000., "xs_D" -> 1., "tau_s" -> 1., "d_th" -> 1., "listen" -> "lf75"|>;
nqBand = 200; nqAll = 1200; fAllLo = 1.; fAllHi = 1.*^7;
amFreqs = {433.92*^6, 1296.*^6, 2.25*^9, 10.*^9};

alphaDR[t_] := 4.2*^-13 (t/300.)^-0.85;                         (* FACT Torr et al. 1977, NO+ *)
kAttO2[t_] := 1.4*^-41 (300./t) Exp[-600./t];                   (* FACT Kossyi 1992 R45, Te = Tg *)
kAttN2[t_] := 1.07*^-43 (300./t)^2 Exp[-70./t];                 (* FACT Kossyi 1992 R46, Te = Tg *)
kDetO2[t_] := 2.7*^-16 (t/300.)^0.5 Exp[-5590./t];              (* FACT Kossyi 1992 R57 *)
nAir[h_] := rhoAir[h]/mAir;

sheathLoss[f_, p_] := Module[{ne = 10.^p["log10_ne"], wp, nu, w, den, er, ei, nn},
   wp = Sqrt[ne qe qe/(eps0 me)];
   nu = p["nu_scale"] nuRef rhoAir[p["h_km"]]/rhoAir[hRef];
   w = 2 N[Pi] f; den = w w + nu nu;
   er = 1 - wp wp/den; ei = wp wp nu/(w den);
   nn = cSqrt[er, ei];
   {dbPerNp2 (w/cLight) nn[[2]] p["d_sh"], 4 nn[[1]]/((nn[[1]] + 1)^2 + nn[[2]]^2), nn[[1]]}];

noiseDensity[f_, p_] := Module[{nts = -102. + 10. Log10[p["rbw"]/30.*^3], env = noiseEnv[p["noise_env"]], kt0b, fa, nn},
   If[env === None, nn = nts,
    kt0b = dBm[kB tRef p["rbw"]]; fa = env[[1]] - env[[2]] Log10[f/1.*^6];
    nn = sumdBm[nts, kt0b + fa - p["SE_dB"]]];
   10.^(nn/10.) 1.*^-3/p["rbw"]];

apArea[kind_, f_] := Which[kind === "hub", hubAeff hubEta, kind === "lf75", aLF75, True, (cLight/f)^2/(4 N[Pi])];

modSetup[pin_Association] := Module[{p = Join[exptDDefaults, modDefaults, pin], b, ne, uu, s = <||>, al, na, nO2, nN2, i0},
   b = exptDModel[p]; ne = 10.^p["log10_ne"]; uu = b["U_ms"];
   s["p"] = p; s["ne"] = ne; s["U"] = uu;
   s["f2"] = p["C_mack"] uu/(2 p["delta_m"]);                  (* FACT Mack 2nd mode *)
   s["f2_lo"] = s["f2"] (1 - p["b2"]/2); s["f2_hi"] = s["f2"] (1 + p["b2"]/2);
   s["fsh"] = p["St"] uu/p["D_m"];                              (* FACT wake Strouhal *)
   s["fsh_lo"] = s["fsh"] (1 - p["bsh"]/2); s["fsh_hi"] = s["fsh"] (1 + p["bsh"]/2);
   al = alphaDR[p["Tw_K"]]; s["alpha"] = al;
   s["t_s"] = p["xs_D"] p["D_m"]/uu;
   s["surv"] = 1./(1. + al ne s["t_s"]);                        (* dn/dt = -alpha n^2 *)
   s["tau_dr"] = 1./(al ne);
   s["f_chem"] = 1./(2 N[Pi] s["tau_dr"]);
   na = nAir[p["h_km"]]; nO2 = xO2 na; nN2 = xN2 na;
   s["nu_att"] = kAttO2[p["Tw_K"]] nO2 nO2 + kAttN2[p["Tw_K"]] nO2 nN2;
   s["nu_det"] = kDetO2[p["Tw_K"]] nO2;
   s["L_wake_m"] = uu s["tau_dr"];
   i0 = b["J_Am2"] p["delta_m"] Sqrt[p["A_s"]];
   s["I0"] = i0; s["It"] = b["Isrc_A"]; s["I2"] = p["m2"] i0; s["Ish"] = p["msh"] s["surv"] i0;
   s["fc"] = b["fc_Hz"]; s["r"] = p["r_km"] 1.*^3;
   s];

psdI[s_, f_] := Module[{p = s["p"], g, sv},
   g = If[f <= s["fc"], 1., (f/s["fc"])^(-5./3.)];
   sv = s["It"]^2 g/(2.5 s["fc"]);
   If[s["f2_lo"] <= f && f < s["f2_hi"], sv += s["I2"]^2/(p["b2"] s["f2"])];
   If[s["fsh_lo"] <= f && f < s["fsh_hi"], sv += s["Ish"]^2/(p["bsh"] s["fsh"])];
   sv];

sOne[s_, f_, a_] := Module[{p = s["p"], loss},
   loss = If[p["chi"] != 0, p["chi"] sheathLoss[f, p][[1]], 0.];
   2 z0 psdI[s, f] a/(4 N[Pi] s["r"])^2 10.^(-loss/10.)];

qBand[s_, fa_, fb_, a_] := Module[{df = (fb - fa)/nqBand},
   Sum[With[{f = fa + (i + 0.5) df}, (sOne[s, f, a]/noiseDensity[f, s["p"]])^2 df], {i, 0, nqBand - 1}]];

qAll[s_, a_] := Module[{la = Log[fAllLo], lb = Log[fAllHi], dl, fmin = cLight/(2 N[Pi] s["r"])},
   dl = (lb - la)/nqAll;
   Sum[With[{f = Exp[la + (i + 0.5) dl]}, If[f < fmin, 0., (sOne[s, f, a]/noiseDensity[f, s["p"]])^2 f dl]], {i, 0, nqAll - 1}]];

etaFromQ[q_, tau_, dth_] := If[q > 0, (dth dth/(tau q))^0.25, Infinity];

tunedRx[s_, f_, ap_] := Module[{p = s["p"], a, g, fs, iband2, loss, p1, nw, q, tau},
   a = apArea[ap, f];
   g = If[f <= s["fc"], 1., (f/s["fc"])^(-5./3.)];
   fs = Min[1., p["rbw"] g/(2.5 s["fc"])];
   iband2 = s["It"]^2 fs + p["rbw"] (psdI[s, f] - s["It"]^2 g/(2.5 s["fc"]));
   loss = p["chi"] sheathLoss[f, p][[1]];
   p1 = 2 z0 iband2 a/(4 N[Pi] s["r"])^2 10.^(-loss/10.);
   nw = noiseDensity[f, p] p["rbw"];
   q = p["rbw"] (p1/nw)^2;
   tau = Max[p["tau_s"], 1./p["rbw"]];
   <|"P1_dBm" -> dBm[p1], "N_dBm" -> dBm[nw], "eta1" -> Sqrt[nw/p1], "eta" -> etaFromQ[q, tau, p["d_th"]],
    "gain_dB" -> 5. Log10[tau p["rbw"]] - 10. Log10[p["d_th"]]|>];

matchedRx[s_, fa_, fb_, fcen_] := Module[{p = s["p"], a, q, tau},
   a = apArea["recip", fcen]; q = qBand[s, fa, fb, a]; tau = Max[p["tau_s"], 1./(fb - fa)];
   <|"A" -> a, "q" -> q, "eta" -> etaFromQ[q, tau, p["d_th"]], "kr" -> 2 N[Pi] s["r"] fcen/cLight, "quarter_wave_m" -> cLight/fcen/4|>];

amFingerprint[p_, f_, m_] := Module[{out, r0},
   out = Table[With[{rr = sheathLoss[f, Append[p, "log10_ne" -> p["log10_ne"] + Log10[1 + sg m]]]},
       {rr[[1]] - 10. Log10[rr[[2]]], 2 N[Pi] f/cLight rr[[3]] p["d_sh"]}], {sg, {1, -1}}];
   r0 = sheathLoss[f, p];
   <|"dL_dB" -> out[[1, 1]] - out[[2, 1]], "dphi_rad" -> out[[1, 2]] - out[[2, 2]], "L0_dB" -> r0[[1]] - 10. Log10[r0[[2]]]|>];

prefixKeys[pre_String, a_Association] := KeyMap[pre <> # &, a];

exptDModModel[pin_Association] := Module[{s = modSetup[pin], p, o, m2, msh, a, qa, q2, qs, p2, eta, fs, am},
   p = s["p"];
   o = Join[<|"version" -> exptDVersion|>, KeyTake[s, {"U", "f2", "f2_lo", "f2_hi", "fsh", "fsh_lo", "fsh_hi", "alpha", "t_s", "surv",
       "tau_dr", "f_chem", "nu_att", "nu_det", "L_wake_m", "I0", "It", "I2", "Ish"}]];
   o = Join[o, prefixKeys["r433_", tunedRx[s, 433.92*^6, "hub"]], prefixKeys["r1296_", tunedRx[s, 1296.*^6, "hub"]],
     prefixKeys["r1M_", tunedRx[s, 1.*^6, "recip"]]];
   m2 = matchedRx[s, s["f2_lo"], s["f2_hi"], s["f2"]]; msh = matchedRx[s, s["fsh_lo"], s["fsh_hi"], s["fsh"]];
   o = Join[o, prefixKeys["rMack_", m2], prefixKeys["rShed_", msh]];
   a = apArea[p["listen"], 1.*^6]; o["A_listen"] = a;
   qa = qAll[s, a]; q2 = qBand[s, s["f2_lo"], s["f2_hi"], a]; qs = qBand[s, s["fsh_lo"], s["fsh_hi"], a];
   o["q_all"] = qa; o["q_mack"] = q2; o["q_shed"] = qs;
   o["eta_all"] = etaFromQ[qa, p["tau_s"], p["d_th"]];
   o["eta_mack"] = etaFromQ[q2, Max[p["tau_s"], 1./(s["f2_hi"] - s["f2_lo"])], p["d_th"]];
   o["eta_shed"] = etaFromQ[qs, Max[p["tau_s"], 1./(s["fsh_hi"] - s["fsh_lo"])], p["d_th"]];
   o["kr_shed"] = 2 N[Pi] s["r"] s["fsh"]/cLight;
   p2 = 2 z0 s["I2"]^2 a/(4 N[Pi] s["r"])^2;
   o["eta_tone_mack"] = If[p2 > 0, Sqrt[p["d_th"] noiseDensity[s["f2"], p]/(p2 p["tau_s"])], Infinity];
   eta = 10.^p["log10_eta"];
   o["dev_all"] = If[o["eta_all"] < Infinity, eta^4/o["eta_all"]^4 p["d_th"], 0.];
   fs = Table[10.^(k/8.), {k, 0, 56}];
   o["spec_f"] = fs;
   o["spec_S_dBmHz"] = dBm[Max[eta eta sOne[s, #, a], 1.*^-300]] & /@ fs;
   o["spec_N_dBmHz"] = dBm[noiseDensity[#, p]] & /@ fs;
   Do[am = amFingerprint[p, f, p["m2"]];
    o["am_" <> ToString[Round[f/1.*^6]] <> "_dL_dB"] = am["dL_dB"];
    o["am_" <> ToString[Round[f/1.*^6]] <> "_dphi"] = am["dphi_rad"];
    o["am_" <> ToString[Round[f/1.*^6]] <> "_L0_dB"] = am["L0_dB"], {f, amFreqs}];
   o];

(* Interactive twin of the page's "Sheath modulation" tab: 4 sliders, one spectrum plot, one-line verdict. *)
exptDModManipulate[] := Manipulate[
   Module[{pars, q, s, a, fs = 10.^Range[0., 7., 0.02], etaV},
    pars = <|"mach" -> mach, "h_km" -> h, "r_km" -> rk, "log10_eta" -> le, "tau_s" -> tau|>;
    q = exptDModModel[pars]; s = modSetup[pars]; a = apArea["lf75", 1.*^6]; etaV = 10.^le;
    Column[{
      Style["Sheath modulation  \[CenterDot]  physics " <> exptDVersion <> " (HYP estimate; SLW strength NOT claimed)", Bold],
      Style["With the flicker pattern exploited: needs \[Eta] > " <> ToString[NumberForm[q["eta_all"], 2]] <>
        " (75 m-class LF antenna, " <> ToString[tau] <> " s averaging). Dan's 433/1296 MHz: needs \[Eta] > " <>
        ToString[NumberForm[q["r433_eta"], 2]] <> " / " <> ToString[NumberForm[q["r1296_eta"], 2]], 14, Bold],
      ListLogLinearPlot[{
        Table[{f, dBm[Max[etaV etaV sOne[s, f, a], 1.*^-300]]}, {f, fs}],
        Table[{f, dBm[noiseDensity[f, s["p"]]]}, {f, fs}]}, Joined -> True,
       PlotLegends -> {"SLW at your \[Eta] (HYP), dBm/Hz", "noise floor, dBm/Hz"},
       AxesLabel -> {"frequency (Hz)", "dBm per Hz"}, ImageSize -> 520],
      Style["Mack band " <> ToString[Round[q["f2"]/1000.]] <> " kHz (FACT) \[CenterDot] wake band " <> ToString[Round[q["fsh"]]] <> " Hz (FACT)", Gray],
      Style["Cloud twin pending sync (" <> exptDVersion <> ")", Italic]}]],
   {{mach, 25., "Mach number (speed / local speed of sound)"}, 5., 26.},
   {{h, 70., "altitude (km)"}, 30., 90.},
   {{rk, 100., "distance to the vehicle (km)"}, 1., 1000.},
   {{le, -3., "log10 \[Eta] (SWEEP, HYP)"}, -12., 0.},
   {{tau, 1., "averaging (dwell) time (s)"}, 0.001, 100.},
   SaveDefinitions -> True];
