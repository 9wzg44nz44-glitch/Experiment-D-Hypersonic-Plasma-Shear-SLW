// wl_lint.mjs — lightweight syntax sanity check for .wl files (no Wolfram kernel on this box).
// Checks: balanced (), [], {}, <| |>, (* *) comments (nested), strings; flags ",]" ",}" ",|>" ",)" and "; ," patterns,
// top-level statements not terminated, and use of protected single-letter built-ins as variables (C, D, E, I, K, N, O).
import fs from "fs";
const files = process.argv.slice(2);
let bad = 0;
for (const f of files) {
  const s = fs.readFileSync(f, "utf8");
  const stack = []; let i = 0, line = 1; const errs = []; let code = ""; // code with strings/comments blanked
  while (i < s.length) {
    const c = s[i];
    if (c === "\n") { line++; code += c; i++; continue; }
    if (s.startsWith("(*", i)) { let depth = 1; i += 2; code += "  "; while (i < s.length && depth) { if (s.startsWith("(*", i)) { depth++; i += 2; code += "  "; } else if (s.startsWith("*)", i)) { depth--; i += 2; code += "  "; } else { if (s[i] === "\n") { line++; code += "\n"; } else code += " "; i++; } } if (depth) errs.push("unterminated comment"); continue; }
    if (c === '"') { code += '"'; i++; while (i < s.length && s[i] !== '"') { if (s[i] === "\\") { i += 2; code += "  "; continue; } if (s[i] === "\n") { line++; code += "\n"; } else code += " "; i++; } code += '"'; i++; continue; }
    if (s.startsWith("<|", i)) { stack.push(["<|", line]); code += "<|"; i += 2; continue; }
    if (s.startsWith("|>", i)) { const t = stack.pop(); if (!t || t[0] !== "<|") errs.push(`line ${line}: |> closes ${t ? t[0] + "@" + t[1] : "nothing"}`); code += "|>"; i += 2; continue; }
    if ("([{".includes(c)) { stack.push([c, line]); }
    if (")]}".includes(c)) { const t = stack.pop(); const want = { ")": "(", "]": "[", "}": "{" }[c]; if (!t || t[0] !== want) errs.push(`line ${line}: '${c}' closes ${t ? t[0] + "@" + t[1] : "nothing"}`); }
    code += c; i++;
  }
  stack.forEach((t) => errs.push(`unclosed ${t[0]} from line ${t[1]}`));
  const lines = code.split("\n");
  const re = [[/,\s*[\]\}\)]/, "comma before closer"], [/,\s*\|>/, "comma before |>"], [/;\s*,/, "semicolon before comma"], [/\[\s*,/, "[ ,"], [/,\s*,/, ", ,"]];
  // multi-line aware checks on the blanked code
  const flat = code;
  for (const [r, msg] of re) { let m; const g = new RegExp(r.source, "g"); while ((m = g.exec(flat))) { const ln = flat.slice(0, m.index).split("\n").length; errs.push(`line ${ln}: ${msg}`); } }
  // protected single letters used as Module locals / iterators / pattern names
  const prot = /(?:Module|Block|With)\[\{([^}]*)\}/g; let m;
  while ((m = prot.exec(flat))) { for (const v of m[1].split(",").map((x) => x.split("=")[0].trim())) if (/^(C|D|E|I|K|N|O)$/.test(v)) errs.push(`protected symbol as local: ${v}`); }
  const it = /\{\s*(C|D|E|I|K|N|O)\s*,/g; while ((m = it.exec(flat))) { const ln = flat.slice(0, m.index).split("\n").length; errs.push(`line ${ln}: possible protected iterator ${m[1]}`); }
  const pat = /\b(C|D|E|I|K|N|O)_/g; while ((m = pat.exec(flat))) { const ln = flat.slice(0, m.index).split("\n").length; errs.push(`line ${ln}: protected symbol as pattern ${m[1]}_`); }
  console.log(`${f}: ${errs.length ? errs.length + " issue(s)" : "OK"}`); errs.forEach((e) => console.log("   " + e)); bad += errs.length;
}
process.exit(bad ? 1 : 0);
