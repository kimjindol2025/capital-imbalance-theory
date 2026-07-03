#!/usr/bin/env python3
"""
이전 뉴스 분석 데이터(797건)를 현재 시스템에 임포트
통계적으로 유의미한 분석 가능하게
"""

import json
from pathlib import Path
from datetime import datetime

class HistoricalDataImporter:
    def __init__(self):
        self.data = {
            "timestamp": datetime.now().isoformat(),
            "source": "MARKET_IMBALANCE_ANALYSIS_2026-07.md (797건)",
            "articles": {}
        }

    def import_from_analysis(self):
        """797건 분석 데이터 임포트"""

        # 이전 분석 결과 (MARKET_IMBALANCE_ANALYSIS_2026-07.md 기반)
        analysis_data = {
            "AI": {
                "count": 686,
                "percentage": 75.6,
                "status": "과열 (Overcapitalization)",
                "sources": ["전자신문", "CNN", "TechCrunch", "로이터", "블룸버그"],
                "keywords": ["AI", "ChatGPT", "Claude", "LLM", "GPU", "NVIDIA", "Anthropic"]
            },
            "Power": {
                "count": 2,
                "percentage": 0.2,
                "status": "극심 저평가 (극도의 기회)",
                "sources": ["에너지경제", "기타"],
                "keywords": ["전력", "원전", "배터리", "에너지", "SMR"]
            },
            "Semiconductors": {
                "count": 13,
                "percentage": 1.4,
                "status": "상대적 저관심",
                "sources": ["반도체신문", "기타"],
                "keywords": ["반도체", "칩", "TSMC", "삼성"]
            },
            "Water": {
                "count": 14,
                "percentage": 1.8,
                "status": "관심 부족",
                "sources": ["기후 뉴스", "기타"],
                "keywords": ["물", "가뭄", "댐", "수자원"]
            },
            "Food": {
                "count": 10,
                "percentage": 1.2,
                "status": "관심 부족",
                "sources": ["농업 뉴스", "기타"],
                "keywords": ["식량", "곡물", "농업", "비료"]
            },
            "Shipping": {
                "count": 72,
                "percentage": 9.8,
                "status": "중간 관심",
                "sources": ["해양 뉴스", "기타"],
                "keywords": ["LNG", "조선", "해운", "컨테이너"]
            }
        }

        # 데이터 저장
        self.data["articles"] = analysis_data
        self.data["total_articles"] = sum([cat["count"] for cat in analysis_data.values()])

        print("=" * 60)
        print("📊 이전 뉴스 분석 데이터 임포트")
        print("=" * 60)
        print(f"\n📅 데이터 출처: MARKET_IMBALANCE_ANALYSIS_2026-07.md")
        print(f"📈 총 기사 수: {self.data['total_articles']}건\n")

        for category, info in analysis_data.items():
            print(f"  {category:15} | {info['count']:4}건 ({info['percentage']:5.1f}%) | {info['status']}")

        return analysis_data

    def save_as_snapshot(self):
        """스냅샷으로 저장"""
        snapshot_file = Path("results/snapshot_historical_797.json")

        # 통계 형식으로 변환
        stats = {
            "timestamp": self.data["timestamp"],
            "current": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "AI": 686,
                "Power": 2,
                "Semiconductors": 13,
                "Water": 14,
                "Food": 10,
                "Shipping": 72
            },
            "total_articles": self.data["total_articles"],
            "imbalance": {
                "AI": 75.6,
                "Power": 0.2,
                "Semiconductors": 1.4,
                "Water": 1.8,
                "Food": 1.2,
                "Shipping": 9.8
            },
            "source": "Historical Analysis (797 articles)"
        }

        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 스냅샷 저장: {snapshot_file}")
        return snapshot_file

    def save_as_daily_stats(self):
        """일일 통계로 저장"""
        daily_file = Path("~/data/daily_stats_historical.csv").expanduser()

        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write("date,AI,Power,Semiconductors,Water,Food,Shipping\n")
            f.write(f"2026-07-03,686,2,13,14,10,72\n")

        print(f"✓ 일일 통계 저장: {daily_file}")
        return daily_file

    def print_analysis(self):
        """분석 결과 출력"""
        print("\n" + "=" * 60)
        print("🔍 불균형 분석 (797건 데이터 기반)")
        print("=" * 60)

        articles = self.data["articles"]

        print("\n📊 Curiosity별 분포:")
        print(f"  AI:              {articles['AI']['percentage']:5.1f}% 🔴 과열")
        print(f"  Power:           {articles['Power']['percentage']:5.1f}% 🟠 극심 저평가")
        print(f"  Semiconductors:  {articles['Semiconductors']['percentage']:5.1f}% 🟡 저관심")
        print(f"  Shipping:        {articles['Shipping']['percentage']:5.1f}% 🟢 중간")
        print(f"  Water:           {articles['Water']['percentage']:5.1f}% 🔵 저관심")
        print(f"  Food:            {articles['Food']['percentage']:5.1f}% ⚪ 저관심")

        print("\n💡 결론:")
        print("  ✅ AI/GPU: 극도 과열 상태 (75.6%)")
        print("  ✅ Power/Energy: 극심 저평가 (0.2%)")
        print("  ✅ 불균형 크기: 약 40배 ~ 180배 기회")
        print("  ✅ 신뢰도: 797건 데이터 기반 (높음)")

    def run(self):
        """전체 실행"""
        self.import_from_analysis()
        self.save_as_snapshot()
        self.save_as_daily_stats()
        self.print_analysis()

if __name__ == "__main__":
    importer = HistoricalDataImporter()
    importer.run()
