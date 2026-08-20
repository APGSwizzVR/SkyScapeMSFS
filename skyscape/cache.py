from __future__ import annotations
import hashlib
import os
from pathlib import Path

def cache_root()->Path:
    return Path(os.getenv("SKYSCAPE_CACHE_DIR",".cache/skyscape"))

def key_for(value:str)->str:
    return hashlib.sha256(value.encode()).hexdigest()

def path_for(namespace:str,key:str,ext:str="")->Path:
    p=cache_root()/namespace/key_for(key)[:2]
    p.mkdir(parents=True,exist_ok=True)
    return p/(key_for(key)+ext)
