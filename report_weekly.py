#!/usr/bin/env python3
"""
Phase 3: 주간 리포트 + AI 분석 트리거
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

class WeeklyReporter:
    def __init__(self):
        self.today = datetime.now()
        self.stats_file = Path("~/data/daily_stats.csv").expanduser()

    def load_weekly_data(self):
        """최근 7일 데이터 로드"""
        if not self.stats_file.exists():
            print("❌ 통계 데이터 없음")
            return None

        df = pd.read_csv(self.stats_file)
        df['date'] = pd.to_datetime(df['date'])

        # 최근 7일
        week_ago = self.today - timedelta(days=7)
        recent = df[df['date'] >= week_ago].copy()

        return recent

    def analyze_weekly(self, df):
        """주간 분석"""
        print("\n=" * 70)
        print("📊 주간 리포트 (최근 7일)")
        print("=" * 70)

        if df is None or len(df) == 0:
            print("\n데이터 부족 (7일 미만)")
            return None

        print(f"\n기간: {df['date'].min().date()} ~ {df['date'].max().date()}")
        print(f"샘플: {len(df)}일\n")

        analysis = {}

        for col in df.columns[1:]:
            if col == 'date':
                continue

            values = df[col].values
            avg = values.mean()
            max_val = values.max()
            min_val = values.min()
            change = ((values[-1] - values[0]) / max(values[0], 1) * 100) if len(values) > 1 else 0

            analysis[col] = {
                "avg": avg,
                "max": max_val,
                "min": min_val,
                "change": change,
                "current": values[-1]
            }

            # 출력
            trend = "⬆️" if change > 5 else ("⬇️" if change < -5 else "➡️")
            print(f"  {col:10} | avg: {avg:5.1f} | cur: {values[-1]:5.1f} | "
                  f"{change:+6.1f}% {trend}")

        return analysis

    def check_ai_trigger(self, analysis):
        """AI 분석 트리거 조건"""
        if analysis is None:
            return False, "데이터 부족"

        # 트리거 조건: Power가 50% 이상 증가
        power = analysis.get("Power", {})
        if power.get("change", 0) > 50:
            return True, "Power 50% 이상 증가"

        # 트리거 조건: 새로운 카테고리 등장
        for category, data in analysis.items():
            if data["current"] > 0 and data["avg"] == 0:
                return True, f"{category} 새로운 신호"

        return False, "현재 트리거 조건 미만"

    def run(self):
        print("\n" + "=" * 70)
        print("PHASE 3: 주간 리포트 + AI 트리거")
        print("=" * 70)

        df = self.load_weekly_data()
        if df is not None and len(df) > 0:
            analysis = self.analyze_weekly(df)

            # AI 트리거 확인
            trigger, reason = self.check_ai_trigger(analysis)

            print("\n" + "-" * 70)
            print("🤖 AI 분석 필요성:\n")
            print(f"  상태: {'🔴 필요' if trigger else '🟢 불필요'}")
            print(f"  사유: {reason}")

            if trigger:
                print("\n  💡 추천: AI 분석 실행 (비용: ~$5-10)")
                print("     python3 ask_ai_analysis.py")
            else:
                print("\n  💡 내일 같은 시간에 재확인")

            print("\n" + "-" * 70)

            # 결과 저장
            report_file = Path("results") / f"report_weekly_{self.today.strftime('%Y%m%d')}.json"
            with open(report_file, 'w') as f:
                json.dump({
                    "timestamp": self.today.isoformat(),
                    "analysis": {str(k): {str(kk): float(vv)
                                          for kk, vv in v.items()}
                                 for k, v in (analysis or {}).items()},
                    "ai_trigger": bool(trigger),
                    "reason": str(reason)
                }, f, indent=2)

            print(f"\n✓ 리포트 저장: {report_file}")

        print("\n✅ Phase 3 완료")

if __name__ == "__main__":
    reporter = WeeklyReporter()
    reporter.run()
