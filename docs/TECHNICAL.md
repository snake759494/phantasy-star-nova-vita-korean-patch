# 기술 설명

## CPK

게임 데이터는 `ux0:app/PCSG00351/`의 `NOVA_FileList_Vita.cpk`(대부분의 데이터)와 `NOVA_FileList_Vita_movie.cpk`(동영상)입니다. CRI CPK이며 `@UTF` 표는 XOR로 가려져 있습니다(키 0x655f에서 시작해 바이트마다 ×0x4115). 일부 파일은 CRILAYLA로 압축되어 있습니다(`tools/cpk.py`).

- 본체 CPK: 바꾼 파일을 ETOC가 있던 자리에 넣고 ETOC를 그 뒤로 옮긴 다음, TOC 행의 오프셋·크기와 헤더만 고칩니다(`cpk.patch_cpk`). 원본 데이터가 그대로 남으므로 xdelta가 작고 파일 크기 제한이 없습니다.
- 동영상 CPK: 다시 인코딩한 MP4를 원래 위치에 덮어쓰고(원본보다 작아야 함) TOC의 크기만 고칩니다(`tools/movpatch.py`).

## 메시지 (`msg_<ID>.rmd`)

대사·메뉴·아이템 설명 등 화면 문자열 21,167개가 각각 RMD 파일 하나입니다. 문자열은 16비트 토큰 열이며 7비트씩 나눠 쓴 값입니다(`v = (c>>8)<<7 | c&0x7f`).

- 값 1~373: 공용 글자표 `BasicCharSet`(숫자·영문·가나·기호, `tools/basicmap.py`)
- 값 401~: 그 메시지 RMD 안에 들어 있는 전용 글리프 아틀라스의 칸 번호
- 0x8000 이상: 제어 코드(`<c3>`…`</c>` 색, `<i..>` 아이콘, `0x8090` 이름 치환 등). 번역문에서는 `<cN>`, `</c>`, `<iN>`, `<XXXX>`(16진) 형식으로 씁니다.

메시지마다 쓰는 한자·한글 글리프를 RMD 안의 DXT3 텍스처(21px 칸, 칸이 많으면 18px)에 직접 그려 두는 구조라 게임 글꼴을 고칠 필요가 없습니다. 빌드는 번역문에서 공용 글자표에 있는 숫자·영문·기호는 공용 글자로, 한글은 나눔스퀘어네오 Bd로 새 아틀라스에 그려 RMD를 다시 만듭니다. 아틀라스 크기는 글자 수에 맞춰 128×32~512×512 중에서 고르고, 원본 메시지의 텍스처 헤더를 틀로 씁니다(`tools/build_msg.py`).

## 그림 글자 (`*.aif`)

UI 텍스처는 AIF(`rdda`/`Xgmi` 블록) 안의 DXT3(일부 DXT1) 데이터이며 Vita 스위즐이 걸려 있습니다(`tools/rmdtex.py`, `tools/dxt.py`). `text/images/<텍스처>.py`의 `B` 목록에 상자 좌표(x0, y0, x1, y1), 한국어, 글꼴·색·외곽선·배경 처리 방법을 적어 두면, 상자 안 원래 글자를 지우고(테두리 색 중앙값·좌우 보간·인페인팅 중 선택) 한글을 상자 크기에 맞춰 그린 뒤 다시 DXT로 인코딩합니다(`tools/uitex.py`, `tools/uiapply.py`).

## 이벤트 캡션 아틀라스

`MP01_020_040_Caption.aif`·`TE01_020_040_Caption.aif`는 이벤트 장면 대사 글자를 등장 순서대로 중복 없이 32px 칸(16열)에 그려 둔 글자판입니다. 빌드할 때 해당 장면 한국어 대사(메시지 ID `10102004…`)의 글자로 같은 규칙의 판을 다시 그립니다(`tools/captex.py`).

## NPC 이름 (시스템 글꼴)

필드 이름표처럼 실행 중에 만들어지는 일부 문자열은 Vita 시스템 글꼴(pvf)과 Shift-JIS로 그려져 한글을 쓸 수 없습니다. `NpcBaseParameter.csv` 27번째 열과 `uireferenceparameter.csv`의 `StringFix_Name*` 값은 영문 로마자 표기로 바꿨습니다(`tools/csvpatch.py`, 표기는 `text/names.json`, 목록에 없는 이름은 `tools/romaji.py`로 자동 변환).

## 동영상 자막

동영상 8개(오프닝 등)는 일본어 자막이 영상에 박혀 있습니다. 자막 구간을 밝기·채도로 찾아(`movsub.py scan`) 글자 영역을 인페인팅으로 지우고 한국어 자막을 그려 libx264로 다시 인코딩합니다(`movsub.py render`). 자막 구간·위치·한국어는 `text/movies/<영상>.json`에 있습니다.
