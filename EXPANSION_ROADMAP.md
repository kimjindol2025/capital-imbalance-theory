# Sensor Observatory 확장 가능성 검토

**작성일:** 2026-07-03  
**목적:** 현재 시뮬레이션된 부분을 실제 데이터로 확장

---

## 현재 상태 점검

### ✅ 구현됨

```
sensor_observatory.py:
├── 뉴스        (Google News RSS - 실제, 인코딩 오류)
├── 공시        (5건 하드코딩)
├── 정부        (2건 하드코딩)
├── 특허        (5건 하드코딩)
├── 채용        (6건 하드코딩)
├── 입찰        (3건 하드코딩)
├── Flow Event  (자동 감지)
├── Pressure    (강도 계산)
└── Report      (JSON 저장)

dashboard.html:
├── 센서 신호 요약
├── 센서 상태 카드
├── Flow Events 표시
├── 뉴스 피드
└── 실행 로그

sensor_observatory_report.json:
└── 결과 저장
```

---

## 🚀 확장 가능한 부분 (우선순위)

### 1️⃣ 뉴스 센서 확장 (P0 - 즉시 가능)

**현재:**
```python
# Google News RSS (UTF-8 인코딩 오류)
url = "https://news.google.com/rss/search?q=AI+전력+채용+특허"
```

**확장 옵션:**

#### A. agent-reach 통합 (가장 강력)
```bash
# 14개 채널 동시 접근
agent-reach search "Semiconductor shortage" --channels=reddit,twitter,youtube,github
```

**장점:**
- API 비용 0
- 14개 채널 (Reddit, X, YouTube, GitHub, RSS, Bilibili 등)
- Self-healing router (통로 막히면 자동 전환)
- 인증 자동화

**구현:**
```python
import subprocess
import json

def collect_news_with_agent_reach(query):
    """agent-reach로 멀티 채널 뉴스 수집"""
    result = subprocess.run(
        ["agent-reach", "search", query, "--format=json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

#### B. Jina Reader (웹페이지 자동 읽기)
```bash
# 어떤 링크든 읽기 가능
curl "https://r.jina.ai/https://example.com"
```

#### C. RSS 피드 다중화
```python
feeds = [
    "https://news.ycombinator.com/rss",
    "https://techcrunch.com/feed/",
    "https://feeds.bloomberg.com/technology/news.rss",
    "https://www.reddit.com/r/technology/.rss",
]
```

---

### 2️⃣ 공시 센서 확장 (P1)

**현재:**
```python
# 하드코딩
disclosures = [
    {"company": "삼성전자", "amount": 20, "type": "투자", "category": "AI"},
]
```

**확장 옵션:**

#### 한국 - DART API (한국거래소)
```python
import requests

def collect_disclosures_korea():
    """DART API로 공시 자동 수집"""
    url = "https://opendart.fss.or.kr/api/list.json"
    params = {
        "crtfc_key": "YOUR_DART_API_KEY",
        "corp_code": "00126380",  # 삼성전자
        "bgn_de": "20260601",
        "end_de": "20260703",
    }
    response = requests.get(url, params=params)
    return response.json()
```

#### 미국 - SEC EDGAR
```python
def collect_disclosures_us():
    """SEC EDGAR로 미국 공시 수집"""
    url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": "0000789019",  # Microsoft
        "type": "8-K",  # 현재보고서
        "dateb": "20260703",
    }
```

---

### 3️⃣ 정부 센서 확장 (P1)

**현재:**
```python
# 하드코딩
gov_data = [
    {"title": "K-AI 전략 발표", "amount": 30},
]
```

**확장 옵션:**

#### 공공데이터포털
```python
def collect_government_korea():
    """공공데이터포털 API"""
    # 정부 정책, 입찰, 발표
    url = "https://www.data.go.kr/tcs/dss/selectApiDocumentDetail.do"
```

#### 정부입찰정보
```python
def collect_government_bidding():
    """나라장터 입찰정보"""
    url = "https://www.g2b.go.kr/index.jsp"
```

---

### 4️⃣ 특허 센서 확장 (P1)

**현재:**
```python
# 하드코딩
patents = [
    {"applicant": "삼성", "field": "AI", "date": "2026-07-03"},
]
```

**확장 옵션:**

#### 한국 특허청 API
```python
def collect_patents_korea():
    """한국 특허청 API"""
    url = "http://www.kipris.or.kr/openapi/search/openapiapilist"
```

#### Google Patents API
```python
def collect_patents_global():
    """Google Patents (라이센스 필요)"""
    # Selenium 기반 크롤링
    # agent-reach YouTube로 특허 발표 추적
```

#### WIPO (세계지식재산기구)
```python
url = "https://www.wipo.int/reference/en/statistics/"
```

---

### 5️⃣ 채용 센서 확장 (P2)

**현재:**
```python
# 하드코딩
jobs = [
    {"company": "삼성", "position": "AI 엔지니어", "count": 50},
]
```

**확장 옵션:**

#### LinkedIn API (agent-reach 지원)
```python
def collect_recruitment_linkedin():
    """agent-reach로 LinkedIn 채용 정보 크롤링"""
    result = subprocess.run([
        "agent-reach", "search",
        "site:linkedin.com/jobs AI engineer semiconductor",
        "--channels=web"
    ])
```

#### 원티드, 잡플래닛, 로켓펀치
```python
def collect_recruitment_korea():
    """한국 채용 사이트 크롤링"""
    # Selenium으로 실시간 채용공고 모니터링
```

#### GitHub Jobs (폐기됨, 대체: Jina Reader)
```python
def collect_recruitment_github():
    """GitHub에서 채용 정보 찾기"""
    url = "https://r.jina.ai/https://github.com/jobs"
```

---

### 6️⃣ 입찰 센서 확장 (P2)

**현재:**
```python
# 하드코딩
procurement = [
    {"buyer": "한국전력", "item": "초대형 변압기", "amount": 100},
]
```

**확장 옵션:**

#### 정부입찰정보시스템
```python
def collect_procurement_korea():
    """나라장터 입찰공고"""
    url = "https://www.g2b.go.kr:8080/ep/mybiz/myprocurement.do"
```

#### Bloomberg Supplychain
```python
def collect_procurement_global():
    """기업 공급망 추적"""
```

---

### 7️⃣ Flow Event Detector 개선 (P1)

**현재:**
```python
# 간단한 규칙 기반
if "투자" in disclosure.get("type", ""):
    self.flow_events.append({...})
```

**확장 옵션:**

#### A. NLP 기반 Signal 추출
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.clustering import KMeans

def detect_flow_events_nlp(signals):
    """NLP로 Flow Event 자동 감지"""
    # 뉴스 제목에서 핵심 신호 추출
    # 감정 분석 (긍정/부정/중립)
    # 엔티티 인식 (회사명, 금액, 기술)
```

#### B. Rule Engine
```python
FLOW_RULES = {
    "investment": {
        "keywords": ["투자", "인수", "합병"],
        "min_amount": 100,
        "importance": 90,
    },
    "patent_spike": {
        "condition": "count >= 2",
        "window": "7days",
        "importance": 60,
    },
}
```

#### C. LLM 기반 분류
```python
def classify_flow_event_llm(signal):
    """Claude를 사용한 Flow Event 판정"""
    response = client.messages.create(
        model="claude-opus-4-8",
        messages=[{
            "role": "user",
            "content": f"이것은 Flow Event인가? {signal['text']}"
        }]
    )
```

---

### 8️⃣ Pressure 계산 개선 (P2)

**현재:**
```python
# 합산만
total_importance = sum([e["importance"] for e in events])
```

**확장 옵션:**

#### A. 시계열 분석
```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

def analyze_pressure_timeseries():
    """Pressure 추세 분석"""
    df = pd.read_csv("daily_stats.csv")
    decomposition = seasonal_decompose(df["AI"], period=7)
```

#### B. 이상치 탐지
```python
from sklearn.ensemble import IsolationForest

def detect_pressure_anomaly(pressures):
    """비정상 Pressure 급증 탐지"""
    clf = IsolationForest()
    anomalies = clf.fit_predict(pressures)
```

#### C. 상관관계 분석
```python
def correlate_pressures():
    """센서 간 Pressure 상관관계"""
    # AI와 Power의 역상관?
    # Energy와 Recruitment의 선행성?
```

---

### 9️⃣ Dynamic Cluster Discovery (P0 - 핵심)

**현재:**
```python
# 사람이 분류
if "AI" in event["title"]:
    categories["AI"].append(event)
```

**확장 옵션:**

#### A. 자동 클러스터링
```python
from sklearn.cluster import DBSCAN
import numpy as np
from sentence_transformers import SentenceTransformer

def discover_clusters_auto(events):
    """신호의 자동 클러스터링"""
    # 각 이벤트를 임베딩 벡터로 변환
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([e["title"] for e in events])
    
    # DBSCAN 클러스터링 (사전 정의 없음)
    clustering = DBSCAN(eps=0.5, min_samples=2).fit(embeddings)
    
    return clustering.labels_
```

#### B. LLM 기반 Cluster Naming
```python
def name_cluster_llm(signals):
    """Claude가 Cluster 이름 지정"""
    response = client.messages.create(
        model="claude-opus-4-8",
        messages=[{
            "role": "user",
            "content": f"이 신호들을 어떻게 부를까? {signals}"
        }]
    )
    return response.content[0].text
```

#### C. Cluster 진화 추적
```python
def track_cluster_evolution():
    """Cluster의 생성→성장→쇠퇴 추적"""
    # Day 1: "CXL" 신호 3개 → Cluster 생성
    # Day 5: "CXL" 신호 15개 → Cluster 성장
    # Day 30: "CXL" 신호 0개 → Cluster 쇠퇴
```

---

### 🔟 대시보드 실시간화 (P1)

**현재:**
```javascript
// 하드코딩된 샘플 데이터
const events = [
    { type: '공시', title: '삼성전자 20조 AI 투자', ... },
];
```

**확장 옵션:**

#### A. 실시간 데이터 연결
```python
# FastAPI에서 실제 센서 데이터 반환
@app.get("/api/sensors/live")
async def get_live_sensors():
    """실시간 센서 신호"""
    return {
        "news": collect_news_live(),
        "disclosure": collect_disclosure_live(),
        "patent": collect_patent_live(),
        ...
    }
```

#### B. 차트 확장
```javascript
// 시계열 차트
new Chart(ctx, {
    type: 'line',
    data: {
        labels: dates,
        datasets: [
            { label: 'AI Pressure', data: pressures.AI },
            { label: 'Power Pressure', data: pressures.Power },
        ]
    }
});

// Cluster Timeline
Timeline showing:
- Cluster birth → growth → peak → decay
```

#### C. 알림 시스템
```python
# Pressure 급등 감지 시 알림
if pressure["AI"] > threshold:
    send_alert("AI Pressure 급증: 660 (Rising)")
```

---

## 📊 확장 로드맵

```
Phase 1 (현재)
├── ✅ Sensor Observatory v1.0 (시뮬레이션)
├── ✅ Flow Event Detector
├── ✅ Pressure 계산
└── ✅ Web Dashboard

Phase 2 (1-2주)
├── 🔄 agent-reach 통합 (뉴스 + 14개 채널)
├── 🔄 공시 API (DART, SEC EDGAR)
├── 🔄 정부 API (공공데이터포털)
└── 🔄 실시간 대시보드

Phase 3 (2-4주)
├── 🔄 특허 API (한국특허청, Google Patents)
├── 🔄 채용 센서 (LinkedIn, 원티드)
├── 🔄 입찰 센서 (나라장터)
└── 🔄 NLP 기반 Flow Event 감지

Phase 4 (1개월)
├── 🔄 자동 Cluster Discovery (DBSCAN)
├── 🔄 LLM 기반 Cluster Naming
├── 🔄 Cluster 진화 추적
└── 🔄 Dynamic Cluster Discovery 완성

Phase 5 (진행 중)
├── 📊 시계열 분석
├── 📊 이상치 탐지
├── 📊 상관관계 분석
└── 📊 Lead Time 극대화
```

---

## 💾 데이터 흐름 확장

```
FROM (현재):
Hardcoded → sensor_observatory.py → JSON → Dashboard

TO (확장):
┌──────────────────────┐
│  agent-reach (14채널) │
├──────────────────────┤
│  공시 API (DART)      │
├──────────────────────┤
│  정부 API (공공데이터) │
├──────────────────────┤
│  특허 API (특허청)    │
├──────────────────────┤
│  채용 크롤링          │
├──────────────────────┤
│  입찰 API (나라장터) │
└──────────────────────┘
        ↓
    Sensor Manager
        ↓
   Evidence Store (DB)
        ↓
   Flow Event Detector
        ↓
   Dynamic Cluster Discovery
        ↓
    Pressure Analysis
        ↓
   Real-time Dashboard
        ↓
   Alerts & Insights
```

---

## 🎯 다음 단계

1. **agent-reach 통합 (우선순위 1)**
   - subprocess로 agent-reach 호출
   - 14개 채널 신호 수집
   - 뉴스 센서 오류 해결

2. **API 통합 (우선순위 2)**
   - DART API로 공시 실시간 수집
   - SEC EDGAR로 글로벌 공시 추적

3. **Cluster Discovery (우선순위 3)**
   - DBSCAN 자동 클러스터링
   - LLM 기반 cluster naming

4. **실시간 대시보드 (우선순위 4)**
   - WebSocket 기반 실시간 업데이트
   - 차트 및 알림 추가

---

**이 확장이 완료되면, Sensor Observatory는 완전한 자동화 시스템이 됩니다!**
