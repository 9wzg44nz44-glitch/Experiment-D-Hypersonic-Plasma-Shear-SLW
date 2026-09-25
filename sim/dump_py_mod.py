"""python3 dump_py_mod.py -> py_mod_outputs.json : evaluates expt_d_mod.model on grid_mod.json
(same grid as dump_js_mod.mjs; non-finite numbers -> null, as JSON.stringify does in JS)."""
import json, math
import expt_d_mod as M


def clean(v):
    if isinstance(v, float) and not math.isfinite(v):
        return None
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [clean(x) for x in v]
    return v


G = json.load(open("grid_mod.json"))
json.dump({"version": M.VERSION, "records": [clean(M.model(p)) for p in G]},
          open("py_mod_outputs.json", "w"))
print(f"wrote py_mod_outputs.json ({len(G)} points, {M.VERSION})")
