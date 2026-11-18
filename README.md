# 판타지 스타 노바 PS Vita 한글패치

PS Vita 일본판 **판타지 스타 노바 (ファンタシースター ノヴァ, PCSG00351)**용 비공식 한국어 패치입니다. 스토리 대사·메뉴·아이템·장비·스킬·퀘스트·튜토리얼·상점까지 게임 안 일본어 메시지 **21,167개 전체**를 한국어로 직접 번역했습니다. 타이틀 한글 부제, 메뉴·튜토리얼 그림 글자 **83장**, 이벤트 캡션 글자판, 오프닝 등 동영상 **8개**의 자막(**141문장**)도 한글로 바꿨습니다. 현재 배포판은 **v1.0.1 (2026-11-18)**입니다.

[패치 다운로드](https://github.com/snake759494/phantasy-star-nova-vita-korean-patch/releases/latest) · [기술 설명](docs/TECHNICAL.md) · [재빌드](docs/BUILD.md) · [용어집](docs/GLOSSARY.md) · [변경 기록](CHANGELOG.md) · [권리 안내](RIGHTS.md)

릴리즈 첨부 파일은 게임 데이터 파일 2개에 각각 대응하는 xdelta 2개입니다. 저장소에는 제작 소스와 한국어 번역만 공개합니다. 원본·완성 게임 파일, 추출한 게임 데이터·그림·영상, 일본어 원문, 글꼴 파일, 외부 실행 파일은 포함하지 않습니다. GitHub가 자동으로 만드는 Source code ZIP/TAR는 저장소 소스를 압축한 것이며 게임 파일이 아닙니다.

## 게임 소개 및 대상 버전

『판타지 스타 노바』는 세가가 발매하고 트라이에이스가 개발한 PS Vita용 액션 RPG입니다(2014년 11월, 일본 발매). 『판타지 스타 온라인 2』와 같은 세계관에서, 미지의 행성 「마키아」에 불시착한 탐사선 「델타 배리언트」의 대원들이 포톤이 통하지 않는 환경에서 「그랑」이라는 새 힘을 얻어 거대한 「기간테스」와 싸우며 살아남는 이야기입니다. 거점을 넓히고 장비를 만들며, 최대 4명이 협력해 거대 적을 쓰러뜨립니다. 일본에서만 발매되었습니다.

이 패치는 **PS Vita 일본판(PCSG00351, 버전 01.00)의 게임 폴더에 있는 CPK 2개**에 적용합니다. 복호화된 게임 폴더(`ux0:app/PCSG00351/`)에 있는 파일이어야 합니다. 파일 이름보다 아래 크기와 해시가 일치하는지가 중요합니다.

## 적용할 원본

| 파일 | 크기 | MD5 | SHA-256 |
| --- | --- | --- | --- |
| 원본 `NOVA_FileList_Vita.cpk` | 2,834,095,024 B | `cc10190d7c45c0ea0159142b1e5f98bf` | `ad85c330c3258b0f18f57dcf77736f9fbea89c40b66dfef3fbb5c4daeff77e7a` |
| 원본 `NOVA_FileList_Vita_movie.cpk` | 395,112,448 B | `60002c4ef23b32f28f7b26e460099e5e` | `b006fcbf06008c1271b47b3999798e042243c6c99de570a6e069188ec971a01e` |
| 결과 `NOVA_FileList_Vita.cpk` | 3,369,310,104 B | `d4d1a7d863eaa25f07979d989000c9df` | `f36e1c28cbee8b1214fdb69a2233a5030d8bf0b7dfd13ac4d11aad4f92b7de9d` |
| 결과 `NOVA_FileList_Vita_movie.cpk` | 395,112,448 B | `ae900ebab8aa1c916cd89a802a3bb00e` | `0eeeee9fcc1cbac72f6dc18929d28ac165e560eb41053dc4a775ba1764d808c0` |
| `Phantasy_Star_Nova_Vita_KO_v1.0.1_main.xdelta` | 224,635,541 B | — | `0282e034fc2998a4b2b12f4cc893cb86e73ca5ef4584f9c8eacfafa6e8005ffd` |
| `Phantasy_Star_Nova_Vita_KO_v1.0.1_movie.xdelta` | 192,230,175 B | — | `8962d6306bf1da7c85462f11ca3ccc77b594328908a533747e55319948b98b09` |

SHA-1과 xdelta의 MD5는 [release_manifest.json](release_manifest.json)에 있습니다. 원본 게임 파일은 사용자가 직접 준비해야 합니다. `eboot.bin`과 그 밖의 파일은 바꾸지 않습니다.

## 패치 적용 방법

### Windows에서 원본 확인

```powershell
Get-FileHash -Algorithm MD5 -LiteralPath '.\NOVA_FileList_Vita.cpk'
Get-FileHash -Algorithm MD5 -LiteralPath '.\NOVA_FileList_Vita_movie.cpk'
```

위 표와 다르면 적용을 중단하세요.

### xdelta UI 사용

1. 릴리즈에서 xdelta 2개를 받습니다.
2. xdelta3 패치를 지원하는 도구에서 **Apply Patch** 기능을 엽니다.
3. **Patch**에는 xdelta 파일을, **Source File**에는 해시가 일치하는 원본 CPK를 선택합니다(`..._main.xdelta` → `NOVA_FileList_Vita.cpk`, `..._movie.xdelta` → `NOVA_FileList_Vita_movie.cpk`).
4. **Output File**에는 새 파일 이름을 지정합니다(예: `NOVA_FileList_Vita_ko.cpk`). 다 만든 뒤 원래 이름으로 바꿔 아래 위치에 넣습니다.

xdelta는 호환성을 위해 압축·2차 압축·파일 경로 헤더 없이 만들었습니다. 본체 결과 파일이 3.3GB이므로 저장 공간을 넉넉히 확보하세요. xdelta 자체는 [공식 프로젝트](https://github.com/jmacd/xdelta)를 참고하세요.

### 명령줄 사용

```powershell
.\xdelta3.exe -d -B 1073741824 -s '.\NOVA_FileList_Vita.cpk' '.\Phantasy_Star_Nova_Vita_KO_v1.0.1_main.xdelta' '.\ko\NOVA_FileList_Vita.cpk'
.\xdelta3.exe -d -B 1073741824 -s '.\NOVA_FileList_Vita_movie.cpk' '.\Phantasy_Star_Nova_Vita_KO_v1.0.1_movie.xdelta' '.\ko\NOVA_FileList_Vita_movie.cpk'
```

해시를 자동으로 검사하는 도구도 있습니다. Python 3와 xdelta3가 필요하며, 원본 CPK 2개와 xdelta 2개가 있는 폴더를 지정하면 결과를 출력 폴더에 만듭니다. 같은 이름의 출력 파일이 이미 있으면 덮어쓰지 않습니다.

```powershell
python tools/apply_release.py --xdelta '.\xdelta3.exe' --source-dir '.\PCSG00351' --patch-dir '.\patch' --output-dir '.\ko'
```

### 게임에 넣기

- **PS Vita 실기(rePatch, 권장)**: 결과 CPK 2개를 `ux0:rePatch/PCSG00351/`에 복사합니다. 원본 게임 폴더는 그대로 둡니다.
- **PS Vita 실기(직접 교체)**: `ux0:app/PCSG00351/`의 CPK 2개를 백업한 뒤 결과 파일로 덮어씁니다.
- **Vita3K**: 설치된 게임 폴더(`<Vita3K 데이터 폴더>/ux0/app/PCSG00351/`)의 CPK 2개를 결과 파일로 바꿉니다.

동영상 자막이 필요 없으면 본체(`main`)만 적용해도 됩니다. 일본판이므로 **○ 버튼이 결정, ✕ 버튼이 취소**입니다. 세이브 데이터 형식은 바꾸지 않았습니다.

## 작업 내용과 범위

| 구분 | 작업량 및 내용 |
| --- | --- |
| 메시지 | 스토리 대사·선택지·퀘스트·튜토리얼·메뉴·옵션·아이템/장비/스킬 설명·상점·도감 등 일본어 메시지 **21,167개 전체** |
| 글리프 | 메시지마다 들어 있는 글자 아틀라스를 한글로 다시 그림(나눔스퀘어네오 Bd) |
| 그림 글자 | 타이틀 화면 한글 부제(「판타지 스타 노바」), 공용 UI·챕터 제목·로딩 화면, 튜토리얼 그림 속 설명 등 **83장** |
| 이벤트 캡션 | 이벤트 장면 대사 글자판 2장(`MP01_020_040`·`TE01_020_040`)을 한국어 대사 글자로 다시 그림 |
| 동영상 | 오프닝·이벤트 동영상 8개의 일본어 자막을 지우고 한국어 자막 **141문장**을 넣음 |
| NPC 이름 | 시스템 글꼴로 그려지는 필드 이름표 343명을 영문 로마자로 표기(예: Fieldea, Lutina) |

바꾼 파일은 원본 CPK 안에 덧붙이고 목차만 고쳤습니다. 원본 데이터는 그대로 남으므로 문장 길이 제한이 없습니다. 자세한 내용은 [docs/TECHNICAL.md](docs/TECHNICAL.md)를 참고하세요.

### 번역 원칙

- 외부 기계 번역 없이 일본어 원문과 문맥을 보고 직접 번역했습니다.
- 고유명사는 한 가지 표기로 통일했습니다([용어집](docs/GLOSSARY.md)). 예: 아크스, 다커, 포톤, 그랑, 기간테스, 델타 배리언트, 필디아, 루티나.
- 캐릭터 대사는 원작 말투를 살렸습니다.

### 번역하지 않은 것

- 음성(일본어)
- 필드 이름표 등 시스템 글꼴(Shift-JIS)로 그려지는 일부 이름: 한글을 표시할 수 없어 영문 로마자로 바꿨습니다.
- PHANTASY STAR NOVA 로고, 「PRESS START BUTTON」 등 영문 표기
- 스태프롤 일부 그림(쓰이지 않는 자리표시 그림)

## 알려진 한계

- 모든 장면을 직접 플레이하며 확인하지는 못했습니다. Vita3K에서 타이틀·캐릭터 크리에이트·오프닝과 추락 동영상 자막·첫 필드 미션(대사·튜토리얼·전투 UI·퀘스트 메시지)·거점 도착·메인 메뉴·아이템 메뉴를 확인했습니다.
- 이벤트 캡션 글자판(`MP01_020_040`)이 실제 장면에서 한글로 나오는지는 확인하지 못했습니다. 상점 화면도 직접 열어 보지 못했습니다.
- 긴 한국어 문장이 상자 밖으로 넘치는 곳이 있으면 이슈로 알려 주세요.
- 온라인(애드혹) 협력 플레이 화면과 실기에서의 동작은 확인하지 못했습니다.

## 저장소 구성

| 경로 | 내용 |
| --- | --- |
| `tools/prepare.py` | 원본 CPK에서 메시지 RMD와 그림 글자 텍스처를 `work/`에 풀어 냄 |
| `tools/build.py` | 원본 CPK에서 한글판 본체 CPK를 빌드(메시지 글리프, 그림 글자, NPC 이름, 이벤트 캡션) |
| `tools/movie.py` | 동영상 CPK의 하드자막 영상 8개를 한국어 자막으로 다시 만듦 |
| `tools/` | 빌드·검증 도구(Python). `cpk.py` CPK 읽기·쓰기, `rmd.py`·`basicmap.py` 메시지 형식, `build_msg.py` 메시지 글리프 아틀라스, `rmdtex.py`·`dxt.py` 텍스처(DXT1/DXT3, 스위즐), `uitex.py`·`uiapply.py` 그림 글자 재작성, `captex.py` 이벤트 캡션, `csvpatch.py`·`romaji.py` NPC 이름, `movsub.py`·`movpatch.py` 동영상 자막, `emu.py`·`hold.py`·`autoplay.py` 에뮬레이터 조작, `apply_release.py` 해시 검사 후 적용 |
| `text/ko.json` | 번역. `<메시지 ID>` → 한국어 |
| `text/images/` | 그림 글자 번역. 텍스처별 좌표·한국어·글자 스타일 |
| `text/movies/` | 동영상 자막 구간·위치·한국어 |
| `text/names.json` | NPC 이름 로마자 표기(일본어 이름의 해시로 연결) |
| `docs/` | 기술 설명, 재빌드 방법, 용어집, 글꼴 출처 |

권리 관련 내용은 [RIGHTS.md](RIGHTS.md)를 참고하세요.
