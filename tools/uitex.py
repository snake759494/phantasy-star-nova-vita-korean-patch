"""UI 텍스처(aif) 한글화: 단어 박스 자동 분할 + 한글 덮어그리기 + DXT3 재인코딩"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import rmdtex
from dxt import _blockpos
ROOT = os.path.join(os.path.dirname(__file__), '..')
FONTS = {k: os.path.join(ROOT, v) for k, v in dict(
    hv='NanumSquareNeo-eHv.ttf', eb='NanumSquareNeo-dEb.ttf', bd='NanumSquareNeo-cBd.ttf',
    rg='NanumSquareNeo-bRg.ttf', sh='SeoulHangangEB.ttf', shm='SeoulHangangM.ttf',
    gal='Galmuri11-Bold.ttf').items()}

def load(name):
    b = open(os.path.join(ROOT, 'work/aif', name + '.aif'), 'rb').read()
    if is1(b):
        d, w, h = rmdtex.tex(b); bw, bh = w // 4, h // 4
        from dxt import _unswz
        blk = _unswz(np.frombuffer(b[d:d + bw * bh * 8], np.uint8).reshape(-1, 8), bw, bh)
        return b, np.array(Image.frombuffer('RGBA', (w, h), blk.tobytes(), 'bcn', 1).convert('RGBA'))
    return b, np.array(rmdtex.decode(b))

def is1(b):
    d, w, h = rmdtex.tex(b); return len(b) - d < w * h

def seg(a, region, gap=6, thr=40, minh=4):
    x0, y0, x1, y1 = region
    m = a[y0:y1, x0:x1, 3] > thr
    md = ndimage.binary_dilation(m, np.ones((3, gap * 2 + 1)))
    lab, n = ndimage.label(md)
    out = []
    for sl in ndimage.find_objects(lab):
        ys, xs = sl
        sub = m[ys, xs]
        if not sub.any(): continue
        yy, xx = np.nonzero(sub)
        bx = (x0 + xs.start + xx.min(), y0 + ys.start + yy.min(), x0 + xs.start + xx.max() + 1, y0 + ys.start + yy.max() + 1)
        if bx[3] - bx[1] >= minh: out.append(bx)
    out.sort(key=lambda b: (b[1] // 8, b[0]))
    return out

def overlay(a, boxes, path):
    im = Image.new('RGBA', (a.shape[1], a.shape[0]), (20, 20, 60, 255))
    im.alpha_composite(Image.fromarray(a))
    d = ImageDraw.Draw(im)
    for i, b in enumerate(boxes):
        d.rectangle(b, outline=(255, 0, 0, 255))
        d.text((b[0], b[3]), str(i), fill=(255, 255, 0, 255))
    im.save(path)

def draw(a, box, text, font='hv', color=None, bg=None, pad=0, align='c', outline=None, scale=1.0, sw=0, minx=0.6):
    """box 영역을 지우고 text를 박스에 맞춰 그림. bg=None이면 테두리에서 추정."""
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1].astype(np.float32)
    if color is None:
        al = reg[..., 3]
        sel = al > 200
        if sel.sum() < 4: sel = al > 60
        rgb = reg[sel][:, :3]
        lum = rgb.sum(1)
        color = tuple(int(v) for v in rgb[lum >= np.percentile(lum, 60)].mean(0)) + (255,)
    if isinstance(bg, str): pass
    elif bg is None:
        bd = np.concatenate([a[y0 - 1, x0 - 1:x1 + 1], a[y1, x0 - 1:x1 + 1], a[y0:y1, x0 - 1], a[y0:y1, x1]]).astype(np.float32)
        bg = tuple(int(v) for v in np.median(bd, 0))
        if bg[3] < 128: bg = (0, 0, 0, 0)
    if bg == 'inp':
        import cv2
        m = np.zeros(a.shape[:2], np.uint8); m[max(0,y0-4):y1+4, max(0,x0-4):x1+4] = 255
        al = a[..., 3].copy()
        a[..., :3] = cv2.inpaint(np.ascontiguousarray(a[..., :3]), m, 5, cv2.INPAINT_TELEA); a[..., 3] = al
    elif bg[3] == 0: a[max(0,y0-2):y1+2, max(0,x0-2):x1+2] = bg
    else: a[y0:y1, x0:x1] = bg
    if not text: return
    W, H = x1 - x0 - 2 * pad, y1 - y0 - 2 * pad
    Ht = max(4, int(H * scale))
    sz = Ht * 2
    while True:
        f = ImageFont.truetype(FONTS[font], sz)
        l, t, r, bb = f.getbbox(text, stroke_width=sw)
        if bb - t <= Ht or sz <= 6: break
        sz -= 1
    tmp = Image.new('RGBA', (r - l + 4, bb - t + 4), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((2 - l, 2 - t), text, font=f, fill=color, stroke_width=sw, stroke_fill=outline)
    tmp = tmp.crop((2, 2, 2 + r - l, 2 + bb - t))
    tw, th = tmp.size
    if tw > W:
        if tw * minx > W:  # 너무 좁으면 높이도 축소
            k = W / (tw * minx); tmp = tmp.resize((W, max(1, int(th * k))), Image.LANCZOS)
        else: tmp = tmp.resize((W, th), Image.LANCZOS)
    tw, th = tmp.size
    ox = pad + {'c': (W - tw) // 2, 'l': 0, 'r': W - tw}[align]
    oy = (y1 - y0 - th) // 2
    base = Image.fromarray(a[y0:y1, x0:x1].copy()); base.alpha_composite(tmp, (ox, oy))
    a[y0:y1, x0:x1] = np.array(base)

def dxt3(a):
    H, W = a.shape[:2]; bw, bh = W // 4, H // 4
    blk = a.reshape(bh, 4, bw, 4, 4).transpose(0, 2, 1, 3, 4).reshape(bh * bw, 16, 4).astype(np.int32)
    al = (blk[:, :, 3] * 15 + 127) // 255
    out = np.zeros((bh * bw, 16), np.uint8)
    for k in range(8): out[:, k] = al[:, 2 * k] | (al[:, 2 * k + 1] << 4)
    rgb = blk[:, :, :3]
    w = (blk[:, :, 3] > 0)[:, :, None]
    lum = rgb.sum(2) + np.where(w[:, :, 0], 0, -10000)
    imx = lum.argmax(1); lum2 = rgb.sum(2) + np.where(w[:, :, 0], 0, 10000); imn = lum2.argmin(1)
    r = np.arange(len(blk))
    cmax, cmin = rgb[r, imx], rgb[r, imn]
    def q(c):
        r5 = (c[:, 0] * 31 + 127) // 255; g6 = (c[:, 1] * 63 + 127) // 255; b5 = (c[:, 2] * 31 + 127) // 255
        return (r5 << 11) | (g6 << 5) | b5, np.stack([r5 * 255 // 31, g6 * 255 // 63, b5 * 255 // 31], 1)
    c0, p0 = q(cmax); c1, p1 = q(cmin)
    sw = c0 < c1
    c0, c1 = np.where(sw, c1, c0), np.where(sw, c0, c1)
    p0, p1 = np.where(sw[:, None], p1, p0), np.where(sw[:, None], p0, p1)
    pal = np.stack([p0, p1, (2 * p0 + p1) // 3, (p0 + 2 * p1) // 3], 1)
    dist = ((rgb[:, :, None, :] - pal[:, None, :, :]) ** 2).sum(3)
    idx = dist.argmin(2).astype(np.uint32)
    bits = np.zeros(len(blk), np.uint32)
    for k in range(16): bits |= idx[:, k] << (2 * k)
    out[:, 8] = c0 & 255; out[:, 9] = c0 >> 8; out[:, 10] = c1 & 255; out[:, 11] = c1 >> 8
    for k in range(4): out[:, 12 + k] = (bits >> (8 * k)) & 255
    bx, by = _blockpos(bw, bh); out = out[by * bw + bx]
    return out.tobytes()

def save(b, a):
    d, w, h = rmdtex.tex(b)
    enc = dxt3(a)
    if is1(b):
        e = np.frombuffer(enc, np.uint8).reshape(-1, 16)[:, 8:].copy()
        eq = (e[:, 0] == e[:, 2]) & (e[:, 1] == e[:, 3]); e[eq, 4:] = 0
        enc = e.tobytes()
    return b[:d] + enc + b[d + len(enc):]
