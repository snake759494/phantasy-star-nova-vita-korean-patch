import struct, sys, os

def _rd(b, o, t):
    if t == 0 or t == 1: return b[o], 1
    if t == 2 or t == 3: return struct.unpack('>H', b[o:o+2])[0], 2
    if t == 4 or t == 5: return struct.unpack('>I', b[o:o+4])[0], 4
    if t == 6 or t == 7: return struct.unpack('>Q', b[o:o+8])[0], 8
    if t == 8: return struct.unpack('>f', b[o:o+4])[0], 4
    if t == 0xA: return ('str', struct.unpack('>I', b[o:o+4])[0]), 4
    if t == 0xB: return ('data',) + struct.unpack('>II', b[o:o+8]), 8
    raise ValueError(t)

def utf_decrypt(b):
    if b[:4] == b'@UTF': return b
    m, out = 0x655f, bytearray()
    for c in b:
        out.append(c ^ (m & 0xff)); m = (m * 0x4115) & 0xffffffff
    return bytes(out)

def parse_utf(b):
    b = utf_decrypt(b)
    assert b[:4] == b'@UTF', b[:4]
    size, rows_off, str_off, data_off, name_off, ncol, rowlen, nrow = struct.unpack('>IIIIIHHI', b[4:32])
    base = 8
    def s(o):
        e = b.index(b'\0', base + str_off + o); return b[base + str_off + o:e].decode('utf-8', 'replace')
    cols, o = [], 32
    for _ in range(ncol):
        fl = b[o]; nm = struct.unpack('>I', b[o+1:o+5])[0]; o += 5
        st, t = fl & 0xf0, fl & 0x0f; const = None
        if st == 0x30:
            v, n = _rd(b, o, t); o += n; const = v
        cols.append((s(nm), st, t, const))
    def conv(v):
        if isinstance(v, tuple):
            if v[0] == 'str': return s(v[1])
            return b[base + data_off + v[1]: base + data_off + v[1] + v[2]]
        return v
    rows = []
    for r in range(nrow):
        o = base + rows_off + r * rowlen; row = {}
        for nm, st, t, const in cols:
            if st == 0x50:
                v, n = _rd(b, o, t); o += n; row[nm] = conv(v)
            elif st == 0x30: row[nm] = conv(const)
            else: row[nm] = None
        rows.append(row)
    return s(name_off), cols, rows

def read_table(f, off):
    f.seek(off); hdr = f.read(16); assert hdr[:4] in (b'CPK ', b'TOC ', b'ITOC', b'ETOC', b'GTOC'), hdr
    sz = struct.unpack('<Q', hdr[8:16])[0]
    return parse_utf(f.read(sz))

class CPK:
    def __init__(s, path):
        s.path = path; s.f = open(path, 'rb')
        _, _, r = read_table(s.f, 0); s.hdr = r[0]
        s.files = []
        if s.hdr.get('TocOffset'):
            _, _, s.toc = read_table(s.f, s.hdr['TocOffset'])
            base = min(s.hdr['TocOffset'], s.hdr.get('ContentOffset') or 1 << 62)
            for e in s.toc:
                d = e.get('DirName') or ''
                s.files.append(dict(name=(d + '/' if d else '') + e['FileName'], off=e['FileOffset'] + base,
                                    size=e['FileSize'], ext=e['ExtractSize'], id=e.get('ID'), row=e))
        if s.hdr.get('ItocOffset'):
            _, _, s.itoc = read_table(s.f, s.hdr['ItocOffset'])
    def read(s, e, raw=False):
        s.f.seek(e['off']); d = s.f.read(e['size'])
        if not raw and e['size'] != e['ext'] and d[:8] == b'CRILAYLA': d = crilayla_dec(d)
        return d

def crilayla_dec(src):
    usize, hoff = struct.unpack('<II', src[8:16])
    out = bytearray(usize + 0x100)
    out[:0x100] = src[16 + hoff:16 + hoff + 0x100]
    data = src[16:16 + hoff]
    # bit reader reading backwards
    pos = len(data) - 1; bitpool = 0; bits = 0
    def get(n):
        nonlocal pos, bitpool, bits
        v = 0
        while n:
            if bits == 0:
                bitpool = data[pos]; pos -= 1; bits = 8
            t = min(bits, n)
            v = (v << t) | ((bitpool >> (bits - t)) & ((1 << t) - 1))
            bits -= t; n -= t
        return v
    w = usize - 1; end = 0
    dst = out
    lvls = (2, 3, 5, 8)
    while w >= 0:
        if get(1):
            off = get(13) + 3; ln = 3
            for i, lv in enumerate(lvls):
                m = get(lv); ln += m
                if m != (1 << lv) - 1: break
            else:
                while True:
                    m = get(8); ln += m
                    if m != 255: break
            for _ in range(ln):
                dst[0x100 + w] = dst[0x100 + w + off]; w -= 1
        else:
            dst[0x100 + w] = get(8); w -= 1
    return bytes(out)

if __name__ == '__main__':
    c = CPK(sys.argv[1])
    print({k: v for k, v in c.hdr.items() if not isinstance(v, bytes)})
    for e in c.files[:int(sys.argv[2]) if len(sys.argv) > 2 else 10**9]:
        print(e['id'], hex(e['off']), e['size'], e['ext'], e['name'])

# ---------------- in-place patcher ----------------
_SZ = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 8, 7: 8, 8: 4, 0xA: 4, 0xB: 8}

def row_offsets(b):
    """return {(row, colname): (offset_in_table_bytes, type)} for per-row columns"""
    size, rows_off, str_off, data_off, name_off, ncol, rowlen, nrow = struct.unpack('>IIIIIHHI', b[4:32])
    cols, o = [], 32
    def s(x):
        e = b.index(b'\0', 8 + str_off + x); return b[8 + str_off + x:e].decode()
    for _ in range(ncol):
        fl = b[o]; nm = struct.unpack('>I', b[o+1:o+5])[0]; o += 5
        if fl & 0xf0 == 0x30: o += _SZ[fl & 0xf]
        cols.append((s(nm), fl & 0xf0, fl & 0xf))
    res = {}
    for r in range(nrow):
        o = 8 + rows_off + r * rowlen
        for nm, st, t in cols:
            if st == 0x50: res[(r, nm)] = (o, t); o += _SZ[t]
    return res

def patch_cpk(src, dst, repl):
    """repl: {name: bytes}. New data inserted where ETOC was; ETOC moved after; header updated."""
    c = CPK(src); hdr = c.hdr; c.f.close()
    fi = open(src, 'rb'); f = open(dst, 'wb')
    eoff, esz = hdr['EtocOffset'], hdr['EtocSize']
    # copy everything before ETOC
    rem = eoff
    while rem:
        n = min(rem, 1 << 24); f.write(fi.read(n)); rem -= n
    fi.seek(eoff); etoc = fi.read(esz + 16 if False else None)  # rest of file from ETOC
    fi.close()
    toff = hdr['TocOffset']
    def get_tbl(off):
        with open(src, 'rb') as g:
            g.seek(off); th = g.read(16); sz = struct.unpack('<Q', th[8:16])[0]; raw = g.read(sz)
        return raw
    raw = get_tbl(toff); enc = raw[:4] != b'@UTF'; tb = bytearray(utf_decrypt(raw))
    offs = row_offsets(tb)
    base = min(toff, hdr.get('ContentOffset') or 1 << 62)
    names = {e['name']: i for i, e in enumerate(c.files)}
    end = eoff
    for nm, data in repl.items():
        r = names[nm]
        pos = (end + 0x7ff) & ~0x7ff
        f.write(b'\x00' * (pos - end)); f.write(data); end = pos + len(data)
        for col, val in (('FileSize', len(data)), ('ExtractSize', len(data)), ('FileOffset', pos - base)):
            o, t = offs[(r, col)]
            tb[o:o + _SZ[t]] = val.to_bytes(_SZ[t], 'big')
    neoff = (end + 0x7ff) & ~0x7ff; f.write(b'\x00' * (neoff - end)); f.write(etoc)
    out = bytes(tb)
    if enc: out = utf_decrypt_force(out)
    f.seek(toff + 16); f.write(out)
    # header
    hraw = get_tbl(0); henc = hraw[:4] != b'@UTF'; hb = bytearray(utf_decrypt(hraw)); ho = row_offsets(hb)
    for col, val in (('EtocOffset', neoff), ('ContentSize', neoff - hdr['ContentOffset'])):
        o, t = ho[(0, col)]; hb[o:o + _SZ[t]] = val.to_bytes(_SZ[t], 'big')
    hout = bytes(hb)
    if henc: hout = utf_decrypt_force(hout)
    f.seek(16); f.write(hout); f.close()

def utf_decrypt_force(b):
    m, out = 0x655f, bytearray()
    for c in b:
        out.append(c ^ (m & 0xff)); m = (m * 0x4115) & 0xffffffff
    return bytes(out)
