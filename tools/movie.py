"""동영상 자막 한글화: NOVA_FileList_Vita_movie.cpk 안의 하드자막 영상 8개를 다시 만든다.
work/orig/NOVA_FileList_Vita_movie.cpk -> out/NOVA_FileList_Vita_movie.cpk
필요: PyAV(av), opencv-python, numpy, Pillow, NanumSquareNeo-cBd.ttf
영상 재인코딩(libx264)이라 결과가 배포 파일과 바이트 단위로 같지는 않습니다.
"""
import os, sys, json, glob, subprocess
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
R = os.path.join(D, '..'); W = os.path.join(R, 'work', 'movie')
from cpk import CPK
src = os.path.join(R, 'work', 'orig', 'NOVA_FileList_Vita_movie.cpk')
names = [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(R, 'text', 'movies', '*.json'))]
c = CPK(src); os.makedirs(os.path.join(W, 'out'), exist_ok=True)
F = {e['name']: e for e in c.files}
for n in names:
    mp4 = os.path.join(W, n + '.mp4'); open(mp4, 'wb').write(c.read(F[n + '.mp4']))
    ev = os.path.join(W, n)
    subprocess.run([sys.executable, os.path.join(D, 'movsub.py'), 'scan', mp4, ev], check=True)
    J = json.load(open(os.path.join(ev, 'ev.json'))); K = json.load(open(os.path.join(R, 'text', 'movies', n + '.json'), encoding='utf-8'))
    if len(J) != len(K): sys.exit('%s: 자막 구간 수가 다릅니다 (%d/%d)' % (n, len(J), len(K)))
    json.dump(K, open(os.path.join(ev, 'ev.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    subprocess.run([sys.executable, os.path.join(D, 'movsub.py'), 'render', mp4, ev, os.path.join(W, 'out', n + '.mp4')], check=True,
                   env=dict(os.environ, BR=os.environ.get('BR', '2000000')))
os.makedirs(os.path.join(R, 'out'), exist_ok=True)
subprocess.run([sys.executable, os.path.join(D, 'movpatch.py'), src, os.path.join(R, 'out', 'NOVA_FileList_Vita_movie.cpk'), os.path.join(W, 'out')], check=True)
