#!/usr/bin/env python3
"""SkyScape MSFS build entry point.

This starter script intentionally does not download or redistribute third-party
imagery. Add source-specific processing after verifying the dataset licence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "regions.json"


def load_regions() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a SkyScape MSFS region")
    parser.add_argument("--region", required=True, help="Region key from config/regions.json")
    args = parser.parse_args()

    config = load_regions()
    regions = config.get("regions", {})

    if args.region not in regions:
        available = ", ".join(regions) or "none"
        raise SystemExit(f"Unknown region '{args.region}'. Available regions: {available}")

    region = regions[args.region]
    print(f"SkyScape MSFS build: {args.region}")
    print(f"Description: {region.get('description', '')}")
    print(f"Bounding box: {region.get('bbox')}")
    print("Processing pipeline is not configured yet.")
    print("Next stages: source ingestion -> reprojection -> tiling -> MSFS packaging.")


if __name__ == "__main__":
    main()
