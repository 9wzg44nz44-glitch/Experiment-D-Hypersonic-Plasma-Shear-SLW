(* ::Package:: *)
(* Experiment D - SLW/SW detectability engine, Mathematica twin of web/js/slw-detect.js and expt_d_model.py.
   PhysicsVersion: expt-d-detect-v0.1   (NOT yet executed: no Wolfram kernel on the build box; syntax checked by eye + wl_lint.mjs)
   Labels: FACT = published/standard physics; HYP = Hively EED as printed (Hively & Loebl 2019 Eq. B5/37;
   US 9,306,527 Eq. 15; hub ledger box C = -mu0 (d_t rho + div J)); ASSUMPTION = modelling choice; SWEEP = unknown coupling.
   Symbols avoid the protected single letters C, D, E, I, K, N, O. *)

exptDVersion = "expt-d-detect-v0.1";

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
      Style["Experiment D: could a receiver hear it?  physics " <> exptDVersion <> " \[CenterDot] UI v0.1.1 (HYP estimate, not flight data)", Bold],
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
