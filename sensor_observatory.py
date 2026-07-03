#!/usr/bin/env python3
"""
Sensor Observatory v1.0
세상의 모든 신호를 수집하고 Flow Event만 추출
"""

import json
from pathlib import Path
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict

class SensorObservatory:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.sensors = {
            "news": [],
            "corporate_disclosure": [],  # 공시
            "government": [],            # 정부
            "patent": [],               # 특허
            "recruitment": [],          # 채용
            "procurement": [],          # 입찰
        }
        self.flow_events = []

    def collect_news(self):
        """뉴스 수집 (센서 1/6)"""
        print("\n📰 Sensor 1: News Collection")
        print("=" * 60)

        try:
            url = "https://news.google.com/rss/search?q=AI+전력+채용+특허&hl=ko&gl=KR&ceid=KR:ko"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)

                count = 0
                for item in root.findall('.//item')[:50]:
                    title_elem = item.find('title')
                    link_elem = item.find('link')

                    if title_elem is not None and link_elem is not None:
                        title = title_elem.text or ""
                        self.sensors["news"].append({
                            "title": title,
                            "link": link_elem.text or "",
                            "source": "Google News",
                            "timestamp": self.timestamp
                        })
                        count += 1

                print(f"✅ 뉴스 수집: {count}건")
                return count
        except Exception as e:
            print(f"❌ 뉴스 수집 실패: {str(e)[:50]}")
            return 0

    def collect_corporate_disclosure(self):
        """공시 데이터 (센서 2/6) - 시뮬레이션"""
        print("\n📋 Sensor 2: Corporate Disclosure")
        print("=" * 60)

        disclosures = [
            {"company": "삼성전자", "amount": 20, "type": "투자", "category": "AI"},
            {"company": "SK하이닉스", "amount": 15, "type": "투자", "category": "반도체"},
            {"company": "한국전력", "amount": 8, "type": "투자", "category": "전력"},
            {"company": "LG에너지솔루션", "amount": 12, "type": "투자", "category": "배터리"},
            {"company": "NAVER", "amount": 3, "type": "채용", "category": "AI"},
        ]

        self.sensors["corporate_disclosure"] = [
            {**d, "timestamp": self.timestamp, "importance": 90}
            for d in disclosures
        ]

        print(f"✅ 공시 수집: {len(disclosures)}건")
        return len(disclosures)

    def collect_government(self):
        """정부 발표 (센서 3/6) - 시뮬레이션"""
        print("\n🏛️ Sensor 3: Government")
        print("=" * 60)

        gov_data = [
            {"title": "K-AI 전략 발표", "amount": 30, "category": "AI"},
            {"title": "탄소중립 전력망 투자", "amount": 50, "category": "전력"},
        ]

        self.sensors["government"] = [
            {**d, "timestamp": self.timestamp, "importance": 100}
            for d in gov_data
        ]

        print(f"✅ 정부 발표: {len(gov_data)}건")
        return len(gov_data)

    def collect_patents(self):
        """특허 출원 (센서 4/6) - 시뮬레이션"""
        print("\n🔬 Sensor 4: Patents")
        print("=" * 60)

        patents = [
            {"applicant": "삼성", "field": "AI", "date": "2026-07-03"},
            {"applicant": "SK", "field": "배터리", "date": "2026-07-02"},
            {"applicant": "LG", "field": "AI", "date": "2026-07-01"},
            {"applicant": "현대", "field": "전기차", "date": "2026-06-30"},
            {"applicant": "SK", "field": "원전", "date": "2026-06-29"},
        ]

        self.sensors["patent"] = [
            {**p, "timestamp": self.timestamp, "importance": 60}
            for p in patents
        ]

        print(f"✅ 특허 수집: {len(patents)}건")
        return len(patents)

    def collect_recruitment(self):
        """채용 공고 (센서 5/6) - 시뮬레이션"""
        print("\n👥 Sensor 5: Recruitment")
        print("=" * 60)

        jobs = [
            {"company": "삼성", "position": "AI 엔지니어", "count": 50},
            {"company": "Google Korea", "position": "ML 엔지니어", "count": 30},
            {"company": "한국전력", "position": "전력 엔지니어", "count": 10},
            {"company": "LG Energy", "position": "배터리 기술자", "count": 25},
            {"company": "NAVER", "position": "AI 연구원", "count": 15},
            {"company": "Kakao", "position": "LLM 개발자", "count": 20},
        ]

        self.sensors["recruitment"] = [
            {**j, "timestamp": self.timestamp, "importance": 40}
            for j in jobs
        ]

        print(f"✅ 채용 정보: {len(jobs)}건")
        return len(jobs)

    def collect_procurement(self):
        """입찰/조달 (센서 6/6) - 시뮬레이션"""
        print("\n🛒 Sensor 6: Procurement")
        print("=" * 60)

        procurement = [
            {"buyer": "한국전력", "item": "초대형 변압기", "amount": 100},
            {"buyer": "삼성전자", "item": "GPU 칩", "amount": 500},
            {"buyer": "LG", "item": "배터리 재료", "amount": 200},
        ]

        self.sensors["procurement"] = [
            {**p, "timestamp": self.timestamp, "importance": 80}
            for p in procurement
        ]

        print(f"✅ 입찰 정보: {len(procurement)}건")
        return len(procurement)

    def detect_flow_events(self):
        """Flow Event 자동 감지"""
        print("\n\n🔍 Flow Event Detection")
        print("=" * 60)

        # 공시: 대부분 Flow Event
        for disclosure in self.sensors["corporate_disclosure"]:
            if "투자" in disclosure.get("type", ""):
                self.flow_events.append({
                    "type": "공시",
                    "title": f"{disclosure['company']} {disclosure['amount']}조 {disclosure['category']} 투자",
                    "importance": 90,
                    "sensor": "corporate_disclosure"
                })

        # 정부: 모두 Flow Event
        for gov in self.sensors["government"]:
            self.flow_events.append({
                "type": "정부",
                "title": gov["title"],
                "importance": 100,
                "sensor": "government"
            })

        # 특허: 다량 출원은 Flow Event
        patent_counts = defaultdict(int)
        for patent in self.sensors["patent"]:
            patent_counts[patent["field"]] += 1

        for field, count in patent_counts.items():
            if count >= 2:
                self.flow_events.append({
                    "type": "특허",
                    "title": f"{field} 특허 {count}건 집중 출원",
                    "importance": 60,
                    "sensor": "patent"
                })

        # 채용: 대량 채용은 Flow Event
        job_counts = defaultdict(int)
        for job in self.sensors["recruitment"]:
            job_counts[job["company"]] += 1

        for company, count in job_counts.items():
            if count >= 2:
                self.flow_events.append({
                    "type": "채용",
                    "title": f"{company} AI 관련 {count}개 직무 동시 채용",
                    "importance": 40,
                    "sensor": "recruitment"
                })

        # 입찰: 모두 Flow Event
        for proc in self.sensors["procurement"]:
            self.flow_events.append({
                "type": "입찰",
                "title": f"{proc['buyer']} {proc['item']} 발주",
                "importance": 80,
                "sensor": "procurement"
            })

        print(f"✅ Flow Event 감지: {len(self.flow_events)}건")

        # 카테고리별 분류
        categories = defaultdict(list)
        for event in self.flow_events:
            if "AI" in event["title"] or "GPU" in event["title"] or "LLM" in event["title"] or "ML" in event["title"]:
                categories["AI"].append(event)
            elif "전력" in event["title"] or "원전" in event["title"]:
                categories["Power"].append(event)
            elif "배터리" in event["title"]:
                categories["Energy"].append(event)
            else:
                categories["Other"].append(event)

        return categories

    def calculate_pressure(self, categories):
        """Pressure 계산"""
        print("\n\n⚡ Pressure Calculation")
        print("=" * 60)

        pressure = {}
        for category, events in categories.items():
            # 중요도 합산
            total_importance = sum([e["importance"] for e in events])
            count = len(events)

            pressure[category] = {
                "count": count,
                "total_importance": total_importance,
                "average_importance": total_importance / count if count > 0 else 0,
                "status": "Rising" if count > 2 else "Stable"
            }

        return pressure

    def detect_reservoirs(self, pressure):
        """Reservoir 감지 (Pressure가 높은 지점)"""
        print("\n\n💧 Reservoir Detection")
        print("=" * 60)

        reservoirs = []

        # Pressure 강도 기준으로 Reservoir 판정
        for category, p in pressure.items():
            total_importance = p["total_importance"]
            count = p["count"]
            status = p["status"]

            # Reservoir 조건: Importance > 300 AND Count > 2
            if total_importance >= 300 and count >= 2:
                reservoir = {
                    "name": category,
                    "pressure": total_importance,
                    "signals": count,
                    "importance": p["average_importance"],
                    "status": status,
                    "confidence": min(100, (total_importance / 500) * 100),  # 신뢰도 (%)
                    "description": self._describe_reservoir(category, p)
                }
                reservoirs.append(reservoir)

        # Pressure 높은 순서로 정렬
        reservoirs.sort(key=lambda x: x["pressure"], reverse=True)

        for r in reservoirs:
            print(f"✅ Reservoir: {r['name']}")
            print(f"   Pressure: {r['pressure']} | Signals: {r['signals']} | Status: {r['status']}")
            print(f"   Confidence: {r['confidence']:.1f}% | Description: {r['description']}")

        return reservoirs

    def _describe_reservoir(self, category, pressure):
        """Reservoir 설명"""
        status = pressure["status"]
        importance = pressure["total_importance"]

        if category == "AI":
            if importance > 700:
                return "AI 자본 대량 집중 → 초고강도 저수지"
            else:
                return "AI 기술 투자 증가 → 고강도 저수지"
        elif category == "Power":
            if importance > 700:
                return "전력 인프라 대규모 확충 → 초고강도 저수지"
            else:
                return "에너지 전환 신호 → 고강도 저수지"
        elif category == "Energy":
            return "배터리/에너지 저장 집중 투자 → 고강도 저수지"
        else:
            return "새로운 기술/산업 신호"

    def generate_report(self):
        """최종 보고서"""
        print("\n\n📊 Sensor Observatory Daily Report")
        print("=" * 60)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # 센서별 수집 결과
        total_signals = sum([len(v) for v in self.sensors.values()])
        print("📡 Total Signals Collected:")
        print(f"  📰 News:                  {len(self.sensors['news']):3}건")
        print(f"  📋 Corporate Disclosure: {len(self.sensors['corporate_disclosure']):3}건")
        print(f"  🏛️  Government:            {len(self.sensors['government']):3}건")
        print(f"  🔬 Patents:               {len(self.sensors['patent']):3}건")
        print(f"  👥 Recruitment:           {len(self.sensors['recruitment']):3}건")
        print(f"  🛒 Procurement:           {len(self.sensors['procurement']):3}건")
        print(f"  {'─' * 45}")
        print(f"  📊 Total:                 {total_signals:3}건")
        print()

        # Flow Event 분류
        categories = self.detect_flow_events()
        print(f"🎯 Flow Events: {len(self.flow_events)}건")
        for cat, events in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {cat:10} {len(events):2}건")
        print()

        # Pressure 계산
        pressure = self.calculate_pressure(categories)
        print("⚡ Pressure Analysis:")
        for category in sorted(pressure.keys(), key=lambda x: pressure[x]["total_importance"], reverse=True):
            p = pressure[category]
            print(f"  {category:10} | Count: {p['count']:2} | Importance: {p['total_importance']:3} | Status: {p['status']}")

        # Reservoir 감지
        reservoirs = self.detect_reservoirs(pressure)

        print(f"\n\n💎 Reservoir Summary:")
        print(f"{'─' * 60}")
        print(f"감지된 Reservoir: {len(reservoirs)}개")
        for i, r in enumerate(reservoirs, 1):
            print(f"\n{i}. {r['name']} Reservoir")
            print(f"   📊 Pressure: {r['pressure']:.0f} (강도)")
            print(f"   📡 Signals: {r['signals']}개")
            print(f"   ⭐ Confidence: {r['confidence']:.1f}%")
            print(f"   📝 Status: {r['status']}")

    def save_results(self):
        """결과 저장"""
        results = {
            "timestamp": self.timestamp,
            "sensors": {
                "total_signals": sum([len(v) for v in self.sensors.values()]),
                "by_sensor": {k: len(v) for k, v in self.sensors.items()}
            },
            "flow_events": {
                "total": len(self.flow_events),
                "events": self.flow_events
            }
        }

        output_file = Path("results/sensor_observatory_report.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 결과 저장: {output_file}")

    def run(self):
        """전체 실행"""
        print("\n" + "=" * 60)
        print("🌍 SENSOR OBSERVATORY v1.0")
        print("세상을 관측하는 센서 시스템")
        print("=" * 60)

        # 센서별 수집
        self.collect_news()
        self.collect_corporate_disclosure()
        self.collect_government()
        self.collect_patents()
        self.collect_recruitment()
        self.collect_procurement()

        # Flow Event 감지
        categories = self.detect_flow_events()

        # Pressure 계산 및 Reservoir 감지
        pressure = self.calculate_pressure(categories)
        reservoirs = self.detect_reservoirs(pressure)

        # 보고서 생성
        self.generate_report()

        # 결과 저장 (reservoirs 포함)
        self.save_results_with_reservoirs(reservoirs, pressure)

    def save_results_with_reservoirs(self, reservoirs, pressure):
        """Reservoir 정보를 포함한 결과 저장"""
        results = {
            "timestamp": self.timestamp,
            "sensors": {
                "total_signals": sum([len(v) for v in self.sensors.values()]),
                "by_sensor": {k: len(v) for k, v in self.sensors.items()}
            },
            "flow_events": {
                "total": len(self.flow_events),
                "events": self.flow_events
            },
            "pressure": {
                k: {
                    "count": v["count"],
                    "total_importance": v["total_importance"],
                    "average_importance": v["average_importance"],
                    "status": v["status"]
                }
                for k, v in pressure.items()
            },
            "reservoirs": {
                "total": len(reservoirs),
                "detected": [
                    {
                        "name": r["name"],
                        "pressure": r["pressure"],
                        "signals": r["signals"],
                        "confidence": r["confidence"],
                        "status": r["status"],
                        "description": r["description"]
                    }
                    for r in reservoirs
                ]
            }
        }

        output_file = Path("results/sensor_observatory_report.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 결과 저장: {output_file}")

if __name__ == "__main__":
    observatory = SensorObservatory()
    observatory.run()
