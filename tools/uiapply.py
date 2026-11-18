import sys,os,runpy,numpy as np
sys.path.insert(0,os.path.dirname(__file__));import uitex
from PIL import Image
def apply(name,out=None):
    cfg=runpy.run_path(os.path.join(uitex.ROOT,'text/images',name+'.py'))
    b,a=uitex.load(name); opt=cfg.get('OPT',{})
    for e in cfg['B']:
        x0,y0,x1,y1,t=e[:5]; o=dict(opt); o.update(e[5] if len(e)>5 else {})
        uitex.draw(a,(x0,y0,x1,y1),t,**o)
    nb=uitex.save(b,a)
    if out:
        im=Image.new('RGBA',(a.shape[1],a.shape[0]),(20,20,60,255));im.alpha_composite(Image.fromarray(np.array(uitex.rmdtex.decode(nb))));im.save(out)
    return nb
if __name__=='__main__':
    apply(sys.argv[1],sys.argv[2])
