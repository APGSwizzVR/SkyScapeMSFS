from __future__ import annotations
from dataclasses import dataclass
from math import floor,pi,tan,sinh,log
@dataclass(frozen=True)
class Tile:
 z:int; x:int; y:int
 @property
 def quadkey(self):
  q=[]
  for i in range(self.z,0,-1):
   d=0;m=1<<(i-1)
   if self.x&m:d+=1
   if self.y&m:d+=2
   q.append(str(d))
  return ''.join(q)
def lonlat_to_tile(lon,lat,z):
 lat=max(-85.05112878,min(85.05112878,lat));n=1<<z;x=floor((lon+180)/360*n);y=floor((1-log(tan(lat*pi/180+pi/4))/pi)/2*n);return Tile(z,x,y)
def tiles_for_bbox(bbox,z):
 w,s,e,n=bbox;a=lonlat_to_tile(w,s,z);b=lonlat_to_tile(e,n,z);return [Tile(z,x,y) for y in range(min(a.y,b.y),max(a.y,b.y)+1) for x in range(min(a.x,b.x),max(a.x,b.x)+1)]
