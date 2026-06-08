#!/usr/bin/env python3
"""Mold Capacity Analysis — Phase 1 MVP Demo

模拟 Phase 1 完整流程：
  Step 1: 配置 Season + Round
  Step 2: 上传数据 → 硬校验（阻断非标准数据）
  Step 3: 计算引擎运行（三种场景）
  Step 4: 统一结果输出（替代分散的 New/Old/Allocation 三个文件）
  Step 5: 生成报告（文本 + HTML）

使用方式:
  cd demo
  python3 phase1_demo.py --season S27 --round Round1

依赖:
  - pandas, openpyxl（读取 Excel）
  - 已有计算结果文件（output data/ 目录下）
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

from config import (
    MOLD_MASTER_FILE, FORECAST_FILE, OUTPUT_DIR,
    BASE_DATA_DIR,
)
from validator import MoldDataValidator, ValidationError
from engine import Phase1Engine
from reporter import Phase1Reporter


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🔧 Mold Capacity Analysis — Phase 1 MVP Demo            ║
║                                                              ║
║     目标: 输入标准化 → 自动计算 → 统一输出                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def run_phase1(season: str, round_name: str, mold_file: Path, forecast_file: Path):
    """执行 Phase 1 完整流程"""

    print_banner()

    # ═══════════════════════════════════════════════════════════
    # Step 1: 配置确认
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("Step 1: 基础配置")
    print(f"{'='*60}")
    print(f"Season:      {season}")
    print(f"Round:       {round_name}")
    print(f"Mold Data:   {mold_file}")
    print(f"Forecast:    {forecast_file}")

    # ═══════════════════════════════════════════════════════════
    # Step 2: 读取数据
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("Step 2: 数据读取")
    print(f"{'='*60}")

    try:
        df_mold = pd.read_excel(mold_file, sheet_name="data_sample")
        print(f"✅ Mold Master Data: {len(df_mold)} 行 × {len(df_mold.columns)} 列")
    except Exception as e:
        print(f"❌ 读取 Mold Master Data 失败: {e}")
        sys.exit(1)

    try:
        df_forecast = pd.read_excel(forecast_file, sheet_name="S27 FC", nrows=1000)
        print(f"✅ Forecast: {len(df_forecast)} 行 × {len(df_forecast.columns)} 列 (预览前1000行)")
    except Exception as e:
        print(f"⚠️ 读取 Forecast 失败: {e}，校验将跳过 Season 一致性检查")
        df_forecast = None

    # ═══════════════════════════════════════════════════════════
    # Step 3: 硬校验（模拟 Defan 上传校验）
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("Step 3: 数据硬校验（模拟 Defan）")
    print(f"{'='*60}")

    validator = MoldDataValidator(season=season, round_name=round_name)

    try:
        validation_result = validator.validate(df_mold, df_forecast)
        print(validator.get_success_report(validation_result))
    except ValidationError:
        print(validator.get_error_report())
        print("\n⛔ 校验失败，已阻断。请修正数据后重新运行。")
        sys.exit(1)

    # ═══════════════════════════════════════════════════════════
    # Step 4: 计算引擎（结果合并）
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("Step 4: 计算引擎 — 合并三种场景结果")
    print(f"{'='*60}")

    engine = Phase1Engine(season=season, round_name=round_name)

    # 定位已有计算结果文件
    result_dir = Path(__file__).resolve().parent.parent / "output data"
    new_file = result_dir / "additional_mold_by_xf_date(New)_buy_month.xlsx"
    old_file = result_dir / "additional_mold_by_xf_date(Old)_buy_month.xlsx"
    alloc_file = result_dir / "additional_mold_by_xf_date(Bondi 10)_buy_month.xlsx"

    if not new_file.exists() or not old_file.exists():
        print(f"❌ 计算结果文件未找到，请确认以下文件存在:")
        print(f"   - {new_file}")
        print(f"   - {old_file}")
        sys.exit(1)

    unified = engine.load_existing_results(
        new_file=new_file,
        old_file=old_file,
        alloc_file=alloc_file if alloc_file.exists() else None,
    )

    # 导出统一结果
    engine.export_unified_result(unified)

    # ═══════════════════════════════════════════════════════════
    # Step 5: 生成报告
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("Step 5: 生成结果报告")
    print(f"{'='*60}")

    reporter = Phase1Reporter(season=season, round_name=round_name)

    # 文本报告
    text_report = reporter.generate_text_report(unified)
    reporter.save_text_report(text_report)
    print("\n" + text_report)

    # HTML 报告
    html_file = reporter.generate_html_report(unified)

    # ═══════════════════════════════════════════════════════════
    # 完成
    # ═══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("✅ Phase 1 Demo 执行完成")
    print(f"{'='*60}")
    print(f"\n输出文件:")
    print(f"  📊 统一结果 Excel: {OUTPUT_DIR}/unified_result_{season}_{round_name}.xlsx")
    print(f"  📝 文本报告:      {OUTPUT_DIR}/report_{season}_{round_name}.txt")
    print(f"  🌐 HTML 报告:     {OUTPUT_DIR}/report_{season}_{round_name}.html")
    print(f"\n请打开 HTML 报告查看可视化结果。")


def main():
    parser = argparse.ArgumentParser(
        description="Mold Capacity Analysis — Phase 1 MVP Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 phase1_demo.py --season S27 --round Round1
  python3 phase1_demo.py --season S27F --round FC_202605
        """,
    )
    parser.add_argument("--season", required=True, help="Season 标识，如 S27、S27F")
    parser.add_argument("--round", required=True, help="轮次，如 Round1、FC_202605")
    parser.add_argument(
        "--mold-file",
        type=Path,
        default=MOLD_MASTER_FILE,
        help=f"Mold Master Data 文件路径 (默认: {MOLD_MASTER_FILE})",
    )
    parser.add_argument(
        "--forecast-file",
        type=Path,
        default=FORECAST_FILE,
        help=f"Forecast 文件路径 (默认: {FORECAST_FILE})",
    )

    args = parser.parse_args()

    run_phase1(
        season=args.season.upper(),
        round_name=args.round,
        mold_file=args.mold_file,
        forecast_file=args.forecast_file,
    )


if __name__ == "__main__":
    main()
