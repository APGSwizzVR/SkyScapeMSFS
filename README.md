# SkyScape MSFS

SkyScape is a Windows-friendly pipeline for turning **licensed geospatial source data** into optimized Microsoft Flight Simulator 2024 scenery.

## What is implemented

- Global, continent, country and custom-bbox tile planning
- Quadtree/quadkey LOD handling
- Local cache foundation
- Cesium ion authentication and asset inspection
- Licensed GeoTIFF imagery -> 256x256 aerial PNG tiles
- MSFS CGL project generation
- Automatic `fspackagetool.exe` invocation
- Build validation
- DEM preprocessing
- OpenStreetMap building acquisition foundation
- CLI commands for doctor, assets and build

Microsoft's MSFS 2024 SDK documentation specifies 256x256 aerial PNG input tiles named by quadkey and a `CGLBuilder` XML configuration; the Package Tool compiles those source tiles into CGL output.

## Setup

```bat
python -m pip install -r requirements.txt
python -m skyscape doctor
```

Create `.env` from `.env.example`. Never commit `.env` or a real token.

## Build real aerial scenery

SkyScape currently expects a **licensed local GeoTIFF** for the actual aerial conversion.

```bat
python -m skyscape build --region ireland --quality high --imagery "D:\Data\ireland.tif"
```

Or:

```bat
python -m skyscape build --bbox -6.6 53.2 -6.0 53.6 --quality high --imagery "D:\Data\dublin.tif"
```

The project is generated under `build\<name>` and the installed MSFS Package Tool is called automatically when imagery tiles exist.

For direct raster preprocessing:

```bat
python scripts/process_raster.py "D:\Data\imagery.tif" --region ireland --lod 18 --output build\tiles
```

## Cesium

Check the authenticated Cesium account and configured asset IDs:

```bat
python -m skyscape assets --check
```

A Cesium token is authentication, not a blanket licence to redistribute imagery or terrain. Only package data whose provider terms allow the intended distribution.

## World support

```bat
python -m skyscape build --world --quality balanced
```

World mode is an orchestration/coverage mode. It must not be treated as a request to generate the entire planet at maximum LOD in one job. The number of tiles grows exponentially with LOD, so production builds should use regional jobs and cached data.

## MSFS SDK

```env
MSFS_SDK_PATH=C:\MSFS 2024 SDK
MSFS_PACKAGE_TOOL=C:\MSFS 2024 SDK\Tools\bin\fspackagetool.exe
```

The external Package Tool is supplied by the MSFS 2024 SDK.
