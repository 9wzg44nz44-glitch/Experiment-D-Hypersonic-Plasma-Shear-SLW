// compare_outputs.mjs A.json B.json [relTol=1e-9] — PASS/FAIL per number (rel tol; exact for strings/null)
import fs from "fs";
const [a = "js_outputs.json", b = "py_outputs.json", rt = "1e-9"] = process.argv.slice(2);
if (!fs.existsSync(b)) { console.error(`${b} not found`); process.exit(2); }
const A = JSON.parse(fs.readFileSync(a, "utf8")), B = JSON.parse(fs.readFileSync(b, "utf8"));
const relTol = +rt; let pass = 0, fail = 0, worst = 0, worstAt = "";
function cmp(x, y, p) {
  if (typeof x === "number" && typeof y === "number") {
    const d = Math.abs(x - y), r = d === 0 ? 0 : d / Math.max(Math.abs(x), Math.abs(y));
    if (r <= relTol) pass++; else { fail++; if (fail <= 20) console.error(`FAIL ${p}: ${x} vs ${y} rel=${r.toExponential(2)}`); }
    if (r > worst) { worst = r; worstAt = p; } return;
  }
  if (Array.isArray(x)) { if (!Array.isArray(y) || x.length !== y.length) { fail++; console.error(`LEN ${p}`); return; } x.forEach((v, i) => cmp(v, y[i], `${p}[${i}]`)); return; }
  if (x && typeof x === "object") { for (const k of new Set([...Object.keys(x), ...Object.keys(y || {})])) { if (!y || !(k in y) || !(k in x)) { fail++; console.error(`KEY ${p}.${k}`); continue; } cmp(x[k], y[k], `${p}.${k}`); } return; }
  if (x === y) pass++; else { fail++; if (fail <= 20) console.error(`FAIL ${p}: ${JSON.stringify(x)} vs ${JSON.stringify(y)}`); }
}
cmp(A, B, "$");
console.log(`${a} vs ${b}: PASS ${pass} / FAIL ${fail} (rel tol ${relTol}); worst rel ${worst.toExponential(2)} at ${worstAt}; versions ${A.version} | ${B.version}`);
process.exit(fail ? 1 : 0);
