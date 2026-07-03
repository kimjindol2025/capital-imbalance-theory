#!/usr/bin/env python3
"""
실행 로그를 JSON으로 저장하는 스크립트
웹 대시보드에서 표시하기 위함
"""

import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys

class LogSaver:
    def __init__(self):
        self.logs = {
            "timestamp": datetime.now().isoformat(),
            "phases": {}
        }

    def capture_phase(self, phase_num, phase_name, command):
        """각 Phase를 실행하고 로그 저장"""
        print(f"\n🔄 {phase_name} 실행 중...")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout
            error = result.stderr if result.returncode != 0 else None

            self.logs["phases"][f"phase_{phase_num}"] = {
                "name": phase_name,
                "status": "✅ 완료" if result.returncode == 0 else "❌ 실패",
                "command": command,
                "output": output[:1000],  # 처음 1000자만
                "error": error,
                "timestamp": datetime.now().isoformat()
            }

            print(f"✅ {phase_name} 완료")
            return result.returncode == 0

        except subprocess.TimeoutExpired:
            self.logs["phases"][f"phase_{phase_num}"] = {
                "name": phase_name,
                "status": "⏱️ 타임아웃",
                "error": "30초 초과"
            }
            print(f"⏱️ {phase_name} 타임아웃")
            return False

    def run_all_phases(self):
        """모든 Phase 실행"""
        print("=" * 60)
        print("Capital Imbalance Engine - 자동화 실행")
        print("=" * 60)

        # Phase 1
        self.capture_phase(
            1,
            "Phase 1: 뉴스 수집",
            "python3 collect_today.py"
        )

        # Phase 2
        self.capture_phase(
            2,
            "Phase 2: 통계 분석",
            "python3 analyze_today.py"
        )

        # Phase 3
        self.capture_phase(
            3,
            "Phase 3: 주간 리포트",
            "python3 report_weekly.py"
        )

    def save_to_file(self):
        """로그를 파일에 저장"""
        log_file = Path("results/execution_logs.json")

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 로그 저장: {log_file}")
        return log_file

    def print_summary(self):
        """요약 출력"""
        print("\n" + "=" * 60)
        print("📊 실행 요약")
        print("=" * 60)

        for phase_key, phase_data in self.logs["phases"].items():
            print(f"\n{phase_data['name']}")
            print(f"  상태: {phase_data['status']}")
            if 'error' in phase_data and phase_data['error']:
                print(f"  오류: {phase_data['error'][:100]}")

if __name__ == "__main__":
    saver = LogSaver()
    saver.run_all_phases()
    saver.save_to_file()
    saver.print_summary()
