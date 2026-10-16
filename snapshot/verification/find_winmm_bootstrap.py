from analyze_native import *
strings=hits(new,b'winmm.dll\0')+hits(new,'winmm.dll\0'.encode('utf-16-le'))+hits(new,'Winmm.dll\0'.encode('utf-16-le'))
print('strings',[hex(x) for x in strings])
out=[]
for section in new.sections:
 if not section.Characteristics&0x20000000:continue
 raw=section.get_data()
 for m in re.finditer(b'[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]....',raw,re.DOTALL):
  at=section.VirtualAddress+m.start();target=at+7+struct.unpack('<i',m.group()[3:])[0]
  if target in strings:
   out.append({'rva':hex(at),'string':hex(target),'asm':dump(new,at-16,180)})
Path(__file__).with_name('winmm-bootstrap-xrefs.json').write_text(json.dumps(out,indent=2))
for row in out:print(row['asm'])
