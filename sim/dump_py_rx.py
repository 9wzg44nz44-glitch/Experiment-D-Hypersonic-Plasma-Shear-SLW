"""python3 dump_py_rx.py -> py_rx_outputs.json + py_rxmod_outputs.json (same grids as dump_js_rx.mjs)."""
import json, math
import expt_d_model as X
import expt_d_mod as M


def clean(v):
    if isinstance(v, float) and not math.isfinite(v):
        return None
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [clean(x) for x in v]
    return v


for grid, out, eng in (("grid_rx.json", "py_rx_outputs.json", X), ("grid_rxmod.json", "py_rxmod_outputs.json", M)):
    G = json.load(open(grid))
    json.dump({"version": eng.VERSION, "records": [clean(eng.model(p)) for p in G]}, open(out, "w"))
    print("wrote", out, len(G))
