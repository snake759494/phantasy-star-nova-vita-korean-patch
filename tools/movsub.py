"""영상 하드자막 교체: scan(자막 구간 검출) / render(일본어 지우고 한글 그리기)"""
import sys, os, json, av, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
Y0, Y1 = 455, 512
def tmask(f):
    c = f[Y0:Y1].astype(np.int16); g = c.mean(2)
    sat = c.max(2) - c.min(2)
    br = (g > 175) & (sat < 60)
    mn = cv2.erode(g.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.int16)
    m = (br & (mn < g - 75)).astype(np.uint8)
    return m
def scan(src, out):
    c = av.open(src); ev = []; cur = None; i = 0
    for fr in c.decode(video=0):
        a = fr.to_ndarray(format='rgb24'); m = tmask(a); n = int(m.sum())
        cols = np.nonzero(m.sum(0))[0]
        on = n > 60 and len(cols) and (cols[-1] - cols[0]) > 30
        if on:
            box = (int(cols[0]), int(cols[-1]))
            if cur and abs(cur['x0'] - box[0]) < 25 and abs(cur['x1'] - box[1]) < 25 and i - cur['e'] <= 3:
                cur['e'] = i; cur['acc'] += m.astype(np.int32)
            else:
                if cur: ev.append(cur)
                cur = dict(s=i, e=i, x0=box[0], x1=box[1], acc=m.astype(np.int32), img=a[Y0 - 10:Y1 + 10].copy())
            if cur['e'] - cur['s'] == 10: cur['img'] = a[Y0 - 10:Y1 + 10].copy()
        i += 1
    if cur: ev.append(cur)
    ev = [e for e in ev if e['e'] - e['s'] >= 8]
    os.makedirs(out, exist_ok=True); J = []
    for k, e in enumerate(ev):
        Image.fromarray(e['img']).save(os.path.join(out, '%03d.png' % k))
        np.save(os.path.join(out, '%03d.npy' % k), (e['acc'] >= 3).astype(np.uint8))
        J.append(dict(s=e['s'], e=e['e'], x0=e['x0'], x1=e['x1'], ko=''))
    json.dump(J, open(os.path.join(out, 'ev.json'), 'w'), indent=0)
    print(src, len(J))
FONT = os.path.join(ROOT, 'NanumSquareNeo-cBd.ttf')
def groups(evd):
    J = json.load(open(os.path.join(evd, 'ev.json'), encoding='utf-8')); G = []
    for k, e in enumerate(J):
        t = e.get('ko', '')
        if t == '-' : continue
        m = np.load(os.path.join(evd, '%03d.npy' % k))
        if G and G[-1]['ko'] == t and t and e['s'] - G[-1]['e'] < 120:
            G[-1]['e'] = e['e']; G[-1]['m'] |= m
        else: G.append(dict(s=e['s'], e=e['e'], ko=t, m=m.copy()))
    for g in G:
        full = np.zeros((544, 960), np.uint8); full[Y0:Y1] = g['m']
        g['M'] = cv2.dilate(full, np.ones((7, 7), np.uint8))
    return G
def extend(src, G):
    c = av.open(src); P = []
    for fr in c.decode(video=0): P.append(np.packbits(tmask(fr.to_ndarray(format='rgb24'))))
    n = len(P); sh = (Y1 - Y0, 960)
    def tm(i): return np.unpackbits(P[i])[:sh[0] * sh[1]].reshape(sh)
    G.sort(key=lambda g: g['s'])
    for gi, g in enumerate(G):
        gm = cv2.dilate(g['m'], np.ones((5, 5), np.uint8)) > 0
        lo = G[gi - 1]['e'] + 1 if gi else 0; hi = G[gi + 1]['s'] - 1 if gi + 1 < len(G) else n - 1
        def hit(i):
            t = tm(i) > 0; k = t.sum()
            return k > 40 and (t & gm).sum() >= 0.6 * k and (t & gm).sum() >= 0.25 * (g['m'] > 0).sum()
        for d, lim in ((-1, lo), (1, hi)):
            i = g['s'] if d < 0 else g['e']; miss = 0
            while miss <= 4:
                j = i + d * (miss + 1)
                if (d < 0 and j < max(lim, g['s'] - 150)) or (d > 0 and j > min(lim, g['e'] + 150)): break
                if hit(j): i = j; miss = 0
                else: miss += 1
            if d < 0: g['s'] = i
            else: g['e'] = i
    return G
def render(src, evd, dst):
    G = extend(src, groups(evd))
    ic = av.open(src); oc = av.open(dst, 'w', format='mp4')
    vi = ic.streams.video[0]; ai = ic.streams.audio[0]
    vo = oc.add_stream('libx264', rate=vi.average_rate); vo.width, vo.height = vi.width, vi.height; vo.pix_fmt = 'yuv420p'
    vo.bit_rate = int(os.environ.get('BR','2500000')); vo.options = {'preset': 'medium', 'profile': 'main', 'x264-params': 'bframes=0:ref=3:keyint=60'}
    vo.time_base = 1 / vi.average_rate
    ao = oc.add_stream_from_template(ai)
    f = ImageFont.truetype(FONT, 22)
    i = 0; aps = []
    for pk in ic.demux(vi, ai):
        if pk.stream is ai:
            if pk.dts is None: continue
            pk.stream = ao; oc.mux(pk); continue
        for fr in pk.decode():
            a = fr.to_ndarray(format='rgb24')
            for g in G:
                if g['s'] - 4 <= i <= g['e'] + 4:
                    a = cv2.inpaint(a, g['M'], 3, cv2.INPAINT_TELEA)
                    if g['s'] <= i <= g['e'] and g['ko']:
                        al = min(1.0, (i - g['s'] + 1) / 6, (g['e'] - i + 1) / 6)
                        ov = Image.new('RGBA', (960, 544)); d = ImageDraw.Draw(ov)
                        lines = g['ko'].split('\n'); y = 484 - 13 * len(lines)
                        for ln in lines:
                            w = d.textlength(ln, font=f)
                            d.text(((960 - w) / 2, y), ln, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(15, 15, 25, 255))
                            y += 26
                        o = np.array(ov).astype(np.float32); k = o[..., 3:4] / 255 * al
                        a = (a * (1 - k) + o[..., :3] * k).astype(np.uint8)
            nf = av.VideoFrame.from_ndarray(a, format='rgb24'); nf.pts = i
            for p in vo.encode(nf): oc.mux(p)
            i += 1
    for p in vo.encode(): oc.mux(p)
    oc.close()
if __name__ == '__main__':
    {'scan': scan, 'render': render}[sys.argv[1]](*sys.argv[2:])
