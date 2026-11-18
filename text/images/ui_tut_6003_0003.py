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
B=[(158,4,221,14,'모든 크루',C),(126,19,162,29,'루티나',T),
(346,6,382,16,'루티나',T),(356,18,393,29,'포스',T),(291,28,310,38,'지인',dict(font='eb',color=(250,230,60,255),bg=LERP)),
(346,29,390,40,'휴먼',T),(475,29,497,40,'여성',R),
(294,48,339,59,'크루 정보',T),(294,64,329,75,'스타일',T),(294,78,348,89,'격투계 걸',T),(294,92,313,102,'특징',T),
(304,106,358,117,'일반 아크스',T),(408,106,444,117,'동료사랑',T),
(304,119,366,130,'벼락치기 괴력',T),(408,119,460,130,'헌터 애호',T),(304,131,340,142,'말재주꾼',T),
(127,177,206,187,'최근 플레이순',C),
(294,172,330,183,'코멘트',T),
(294,187,424,198,'파트너의 회복 담당은 나니까',T),(294,199,379,210,'언제든 불러 줘!',T),
(8,181,41,189,'루티나',N),(8,209,49,219,'휴마',N)]
