# ANTIGRAVITY.md

이 문서는 Antigravity 환경에서 ARGON NV (Night Vision) 코드베이스를 분석하고 유지보수할 때 준수해야 할 아키텍처 명세입니다.

---

## 1. 아키텍처 핵심 원칙

- **단일 파일 무의존성 구조**: 모든 HTML, CSS, JavaScript는 [`index.html`](file:///D:/AI_Antigravity/NightVision/index.html) 단일 파일에 위치하며, 외부 라이브러리나 빌드 도구를 일절 사용하지 않습니다.
- **Zero-Allocation 핫패스**: 매 프레임 실행되는 [`renderFilter`](file:///D:/AI_Antigravity/NightVision/index.html#L653-L735) 루프 내부에서는 객체 생성을 금지하고 사전 할당된 `Float32Array`(`dnrBuffer`), `Uint32Array`(`histBins`), `Uint8Array`(`thermalLUT`) 및 비트 연산(`| 0`)만을 사용합니다.

---

## 2. 광학 처리 파이프라인 (ISP Pipeline)

### 2.1 Reinhard Soft-Knee Tone-Mapping & Temporal DNR
```javascript
const lum = d[i] * 0.299 + d[i + 1] * 0.587 + d[i + 2] * 0.114;
const raw = lum * pixelGain + offset;
let boost = (255 * raw) / (raw + knee);

if (dnrActive) {
  const prev = dnrBuffer[p];
  boost = prev === 0 ? boost : (prev * dnrAlpha + boost * (1 - dnrAlpha));
  dnrBuffer[p] = boost;
}
```
> [!CAUTION]
> **과도한 밝기 중복 증폭(Stacked Brightness Boost) 금지**  
> 카메라 하드웨어 `exposureCompensation`을 강제로 최대치로 올리거나 `ctx.filter = brightness(...)`를 픽셀 루프와 중첩하면 정상 조도에서 화이트아웃이 발생합니다. 밝기 증폭은 반드시 소프트웨어 게인(`gain`)과 Reinhard 소프트-니 톤매핑으로만 제어합니다.

### 2.2 4종 컬러 팔레트 및 사전 계산 LUT
- `green` (P43), `white` (P45), `amber` (전술 앰버)는 단일 곱연산 및 비트 절삭으로 처리합니다.
- `thermal` (열화상 의사 컬러)은 초기화 시 생성된 256×3 크기의 [`thermalLUT`](file:///D:/AI_Antigravity/NightVision/index.html#L448-L473) 배열을 O(1) 인덱싱으로 참조하여 프레임 드랍 없이 렌더링합니다.

### 2.3 프로그레시브 장노출 합성 ([`startLongExposure`](file:///D:/AI_Antigravity/NightVision/index.html#L783-L869))
- `1.5s`, `3.0s`, `5.0s` 동안 `Float32Array(w * h * 3)` 버퍼에 프레임을 누적하면서 매 프레임 합성 과정을 메인 캔버스에 실시간으로 렌더링합니다.
- 지원 합성 모드: `max` (최댓값 합성), `avg` (평균 노이즈 억제), `hdr` (누적 평균 + Reinhard 소프트-니 톤매핑).

---

## 3. 수명 주기 및 호환성

- `visibilitychange` 이벤트에서 백그라운드 진입 시 즉시 `cancelAnimationFrame`을 호출하고 포그라운드 복귀 시 현재 모드의 루프를 복원합니다.
- 캔버스 리사이즈([`resizeCanvas`](file:///D:/AI_Antigravity/NightVision/index.html#L556-L566)) 발생 시 픽셀 수가 변경되므로 `dnrBuffer = null`로 초기화하여 다음 프레임에 새 해상도에 맞게 재할당되도록 보장합니다.
