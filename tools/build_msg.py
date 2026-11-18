import sys,os,struct,re,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from PIL import Image,ImageDraw,ImageFont
from dxt import _blockpos
from basicmap import B
from rmd import enc7,LBASE,NBASIC
D=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(D,'..')
FONT=os.path.join(ROOT,'NanumSquareNeo-cBd.ttf'); FSIZE=int(os.environ.get('KFSIZE','19'))
CELL=21; STRIDE=23; ADV=int(os.environ.get('KADV','20'))
# basic char -> index (prefer first = halfwidth for ascii)
BI={}
for i,c in enumerate(B):
    BI.setdefault(c,i)
USE_BASIC=set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")|set("！？、。・…〜「」『』（）【】：；＋－×％＆＊／☆★＠＄＃♪“”‘’")|set("!?()<>[]{}:;=+-*/%&$#@\"',._~^|")|set('０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ')|{' ','　','ー'}
TPL={}
def load_templates(msgdir):
    import glob
    want={(128,32):'msg_100000010010013.rmd',(128,64):'msg_100000010070017.rmd',(128,128):'msg_100001.rmd',(256,64):'msg_100002.rmd',(256,128):'msg_100003.rmd'}
    for k,f in want.items():
        b=open(os.path.join(msgdir,f),'rb').read(); te=struct.unpack('<I',b[0x3c:0x40])[0]
        j=b.index(b'rdda',te)+0x60
        TPL[k]=(b[0x48:0x50],b[0x68:0x6c],b[0x70:0x78],b[te:j],len(b)-j)
SIZES=[(128,32),(128,64),(256,64),(128,128),(256,128),(256,256),(512,256),(512,512)]
def gen_tpl(W,H):
    h48,h68,h70,t,_=TPL[(256,128)]; DS=W*H; t=bytearray(t)
    struct.pack_into('<HH',t,0xb8,W,H); struct.pack_into('<HH',t,0xc2,W//4,H//4)
    struct.pack_into('<II',t,0xc8,W*4,DS); struct.pack_into('<I',t,0x104,DS+0xf0)
    struct.pack_into('<I',t,0x160,DS); struct.pack_into('<I',t,0x1b0,DS)
    r=(struct.pack('<II',DS+0x1e0,DS+0x200),struct.pack('<I',DS+0x1e0),struct.pack('<II',W,H),bytes(t),DS)
    TPL[(W,H)]=r; return r
_font=None; _gc={}
import pickle
_SYM=None
def sym():
    global _SYM
    if _SYM is None:
        try: _SYM=pickle.load(open(os.path.join(ROOT,'work','symglyph.pkl'),'rb'))
        except Exception: _SYM={}
    return _SYM
def glyph(ch):
    global _font
    if ch in _gc: return _gc[ch]
    if not ('가'<=ch<='힣') and ch in sym():
        a,m=sym()[ch]; c=np.zeros((CELL,CELL),np.uint8); c[:a.shape[0],:a.shape[1]]=a[:CELL,:CELL]
        _gc[ch]=(c,m[0],m[1]); return _gc[ch]
    if _font is None: _font=ImageFont.truetype(FONT,FSIZE)
    im=Image.new('L',(CELL,CELL)); d=ImageDraw.Draw(im)
    # center horizontally, place on baseline similar to kanji (ink rows ~0..19)
    l,t,r,bm=_font.getbbox('한'); 
    w=_font.getlength(ch)
    d.text(((CELL-w)/2,(CELL-(bm-t))/2-t),ch,font=_font,fill=255)
    a=np.asarray(im); _gc[ch]=(a,ADV,0x0f); return _gc[ch]
def tokenize(text):
    """returns list of tokens: ('ch',c) / ('ctl',bytes)"""
    out=[];i=0
    while i<len(text):
        m=re.match(r'<c(\d+)>|</c>|<i(\d+)>|<([0-9A-F]{4})>',text[i:])
        if m:
            if m.group(0)=='</c>': out.append(('ctl',b'\x82\x80'))
            elif m.group(3): out.append(('ctl',int(m.group(3),16).to_bytes(2,'little')))
            elif m.group(1): out.append(('ctl',b'\x81\x80'+bytes([int(m.group(1))])))
            else: out.append(('ctl',b'\x99\x80'+bytes([int(m.group(2))])))
            i+=len(m.group(0)); continue
        c=text[i]; i+=1
        if c=='\n': out.append(('ctl',b'\x80\x80'))
        elif c in '{}': continue
        else: out.append(('ch',c))
    return out
def dxt3_encode(alpha):
    H,W=alpha.shape; bw,bh=W//4,H//4
    a=(alpha.astype(np.int32)*15+127)//255
    blk=a.reshape(bh,4,bw,4).transpose(0,2,1,3).reshape(bh*bw,16)
    out=np.zeros((bh*bw,16),np.uint8)
    for k in range(8): out[:,k]=blk[:,2*k]|(blk[:,2*k+1]<<4)
    # color: white c0=c1=ffff, indices 0
    out[:,8]=0xff;out[:,9]=0xff;out[:,10]=0xff;out[:,11]=0xff
    bx,by=_blockpos(bw,bh); out=out[by*bw+bx]
    return out.tobytes()
def build(orig,text):
    toks=tokenize(text); loc=[]; li={}
    s=bytearray(); nl=1
    for t in toks:
        if t[0]=='ctl':
            s+=t[1]
            if t[1]==b'\x80\x80': nl+=1
            continue
        c=t[1]
        if c in USE_BASIC and c in BI: s+=enc7(BI[c]+1); continue
        if c not in li: li[c]=len(loc); loc.append(c)
        s+=enc7(LBASE+li[c])
    s+=b'\0\0'
    n=len(loc); cnt=NBASIC+n
    # atlas size
    st,cs=STRIDE,CELL
    for (W,H) in SIZES[:5]:
        cols=W//st; rows=H//st
        if cols*rows>=n: break
    else:
        W,H=256,128
        st=cs=21 if n<=72 else 18
        cols=W//st; rows=H//st
        if cols*rows<n: raise ValueError('too many glyphs %d'%n)
    atlas=np.zeros((H,W),np.uint8); ents=bytearray(20*cnt)
    for i,c in enumerate(loc):
        x=(i%cols)*st; y=(i//cols)*st
        a,adv,b1=glyph(c)
        if cs!=CELL: a=np.asarray(Image.fromarray(a).resize((cs,cs),Image.LANCZOS))
        atlas[y:y+cs,x:x+cs]=a
        ents[20*i:20*i+20]=bytes([adv,b1,0,0])+struct.pack('<4f',x/W,y/H,(x+cs)/W,(y+cs)/H)
    so=0x100; to=so+((0x10+len(s)+0x7f)&~0x7f); te=to+((0x10+len(ents)+0x7f)&~0x7f)
    tpl=TPL.get((W,H)) or gen_tpl(W,H)
    out=bytearray(orig[:0x100]); 
    out+=b'\0'*16+s; out+=b'\0'*(to-len(out)); out+=b'\0'*16+ents; out+=b'\0'*(te-len(out))
    struct.pack_into('<I',out,0x04,te+0x10); struct.pack_into('<I',out,0x0c,te+0x10)
    struct.pack_into('<5I',out,0x30,0x80,so,to,te,te); struct.pack_into('<I',out,0x44,cnt)
    out[0x48:0x50]=tpl[0]; out[0x68:0x6c]=tpl[1]; out[0x70:0x78]=tpl[2]
    struct.pack_into('<f',out,0xa0,21.0+20*(nl-1))
    data=dxt3_encode(atlas); import hashlib; tl=bytearray(tpl[3]); h1=hashlib.md5(data).digest(); h2=hashlib.md5(data+b'n').digest()
    ote=struct.unpack('<I',orig[0x3c:0x40])[0]; tl[0xa0:0xa4]=orig[ote+0xa0:ote+0xa4]; tl[0xd0:0xe0]=h1; tl[0x1a0:0x1b0]=h1; tl[0x130:0x140]=h2
    out+=tl; assert len(data)==tpl[4],(len(data),tpl[4]); out+=data
    return bytes(out)
