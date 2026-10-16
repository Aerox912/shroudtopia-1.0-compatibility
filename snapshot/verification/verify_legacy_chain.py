from pathlib import Path
import subprocess,hashlib,json,sys
root=Path(__file__).resolve().parent;source=root/'source/legacy-chain'
msbuild=r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
cmake=r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
ctest=str(Path(cmake).with_name('ctest.exe'))
def run(name,args):
 with (root/(name+'.log')).open('w') as log:r=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT)
 if r.returncode:print((root/(name+'.log')).read_text()[-3000:]);raise SystemExit(r.returncode)
for name in ['shroudtopia','winmm']:
 run('build-legacy-'+name,[msbuild,str(source/name/(name+'.vcxproj')),'/p:Configuration=Release','/p:Platform=x64','/p:PlatformToolset=v143',f'/p:SolutionDir={source}\\',f'/p:OutDir={root}/legacy-chain-binary/',f'/p:IntDir={root}/legacy-chain-obj/{name}/','/nologo','/v:q'])
run('configure-legacy-tests',[cmake,'-S',str(source/'shroudtopia/tests'),'-B',str(root/'legacy-chain-tests'),'-A','x64'])
run('build-legacy-tests',[cmake,'--build',str(root/'legacy-chain-tests'),'--config','Release','--parallel'])
run('test-legacy-chain',[ctest,'--test-dir',str(root/'legacy-chain-tests'),'-C','Release','--output-on-failure'])
sys.path.insert(0,r'E:\PackageCaches\enshrouded-analysis');import pefile
exe=pefile.PE(r'E:\Build\esm-native-1.0-20261015\enshrouded-25966634.exe')
imports={entry.dll.decode().lower():[x.name.decode() if x.name else x.ordinal for x in entry.imports] for entry in exe.DIRECTORY_ENTRY_IMPORT}
delay={entry.dll.decode().lower():[x.name.decode() if x.name else x.ordinal for x in entry.imports] for entry in getattr(exe,'DIRECTORY_ENTRY_DELAY_IMPORT',[])}
win=pefile.PE(str(root/'legacy-chain-binary/winmm.dll'))
exports={x.name.decode():x.forwarder.decode() if x.forwarder else None for x in win.DIRECTORY_ENTRY_EXPORT.symbols if x.name}
assert 'winmm.dll' in imports or 'winmm.dll' in delay,'game does not import proxy'
required=imports.get('winmm.dll',[])+delay.get('winmm.dll',[])
assert all(isinstance(x,str) and x in exports and exports[x].startswith('c:\\windows\\system32\\winmm.') for x in required)
result={'binary_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'legacy-chain-binary').glob('*.dll')},'winmm_required':required,'winmm_import_kind':'normal' if 'winmm.dll' in imports else 'delay','runtime_accepted':False}
(root/'legacy-chain-build.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
