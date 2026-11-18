import sys,os,json,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build_msg as bm
from cpk import patch_cpk
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
SRC=os.path.join(ROOT,'work','orig','NOVA_FileList_Vita.cpk')
def main(tr, dst):
    bm.load_templates(os.path.join(ROOT,'work','msg'))
    repl={}; err=[]
    for mid,txt in tr.items():
        f='msg_%s.rmd'%mid; o=open(os.path.join(ROOT,'work','msg',f),'rb').read()
        try: repl[f]=bm.build(o,txt)
        except Exception as e: err.append((mid,str(e)))
    import uiapply
    for u in glob.glob(os.path.join(ROOT,'text','images','*.py')):
        n=os.path.basename(u)[:-3]; repl[n+'.aif']=uiapply.apply(n)
    import csvpatch
    from cpk import CPK
    c=CPK(SRC); F_={e["name"]:e for e in c.files}; repl.update(csvpatch.patch(c,F_)); import captex; repl.update(captex.patch(c,F_))
    print('built',len(repl),'errors',len(err),err[:10])
    patch_cpk(SRC,dst,repl)
if __name__=='__main__':
    tr=json.load(open(sys.argv[1],encoding='utf-8')); main(tr,sys.argv[2])
