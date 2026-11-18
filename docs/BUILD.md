# 재빌드

## 준비물

- 원본 CPK 2개 (PCSG00351 복호화 게임 폴더 `ux0:app/PCSG00351/`): `NOVA_FileList_Vita.cpk`, `NOVA_FileList_Vita_movie.cpk` (해시는 `release_manifest.json`)
- Python 3.13, `Pillow`, `numpy`, `scipy`, `opencv-python`, 동영상까지 만들 때 `av`(PyAV)
- 글꼴: `docs/FONT_CREDITS.md`의 7개를 저장소 최상위 폴더에
- xdelta3 (배포 파일을 만들 때만)

## 빌드

원본 CPK 2개를 `work/orig/`에 넣고 저장소 폴더에서 실행합니다.

```powershell
python tools/prepare.py
python tools/build.py
python tools/movie.py
```

`prepare.py`는 원본에서 메시지 RMD와 그림 글자 텍스처를 `work/`에 풀어 냅니다. `build.py`는 `out/NOVA_FileList_Vita.cpk`를, `movie.py`는 `out/NOVA_FileList_Vita_movie.cpk`를 만듭니다.

메시지 글리프 중 기호 44개(…·「」·『』·①~⑩·※ 등)는 배포판을 만들 때 원본 게임 글자에서 잘라 쓴 것인데, 게임 데이터라 저장소에 넣지 않았습니다. 재빌드하면 이 기호를 나눔스퀘어네오로 그리므로, 결과가 배포 파일과 바이트 단위로 같지 않을 수 있습니다. 동영상은 재인코딩이라 배포 파일과 바이트 단위로 같지 않습니다.

## 배포 파일

```powershell
xdelta3 -e -0 -S none -A -s work\orig\NOVA_FileList_Vita.cpk out\NOVA_FileList_Vita.cpk Phantasy_Star_Nova_Vita_KO_v1.0_main.xdelta
xdelta3 -e -0 -S none -A -s work\orig\NOVA_FileList_Vita_movie.cpk out\NOVA_FileList_Vita_movie.cpk Phantasy_Star_Nova_Vita_KO_v1.0_movie.xdelta
```

## 번역 수정

- `text/ko.json`: `{"<메시지 ID>": "한국어"}`. `\n`은 줄바꿈입니다. `<...>` 형식 태그는 그대로 둡니다. 원문은 `work/msg/msg_<ID>.rmd`를 `tools/rmd.py`로 읽어 볼 수 있습니다.
- 그림 글자: `text/images/<텍스처>.py`의 `B` 목록을 고칩니다. 항목은 `(x0, y0, x1, y1, '한국어', 옵션)`이며 옵션은 `font`(hv·eb·bd·rg·sh·shm·gal), `color`, `outline`, `sw`(외곽선 두께), `bg`(배경 처리), `align`, `scale`입니다.
- NPC 이름: `text/names.json`(일본어 이름 SHA-1 앞 16자리 → 로마자).
- 동영상 자막: `text/movies/<영상>.json`의 `ko`. `-`는 자막 없이 지우기만 합니다.

## 에뮬레이터 확인

`tools/emu.py`는 저장소 옆 `emu/`에 설치한 Vita3K를 보이지 않는 창으로 띄워 키 입력과 스크린샷(F12)을 보냅니다. `start`, `key c _2 x`, `shot out.png`, `stop` 순서로 씁니다. 결과 CPK를 `emu/fs/ux0/app/PCSG00351/`에 넣고 확인합니다. 일본판이라 ○가 결정, ✕가 취소입니다.
