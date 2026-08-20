from __future__ import annotations
from pathlib import Path
from PIL import Image
def tile_dem(source,bbox,z,out,size=256):
 import numpy as np,rasterio
 from rasterio.enums import Resampling
 from rasterio.warp import transform_bounds
 from .world import tiles_for_bbox
 from .imagery import tile_bounds
 out=Path(out);out.mkdir(parents=True,exist_ok=True);count=0
 with rasterio.open(source) as src:
  if not src.crs:raise ValueError("DEM has no CRS")
  for t in tiles_for_bbox(bbox,z):
   w,s,e,n=tile_bounds(t);l,b,r,top=transform_bounds("EPSG:4326",src.crs,w,s,e,n,densify_pts=21);win=rasterio.windows.from_bounds(l,b,r,top,src.transform);data=src.read(1,window=win,out_shape=(size,size),resampling=Resampling.bilinear).astype(np.float32);lo,hi=np.nanpercentile(data,[0.1,99.9]);hi=max(hi,lo+1);Image.fromarray((np.clip((data-lo)/(hi-lo),0,1)*65535).astype(np.uint16)).save(out/f"{t.quadkey}.png");count+=1
 return count
