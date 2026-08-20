from __future__ import annotations
import os,subprocess
from pathlib import Path
from xml.sax.saxutils import escape
def sdk_tool():
 p=os.getenv("MSFS_PACKAGE_TOOL","").strip()
 if p:return Path(p)
 root=os.getenv("MSFS_SDK_PATH","").strip()
 if root:return Path(root)/"Tools"/"bin"/"fspackagetool.exe"
 return Path(r"C:\MSFS 2024 SDK\Tools\bin\fspackagetool.exe")
def create_aerial_project(root,name):
 root=Path(root);cgl=root/"PackageSources"/"CGL";(cgl/"aerial_images").mkdir(parents=True,exist_ok=True);(root/"PackageDefinitions").mkdir(parents=True,exist_ok=True)
 (cgl/"CGLBuilderConfig.xml").write_text('<CGLBuilder>\n<CGL type="SecondaryAerialImage" input="Tiles" directory="aerial_images"/>\n</CGLBuilder>\n',encoding="utf-8")
 (root/"PackageDefinitions"/f"{name}.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>\n<AssetPackage Name="{escape(name)}" Version="0.1.0"><ItemSettings><ContentType>SCENERY</ContentType><Title>SkyScape {escape(name)}</Title><Manufacturer>SkyScape</Manufacturer><Creator>SkyScape</Creator><Description>Generated aerial scenery.</Description></ItemSettings><AssetGroups><AssetGroup Name="SkyScapeCGL"><Type>CGL</Type><Flags><FSXCompatibility>false</FSXCompatibility></Flags><AssetDir>PackageSources\\CGL</AssetDir><OutputDir>CGL</OutputDir></AssetGroup></AssetGroups></AssetPackage>""",encoding="utf-8")
 p=root/"SkyScapeProject.xml";p.write_text(f"""<?xml version="1.0" encoding="utf-8"?>\n<Project Version="2" Name="{escape(name)}" FolderName="Packages" MetadataFolderName="PackagesMetadata"><OutputDirectory>.</OutputDirectory><TemporaryOutputDirectory>_PackageInt</TemporaryOutputDirectory><Packages><Package>PackageDefinitions\\{escape(name)}.xml</Package></Packages></Project>""",encoding="utf-8");return p
def package(project):
 tool=sdk_tool()
 if not tool.exists():raise FileNotFoundError(f"MSFS Package Tool not found: {tool}")
 return subprocess.run([str(tool),str(project)],cwd=Path(project).parent,text=True,capture_output=True,check=False)
