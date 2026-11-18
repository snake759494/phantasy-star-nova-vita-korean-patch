"""영상 cpk 제자리 패치: 원래 오프셋에 덮어쓰고 TOC 크기만 수정"""
import sys,glob,os,struct,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK,row_offsets,utf_decrypt,utf_decrypt_force,_SZ
src,dst,d=sys.argv[1:4]
shutil.copyfile(src,dst)
c=CPK(dst);toff=c.hdr['TocOffset'];F={e['name']:(i,e) for i,e in enumerate(c.files)};c.f.close()
f=open(dst,'r+b');f.seek(toff);th=f.read(16);sz=struct.unpack('<Q',th[8:16])[0];raw=f.read(sz)
enc=raw[:4]!=b'@UTF';tb=bytearray(utf_decrypt(raw));o=row_offsets(tb)
for p in sorted(glob.glob(d+'/*.mp4')):
    b=open(p,'rb').read();r,e=F[os.path.basename(p)];assert len(b)<=e['size'],p
    f.seek(e['off']);f.write(b+b'\0'*(e['size']-len(b)))
    for col in ('FileSize','ExtractSize'):
        a,t=o[(r,col)];tb[a:a+_SZ[t]]=len(b).to_bytes(_SZ[t],'big')
out=bytes(tb)
if enc: out=utf_decrypt_force(out)
f.seek(toff+16);f.write(out);f.close();print('patched')
