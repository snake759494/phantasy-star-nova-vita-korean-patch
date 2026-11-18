"""Check the original CPK hashes, apply the 2 release xdeltas, check the results.

usage: python tools/apply_release.py --xdelta xdelta3.exe --source-dir VITA --patch-dir patch --output-dir ko
"""
import argparse, hashlib, json, os, subprocess, sys
R = os.path.join(os.path.dirname(__file__), '..')
m = json.load(open(os.path.join(R, 'release_manifest.json'), encoding='utf8'))
ap = argparse.ArgumentParser()
for a in ('--xdelta', '--source-dir', '--patch-dir', '--output-dir'): ap.add_argument(a, required=True)
a = ap.parse_args()
def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while b := f.read(1 << 24): h.update(b)
    return h.hexdigest()
os.makedirs(a.output_dir, exist_ok=True)
for f in m['files']:
    src = os.path.join(a.source_dir, f['target']); pat = os.path.join(a.patch_dir, f['asset']); out = os.path.join(a.output_dir, f['target'])
    if os.path.exists(out): sys.exit('출력 파일이 이미 있습니다: ' + out)
    print(f['target'], '원본 확인 중...')
    if sha256(src) != f['source_sha256']: sys.exit('원본 %s의 SHA-256이 다릅니다. 적용을 중단합니다.' % f['target'])
    if sha256(pat) != f['asset_sha256']: sys.exit('xdelta 파일의 SHA-256이 다릅니다: ' + f['asset'])
    subprocess.run([a.xdelta, '-d', '-s', src, pat, out], check=True)
    if sha256(out) != f['output_sha256']: sys.exit('결과 파일의 SHA-256이 다릅니다: ' + out)
print('완료:', a.output_dir)
