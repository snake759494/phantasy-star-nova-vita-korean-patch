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
C=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,bg=LERP)
P=dict(font='eb',color=(235,240,250,255),align='l',bg=KEEP)
B=[(61,33,96,42,'강철 황야',C),(21,47,66,58,'동료 수색',T),
(293,10,313,21,'장소',T),(351,10,392,21,'강철 황야',T),(293,24,338,34,'퀘스트명',T),(363,24,408,34,'동료 수색',T),
(293,49,338,61,'클리어 목표',T),(351,49,406,61,'선발대 구출',T),
(293,62,331,73,'실패 조건',T),(351,62,372,73,'없음',T),
(293,75,345,86,'출현 에너미',T),(352,75,397,86,'G클라다',T),(352,88,388,99,'G다간',T),
(291,114,497,178,'',dict(bg='inp')),(291,187,362,198,'',dict(bg='inp')),
(293,117,497,126,'의뢰인: 필디아',P),
(293,127,497,136,'강철의 황야에 남겨진 선발대 생존자를',P),
(293,137,497,146,'수색해 줘.',P),
(293,147,497,156,'다커가 우글거려서 어떤 타입이 나올지',P),
(293,157,497,166,'나도 모르지만, 생존자 구출은 필수다!',P),
(293,167,497,176,'지금 싸울 수 있는 건 너희뿐이야. 부탁한다!',P),
(293,188,497,197,'동행자: 루티나',P)]
