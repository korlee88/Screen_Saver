# 260331_Screen Saver — Project Guide

## Project Overview

두 개의 독립된 Python 유틸리티로 구성된 프로젝트.

```
260331_Screen Saver/
├── screen saver/          # 화면보호기 방지 도구
│   ├── screen_saver.py    # 메인 스크립트 (pyautogui)
│   ├── screen_saver.spec  # PyInstaller 빌드 설정
│   └── dist/screen_saver.exe  # 빌드된 실행 파일
│
└── log_analysis/          # 산업장비 로그 분석 도구
    ├── app.py             # Flask 웹 앱 (인터랙티브 시각화)
    ├── log.py             # 독립 실행형 Plotly 스크립트
    ├── log.csv            # 장비 로그 데이터
    └── log_3kW.csv        # 3kW 장비 로그 데이터
```

---

## 1. Screen Saver (`screen saver/`)

### 목적
pyautogui를 사용해 9분 55초마다 현재 마우스 위치를 클릭하여 화면보호기 활성화를 방지.

### 실행
```bash
python screen_saver.py
# 또는 빌드된 exe 직접 실행
dist/screen_saver.exe
```

### 빌드 (PyInstaller)
```bash
pyinstaller screen_saver.spec
```

### 주요 설정
- `INTERVAL = 9 * 60 + 55` (595초) — screen_saver.py:5
- `pyautogui.FAILSAFE = True` — 마우스를 화면 모서리로 이동하면 긴급 종료

---

## 2. Log Analysis (`log_analysis/`)

### 목적
산업장비(마이크로파 전원공급장치)의 CSV 로그를 시각화하는 도구.

### CSV 포맷
```
ChannelID;Time;Value
9;2024-12-20T06:42:13;100.0
```
- 구분자: `;` (세미콜론)
- Time: ISO 8601 형식
- ChannelID: 정수 (채널 ID 맵 참고)

### 실행 방법

**웹 앱 (권장):**
```bash
cd log_analysis
source .venv/Scripts/activate
python app.py
# → http://localhost:5000 접속
```

**독립 스크립트:**
```bash
python log.py   # log.csv를 읽어 Plotly 창으로 표시
```

### 채널 구성 (CHANNEL_MAP)
| 신뢰도 | 주요 채널 |
|--------|-----------|
| HIGH   | Anode Current (9), Phase Voltages (35/36/37), Water Temperatures (11/12/17), Operating Hours |
| MEDIUM | Power Setpoint (0), Forward/Reflected Power (1/2), Head Temp/Humidity (5/7), PS Temps (13/14) |

- `na_marker`: 채널 17, 16에서 `127.0`은 N/A로 처리

### 채널 그룹
- **Power Supply**: 전원공급장치 관련 (전압, 전류, 온도, 습도)
- **Head**: 헤드부 온도/습도/전압
- **Magnetron**: 마그네트론 전력/전류/운영시간
- **기타**: 미분류 채널

### 의존성 (venv: Python 3.14.2)
- flask
- pandas
- plotly

### Flask 라우트
| 라우트 | 메서드 | 설명 |
|--------|--------|------|
| `/` | GET | 메인 UI |
| `/scan` | POST | CSV 파일의 채널 목록 반환 |
| `/plot` | POST | 선택된 채널/시간범위로 Plotly figure 반환 |

---

## 개발 환경

- Python: 3.14.2
- 가상환경: `log_analysis/.venv`
- 활성화: `source log_analysis/.venv/Scripts/activate`
- OS: Windows 11
