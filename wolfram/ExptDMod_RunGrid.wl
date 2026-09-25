(* Run on a machine with Wolfram:  wolframscript -file wolfram/ExptDMod_RunGrid.wl   (repo root; grid_mod.json in ./sim/)
   Evaluates the sheath-modulation twin (physics v0.3; n(f) uses the v0.3 receiver chain) on grid_mod.json and writes wl_mod_outputs.json; then in sim/:
   node dump_js_mod.mjs && node compare_outputs.mjs js_mod_outputs.json wl_mod_outputs.json 1e-9 *)
dir = If[$InputFileName =!= "", ParentDirectory[DirectoryName[$InputFileName]], Directory[]];
Get[FileNameJoin[{dir, "wolfram", "ExptDDetect.wl"}]];
gridFile = SelectFirst[{FileNameJoin[{dir, "grid_mod.json"}], FileNameJoin[{dir, "sim", "grid_mod.json"}]}, FileExistsQ];
grid = Import[gridFile, "RawJSON"];
toNum[v_] := If[NumericQ[v], N[v], v];
recs = (exptDModModel[toNum /@ Association[#]] /. {Infinity -> Null, DirectedInfinity[_] -> Null}) & /@ grid;
Export[FileNameJoin[{DirectoryName[gridFile], "wl_mod_outputs.json"}], <|"version" -> exptDVersion, "records" -> recs|>, "RawJSON"];
Print["wrote wl_mod_outputs.json: ", Length[recs], " records, ", exptDVersion];
