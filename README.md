# Night Vision Web App

모바일 및 데스크톱 웹 브라우저에서 동작하는 고성능 야간 투시(Night Vision) 웹 애플리케이션입니다.  
외부 번들러나 빌드 도구 없이 단일 [`index.html`](file:///D:/AI_Antigravity/NightVision/index.html)로 구성되어 가볍고 빠른 실행이 가능합니다.

- **웹앱 접속 URL**: [https://kiuza1004.github.io/anti_NightVision/](https://kiuza1004.github.io/anti_NightVision/)
- **저장소**: [https://github.com/kiuza1004/anti_NightVision](https://github.com/kiuza1004/anti_NightVision)

---

## 주요 기능

1. **필터 모드 (Filter Mode)**
   - 후면 카메라 스트림에 실시간 픽셀 조작 파이프라인 적용
   - **Reinhard Soft-Knee Tone Mapping**: 하이라이트 번짐 방지 및 중간톤 대비 향상
   - **소프트웨어 감도 게인(Gain ×1.0 ~ ×8.0)**: 슬라이더를 통한 즉각적인 밝기 제어
   - 야간 투시경 스타일의 모노크롬 그린 톤(`R·0.10`, `G·1.0`, `B·0.18`) 및 비네팅 렌더링

2. **장노출 모드 (Long Exposure Mode)**
   - 3초간 입력 프레임을 부동소수점 버퍼(`Float32Array`)에 누적 합성
   - **Max 모드 (빛 모으기)**: 프레임 간 최대 밝기를 선택하여 별빛, 가로등, 불빛 궤적 포착
   - **Avg 모드 (노이즈 감소)**: 프레임 평균을 계산하여 야간 암부의 센서 노이즈 대폭 억제
   - 촬영 완료 후 타임스탬프가 포함된 고화질 PNG 저장 지원 (`night-vision-YYYYMMDD_HHmmss.png`)

3. **센서 모드 (Sensor Mode)**
   - WebXR Device API 기반의 `immersive-ar` 및 `depth-sensing` 하드웨어 지원 여부 실시간 진단
   - 미지원 기기에서도 친절한 피드백 메시지 제공

---

## 실행 방법

카메라 스트림(`getUserMedia`)은 브라우저 보안 정책상 **`https://`** 또는 **`localhost` / `127.0.0.1`** 환경에서만 동작합니다.

### 1. 로컬 환경 (데스크톱 테스트)
Python 기본 내장 모듈을 통해 즉시 실행할 수 있습니다:
```bash
# 기본 HTTP 서버 실행 (포트 8000)
python serve.py
# 또는
python -m http.server 8000
```
브라우저에서 `http://localhost:8000`에 접속합니다.

### 2. 모바일 기기 테스트
모바일 브라우저에서 테스트할 경우 다음 방법 중 하나를 권장합니다:
- **GitHub Pages / Vercel 배포**: 자동 HTTPS가 적용되어 모바일 실기기 테스트에 가장 적합합니다.
- **로컬 HTTPS 서빙**: `mkcert` 등을 사용해 로컬 인증서를 발급한 후 서빙합니다.

---

## 기술 스택 및 호환성

- **프론트엔드**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **그래픽스**: HTML5 Canvas 2D Context (`willReadFrequently: true` 최적화)
- **미디어/센서**: MediaDevices API (`getUserMedia`), WebXR Device API
- **권장 브라우저**:
  - Android: Chrome / Edge (WebXR Depth Sensing 일부 기기 지원)
  - iOS: Safari (카메라, 필터, 장노출 지원)
