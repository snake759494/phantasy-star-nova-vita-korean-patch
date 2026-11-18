import sys as _s, numpy as _np
_O=[]
class _BG:
    # bg 대체: LERP = 박스 좌우 테두리 픽셀을 행마다 선형보간(그라데이션 바용), KEEP = 지우지 않음, ORIG = 원본 픽셀 복원
    def __init__(s,m): s.m=m
    def __getitem__(s,i): return 255
    def __eq__(s,o): return False
    __hash__=object.__hash__
    def __array__(s,dtype=None,copy=None):
        f=_s._getframe(1); L=f.f_locals; a=L['a']; x0,y0,x1,y1=L['x0'],L['y0'],L['x1'],L['y1']
        if not _O: _O.append(a.copy())
        if s.m=='keep': return a[y0:y1,x0:x1].copy()
        if s.m=='orig': return _O[0][y0:y1,x0:x1].copy()
        l=a[y0:y1,x0-1].astype(float); r=a[y0:y1,x1].astype(float); t=_np.linspace(0,1,x1-x0)[None,:,None]
        return (l[:,None]*(1-t)+r[:,None]*t).round().astype(_np.uint8)
LERP=_BG('lerp'); KEEP=_BG('keep'); ORIG=_BG('orig')
T=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,align='l',bg=LERP)
C=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,bg=LERP)
B=[(102,18,156,29,'스킬 보드',C),(271,20,326,31,'세트 스킬',T),(393,20,447,31,'콤보 스킬',T),
(283,35,344,46,'저스트 가드',T),(283,48,342,59,'타격력 업Ⅰ',T),
(283,61,345,72,'타격력 업Ⅱ',T),(393,36,457,44,'타격력 업Ⅳ',dict(T,bg=(24,36,49,255),outline=None,sw=0))]
