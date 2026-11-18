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
B=[(9,32,44,43,'퀘스트',T),(8,48,73,59,'줄거리 확인',T),
(222,94,289,104,'델타 배리언트',dict(font='eb',color=(235,240,250,255)))]
