# Capital Imbalance Engine → "Flow" (또는 "Capital Weather")

## UI 철학 재설계 로드맵

**문서 작성:** 2026-07-03  
**전환 목표:** "통계 프로그램" → "관측 플랫폼"

---

## Executive Summary

### 현재 상태
```
기술: 9/10 ✅ 우수
철학: 4/10 ⚠️ 미흡
전체: 5/10 (재설계 필요)
```

### 목표
```
기술: 9/10 (유지)
철학: 9/10 (개선)
전체: 9/10 (사용자 중심 제품으로 전환)
```

---

## 핵심 전략

### 1. 제품명 이중화

| 대상 | 이름 | 특징 |
|------|------|------|
| **사용자** | **"Flow"** 또는 **"Capital Weather"** | 직관적, 단순, 일상적 |
| **개발자** | "Capital Imbalance Engine" | 기술적, 정확, 과학적 |

**의도:** 복잡한 엔진을 단순한 인터페이스로 감싸기

---

## 메인 화면 재설계

### Current (문제)
```
📊 Capital Imbalance Engine 🔴 LIVE

AI/GPU         100.0%
Power/Energy     0.0%
Water            0.0%
[도넛 차트]
```

**문제점:**
- 숫자로 시작 ("아 뭐야?")
- 정적 (변화 없음)
- "그래서?" 질문 유발

---

### After: "Today's Capital Weather"

#### Card 1️⃣: Today's Observation (가장 중요)

```
🌍 Today's Observation

TODAY'S SUMMARY

새로운 Reservoir
❌ 없음

Pressure 변화
🔴 AI: Cooling ↓
🟠 Power: Observing ↑

Reservoir Status
🔵 HBM: Stable (214일)
🟡 Power: Candidate (Confidence 43%)

Observation Confidence
✅ 91%
```

**효과:** 첫 30초 만에 세계 자본 상황 이해

---

#### Card 2️⃣: Reservoir Weather

```
🌡️ Reservoir Weather

Active Reservoirs

🔴 AI Compute
Status: Cooling
Duration: 214 days (2023-05 ~ now)
Confidence: 91%

Watch List

🟡 Power (Emerging)
Pressure up: +31 days
Confidence: 43%
⚠️ Need continuous monitoring
```

---

#### Card 3️⃣: Lifecycle Timeline (NEW - 시간축)

```
📈 Lifecycle Timeline

AI Compute
Growing ──── Peak ──── Cooling ──── Decay
2023    2024    2025    2026    →

Power (Candidate)
──────────── Early Signal ────
2026-01   2026-07    2026-?

Confidence increases over time
```

**핵심:** 숫자 대신 **시간 변화**를 보여줌

---

#### Card 4️⃣: Observation Process (강화)

```
📋 Today's Observation Log

뉴스 수집
✅ 797건 수집 (6시간)

증거 추출
✅ 214개 Pressure 신호

분석
✅ AI Pressure: -5 (Cooling)
✅ Power Pressure: +3 (Emerging)

새 Reservoir 감지
❌ 없음

Observation 완료
✅ 신뢰도 91%

다음 관찰
⏰ 내일 09:00
```

**효과:** "관측 과정"이 신뢰를 만든다

---

## 색상 코드 (기상청 스타일)

```
🔴 Red: Cooling / Bubble / High Risk / Overheated
🟠 Orange: Candidate / Emerging / Monitor Closely
🟡 Yellow: Caution / Pressure Rising / Yellow Alert
🟢 Green: Stable / Normal / No Change
🔵 Blue: Information / Historical / Reference
⚫ Black: N/A / No Signal / Dormant
```

---

## 메뉴 구조

```
Flow (또는 Capital Weather)

├─ 🌍 Today's Weather (메인 대시보드)
│  ├─ Today's Observation
│  ├─ Reservoir Weather
│  ├─ Timeline
│  └─ Observation Log

├─ 🔍 Deep Dive (상세 분석)
│  ├─ AI Compute (5년 역사)
│  ├─ Power (새로운 후보)
│  ├─ Water
│  ├─ Shipping
│  └─ Food

├─ 📊 Historical Data
│  ├─ 5-Year Timeline
│  ├─ Case Studies (HBM, etc)
│  └─ Patterns

├─ ⚙️ About Engine
│  ├─ Capital Imbalance Theory
│  ├─ Methodology
│  ├─ Confidence Metrics
│  └─ How It Works
```

---

## 구현 로드맵

### Phase 1: Philosophy & Branding (1주)
- [ ] 제품명 선정: "Flow" 또는 "Capital Weather"
- [ ] 로고 디자인 (기상청 스타일)
- [ ] 색상 코드 정의
- [ ] 메뉴 구조 최종화

### Phase 2: Today's Weather 화면 (2주)
- [ ] "Today's Observation" 카드 구현
- [ ] "Reservoir Weather" 카드 구현
- [ ] 색상 및 아이콘 적용
- [ ] 모바일 반응형 테스트

### Phase 3: Timeline 추가 (1주)
- [ ] Lifecycle timeline 그래프 (시간축)
- [ ] Historical data visualization
- [ ] Interactive timeline

### Phase 4: Process Transparency (1주)
- [ ] Observation Log 상세화
- [ ] Step-by-step visualization
- [ ] Confidence metrics 시각화

### Phase 5: Deep Dive Pages (2주)
- [ ] 각 Reservoir 상세 분석 페이지
- [ ] 5-year case study pages
- [ ] Historical comparison

### Phase 6: Refinement (1주)
- [ ] 사용성 테스트
- [ ] 성능 최적화
- [ ] 모바일 완성

**총 예상 기간:** 4-5주

---

## 설계 원칙

### 1. 시간축 강조

```
Before: "75.6%" (정적)
After: "214일 지속 중" (동적)
```

### 2. 관측 과정 투명화

```
결론 ❌
→
관측 과정 ✅
```

### 3. 한눈에 이해

```
최고의 UI = 설명 없이 이해 가능
5초 관찰 → 상황 파악
```

### 4. 기상청 은유

```
"오늘 날씨?" = "오늘 자본이 어디로?"

고기압 = 자본 집중
저기압 = 기회 (저평가)
전선 = 변화 중
폭우 = 버블
```

---

## 예상 효과

### Before
```
"자본 불균형 엔진?"
→ "뭐 하는 건데?"
→ "복잡함" 느낌
→ 떠난다
```

### After
```
"Capital Weather"
→ "아, 오늘 뭐 됐네?"
→ "단순함" 느낌
→ 매일 확인한다
```

---

## 성공 지표

| 지표 | 현재 | 목표 | 검증 |
|------|------|------|------|
| **초 단위 이해도** | 30초 어려움 | 5초 이해 | 사용자 테스트 |
| **철학 전달** | 4/10 | 9/10 | 설문 |
| **일일 사용자** | 낮음 | 높음 | 분석 |
| **기술 점수** | 9/10 | 9/10 | 자동화 테스트 |

---

## 핵심 인사이트

### 차이점: 제품 vs 엔진

```
좋은 엔진
= 복잡한 기술
= 엔지니어들이 쓴다

좋은 제품
= 엔진을 감싼다
= 모두가 매일 쓴다
```

### 현재 상태

- ✅ 엔진: 8~9점 (훌륭함)
- ⚠️ 제품: 4/10 (엔진이 노출됨)

### 목표

- ✅ 엔진: 9/10 (유지/개선)
- ✅ 제품: 9/10 (감싸기)

---

## 다음 단계

1. **이 문서 검토**: 철학에 동의하는가?
2. **제품명 선정**: "Flow" vs "Capital Weather"
3. **Phase 1 시작**: 로고, 색상, 구조

---

## 최종 비전

> **"매일 확인하는 관측 플랫폼"**
>
> 날씨 앱처럼 매일 열어서 "오늘 세계 자본이 어디로 흐르나"를 본다.
>
> 그 순간, Capital Imbalance Engine은 단순한 분석 도구가 아니라
> **필수 불가결한 금융 인프라**가 된다.
