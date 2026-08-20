from __future__ import annotations
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from rasterio.warp import reproject
from PIL import Image
from .tiling import tiles_for_bbox,tile_bounds,quadkey
def plan_terrain(bbox,max_lod): return {'bbox':tuple(bbox),'max_lod':max_lod,'tiles':len(list(tiles_for_bbox(tuple(bbox),max_lod))),'status':'ready-for-source'}
def tile_dem(source,bbox,lod,output_dir,size=256):
    if not source.exists(): raise FileNotFoundError(source)
    output_dir.mkdir(parents=True,exist_ok=True); tiles=list(tiles_for_bbox(tuple(bbox),lod))
    with rasterio.open(source) as src:
        if src.crs is None: raise ValueError('DEM has no CRS')
        for tile in tiles:
            west,south,east,north=tile_bounds(tile); transform=from_bounds(west,south,east,north,size,size); dst=np.zeros((size,size),dtype=np.float32)
            reproject(source=rasterio.band(src,1),destination=dst,src_transform=src.transform,src_crs=src.crs,dst_transform=transform,dst_crs='EPSG:4326',resampling=Resampling.bilinear,dst_nodata=0)
            lo,hi=np.nanpercentile(dst,[0.1,99.9]); hi=max(hi,lo+1.0); normalized=np.clip((dst-lo)/(hi-lo),0,1)
            Image.fromarray((normalized*65535).astype(np.uint16),mode='I;16').save(output_dir/f'{quadkey(tile)}.png')
    return len(tiles)
