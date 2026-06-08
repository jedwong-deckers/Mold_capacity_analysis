"""Phase 1 Demo — 结果报告生成器（HTML + 文本摘要）"""
import pandas as pd
from pathlib import Path
from config import OUTPUT_DIR


class Phase1Reporter:
    """生成 Phase 1 Demo 的结果报告"""

    def __init__(self, season: str, round_name: str):
        self.season = season
        self.round_name = round_name

    def generate_text_report(self, unified: pd.DataFrame) -> str:
        """生成文本格式的摘要报告"""
        lines = [
            "=" * 60,
            f"  Mold Capacity Analysis — Phase 1 Demo 结果报告",
            "=" * 60,
            f"  Season:  {self.season}",
            f"  Round:   {self.round_name}",
            f"  生成时间: 2026-05-20",
            "",
            "—" * 60,
            "  核心指标",
            "—" * 60,
            f"  总模具线数:        {len(unified)}",
            f"  需加模线数:        {(unified['additional_mold_qty'] > 0).sum()}",
            f"  总加模数量:        {int(unified['additional_mold_qty'].sum())} 套",
            f"  产能充足率:        {(unified['additional_mold_qty'] == 0).mean() * 100:.1f}%",
            "",
            "—" * 60,
            "  按场景分布",
            "—" * 60,
        ]

        scenario_stats = unified.groupby("scenario").agg(
            模具线数=("additional_mold_qty", "count"),
            需加模数=("additional_mold_qty", lambda x: (x > 0).sum()),
            总加模量=("additional_mold_qty", "sum"),
            平均加模=("additional_mold_qty", "mean"),
            最大加模=("additional_mold_qty", "max"),
        ).reset_index()

        for _, row in scenario_stats.iterrows():
            lines.append(f"\n  【{row['scenario']}】")
            lines.append(f"    模具线数: {int(row['模具线数'])}")
            lines.append(f"    需加模:   {int(row['需加模数'])} / {int(row['模具线数'])}")
            lines.append(f"    总加模:   {int(row['总加模量'])} 套")
            lines.append(f"    平均:     {row['平均加模']:.1f} 套")
            lines.append(f"    最大:     {int(row['最大加模'])} 套")

        lines.extend([
            "",
            "—" * 60,
            "  Top 10 加模需求（按 additional_mold_qty 降序）",
            "—" * 60,
        ])

        top10 = unified.nlargest(10, "additional_mold_qty")[[
            "brand", "component", "mold_code", "supplier", "factory",
            "scenario", "existing_mold_qty", "additional_mold_qty", "risk_level"
        ]]

        for i, (_, row) in enumerate(top10.iterrows(), 1):
            brand = str(row.get('brand', '') or '')[:5]
            mold_code = str(row.get('mold_code', '') or '')[:20]
            factory = str(row.get('factory', '') or '')[:10]
            existing = int(row.get('existing_mold_qty', 0) or 0)
            additional = int(row.get('additional_mold_qty', 0) or 0)
            risk = str(row.get('risk_level', ''))
            lines.append(
                f"  {i:2d}. {brand:5s} | {mold_code:20s} | "
                f"{factory:10s} | existing={existing} | "
                f"add={additional:3d} | {risk}"
            )

        lines.extend([
            "",
            "=" * 60,
            "  输出文件",
            "=" * 60,
            f"  统一结果 Excel: output/unified_result_{self.season}_{self.round_name}.xlsx",
            f"  HTML 报告:      output/report_{self.season}_{self.round_name}.html",
            "",
            "  下一步行动:",
            "    1. 查看 risk_list sheet，确认需加模的模具线",
            "    2. 与工厂开会，用品牌方计算结果 Verify 工厂数据",
            "    3. 决策：加模 / 拉单 / 调整 Buy Plan",
            "",
            "=" * 60,
        ])

        return "\n".join(lines)

    def generate_html_report(self, unified: pd.DataFrame) -> Path:
        """生成 HTML 格式的可视化报告"""
        output_file = OUTPUT_DIR / f"report_{self.season}_{self.round_name}.html"

        # 计算统计指标
        total_lines = len(unified)
        need_mold = (unified["additional_mold_qty"] > 0).sum()
        total_add = int(unified["additional_mold_qty"].sum())
        sufficient_rate = (unified["additional_mold_qty"] == 0).mean() * 100

        # 场景统计
        scenario_stats = unified.groupby("scenario").agg(
            lines=("additional_mold_qty", "count"),
            need=("additional_mold_qty", lambda x: (x > 0).sum()),
            total_add=("additional_mold_qty", "sum"),
        ).reset_index()

        # Top 10 风险
        top10 = unified.nlargest(10, "additional_mold_qty")[[
            "brand", "mold_code", "supplier", "factory", "scenario",
            "existing_mold_qty", "additional_mold_qty", "risk_level"
        ]]

        # 品牌分布
        brand_stats = unified.groupby("brand")["additional_mold_qty"].sum().reset_index()
        brand_bars = "\n".join([
            f'<div class="bar-row"><span class="bar-label">{r["brand"]}</span>'
            f'<div class="bar" style="width:{min(r["additional_mold_qty"]/total_add*500, 100)}%"></div>'
            f'<span class="bar-value">{int(r["additional_mold_qty"])}</span></div>'
            for _, r in brand_stats.iterrows()
        ])

        # Top 10 表格行
        top10_rows = "\n".join([
            f"<tr><td>{i}</td><td>{r['brand']}</td><td>{r['mold_code']}</td>"
            f"<td>{r['factory']}</td><td>{r['scenario']}</td>"
            f"<td>{int(r['existing_mold_qty'])}</td><td>{int(r['additional_mold_qty'])}</td>"
            f"<td>{r['risk_level']}</td></tr>"
            for i, (_, r) in enumerate(top10.iterrows(), 1)
        ])

        # 场景卡片
        scenario_cards = "\n".join([
            f'<div class="card">'
            f'<div class="card-title">{r["scenario"]}</div>'
            f'<div class="card-metric">{int(r["need"])}/{int(r["lines"])}</div>'
            f'<div class="card-label">需加模 / 总线数</div>'
            f'<div class="card-metric">{int(r["total_add"])}</div>'
            f'<div class="card-label">总加模量</div>'
            f'</div>'
            for _, r in scenario_stats.iterrows()
        ])

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Mold Capacity Analysis — Phase 1 Demo</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 40px 20px; background: #f5f5f5; }}
  .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; }}
  .header h1 {{ margin: 0 0 10px 0; font-size: 28px; }}
  .header .meta {{ opacity: 0.9; font-size: 14px; }}
  .kpi-row {{ display: flex; gap: 20px; margin-bottom: 30px; }}
  .kpi-card {{ flex: 1; background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; }}
  .kpi-value {{ font-size: 36px; font-weight: 700; color: #667eea; margin: 8px 0; }}
  .kpi-label {{ font-size: 13px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }}
  .section {{ background: white; padding: 28px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
  .section h2 {{ margin-top: 0; font-size: 18px; color: #333; border-bottom: 2px solid #667eea; padding-bottom: 12px; margin-bottom: 20px; }}
  .scenario-cards {{ display: flex; gap: 16px; flex-wrap: wrap; }}
  .card {{ flex: 1; min-width: 200px; background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border-left: 4px solid #667eea; }}
  .card-title {{ font-weight: 600; color: #333; margin-bottom: 12px; }}
  .card-metric {{ font-size: 28px; font-weight: 700; color: #667eea; }}
  .card-label {{ font-size: 12px; color: #888; margin-top: 4px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #f8f9fa; padding: 12px; text-align: left; font-weight: 600; color: #555; border-bottom: 2px solid #e0e0e0; }}
  td {{ padding: 12px; border-bottom: 1px solid #eee; }}
  tr:hover {{ background: #f8f9fa; }}
  .bar-row {{ display: flex; align-items: center; margin: 8px 0; }}
  .bar-label {{ width: 80px; font-size: 14px; font-weight: 500; }}
  .bar {{ height: 24px; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 4px; margin: 0 12px; min-width: 4px; }}
  .bar-value {{ width: 60px; text-align: right; font-size: 14px; font-weight: 600; color: #667eea; }}
  .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }}
</style>
</head>
<body>
  <div class="header">
    <h1>🔧 Mold Capacity Analysis</h1>
    <div class="meta">Phase 1 Demo | Season: {self.season} | Round: {self.round_name} | 生成时间: 2026-05-20</div>
  </div>

  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-label">总模具线数</div>
      <div class="kpi-value">{total_lines}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">需加模线数</div>
      <div class="kpi-value">{need_mold}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">总加模数量</div>
      <div class="kpi-value">{total_add}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">产能充足率</div>
      <div class="kpi-value">{sufficient_rate:.1f}%</div>
    </div>
  </div>

  <div class="section">
    <h2>📊 按场景分布</h2>
    <div class="scenario-cards">
      {scenario_cards}
    </div>
  </div>

  <div class="section">
    <h2>🏭 按品牌加模分布</h2>
    {brand_bars}
  </div>

  <div class="section">
    <h2>🔴 Top 10 加模需求（风险最高）</h2>
    <table>
      <tr><th>#</th><th>Brand</th><th>Mold Code</th><th>Factory</th><th>Scenario</th>
          <th>Existing</th><th>Additional</th><th>Risk</th></tr>
      {top10_rows}
    </table>
  </div>

  <div class="section">
    <h2>📋 输出文件</h2>
    <p>统一结果 Excel: <code>output/unified_result_{self.season}_{self.round_name}.xlsx</code></p>
    <p>包含 3 个 Sheet: <b>summary</b>（汇总）| <b>detail</b>（明细）| <b>risk_list</b>（风险清单）</p>
  </div>

  <div class="footer">
    Mold Capacity Analysis — Phase 1 Demo | 基于已有计算结果合并生成
  </div>
</body>
</html>"""

        output_file.write_text(html, encoding="utf-8")
        print(f"✅ HTML 报告已生成: {output_file}")
        return output_file

    def save_text_report(self, report_text: str) -> Path:
        """保存文本报告"""
        output_file = OUTPUT_DIR / f"report_{self.season}_{self.round_name}.txt"
        output_file.write_text(report_text, encoding="utf-8")
        print(f"✅ 文本报告已生成: {output_file}")
        return output_file
