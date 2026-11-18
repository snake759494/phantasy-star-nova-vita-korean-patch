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
T=dict(font='eb',color=(240,245,250,255),outline=(10,20,35,255),sw=1,align='l',bg=LERP)
C=dict(font='eb',color=(240,245,250,255),outline=(10,20,35,255),sw=1,bg=LERP)
R=dict(font='eb',color=(240,245,250,255),outline=(10,20,35,255),sw=1,align='r',bg=LERP)
B=[(0,0,1,1,'',dict(bg=KEEP)),
(56,4,96,14,'루빈',T),(65,16,101,27,'포스',T),(56,29,101,39,'휴먼',T),(154,29,176,39,'여성',R),
(81,65,108,75,'전체',C),
(7,79,51,90,'자르두',T),(7,96,44,107,'탈라',T),(7,112,33,122,'케이나',T),(7,127,53,138,'사페드',T),
(7,143,44,154,'쿼트',T),(7,159,53,169,'후토르닉',T),(7,175,44,185,'크라스트',T),
(44,208,81,218,'기본 정렬',C),
(339,6,378,16,'자넬',T),(349,19,396,30,'레인저',T),(339,31,383,40,'휴먼',T),(477,31,498,41,'여성',R),
(294,48,339,58,'크루 정보',T),
(294,61,378,71,'스타일:',T),(286,71,507,74,'',dict(bg=ORIG)),
(294,80,316,90,'특징:',T),(304,93,356,103,'일반 아크스',T),(412,93,479,103,'전투 타입:공격',T),(304,105,356,115,'주목받는 상인',T),
(305,172,434,183,'숍 효과  아이템 숍',T),(294,192,362,203,'도구★4 소재 감소',T)]
