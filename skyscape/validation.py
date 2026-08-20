from __future__ import annotations
from pathlib import Path

def validate(root:Path)->list[str]:
    errors=[]
    if not root.exists(): errors.append(f"Build directory does not exist: {root}")
    return errors
