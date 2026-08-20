#!/usr/bin/env python3
from pathlib import Path
import argparse
from skyscape.imagery import tile_local_raster
from skyscape.config import get_region
def main():
 p=argparse.ArgumentParser(description='Convert a licensed GeoTIFF into MSFS aerial PNG tiles'); p.add_argument('input',type=Path); p.add_argument('--region'); p.add_argument('--bbox',nargs=4,type=float); p.add_argument('--lod',type=int,default=18); p.add_argument('--output',type=Path,default=Path('build/tiles')); a=p.parse_args(); bbox=get_region(a.region).bbox if a.region else tuple(a.bbox) if a.bbox else None
 if bbox is None:p.error('provide --region or --bbox')
 print(f'Created {tile_local_raster(a.input,bbox,a.lod,a.output)} tiles in {a.output}')
if __name__=='__main__': main()
