from __future__ import annotations
from pathlib import Path

def write_aerial_xml(output:Path,name:str,tiles_dir:Path):
    output.parent.mkdir(parents=True,exist_ok=True)
    xml=f"""<?xml version="1.0" encoding="utf-8"?>\n<AssetPackage Name="{name}">\n  <!-- MSFS 2024 aerial CGL definition placeholder. Populate with SDK-validated CGL properties during packaging. -->\n  <Source>{tiles_dir.as_posix()}</Source>\n</AssetPackage>\n"""
    output.write_text(xml,encoding="utf-8")
    return output

def project_layout(root:Path):
    for p in [root/"PackageSources"/"aerial_images",root/"PackageSources"/"terrain",root/"PackageSources"/"buildings",root/"PackageDefinitions"]: p.mkdir(parents=True,exist_ok=True)
