from __future__ import annotations
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Tile:
    z:int; x:int; y:int

def lonlat_to_tile(lon:float,lat:float,z:int)->Tile:
    lat=max(-85.05112878,min(85.05112878,lat))
    n=2**z
    x=int((lon+180.0)/360.0*n)
    latr=math.radians(lat)
    y=int((1-math.asinh(math.tan(latr))/math.pi)/2*n)
    return Tile(z,max(0,min(n-1,x)),max(0,min(n-1,y)))

def tiles_for_bbox(bbox:tuple[float,float,float,float],z:int):
    west,south,east,north=bbox
    a=lonlat_to_tile(west,north,z); b=lonlat_to_tile(east,south,z)
    for x in range(min(a.x,b.x),max(a.x,b.x)+1):
        for y in range(min(a.y,b.y),max(a.y,b.y)+1): yield Tile(z,x,y)

def quadkey(tile:Tile)->str:
    out=[]
    for i in range(tile.z,0,-1):
        d=0; mask=1<<(i-1)
        if tile.x & mask: d+=1
        if tile.y & mask: d+=2
        out.append(str(d))
    return ''.join(out)
