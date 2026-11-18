import sys,os,numpy as np
sys.path.insert(0,os.path.dirname(__file__))
from dxt import _unswz
from PIL import Image
def tex(b):
    i=b.index(b'rdda'); d=i+0x60  # data start
    j=b.index(b'Xgmi'); w,h=np.frombuffer(b[j+0x28:j+0x2c],'<u2')
    return d,int(w),int(h)
def decode(b,swz=True):
    d,w,h=tex(b); bw,bh=w//4,h//4
    blk=np.frombuffer(b[d:d+bw*bh*16],np.uint8).reshape(-1,16)
    if swz: blk=_unswz(blk,bw,bh)
    return Image.frombuffer('RGBA',(w,h),blk.tobytes(),'bcn',2)
if __name__=='__main__':
    b=open(sys.argv[1],'rb').read(); im=decode(b,sys.argv[3]!='0' if len(sys.argv)>3 else True)
    bg=Image.new('RGBA',im.size,(0,0,80,255)); bg.alpha_composite(im); bg.save(sys.argv[2])
