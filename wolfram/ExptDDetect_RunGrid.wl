(* Run on a machine with Wolfram:  wolframscript -file wolfram/ExptDDetect_RunGrid.wl   (from /workspace/sim-lab/expt-d, or the repo root: grid.json in ./ or ./sim/)
   Evaluates the twin on grid.json and writes wl_outputs.json; then: node compare_outputs.mjs js_outputs.json wl_outputs.json 1e-9 *)
dir = If[$InputFileName =!= "", ParentDirectory[DirectoryName[$InputFileName]], Directory[]];
Get[FileNameJoin[{dir, "wolfram", "ExptDDetect.wl"}]];
gridFile = SelectFirst[{FileNameJoin[{dir, "grid.json"}], FileNameJoin[{dir, "sim", "grid.json"}]}, FileExistsQ];
grid = Import[gridFile, "RawJSON"];
recs = exptDModel[N /@ #] & /@ (Association /@ grid);
Export[FileNameJoin[{DirectoryName[gridFile], "wl_outputs.json"}], <|"version" -> exptDVersion, "records" -> recs|>, "RawJSON"];
Print["wrote wl_outputs.json: ", Length[recs], " records, ", exptDVersion];
