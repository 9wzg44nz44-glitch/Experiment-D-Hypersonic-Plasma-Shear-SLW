// node regress_v02.mjs <v0.2 js dir> : v0.3 engines at the DEFAULT receiver chain vs the v0.2 engines, on grid.json + grid_mod.json.
// Every v0.2 output key must match (exact equality counted separately from rel <= 1e-12).
import fs from "fs"; import { createRequire } from "module"; import path from "path";
const require = createRequire(import.meta.url);
const old = process.argv[2] || "/tmp/v02/js";
const here = path.dirname(new URL(import.meta.url).pathname);
const cand = (f) => [path.join(here, "web/js", f), path.join(here, "../js", f)].find((x) => fs.existsSync(x));
const N3 = require(cand("slw-detect.js")), M3 = require(cand("slw-modulation.js"));
const N2 = require(path.join(old, "slw-detect.js")), M2 = require(path.join(old, "slw-modulation.js"));
let n = 0, exact = 0, worst = 0, at = "";
function cmp(a, b, p) {
  if (typeof b === "string") { n++; if (a === b || p.endsWith(".version")) exact++; else { worst = Infinity; at = p; } return; }
  if (Array.isArray(b)) { b.forEach((v, i) => cmp(a[i], v, p + "[" + i + "]")); return; }
  n++; if (a === b || (Number.isNaN(a) && Number.isNaN(b))) { exact++; return; }
  const r = Math.abs(a - b) / Math.max(Math.abs(a), Math.abs(b)); if (!(r <= worst)) { worst = r; at = p; }
}
const G = JSON.parse(fs.readFileSync(path.join(here, "grid.json"))), GM = JSON.parse(fs.readFileSync(path.join(here, "grid_mod.json")));
G.forEach((g, i) => { const a = N3.model(g), b = N2.model(g); for (const k in b) if (k !== "version") cmp(a[k], b[k], `main[${i}].${k}`); });
GM.forEach((g, i) => { const a = M3.model(g), b = M2.model(g); for (const k in b) if (k !== "version") cmp(a[k], b[k], `mod[${i}].${k}`); });
console.log(`v0.3 default chain vs v0.2: ${n} values, bit-identical ${exact}, worst rel ${worst.toExponential(2)} ${at}`);
process.exit(worst <= 1e-12 ? 0 : 1);
