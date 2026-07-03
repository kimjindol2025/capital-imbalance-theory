#!/usr/bin/env python3
"""
HBM Reservoir Evolution — Phase 2: Constraint Analysis
각 Event에서 무엇이 부족한지 식별 (5가지 Constraint)
"""

import json
import pandas as pd
from datetime import datetime

class ConstraintAnalyzer:
    def __init__(self):
        self.events = []
        self.constraints_by_date = {}

        # 5가지 Constraint 타입
        self.constraint_types = {
            'supply': 'Supply Constraint - 공급 부족',
            'technology': 'Technology Constraint - 기술 병목',
            'policy': 'Policy Constraint - 규제',
            'time': 'Time Constraint - 시간 부족',
            'capacity': 'Capacity Constraint - 생산능력 부족'
        }

    def load_events(self):
        """Phase 1에서 수집한 Event 로드"""
        with open('data/hbm_events_raw.json', 'r', encoding='utf-8') as f:
            self.events = json.load(f)
        print(f"✓ {len(self.events)}개 Event 로드됨")

    def analyze_constraints(self):
        """각 Event에서 Constraint 식별"""
        print("\n📊 Constraint 분석 중...")

        for event in self.events:
            date = event['date']
            constraints = []

            # Event 타입별 Constraint 식별
            if event['event_type'] == 'price_signal':
                # GPU 가격 상승 → Supply Constraint
                if event['pressure_potential'] > 50:
                    constraints.append({
                        'type': 'supply',
                        'title': 'GPU 공급 부족',
                        'strength': min(event['pressure_potential'], 100),
                        'evidence': f"GPU 가격: {event.get('description', 'N/A')}"
                    })

            elif event['event_type'] == 'major_investment':
                # 대규모 투자 → Supply/Capacity Constraint
                constraints.append({
                    'type': 'supply',
                    'title': 'HBM 공급 부족',
                    'strength': 70,
                    'evidence': event.get('title', 'N/A')
                })
                constraints.append({
                    'type': 'capacity',
                    'title': 'HBM 생산능력 한계',
                    'strength': 65,
                    'evidence': '증설 투자 공시'
                })

            elif event['event_type'] == 'news':
                # 뉴스 분석
                title = event.get('title', '')
                if '부족' in title or '병목' in title:
                    if '메모리' in title or 'HBM' in title:
                        constraints.append({
                            'type': 'technology',
                            'title': 'HBM 메모리 병목',
                            'strength': 80,
                            'evidence': title
                        })
                    else:
                        constraints.append({
                            'type': 'supply',
                            'title': '전체 공급 부족',
                            'strength': 70,
                            'evidence': title
                        })
                if '증설' in title or '생산' in title:
                    constraints.append({
                        'type': 'capacity',
                        'title': '생산능력 확충 필요',
                        'strength': 75,
                        'evidence': title
                    })

            elif event['event_type'] == 'statistic':
                # 통계 데이터
                if 'Shipment' in event.get('metric', ''):
                    constraints.append({
                        'type': 'supply',
                        'title': 'GPU 출하량 증가 → 수요 높음',
                        'strength': int(event.get('value', 0) * 10) % 100,
                        'evidence': f"출하량: {event.get('value')} 백만개"
                    })
                if 'Demand' in event.get('metric', ''):
                    constraints.append({
                        'type': 'supply',
                        'title': 'HBM 수요 급증',
                        'strength': min(int(event.get('value', 0) * 5), 100),
                        'evidence': f"수요: {event.get('value')}"
                    })
                if 'Datacenter_Spending' in event.get('metric', ''):
                    constraints.append({
                        'type': 'capacity',
                        'title': '데이터센터 용량 확충 필요',
                        'strength': int(event.get('value', 0) / 5) % 100,
                        'evidence': f"투자: ${event.get('value')}B"
                    })

            # 날짜별 Constraint 저장
            if date not in self.constraints_by_date:
                self.constraints_by_date[date] = []

            for constraint in constraints:
                self.constraints_by_date[date].append(constraint)

        print(f"✓ 총 {sum(len(c) for c in self.constraints_by_date.values())}개 Constraint 식별됨")

    def aggregate_by_type(self):
        """Constraint를 타입별로 집계"""
        aggregated = {}

        for date, constraints in self.constraints_by_date.items():
            for constraint in constraints:
                ctype = constraint['type']
                if ctype not in aggregated:
                    aggregated[ctype] = []
                aggregated[ctype].append({
                    'date': date,
                    'strength': constraint['strength'],
                    'title': constraint['title'],
                    'evidence': constraint['evidence']
                })

        print("\n📈 Constraint 타입별 통계:")
        for ctype, items in aggregated.items():
            avg_strength = sum(item['strength'] for item in items) / len(items)
            print(f"  {self.constraint_types[ctype]}: {len(items)}개 (평균 강도: {avg_strength:.1f}/100)")

        return aggregated

    def save_constraints(self):
        """Constraint를 CSV로 저장 (Phase 3용)"""
        output_file = "data/hbm_constraints.csv"

        # 날짜별 주요 Constraint
        rows = []
        for date in sorted(self.constraints_by_date.keys()):
            constraints = self.constraints_by_date[date]
            if constraints:
                # 강도가 가장 높은 constraint
                top_constraint = max(constraints, key=lambda x: x['strength'])
                rows.append({
                    'date': date,
                    'constraint_type': top_constraint['type'],
                    'constraint_title': top_constraint['title'],
                    'strength': top_constraint['strength'],
                    'evidence': top_constraint['evidence']
                })

        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False, encoding='utf-8')

        print(f"\n✓ Constraint 데이터 저장: {output_file}")

        return df

    def visualize_timeline(self, df):
        """Constraint 타임라인 시각화"""
        print("\n📊 Constraint 타임라인 (텍스트):")
        print("\ndate            | constraint_type | strength | title")
        print("-" * 80)

        for _, row in df.head(20).iterrows():
            strength_bar = '█' * int(row['strength'] / 5)
            print(f"{row['date']} | {row['constraint_type']:<15} | {strength_bar:<20} | {row['constraint_title'][:30]}")

    def run(self):
        """전체 Constraint 분석 실행"""
        print("=" * 80)
        print("HBM Reservoir Evolution — Phase 2: Constraint Analysis")
        print("=" * 80)

        self.load_events()
        self.analyze_constraints()
        aggregated = self.aggregate_by_type()
        df = self.save_constraints()
        self.visualize_timeline(df)

        print("\n✅ Phase 2 완료")

if __name__ == "__main__":
    analyzer = ConstraintAnalyzer()
    analyzer.run()
