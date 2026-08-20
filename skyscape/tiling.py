from __future__ import annotations
import math
from dataclasses import dataclass
WEB_MERCATOR_MAX_LAT = 85.05112878
@dataclass(frozen=True)
class Tile:
    z: int
    x: int
    y: int
def lonlat_to_tile(lon: float, lat: float, z: int) -> Tile:
    lat=max(-WEB_MERCATOR_MAX_LAT,min(WEB_MERCATOR_MAX_LAT,lat)); n=2**z
    x=int((lon+180.0)/360.0*n); latr=math.radians(lat)
    y=int((1.0-math.asinh(math.tan(latr))/math.pi)/2.0*n)
    return Tile(z,max(0,min(n-1,x)),max(0,min(n-1,y)))
def tile_bounds(tile: Tile):
    n=2**tile.z; west=tile.x/n*360-180; east=(tile.x+1)/n*360-180
    def lat(y): return math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n))))
    return west,lat(tile.y+1),east,lat(tile.y)
def tiles_for_bbox(bbox,z):
    west,south,east,north=bbox
    if west>east: raise ValueError("Dateline-crossing bbox must be split")
    a=lonlat_to_tile(west,north,z); b=lonlat_to_tile(east,south,z)
    for x in range(min(a.x,b.x),max(a.x,b.x)+1):
        for y in range(min(a.y,b.y),max(a.y,b.y)+1): yield Tile(z,x,y)
def quadkey(tile):
    out=[]
    for i in range(tile.z,0,-1):
        d=0; mask=1<<(i-1)
        if tile.x&mask:d+=1
        if tile.y&mask:d+=2
        out.append(str(d))
    return ''.join(out)
def parse_quadkey(value):
    z=len(value); x=y=0
    for i,c in enumerate(value):
        d=int(c)
        if d not in (0,1,2,3): raise ValueError(f"Invalid quadkey digit: {c}")
        mask=1<<(z-i-1)
        if d&1:x|=mask
        if d&2:y|=mask
    return Tile(z,x,y)
