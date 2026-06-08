"""Phase 1 Demo — 计算引擎（结果合并器）

Phase 1 MVP 的核心价值：将分散的 New/Old/Allocation 三个场景结果，
合并为统一的输出格式。

当前实现：读取已有脚本的输出结果，统一合并。
未来可扩展：直接接入计算逻辑，无需依赖已有输出文件。
"""
import pandas as pd
from typing import Optional
from pathlib import Path
from config import OUTPUT_DIR


class Phase1Engine:
    """Phase 1 计算引擎：统一三种场景的结果输出"""

    def __init__(self, season: str, round_name: str):
        self.season = season
        self.round_name = round_name
        self.results = {}

    def load_existing_results(self, new_file: Path, old_file: Path, alloc_file: Optional[Path] = None):
        """读取已有脚本输出，统一合并（Demo 模式）

        Args:
            new_file: New mold 结果文件路径
            old_file: Old mold 结果文件路径
            alloc_file: Allocation (Share Mold) 结果文件路径（可选）
        """
        print(f"\n{'='*60}")
        print("📊 Phase 1 计算引擎 — 结果合并")
        print(f"{'='*60}")

        # 读取 New mold 结果
        df_new = self._load_summary(new_file, "New")
        self.results["New"] = df_new

        # 读取 Old mold 结果
        df_old = self._load_summary(old_file, "Old")
        self.results["Old"] = df_old

        # 读取 Allocation 结果
        if alloc_file and alloc_file.exists():
            df_alloc = self._load_summary(alloc_file, "Allocation")
            self.results["Allocation"] = df_alloc
        else:
            self.results["Allocation"] = pd.DataFrame()
            print("⚠️ Allocation 结果文件未找到，跳过")

        # 合并统一结果
        unified = self._unify_results()
        return unified

    def _load_summary(self, file_path: Path, scenario: str) -> pd.DataFrame:
        """读取单个场景的结果 summary sheet"""
        print(f"\n📁 读取 {scenario} 结果: {file_path.name}")

        try:
            df = pd.read_excel(file_path, sheet_name="additional_mold_summary")
            df["scenario"] = scenario
            df["season"] = self.season
            df["round"] = self.round_name

            # 标准化列名
            col_mapping = {
                "mold_code_short": "mold_code",
                "new_old": "mold_type_tag",
                "single_mold": "share_type",
            }
            df = df.rename(columns=col_mapping)

            # 确保核心列存在
            core_cols = [
                "brand", "component", "mold_code", "supplier", "factory",
                "share_type", "cycle_time", "existing_mold_qty", "additional_mold_qty",
                "scenario", "season", "round",
            ]
            for c in core_cols:
                if c not in df.columns:
                    df[c] = None

            total_lines = len(df)
            need_mold = (df["additional_mold_qty"] > 0).sum()
            total_add = df["additional_mold_qty"].sum()

            print(f"   模具线数: {total_lines}")
            print(f"   需加模: {need_mold} 条")
            print(f"   总加模数量: {int(total_add)} 套")

            return df

        except Exception as e:
            print(f"   ❌ 读取失败: {e}")
            return pd.DataFrame()

    def _unify_results(self) -> pd.DataFrame:
        """将三种场景合并为统一的 DataFrame"""
        dfs = [df for df in self.results.values() if not df.empty]

        if not dfs:
            raise ValueError("没有可用的计算结果")

        unified = pd.concat(dfs, ignore_index=True)

        # 统一列顺序
        output_cols = [
            "season", "round", "scenario", "brand", "component",
            "mold_code", "supplier", "factory", "share_type",
            "cycle_time", "existing_mold_qty", "additional_mold_qty",
        ]
        # 只保留存在的列
        output_cols = [c for c in output_cols if c in unified.columns]
        # 追加其他列
        other_cols = [c for c in unified.columns if c not in output_cols]
        unified = unified[output_cols + other_cols]

        # 添加风险标记
        unified["risk_level"] = "🟢 正常"
        unified.loc[unified["additional_mold_qty"] > 0, "risk_level"] = "🟡 需加模"
        unified.loc[unified["additional_mold_qty"] > 50, "risk_level"] = "🔴 严重缺口"

        print(f"\n{'='*60}")
        print("📊 统一结果汇总")
        print(f"{'='*60}")
        print(f"总模具线数: {len(unified)}")
        print(f"需加模线数: {(unified['additional_mold_qty'] > 0).sum()}")
        print(f"总加模数量: {int(unified['additional_mold_qty'].sum())} 套")
        print(f"\n按场景分布:")
        print(unified.groupby("scenario")["additional_mold_qty"].agg(["count", "sum"]).rename(
            columns={"count": "模具线数", "sum": "加模数量"}
        ))
        print(f"\n按品牌分布:")
        print(unified.groupby("brand")["additional_mold_qty"].agg(["count", "sum"]).rename(
            columns={"count": "模具线数", "sum": "加模数量"}
        ))

        return unified

    def export_unified_result(self, unified: pd.DataFrame) -> Path:
        """导出统一结果到 Excel"""
        output_file = OUTPUT_DIR / f"unified_result_{self.season}_{self.round_name}.xlsx"

        with pd.ExcelWriter(output_file) as writer:
            # Sheet 1: 汇总
            summary = unified.groupby([
                "brand", "component", "mold_code", "supplier", "factory", "scenario"
            ])[["existing_mold_qty", "additional_mold_qty"]].sum().reset_index()
            summary.to_excel(writer, sheet_name="summary", index=False)

            # Sheet 2: 明细
            unified.to_excel(writer, sheet_name="detail", index=False)

            # Sheet 3: 风险清单（需加模的）
            risk = unified[unified["additional_mold_qty"] > 0].copy()
            risk = risk.sort_values("additional_mold_qty", ascending=False)
            risk.to_excel(writer, sheet_name="risk_list", index=False)

        print(f"\n✅ 统一结果已导出: {output_file}")
        return output_file
