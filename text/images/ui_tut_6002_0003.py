import sys as _s, numpy as _np
class _BG:
    # bg 대체: 'lerp' = 박스 좌우 테두리 픽셀을 행마다 선형보간(그라데이션 바용), 'keep' = 지우지 않음
    def __init__(s,m): s.m=m
    def __getitem__(s,i): return 255
    def __eq__(s,o): return False
    __hash__=object.__hash__
    def __array__(s,dtype=None,copy=None):
        f=_s._getframe(1); L=f.f_locals; a=L['a']; x0,y0,x1,y1=L['x0'],L['y0'],L['x1'],L['y1']
        if s.m=='keep': return a[y0:y1,x0:x1].copy()
        l=a[y0:y1,x0-1].astype(float); r=a[y0:y1,x1].astype(float); t=_np.linspace(0,1,x1-x0)[None,:,None]
        return (l[:,None]*(1-t)+r[:,None]*t).round().astype(_np.uint8)
LERP=_BG('lerp'); KEEP=_BG('keep')
T=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,align='l',bg=LERP)
W=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,bg=LERP)
R=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,align='r',bg=LERP)
N=dict(font='eb',color=(240,245,255,255),outline=(0,0,0,255),sw=1,align='l',bg='inp')
B=[(11,4,83,17,'파티 결성',T),(269,4,341,17,'파티 참가',T),
(274,21,348,34,'파티 목록',W),(390,22,434,33,'목록 갱신',W),
(270,38,325,49,'레이캐스트',T),(280,50,326,62,'레인저',T),(270,63,306,74,'캐스트',T),(413,63,434,75,'남성',R),
(39,90,133,101,'멤버 결정을 누르면',dict(T,bg=(24,38,51,255))),(39,100,210,112,'현재 멤버로 파티를 결성합니다.',dict(T,bg=(24,36,49,255))),
(96,118,154,130,'멤버 결정',W),(84,135,166,148,'파티 모집 중지',W),
(8,181,57,189,'레이캐스트',N),(8,209,49,219,'휴마',N)]
