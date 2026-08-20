from __future__ import annotations
import os
import requests

API="https://api.cesium.com/v1"

def get_token()->str:
    token=os.getenv("CESIUM_ION_TOKEN","").strip()
    if not token or token == "CESIUM ION KEY HERE":
        raise RuntimeError("Cesium ion token is not configured. Copy .env.example to .env and replace CESIUM ION KEY HERE with your token.")
    return token

def headers()->dict[str,str]:
    return {"Authorization":f"Bearer {get_token()}"}

def check_token()->dict:
    r=requests.get(f"{API}/me",headers=headers(),timeout=20)
    r.raise_for_status()
    return r.json()

def asset_endpoint(asset_id:int)->dict:
    r=requests.get(f"{API}/assets/{asset_id}/endpoint",headers=headers(),timeout=30)
    r.raise_for_status()
    return r.json()
