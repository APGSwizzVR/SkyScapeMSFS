from __future__ import annotations
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from .config import get_region,load_config
from .tiling import tiles_for_bbox
from .imagery import plan_imagery
from .terrain import plan_terrain
from .buildings import plan_buildings
from .cache import cache_root
from .validation import validate

def main():
    load_dotenv()
    p=argparse.ArgumentParser(prog="skyscape",description="Global optimized MSFS 2024 scenery pipeline")
    sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("doctor")
    b=sub.add_parser("build")
    b.add_argument("--region")
    b.add_argument("--bbox",nargs=4,type=float,metavar=("WEST","SOUTH","EAST","NORTH"))
    b.add_argument("--world",action="store_true")
    b.add_argument("--quality",choices=list(load_config()["quality"]),default="balanced")
    args=p.parse_args()
    if args.cmd=="doctor":
        print("SkyScape 0.2.0")
        print(f"Cache: {cache_root()}")
        token=os.getenv("CESIUM_ION_TOKEN","").strip()
        print("Cesium token: configured" if token and token!="CESIUM ION KEY HERE" else "Cesium token: NOT CONFIGURED")
        return
    if args.cmd=="build":
        if args.region:
            region=get_region(args.region); bbox=region.bbox; name=args.region
        elif args.bbox:
            bbox=tuple(args.bbox); name="custom"
        elif args.world:
            bbox=(-180.0,-85.05112878,180.0,85.05112878); name="world"
        else: p.error("choose --region, --bbox, or --world")
        q=load_config()["quality"][args.quality]; lod=q["max_lod"]
        print(f"SkyScape build: {name}")
        print(f"Quality: {args.quality} | max LOD: {lod}")
        print(f"BBox: {bbox}")
        print(f"Imagery tile plan: {len(plan_imagery(bbox,lod))} tiles at LOD {lod}")
        print(f"Terrain: {plan_terrain(bbox,lod)}")
        print(f"Buildings: {plan_buildings(bbox)}")
        print("Data acquisition and MSFS CGL packaging are provider/SDK stages; no restricted dataset is downloaded by this planning command.")
        return
