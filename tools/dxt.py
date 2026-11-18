"""Vita swizzled DXT1 grayscale codec (numpy)"""
import numpy as np

def _blockpos(bw, bh):
    """index i -> (bx, by) for Vita morton swizzle over block grid"""
    n = bw * bh; i = np.arange(n)
    m = min(bw, bh); nb = int(np.log2(m))
    x = np.zeros(n, np.int64); y = np.zeros(n, np.int64)
    for b in range(nb):
        x |= ((i >> (2 * b + 1)) & 1) << b
        y |= ((i >> (2 * b)) & 1) << b
    rem = i >> (2 * nb)
    if bw > bh: x |= rem << nb
    elif bh > bw: y |= rem << nb
    return x, y

def decode(d, w, h, swz=True):
    bw, bh = w // 4, h // 4
    a = np.frombuffer(d[:bw * bh * 8], np.uint8).reshape(-1, 8)
    c0 = a[:, 0].astype(np.int32) | a[:, 1].astype(np.int32) << 8
    c1 = a[:, 2].astype(np.int32) | a[:, 3].astype(np.int32) << 8
    g0 = ((c0 >> 5) & 63) * 255 // 63; g1 = ((c1 >> 5) & 63) * 255 // 63
    four = c0 > c1
    pal = np.stack([g0, g1, np.where(four, (2 * g0 + g1) // 3, (g0 + g1) // 2), np.where(four, (g0 + 2 * g1) // 3, 0)], 1)
    bits = a[:, 4].astype(np.uint32) | a[:, 5].astype(np.uint32) << 8 | a[:, 6].astype(np.uint32) << 16 | a[:, 7].astype(np.uint32) << 24
    idx = np.stack([(bits >> (2 * k)) & 3 for k in range(16)], 1)
    px = np.take_along_axis(pal, idx.astype(np.int64), 1).reshape(-1, 4, 4)
    if swz: bx, by = _blockpos(bw, bh)
    else: bx, by = np.arange(bw * bh) % bw, np.arange(bw * bh) // bw
    img = np.zeros((h, w), np.uint8)
    for k in range(bw * bh):
        img[by[k] * 4:by[k] * 4 + 4, bx[k] * 4:bx[k] * 4 + 4] = px[k]
    return img

def encode(img, swz=True):
    """grayscale uint8 (h,w) -> DXT1 bytes. endpoints = block min/max (gray 565)"""
    h, w = img.shape; bw, bh = w // 4, h // 4
    blocks = img.reshape(bh, 4, bw, 4).transpose(0, 2, 1, 3).reshape(bh * bw, 16).astype(np.int32)
    if swz:
        bx, by = _blockpos(bw, bh); order = by * bw + bx
        blocks = blocks[order]
    mx = blocks.max(1); mn = blocks.min(1)
    def to565(g):
        r5 = (g * 31 + 127) // 255; g6 = (g * 63 + 127) // 255
        return (r5 << 11) | (g6 << 5) | r5, g6 * 255 // 63
    c0, q0 = to565(mx); c1, q1 = to565(mn)
    same = c0 == c1
    # force 4-colour mode c0>c1; if equal, all indices 0
    pal = np.stack([q0, q1, (2 * q0 + q1) // 3, (q0 + 2 * q1) // 3], 1)
    dist = np.abs(blocks[:, :, None] - pal[:, None, :])
    idx = dist.argmin(2).astype(np.uint32)
    idx[same] = 0
    bits = np.zeros(len(blocks), np.uint32)
    for k in range(16): bits |= idx[:, k] << (2 * k)
    out = np.zeros((len(blocks), 8), np.uint8)
    out[:, 0] = c0 & 255; out[:, 1] = c0 >> 8; out[:, 2] = c1 & 255; out[:, 3] = c1 >> 8
    for k in range(4): out[:, 4 + k] = (bits >> (8 * k)) & 255
    return out.tobytes()

def p2(n):
    v = 1
    while v < n: v *= 2
    return v

def _unswz(blocks, bw, bh):
    bx, by = _blockpos(bw, bh); out = np.zeros_like(blocks)
    out[by * bw + bx] = blocks
    return out

def decode_rgba(d, w, h, fmt, swz=True):
    """returns RGBA (H,W,4) of padded pow2 dims; fmt 0x0f DXT1, 0x11 DXT5, 0x01 BGRA8"""
    from PIL import Image
    W, H = (p2(w), p2(h)) if swz else ((w + 3) // 4 * 4, (h + 3) // 4 * 4)
    if fmt == 0x01:
        a = np.frombuffer(d[:W * H * 4], np.uint8).reshape(H, W, 4)[:, :, [2, 1, 0, 3]]
        return a
    bs = 8 if fmt == 0x0f else 16
    bw, bh = max(1, W // 4), max(1, H // 4)
    blk = np.frombuffer(d[:bw * bh * bs], np.uint8).reshape(-1, bs)
    if swz: blk = _unswz(blk, bw, bh)
    im = Image.frombuffer('RGBA', (W, H), blk.tobytes(), 'bcn', 1 if fmt == 0x0f else 3)
    return np.array(im)

def _enc_dxt5_blocks(px):
    """px (N,16,4) uint8 -> (N,16) bytes"""
    px = px.astype(np.int32); N = len(px)
    out = np.zeros((N, 16), np.uint8)
    # alpha
    a = px[:, :, 3]; a0 = a.max(1); a1 = a.min(1)
    lv = np.stack([a0, a1] + [((7 - i) * a0 + i * a1) // 7 for i in range(1, 7)], 1)
    ai = np.abs(a[:, :, None] - lv[:, None, :]).argmin(2).astype(np.uint64)
    eq = a0 == a1; ai[eq] = 0
    out[:, 0] = a0; out[:, 1] = a1
    bits = np.zeros(N, np.uint64)
    for k in range(16): bits |= ai[:, k] << np.uint64(3 * k)
    for k in range(6): out[:, 2 + k] = ((bits >> np.uint64(8 * k)) & np.uint64(255)).astype(np.uint8)
    # colour: endpoints along luminance extremes (weight by alpha)
    rgb = px[:, :, :3]
    lum = rgb @ np.array([3, 6, 1]) + (px[:, :, 3] == 0) * -100000
    lum2 = rgb @ np.array([3, 6, 1]) + (px[:, :, 3] == 0) * 100000
    imax = lum.argmax(1); imin = lum2.argmin(1)
    cmax = rgb[np.arange(N), imax]; cmin = rgb[np.arange(N), imin]
    def q(c):
        r = (c[:, 0] * 31 + 127) // 255; g = (c[:, 1] * 63 + 127) // 255; b = (c[:, 2] * 31 + 127) // 255
        return (r << 11) | (g << 5) | b, np.stack([r * 255 // 31, g * 255 // 63, b * 255 // 31], 1)
    c0, e0 = q(cmax); c1, e1 = q(cmin)
    swap = c0 < c1
    c0, c1 = np.where(swap, c1, c0), np.where(swap, c0, c1)
    e0, e1 = np.where(swap[:, None], e1, e0), np.where(swap[:, None], e0, e1)
    pal = np.stack([e0, e1, (2 * e0 + e1) // 3, (e0 + 2 * e1) // 3], 1)
    dist = ((rgb[:, :, None, :] - pal[:, None, :, :]) ** 2).sum(3)
    ci = dist.argmin(2).astype(np.uint32); ci[c0 == c1] = 0
    cb = np.zeros(N, np.uint32)
    for k in range(16): cb |= ci[:, k] << (2 * k)
    out[:, 8] = c0 & 255; out[:, 9] = c0 >> 8; out[:, 10] = c1 & 255; out[:, 11] = c1 >> 8
    for k in range(4): out[:, 12 + k] = (cb >> (8 * k)) & 255
    return out

def encode_rgba(img, fmt, swz=True):
    """img RGBA (H,W,4) with pow2 dims"""
    H, W = img.shape[:2]
    if fmt == 0x01: return img[:, :, [2, 1, 0, 3]].astype(np.uint8).tobytes()
    assert fmt in (0x11, 0x0f)
    bw, bh = W // 4, H // 4
    px = img.reshape(bh, 4, bw, 4, 4).transpose(0, 2, 1, 3, 4).reshape(bh * bw, 16, 4)
    blk = _enc_dxt5_blocks(px)
    if fmt == 0x0f: blk = np.ascontiguousarray(blk[:, 8:])
    if swz:
        bx, by = _blockpos(bw, bh); blk = blk[by * bw + bx]
    return blk.tobytes()

def decode_tex(d, t):
    """decode any supported SRD texture -> RGBA (h_pad, w_pad, 4); returns (img, swz_flag)"""
    if t['fmt'] == 0x05:
        sc = t['scan'] // 2
        a = np.frombuffer(d[:sc * t['h'] * 2], '<u2').reshape(t['h'], sc).astype(np.uint32)
        im = np.dstack([((a >> s) & 15) * 17 for s in (8, 4, 0, 12)]).astype(np.uint8)
        return im, False
    if t['fmt'] == 0x01 and len(d) >= t['scan'] * t['h'] and t['scan'] < p2(t['w']) * 4 or (t['fmt'] == 0x01 and len(d) < p2(t['w']) * p2(t['h']) * 4):
        sc = t['scan'] // 4
        a = np.frombuffer(d[:sc * t['h'] * 4], np.uint8).reshape(t['h'], sc, 4)[:, :, [2, 1, 0, 3]]
        return a.copy(), 'lin'
    sw = True if t['fmt'] in (0x0f, 0x11) else t['swz'] != 0
    return decode_rgba(d, t['w'], t['h'], t['fmt'], sw), sw

def encode_tex(img, t, sw):
    if t['fmt'] == 0x05:
        q = (img.astype(np.int32) + 8) // 17
        q = np.clip(q, 0, 15).astype(np.uint32)
        v = (q[..., 3] << 12) | (q[..., 0] << 8) | (q[..., 1] << 4) | q[..., 2]
        return v.astype('<u2').tobytes()
    if sw == 'lin':
        return img[:, :, [2, 1, 0, 3]].astype(np.uint8).tobytes()
    return encode_rgba(img, t['fmt'], sw)
