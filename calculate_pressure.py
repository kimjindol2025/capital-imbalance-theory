#!/usr/bin/env python3
"""
HBM Reservoir Evolution — Phase 3: Pressure Calculation
5가지 차원별 일일 Pressure 점수 계산
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class PressureCalculator:
    def __init__(self):
        self.events = []
        self.constraints = None
        self.pressure_timeseries = {}

        # 5가지 Pressure 차원
        self.dimensions = {
            'supply': 'Supply Pressure - 공급 부족',
            'demand': 'Demand Pressure - 수요 증가',
            'investment': 'Investment Pressure - 투자 결정',
            'policy': 'Policy Pressure - 정책 변화',
            'technology': 'Technology Pressure - 기술 병목'
        }

    def load_data(self):
        """Event와 Constraint 데이터 로드"""
        with open('data/hbm_events_raw.json', 'r', encoding='utf-8') as f:
            self.events = json.load(f)

        self.constraints = pd.read_csv('data/hbm_constraints.csv')
        print(f"✓ Event {len(self.events)}개, Constraint {len(self.constraints)}개 로드됨")

    def calculate_daily_pressure(self):
        """일일 Pressure 점수 계산"""
        print("\n📊 일일 Pressure 계산 중...")

        # 2023-01-01 ~ 2026-07-03
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2026, 7, 3)
        current_date = start_date

        # 누적 Pressure 추적
        cumulative_pressure = {dim: [] for dim in self.dimensions.keys()}
        dates = []

        while current_date <= end_date:
            date_str = current_date.strftime("%Y%m%d")
            dates.append(date_str)

            daily_pressure = {dim: 0 for dim in self.dimensions.keys()}

            # 이 날의 Event 찾기
            day_events = [e for e in self.events if e['date'] == date_str]

            # 1. Supply Pressure (공급 부족)
            # Event에서 pressure_potential 활용
            for event in day_events:
                if event['event_type'] == 'price_signal':
                    # GPU 가격 상승 = Supply 압력
                    daily_pressure['supply'] += event.get('pressure_potential', 0) * 0.8
                elif event['event_type'] == 'news' and ('부족' in event.get('title', '') or '병목' in event.get('title', '')):
                    daily_pressure['supply'] += event.get('pressure_potential', 0) * 0.6

            # 2. Demand Pressure (수요 증가)
            # AI 수요, GPU 수요 신호
            for event in day_events:
                if 'GPU' in event.get('title', '') or 'AI' in event.get('title', ''):
                    daily_pressure['demand'] += event.get('pressure_potential', 0) * 0.7
                if event['event_type'] == 'statistic' and 'Shipment' in event.get('metric', ''):
                    # GPU 출하량 = 수요 지표
                    daily_pressure['demand'] += event.get('pressure_potential', 0) * 0.5

            # 3. Investment Pressure (투자 결정)
            # 공시, 투자 뉴스
            for event in day_events:
                if event['event_type'] == 'major_investment' or '투자' in event.get('title', ''):
                    daily_pressure['investment'] += event.get('pressure_potential', 0) * 0.9
                if event['event_type'] == 'statistic' and 'Spending' in event.get('metric', ''):
                    daily_pressure['investment'] += event.get('pressure_potential', 0) * 0.7

            # 4. Policy Pressure (정책 변화)
            # 규제, 정책 관련 뉴스
            for event in day_events:
                if '규제' in event.get('title', '') or '정책' in event.get('title', ''):
                    daily_pressure['policy'] += event.get('pressure_potential', 0) * 0.8

            # 5. Technology Pressure (기술 병목)
            # 기술 관련 이슈
            for event in day_events:
                if '메모리' in event.get('title', '') or '병목' in event.get('title', ''):
                    daily_pressure['technology'] += event.get('pressure_potential', 0) * 0.9

            # 누적 (이전 값 + 현재 값의 일부)
            # Pressure는 축적되지만 시간에 따라 감소하기도 함 (decay factor)
            decay_factor = 0.95  # 매일 5% 감소

            for dim in self.dimensions.keys():
                if cumulative_pressure[dim]:
                    prev_pressure = cumulative_pressure[dim][-1] * decay_factor
                else:
                    prev_pressure = 0

                current_pressure = min(prev_pressure + daily_pressure[dim], 100)
                cumulative_pressure[dim].append(current_pressure)

            current_date += timedelta(days=1)

        # DataFrame으로 변환
        df_pressure = pd.DataFrame({
            'date': dates,
            'supply': cumulative_pressure['supply'],
            'demand': cumulative_pressure['demand'],
            'investment': cumulative_pressure['investment'],
            'policy': cumulative_pressure['policy'],
            'technology': cumulative_pressure['technology']
        })

        # Total Pressure (5가지 차원의 가중 평균)
        weights = {
            'supply': 0.35,      # Supply가 주도
            'demand': 0.25,
            'investment': 0.20,
            'policy': 0.10,
            'technology': 0.10
        }

        df_pressure['total'] = (
            df_pressure['supply'] * weights['supply'] +
            df_pressure['demand'] * weights['demand'] +
            df_pressure['investment'] * weights['investment'] +
            df_pressure['policy'] * weights['policy'] +
            df_pressure['technology'] * weights['technology']
        )

        print(f"✓ {len(df_pressure)}일간의 Pressure 계산 완료")

        return df_pressure

    def save_pressure(self, df_pressure):
        """Pressure 데이터 저장"""
        output_file = "data/hbm_pressure_daily.csv"
        df_pressure.to_csv(output_file, index=False)
        print(f"✓ Pressure 데이터 저장: {output_file}")

        return df_pressure

    def analyze_pressure(self, df_pressure):
        """Pressure 통계 분석"""
        print("\n📈 Pressure 통계:")
        print(f"  Total Pressure 평균: {df_pressure['total'].mean():.1f}/100")
        print(f"  Total Pressure 최고: {df_pressure['total'].max():.1f}/100 ({df_pressure.loc[df_pressure['total'].idxmax(), 'date']})")
        print(f"  Total Pressure 최저: {df_pressure['total'].min():.1f}/100")

        print("\n차원별 평균 Pressure:")
        for dim in self.dimensions.keys():
            avg = df_pressure[dim].mean()
            max_val = df_pressure[dim].max()
            print(f"  {self.dimensions[dim]}: 평균 {avg:.1f}, 최고 {max_val:.1f}")

        # Phase 3 키 포인트: Pressure 상승 시점
        print("\n🔍 Pressure 상승 시점:")

        # Total Pressure가 50 이상인 구간 찾기
        high_pressure = df_pressure[df_pressure['total'] >= 50]

        if len(high_pressure) > 0:
            first_high = high_pressure.iloc[0]
            last_high = high_pressure.iloc[-1]
            print(f"  처음 높은 Pressure (≥50): {first_high['date']} ({first_high['total']:.1f})")
            print(f"  마지막 높은 Pressure: {last_high['date']} ({last_high['total']:.1f})")
            print(f"  지속 기간: {len(high_pressure)}일")

        # 최고점
        peak = df_pressure[df_pressure['total'] == df_pressure['total'].max()].iloc[0]
        print(f"  최고점: {peak['date']} ({peak['total']:.1f})")

    def visualize_pressure(self, df_pressure):
        """Pressure 타임라인 시각화 (텍스트)"""
        print("\n📊 Pressure 타임라인 (분기별 샘플):")
        print("\ndate        | supply | demand | invest | policy | tech | total")
        print("-" * 75)

        # 분기별로 샘플링
        for i in range(0, len(df_pressure), len(df_pressure) // 12):  # 12개월 샘플
            row = df_pressure.iloc[i]
            print(f"{row['date']} | {row['supply']:6.1f} | {row['demand']:6.1f} | {row['investment']:6.1f} | {row['policy']:6.1f} | {row['technology']:4.1f} | {row['total']:6.1f}")

    def identify_reservoir_birth(self, df_pressure):
        """Reservoir 태어나는 시점 식별"""
        print("\n🎯 Reservoir Birth 식별:")

        # Threshold 설정
        birth_threshold = 60  # Pressure가 60 이상이 되는 시점

        high_pressure = df_pressure[df_pressure['total'] >= birth_threshold]

        if len(high_pressure) > 0:
            birth_date = high_pressure.iloc[0]['date']
            birth_pressure = high_pressure.iloc[0]['total']
            print(f"  HBM Reservoir 태어난 시점: {birth_date}")
            print(f"  당시 Pressure: {birth_pressure:.1f}/100")
            print(f"  ✓ Reservoir Birth 확정!")
        else:
            print(f"  ⚠️ Pressure ≥ {birth_threshold}인 시점 없음")

    def run(self):
        """전체 Pressure 계산 실행"""
        print("=" * 80)
        print("HBM Reservoir Evolution — Phase 3: Pressure Calculation")
        print("=" * 80)

        self.load_data()
        df_pressure = self.calculate_daily_pressure()
        df_pressure = self.save_pressure(df_pressure)
        self.analyze_pressure(df_pressure)
        self.visualize_pressure(df_pressure)
        self.identify_reservoir_birth(df_pressure)

        print("\n✅ Phase 3 완료")
        print("\n다음: Phase 4 Reservoir 확정 (Ground Truth 검증)")

if __name__ == "__main__":
    calculator = PressureCalculator()
    calculator.run()
