from __future__ import annotations
import os,subprocess
from pathlib import Path
from xml.sax.saxutils import escape
def sdk_tool():
    configured=os.getenv('MSFS_PACKAGE_TOOL','').strip()
    if configured:return Path(configured)
    root=os.getenv('MSFS_SDK_PATH','').strip()
    if root:return Path(root)/'Tools'/'bin'/'fspackagetool.exe'
    return Path(r'C:\MSFS 2024 SDK\Tools\bin\fspackagetool.exe')
def project_layout(root):
    for p in [root/'PackageDefinitions',root/'PackageSources'/'CGL'/'aerial_images']:p.mkdir(parents=True,exist_ok=True)
def write_cgl_config(root):
    path=root/'PackageSources'/'CGL'/'CGLBuilderConfig.xml'; path.write_text('<CGLBuilder>\n  <CGL type="SecondaryAerialImage" input="Tiles" directory="aerial_images"/>\n</CGLBuilder>\n',encoding='utf-8'); return path
def write_package_definition(root,package_name):
    path=root/'PackageDefinitions'/f'{package_name}.xml'; path.write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<AssetPackage Name="{escape(package_name)}" Version="0.1.0">
<ItemSettings><ContentType>SCENERY</ContentType><Title>SkyScape {escape(package_name)}</Title><Manufacturer>SkyScape</Manufacturer><Creator>SkyScape</Creator><Description>Generated SkyScape aerial scenery.</Description></ItemSettings>
<Flags><VisibleInStore>false</VisibleInStore></Flags>
<AssetGroups><AssetGroup Name="Secondary aerial"><Type>CGL</Type><Flags><FSXCompatibility>false</FSXCompatibility></Flags><AssetDir>PackageSources\CGL\</AssetDir><OutputDir>CGL\</OutputDir></AssetGroup></AssetGroups>
</AssetPackage>\n""",encoding='utf-8'); return path
def write_project(root,package_name):
    path=root/'SkyScapeProject.xml'; path.write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<Project Version="2" Name="{escape(package_name)}" FolderName="Packages" MetadataFolderName="PackagesMetadata"><OutputDirectory>.</OutputDirectory><TemporaryOutputDirectory>_PackageInt</TemporaryOutputDirectory><Packages><Package>PackageDefinitions\{escape(package_name)}.xml</Package></Packages></Project>\n""",encoding='utf-8'); return path
def create_aerial_project(root,package_name):
    project_layout(root); write_cgl_config(root); write_package_definition(root,package_name); return write_project(root,package_name)
def package(project_file):
    tool=sdk_tool()
    if not tool.exists(): raise FileNotFoundError(f'MSFS Package Tool not found: {tool}')
    return subprocess.run([str(tool),str(project_file)],cwd=project_file.parent,text=True,capture_output=True,check=False)
