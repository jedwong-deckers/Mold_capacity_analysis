# Mold Capacity Analysis — Business Requirements Document (BRD) / 业务需求文档

> **Document Version / 文档版本**: v1.2  
> **Updated Date / 更新日期**: 2026-05-20  
> **Purpose / 用途**: Document the long-term product vision, multi-phase roadmap, algorithm evolution, and platformization plans for Mold Capacity Analysis. / 记录 Mold Capacity Analysis 的长期产品愿景、多阶段路线图、算法演进及平台化规划。  
> **Relationship with PRD / 与 PRD 关系**: The PRD (`Mold Capacity Analysis — PRD.md`) focuses only on the Phase 1 MVP frontend demo. This BRD covers everything beyond that scope. / PRD 仅聚焦 Phase 1 MVP 前端 Demo，本 BRD 覆盖超出该范围的所有内容。

---

## English Version

> **Version**: v1.2  
> **Date**: 2026-05-20  
> **Scope**: Long-term vision, multi-phase roadmap, algorithm evolution, and platformization

---

### 1. Product Vision

Build a brand-side independent mold capacity planning system that:

1. **Verifies factory output** with standardized data and transparent calculation logic.
2. **Identifies capacity gaps early** so CPT and GSP can decide among mold adds, pull-forward, or buy-plan adjustments.
3. **Becomes the single reference** for both brand and factory, eliminating duplicated calculations and inconsistent口径.

---

### 2. Strategic Objectives

| # | Objective | Why It Matters |
|---|-----------|----------------|
| 1 | **Intelligent bottleneck detection with decision space** | Automatically compare mold capacity vs. forecast demand and surface gap location and size, giving business a quantitative basis for decisions (add molds / pull orders / adjust buy plan). |
| 2 | **Unified mold-add logic and metrics across factories** | Different factories currently use different calculation口径; brand-side standardization removes confusion. |
| 3 | **Establish the single source of truth (long-term)** | Gradually make factory accept brand-side calculation results as the shared capacity baseline, removing the need for factories to repeat calculations. |

---

### 3. Multi-Phase Roadmap

#### Phase 0 — Proven Script (Completed)

- Python script + Excel input/output.
- Logic validated on historical seasons.

#### Phase 1 — MVP (1–2 months)

**Goal**: Standardize inputs and get business users using the tool.

| Workstream | Deliverable |
|------------|-------------|
| Defan module | New Calculation Task wizard, task list, status tracking |
| Script engine refactor | Read from/write to database tables instead of Excel files |
| Hard validation | Admission gate for manual data; block only when data is insufficient for calculation |
| Power BI reports | Overview, Factory Comparison, SKU Analysis, Trend Analysis |
| Output | Additional mold quantity, overdue details, days without additional molds |

> **Hard-validation principle**: The admission gate should enforce the **minimum information required for a deterministic calculation**, not demand perfect data. Blocking rules cover missing files, missing required columns, empty core fields, data-type errors, Season mismatch, and invalid enums. Non-blocking warnings (e.g., low old-mold match rate, multi-supplier QA) are reported in the result without stopping the user.

> **Scope note**: Phase 1 MVP frontend demo is detailed in the PRD.

#### Phase 2 — Enhanced Analysis (2–4 months)

**Goal**: Move from "what is the gap" to "what should we do".

| Feature | Description | Priority |
|---------|-------------|----------|
| **Delay impact by XF Month** | Break down delay orders and delay days by XF month instead of aggregate totals | P1 |
| **Surplus capacity dashboard** | Show `mold qty × cycle time × remaining working days − open PO` per factory/line | P1 |
| **Weighted priority scheduling** | Replace first-come-first-served (FCFS) with scoring based on urgency, order value, and customer grade | P1 |
| **Cost-optimal strategy recommendation** | Assign costs to mold-add, pull-forward, and delay; auto-recommend the cheapest strategy | P1 |
| **Factory Working Holiday** | Use actual factory working calendars instead of fixed 6-day weeks | P2 |
| **Mold Opening Leadtime** | Standard order-to-available leadtime to judge whether adding molds now is still feasible | P2 |

#### Phase 3 — Platformization (3–6 months)

**Goal**: Enterprise-grade platform with optimization, governance, and continuous planning.

| Feature | Description |
|---------|-------------|
| **Integer / Linear Programming (IP/LP)** | Global optimal solution across all orders, factories, and constraints |
| **Rolling plan + dynamic re-scheduling** | Weekly incremental updates with localized re-scheduling |
| **Approval workflow** | Mold-add recommendation → approval → execution tracking |
| **Cross-season comparison** | Historical trend analysis and capacity evolution |
| **Data lineage** | Trace every result field back to its source data and transformation step |

---

### 4. Target End-to-End Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Layer                              │
│  ┌─────────────┐    ┌─────────────────────────────────────┐ │
│  │  CPT        │    │  GSP                                │ │
│  │  Upload/View │    │  View dashboard / Adjust Buy Plan   │ │
│  └──────┬──────┘    └────────────────┬────────────────────┘ │
│         │                            │                       │
│         ▼                            ▼                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Defan【New Calculation Task】Module      │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │ Step 1      │  │ Step 2      │  │ Step 3      │   │  │
│  │  │ Config      │  │ Upload      │  │ Submit      │   │  │
│  │  │ Season+Round│  │ Hard validate│  │ Track status│   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  │                                                      │  │
│  │  Historical task list                                │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │  Validation passed → DB tables │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Script Engine                           │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐        │  │
│  │  │ Data clean │  │ Capacity  │  │ Write back│        │  │
│  │  │ Join validate│ │ Iterate   │  │ DB tables │        │  │
│  │  └───────────┘  └───────────┘  └───────────┘        │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Power BI Visualization Layer            │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │
│  │  │ Overview│ │ Factory │ │ SKU     │ │ Trend   │   │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### 5. Algorithm Evolution

#### 5.1 Phase 1 Algorithm (Baseline)

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

#### 5.2 Phase 2 Algorithm Enhancements

| Algorithm | Description | Priority |
|-----------|-------------|----------|
| **Weighted priority scheduling** | Replace FCFS with score = urgency × order value × customer grade | P1 |
| **Load leveling** | Smooth weekly load to avoid front-loose / back-tight concentration that drives unnecessary mold adds | P1 |
| **Cost-optimal strategy recommendation** | Assign unit costs to mold-add, pull-forward, and delay; recommend minimum-cost strategy | P1 |
| **Factory Working Holiday** | Replace fixed 6-day week with actual factory calendar | P2 |
| **Mold Opening Leadtime** | Standard leadtime from order to mold available; determines if adding molds now is still feasible | P2 |
| **Integer / Linear Programming** | Global optimization: decision variables include early/pull/add/outsource per order | P3 |

#### 5.3 Phase 3 Algorithm Enhancements

| Algorithm | Description |
|-----------|-------------|
| **Global IP/LP solver** | Optimize across all orders, factories, and constraints simultaneously |
| **Rolling horizon re-scheduling** | Weekly incremental updates with localized re-optimization |
| **Multi-objective optimization** | Balance cost, service level, and factory utilization |

---

### 6. Power BI Visualization Roadmap

#### 6.1 Phase 1 Reports (4 Pages)

##### Page 1: Overview

| Visual | Content |
|--------|---------|
| KPI cards | Total mold lines, lines needing additional molds, total additional mold qty, overdue order share |
| Pie chart | New / Old / Share mold-add distribution |
| Bar chart | Additional mold qty by Brand |
| Table | Top 10 mold lines by additional mold qty |
| Filters | Season, Round, Brand, Factory |

##### Page 2: Factory Comparison

| Visual | Content |
|--------|---------|
| Bar chart | Factory capacity utilization comparison |
| Heatmap | Factory × Mold Code capacity load matrix |
| Table | Factory-level additional molds, overdue orders, max overdue days |
| Drill-down | Factory → mold line → size |

##### Page 3: SKU Analysis

| Visual | Content |
|--------|---------|
| Scatter plot | X = demand, Y = capacity gap, bubble size = additional mold qty |
| Table | SKU-level mold-add need and risk level (red/yellow/green) |
| Filters | Master Style, Division, Class |

##### Page 4: Trend Analysis

| Visual | Content |
|--------|---------|
| Line chart | Capacity vs. demand by XF Month |
| Area chart | Monthly surplus capacity change |
| Table | Monthly delay order count and delay days |

#### 6.2 Phase 2 Reports

- Delay impact by XF Month (from aggregate to monthly breakdown).
- Surplus capacity dashboard.
- Strategy recommendation report (add vs. pull-forward vs. delay).

#### 6.3 Phase 3 Reports

- Rolling plan comparison.
- Cross-season trend and learning.
- Data lineage explorer.

#### 6.4 Export Roadmap

| Format | Phase | Use Case |
|--------|-------|----------|
| PDF | Phase 1 | Factory meeting report (A4 layout: cover + overview + factory comparison + risk SKUs) |
| Excel | Phase 1 | Raw result table for secondary analysis or PPT |
| PowerPoint | Phase 2 | One-click presentation generation |

---

### 7. User Journey (End-to-End Target)

#### CPT User Journey

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

### 8. Governance & Non-Functional Roadmap

#### 8.1 Permissions

| Role | Defan | Power BI |
|------|-------|----------|
| Business user (CPT/GSP) | Create tasks, view own tasks, download results | View all (or row-level by factory) |
| Admin | All tasks, configure base data, view system logs | View all |

#### 8.2 Performance Targets

| Indicator | Target | Condition |
|-----------|--------|-----------|
| File validation | < 10s | Single file < 10k rows |
| Script calculation | < 5 min | Single season full calculation |
| Power BI refresh | < 2 min | DB → visualization |
| Concurrent users | 3–5 | Phase 1 target |

#### 8.3 Maintainability

| Item | Requirement |
|------|-------------|
| Logging | Each calculation records uploader, season, round, duration, result rows, errors |
| Versioning | Same Season + Round supports multiple calculations; history retained |
| Rollback | Can reference previous round's result |
| Monitoring | Calculation failure auto-notifies data team |

#### 8.4 Data Governance (Phase 3)

| Item | Requirement |
|------|-------------|
| Data lineage | Trace each result field to source data and transformation |
| Change log | Record every manual edit to base data sources |
| Approval | Mold-add recommendations go through approval workflow before execution |

---

### 9. Open Questions & Future Exploration

| # | Topic | Notes |
|---|-------|-------|
| 1 | Factory acceptance process | How to align factory with brand-side results? |
| 2 | Real-time vs. batch | Should forecast updates trigger automatic re-calculation? |
| 3 | Cost model | Who defines unit costs for mold-add, pull-forward, delay? |
| 4 | Multi-brand expansion | Extend beyond UGG/HOKA/TEVA? |
| 5 | Integration with ERP | Pull PO actuals back for rolling plan accuracy |

---

## 中文版

> **版本**: v1.2  
> **日期**: 2026-05-20  
> **范围**: 长期愿景、多阶段路线图、算法演进、平台化

---

### 1. 产品愿景

构建一个品牌方独立的模具产能规划系统，实现：

1. 用标准化数据和透明计算逻辑 **Verify** 工厂输出。
2. 提前识别产能缺口，使 CPT 和 GSP 能够在加模、拉单或调整 Buy Plan 之间做出决策。
3. 成为品牌方和工厂共同的唯一参考，消除重复计算和口径不一致。

---

### 2. 战略目标

| # | 目标 | 重要性 |
|---|------|--------|
| 1 | **智能识别瓶颈并提供决策空间** | 自动对比模具产能与预测需求，输出缺口位置和大小，为业务提供加模/拉单/调整 buy plan 的量化依据。 |
| 2 | **统一各工厂加模逻辑和度量衡** | 不同工厂目前计算口径不一，品牌方统一口径可消除混乱。 |
| 3 | **建立唯一参考结果（长期）** | 逐步让工厂认可品牌方计算结果作为共同产能基准，无需重复计算。 |

---

### 3. 多阶段路线图

#### Phase 0 — 脚本验证（已完成）

- Python 脚本 + Excel 输入输出。
- 已在历史季节验证逻辑。

#### Phase 1 — MVP（1–2 个月）

**目标**: 标准化输入并让业务先用起来。

| 工作流 | 产出 |
|--------|------|
| Defan 模块 | 新建计算任务向导、任务列表、状态追踪 |
| 脚本引擎重构 | 从数据库表读写，替代 Excel |
| 硬校验 | 手工数据准入门槛；仅当数据不足以支撑计算时才阻断 |
| Power BI 报告 | 总览、工厂对比、SKU 分析、趋势分析 |
| 输出 | 加模数量、超期明细、不加模超期天数 |

> **硬校验原则**: 准入门槛应强制要求**产生确定性计算所需的最小信息**，而非追求完美数据。阻断规则包括文件缺失、必填列缺失、核心字段为空、数据类型错误、Season 不一致、枚举值无效等；非阻断警告（如旧模匹配率低、multi-supplier QA）在结果中报告，但不阻止用户继续。

> **范围说明**: Phase 1 MVP 前端 Demo 详见 PRD。

#### Phase 2 — 增强分析（2–4 个月）

**目标**: 从"缺口是什么"进化到"我们应该做什么"。

| 功能 | 说明 | 优先级 |
|------|------|--------|
| **Delay 按 XF Month 拆解** | 将延迟订单和延迟天数按 XF Month 拆分，替代汇总值 | P1 |
| **盈余产能看板** | 按工厂/模具线展示 `模具数量 × 周期时间 × 剩余工作日 − Open PO` | P1 |
| **加权优先级排程** | 用基于交期紧迫度、订单价值、客户等级的评分替代 FCFS | P1 |
| **成本最优策略推荐** | 给加模、拉单、延迟赋予成本，自动推荐最便宜的策略 | P1 |
| **Factory Working Holiday** | 用实际工厂工作日历替代固定每周 6 天 | P2 |
| **Mold Opening Leadtime** | 标准下单到可用提前期，判断现在加模是否来得及 | P2 |

#### Phase 3 — 平台化（3–6 个月）

**目标**: 企业级平台，具备优化、治理和滚动计划能力。

| 功能 | 说明 |
|------|------|
| **整数/线性规划（IP/LP）** | 跨所有订单、工厂和约束的全局最优解 |
| **滚动计划 + 动态重排** | 每周增量更新并局部重排 |
| **审批流** | 加模建议 → 审批 → 执行跟踪 |
| **跨季对比** | 历史趋势分析和产能演进 |
| **数据血缘** | 追溯每个结果字段到源数据和转换步骤 |

---

### 4. 目标端到端架构

```
┌─────────────────────────────────────────────────────────────┐
│                       用户层                                 │
│  ┌─────────────┐    ┌─────────────────────────────────────┐ │
│  │  CPT        │    │  GSP                                │ │
│  │  上传/查看   │    │  查看看板 / 调整 Buy Plan            │ │
│  └──────┬──────┘    └────────────────┬────────────────────┘ │
│         │                            │                       │
│         ▼                            ▼                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Defan【新建计算任务】模块                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │  第一步     │  │  第二步     │  │  第三步     │   │  │
│  │  │ 配置 Season │  │ 上传文件    │  │ 提交计算    │   │  │
│  │  │ + Round     │  │ 硬校验      │  │ 状态追踪    │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  │                                                      │  │
│  │  历史任务列表                                         │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │  校验通过 → 写入数据库表        │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              脚本计算引擎                             │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐        │  │
│  │  │ 数据清洗   │  │ 产能计算   │  │ 结果回写   │        │  │
│  │  │ 关联校验   │  │ 逐套迭代   │  │ 数据库表   │        │  │
│  │  └───────────┘  └───────────┘  └───────────┘        │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Power BI 展示层                          │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │
│  │  │ 总览页   │ │ 工厂对比  │ │ SKU维度 │ │ 趋势分析  │   │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### 5. 算法演进

#### 5.1 Phase 1 算法（基线）

**核心逻辑**: 连续生产排产 + 逐套迭代加模。

```
1. 订单排序: 按 mfg_start_date → real_xf_date → buy_month 升序
2. 模具最早可用: max(Initial Mfg Start Date, T3 Ready Date) + 7 天
3. 逐订单排产:
   actual_start = max(prev_order_end, mfg_start_date, mold_earliest)
   working_days = qty × 7 / total_mold / cycle_time / 6
   actual_end   = actual_start + working_days
4. 超期判断: actual_end > real_xf_date + 1 天
5. 加模迭代: 从 existing 开始，每次 +1，直到无超期或达到 200 套上限
```

**三种并行场景**：

| 场景 | 现有模具数来源 | 关键差异 |
|------|----------------|----------|
| 单模-新模 | 固定规则（默认 1，特定尺码 2） | 不关联 Assets |
| 单模-旧模 | 从 Assets Master List 匹配 | 约 80% 匹配率，未匹配默认 1 |
| 共用模-分配 | 固定规则 + Allocation 表 | Forecast 按 style_color 聚合 |

#### 5.2 Phase 2 算法增强

| 算法 | 说明 | 优先级 |
|------|------|--------|
| **加权优先级排程** | 用 交期紧迫度 × 订单价值 × 客户等级 评分替代 FCFS | P1 |
| **负荷均衡** | 平滑每周负荷，避免"前松后紧"导致集中加模 | P1 |
| **成本最优策略推荐** | 给加模、拉单、延迟赋予单位成本，推荐最低成本策略 | P1 |
| **Factory Working Holiday** | 用实际工厂日历替代固定每周 6 天 | P2 |
| **Mold Opening Leadtime** | 标准下单到模具可用提前期，判断现在加模是否来得及 | P2 |
| **整数/线性规划** | 全局优化：决策变量包括每个订单是否提前/拉单/加模/外发 | P3 |

#### 5.3 Phase 3 算法增强

| 算法 | 说明 |
|------|------|
| **全局 IP/LP 求解器** | 同时优化所有订单、工厂和约束 |
| **滚动期重排** | 每周增量更新并局部重优化 |
| **多目标优化** | 平衡成本、服务水平和工厂利用率 |

---

### 6. Power BI 可视化路线图

#### 6.1 Phase 1 报告（4 页）

##### 总览页

| 可视化元素 | 内容 |
|-----------|------|
| KPI 卡片 | 模具线总数、需加模线数、总加模数量、超期订单占比 |
| 饼图 | New / Old / Share 加模分布 |
| 柱状图 | 按 Brand 的加模数量 |
| 表格 | 加模数量最多的 Top 10 模具线 |
| 筛选器 | Season、Round、Brand、工厂 |

##### 工厂对比页

| 可视化元素 | 内容 |
|-----------|------|
| 柱状图 | 各工厂产能利用率对比 |
| 热力图 | 工厂 × Mold Code 产能负荷矩阵 |
| 表格 | 各工厂加模数量、超期订单数、最大超期天数 |
| 下钻 | 工厂 → 模具线 → 尺码 |

##### SKU 分析页

| 可视化元素 | 内容 |
|-----------|------|
| 散点图 | X轴=需求量，Y轴=产能缺口，气泡大小=加模数量 |
| 表格 | SKU 级别的加模需求、风险等级（红/黄/绿） |
| 筛选器 | Master Style、Division、Class |

##### 趋势分析页

| 可视化元素 | 内容 |
|-----------|------|
| 折线图 | 按 XF Month 的产能 vs 需求趋势 |
| 面积图 | 每月盈余产能变化 |
| 表格 | 按月份的 delay 订单量、超期天数 |

#### 6.2 Phase 2 报告

- Delay 按 XF Month 拆解（从汇总到按月拆分）。
- 盈余产能看板。
- 策略推荐报告（加模 vs. 拉单 vs. 延迟）。

#### 6.3 Phase 3 报告

- 滚动计划对比。
- 跨季趋势与学习。
- 数据血缘浏览器。

#### 6.4 导出路线图

| 格式 | 阶段 | 用途 |
|------|------|------|
| PDF | Phase 1 | 工厂会议报告（A4 排版：封面+总览+工厂对比+风险 SKU） |
| Excel | Phase 1 | 原始结果表，便于二次分析或贴进 PPT |
| PowerPoint | Phase 2 | 一键生成汇报页 |

---

### 7. 用户旅程（端到端目标态）

#### CPT 用户旅程

```
第一步：准备数据
  ├── 从 Mold Analysis Summary 提取 Mold Master Data（16 列）
  ├── 从 Global Planning 获取 Forecast
  └── 确认基础数据源已就绪（Assets / LineSheet / Leadtime / Supplier Country）

第二步：新建计算任务（Defan）
  ├── 选择 Season + Round
  ├── 上传文件（触发硬校验）
  └── 提交计算

第三步：等待计算
  ├── 校验通过 → 状态"计算中"
  ├── 校验失败 → 显示具体错误，业务自助修正后重新上传
  └── 计算完成 → 通知（企微/邮件/Defan 消息中心）

第四步：查看结果
  ├── Defan 结果卡片：核心指标 + 风险摘要
  ├── 点击"查看 Power BI" → 自动过滤到 Season + Round
  └── Power BI 下钻：总览 → 工厂 → SKU → 单模具

第五步：导出用于会议
  ├── 从 Power BI 导出 PDF 会议报告
  └── 或下载 Excel 摘要

第六步：与工厂开会
  ├── 用品牌方独立计算结果 Verify 工厂数据
  ├── 识别差异，讨论加模/拉单/分配调整
  └── 更新下一轮 Forecast 并重新计算
```

---

### 8. 治理与非功能路线图

#### 8.1 权限

| 角色 | Defan | Power BI |
|------|-------|----------|
| 业务用户（CPT/GSP） | 创建任务、查看自己的任务、下载结果 | 查看全部（或按工厂行级隔离） |
| 管理员 | 全部任务、配置基础数据、查看系统日志 | 查看全部 |

#### 8.2 性能目标

| 指标 | 目标 | 条件 |
|------|------|------|
| 文件校验 | < 10s | 单文件 < 1 万行 |
| 脚本计算 | < 5 min | 单季全量计算 |
| Power BI 刷新 | < 2 min | 数据库到可视化 |
| 并发用户 | 3–5 | Phase 1 目标 |

#### 8.3 可维护性

| 项 | 要求 |
|----|------|
| 日志 | 每次计算记录上传人、Season、Round、耗时、结果行数、错误 |
| 版本 | 同一 Season + Round 支持多次计算并保留历史 |
| 回滚 | 可回溯到上一轮计算结果 |
| 监控 | 计算失败自动通知数据团队 |

#### 8.4 数据治理（Phase 3）

| 项 | 要求 |
|----|------|
| 数据血缘 | 追溯每个结果字段到源数据和转换 |
| 变更日志 | 记录每次对基础数据源的手工修改 |
| 审批 | 加模建议执行前需经过审批流 |

---

### 9. 待确认与未来探索

| # | 事项 | 说明 |
|---|------|------|
| 1 | 工厂接受流程 | 如何让工厂与品牌方结果达成一致？ |
| 2 | 实时 vs. 批量 | Forecast 更新是否触发自动重算？ |
| 3 | 成本模型 | 加模、拉单、延迟的单位成本由谁定义？ |
| 4 | 多品牌扩展 | 是否扩展到 UGG/HOKA/TEVA 之外？ |
| 5 | 与 ERP 集成 | 回传 PO 实际数据以提高滚动计划准确性 |

---

*Document Version / 文档版本: v1.2*  
*Based on / 基于: product discussions, CLI sessions, and Kimi web sessions on "模具产能分析产品化" / 产品讨论、CLI 会话及 Kimi 网页版"模具产能分析产品化"会话*
