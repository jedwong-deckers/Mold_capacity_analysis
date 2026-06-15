# Mold Capacity Analysis — Business Requirements Document (BRD)

> **Document Version**: v1.0  
> **Updated Date**: 2026-05-20  
> **Purpose**: Document the long-term product vision, multi-phase roadmap, algorithm evolution, and platformization plans for Mold Capacity Analysis.  
> **Relationship with PRD**: The PRD (`Mold Capacity Analysis — PRD.md`) focuses only on the Phase 1 MVP frontend demo. This BRD covers everything beyond that scope.

---

## 1. Product Vision

Build a brand-side independent mold capacity planning system that:

1. **Verifies factory output** with standardized data and transparent calculation logic.
2. **Identifies capacity gaps early** so CPT and GSP can decide among mold adds, pull-forward, or buy-plan adjustments.
3. **Becomes the single reference** for both brand and factory, eliminating duplicated calculations and inconsistent口径.

---

## 2. Strategic Objectives

| # | Objective | Why It Matters |
|---|-----------|----------------|
| 1 | **Intelligent bottleneck detection with decision space** | Automatically compare mold capacity vs. forecast demand and surface gap location and size, giving business a quantitative basis for decisions (add molds / pull orders / adjust buy plan). |
| 2 | **Unified mold-add logic and metrics across factories** | Different factories currently use different calculation口径; brand-side standardization removes confusion. |
| 3 | **Establish the single source of truth (long-term)** | Gradually make factory accept brand-side calculation results as the shared capacity baseline, removing the need for factories to repeat calculations. |

---

## 3. Multi-Phase Roadmap

### Phase 0 — Proven Script (Completed)

- Python script + Excel input/output.
- Logic validated on historical seasons.

### Phase 1 — MVP (1–2 months)

**Goal**: Standardize inputs and get business users using the tool.

| Workstream | Deliverable |
|------------|-------------|
| Defan module | New Calculation Task wizard, task list, status tracking |
| Script engine refactor | Read from/write to database tables instead of Excel files |
| Hard validation | Block non-standard uploads with specific error messages |
| Power BI reports | Overview / Factory Comparison / SKU Analysis / Trend Analysis |
| Output | Additional mold quantity, overdue details, days without additional molds |

> **Scope note**: Phase 1 MVP frontend demo is detailed in the PRD.

### Phase 2 — Enhanced Analysis (2–4 months)

**Goal**: Move from "what is the gap" to "what should we do".

| Feature | Description | Priority |
|---------|-------------|----------|
| **Delay impact by XF Month** | Break down delay orders and delay days by XF month instead of aggregate totals | P1 |
| **Surplus capacity dashboard** | Show `mold qty × cycle time × remaining working days − open PO` per factory/line | P1 |
| **Weighted priority scheduling** | Replace first-come-first-served (FCFS) with scoring based on urgency, order value, and customer grade | P1 |
| **Cost-optimal strategy recommendation** | Assign costs to mold-add, pull-forward, and delay; auto-recommend the cheapest strategy | P1 |
| **Factory Working Holiday** | Use actual factory working calendars instead of fixed 6-day weeks | P2 |
| **Mold Opening Leadtime** | Standard order-to-available leadtime to judge whether adding molds now is still feasible | P2 |

### Phase 3 — Platformization (3–6 months)

**Goal**: Enterprise-grade platform with optimization, governance, and continuous planning.

| Feature | Description |
|---------|-------------|
| **Integer / Linear Programming (IP/LP)** | Global optimal solution across all orders, factories, and constraints |
| **Rolling plan + dynamic re-scheduling** | Weekly incremental updates with局部重排 |
| **Approval workflow** | Mold-add recommendation → approval → execution tracking |
| **Cross-season comparison** | Historical trend analysis and capacity evolution |
| **Data lineage** | Trace every result field back to its source data and transformation step |

---

## 4. Target End-to-End Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Layer                              │
│  ┌─────────────┐    ┌─────────────────────────────────────┐ │
│  │  CPT        │    │  GSP                                │ │
│  │  上传/查看   │    │  查看看板 / 调整 Buy Plan            │ │
│  └──────┬──────┘    └────────────────┬────────────────────┘ │
│         │                            │                       │
│         ▼                            ▼                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Defan【新建计算任务】单模块                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │ Step 1      │  │ Step 2      │  │ Step 3      │   │  │
│  │  │ 配置 Season │  │ 上传文件    │  │ 提交计算    │   │  │
│  │  │ + 轮次      │  │ 硬校验      │  │ 状态追踪    │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  │                                                      │  │
│  │  历史任务列表（同一页面下半部分）                       │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │  校验通过 → 写入数据库表        │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              脚本计算引擎（Script Engine）             │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐        │  │
│  │  │ 数据清洗   │  │ 产能计算   │  │ 结果回写   │        │  │
│  │  │ 关联校验   │  │ 逐套迭代   │  │ 数据库表   │        │  │
│  │  └───────────┘  └───────────┘  └───────────┘        │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Power BI 展示层（Visualization）         │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │
│  │  │ 总览页   │ │工厂对比  │ │ SKU维度 │ │趋势分析  │   │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Algorithm Evolution

### 5.1 Phase 1 Algorithm (Baseline)

**Core logic**: continuous production scheduling + iterative mold-add.

```
1. Order sorting: by mfg_start_date → real_xf_date → buy_month (ascending)
2. Mold earliest available: max(Initial Mfg Start Date, T3 Ready Date) + 7 days
3. Schedule order by order:
   actual_start = max(prev_order_end, mfg_start_date, mold_earliest)
   working_days = qty × 7 / total_mold / cycle_time / 6
   actual_end   = actual_start + working_days
4. Overdue check: actual_end > real_xf_date + 1 day
5. Mold-add iteration: start from existing qty, +1 per iteration, until no overdue or max 200
```

**Three scenarios handled in parallel**:

| Scenario | Existing Mold Qty Source | Key Difference |
|----------|--------------------------|----------------|
| Single Mold - New | Fixed rule (default 1, specific sizes 2) | No Assets association |
| Single Mold - Old | Matched from Assets Master List | ~80% match rate; unmatched default 1 |
| Share Mold - Allocation | Fixed rule + Allocation table | Forecast aggregated by style_color |

### 5.2 Phase 2 Algorithm Enhancements

| Algorithm | Description | Priority |
|-----------|-------------|----------|
| **Weighted priority scheduling** | Replace FCFS with score = urgency × order value × customer grade | P1 |
| **Load leveling** | Smooth weekly load to avoid front-loose / back-tight concentration that drives unnecessary mold adds | P1 |
| **Cost-optimal strategy recommendation** | Assign unit costs to mold-add, pull-forward, and delay; recommend minimum-cost strategy | P1 |
| **Factory Working Holiday** | Replace fixed 6-day week with actual factory calendar | P2 |
| **Mold Opening Leadtime** | Standard leadtime from order to mold available; determines if adding molds now is still feasible | P2 |
| **Integer / Linear Programming** | Global optimization: decision variables include early/pull/add/outsource per order | P3 |

### 5.3 Phase 3 Algorithm Enhancements

| Algorithm | Description |
|-----------|-------------|
| **Global IP/LP solver** | Optimize across all orders, factories, and constraints simultaneously |
| **Rolling horizon re-scheduling** | Weekly incremental updates with localized re-optimization |
| **Multi-objective optimization** | Balance cost, service level, and factory utilization |

---

## 6. Power BI Visualization Roadmap

### 6.1 Phase 1 Reports (4 Pages)

#### Page 1: Overview

| Visual | Content |
|--------|---------|
| KPI cards | Total mold lines, lines needing additional molds, total additional mold qty, overdue order share |
| Pie chart | New / Old / Share mold-add distribution |
| Bar chart | Additional mold qty by Brand |
| Table | Top 10 mold lines by additional mold qty |
| Filters | Season, Round, Brand, Factory |

#### Page 2: Factory Comparison

| Visual | Content |
|--------|---------|
| Bar chart | Factory capacity utilization comparison |
| Heatmap | Factory × Mold Code capacity load matrix |
| Table | Factory-level additional molds, overdue orders, max overdue days |
| Drill-down | Factory → mold line → size |

#### Page 3: SKU Analysis

| Visual | Content |
|--------|---------|
| Scatter plot | X = demand, Y = capacity gap, bubble size = additional mold qty |
| Table | SKU-level mold-add need and risk level (red/yellow/green) |
| Filters | Master Style, Division, Class |

#### Page 4: Trend Analysis

| Visual | Content |
|--------|---------|
| Line chart | Capacity vs. demand by XF Month |
| Area chart | Monthly surplus capacity change |
| Table | Monthly delay order count and delay days |

### 6.2 Phase 2 Reports

- Delay impact by XF Month (from aggregate to monthly breakdown).
- Surplus capacity dashboard.
- Strategy recommendation report (add vs. pull-forward vs. delay).

### 6.3 Phase 3 Reports

- Rolling plan comparison.
- Cross-season trend and learning.
- Data lineage explorer.

### 6.4 Export Roadmap

| Format | Phase | Use Case |
|--------|-------|----------|
| PDF | Phase 1 | Factory meeting report (A4 layout: cover + overview + factory comparison + risk SKUs) |
| Excel | Phase 1 | Raw result table for secondary analysis or PPT |
| PowerPoint | Phase 2 | One-click presentation generation |

---

## 7. User Journey (End-to-End Target)

### CPT User Journey

```
Step 1: Prepare Data
  ├── Extract Mold Master Data (16 columns) from Mold Analysis Summary
  ├── Get Forecast from Global Planning
  └── Confirm base data sources are ready (Assets / LineSheet / Leadtime / Supplier Country)

Step 2: Create Calculation Task (Defan)
  ├── Select Season + Round
  ├── Upload files (trigger hard validation)
  └── Submit calculation

Step 3: Wait for Calculation
  ├── Validation passed → status "Running"
  ├── Validation failed → show specific errors, user self-corrects and re-uploads
  └── Calculation done → notification (WeCom / email / Defan message center)

Step 4: Review Results
  ├── Defan result card: core metrics + risk summary
  ├── Click "View Power BI" → auto-filter to Season + Round
  └── Power BI drill-down: Overview → Factory → SKU → Single mold

Step 5: Export for Meeting
  ├── Export PDF meeting report from Power BI
  └── Or download Excel summary

Step 6: Factory Meeting
  ├── Use brand-side independent result to verify factory data
  ├── Identify gaps, discuss mold-add / pull-forward / allocation adjustment
  └── Update next-round Forecast and re-calculate
```

---

## 8. Governance & Non-Functional Roadmap

### 8.1 Permissions

| Role | Defan | Power BI |
|------|-------|----------|
| Business user (CPT/GSP) | Create tasks, view own tasks, download results | View all (or row-level by factory) |
| Admin | All tasks, configure base data, view system logs | View all |

### 8.2 Performance Targets

| Indicator | Target | Condition |
|-----------|--------|-----------|
| File validation | < 10s | Single file < 10k rows |
| Script calculation | < 5 min | Single season full calculation |
| Power BI refresh | < 2 min | DB → visualization |
| Concurrent users | 3–5 | Phase 1 target |

### 8.3 Maintainability

| Item | Requirement |
|------|-------------|
| Logging | Each calculation records uploader, season, round, duration, result rows, errors |
| Versioning | Same Season + Round supports multiple calculations; history retained |
| Rollback | Can reference previous round's result |
| Monitoring | Calculation failure auto-notifies data team |

### 8.4 Data Governance (Phase 3)

| Item | Requirement |
|------|-------------|
| Data lineage | Trace each result field to source data and transformation |
| Change log | Record every manual edit to base data sources |
| Approval | Mold-add recommendations go through approval workflow before execution |

---

## 9. Open Questions & Future Exploration

| # | Topic | Notes |
|---|-------|-------|
| 1 | Factory acceptance process | How to align factory with brand-side results? |
| 2 | Real-time vs. batch | Should forecast updates trigger automatic re-calculation? |
| 3 | Cost model | Who defines unit costs for mold-add, pull-forward, delay? |
| 4 | Multi-brand expansion | Extend beyond UGG/HOKA/TEVA? |
| 5 | Integration with ERP | Pull PO actuals back for rolling plan accuracy |

---

*Document Version: v1.0*  
*Based on: product discussions, CLI sessions, and Kimi web sessions on "模具产能分析产品化"*
