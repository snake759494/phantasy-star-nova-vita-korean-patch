"""원본 CPK(work/orig/)에서 빌드에 필요한 파일을 work/에 풀어 둔다.
- work/msg/msg_*.rmd : 대사·메뉴 메시지 (text/ko.json 키와 같은 ID)
- work/aif/<이름>.aif : text/images/에 설정이 있는 그림 글자 텍스처
usage: python tools/prepare.py
"""
import os, sys, glob, hashlib, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
src = os.path.join(R, 'work', 'orig', 'NOVA_FileList_Vita.cpk')
if not os.path.exists(src): sys.exit('work/orig/NOVA_FileList_Vita.cpk 가 없습니다.')
m = json.load(open(os.path.join(R, 'release_manifest.json'), encoding='utf8'))
want = next(f for f in m['files'] if f['target'] == 'NOVA_FileList_Vita.cpk')['source_size']
if os.path.getsize(src) != want: print('경고: 원본 크기가 release_manifest.json과 다릅니다.')
c = CPK(src)
img = {os.path.basename(p)[:-3] + '.aif' for p in glob.glob(os.path.join(R, 'text', 'images', '*.py'))}
for d in ('msg', 'aif'): os.makedirs(os.path.join(R, 'work', d), exist_ok=True)
n = 0
for e in c.files:
    nm = e['name']
    if nm.startswith('msg_') and nm.endswith('.rmd'): d = 'msg'
    elif nm in img: d = 'aif'
    else: continue
    open(os.path.join(R, 'work', d, nm), 'wb').write(c.read(e)); n += 1
print('풀어 낸 파일', n)
