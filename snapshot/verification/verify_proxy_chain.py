from pathlib import Path
import subprocess,shutil,json,hashlib,sys
root=Path(__file__).resolve().parent
sys.path.insert(0,r'E:\PackageCaches\enshrouded-analysis');import pefile
exe=pefile.PE(r'E:\Build\esm-native-1.0-20261015\enshrouded-25966634.exe')
base=exe.OPTIONAL_HEADER.ImageBase
imports={x.address-base:x.name for d in exe.DIRECTORY_ENTRY_IMPORT for x in d.imports}
assert exe.get_data(0x8952dd,7)==bytes.fromhex('488d0d9ccc4b01')
assert exe.get_data(0x8952eb,6)==bytes.fromhex('ff15efa4b100')
assert exe.get_data(0x1d51f80,20)=='Winmm.dll\0'.encode('utf-16-le')
assert imports[0x13af7e0]==b'LoadLibraryW' and imports[0x13af908]==b'GetProcAddress'
cmake=r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
for name,args in [('configure-proxy-probe',[cmake,'-S',str(root/'chain-probe-source'),'-B',str(root/'chain-probe-build'),'-A','x64']),('build-proxy-probe',[cmake,'--build',str(root/'chain-probe-build'),'--config','Release'])]:
 with (root/(name+'.log')).open('w') as log:r=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT)
 if r.returncode:print((root/(name+'.log')).read_text()[-2000:]);raise SystemExit(r.returncode)
stage=Path(r'E:\Scratch\esm-legacy-chain-probe-20261016');stage.mkdir()
for p in (root/'legacy-chain-binary').glob('*.dll'):shutil.copy2(p,stage/p.name)
shutil.copy2(root/'chain-probe-build/Release/chain_probe.exe',stage/'chain_probe.exe')
(stage/'shroudtopia.json').write_text(json.dumps({'active':False,'bootDelay':0,'updateDelay':500,'enableLogging':True,'logLevel':'INFO','mods':{}}))
first=root/'first-person-binary/first_person_view.dll'
minimap=Path(r'E:\Build\esm-mods-1.0-wave2-20261015\ESM-wave2-client-25966634-r1\mods\minimap_mod\minimap_mod.dll')
with (root/'test-proxy-probe.log').open('w') as log:r=subprocess.run([str(stage/'chain_probe.exe'),str(first),str(minimap)],cwd=stage,stdout=log,stderr=subprocess.STDOUT,timeout=20)
print((root/'test-proxy-probe.log').read_text());assert r.returncode==0,r.returncode
result={'game_sha256':hashlib.sha256(Path(r'E:\Build\esm-native-1.0-20261015\enshrouded-25966634.exe').read_bytes()).hexdigest(),'binary_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'legacy-chain-binary').glob('*.dll')},'dynamic_winmm_call':'0x8952eb','iat_LoadLibraryW':'0x13af7e0','bootstrap_proxy_probe':True,'game_runtime_accepted':False,'EML_coexistence_runtime_accepted':False}
(root/'legacy-chain-build.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
