(* Publish the Cloud twin (Dan's account). Run on a machine with Wolfram after CloudConnect["..."] as danbritton5.
   Target: https://www.wolframcloud.com/obj/danbritton5/ExptDDetect   (NOT yet published) *)
dir = If[$InputFileName =!= "", ParentDirectory[DirectoryName[$InputFileName]], Directory[]];
Get[FileNameJoin[{dir, "wolfram", "ExptDDetect.wl"}]];
obj = CloudDeploy[exptDManipulate[], CloudObject["ExptDDetect"], Permissions -> "Public"];
Print["published ", exptDVersion, " -> ", obj];
