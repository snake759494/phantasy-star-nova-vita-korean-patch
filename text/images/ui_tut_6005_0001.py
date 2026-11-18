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
S=dict(font="hv",color=(235,25,25,255),outline=(255,250,225,255),sw=1,bg="inp",align="l")
T=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,align='l',bg=LERP)
C=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,bg=LERP)
B=[(0,0,1,1,'',dict(bg=KEEP)),
(100,151,160,162,'스킬 보드2',C),(100,19,158,29,'스킬 보드1',C),
(271,20,329,31,'세트 스킬',T),(393,20,450,31,'콤보 스킬',T),
(271,154,329,165,'세트 스킬',T),(393,154,450,165,'콤보 스킬',T),
(283,37,391,47,'위크 히트 어드밴스',T),(393,37,457,47,'타격력 업Ⅳ',T),
(283,50,347,60,'저스트 가드',T),(283,63,355,73,'스텝 어택',T),(283,76,347,86,'가드 스탠스',T),
(283,89,336,99,'기량 업Ⅰ',T),(283,102,345,112,'타격력 업Ⅰ',T),(283,115,345,125,'타격력 업Ⅱ',T),
(12,9,81,29,'1장째',S),
(12,137,81,158,'2장째',S),
(76,128,184,156,'',dict(bg=ORIG))]
