from __future__ import annotations
import argparse,os
from pathlib import Path
from dotenv import load_dotenv
from . import __version__
from .config import get_region,load_config
from .tiling import tiles_for_bbox
from .terrain import plan_terrain
from .buildings import plan_buildings
from .cache import cache_root
from .cesium import check_token,configured_asset_ids,CesiumError
from .msfs import sdk_tool
from .validation import validate_sdk
from .pipeline import build_from_local_sources
def main():
    load_dotenv(); p=argparse.ArgumentParser(prog='skyscape',description='Global optimized MSFS 2024 scenery pipeline'); sub=p.add_subparsers(dest='cmd',required=True); sub.add_parser('doctor'); assets=sub.add_parser('assets'); assets.add_argument('--check',action='store_true'); b=sub.add_parser('build'); b.add_argument('--region'); b.add_argument('--bbox',nargs=4,type=float,metavar=('WEST','SOUTH','EAST','NORTH')); b.add_argument('--world',action='store_true'); b.add_argument('--quality',choices=list(load_config()['quality']),default='balanced'); b.add_argument('--imagery',type=Path,help='Licensed local GeoTIFF imagery'); b.add_argument('--dem',type=Path,help='Licensed local DEM GeoTIFF'); b.add_argument('--output',type=Path,default=Path(os.getenv('SKYSCAPE_BUILD_DIR','build'))); args=p.parse_args()
    if args.cmd=='doctor':
        print(f'SkyScape {__version__}'); print(f'Cache: {cache_root()}'); token=os.getenv('CESIUM_ION_TOKEN','').strip(); print('Cesium token: configured' if token and token!='CESIUM ION KEY HERE' else 'Cesium token: NOT CONFIGURED'); print(f'MSFS Package Tool: {sdk_tool()}'); [print(f'SDK: {e}') for e in validate_sdk()]; return
    if args.cmd=='assets':
        try: print(f'Cesium account: {check_token().get("id","authenticated")}'); print(f'Configured asset IDs: {configured_asset_ids() or "none"}')
        except CesiumError as exc: raise SystemExit(str(exc))
        return
    if args.cmd=='build':
        if args.region: region=get_region(args.region); bbox=region.bbox; name=args.region
        elif args.bbox: bbox=tuple(args.bbox); name='custom'
        elif args.world: bbox=(-180.0,-85.05112878,180.0,85.05112878); name='world'
        else: p.error('choose --region, --bbox, or --world')
        lod=int(load_config()['quality'][args.quality]['max_lod']); count=len(list(tiles_for_bbox(bbox,lod))); print(f'SkyScape build: {name}'); print(f'Quality: {args.quality} | max LOD: {lod}'); print(f'BBox: {bbox}'); print(f'Aerial tiles at selected LOD: {count}')
        if not args.imagery and not args.dem: print('Planning-only build: provide --imagery and/or --dem to process real licensed source data.'); print(f'Terrain plan: {plan_terrain(bbox,lod)}'); print(f'Buildings plan: {plan_buildings(bbox)}'); return
        print(build_from_local_sources(name,bbox,args.quality,args.imagery,args.dem,args.output))
