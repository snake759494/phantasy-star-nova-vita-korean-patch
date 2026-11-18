import sys,os,time,subprocess
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,D);import emu
n=int(sys.argv[1]);pre=sys.argv[2];keys=sys.argv[3].split(',') if len(sys.argv)>3 else ['c']
os.makedirs('work/s/'+pre,exist_ok=True);fs=[]
for i in range(n):
    for k in keys:
        if k.startswith('_'):time.sleep(float(k[1:]))
        else: emu.key(k)
    time.sleep(2.5)
    f='work/s/%s/%03d.png'%(pre,i)
    if subprocess.run([sys.executable,os.path.join(D,'emu.py'),'shot',f],capture_output=True).returncode==0: fs.append(f)
# 시트
W=4;ims=[Image.open(f).resize((480,272)) for f in fs]
for s in range(0,len(ims),12):
    g=ims[s:s+12];sh=Image.new('RGB',(480*W,272*((len(g)+W-1)//W)))
    for j,im in enumerate(g):sh.paste(im,(480*(j%W),272*(j//W)))
    sh.save('work/s/%s_sheet%02d.png'%(pre,s//12))
print(len(fs))
