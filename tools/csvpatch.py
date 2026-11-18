"""시스템 폰트(pvf)로 그려지는 CSV 문자열 교체. pvf/게임 내부가 SJIS라 한글 불가 -> 로마자"""
import os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
import json,hashlib
class names:
    """text/names.json: 일본어 이름의 SHA-1 앞 16자리 -> 로마자 표기 (원문은 저장하지 않음)"""
    def __init__(s): s.d=json.load(open(os.path.join(ROOT,'text','names.json'),encoding='utf-8'))
    def get(s,k,default=None): return s.d.get(hashlib.sha1(k.encode('utf-8')).hexdigest()[:16],default)
def patch(c,F):
    N=names(); out={}
    # NpcBaseParameter: 27번째 열(이름)
    t=c.read(F['NpcBaseParameter.csv']).decode('cp932'); L=t.split('\r\n') if '\r\n' in t else t.split('\n'); sep='\r\n' if '\r\n' in t else '\n'
    for i,l in enumerate(L):
        f=l.split(',')
        if len(f)>26 and re.search('[぀-ヿ一-鿿]',f[26]):
            from romaji import romaji
            f[26]=N.get(f[26]) or romaji(f[26].replace('ガチャ','Gacha ')); L[i]=','.join(f)
    out['NpcBaseParameter.csv']=sep.join(L).encode('cp932')
    t=c.read(F['uireferenceparameter.csv']).decode('cp932')
    t=re.sub(r'^(StringFix_Name\w+,,,,)([^\r\n,]+)',lambda m:m.group(1)+N.get(m.group(2),m.group(2)),t,flags=re.M)
    out['uireferenceparameter.csv']=t.encode('cp932')
    return out
if __name__=='__main__':
    from cpk import CPK
    c=CPK(os.path.join(ROOT,'work','orig','NOVA_FileList_Vita.cpk'));F={e['name']:e for e in c.files}
    o=patch(c,F)
    for k,v in o.items():
        s=v.decode('cp932'); print(k,len(v),len(re.findall('[\u30a0-\u30ff]',s)))
