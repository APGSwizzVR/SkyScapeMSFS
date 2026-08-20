# SkyScapeMSFS

Automated MSFS 2024 scenery pipeline for licensed geospatial data.

The current engine includes Cesium ion account/asset discovery, imagery acquisition when an endpoint exposes a tile template, GeoTIFF aerial tiling, DEM tiling, OSM building extraction, quadkey LOD tiling, CGL project generation, and automatic `fspackagetool.exe` invocation.

Setup:
```bat
python -m pip install -r requirements.txt
python -m skyscape doctor
python -m skyscape assets --auto
```

Build a test area:
```bat
python -m skyscape build --bbox -6.6 53.2 -6.0 53.6 --quality performance
```

For local licensed sources:
```bat
python -m skyscape build --bbox -6.6 53.2 -6.0 53.6 --quality performance --imagery D:\Data\imagery.tif --dem D:\Data\terrain.tif
```

A Cesium token authenticates access but does not automatically grant redistribution rights. Verify provider terms before public distribution. OSM-derived building data requires ODbL attribution.
