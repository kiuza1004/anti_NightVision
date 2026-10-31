# ANTIGRAVITY.md

이 문서는 Antigravity 환경에서 Night Vision 코드베이스를 분석하고 수정할 때 필요한 아키텍처 규칙과 개발 가이드를 정의합니다.

---

## 1. 프로젝트 구조

- **단일 파일 아키텍처**: 모든 프론트엔드 코드(HTML, CSS, JavaScript)는 [`index.html`](file:///D:/AI_Antigravity/NightVision/index.html) 단일 파일에 위치합니다.
- **무의존성(Zero-Dependency)**: 외부 패키지 매니저(npm, yarn), 번들러(webpack, vite), 외부 CDN 라이브러리를 사용하지 않고 순수 웹 표준 API로만 유지합니다.
- **국문 UI 유지**: UI 텍스트 및 에러 메시지는 일관된 한국어 톤을 유지합니다.

---

## 2. 렌더링 파이프라인 및 핵심 제약사항

### 2.1 Reinhard Soft-Knee Tone-Mapping (필터 모드)
```javascript
const lum = d[i] * 0.299 + d[i+1] * 0.587 + d[i+2] * 0.114;
const raw = lum * pixelGain + offset;
const boost = (255 * raw) / (raw + knee);
```
> [!CAUTION]
> **과도한 밝기 중복 증폭(Stacked Brightness Boost) 금지**  
> `ctx.filter = brightness(...)`와 픽셀 곱연산, 그리고 카메라 `exposureCompensation = max`를 동시에 적용하면 화면이 완전히 하얗게 날아가는 화이트아웃 현상이 발생합니다.  
> 반드시 **카메라 기본 노출 유지 + 단일 소프트웨어 게인 + Reinhard 톤매핑** 구조를 유지하십시오.

### 2.2 장노출 모드 (Long Exposure)
- `Float32Array(w * h * 3)` 정밀 누적 버퍼를 사용하여 정밀도 손실 없이 프레임을 합성합니다.
- `lxMode === 'max'`: 각 픽셀 채널의 최댓값을 취해 점광원 및 별빛 포착.
- `lxMode === 'avg'`: 프레임 누적합을 총 프레임 수로 나누어 야간 센서 노이즈 대폭 경감.
- 촬영 중 프레임 드랍을 막기 위해 오프스크린 캔버스에 `willReadFrequently: true` 옵션을 적용합니다.

### 2.3 WebXR 센서 모드
- 현재 WebXR 기기의 `immersive-ar` 세션 생성 및 `depth-sensing` 지원 여부를 안전하게 감지하고 피드백을 전달합니다.
- 미지원 환경(예: iOS Safari 또는 구형 안드로이드 기기)에서도 에러가 전파되지 않도록 우아하게 예외를 처리합니다.

---

## 3. 라이프사이클 및 브라우저 호환성 규칙

1. **자동재생 정책(Autoplay Policy) 방어**: 모바일 저전력 모드나 정책으로 인해 비디오 자동재생이 차단될 경우, 터치 시작 유도 오버레이([`playFallback`](file:///D:/AI_Antigravity/NightVision/index.html))를 통해 복구합니다.
2. **백그라운드 전환 감지**: `visibilitychange` 이벤트 수신 시 `cancelAnimationFrame`을 호출해 백그라운드 배터리 소모를 방지하고, 포그라운드 복귀 시 현재 모드 루프를 재개합니다.
3. **핫패스 최적화**: 매 프레임 실행되는 `getImageData` 루프 내부에서는 객체 할당(GC 유발), `Math.floor` 호출을 지양하고 비트 연산(`| 0`) 및 사전 할당 버퍼를 사용합니다.

---

## 4. 로컬 구동 및 테스트

Python 표준 라이브러리 기반 서버:
```bash
python serve.py 8000
```
웹 브라우저에서 `http://localhost:8000`에 접속하여 테스트합니다.
