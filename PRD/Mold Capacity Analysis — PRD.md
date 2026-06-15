# Mold Capacity Analysis — Product Requirements Document (PRD) / 产品需求文档

> **Document Version / 文档版本**: v2.2  
> **Updated Date / 更新日期**: 2026-05-20  
> **Product Scope / 产品范围**: Phase 1 MVP Frontend Demo (`demo/frontend/html-v2.html`) / Phase 1 MVP 前端 Demo  
> **Positioning / 产品定位**: Brand-side independent mold capacity verification tool for CPT/GSP users to upload standardized data, trigger calculations, and review results. / 品牌方独立模具产能核算工具，供 CPT/GSP 用户上传标准化数据、触发计算并查看结果。

---

## English Version

> **Version**: v2.2  
> **Date**: 2026-05-20  
> **Scope**: Phase 1 MVP Frontend Demo (`demo/frontend/html-v2.html`)

---

### 1. Product Overview

#### 1.1 Background & Pain Points

Current mold capacity analysis relies on a manually consolidated **88-column Excel summary** pulled from 7+ data sources each season. Key pain points:

| Pain Point | Manifestation | Impact |
|------------|---------------|--------|
| Non-standard inputs | Each season's Excel structure differs, making scripts hard to reuse | Custom script rework every season |
| Opaque calculations | Business users cannot see how results are derived | No way to verify or run what-if analysis |
| Fragmented outputs | New / Old / Allocation scenarios each produce separate Excel files | Manual consolidation required |
| Delayed decisions | Capacity gaps are often discovered too late to react | Forced into passive mold adds or accepted delays |

#### 1.2 Product Goals (Phase 1)

| # | Goal | Description |
|---|------|-------------|
| 1 | **Standardize inputs** | Enforce a fixed 16-column Mold Master Data template and required companion files so the calculation engine always reads the same schema. |
| 2 | **Centralize task management** | Provide a single page where CPT users create, track, edit, and review calculation tasks by Season + Round. |
| 3 | **Surface core results quickly** | Show mold match status, delay risk, additional mold requirements, and unmatched/old-mold gaps in a unified result modal. |
| 4 | **Maintain base data sources** | Let admins preview and edit system-managed reference tables in one place. |

#### 1.3 Scope Boundary

This PRD covers **only the Phase 1 MVP frontend demo** implemented in `demo/frontend/html-v2.html`. Long-term road-map, algorithm enhancements beyond the current calculation logic, and platformization topics are documented separately in `Mold Capacity Analysis — BRD.md`.

```
In scope (this PRD):
├── Left-sidebar navigation: Tasks / Data Sources
├── Tasks page: list, create, edit, view result
├── New/Edit Task modal: 3-step wizard
├── Calculation Result modal: 4-section summary
└── Data Sources page: cards + preview / inline edit

Out of scope (see BRD):
├── Phase 2 algorithm upgrades
├── Phase 3 platformization
└── Real backend integration / Power BI
```

---

### 2. User Roles & Scenarios

#### 2.1 CPT (Capacity Planning Team)

| Scenario | Current Practice | With Product |
|----------|-----------------|--------------|
| Seasonal mold-add decision | Manually consolidate 88-column Excel, judge line by line | Upload standard files → auto-calculate → see constraints directly |
| Verify factory assumptions | Trust factory-calculated numbers with limited visibility | Use brand-side independent result to verify and challenge factory output |
| Re-run after forecast update | Rebuild Excel and re-run local scripts | Click Edit on a historical task, replace files, and submit again |

#### 2.2 GSP (Global Supply Planning)

| Scenario | Current Practice | With Product |
|----------|-----------------|--------------|
| Adjust Buy Plan | Mold constraints are invisible, Buy Plan and capacity are decoupled | Review task results to know which SKU/factory has bottleneck before adjusting buy |

#### 2.3 Admin / Data Owner

| Scenario | With Product |
|----------|--------------|
| Maintain reference data | Open Data Sources → preview Transportation Leadtime / Supplier Country → add, edit, delete rows in the preview modal |
| Monitor upstream sync | See sync status tags on Assets Master List (real-time) and LineSheet (daily) |

---

### 3. Product Architecture (Phase 1 Demo)

#### 3.1 Frontend-Only Demo Stack

```
┌─────────────────────────────────────────────────────────────┐
│                  Browser (html-v2.html)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Left Sidebar                                        │  │
│  │  • Tasks                                             │  │
│  │  • Data Sources                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│         ┌─────────────────┴─────────────────┐               │
│         ▼                                   ▼               │
│  ┌──────────────┐                  ┌─────────────────┐     │
│  │  Tasks Page  │                  │  Data Sources   │     │
│  │  • Task list │                  │  • 6 cards      │     │
│  │  • New/Edit  │                  │  • Preview modal│     │
│  │  • View Result│                 │  • Inline edit  │     │
│  └──────────────┘                  └─────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              Mocked JS data (tasks, preview rows, results)
                              │
                              ▼
              Future backend: Defan module + script engine + DB
```

> **Note**: The current demo uses static JavaScript data. File uploads, validations, and calculation results are simulated in the browser. Backend integration is not part of this PRD scope.

#### 3.2 Data Flow (Target State for Phase 1)

```
CPT User
  │
  ▼
New Calculation Task (Defan module)
  ├── Select Season + Round + Remark
  ├── Upload Mold Master Data (16-column standard)
  ├── Upload Forecast
  ├── Upload Style-Factory Allocation
  └── Optional: upload Old Mold Manual Match list
  │
  ▼ Hard validation
  ├── Missing columns      → block, show missing column names
  ├── Data type errors     → block, show row number
  ├── Season mismatch      → block
  └── Required files missing → block Next button
  │
  ▼ Validation passed
Create calculation task → status "Running"
  │
  ▼ (Future) Script engine reads DB tables → writes results
Task status → "Done" → user clicks View Result
```

#### 3.3 Relationship with Factory Data

> **Principle**: Brand-side independent calculation, used to **verify** factory output, not to replace factory scheduling.

| Dimension | Brand-side Calculation | Factory Calculation |
|-----------|------------------------|---------------------|
| Perspective | Demand + risk (global) | Supply + execution (single factory) |
| Data | Forecast, SKU Plan, MOQ | Actual equipment status, changeover time, labor schedule |
| Purpose | Early gap detection, verify factory assumptions, unify multi-factory口径 | Fine scheduling, maximize equipment utilization |
| Usage | Final decision reference; brand must know "why this number and where the deviation is" | Execution baseline |

---

### 4. Functional Modules

#### 4.1 Page Layout: Left Sidebar Navigation

| Element | Description |
|---------|-------------|
| Brand block | Icon + "Mold Capacity / Analysis" |
| Navigation | Tasks · Data Sources |
| Footer badge | Demo version label |
| Active state | Highlight current page |

#### 4.2 Tasks Page

##### 4.2.1 Page Header

- Title: "Task List"
- Primary action: "+ New Calculation Task"

##### 4.2.2 Task List Table

| Column | Description |
|--------|-------------|
| Season | Business-readable season label, e.g. "Fall 2027" |
| Round | Buy-based round label, e.g. "after May buy" |
| Remark | Optional user remark, truncated with ellipsis if too long |
| Total Molds | Total mold lines in this task |
| Matched Molds | Mold lines successfully matched |
| Match Rate | Matched / Total, displayed as tag |
| Status | Done / Running / Failed |
| Created At | Timestamp |
| Actions | View Result / Edit / Cancel |

**Anti-wrap requirements**: Actions column and numeric columns use `white-space: nowrap`; the table is wrapped in a horizontal-scroll container so buttons and tags never wrap unexpectedly on narrow screens.

##### 4.2.3 Action Rules

| Status | Available Actions |
|--------|-------------------|
| Done | View Result, Edit |
| Running | View Result (disabled), Cancel |
| Failed | Retry, Edit |

#### 4.3 New / Edit Calculation Task Modal

A 3-step wizard launched from the Tasks page.

##### Step 1 — Basic Config

| Field | Required | Options / Type |
|-------|----------|----------------|
| Season | Yes | Fall 2027, Spring 2027, Fall 2028 |
| Round (after Buy) | Yes | after March buy, after April buy, after May buy |
| Remark | No | Free text textarea |

Edit mode pre-fills Season, Round, and Remark from the selected historical task.

##### Step 2 — Upload Data

| File | Required | Purpose |
|------|----------|---------|
| Mold Master Data | Yes | 16-column standard template |
| Forecast | Yes | Global Planning forecast |
| Style-Factory Allocation | Yes | factory + style_color + supplier mapping |
| Old Mold Manual Match | No | Supplement old-mold inventory not matched in Assets Master List |

**Interactions**:
- Drag & drop or click to upload Excel.
- File list shows file name, size, and validation status.
- Required files must pass validation before the Next button is enabled.
- Optional Old Mold file shows "Uploaded" without blocking submission.
- "Download Template" links for each required file and "Download Mapping List" for the optional old-mold file.
- "Linked Base Data Sources" section lists Assets Master List, LineSheet (PLM), Transportation Leadtime, Supplier Country, with a button to jump to the Data Sources page.

##### Step 2a — Hard Validation Strategy

> **Core principle**: Hard validation is the **admission gate** that standardizes manual data imports. The goal is **not** to require perfect data, but to ensure the uploaded data is **sufficient for the calculation engine to run**. If the core schema, required fields, and key relationships are valid, the task should be allowed to proceed.

**Blocking errors** (must be fixed before the Next button is enabled):

| Validation | Rule | User Feedback |
|------------|------|---------------|
| File missing | Any required file (Mold Master Data, Forecast, Style-Factory Allocation) is not uploaded | "Please upload [file name]" |
| Required column missing | Any of the 16 standard columns in Mold Master Data is missing | "Missing column(s): [column list]. Please use the standard template." |
| Required field empty | Core fields (Brand, Mold Code, Mold Code#, Factory, Share/Single, Cycle Time) contain empty values | "Row [N]: [column] is required" |
| Data type error | Numeric fields contain non-numeric values; date fields are not parseable | "Row [N]: [column] data type error, expected [type]" |
| Season mismatch | The Season value in uploaded files does not match Step 1 selection | "Season mismatch: file shows [X], task is [Y]" |
| Invalid enum value | Brand not in UGG/HOKA/TEVA; New/Old not in New/Old/CO; Share/Single not in allowed values | "Row [N]: [column] contains invalid value [X]" |
| Non-positive cycle time | Cycle Time ≤ 0 | "Row [N]: Cycle Time must be greater than 0" |

**Non-blocking warnings / QA flags** (do not block Next; reported in calculation log and result):

| Validation | Rule | Handling |
|------------|------|----------|
| Non-critical column missing | Optional columns (Size Grading, T3 Ready Date, Sole Special Process Leadtime) are empty | Continue; use default or null |
| Format auto-correction | Brand written as "Hoka" instead of "HOKA" | Auto-convert and log |
| Multi-supplier QA | Same mold+factory+style maps to multiple suppliers | Flag row, exclude from calculation, include in QA report |
| Low old-mold match rate | Matched old molds < threshold (e.g. 70%) | Continue but warn user to verify Assets Master List or upload manual match |
| Forecast style not found in LineSheet | Style in Forecast has no matching LineSheet record | Continue with placeholder; flag for data review |

**Admission threshold**: A file passes hard validation when:
1. All required files are present.
2. All required columns exist.
3. All required fields are non-empty and type-correct.
4. Season and key enum values are consistent.
5. Numeric/date fields are parseable and within reasonable ranges.

> **Balancing act**: If validation is too strict, users cannot proceed even when the data is usable. If too loose, garbage enters the calculation. The admission criteria must reflect the **minimum information the script engine needs to produce a deterministic result**.

##### Step 3 — Run Calculation

- Shows progress bar: "Uploading files → Validating data format → Creating calculation task → Task created".
- After completion, displays "Task Created Successfully" message:
  > "The calculation task has been submitted. Results are not generated instantly. Please wait a few minutes, then return to the task list to view the result."
- User clicks "Back to Task List" to close the modal.

> **Demo note**: Calculation is simulated; no real backend job is created.

#### 4.4 Calculation Result Modal

Opened by clicking "View Result" on a Done task. Structured into four sections:

##### Section 1 — Mold Match Status

| Metric | Description |
|--------|-------------|
| Total Molds | Total mold lines in the task |
| Matched Molds | Mold lines successfully matched to data sources |
| Match Rate | Matched / Total |

##### Section 2 — Risk Without Additional Mold

| Metric | Description |
|--------|-------------|
| Total Delay Pairs | Total pairs that would be delayed if no additional molds are added |
| Total Delay Rate | Delay pairs / total pairs |
| Max Delay Day | Maximum delay days among delayed orders |

##### Section 3 — Additional Mold Result

| Metric | Description |
|--------|-------------|
| Total Matched Molds | Same as Section 1 Matched Molds |
| Molds Constraint | Number of mold lines with constraint |
| Mold Constraint Rate | Constraint molds / matched molds |
| Total Additional Mold Qty | Recommended total additional mold quantity |

##### Section 4 — Unmatched Result

**4.1 Old Mold Inventory Matched Report**
- Progress bar showing old-mold match rate.
- Breakdown: Matched (Assets Master List), Manual Supplement (uploaded), Unmatched.
- Action: "Download Full Mapping List".

**4.2 Data Source Issue**
- Count of unmatched molds caused by data-source mapping gaps.
- Action: "Download Detailed Unmatched List".

**Modal footer actions**: Close, Download Full Report.

> **Demo note**: Result numbers are static mock data differentiated by taskId (1, 2, 4).

#### 4.5 Data Sources Page

##### 4.5.1 Page Header

- Title: "Data Source Configuration"
- Hint: "Click a data source card to preview · System-managed sources only"

##### 4.5.2 Data Source Cards

| Data Source | Source | Status | Preview Features |
|-------------|--------|--------|------------------|
| Assets Master List | Mold Asset System export | Real-time sync | Preview table, Export Excel (CSV) |
| LineSheet | PLM export | Daily sync | Preview table, Export Excel (CSV) |
| Transportation Leadtime | Manual maintenance | Configurable | Preview + inline add/edit/delete, range input as "X-Y days" |
| Supplier Country | Manual maintenance | Configurable | Preview + inline add/edit/delete |
| Factory Working Holiday | Future Phase 2 | Future | Disabled card |
| Mold Opening Leadtime | Future Phase 2 | Future | Disabled card |

##### 4.5.3 Preview Modal Behavior

- Title reflects selected data source.
- Renders first N rows as a table.
- Editable sources: cells become input/select fields; supports add row and delete row.
- "Save Changes" persists to in-memory `previewData`.
- "Export Excel" downloads the current preview as CSV.
- "Close" dismisses the modal.

---

### 5. Data Specifications

#### 5.1 Input Standard: Mold Master Data Template (16 columns)

| Column | Required | Type | Rule |
|--------|----------|------|------|
| Brand | Yes | Text | UGG / HOKA / TEVA (uppercase) |
| Outsole/Midsole | Yes | Text | Only one value |
| Mold Type | Yes | Text | CM / IM / SCF / BPU / Pouring PU etc. |
| New/Old | Yes | Text | New / Old / CO |
| Mold Code | Yes | Text | Full mold code (long description) |
| Mold Code# | Yes | Text | Short code, unique identifier |
| Mold Supplier | Yes | Text | Supplier code, e.g. SF-NVNSF |
| Country of Origin | Yes | Text | Origin country |
| Factory | Yes | Text | Multiple values separated by "/" or "," |
| Share mold or single mold | Yes | Text | Single Mold / Share Mold |
| Master Style No# | Yes | Text | Multiple values separated by "/" |
| Size Grading | No | Text | Only one "=", e.g. "8=9.5" |
| Sole Special Process Leadtime | No | Text | Must contain a number (days) |
| Cycle Time (Pairs / Day) | Yes | Number | Must be > 0 |
| Initial Manufactoring Start Date | Yes | Date | Keep date format |
| T3 Ready Date | No | Date | Keep date format |

#### 5.2 Other Required Upload Files

| File | Key Columns | Purpose |
|------|-------------|---------|
| Forecast | Season, style_color, factory, qty, buy_month, xf_date | Demand input |
| Style-Factory Allocation | factory, style_color, supplier | Maps styles to factories/suppliers for Share Mold scenario |
| Old Mold Manual Match (optional) | mold_code, factory, existing_qty | Supplements Assets Master List gaps |

#### 5.3 System-Managed Reference Tables

| Table | Key Fields | Maintenance |
|-------|------------|-------------|
| Assets Master List | Brand, Mold Code, Component, Material, Bottom Supplier, Mold Type, Mold Pairs | Real-time sync from Mold Asset System |
| LineSheet | Season Name, Style Name, Division, Factory, Midsole, Outsole, Size Run | Daily sync from PLM |
| Transportation Leadtime | supplier_country, factory_country, lead_time_range (min-max days), transfer_lead_time | Manual editable in preview |
| Supplier Country | supplier, supplier_country | Manual editable in preview |

#### 5.4 Output Metric Definitions

| Metric | Definition | Unit |
|--------|------------|------|
| Total Molds | Total mold lines in the task | lines |
| Matched Molds | Mold lines successfully matched to reference data | lines |
| Match Rate | Matched Molds / Total Molds | % |
| Total Delay Pairs | Pairs that would be delayed without additional molds | pairs |
| Total Delay Rate | Total Delay Pairs / total pairs | % |
| Max Delay Day | Maximum delay days among all delayed orders | days |
| Molds Constraint | Mold lines where demand exceeds available capacity | lines |
| Mold Constraint Rate | Molds Constraint / Matched Molds | % |
| Total Additional Mold Qty | Recommended additional mold quantity across all lines | qty |
| Old Mold Match Rate | Old molds matched (Assets + manual) / total old molds | % |
| Data Source Issue Count | Unmatched molds caused by missing reference mappings | count |

---

### 6. Non-Functional Requirements (Phase 1 Demo)

#### 6.1 UI / UX

| Item | Requirement |
|------|-------------|
| Visual style | Premium, minimalist B-side enterprise style; fixed left sidebar; card-based layout |
| Responsiveness | Minimum 768px desktop; table columns use nowrap + horizontal scroll |
| Language | English UI |
| Feedback | Clear validation states, progress indication, success confirmation |

#### 6.2 Permissions (Target)

| Role | Permissions |
|------|-------------|
| CPT / GSP | Create tasks, view own tasks, view results, download reports |
| Admin | All tasks, configure base data sources, view system logs |

#### 6.3 Performance Targets (Future Backend)

| Indicator | Target | Note |
|-----------|--------|------|
| File validation | < 10s | Single file < 10k rows |
| Script calculation | < 5 min | Single season full calculation |
| Result refresh | < 2 min | From DB to frontend |
| Concurrent users | 3–5 | Phase 1 target |

#### 6.4 Maintainability

| Item | Requirement |
|------|-------------|
| Logging | Record uploader, season, round, duration, result row count, errors |
| Versioning | Same Season + Round supports multiple calculations; keep history |
| Rollback | Can reference previous round's result |
| Monitoring | Calculation failure automatically notifies data team |

---

### 7. Out of Scope (Documented in BRD)

The following topics are intentionally excluded from this PRD and are covered in `Mold Capacity Analysis — BRD.md`:

- Phase 2 algorithm enhancements: weighted priority scheduling, load leveling, cost-optimal strategy recommendation, Factory Working Holiday, Mold Opening Leadtime.
- Phase 3 platformization: integer programming / linear programming global optimization, rolling plan + dynamic re-scheduling, approval workflow, cross-season comparison, data lineage.
- Real backend implementation, Defan module integration, script engine, database schema, and Power BI visualization layer.

---

## 中文版

> **版本**: v2.2  
> **日期**: 2026-05-20  
> **范围**: Phase 1 MVP 前端 Demo (`demo/frontend/html-v2.html`)

---

### 1. 产品概述

#### 1.1 背景与痛点

当前模具产能分析依赖业务每季手工整合 **88 列 Excel 总表**，从 7+ 个数据源抽取数据。主要痛点如下：

| 痛点 | 具体表现 | 影响 |
|------|---------|------|
| 输入不标准 | 每季 Excel 结构不同，脚本无法复用 | 每季都要定制化改造脚本 |
| 计算不透明 | 业务看不到计算过程 | 无法验证、无法做 what-if |
| 结果分散 | New / Old / Allocation 三个场景各输出一个 Excel | 需要手动整合 |
| 决策滞后 | 产能缺口发现时往往已来不及调整 | 被迫被动加模或接受延迟 |

#### 1.2 产品目标（Phase 1）

| # | 目标 | 说明 |
|---|------|------|
| 1 | **输入标准化** | 强制使用固定 16 列 Mold Master Data 模板及配套文件，使计算引擎始终读取统一 Schema。 |
| 2 | **集中任务管理** | 为 CPT 提供单一页面，按 Season + Round 创建、追踪、编辑和查看计算任务。 |
| 3 | **快速呈现核心结果** | 在统一结果弹窗中展示模具匹配状态、延迟风险、加模需求和未匹配/旧模缺口。 |
| 4 | **维护基础数据源** | 让管理员在一个地方预览和编辑系统维护的参考表。 |

#### 1.3 范围边界

本 PRD 仅覆盖 `demo/frontend/html-v2.html` 中实现的 **Phase 1 MVP 前端 Demo**。长期路线图、超出当前计算逻辑的算法升级以及平台化内容另见 `Mold Capacity Analysis — BRD.md`。

```
本 PRD 范围：
├── 左侧边栏导航：Tasks / Data Sources
├── 任务页：列表、创建、编辑、查看结果
├── 新建/编辑任务弹窗：三步向导
├── 计算结果弹窗：四段式摘要
└── 数据源页：卡片 + 预览/行内编辑

不在本 PRD 范围（见 BRD）：
├── Phase 2 算法升级
├── Phase 3 平台化
└── 真实后端集成 / Power BI
```

---

### 2. 用户角色与使用场景

#### 2.1 CPT（Capacity Planning Team）

| 场景 | 当前做法 | 产品化后 |
|------|---------|---------|
| 每季加模决策 | 手工整合 88 列 Excel，逐个判断 | 上传标准文件 → 自动计算 → 直接看到 constraint |
| 验证工厂假设 | 信任工厂数据但可见性有限 | 用品牌方独立结果验证并挑战工厂输出 |
| 预测更新后重跑 | 重建 Excel 并重新跑本地脚本 | 点击历史任务 Edit，替换文件后重新提交 |

#### 2.2 GSP（Global Supply Planning）

| 场景 | 当前做法 | 产品化后 |
|------|---------|---------|
| 调整 Buy Plan | 看不到 mold constraint，Buy Plan 和产能脱节 | 先看任务结果，知道哪些 SKU/工厂有瓶颈再调整 buy |

`备注：GSP当前不会直接使用这个系统，未来会从我们建立的PowerBI分析专题中查看数据`

#### 2.3 管理员 / 数据负责人

| 场景 | 产品化后 |
|------|----------|
| 维护参考数据 | 打开 Data Sources → 预览 Transportation Leadtime / Supplier Country → 在预览弹窗中增删改行 |
| 监控上游同步 | 查看 Assets Master List（实时）和 LineSheet（每日）的同步状态标签 |

---

### 3. 产品架构（Phase 1 Demo）

#### 3.1 数据流

```
CPT 用户
  │
  ▼
新建计算任务（Defan 模块）
  ├── 选择 Season + Round + Remark
  ├── 上传 Mold Master Data（16 列标准）
  ├── 上传 Forecast
  ├── 上传 Style-Factory Allocation
  └── 可选：上传旧模手工匹配清单
  │
  ▼ 硬校验
  ├── 字段缺失      → 阻断并显示缺失列
  ├── 数据类型异常  → 阻断并显示行号
  ├── Season 不一致 → 阻断
  └── 必填文件缺失  → 阻断 Next 按钮
  │
  ▼ 校验通过
创建计算任务 → 状态"计算中"
  │
  ▼ 脚本引擎读取数据库表 → 写入结果
任务状态 → "完成" → 用户点击查看结果
```

#### 3.2 与工厂数据的关系

> **原则**: 品牌方独立核算，用于 **Verify** 工厂数据，不替代工厂排产。

| 维度 | 品牌方计算 | 工厂计算 |
|------|-----------|---------|
| 视角 | 需求 + 风险（全局） | 供给 + 执行（单厂） |
| 数据 | Forecast、SKU Plan、MOQ | 实际设备状态、换线时间、人员排班 |
| 目的 | 提前发现缺口、验证工厂假设、统一多厂口径 | 精确排产、最大化设备利用率 |
| 使用方式 | 最终决策参考；品牌必须知道"为什么用这个结果、偏差在哪" | 执行基准 |

---

### 4. 功能模块

#### 4.1 页面布局：左侧边栏导航

| 元素 | 说明 |
|------|------|
| 品牌区 | Icon + "Mold Capacity / Analysis" |
| 导航 | Tasks · Data Sources |
| 底部标签 | 产品版本号 |
| 激活状态 | 高亮当前页面 |

#### 4.2 任务页

##### 4.2.1 页面头部

- 标题: "Task List / 任务列表"
- 主要操作: "+ New Calculation Task / + 新建计算任务"

##### 4.2.2 任务列表表格

| 列 | 说明 |
|----|------|
| Season / 季节 | 业务可读季节标签，如 "Fall 2027" |
| Round / 轮次 | 基于 buy 的轮次标签，如 "after May buy" |
| Remark / 备注 | 可选备注，过长时省略 |
| Total Molds / 模具总数 | 本任务模具总数 |
| Matched Molds / 已匹配模具 | 成功匹配的模具数 |
| Match Rate / 匹配率 | 已匹配/总数，以标签展示 |
| Status / 状态 | 完成 / 计算中 / 失败 |
| Created At / 创建时间 | 时间戳 |
| Actions / 操作 | 查看结果 / 编辑 / 取消 |

**防折行要求**: Actions 列和数字列使用 `white-space: nowrap`；表格置于横向滚动容器中，避免按钮和标签在窄屏下意外换行。

##### 4.2.3 操作规则

| 状态 | 可用操作 |
|------|----------|
| 完成 | 查看结果、编辑 |
| 计算中 | 查看结果（禁用）、取消 |
| 失败 | 重试、编辑 |

#### 4.3 新建/编辑计算任务弹窗

从任务页打开的三步向导弹窗。

##### 第一步 — 基础配置

| 字段 | 必填 | 选项或类型 |
|------|------|------------|
| Season / 季节 | 是 | Fall 2027, Spring 2027, Fall 2028 |
| Round (after Buy) / 轮次 | 是 | after March buy, after April buy, after May buy |
| Remark / 备注 | 否 | 自由文本文本框 |

编辑模式会预填充所选历史任务的 Season、Round 和 Remark。

##### 第二步 — 上传数据

| 文件 | 必填 | 用途 |
|------|------|------|
| Mold Master Data / 模具主数据 | 是 | 16 列标准模板 |
| Forecast / 预测 | 是 | Global Planning 预测 |
| Style-Factory Allocation / 款式-工厂分配 | 是 | 工厂+款式颜色+供应商映射 |
| Old Mold Manual Match / 旧模手工匹配 | 否 | 补充 Assets Master List 未覆盖的旧模库存 |

**交互**：
- 拖拽或点击上传 Excel。
- 文件列表展示文件名、大小和校验状态。
- 必填文件校验通过后 Next 按钮才可用。
- 可选旧模文件显示"已上传"，不阻塞提交。
- 每个必填文件提供"下载模板"，旧模可选文件提供"下载 Mapping List"。
- "关联基础数据源"区域列出 Assets Master List、LineSheet (PLM)、Transportation Leadtime、Supplier Country，并提供跳转到数据源页的按钮。

##### 第二步补充 — 硬校验策略

> **核心原则**：硬校验是约束用户手工数据导入系统的**准入门槛**。其目标**不是**要求数据 100% 完美，而是确保上传的数据**足够支撑计算引擎运行**。只要核心 Schema、必填字段和关键关联关系正确，就应允许任务进入下一步。

**阻断性错误**（必须修复后 Next 按钮才可用）：

| 校验项 | 规则 | 用户反馈 |
|--------|------|----------|
| 文件缺失 | 必填文件（Mold Master Data、Forecast、Style-Factory Allocation）未上传 | "请上传 [文件名]" |
| 必填列缺失 | Mold Master Data 16 列标准模板中缺失任何一列 | "缺失列：[列名列表]。请使用标准模板。" |
| 必填字段为空 | 核心字段（Brand、Mold Code、Mold Code#、Factory、Share/Single、Cycle Time）存在空值 | "第 [N] 行：[列名] 为必填项" |
| 数据类型错误 | 数字字段包含非数字值；日期字段不可解析 | "第 [N] 行：[列名] 数据类型错误，应为 [类型]" |
| Season 不一致 | 上传文件中的 Season 与 Step 1 选择不一致 | "Season 不一致：文件为 [X]，任务为 [Y]" |
| 枚举值无效 | Brand字段值 不在 UGG/HOKA/TEVA 中| "第 [N] 行：[列名] 包含无效值 [X]" |
| Cycle Time 非正数 | Cycle Time ≤ 0 | "第 [N] 行：Cycle Time 必须大于 0" |


**准入门槛**：文件通过硬校验需满足：
1. 所有必填文件已上传；
2. 所有必填列存在；
3. 所有必填字段非空且类型正确；
4. Season 和关键枚举值一致；
5. 数字/日期字段可解析且在合理范围内。

> **平衡原则**：校验过严会导致数据明明可用却无法继续；过松则会让脏数据进入计算。准入标准应反映**脚本引擎产生确定性结果所需的最小信息集合**。

##### 第三步 — 提交计算

- 展示进度条："正在上传文件 → 正在校验数据格式 → 正在创建计算任务 → 任务已创建"。
- 完成后显示"任务创建成功"提示：
  > "计算任务已提交。结果不会立即生成，请等待几分钟后返回任务列表查看结果。"
- 用户点击"返回任务列表"关闭弹窗。


#### 4.4 计算结果弹窗

点击已完成任务的"查看结果"打开，分为四个模块：

##### 模块 1 — 模具匹配状态

| 指标 | 说明 |
|------|------|
| Total Molds / 模具总数 | 本任务模具总数 |
| Matched Molds / 已匹配模具 | 成功匹配到数据源的模具数 |
| Match Rate / 匹配率 | 已匹配/总数 |

##### 模块 2 — 不加模风险

| 指标 | 说明 |
|------|------|
| Total Delay Pairs / 总延迟双数 | 不加模情况下会延迟的总双数 |
| Total Delay Rate / 总延迟率 | 延迟双数/总双数 |
| Max Delay Day / 最大延迟天数 | 延迟订单中的最大延迟天数 |

##### 模块 3 — 加模结果

| 指标 | 说明 |
|------|------|
| Total Matched Molds / 总匹配模具 | 同模块 1 的已匹配模具 |
| Molds Constraint / 受限模具数 | 存在产能约束的模具数 |
| Mold Constraint Rate / 受限率 | 受限模具/已匹配模具 |
| Total Additional Mold Qty / 总加模数量 | 所有模具推荐加模数量之和 |

##### 模块 4 — 未匹配结果

**4.1 旧模库存匹配报告**
- 进度条展示旧模匹配率。
- breakdown：已匹配（Assets Master List）、手工补充（已上传）、未匹配。
- 操作："下载完整 Mapping List"。

**4.2 数据源问题**
- 因数据源映射缺失导致的未匹配模具数量。
- 操作："下载详细未匹配清单"。

**弹窗底部操作**: 关闭、下载完整报告。


#### 4.5 数据源页

##### 4.5.1 页面头部

- 标题: "Data Source Configuration / 数据源配置"
- 提示: "点击数据源卡片预览 · 仅系统维护数据源"

##### 4.5.2 数据源卡片

| 数据源 | 来源 | 状态 | 预览功能 |
|--------|------|------|----------|
| Assets Master List / 资产主数据 | Mold Asset System 导出 | 实时同步 | 预览表格、导出 Excel（CSV） |
| LineSheet / 产品资料表 | PLM 导出 | 每日同步 | 预览表格、导出 Excel（CSV） |
| Transportation Leadtime / 运输提前期 | 手工维护 | 可配置 | 预览+行内增删改，范围输入为 "X-Y days" |
| Supplier Country / 供应商国家 | 手工维护 | 可配置 | 预览+行内增删改 |
| Factory Working Holiday / 工厂工作日历 | Phase 2 引入 | 未来 | 禁用卡片 |
| Mold Opening Leadtime / 模具开模提前期 | Phase 2 引入 | 未来 | 禁用卡片 |

##### 4.5.3 预览弹窗行为

- 标题反映所选数据源。
- 渲染前 N 行为表格。
- 可编辑源：单元格变为输入/选择框；支持新增行和删除行。
- "保存修改"持久化到内存中的 `previewData`。
- "导出 Excel"将当前预览下载为 CSV。
- "关闭"关闭弹窗。

---

### 5. 数据规范

#### 5.1 输入标准：Mold Master Data 模板（16 列）

| 列名 | 必填 | 类型 | 规范 |
|------|------|------|------|
| Brand / 品牌 | 是 | 文本 | UGG / HOKA / TEVA（大写） |
| Outsole/Midsole / 外底/中底 | 是 | 文本 | 只允许一个值 |
| Mold Type / 模具类型 | 是 | 文本 | CM / IM / SCF / BPU / Pouring PU 等 |
| New/Old / 新模/旧模 | 是 | 文本 | New / Old / CO |
| Mold Code / 模具编码 | 是 | 文本 | 完整模具编码（长描述） |
| Mold Code# / 模具编码# | 是 | 文本 | 简短编码，唯一标识 |
| Mold Supplier / 模具供应商 | 是 | 文本 | 供应商代码，如 SF-NVNSF |
| Country of Origin / 产地 | 是 | 文本 | 产地 |
| Factory / 工厂 | 是 | 文本 | 多值用 "/" 或 "," 分隔 |
| Share mold or single mold / 共用模或单模 | 是 | 文本 | Single Mold / Share Mold |
| Master Style No# / 主款号 | 是 | 文本 | 多值用 "/" 分隔 |
| Size Grading / 尺码级配 | 否 | 文本 | 仅包含一个 "="，如 "8=9.5" |
| Sole Special Process Leadtime / 鞋底特殊工艺提前期 | 否 | 文本 | 必须包含数字（天数） |
| Cycle Time (Pairs / Day) / 周期时间（双/天） | 是 | 数字 | 必须 > 0 |
| Initial Manufactoring Start Date / 初始生产开始日期 | 是 | 日期 | 保留日期格式 |
| T3 Ready Date / T3 就绪日期 | 否 | 日期 | 保留日期格式 |

#### 5.2 其他必填上传文件

| 文件 | 关键列 | 用途 |
|------|--------|------|
| Forecast / 预测 | Season, style_color, factory, qty, buy_month, xf_date | 需求输入 |
| Style-Factory Allocation / 款式-工厂分配 | factory, style_color, supplier | 映射款式到工厂/供应商，用于 Share Mold 场景 |
| Old Mold Manual Match / 旧模手工匹配（可选） | mold_code, factory, existing_qty | 补充 Assets Master List 缺口 |

#### 5.3 系统维护参考表

| 表 | 关键字段 | 维护方式 |
|----|----------|----------|
| Assets Master List / 资产主数据 | Brand, Mold Code, Component, Material, Bottom Supplier, Mold Type, Mold Pairs | 从 Mold Asset System 实时同步 |
| LineSheet / 产品资料表 | Season Name, Style Name, Division, Factory, Midsole, Outsole, Size Run | 从 PLM 每日同步 |
| Transportation Leadtime / 运输提前期 | supplier_country, factory_country, lead_time_range (min-max days), transfer_lead_time | 在预览中手工编辑 |
| Supplier Country / 供应商国家 | supplier, supplier_country | 在预览中手工编辑 |

#### 5.4 输出指标定义

| 指标 | 定义 | 单位 |
|------|------|------|
| Total Molds / 模具总数 | 本任务模具线总数 | 条 |
| Matched Molds / 已匹配模具 | 成功匹配到参考数据的模具线数 | 条 |
| Match Rate / 匹配率 | 已匹配模具/模具总数 | % |
| Total Delay Pairs / 总延迟双数 | 不加模情况下会延迟的总双数 | 双 |
| Total Delay Rate / 总延迟率 | 总延迟双数/总双数 | % |
| Max Delay Day / 最大延迟天数 | 所有延迟订单中的最大延迟天数 | 天 |
| Molds Constraint / 受限模具数 | 需求超过可用产能的模具线数 | 条 |
| Mold Constraint Rate / 受限率 | 受限模具/已匹配模具 | % |
| Total Additional Mold Qty / 总加模数量 | 所有模具线推荐加模数量之和 | 套 |
| Old Mold Match Rate / 旧模匹配率 | 旧模已匹配（Assets + 手工）/ 旧模总数 | % |
| Data Source Issue Count / 数据源问题数 | 因参考映射缺失导致的未匹配模具数 | 个 |

---

### 6. 非功能性需求（Phase 1 Demo）

#### 6.1 用户界面与体验

| 项 | 要求 |
|----|------|
| 视觉风格 | 高级极简 B-side 企业风格；固定左侧边栏；卡片式布局 |
| 响应式 | 最小 768px 桌面端；表格列使用 nowrap + 横向滚动 |
| 语言 | 英文界面 |
| 反馈 | 清晰的校验状态、进度指示、成功确认 |

#### 6.2 权限（目标态）

| 角色 | 权限 |
|------|------|
| CPT / GSP | 创建任务、查看自己的任务、查看结果、下载报告 |
| 管理员 | 全部任务、配置基础数据源、查看系统日志 |

#### 6.3 性能目标（未来后端）

| 指标 | 目标 | 说明 |
|------|------|------|
| 文件校验 | < 10s | 单文件 < 1 万行 |
| 脚本计算 | < 5 min | 单季全量计算 |
| 结果刷新 | < 2 min | 从数据库到前端 |
| 并发用户 | 3–5 | Phase 1 目标 |

#### 6.4 可维护性

| 项 | 要求 |
|----|------|
| 日志 | 记录上传人、Season、Round、耗时、结果行数、错误 |
| 版本 | 同一 Season + Round 支持多次计算并保留历史 |
| 回滚 | 可回溯到上一轮计算结果 |
| 监控 | 计算失败自动通知数据团队 |

---

### 7. 不在本 PRD 范围（见 BRD）

以下内容有意排除在本 PRD 之外，详见 `Mold Capacity Analysis — BRD.md`：

- Phase 2 算法增强：加权优先级排程、负荷均衡、成本最优策略推荐、Factory Working Holiday、Mold Opening Leadtime。
- Phase 3 平台化：整数规划/线性规划全局优化、滚动计划+动态重排、审批流、跨季对比、数据血缘。
- 真实后端实现、Defan 模块集成、脚本引擎、数据库 Schema、Power BI 可视化层。

---

*Document Version / 文档版本: v2.2*  
*Based on / 基于: current `demo/frontend/html-v2.html` implementation and iteration changelog / 当前 `demo/frontend/html-v2.html` 实现及迭代修改记录*
