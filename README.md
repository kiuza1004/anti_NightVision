# ARGON NV · Gen-4 Optical Night Vision Web App

모바일 및 데스크톱 웹 브라우저에서 동작하는 전술 광학 야간 투시(Night Vision) 웹 애플리케이션입니다.  
외부 라이브러리나 빌드 도구 없이 단일 [`index.html`](file:///D:/AI_Antigravity/NightVision/index.html)로 구성되어 최고의 호환성과 60fps 성능을 제공합니다.

- **웹앱 실행 URL**: [https://kiuza1004.github.io/anti_NightVision/](https://kiuza1004.github.io/anti_NightVision/)
- **저장소**: [https://github.com/kiuza1004/anti_NightVision](https://github.com/kiuza1004/anti_NightVision)

---

## 주요 기능

### 1. 01 필터 투시 모드 (Filter Mode)
- **Reinhard Soft-Knee Tone Mapping**: 하이라이트 화이트아웃(번짐)을 억제하면서 암부 디테일을 끌어올리는 비선형 광학 증폭
- **4종 전술 광학 팔레트**:
  - **P43 그린 (Phosphor Green)**: 클래식 야간 투시경 녹색 형광체 톤
  - **P45 화이트 (White Phosphor)**: 고대비 아이스 시안/화이트 포스퍼 톤
  - **전술 앰버 (Tactical Amber)**: 눈부심 억제 앰버 골드 톤
  - **열화상 LUT (Thermal Ironbow)**: 사전 계산된 256단계 RGB 룩업 테이블(`Uint8Array`) 기반 실시간 의사 열화상 변환
- **시간축 노이즈 억제 (Temporal DNR)**: `Float32Array` 지수 이동 평균(EMA) 버퍼를 통해 야간 고감도 증폭 시 발생하는 센서 노이즈 실시간 제거
- **실시간 루미넌스 히스토그램 & 전술 HUD**: 32-bin 실시간 휘도 분포 그래프, 조준 레티클, 디지털 줌(1.0×~4.0×), 자동 감도(AUTO GAIN), 원본 비교(HOLD), 즉시 스냅샷 캡처 지원

### 2. 02 장노출 합성 모드 (Long Exposure Mode)
- **노출 시간 선택**: `1.5s` / `3.0s` / `5.0s` 다중 프레임 누적 촬영
- **3종 합성 엔진**:
  - **MAX (빛 모으기)**: 프레임 간 채널별 최댓값을 취해 별빛, 미세 광원, 광궤적 포착
  - **AVG (노이즈 제거)**: 프레임 누적 평균으로 암부 열잡음 및 노이즈 제거
  - **HDR (톤매핑 합성)**: 누적 평균 데이터에 Reinhard 소프트-니 톤매핑을 결합해 명부 클리핑 방지 및 암부 극대화
- **라이브 프로그레시브 프리뷰**: 촬영 중 빛이 누적되어 밝아지는 과정을 캔버스에 실시간으로 렌더링

### 3. 03 센서 · 진단 모드 (Sensor & Diagnostics Mode)
- **WebXR Depth & AR 진단**: 기기의 하드웨어 깊이 센서(`depth-sensing`, ToF/LiDAR) 지원 여부 판별
- **광학 스트림 텔레메트리**: 카메라 해상도, 실시간 FPS, 노출 모드, EV 보정 범위, 포커스 모드, 하드웨어 토치(플래시) 가용성 표시
- **장면 광도 분석 (Scene Photometry)**: 평균 휘도, 암부/명부 비율 및 현재 조도에 따른 최적 증폭 배율 자동 산출

---

## 실행 방법

카메라 스트림(`getUserMedia`)은 **`https://`** 또는 **`localhost` / `127.0.0.1`** 환경에서만 동작합니다.

```bash
# 로컬 개발 서버 실행 (포트 8000)
python serve.py 8000
```
브라우저에서 `http://localhost:8000`에 접속합니다.
