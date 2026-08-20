#!/usr/bin/env python3
"""Placeholder for licensed raster processing.

The eventual implementation will reproject, clip, validate, and tile imagery
for a selected region. It will only operate on source data the user is allowed
to process and redistribute.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Process a SkyScape raster")
    parser.add_argument("input", type=Path, help="Input raster")
    parser.add_argument("output", type=Path, help="Output directory")
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input does not exist: {args.input}")

    args.output.mkdir(parents=True, exist_ok=True)
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print("Raster processing implementation will be added after the source format is selected.")


if __name__ == "__main__":
    main()
