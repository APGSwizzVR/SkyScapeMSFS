from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from . import __version__
from .config import load_config, get_region
from .cesium import account, configured_asset_ids, choose_assets
from .pipeline import build


def main() -> None:
    load_dotenv()
    cfg = load_config()

    parser = argparse.ArgumentParser(
        prog="skyscape",
        description="SkyScape MSFS 2024 scenery generator",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="Check local configuration and SDK tools")

    assets = sub.add_parser("assets", help="Show configured Cesium assets")
    assets.add_argument("--auto", action="store_true", help="Discover usable Cesium assets")

    b = sub.add_parser("build", help="Build scenery for a region or bounding box")
    b.add_argument("--region")
    b.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("WEST", "SOUTH", "EAST", "NORTH"),
    )
    b.add_argument("--world", action="store_true")
    b.add_argument("--quality", choices=list(cfg["quality"]), default="balanced")
    b.add_argument("--imagery", type=Path)
    b.add_argument("--dem", type=Path)
    b.add_argument("--output", type=Path, default=Path(os.getenv("SKYSCAPE_BUILD_DIR", "build")))
    b.add_argument("--no-buildings", action="store_true")

    args = parser.parse_args()

    if args.cmd == "doctor":
        token = os.getenv("CESIUM_ION_TOKEN", "").strip()
        print(f"SkyScape {__version__}")
        print(f"Cache: {os.getenv('SKYSCAPE_CACHE_DIR', '.cache/skyscape')}")
        print(f"Cesium token: {'configured' if token else 'NOT CONFIGURED'}")
        print(f"MSFS Package Tool: {os.getenv('MSFS_PACKAGE_TOOL', 'auto-detect')}")
        return

    if args.cmd == "assets":
        try:
            info = account()
            print("Cesium account:", info.get("id", "unknown"))
        except Exception as exc:
            print("Cesium account: unavailable")
            print("Reason:", exc)
            return
        ids = choose_assets() if args.auto else configured_asset_ids()
        print("Selected asset IDs:", json.dumps(ids, indent=2))
        return

    if args.region:
        region = get_region(args.region)
        bbox = region.bbox
        name = args.region
    elif args.bbox:
        bbox = tuple(args.bbox)
        name = "custom"
    elif args.world:
        bbox = (-180.0, -85.05112878, 180.0, 85.05112878)
        name = "world"
    else:
        parser.error("choose --region, --bbox, or --world")
        return

    if name == "world" and args.quality in ("high", "ultra"):
        parser.error("world high/ultra builds must be split into regional jobs")

    result = build(
        name,
        bbox,
        args.quality,
        args.imagery,
        args.dem,
        args.output,
        True,
        not args.no_buildings,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
