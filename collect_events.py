#!/usr/bin/env python3
"""
HBM Reservoir Evolution — Phase 1: Event Collection
2023-01-01 ~ 2026-07-03의 모든 관련 Event 수집
"""

import json
import requests
from datetime import datetime, timedelta
import pandas as pd

class HBMEventCollector:
    def __init__(self):
        self.events = []
        self.start_date = "2023-01-01"
        self.end_date = "2026-07-03"

    def collect_dart_filings(self):
        """DART OpenAPI로 공시 수집"""
        print("[1/4] DART 공시 수집 중...")

        # 관심 회사
        companies = {
            '000660': 'SK하이닉스',  # SKM
            '005930': '삼성전자',    # Samsung
            '047050': 'Micron'      # 한국 상장사 아니므로 추후 SEC 사용
        }

        dart_key = "YOUR_DART_API_KEY"  # 환경변수에서 로드 필요

        for crp_cd, name in companies.items():
            print(f"  {name} 수집 중...")

            try:
                # DART API 호출 (공시 목록)
                url = "https://opendart.fss.or.kr/api/list.json"
                params = {
                    "auth": dart_key,
                    "crp_cd": crp_cd,
                    "start_dt": "20230101",
                    "end_dt": "20260703"
                }

                # 실제 API 호출 (데모용 더미 데이터)
                # response = requests.get(url, params=params)
                # filings = response.json()

                # 더미 데이터 (실제로는 API에서)
                dummy_filings = [
                    {
                        "corp_name": name,
                        "report_nm": "HBM 증설 계획 공시",
                        "rcept_dt": "20240115",
                        "flr_nm": "대표이사",
                        "event_type": "major_investment"
                    },
                    {
                        "corp_name": name,
                        "report_nm": "분기실적 보고",
                        "rcept_dt": "20240430",
                        "flr_nm": "대표이사",
                        "event_type": "financial_report"
                    }
                ]

                for filing in dummy_filings:
                    event = {
                        "date": filing["rcept_dt"],
                        "source": "DART",
                        "company": filing["corp_name"],
                        "event_type": filing["event_type"],
                        "title": filing["report_nm"],
                        "description": f"{filing['corp_name']} - {filing['report_nm']}",
                        "pressure_potential": self._estimate_pressure(filing["event_type"])
                    }
                    self.events.append(event)

            except Exception as e:
                print(f"  ⚠️ {name} 수집 실패: {e}")

    def collect_gpu_prices(self):
        """GPU 가격 데이터 수집"""
        print("[2/4] GPU 가격 데이터 수집 중...")

        # 더미 데이터 (실제로는 yfinance, Trading Economics 등에서)
        dates = pd.date_range('2023-01-01', '2026-07-03', freq='M')

        for date in dates:
            # 2023년 초: GPU 부족, 가격 최고
            # 2024년: GPU 공급 증가, 가격 하락
            # 2025년: GPU 가격 정상화

            if date.year == 2023 and date.month < 6:
                price_change = 2000 + (date.month * 500)  # 상승
                pressure = 40 + (date.month * 10)
            elif date.year == 2023 and date.month >= 6:
                price_change = 4000 + ((12 - date.month) * 200)  # 정점
                pressure = 80 + (date.month % 6) * 5
            elif date.year == 2024:
                price_change = 3000 - ((date.month) * 100)  # 하락
                pressure = 50 - (date.month * 3)
            else:
                price_change = 1500  # 정상화
                pressure = 20

            event = {
                "date": date.strftime("%Y%m%d"),
                "source": "GPU_Market",
                "event_type": "price_signal",
                "title": f"GPU 가격 신호 ({price_change}$ per unit)",
                "description": f"GPU 가격: {price_change}$ (Pressure: {pressure})",
                "pressure_potential": pressure
            }
            self.events.append(event)

    def collect_news(self):
        """뉴스 아카이브 수집"""
        print("[3/4] 뉴스 아카이브 수집 중...")

        # 실제로는 Google News API, 뉴스사 RSS, 웹 크롤링
        dummy_news = [
            {
                "date": "2023-01-15",
                "source": "전자신문",
                "title": "ChatGPT 열풍에 GPU 품귀 심화",
                "keywords": ["GPU", "부족", "가격상승"]
            },
            {
                "date": "2023-06-20",
                "source": "반도체신문",
                "title": "HBM, 신GPU의 메모리 병목 극복 핵심",
                "keywords": ["HBM", "메모리", "병목"]
            },
            {
                "date": "2024-01-15",
                "source": "전자신문",
                "title": "SK하이닉스, HBM 생산 능력 50% 확대",
                "keywords": ["SK하이닉스", "HBM", "증설"]
            },
            {
                "date": "2025-06-10",
                "source": "디지털데일리",
                "title": "AI 데이터센터 전력부족 새 병목으로",
                "keywords": ["전력", "데이터센터", "부하"]
            }
        ]

        for news in dummy_news:
            event = {
                "date": news["date"],
                "source": news["source"],
                "event_type": "news",
                "title": news["title"],
                "description": f"{news['source']}: {news['title']}",
                "keywords": news["keywords"],
                "pressure_potential": self._estimate_news_pressure(news["keywords"])
            }
            self.events.append(event)

    def collect_statistics(self):
        """산업 통계 수집"""
        print("[4/4] 산업 통계 수집 중...")

        # IEA, SEMI, IDC 등 통계
        dummy_stats = [
            {
                "date": "2023-Q1",
                "source": "SEMI",
                "metric": "GPU_Shipment",
                "value": 5.2,  # 백만 개
                "description": "GPU 출하량"
            },
            {
                "date": "2023-Q2",
                "source": "SEMI",
                "metric": "HBM_Demand",
                "value": 12.8,
                "description": "HBM 수요"
            },
            {
                "date": "2024-Q1",
                "source": "IDC",
                "metric": "Datacenter_Spending",
                "value": 28.5,  # 십억 달러
                "description": "데이터센터 투자"
            }
        ]

        for stat in dummy_stats:
            event = {
                "date": stat["date"],
                "source": stat["source"],
                "event_type": "statistic",
                "metric": stat["metric"],
                "value": stat["value"],
                "title": stat["description"],
                "description": f"{stat['source']}: {stat['description']} = {stat['value']}",
                "pressure_potential": stat["value"] / 10  # 정규화
            }
            self.events.append(event)

    def _estimate_pressure(self, event_type):
        """Event 타입별 Pressure 추정"""
        pressure_map = {
            "major_investment": 60,
            "financial_report": 30,
            "price_increase": 50,
            "supply_constraint": 70,
            "equipment_order": 65
        }
        return pressure_map.get(event_type, 30)

    def _estimate_news_pressure(self, keywords):
        """키워드별 뉴스 Pressure 추정"""
        pressure = 20
        keywords_high = ["부족", "병목", "증설", "투자", "확대"]
        keywords_medium = ["변화", "신호", "동향"]

        for kw in keywords:
            if kw in keywords_high:
                pressure += 30
            elif kw in keywords_medium:
                pressure += 15

        return min(pressure, 100)

    def save_events(self):
        """Event를 JSON으로 저장"""
        # 날짜 순 정렬
        self.events.sort(key=lambda x: x["date"])

        output_file = "data/hbm_events_raw.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)

        print(f"\n✓ {len(self.events)}개 Event 수집 완료")
        print(f"  저장: {output_file}")

        # 통계
        self._print_summary()

    def _print_summary(self):
        """수집 통계 출력"""
        source_count = {}
        for event in self.events:
            source = event.get("source", "Unknown")
            source_count[source] = source_count.get(source, 0) + 1

        print("\n📊 Event 소스별 통계:")
        for source, count in sorted(source_count.items(), key=lambda x: -x[1]):
            print(f"  {source}: {count}개")

    def run(self):
        """전체 수집 실행"""
        print("=" * 60)
        print("HBM Reservoir Evolution — Phase 1: Event Collection")
        print(f"기간: {self.start_date} ~ {self.end_date}")
        print("=" * 60)

        self.collect_dart_filings()
        self.collect_gpu_prices()
        self.collect_news()
        self.collect_statistics()
        self.save_events()

        print("\n✅ Phase 1 완료")

if __name__ == "__main__":
    collector = HBMEventCollector()
    collector.run()
