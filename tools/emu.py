import ctypes, ctypes.wintypes as wt, subprocess, sys, time, os, struct
u=ctypes.windll.user32; k32=ctypes.windll.kernel32
D=os.path.dirname(os.path.abspath(__file__)); EMU=os.path.join(D,'..','emu','Vita3K.exe')
PIDF=os.path.join(D,'emu.pid')
def find():
    pid=int(open(PIDF).read()); res=[]
    @ctypes.WINFUNCTYPE(ctypes.c_bool,wt.HWND,wt.LPARAM)
    def cb(h,l):
        p=wt.DWORD(); u.GetWindowThreadProcessId(h,ctypes.byref(p))
        if p.value==pid and u.IsWindowVisible(h):
            b=ctypes.create_unicode_buffer(256); u.GetWindowTextW(h,b,256)
            r=wt.RECT(); u.GetClientRect(h,ctypes.byref(r)); res.append((('PCSG' in b.value)*10**8+r.right*r.bottom,h))
        return True
    u.EnumWindows(cb,0); return max(res)[1] if res else None
def fakefg(pid,h):
    k=k32
    k.OpenProcess.restype=ctypes.c_void_p; k.GetModuleHandleW.restype=ctypes.c_void_p; k.GetProcAddress.restype=ctypes.c_void_p
    k.GetProcAddress.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
    k.VirtualProtectEx.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_ulong,ctypes.POINTER(ctypes.c_ulong)]
    k.WriteProcessMemory.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_void_p]
    hp=k.OpenProcess(0x1F0FFF,False,pid)
    stub=b'\x48\xB8'+struct.pack('<Q',h)+b'\xC3'
    for fn in (b'GetForegroundWindow',):
        a=k.GetProcAddress(k.GetModuleHandleW('user32.dll'),fn); old=ctypes.c_ulong()
        k.VirtualProtectEx(hp,a,len(stub),0x40,ctypes.byref(old)); k.WriteProcessMemory(hp,a,stub,len(stub),None)
        k.VirtualProtectEx(hp,a,len(stub),old.value,ctypes.byref(old))
    k.CloseHandle(hp)
def start(app='PCSG00351'):
    p=subprocess.Popen([EMU,'-r',app],cwd=os.path.dirname(EMU),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,env=dict(os.environ,SDL_WINDOWS_GAMEINPUT='0',SDL_WINDOWS_RAW_KEYBOARD='0'))
    open(PIDF,'w').write(str(p.pid)); h=None
    for i in range(60):
        time.sleep(1); h=find()
        if h: break
    # near-invisible, click-through, always-on-top so it is never occluded
    u.GetWindowLongW.restype=ctypes.c_long
    ex=u.GetWindowLongW(h,-20); u.SetWindowLongW(h,-20,ex|0x80000|0x20|0x80)  # LAYERED|TRANSPARENT|TOOLWINDOW
    u.SetLayeredWindowAttributes(h,0,1,2)
    u.SetWindowPos(h,-1,0,0,0,0,0x0001|0x0010|0x0020)
    fakefg(p.pid,h)
    u.SendMessageW(h,0x0006,1,0); u.SendMessageW(h,0x0007,0,0)
    print('started',p.pid,h)
VK={'enter':(0x0D,0x1C),'x':(0x58,0x2D),'c':(0x43,0x2E),'z':(0x5A,0x2C),'v':(0x56,0x2F),'up':(0x26,0x48),'down':(0x28,0x50),'left':(0x25,0x4B),'right':(0x27,0x4D),'q':(0x51,0x10),'e':(0x45,0x12),'w':(0x57,0x11),'a':(0x41,0x1E),'s':(0x53,0x1F),'d':(0x44,0x20),'h':(0x48,0x23),'t':(0x54,0x14),'r':(0x52,0x13),'i':(0x49,0x17),'j':(0x4A,0x24),'k':(0x4B,0x25),'l':(0x4C,0x26),'f':(0x46,0x21),'f12':(0x7B,0x58),'rshift':(0x10,0x36)}
def key(k,hold=0.2):
    h=find(); u.SendMessageW(h,0x0086,1,0); u.SendMessageW(h,0x0006,1,0); u.SendMessageW(h,0x0007,0,0); vk,sc=VK[k]; ext=0x1000000 if k in('up','down','left','right') else 0
    u.PostMessageW(h,0x100,vk,1|(sc<<16)|ext); time.sleep(hold)
    u.PostMessageW(h,0x101,vk,1|(sc<<16)|ext|0xC0000000); time.sleep(0.15)
def tap(x,y):
    h=find(); r=wt.RECT(); u.GetClientRect(h,ctypes.byref(r))
    X=int(x*r.right/960); Y=int(y*r.bottom/544); lp=(Y<<16)|X
    u.SendMessageW(h,0x0086,1,0); u.SendMessageW(h,0x0006,1,0)
    u.PostMessageW(h,0x200,0,lp); time.sleep(0.05); u.PostMessageW(h,0x201,1,lp); time.sleep(0.15); u.PostMessageW(h,0x202,0,lp); time.sleep(0.2)
def stop():
    try: os.system('taskkill /F /PID %s >nul 2>&1'%open(PIDF).read()); os.remove(PIDF)
    except Exception: pass
if __name__=='__main__':
    c=sys.argv[1]
    if c=='start': start()
    elif c=='key':
        for kk in sys.argv[2:]:
            if kk.startswith('_'): time.sleep(float(kk[1:]))
            elif '*' in kk:
                n,kk2=kk.split('*'); [key(kk2) for _ in range(int(n))]
            elif kk.startswith('T'): x,y=kk[1:].split(','); tap(int(x),int(y))
            elif kk.startswith('H'): key(kk[1:].split(':')[0],float(kk.split(':')[1]))
            else: key(kk)
    elif c=='stop': stop()
    elif c=='shot':
        import glob,shutil
        sd=os.path.join(D,'..','emu','screenshots'); before=set(glob.glob(sd+'/**/*.jpg',recursive=True))
        key('f12')
        for i in range(30):
            time.sleep(0.5); new=set(glob.glob(sd+'/**/*.jpg',recursive=True))-before
            if new: break
        time.sleep(0.5); f=new.pop()
        from PIL import Image; Image.open(f).save(sys.argv[2]); os.remove(f)
