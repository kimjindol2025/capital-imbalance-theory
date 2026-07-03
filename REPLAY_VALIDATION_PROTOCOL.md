# Capital Physics Validation Protocol
## 5년 Replay 검증 실험 설계서

**작성일:** 2026-07-03  
**상태:** 실험 설계 확정  
**목표:** Reservoir 감지의 Lead Time 검증

---

## 🎯 핵심 질문

> **"2021년 신호로 Reservoir를 감지했다면,  
> 2021-2026년 사이에 실제로 맞았는가?"**

---

## 📊 검증 방식: Replay

### 시뮬레이션 Timeline

```
2021-01-01 ─── 시뮬레이션 시작점
   ↓
   [월별로 신호 하나씩 수집]
   - 2021-01: 기업 투자 신호 1개
   - 2021-02: 특허 출원 신호 2개
   - 2021-03: 정부 정책 신호 1개
   ↓
2021-06-30 ─── AI Reservoir 감지 (Pressure >= 300)
   ↓
   [이 순간의 Pressure 기록]
   AI Reservoir Detected: Pressure 320 (confidence 64%)
   ↓
2021-07-01 ~ 2026-06-30 ─── 검증 기간
   ↓
   [실제로 일어난 일들]
   - 2021: 엔비디아 GPU 수요 급증
   - 2022: 삼성/SK 반도체 투자 본격화
   - 2023: AI 부흥 (ChatGPT 등)
   - 2024-2026: AI 칩 가격 폭등, 채용 급증
   ↓
2026-07-03 ─── 검증
   "Reservoir가 정말 맞았나?"
```

---

## ✅ 검증 기준 (Validation Metrics)

### 1. Lead Time (얼마나 빨리 감지했나)

```
뉴스 보도: 2023-11 (ChatGPT 공개)
시장 반응: 2024-01 (주가 폭등)
Sensor 감지: 2021-06 (Replay에서 감지)

Lead Time = 시장 반응 - Sensor 감지
          = 2024-01 - 2021-06
          = 19개월 선행
```

**판정 기준:** Lead Time > 6개월 = ✅

### 2. Pressure Trajectory (계속 올라갔나)

```
2021-06: Pressure 320 → AI Reservoir 감지 ✅
  ↓
2021-12: Pressure 380 (상승) ✅
2022-06: Pressure 450 (상승) ✅
2023-06: Pressure 580 (상승) ✅
2024-06: Pressure 700 (상승) ✅
2026-06: Pressure 660 (약간 하락이지만 여전히 고강도) ✅
```

**판정 기준:** 
- 처음 감지 후 80% 이상 기간 동안 상승 또는 유지 = ✅
- 단순히 내려가면 = ❌

### 3. Reality Check (실제로 맞았나)

```
AI Reservoir가 감지됨 (2021-06)
  ↓
예측: "앞으로 AI 산업에 자본이 몰릴 것"
  ↓
실제 2021-2026:
  ✅ 엔비디아 GPU 주가 1000% 상승
  ✅ AI 칩 공급 부족 현상 발생
  ✅ 삼성/SK/TSMC 반도체 투자 폭증
  ✅ AI 인력 채용 급증
  ✅ 전력 수요 폭증 (GPU 전력 소비)
  
결론: "Reservoir 감지가 맞았다" ✅
```

---

## 🔍 검증 실행 계획

### Phase 1: 데이터 준비 (1주)

```
1. 2021-01 ~ 2026-06 월별 신호 데이터 수집
   - DART: 기업 투자 공시
   - 특허청: 특허 출원
   - 정부: 정책 발표
   - 뉴스: 보도 시점

2. Pressure 월별 계산
   - 2021-01: 20
   - 2021-02: 35
   - 2021-03: 45
   ... (월별)
   - 2026-06: 660

3. Reservoir 감지 시점 기록
   - AI: 2021-06 (Pressure 300)
   - Power: 2021-09 (Pressure 310)
   - Energy: 2021-08 (Pressure 305)
```

### Phase 2: Trajectory 분석 (1주)

```
각 Reservoir별로:
1. 감지 시점의 Pressure
2. 매월 Pressure 변화
3. 5년간 최고/최저
4. 최종 Pressure (2026-06)

그래프:
  Pressure
    |        ╱╲
    |       ╱  ╲
    |      ╱    ╲
  300 ───╱──────╲─── (threshold)
    |   /
    |  /
    └─────────────→ Time
    2021-06 ~ 2026-06
```

### Phase 3: Reality Verification (1주)

```
각 Reservoir별로 "실제로 맞았나" 확인:

AI:
  ✅ 엔비디아 주가 상승?
  ✅ GPU 공급 부족?
  ✅ 반도체 투자 증가?
  → 모두 YES = CONFIRMED

Power:
  ✅ 원전 논의 시작?
  ✅ 전력 수요 증가?
  ✅ 관련 투자 증가?
  → 모두 YES = CONFIRMED

Energy:
  ✅ EV 시장 확대?
  ✅ 배터리 투자 증가?
  ✅ 원자재 가격 상승?
  → 모두 YES = CONFIRMED
```

---

## 📈 예상 결과

### 최선의 경우 (Best Case)

```
3개 Reservoir 모두:
  ✅ Lead Time > 12개월
  ✅ Pressure 지속 상승
  ✅ Reality Check 100% 일치

→ "Capital Observatory는 정확하다"
→ 다음: 미래 Reservoir 예측 (2027-2030)
```

### 최악의 경우 (Worst Case)

```
1개 이상 Reservoir:
  ❌ Lead Time < 6개월
  ❌ Pressure 급락
  ❌ Reality Check 불일치

→ "일부 Reservoir는 오탐지"
→ 다음: 오탐지 원인 분석 + 필터 개선
```

---

## 🎯 최종 목표

```
"Sensor Observatory가 시장보다
 정말 6개월 이상 먼저 신호를 포착하는가?"

YES → Capital Observatory 검증 성공
NO  → 개선 후 재검증
```

---

## 📋 체크리스트

- [ ] 2021-2026 월별 신호 데이터 수집
- [ ] 월별 Pressure 계산
- [ ] Reservoir 감지 시점 확인
- [ ] Lead Time 계산
- [ ] Pressure Trajectory 분석
- [ ] Reality Check 증거 수집
- [ ] 최종 판정

---

## 🚀 시작 조건

```
✅ Ground Truth 정의 완료
✅ 3개 Reservoir 확정
✅ Replay 검증 설계서 작성

다음: Phase 1 시작 (데이터 수집)
```
