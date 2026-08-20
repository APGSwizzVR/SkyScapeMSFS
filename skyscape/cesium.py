from __future__ import annotations
import os,requests
API="https://api.cesium.com/v1"
class CesiumError(RuntimeError):pass
def token():
 t=os.getenv("CESIUM_ION_TOKEN","").strip()
 if not t or t=="CESIUM ION KEY HERE":raise CesiumError("CESIUM_ION_TOKEN is not configured")
 return t
def get(path,params=None,timeout=60):
 r=requests.get(API+path,headers={"Authorization":f"Bearer {token()}"},params=params,timeout=timeout)
 if not r.ok:raise CesiumError(f"Cesium HTTP {r.status_code}: {r.text[:500]}")
 return r.json()
def account():return get("/me")
def assets(types=None):
 p={"status":"COMPLETE"}
 if types:p["type"]=','.join(types)
 return get("/assets",p).get("items",[])
def configured_asset_ids():
 out={}
 for k in ("imagery","terrain","buildings"):
  v=os.getenv(f"CESIUM_{k.upper()}_ASSET_ID","").strip()
  if v:out[k]=int(v)
 return out
def endpoint(asset_id):return get(f"/assets/{int(asset_id)}/endpoint")
def choose_assets():
 ids=configured_asset_ids()
 for a in assets(["IMAGERY","TERRAIN","3DTILES"]):
  k={"IMAGERY":"imagery","TERRAIN":"terrain","3DTILES":"buildings"}.get(a.get("type"))
  if k and k not in ids:ids[k]=a["id"]
 return ids
