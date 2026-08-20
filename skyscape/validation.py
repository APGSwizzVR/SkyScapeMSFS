from __future__ import annotations
from pathlib import Path
import re
from .msfs import sdk_tool
def validate(root:Path):
    errors=[]
    if not root.exists(): errors.append(f'Build directory does not exist: {root}')
    if root.exists() and not (root/'PackageDefinitions').exists(): errors.append('Missing PackageDefinitions')
    if root.exists() and not (root/'PackageSources'/'CGL'/'CGLBuilderConfig.xml').exists(): errors.append('Missing CGLBuilderConfig.xml')
    tiles=(root/'PackageSources'/'CGL'/'aerial_images') if root.exists() else None
    if tiles and tiles.exists():
        for tile in tiles.glob('*.png'):
            if not re.fullmatch(r'[0-3]+',tile.stem): errors.append(f'Invalid aerial tile name: {tile.name}')
    return errors
def validate_sdk():
    tool=sdk_tool(); return [] if tool.exists() else [f'MSFS Package Tool not found: {tool}']
