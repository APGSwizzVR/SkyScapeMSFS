# SkyScape roadmap

## Core architecture
- [x] Global region model and bbox builds
- [x] Quality/LOD profiles
- [x] Quadtree tile planning
- [x] Local cache foundation
- [x] Cesium ion token integration point
- [x] Provider-separated imagery/terrain/buildings modules
- [x] CLI and doctor command

## Implementation stages
- [ ] Implement permitted Cesium asset ingestion/export paths
- [ ] Implement source-specific imagery reprojection/resampling
- [ ] Generate SDK-valid MSFS 2024 aerial CGLs
- [ ] Add terrain conversion where the source licence permits it
- [ ] Add OSM-derived building generation and packaging
- [ ] Add resumable workers and parallel tile processing
- [ ] Add LOD-aware disk/memory budgets
- [ ] Add automated MSFS package validation
- [ ] Add GUI
- [ ] Expand global provider profiles

The architecture intentionally supports the whole world while keeping high resolution local and bounded by LOD.
