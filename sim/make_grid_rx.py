"""python3 make_grid_rx.py -> grid_rx.json (main engine) + grid_rxmod.json (modulation engine): v0.3 receiver-chain cross-check grids."""
import json
PRESETS = ["tinysa", "tinysa_lna", "airspy_hfd", "uxa_preamp", "ideal"]
LNA = [(0, None)] + [(n, gn) for n in (1, 2, 3) for gn in ((21, 3), (10, 1), (30, 6))]


def lna_fields(n, gn):
    d = dict(n_lna=n)
    if gn:
        for k in range(1, 4):  # stage k: gain falls 3 dB and NF rises 0.5 dB per stage (exercise unequal stages)
            d["lna%d_G_dB" % k] = gn[0] - 3 * (k - 1)
            d["lna%d_NF_dB" % k] = gn[1] + 0.5 * (k - 1)
    return d


G = []
for pr in PRESETS:
    for n, gn in LNA:
        for cab in (0, 2):
            for f in (241e3, 1e6, 30e6, 433.59e6, 433.92e6, 1296e6):
                for env in ("quiet_rural", "residential", "none"):
                    for se in (0, 55, 80):
                        for rbw in (30e3, 1e3):
                            g = dict(rx_preset=pr, cable_dB=cab, f_rx=f, noise_env=env, SE_dB=se, rbw=rbw,
                                     aperture="recip" if f <= 1e6 else "hub")
                            g.update(lna_fields(n, gn))
                            G.append(g)
GM = []
for pr in PRESETS:
    for n in (0, 1, 2, 3):
        for env in ("quiet_rural", "residential"):
            for se in (55, 80):
                g = dict(rx_preset=pr, noise_env=env, SE_dB=se, cable_dB=(2 if n == 1 and se == 80 else 0))
                g.update(lna_fields(n, (21, 3) if n else None))
                GM.append(g)
json.dump(G, open("grid_rx.json", "w"))
json.dump(GM, open("grid_rxmod.json", "w"))
print(len(G), len(GM))
