from __future__ import annotations
from pathlib import Path
import io,requests,math
from PIL import Image
from .world import tiles_for_bbox
def endpoint_template(ep):
 for k in ("url","template","tileUrl","tiles"):
  v=ep.get(k)
  if isinstance(v,str) and "{z}" in v:return v
 raise RuntimeError("Cesium imagery endpoint has no direct tile template; use licensed GeoTIFF/WMTS/TMS data")
def tile_bounds(t):
 n=2**t.z;w=t.x/n*360-180;e=(t.x+1)/n*360-180
 def lat(y):return math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n))))
 return w,lat(t.y+1),e,lat(t.y)
def fetch_imagery(ep,bbox,z,out,access_token):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);template=endpoint_template(ep);count=0
 for t in tiles_for_bbox(bbox,z):
  p=out/f"{t.quadkey}.png"
  if p.exists():count+=1;continue
  url=template.replace("{z}",str(t.z)).replace("{x}",str(t.x)).replace("{y}",str(t.y)).replace("{quadkey}",t.quadkey);r=requests.get(url,params={"access_token":access_token},timeout=90);r.raise_for_status();Image.open(io.BytesIO(r.content)).convert("RGB").save(p,"PNG",optimize=True);count+=1
 return count
def tile_local_raster(source,bbox,z,out,size=256):
 import numpy as np,rasterio
 from rasterio.enums import Resampling
 from rasterio.warp import transform_bounds
 out=Path(out);out.mkdir(parents=True,exist_ok=True);count=0
 with rasterio.open(source) as src:
  if not src.crs:raise ValueError("Source raster has no CRS")
  for t in tiles_for_bbox(bbox,z):
   w,s,e,n=tile_bounds(t);l,b,r,top=transform_bounds("EPSG:4326",src.crs,w,s,e,n,densify_pts=21);win=rasterio.windows.from_bounds(l,b,r,top,src.transform);data=src.read([1,2,3] if src.count>=3 else 1,window=win,out_shape=(min(3,src.count),size,size),resampling=Resampling.bilinear)
   if data.ndim==2:data=np.repeat(data[None,...],3,axis=0)
   Image.fromarray(np.moveaxis(data,0,2).astype(np.uint8)).save(out/f"{t.quadkey}.png");count+=1
 return count
