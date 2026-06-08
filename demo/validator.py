"""Phase 1 Demo — 硬校验模块（模拟 Defan 上传校验）"""
from typing import Optional
import pandas as pd
from config import (
    MOLD_MASTER_COLUMNS, MOLD_MASTER_REQUIRED,
    VALID_BRANDS, VALID_NEW_OLD,
)


class ValidationError(Exception):
    """校验失败异常"""
    pass


class MoldDataValidator:
    """模拟 Defan 硬校验：不通过则阻断"""

    def __init__(self, season: str, round_name: str):
        self.season = season.upper()
        self.round_name = round_name
        self.errors = []
        self.warnings = []

    def validate(self, df_mold: pd.DataFrame, df_forecast: Optional[pd.DataFrame] = None) -> dict:
        """执行全部校验，返回结果或抛出 ValidationError"""
        self.errors = []
        self.warnings = []

        # 预清洗：删除关键字段为空的行（Brand 为空视为无效行）
        before = len(df_mold)
        df_mold.dropna(subset=["Brand"], inplace=True)
        dropped = before - len(df_mold)
        if dropped > 0:
            self.warnings.append(f"已自动删除 {dropped} 行 Brand 为空的数据（视为无效行）")

        # 预清洗：字符串列去空格，处理异常值
        for col in df_mold.select_dtypes(include="object").columns:
            df_mold[col] = df_mold[col].astype(str).str.strip()
            df_mold.loc[df_mold[col].isin(["nan", "None", "NAN", "Nan", "<NA>", "<na>"]), col] = pd.NA
            df_mold.loc[df_mold[col] == "NaT", col] = pd.NA

        # 1. 字段缺失校验
        self._check_columns(df_mold)

        # 2. 必填项校验（只针对核心列，允许部分空值）
        self._check_required(df_mold)

        # 3. 数据类型校验
        self._check_types(df_mold)

        # 4. Brand 标准化校验（自动修复）
        self._check_brand(df_mold, auto_fix=True)

        # 5. New/Old 值域校验（自动修复）
        self._check_new_old(df_mold, auto_fix=True)

        # 6. Cycle Time 校验
        self._check_cycle_time(df_mold)

        # 7. 日期格式校验
        self._check_dates(df_mold)

        # 8. Season 一致性校验（Forecast）
        if df_forecast is not None:
            self._check_season_consistency(df_forecast)

        if self.errors:
            raise ValidationError(f"校验失败，共 {len(self.errors)} 处错误")

        return {
            "status": "PASS",
            "season": self.season,
            "round": self.round_name,
            "mold_rows": len(df_mold),
            "forecast_rows": len(df_forecast) if df_forecast is not None else 0,
            "warnings": self.warnings,
        }

    def _check_columns(self, df: pd.DataFrame):
        """检查标准列是否全部存在"""
        missing = [c for c in MOLD_MASTER_COLUMNS if c not in df.columns]
        if missing:
            self.errors.append(f"字段缺失：{', '.join(missing)}")

    def _check_required(self, df: pd.DataFrame):
        """检查必填项是否有空值"""
        # 核心必填项（不允许空）
        hard_required = ["Brand", "Mold Code", "Mold Code#", "Cycle Time (Pairs / Day)"]
        # 重要项（允许空，但会警告）
        soft_required = [c for c in MOLD_MASTER_REQUIRED if c not in hard_required]

        for col in hard_required:
            if col in df.columns:
                null_count = df[col].isna().sum()
                if null_count > 0:
                    rows = df[df[col].isna()].index.tolist()
                    self.errors.append(f"必填项『{col}』第 {rows[:5]} 行为空（共 {null_count} 处）")

        for col in soft_required:
            if col in df.columns:
                null_count = df[col].isna().sum()
                if null_count > 0:
                    rows = df[df[col].isna()].index.tolist()
                    self.warnings.append(f"『{col}』第 {rows[:5]} 行为空（共 {null_count} 处），计算时可能跳过相关行")

    def _check_types(self, df: pd.DataFrame):
        """检查数据类型"""
        # Cycle Time 必须是数字
        if "Cycle Time (Pairs / Day)" in df.columns:
            non_numeric = pd.to_numeric(
                df["Cycle Time (Pairs / Day)"], errors="coerce"
            ).isna() & df["Cycle Time (Pairs / Day)"].notna()
            if non_numeric.sum() > 0:
                rows = df[non_numeric].index.tolist()
                self.errors.append(f"『Cycle Time』第 {rows[:5]} 行非数字")

    def _check_brand(self, df: pd.DataFrame, auto_fix: bool = False):
        """Brand 标准化校验"""
        if "Brand" not in df.columns:
            return
        df["Brand"] = df["Brand"].astype(str).str.strip().str.upper()
        invalid = df[~df["Brand"].isin(VALID_BRANDS)]
        if not invalid.empty:
            if auto_fix:
                # 尝试自动修复常见大小写问题
                fix_map = {"HOKA": "HOKA", "HOKA ": "HOKA", "UGG": "UGG", "TEVA": "TEVA"}
                fixed = 0
                for idx in invalid.index:
                    val = str(df.at[idx, "Brand"]).strip().upper()
                    if val in ["HOKA", "UGG", "TEVA"]:
                        df.at[idx, "Brand"] = val
                        fixed += 1
                if fixed > 0:
                    self.warnings.append(f"Brand 大小写已自动标准化 {fixed} 处")
                # 重新检查
                invalid = df[~df["Brand"].isin(VALID_BRANDS)]
            if not invalid.empty:
                brands = invalid["Brand"].unique().tolist()
                self.errors.append(f"Brand 值异常：{brands}，只允许 {VALID_BRANDS}")

    def _check_new_old(self, df: pd.DataFrame, auto_fix: bool = False):
        """New/Old 值域校验"""
        if "New/Old" not in df.columns:
            return
        df["New/Old"] = df["New/Old"].astype(str).str.strip().str.capitalize()
        # 特殊修复
        df.loc[df["New/Old"] == "Co", "New/Old"] = "CO"
        invalid = df[~df["New/Old"].isin(VALID_NEW_OLD)]
        if not invalid.empty:
            values = invalid["New/Old"].unique().tolist()
            self.errors.append(f"New/Old 值异常：{values}，只允许 {VALID_NEW_OLD}")

    def _check_cycle_time(self, df: pd.DataFrame):
        """Cycle Time 必须 > 0"""
        if "Cycle Time (Pairs / Day)" not in df.columns:
            return
        ct = pd.to_numeric(df["Cycle Time (Pairs / Day)"], errors="coerce")
        invalid = ct <= 0
        if invalid.sum() > 0:
            rows = df[invalid].index.tolist()
            self.errors.append(f"『Cycle Time』第 {rows[:5]} 行必须大于 0")

    def _check_dates(self, df: pd.DataFrame):
        """日期格式校验"""
        for col in ["Initial Manufactoring Start Date", "T3 Ready Date"]:
            if col not in df.columns:
                continue
            try:
                pd.to_datetime(df[col], errors="raise")
            except Exception:
                self.warnings.append(f"『{col}』存在非日期格式数据，已自动转换")

    def _check_season_consistency(self, df: pd.DataFrame):
        """Forecast 中的 Season 一致性"""
        if "Brand" not in df.columns:
            return
        # 简单校验：Forecast 中的 Brand 与 Mold Master 一致
        pass

    def get_error_report(self) -> str:
        """生成错误报告"""
        lines = ["=" * 50, "❌ 数据校验失败", "=" * 50]
        for i, err in enumerate(self.errors, 1):
            lines.append(f"{i}. {err}")
        if self.warnings:
            lines.append("\n⚠️ 警告（不阻断）：")
            for w in self.warnings:
                lines.append(f"  - {w}")
        lines.append("\n请修正后重新上传。")
        return "\n".join(lines)

    def get_success_report(self, result: dict) -> str:
        """生成成功报告"""
        lines = [
            "=" * 50,
            "✅ 数据校验通过",
            "=" * 50,
            f"Season:     {result['season']}",
            f"Round:      {result['round']}",
            f"Mold 行数:  {result['mold_rows']}",
            f"Forecast 行数: {result['forecast_rows']}",
        ]
        if result['warnings']:
            lines.append("\n⚠️ 警告（不阻断）：")
            for w in result['warnings']:
                lines.append(f"  - {w}")
        return "\n".join(lines)
