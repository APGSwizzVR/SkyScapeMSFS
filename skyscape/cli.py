from __future__ import annotations
import argparse,os,json
from pathlib import Path
from dotenv import load_dotenv
from . import __version__
from .config import load_config,get_region
from .cesium import account,configured_asset_ids,choose_assets
from .pipeline import build
def main():
 load_dotenv();cfg=load_config();p=argparse.ArgumentParser(prog='skyscape',description='SkyScape MSFS 2024 scenery generator');s=p.add_subparsers(dest='cmd',required=True);s.add_parser('doctor');a=s.add_parser('assets');a.add_argument('--auto',action='store_true');b=s.add_parser('build');b.add_argument('--region');b.add_argument('--bbox',nargs=4,type=float,metavar=('WEST','SOUTH','EAST','NORTH'));b.add_argument('--world',action='store_true');b.add_argument('--quality',choices=list(cfg['quality']),default='balanced');b.add_argument('--imagery',type=Path);b.add_argument('--dem',type=Path);b.add_argument('--output',type=Path,default=Path(os.getenv('SKYSCAPE_BUILD_DIR','build')));b.add_argument('--no-buildings',action='store_true');x=p.parse_args()
 if x.cmd=='doctor':print(f'SkyScape {__version__}
Cache: {os.getenv("SKYSCAPE_CACHE_DIR",".cache/skyscape")}
Cesium token: {"configured" if os.getenv("CESIUM_ION_TOKEN") and os.getenv("CESIUM_ION_TOKEN")!="CESIUM ION KEY HERE" else "NOT CONFIGURED"}
MSFS Package Tool: {os.getenv("MSFS_PACKAGE_TOOL") or "auto-detect"}');return
 if x.cmd=='assets':print('Cesium account:',account().get('id'));print('Selected asset IDs:',choose_assets() if x.auto else configured_asset_ids());return
 if x.region:r=get_region(x.region);bbox=r.bbox;name=x.region
 elif x.bbox:bbox=tuple(x.bbox);name='custom'
 elif x.world:bbox=(-180,-85.05112878,180,85.05112878);name='world'
 else:p.error('choose --region, --bbox or --world')
 if name=='world' and x.quality in ('high','ultra'):p.error('world high/ultra must be split into regional jobs')
 print(json.dumps(build(name,bbox,x.quality,x.imagery,x.dem,x.output,True,not x.no_buildings),indent=2))
