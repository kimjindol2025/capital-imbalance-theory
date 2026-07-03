#!/usr/bin/env python3
"""
Capital Imbalance Engine - Web Dashboard
실시간 불균형 감지 및 시각화
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

app = FastAPI()

# 데이터 경로
DATA_DIR = Path("data")
RESULTS_DIR = Path("results")

@app.get("/api/stats")
async def get_stats():
    """현재 통계"""
    stats_file = DATA_DIR / "daily_stats.csv"

    if stats_file.exists():
        df = pd.read_csv(stats_file)
        latest = df.iloc[-1].to_dict()

        # 계산: 불균형 비율
        total = sum([v for k, v in latest.items() if k != 'date'])

        return {
            "timestamp": datetime.now().isoformat(),
            "current": latest,
            "total_articles": total,
            "imbalance": {
                "AI": (latest.get("AI", 0) / total * 100) if total > 0 else 0,
                "Power": (latest.get("Power", 0) / total * 100) if total > 0 else 0,
                "Water": (latest.get("Water", 0) / total * 100) if total > 0 else 0,
                "Shipping": (latest.get("Shipping", 0) / total * 100) if total > 0 else 0,
                "Food": (latest.get("Food", 0) / total * 100) if total > 0 else 0
            }
        }

    return {"error": "No data"}

@app.get("/api/snapshot")
async def get_snapshot():
    """최신 스냅샷"""
    snapshots = list(RESULTS_DIR.glob("snapshot_*.json"))
    if snapshots:
        latest = sorted(snapshots)[-1]
        with open(latest) as f:
            return json.load(f)
    return {"error": "No snapshot"}

@app.get("/api/report")
async def get_report():
    """최신 주간 리포트"""
    reports = list(RESULTS_DIR.glob("report_weekly_*.json"))
    if reports:
        latest = sorted(reports)[-1]
        with open(latest) as f:
            return json.load(f)
    return {"error": "No report"}

@app.get("/")
async def serve_dashboard():
    """메인 대시보드"""
    html_file = Path("dashboard.html")
    if html_file.exists():
        return FileResponse(html_file)
    return {"error": "Dashboard not found"}

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("Capital Imbalance Engine - Web Dashboard")
    print("=" * 60)
    print("\n🌐 웹 서버 시작: http://localhost:5555")
    print("📊 대시보드: http://localhost:5555")
    print("🔌 API: http://localhost:5555/api/stats")
    print("\n⚠️ 중단: Ctrl+C\n")

    uvicorn.run(app, host="0.0.0.0", port=5555)
