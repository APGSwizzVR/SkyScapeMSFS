# SkyScape MSFS

Global, optimized Microsoft Flight Simulator 2024 scenery-generation pipeline. SkyScape is designed around tiled LOD processing, local caching, source-provider adapters, aerial imagery, terrain, OpenStreetMap-derived buildings, validation, and MSFS package generation.

## Important status
This repository is the architecture and implementation foundation. It does not redistribute Cesium-hosted datasets. Source-data licensing and attribution must be checked before packaging any generated scenery.

## Quick start

1. Install Python 3.11+ (3.13 recommended).
2. Clone this repository.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it on Windows: `.venv\Scripts\activate`
5. Install dependencies: `python -m pip install -r requirements.txt`
6. Copy `.env.example` to `.env`.
7. Put your Cesium ion token in the local `.env` file. **Never commit a real token.**
8. Run `python -m skyscape doctor`.
9. Build a configured region with `python -m skyscape build --region ireland`.

The placeholder in `.env.example` is intentionally `CESIUM ION KEY HERE`.

## Global design
SkyScape is not limited to Ireland or tiny hand-authored areas. Regions are just build presets. The core uses geographic quadtree tiles, LOD selection, disk caching, resumable processing, and provider adapters so the same pipeline can target a bbox, country, continent, or world.

Examples:

```text
python -m skyscape build --region ireland
python -m skyscape build --region uk
python -m skyscape build --bbox 53.0,-7.0,54.0,-5.5
python -m skyscape build --world --quality balanced
```

`--world` is an orchestration mode; it must not imply downloading the entire planet at maximum resolution. LOD and caching keep processing bounded and reusable.

## Architecture

- `skyscape/cli.py` — command line interface
- `skyscape/config.py` — settings and regions
- `skyscape/cesium.py` — Cesium ion authentication and asset discovery
- `skyscape/tiling.py` — quadtree/LOD tile planning
- `skyscape/cache.py` — content-addressed local cache
- `skyscape/imagery.py` — imagery pipeline scaffolding
- `skyscape/terrain.py` — terrain pipeline scaffolding
- `skyscape/buildings.py` — OSM/building pipeline scaffolding
- `skyscape/msfs.py` — MSFS 2024 aerial/CGL package scaffolding
- `skyscape/validation.py` — build validation

Microsoft's MSFS 2024 SDK documents the SimpleAerial workflow and CGL-based aerial imagery packages. Cesium ion provides authenticated asset access and tiled assets. See the official documentation links in `docs/`.
