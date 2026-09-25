// node dump_js_mod.mjs -> js_mod_outputs.json : evaluates slw-modulation.js on grid_mod.json
import fs from "fs"; import { createRequire } from "module";
const require = createRequire(import.meta.url);
const cand = ["./web/js/slw-modulation.js", "../js/slw-modulation.js"];
const M = require(cand.find((f) => fs.existsSync(new URL(f, import.meta.url))));
const G = JSON.parse(fs.readFileSync("grid_mod.json", "utf8"));
const recs = G.map((p) => { const o = M.model(p); for (const k in o) if (typeof o[k] === "number" && !isFinite(o[k])) o[k] = null; return o; });
fs.writeFileSync("js_mod_outputs.json", JSON.stringify({ version: M.VERSION, records: recs }));
console.log("wrote js_mod_outputs.json", recs.length);
