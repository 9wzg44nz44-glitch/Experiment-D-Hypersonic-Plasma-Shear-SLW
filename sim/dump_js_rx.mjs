// node dump_js_rx.mjs -> js_rx_outputs.json + js_rxmod_outputs.json (v0.3 receiver-chain grids; non-finite -> null)
import fs from "fs"; import { createRequire } from "module";
const require = createRequire(import.meta.url);
const pick = (f) => ["./web/js/" + f, "../js/" + f].find((x) => fs.existsSync(new URL(x, import.meta.url)));
const X = require(pick("slw-detect.js")), M = require(pick("slw-modulation.js"));
const clean = (o) => { for (const k in o) if (typeof o[k] === "number" && !isFinite(o[k])) o[k] = null; else if (Array.isArray(o[k])) o[k] = o[k].map((v) => (typeof v === "number" && !isFinite(v)) ? null : v); return o; };
for (const [grid, out, eng] of [["grid_rx.json", "js_rx_outputs.json", X], ["grid_rxmod.json", "js_rxmod_outputs.json", M]]) {
  const G = JSON.parse(fs.readFileSync(grid, "utf8"));
  fs.writeFileSync(out, JSON.stringify({ version: eng.VERSION, records: G.map((p) => clean(eng.model(p))) }));
  console.log("wrote", out, G.length);
}
