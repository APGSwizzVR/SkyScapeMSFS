from __future__ import annotations
from pathlib import Path
import json,requests
from shapely.geometry import shape,box
OVERPASS='https://overpass-api.de/api/interpreter'
def fetch_osm_buildings(bbox,out):
 w,s,e,n=bbox;q=f'[out:json][timeout:180];way[building]({s},{w},{n},{e});out geom tags;';r=requests.post(OVERPASS,data=q,timeout=240);r.raise_for_status();Path(out).write_text(r.text,encoding='utf-8');return out
def buildings_geojson(raw,out,bbox):
 data=json.loads(Path(raw).read_text());clip=box(*bbox);features=[]
 for el in data.get('elements',[]):
  g=el.get('geometry')
  if not g or len(g)<4:continue
  c=[(p['lon'],p['lat']) for p in g]
  if c[0]!=c[-1]:c.append(c[0])
  geom=shape({'type':'Polygon','coordinates':[c]})
  if geom.is_valid and geom.intersects(clip):features.append({'type':'Feature','properties':el.get('tags',{}),'geometry':geom.__geo_interface__})
 Path(out).write_text(json.dumps({'type':'FeatureCollection','features':features}),encoding='utf-8');return out
