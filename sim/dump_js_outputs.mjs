// node dump_js_outputs.mjs -> js_outputs.json, evaluates web/js/slw-detect.js on grid.json
import fs from "fs"; import { createRequire } from "module";
const require = createRequire(import.meta.url);
const cand = ["./web/js/slw-detect.js", "../js/slw-detect.js"]; // sim-lab layout | repo sim/ layout
const M = require(cand.find((f) => fs.existsSync(new URL(f, import.meta.url))));
const G = JSON.parse(fs.readFileSync("grid.json", "utf8"));
const recs = G.map((p) => { const o = M.model(p); for (const k in o) if (o[k] === -Infinity) o[k] = null; return o; });
fs.writeFileSync("js_outputs.json", JSON.stringify({ version: M.VERSION, records: recs }));
console.log("wrote js_outputs.json", recs.length);
