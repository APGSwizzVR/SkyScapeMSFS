from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"config"/"regions.json"

@dataclass(frozen=True)
class Region:
    name:str
    bbox:tuple[float,float,float,float]
    description:str=""

def load_config():
    return json.loads(CONFIG.read_text(encoding="utf-8"))

def get_region(name:str)->Region:
    data=load_config()["regions"]
    if name not in data: raise KeyError(name)
    r=data[name]
    return Region(name,tuple(r["bbox"]),r.get("description",""))
