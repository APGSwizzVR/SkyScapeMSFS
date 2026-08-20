from __future__ import annotations
from pathlib import Path
from .tiling import tiles_for_bbox,quadkey

def plan_imagery(bbox, max_lod:int):
    return [{"z":t.z,"x":t.x,"y":t.y,"quadkey":quadkey(t)} for t in tiles_for_bbox(bbox,max_lod)]

def prepare_tile(source:Path, output:Path, size:int=256):
    # Source-specific reprojection/resampling belongs here. No third-party imagery is downloaded automatically.
    output.parent.mkdir(parents=True,exist_ok=True)
    return {"source":str(source),"output":str(output),"size":size,"status":"planned"}
