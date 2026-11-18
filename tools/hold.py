import sys,os,time,ctypes;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import emu
u=ctypes.windll.user32
def down(k):
    h=emu.find();vk,sc=emu.VK[k];ext=0x1000000 if k in('up','down','left','right') else 0;u.PostMessageW(h,0x100,vk,1|(sc<<16)|ext)
def up(k):
    h=emu.find();vk,sc=emu.VK[k];ext=0x1000000 if k in('up','down','left','right') else 0;u.PostMessageW(h,0x101,vk,1|(sc<<16)|ext|0xC0000000)
# usage: hold.py w,d 6 x:1.0  (hold keys for secs, tapping key every interval)
ks=sys.argv[1].split(',');T=float(sys.argv[2]);tap=sys.argv[3].split(':') if len(sys.argv)>3 else None
for k in ks:down(k)
t0=time.time()
while time.time()-t0<T:
    if tap: emu.key(tap[0],0.15);time.sleep(float(tap[1]))
    else: time.sleep(0.2)
    for k in ks:down(k)
for k in ks:up(k)
