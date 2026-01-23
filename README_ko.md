# 🎨 SVG 마스터 프로 (SVG Master Pro)

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0+-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](LICENSE)

[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-important?style=for-the-badge)](#)

**SVG 마스터 프로**는 파이썬(PyQt6) 기반의 강력하고 직관적인 벡터 그래픽 편집 도구입니다. 복잡한 SVG 파일을 손쉽게 불러와 개별 요소를 편집, 그룹화하고, 원하는 부분만 추출하여 저장할 수 있습니다.

우아한 다크 모드 인터페이스와 함께 전문가 수준의 SVG 편집 경험을 제공합니다.

---

## ✨ 주요 기능

*   **📂 완벽한 SVG 호환성**: `svgelements` 엔진을 탑재하여 복잡한 SVG 경로와 속성을 정확하게 파싱하고 렌더링합니다.
*   **🖼️ 직관적인 캔버스**: 그리드 시스템, 마우스 드래그 이동, 휠 줌/팬 기능을 지원하는 고성능 캔버스.
*   **📦 스마트 그룹 관리**:
    *   여러 객체를 하나로 묶기 (`Ctrl+G`)
    *   그룹 해제하여 개별 수정하기 (`Ctrl+U`)
*   **🎨 실시간 스타일 편집**: 선택된 요소의 색상을 즉시 변경하고 미리볼 수 있습니다.
*   **📤 강력한 내보내기 시스템**:
    *   **선택 내보내기**: 원하는 객체만 골라 별도의 SVG 파일로 저장.
    *   **일괄 분할 저장**: 전체 디자인을 구성 요소별로 자동 분해하여 개별 파일로 대량 저장 (`이름_1.svg`, `이름_2.svg`...).
*   **🔍 자유로운 시각화**: 확대/축소(`Ctrl++`, `Ctrl+-`) 및 화면 맞춤(`Ctrl+0`) 기능을 통해 정밀한 작업이 가능합니다.
*   **🖱️ 편리한 컨텍스트 메뉴**: 마우스 우클릭으로 모든 주요 기능에 빠르게 접근 가능.

## 📦 배포 (Github Releases)

이 프로젝트는 Github Actions를 통해 **Linux, Windows, MacOS** 3대 운영체제용 단일 실행 파일을 자동으로 빌드합니다.
릴리즈 페이지에서 본인의 OS에 맞는 파일을 다운로드하여 별도의 설치 없이 바로 실행할 수 있습니다.
또한 `ghcr.io`를 통해 도커 이미지로도 제공됩니다.


## 🛠️ 설치 및 실행

사용 환경에 맞는 최적의 설치 방법을 선택하세요.

### 1. 🚀 데스크톱 앱 (추천)
별도의 설치 없이 [릴리즈 페이지](https://github.com/hslcrb/svgedit-aPyApp/releases)에서 본인의 OS에 맞는 실행 파일을 다운로드하여 바로 사용하세요.
- **Linux**: `SVGMasterPro_Linux`
- **Windows**: `SVGMasterPro_Windows.exe`
- **MacOS**: `SVGMasterPro_MacOS`

### 2. 🐳 도커 (Docker)
시스템에 직접 라이브러리를 설치하지 않고 도커를 사용하여 격리된 환경에서 실행할 수 있습니다.
```bash
# 최신 이미지 풀
docker pull ghcr.io/hslcrb/svgedit-apyapp:main

# X11 포워딩을 이용한 실행 (리눅스 예시)
xhost +local:docker
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ghcr.io/hslcrb/svgedit-apyapp:main
```

### 3. 🐍 소스 코드 (개발자용)

#### A. 간편 스크립트 사용
```bash
cd app
chmod +x run.sh
./run.sh
```

#### B. 수동 설치 및 실행
```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 필수 패키지 설치
pip install PyQt6 svgelements lxml

# 실행
python app/main.py
```


## 🎮 사용 가이드

| 동작 | 단축키 / 방법 | 설명 |
| :--- | :--- | :--- |
| **이동** | 마우스 드래그 | 선택한 객체를 자유롭게 이동합니다. |
| **다중 선택** | `Ctrl` + 클릭 | 여러 객체를 동시에 선택합니다. |
| **화면 이동** | 휠 클릭 드래그 | 캔버스를 상하좌우로 이동합니다 (패닝). |
| **그룹화** | `Ctrl` + `G` | 선택한 객체들을 하나의 그룹으로 묶습니다. |
| **그룹 해제** | `Ctrl` + `U` | 선택한 그룹을 개별 요소로 분리합니다. |
| **삭제** | `Delete` | 선택한 요소를 캔버스에서 제거합니다. |
| **메뉴 호출** | 마우스 우클릭 | 편집 메뉴를 호출합니다. |

---

## 📝 라이선스

이 프로젝트는 **GNU GPL v3** 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 및 [LICENSE_ko.md](./LICENSE_ko.md) 파일을 확인해 주세요.


Copyright (c) 2026 Rhee Works.
