#!/usr/bin/env python3
"""
Phase 2: 일일 통계 분석 및 패턴 감지
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

class DailyAnalyzer:
    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.stats_file = Path("~/data/daily_stats.csv").expanduser()
        self.stats_file.parent.mkdir(exist_ok=True)

    def load_latest_snapshot(self):
        """최신 스냅샷 로드"""
        snapshot_files = list(Path("results").glob("snapshot_*.json"))
        if not snapshot_files:
            return None
        latest = sorted(snapshot_files)[-1]
        with open(latest) as f:
            return json.load(f)

    def calculate_stats(self, snapshot):
        """통계 계산"""
        stats = {"date": self.today}
        for category, articles in snapshot.get("articles", {}).items():
            stats[category] = len(articles)
        return stats

    def append_history(self, stats):
        """히스토리에 추가"""
        if self.stats_file.exists():
            df = pd.read_csv(self.stats_file)
            new_row = pd.DataFrame([stats])
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = pd.DataFrame([stats])

        df.to_csv(self.stats_file, index=False)
        print(f"✓ 통계 저장: {self.stats_file}")
        return df

    def detect_trends(self, df):
        """추이 분석"""
        if len(df) < 2:
            print("⚠️ 데이터 부족 (최소 2일 필요)")
            return

        print("\n📈 최근 추이:\n")

        for col in df.columns[1:]:
            recent = df[col].tail(7)
            if len(recent) > 1:
                change_pct = ((recent.iloc[-1] - recent.iloc[0]) / max(recent.iloc[0], 1)) * 100

                if abs(change_pct) > 0.1:
                    if change_pct > 0:
                        print(f"  ⬆️ {col:10} | +{change_pct:6.1f}% | {recent.iloc[-1]:.0f}건")
                    else:
                        print(f"  ⬇️ {col:10} | {change_pct:6.1f}% | {recent.iloc[-1]:.0f}건")
                else:
                    print(f"  ➡️ {col:10} | 안정 | {recent.iloc[-1]:.0f}건")

    def run(self):
        print("=" * 60)
        print("PHASE 2: 일일 통계 분석")
        print("=" * 60)

        snapshot = self.load_latest_snapshot()
        if not snapshot:
            print("❌ 스냅샷 없음 - collect_today.py 먼저 실행 필요")
            return

        stats = self.calculate_stats(snapshot)
        df = self.append_history(stats)
        self.detect_trends(df)

        print("\n✅ Phase 2 완료")

if __name__ == "__main__":
    analyzer = DailyAnalyzer()
    analyzer.run()
