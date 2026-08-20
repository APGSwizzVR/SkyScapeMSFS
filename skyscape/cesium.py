from __future__ import annotations
import os,requests
API='https://api.cesium.com/v1'
class CesiumError(RuntimeError): pass
def get_token():
    token=os.getenv('CESIUM_ION_TOKEN','').strip()
    if not token or token=='CESIUM ION KEY HERE': raise CesiumError('Cesium ion token is not configured')
    return token
def headers(): return {'Authorization':f'Bearer {get_token()}'}
def request_json(url,timeout=60):
    try:r=requests.get(url,headers=headers(),timeout=timeout)
    except requests.RequestException as exc: raise CesiumError(f'Cesium request failed: {exc}') from exc
    if not r.ok: raise CesiumError(f'Cesium returned HTTP {r.status_code}: {r.text[:500]}')
    return r.json()
def check_token(): return request_json(f'{API}/me',20)
def asset_endpoint(asset_id): return request_json(f'{API}/assets/{asset_id}/endpoint',30)
def configured_asset_ids():
    result={}
    for name in ('imagery','terrain'):
        raw=os.getenv(f'CESIUM_{name.upper()}_ASSET_ID','').strip()
        if raw:
            try: result[name]=int(raw)
            except ValueError as exc: raise CesiumError(f'CESIUM_{name.upper()}_ASSET_ID must be an integer') from exc
    return result
