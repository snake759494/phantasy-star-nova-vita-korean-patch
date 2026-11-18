"""이벤트 캡션 글자 아틀라스(MP01/TE01_020_040_Caption.aif) 한글화
원본: 512x256, 32px 셀 16열, 이벤트 대사 글자를 등장 순서대로 중복 제거해 배치한 글리프 시트.
한글 번역 대사로 같은 규칙의 시트를 다시 그린다."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
import uitex, rmdtex
ROOT = uitex.ROOT
NAMES = ('MP01_020_040_Caption.aif', 'TE01_020_040_Caption.aif')
SMALL = set('!?！？…,.、~-')

def chars():
    ko = json.load(open(os.path.join(ROOT, 'text/ko.json'), encoding='utf8'))
    s = ''.join(ko[k] for k in sorted(ko) if k.startswith('10102004'))
    out = ''
    for ch in s:
        if ch not in out and not ch.isspace(): out += ch
    return out

def render(b):
    d, w, h = rmdtex.tex(b)
    a = np.zeros((h, w, 4), np.uint8)
    im = Image.fromarray(a); dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(uitex.FONTS['eb'], 26)
    cs = chars(); assert len(cs) <= (w // 32) * (h // 32), len(cs)
    for i, ch in enumerate(cs):
        x, y = (i % 16) * 32, (i // 16) * 32
        dr.text((x + 16, y + 16), ch, font=f, anchor='mm', fill=(255, 255, 255, 255),
                stroke_width=1, stroke_fill=(40, 40, 40, 255))
    return uitex.save(b, np.array(im)), cs

def patch(c, F):
    out = {}
    for n in NAMES:
        nb, cs = render(c.read(F[n])); out[n] = nb
    return out

if __name__ == '__main__':
    from cpk import CPK
    c = CPK(os.path.join(ROOT, 'work/orig/NOVA_FileList_Vita.cpk'))
    F = {e['name']: e for e in c.files}
    nb, cs = render(c.read(F[NAMES[0]])); print(len(cs), cs)
    im = rmdtex.decode(nb).convert('RGBA'); bg = Image.new('RGBA', im.size, (0, 0, 90, 255)); bg.alpha_composite(im)
    bg.save(sys.argv[1])
