# Mold Capacity Analysis — Business Requirements Document (BRD) / 业务需求文档

> **Document Version / 文档版本**: v1.1  
> **Updated Date / 更新日期**: 2026-05-20  
> **Purpose / 用途**: Document the long-term product vision, multi-phase roadmap, algorithm evolution, and platformization plans for Mold Capacity Analysis. / 记录 Mold Capacity Analysis 的长期产品愿景、多阶段路线图、算法演进及平台化规划。  
> **Relationship with PRD / 与 PRD 关系**: The PRD (`Mold Capacity Analysis — PRD.md`) focuses only on the Phase 1 MVP frontend demo. This BRD covers everything beyond that scope. / PRD 仅聚焦 Phase 1 MVP 前端 Demo，本 BRD 覆盖超出该范围的所有内容。

---

## 1. Product Vision / 产品愿景

Build a brand-side independent mold capacity planning system that:

构建一个品牌方独立的模具产能规划系统，实现：

1. **Verifies factory output** with standardized data and transparent calculation logic. / 用标准化数据和透明计算逻辑 **Verify** 工厂输出。
2. **Identifies capacity gaps early** so CPT and GSP can decide among mold adds, pull-forward, or buy-plan adjustments. / 提前识别产能缺口，使 CPT 和 GSP 能够在加模、拉单或调整 Buy Plan 之间做出决策。
3. **Becomes the single reference** for both brand and factory, eliminating duplicated calculations and inconsistent口径. / 成为品牌方和工厂共同的唯一参考，消除重复计算和口径不一致。

---

## 2. Strategic Objectives / 战略目标

| # | Objective / 目标 | Why It Matters / 重要性 |
|---|------------------|-------------------------|
| 1 | **Intelligent bottleneck detection with decision space / 智能识别瓶颈并提供决策空间** | Automatically compare mold capacity vs. forecast demand and surface gap location and size, giving business a quantitative basis for decisions (add molds / pull orders / adjust buy plan). / 自动对比模具产能与预测需求，输出缺口位置和大小，为业务提供加模/拉单/调整 buy plan 的量化依据。 |
| 2 | **Unified mold-add logic and metrics across factories / 统一各工厂加模逻辑和度量衡** | Different factories currently use different calculation口径; brand-side standardization removes confusion. / 不同工厂目前计算口径不一，品牌方统一口径可消除混乱。 |
| 3 | **Establish the single source of truth (long-term) / 建立唯一参考结果（长期）** | Gradually make factory accept brand-side calculation results as the shared capacity baseline, removing the need for factories to repeat calculations. / 逐步让工厂认可品牌方计算结果作为共同产能基准，无需重复计算。 |

---

## 3. Multi-Phase Roadmap / 多阶段路线图

### Phase 0 — Proven Script / 脚本验证（已完成）

- Python script + Excel input/output. / Python 脚本 + Excel 输入输出。
- Logic validated on historical seasons. / 已在历史季节验证逻辑。

### Phase 1 — MVP (1–2 months) / MVP（1–2 个月）

**Goal / 目标**: Standardize inputs and get business users using the tool. / 标准化输入并让业务先用起来。

| Workstream / 工作流 | Deliverable / 产出 |
|---------------------|--------------------|
| Defan module / Defan 模块 | New Calculation Task wizard, task list, status tracking / 新建计算任务向导、任务列表、状态追踪 |
| Script engine refactor / 脚本引擎重构 | Read from/write to database tables instead of Excel files / 从数据库表读写，替代 Excel |
| Hard validation / 硬校验 | Admission gate for manual data; block only when data is insufficient for calculation / 手工数据准入门槛；仅当数据不足以支撑计算时才阻断 |
| Power BI reports / Power BI 报告 | Overview / 总览、Factory Comparison / 工厂对比、SKU Analysis / SKU 分析、Trend Analysis / 趋势分析 |
| Output / 输出 | Additional mold quantity, overdue details, days without additional molds / 加模数量、超期明细、不加模超期天数 |

> **Scope note / 范围说明**: Phase 1 MVP frontend demo is detailed in the PRD. / Phase 1 MVP 前端 Demo 详见 PRD。

> **Hard-validation principle / 硬校验原则**: The admission gate should enforce the **minimum information required for a deterministic calculation**, not demand perfect data. Blocking rules cover missing files, missing required columns, empty core fields, data-type errors, Season mismatch, and invalid enums. Non-blocking warnings (e.g., low old-mold match rate, multi-supplier QA) are reported in the result without stopping the user. / 准入门槛应强制要求**产生确定性计算所需的最小信息**，而非追求完美数据。阻断规则包括文件缺失、必填列缺失、核心字段为空、数据类型错误、Season 不一致、枚举值无效等；非阻断警告（如旧模匹配率低、multi-supplier QA）在结果中报告，但不阻止用户继续。

### Phase 2 — Enhanced Analysis (2–4 months) / 增强分析（2–4 个月）

**Goal / 目标**: Move from "what is the gap" to "what should we do". / 从"缺口是什么"进化到"我们应该做什么"。

| Feature / 功能 | Description / 说明 | Priority / 优先级 |
|----------------|--------------------|-------------------|
| **Delay impact by XF Month / Delay 按 XF Month 拆解** | Break down delay orders and delay days by XF month instead of aggregate totals / 将延迟订单和延迟天数按 XF Month 拆分，替代汇总值 | P1 |
| **Surplus capacity dashboard / 盈余产能看板** | Show `mold qty × cycle time × remaining working days − open PO` per factory/line / 按工厂/模具线展示 `模具数量 × 周期时间 × 剩余工作日 − Open PO` | P1 |
| **Weighted priority scheduling / 加权优先级排程** | Replace first-come-first-served (FCFS) with scoring based on urgency, order value, and customer grade / 用基于交期紧迫度、订单价值、客户等级的评分替代 FCFS | P1 |
| **Cost-optimal strategy recommendation / 成本最优策略推荐** | Assign costs to mold-add, pull-forward, and delay; auto-recommend the cheapest strategy / 给加模、拉单、延迟赋予成本，自动推荐最便宜的策略 | P1 |
| **Factory Working Holiday / 工厂工作日历** | Use actual factory working calendars instead of fixed 6-day weeks / 用实际工厂工作日历替代固定每周 6 天 | P2 |
| **Mold Opening Leadtime / 模具开模提前期** | Standard order-to-available leadtime to judge whether adding molds now is still feasible / 标准下单到可用提前期，判断现在加模是否来得及 | P2 |

### Phase 3 — Platformization (3–6 months) / 平台化（3–6 个月）

**Goal / 目标**: Enterprise-grade platform with optimization, governance, and continuous planning. / 企业级平台，具备优化、治理和滚动计划能力。

| Feature / 功能 | Description / 说明 |
|----------------|--------------------|
| **Integer / Linear Programming (IP/LP) / 整数/线性规划** | Global optimal solution across all orders, factories, and constraints / 跨所有订单、工厂和约束的全局最优解 |
| **Rolling plan + dynamic re-scheduling / 滚动计划 + 动态重排** | Weekly incremental updates with局部重排 / 每周增量更新并局部重排 |
| **Approval workflow / 审批流** | Mold-add recommendation → approval → execution tracking / 加模建议 → 审批 → 执行跟踪 |
| **Cross-season comparison / 跨季对比** | Historical trend analysis and capacity evolution / 历史趋势分析和产能演进 |
| **Data lineage / 数据血缘** | Trace every result field back to its source data and transformation step / 追溯每个结果字段到源数据和转换步骤 |

---

## 4. Target End-to-End Architecture / 目标端到端架构

```
┌─────────────────────────────────────────────────────────────┐
│                     User Layer / 用户层                      │
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

## 5. Algorithm Evolution / 算法演进

### 5.1 Phase 1 Algorithm (Baseline) / Phase 1 算法（基线）

**Core logic / 核心逻辑**: continuous production scheduling + iterative mold-add. / 连续生产排产 + 逐套迭代加模。

```
1. Order sorting / 订单排序: by mfg_start_date → real_xf_date → buy_month (ascending)
2. Mold earliest available / 模具最早可用: max(Initial Mfg Start Date, T3 Ready Date) + 7 days
3. Schedule order by order / 逐订单排产:
   actual_start = max(prev_order_end, mfg_start_date, mold_earliest)
   working_days = qty × 7 / total_mold / cycle_time / 6
   actual_end   = actual_start + working_days
4. Overdue check / 超期判断: actual_end > real_xf_date + 1 day
5. Mold-add iteration / 加模迭代: start from existing qty, +1 per iteration, until no overdue or max 200
   从 existing 开始，每次 +1，直到无超期或达到 200 套上限
```

**Three scenarios handled in parallel / 三种并行场景**：

| Scenario / 场景 | Existing Mold Qty Source / 现有模具数来源 | Key Difference / 关键差异 |
|-----------------|-------------------------------------------|---------------------------|
| Single Mold - New / 单模-新模 | Fixed rule (default 1, specific sizes 2) / 固定规则（默认 1，特定尺码 2） | No Assets association / 不关联 Assets |
| Single Mold - Old / 单模-旧模 | Matched from Assets Master List / 从 Assets Master List 匹配 | ~80% match rate; unmatched default 1 / 约 80% 匹配率，未匹配默认 1 |
| Share Mold - Allocation / 共用模-分配 | Fixed rule + Allocation table / 固定规则 + Allocation 表 | Forecast aggregated by style_color / Forecast 按 style_color 聚合 |

### 5.2 Phase 2 Algorithm Enhancements / Phase 2 算法增强

| Algorithm / 算法 | Description / 说明 | Priority / 优先级 |
|------------------|--------------------|-------------------|
| **Weighted priority scheduling / 加权优先级排程** | Replace FCFS with score = urgency × order value × customer grade / 用 交期紧迫度 × 订单价值 × 客户等级 评分替代 FCFS | P1 |
| **Load leveling / 负荷均衡** | Smooth weekly load to avoid front-loose / back-tight concentration that drives unnecessary mold adds / 平滑每周负荷，避免"前松后紧"导致集中加模 | P1 |
| **Cost-optimal strategy recommendation / 成本最优策略推荐** | Assign unit costs to mold-add, pull-forward, and delay; recommend minimum-cost strategy / 给加模、拉单、延迟赋予单位成本，推荐最低成本策略 | P1 |
| **Factory Working Holiday / 工厂工作日历** | Replace fixed 6-day week with actual factory calendar / 用实际工厂日历替代固定每周 6 天 | P2 |
| **Mold Opening Leadtime / 模具开模提前期** | Standard leadtime from order to mold available; determines if adding molds now is still feasible / 标准下单到模具可用提前期，判断现在加模是否来得及 | P2 |
| **Integer / Linear Programming / 整数/线性规划** | Global optimization: decision variables include early/pull/add/outsource per order / 全局优化：决策变量包括每个订单是否提前/拉单/加模/外发 | P3 |

### 5.3 Phase 3 Algorithm Enhancements / Phase 3 算法增强

| Algorithm / 算法 | Description / 说明 |
|------------------|--------------------|
| **Global IP/LP solver / 全局 IP/LP 求解器** | Optimize across all orders, factories, and constraints simultaneously / 同时优化所有订单、工厂和约束 |
| **Rolling horizon re-scheduling / 滚动期重排** | Weekly incremental updates with localized re-optimization / 每周增量更新并局部重优化 |
| **Multi-objective optimization / 多目标优化** | Balance cost, service level, and factory utilization / 平衡成本、服务水平和工厂利用率 |

---

## 6. Power BI Visualization Roadmap / Power BI 可视化路线图

### 6.1 Phase 1 Reports (4 Pages) / Phase 1 报告（4 页）

#### Page 1: Overview / 总览页

| Visual / 可视化元素 | Content / 内容 |
|---------------------|----------------|
| KPI cards / KPI 卡片 | Total mold lines, lines needing additional molds, total additional mold qty, overdue order share / 模具线总数、需加模线数、总加模数量、超期订单占比 |
| Pie chart / 饼图 | New / Old / Share mold-add distribution / New / Old / Share 加模分布 |
| Bar chart / 柱状图 | Additional mold qty by Brand / 按 Brand 的加模数量 |
| Table / 表格 | Top 10 mold lines by additional mold qty / 加模数量最多的 Top 10 模具线 |
| Filters / 筛选器 | Season, Round, Brand, Factory / Season、Round、Brand、工厂 |

#### Page 2: Factory Comparison / 工厂对比页

| Visual / 可视化元素 | Content / 内容 |
|---------------------|----------------|
| Bar chart / 柱状图 | Factory capacity utilization comparison / 各工厂产能利用率对比 |
| Heatmap / 热力图 | Factory × Mold Code capacity load matrix / 工厂 × Mold Code 产能负荷矩阵 |
| Table / 表格 | Factory-level additional molds, overdue orders, max overdue days / 各工厂加模数量、超期订单数、最大超期天数 |
| Drill-down / 下钻 | Factory → mold line → size / 工厂 → 模具线 → 尺码 |

#### Page 3: SKU Analysis / SKU 分析页

| Visual / 可视化元素 | Content / 内容 |
|---------------------|----------------|
| Scatter plot / 散点图 | X = demand, Y = capacity gap, bubble size = additional mold qty / X轴=需求量，Y轴=产能缺口，气泡大小=加模数量 |
| Table / 表格 | SKU-level mold-add need and risk level (red/yellow/green) / SKU 级别的加模需求、风险等级（红/黄/绿） |
| Filters / 筛选器 | Master Style, Division, Class / Master Style、Division、Class |

#### Page 4: Trend Analysis / 趋势分析页

| Visual / 可视化元素 | Content / 内容 |
|---------------------|----------------|
| Line chart / 折线图 | Capacity vs. demand by XF Month / 按 XF Month 的产能 vs 需求趋势 |
| Area chart / 面积图 | Monthly surplus capacity change / 每月盈余产能变化 |
| Table / 表格 | Monthly delay order count and delay days / 按月份的 delay 订单量、超期天数 |

### 6.2 Phase 2 Reports / Phase 2 报告

- Delay impact by XF Month (from aggregate to monthly breakdown). / Delay 按 XF Month 拆解（从汇总到按月拆分）。
- Surplus capacity dashboard. / 盈余产能看板。
- Strategy recommendation report (add vs. pull-forward vs. delay). / 策略推荐报告（加模 vs. 拉单 vs. 延迟）。

### 6.3 Phase 3 Reports / Phase 3 报告

- Rolling plan comparison. / 滚动计划对比。
- Cross-season trend and learning. / 跨季趋势与学习。
- Data lineage explorer. / 数据血缘浏览器。

### 6.4 Export Roadmap / 导出路线图

| Format / 格式 | Phase / 阶段 | Use Case / 用途 |
|---------------|--------------|-----------------|
| PDF | Phase 1 | Factory meeting report (A4 layout: cover + overview + factory comparison + risk SKUs) / 工厂会议报告（A4 排版：封面+总览+工厂对比+风险 SKU） |
| Excel | Phase 1 | Raw result table for secondary analysis or PPT / 原始结果表，便于二次分析或贴进 PPT |
| PowerPoint | Phase 2 | One-click presentation generation / 一键生成汇报页 |

---

## 7. User Journey (End-to-End Target) / 用户旅程（端到端目标态）

### CPT User Journey / CPT 用户旅程

```
Step 1: Prepare Data / 准备数据
  ├── Extract Mold Master Data (16 columns) from Mold Analysis Summary
  │   从 Mold Analysis Summary 提取 Mold Master Data（16 列）
  ├── Get Forecast from Global Planning
  │   从 Global Planning 获取 Forecast
  └── Confirm base data sources are ready (Assets / LineSheet / Leadtime / Supplier Country)
      确认基础数据源已就绪（Assets / LineSheet / Leadtime / Supplier Country）

Step 2: Create Calculation Task (Defan) / 新建计算任务
  ├── Select Season + Round
  │   选择 Season + Round
  ├── Upload files (trigger hard validation)
  │   上传文件（触发硬校验）
  └── Submit calculation
      提交计算

Step 3: Wait for Calculation / 等待计算
  ├── Validation passed → status "Running"
  │   校验通过 → 状态"计算中"
  ├── Validation failed → show specific errors, user self-corrects and re-uploads
  │   校验失败 → 显示具体错误，业务自助修正后重新上传
  └── Calculation done → notification (WeCom / email / Defan message center)
      计算完成 → 通知（企微/邮件/Defan 消息中心）

Step 4: Review Results / 查看结果
  ├── Defan result card: core metrics + risk summary
  │   Defan 结果卡片：核心指标 + 风险摘要
  ├── Click "View Power BI" → auto-filter to Season + Round
  │   点击"查看 Power BI" → 自动过滤到 Season + Round
  └── Power BI drill-down: Overview → Factory → SKU → Single mold
      Power BI 下钻：总览 → 工厂 → SKU → 单模具

Step 5: Export for Meeting / 导出用于会议
  ├── Export PDF meeting report from Power BI
  │   从 Power BI 导出 PDF 会议报告
  └── Or download Excel summary
      或下载 Excel 摘要

Step 6: Factory Meeting / 与工厂开会
  ├── Use brand-side independent result to verify factory data
  │   用品牌方独立计算结果 Verify 工厂数据
  ├── Identify gaps, discuss mold-add / pull-forward / allocation adjustment
  │   识别差异，讨论加模/拉单/分配调整
  └── Update next-round Forecast and re-calculate
      更新下一轮 Forecast 并重新计算
```

---

## 8. Governance & Non-Functional Roadmap / 治理与非功能路线图

### 8.1 Permissions / 权限

| Role / 角色 | Defan | Power BI |
|-------------|-------|----------|
| Business user (CPT/GSP) / 业务用户 | Create tasks, view own tasks, download results / 创建任务、查看自己的任务、下载结果 | View all (or row-level by factory) / 查看全部（或按工厂行级隔离） |
| Admin / 管理员 | All tasks, configure base data, view system logs / 全部任务、配置基础数据、查看系统日志 | View all / 查看全部 |

### 8.2 Performance Targets / 性能目标

| Indicator / 指标 | Target / 目标 | Condition / 条件 |
|------------------|---------------|------------------|
| File validation / 文件校验 | < 10s | Single file < 10k rows / 单文件 < 1 万行 |
| Script calculation / 脚本计算 | < 5 min | Single season full calculation / 单季全量计算 |
| Power BI refresh / Power BI 刷新 | < 2 min | DB → visualization / 数据库到可视化 |
| Concurrent users / 并发用户 | 3–5 | Phase 1 target / Phase 1 目标 |

### 8.3 Maintainability / 可维护性

| Item / 项 | Requirement / 要求 |
|-----------|--------------------|
| Logging / 日志 | Each calculation records uploader, season, round, duration, result rows, errors / 每次计算记录上传人、Season、Round、耗时、结果行数、错误 |
| Versioning / 版本 | Same Season + Round supports multiple calculations; history retained / 同一 Season + Round 支持多次计算并保留历史 |
| Rollback / 回滚 | Can reference previous round's result / 可回溯到上一轮计算结果 |
| Monitoring / 监控 | Calculation failure auto-notifies data team / 计算失败自动通知数据团队 |

### 8.4 Data Governance (Phase 3) / 数据治理（Phase 3）

| Item / 项 | Requirement / 要求 |
|-----------|--------------------|
| Data lineage / 数据血缘 | Trace each result field to source data and transformation / 追溯每个结果字段到源数据和转换 |
| Change log / 变更日志 | Record every manual edit to base data sources / 记录每次对基础数据源的手工修改 |
| Approval / 审批 | Mold-add recommendations go through approval workflow before execution / 加模建议执行前需经过审批流 |

---

## 9. Open Questions & Future Exploration / 待确认与未来探索

| # | Topic / 事项 | Notes / 说明 |
|---|--------------|--------------|
| 1 | Factory acceptance process / 工厂接受流程 | How to align factory with brand-side results? / 如何让工厂与品牌方结果达成一致？ |
| 2 | Real-time vs. batch / 实时 vs. 批量 | Should forecast updates trigger automatic re-calculation? / Forecast 更新是否触发自动重算？ |
| 3 | Cost model / 成本模型 | Who defines unit costs for mold-add, pull-forward, delay? / 加模、拉单、延迟的单位成本由谁定义？ |
| 4 | Multi-brand expansion / 多品牌扩展 | Extend beyond UGG/HOKA/TEVA? / 是否扩展到 UGG/HOKA/TEVA 之外？ |
| 5 | Integration with ERP / 与 ERP 集成 | Pull PO actuals back for rolling plan accuracy / 回传 PO 实际数据以提高滚动计划准确性 |

---

*Document Version / 文档版本: v1.1*  
*Based on / 基于: product discussions, CLI sessions, and Kimi web sessions on "模具产能分析产品化" / 产品讨论、CLI 会话及 Kimi 网页版"模具产能分析产品化"会话*
