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
R=dict(font='eb',color=(235,240,250,255),outline=(10,20,35,255),sw=1,align='r',bg=LERP)
N=dict(font='eb',color=(240,245,255,255),outline=(0,0,0,255),sw=1,bg='inp')
B=[(47,4,142,14,'최근 함께한 게스트',C),
(29,18,82,29,'레이캐스트',T),(39,31,84,42,'레인저',T),(29,44,65,55,'캐스트',T),(154,44,173,55,'남성',R),
(29,60,91,71,'포뉴엘',T),(39,73,76,84,'포스',T),(29,86,75,97,'뉴먼',T),(154,86,173,97,'여성',R),
(179,99,238,108,'포뉴엘',N),(271,86,289,95,'레이',dict(N,align='l')),
(294,48,340,59,'크루 정보',T),(294,64,330,75,'스타일',T),(294,92,313,103,'특징',T),
(305,105,365,116,'단체 행동 서툶',T),(407,105,426,116,'냉정',T),
(32,229,102,239,'최근 플레이순',C)]
