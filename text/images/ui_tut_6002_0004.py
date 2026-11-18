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
N=dict(font='eb',color=(240,245,255,255),outline=(0,0,0,255),sw=1,align='l',bg='inp')
B=[(162,4,216,14,'게스트 크루',C),
(126,19,190,29,'포뉴엘',T),(126,35,180,45,'레이캐스트',T),
(311,4,374,15,'포뉴엘',T),(319,18,359,28,'포스',T),(292,27,310,37,'타인',dict(font='eb',color=(140,230,60,255))),
(311,30,357,42,'뉴먼',T),(477,31,496,41,'여성',R),
(294,48,340,59,'크루 정보',T),(294,64,330,75,'스타일',T),(294,92,313,103,'특징',T),
(305,105,357,116,'위기에 강함',T),(407,105,469,116,'지구력 부족',T),
(127,177,206,187,'최근 플레이순',C),
(8,157,57,165,'레이캐스트',N),(8,181,65,189,'포뉴엘',N),(8,209,49,219,'휴마',N)]
