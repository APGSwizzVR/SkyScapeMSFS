from __future__ import annotations
from pathlib import Path
import json,requests
from shapely.geometry import shape,box
OVERPASS='https://overpass-api.de/api/interpreter'
def plan_buildings(bbox): return {'bbox':tuple(bbox),'status':'ready','source':'OpenStreetMap Overpass','redistribution':'verify ODbL attribution before distribution'}
def fetch_osm_buildings(bbox,output:Path):
    west,south,east,north=bbox; query=f'[out:json][timeout:180];(way[building]({south},{west},{north},{east});relation[building]({south},{west},{north},{east}););out geom;'; r=requests.post(OVERPASS,data=query,timeout=210); r.raise_for_status(); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(r.text,encoding='utf-8'); return output
def filter_buildings(input_json:Path,bbox,output_geojson:Path):
    data=json.loads(input_json.read_text(encoding='utf-8')); target=box(*bbox); features=[]
    for element in data.get('elements',[]):
        geometry=element.get('geometry');
        if not geometry or len(geometry)<3: continue
        coords=[(p['lon'],p['lat']) for p in geometry]; poly=shape({'type':'Polygon','coordinates':[coords+[coords[0]]]})
        if not poly.is_valid: poly=poly.buffer(0)
        if poly.is_empty or not poly.intersects(target): continue
        features.append({'type':'Feature','properties':element.get('tags',{}),'geometry':poly.__geo_interface__})
    output_geojson.parent.mkdir(parents=True,exist_ok=True); output_geojson.write_text(json.dumps({'type':'FeatureCollection','features':features}),encoding='utf-8'); return output_geojson
