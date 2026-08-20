from __future__ import annotations
import hashlib,os
from pathlib import Path
def cache_root():
    root=Path(os.getenv('SKYSCAPE_CACHE_DIR','.cache/skyscape')); root.mkdir(parents=True,exist_ok=True); return root
def key_for(value): return hashlib.sha256(value.encode('utf-8')).hexdigest()
def path_for(namespace,key,ext=''):
    digest=key_for(key); p=cache_root()/namespace/digest[:2]; p.mkdir(parents=True,exist_ok=True); return p/(digest+ext)
def atomic_write_bytes(path,data):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+'.tmp'); tmp.write_bytes(data); os.replace(tmp,path)
