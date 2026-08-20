from __future__ import annotations
import json
from pathlib import Path
from .config import load_config
from .cesium import token,endpoint,choose_assets
from .imagery import tile_local_raster,fetch_imagery
from .terrain import tile_dem
from .buildings import fetch_osm_buildings,buildings_geojson
from .msfs import create_aerial_project,package
def build(name,bbox,quality,imagery=None,dem=None,output=Path('build'),auto_cesium=True,buildings=True):
 z=int(load_config()['quality'][quality]['max_lod']);root=Path(output)/name;root.mkdir(parents=True,exist_ok=True);img=root/'PackageSources'/'CGL'/'aerial_images';terrain=root/'terrain_tiles';data=root/'data';data.mkdir(parents=True,exist_ok=True);result={'name':name,'quality':quality,'lod':z,'output':str(root),'imagery_tiles':0,'terrain_tiles':0,'buildings':0}
 if imagery:result['imagery_tiles']=tile_local_raster(imagery,bbox,z,img)
 elif auto_cesium:
  ids=choose_assets();iid=ids.get('imagery')
  if iid:
   result['imagery_tiles']=fetch_imagery(endpoint(iid),bbox,z,img,token());result['imagery_asset_id']=iid
 if dem:result['terrain_tiles']=tile_dem(dem,bbox,z,terrain)
 if buildings:
  raw=fetch_osm_buildings(bbox,data/'buildings.json');geo=buildings_geojson(raw,data/'buildings.geojson',bbox);result['buildings_geojson']=str(geo);result['buildings']=len(json.loads(Path(geo).read_text())['features'])
 if result['imagery_tiles']:
  proc=package(create_aerial_project(root,name));result.update(package_returncode=proc.returncode,package_stdout=proc.stdout[-4000:],package_stderr=proc.stderr[-4000:])
 else:result['package_status']='not-built-no-imagery'
 (root/'skyscape-build.json').write_text(json.dumps(result,indent=2),encoding='utf-8');return result
