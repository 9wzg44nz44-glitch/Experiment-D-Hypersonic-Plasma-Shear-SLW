(* Run on a machine with Wolfram:  wolframscript -file wolfram/ExptDRx_RunGrid.wl   (repo root; grids in ./sim/)
   v0.3 receiver-chain cross-check: evaluates the twin on grid_rx.json (main engine) and grid_rxmod.json (modulation engine),
   writes wl_rx_outputs.json + wl_rxmod_outputs.json; then in sim/:
   node dump_js_rx.mjs && node compare_outputs.mjs js_rx_outputs.json wl_rx_outputs.json 1e-9 && node compare_outputs.mjs js_rxmod_outputs.json wl_rxmod_outputs.json 1e-9 *)
dir = If[$InputFileName =!= "", ParentDirectory[DirectoryName[$InputFileName]], Directory[]];
Get[FileNameJoin[{dir, "wolfram", "ExptDDetect.wl"}]];
toNum[v_] := If[NumericQ[v], N[v], v];
clean[x_] := x /. {Infinity -> Null, -Infinity -> Null, DirectedInfinity[_] -> Null};
Do[
  With[{gridFile = SelectFirst[{FileNameJoin[{dir, job[[1]]}], FileNameJoin[{dir, "sim", job[[1]]}]}, FileExistsQ]},
   With[{recs = clean[job[[3]][toNum /@ Association[#]]] & /@ Import[gridFile, "RawJSON"]},
    Export[FileNameJoin[{DirectoryName[gridFile], job[[2]]}], <|"version" -> exptDVersion, "records" -> recs|>, "RawJSON"];
    Print["wrote ", job[[2]], ": ", Length[recs], " records, ", exptDVersion]]],
  {job, {{"grid_rx.json", "wl_rx_outputs.json", exptDModel}, {"grid_rxmod.json", "wl_rxmod_outputs.json", exptDModModel}}}];
