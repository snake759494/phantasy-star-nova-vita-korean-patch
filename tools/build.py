"""한글판 NOVA_FileList_Vita.cpk 빌드 (대사·메뉴 메시지, 그림 글자, NPC 이름, 이벤트 캡션)
usage: python tools/build.py [--out out]
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(R, 'out')); a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
import mkcpk
tr = json.load(open(os.path.join(R, 'text', 'ko.json'), encoding='utf-8'))
mkcpk.main(tr, os.path.join(a.out, 'NOVA_FileList_Vita.cpk'))
