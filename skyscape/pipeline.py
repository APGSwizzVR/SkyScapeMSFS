from __future__ import annotations
import json
from pathlib import Path
from .config import load_config
from .imagery import tile_local_raster
from .terrain import tile_dem
from .msfs import create_aerial_project,package
from .validation import validate
def build_from_local_sources(name,bbox,quality,imagery,dem,output_root):
    lod=int(load_config()['quality'][quality]['max_lod']); root=output_root/name; tiles_dir=root/'PackageSources'/'CGL'/'aerial_images'; result={'name':name,'lod':lod,'output':str(root),'imagery_tiles':0,'terrain_tiles':0,'package':None}
    if imagery: result['imagery_tiles']=tile_local_raster(imagery,tuple(bbox),lod,tiles_dir)
    if dem: result['terrain_tiles']=tile_dem(dem,tuple(bbox),lod,root/'terrain_tiles')
    project=create_aerial_project(root,name); errors=validate(root)
    if errors: raise RuntimeError('Build validation failed: '+'; '.join(errors))
    if result['imagery_tiles']:
        proc=package(project); result['package']={'returncode':proc.returncode,'stdout':proc.stdout[-4000:],'stderr':proc.stderr[-4000:]}
        if proc.returncode!=0: raise RuntimeError(proc.stderr or proc.stdout or 'Package Tool failed')
    else: result['package']={'status':'not-run','reason':'No imagery source supplied'}
    (root/'skyscape-build.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); return result
