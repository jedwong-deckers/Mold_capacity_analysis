# Mold Capacity Analysis — Product Requirements Document (PRD)

> **Document Version**: v2.0  
> **Updated Date**: 2026-05-20  
> **Product Scope**: Phase 1 MVP Frontend Demo (`demo/frontend/html-v2.html`)  
> **Positioning**: Brand-side independent mold capacity verification tool for CPT/GSP users to upload standardized data, trigger calculations, and review results.

---

## 1. Product Overview

### 1.1 Background & Pain Points

Current mold capacity analysis relies on a manually consolidated **88-column Excel summary** pulled from 7+ data sources each season. Key pain points:

| Pain Point | Manifestation | Impact |
|------------|---------------|--------|
| Non-standard inputs | Each season's Excel structure differs, making scripts hard to reuse | Custom script rework every season |
| Opaque calculations | Business users cannot see how results are derived | No way to verify or run what-if analysis |
| Fragmented outputs | New / Old / Allocation scenarios each produce separate Excel files | Manual consolidation required |
| Delayed decisions | Capacity gaps are often discovered too late to react | Forced into passive mold adds or accepted delays |

### 1.2 Product Goals (Phase 1)

| # | Goal | Description |
|---|------|-------------|
| 1 | **Standardize inputs** | Enforce a fixed 16-column Mold Master Data template and required companion files so the calculation engine always reads the same schema. |
| 2 | **Centralize task management** | Provide a single page where CPT users create, track, edit, and review calculation tasks by Season + Round. |
| 3 | **Surface core results quickly** | Show mold match status, delay risk, additional mold requirements, and unmatched/old-mold gaps in a unified result modal. |
| 4 | **Maintain base data sources** | Let admins preview and edit system-managed reference tables (Assets, LineSheet, Leadtime, Supplier Country) in one place. |

### 1.3 Scope Boundary

This PRD covers **only the Phase 1 MVP frontend demo** implemented in `demo/frontend/html-v2.html`. Long-term road-map, algorithm enhancements beyond the current calculation logic, and platformization topics are documented separately in `Mold Capacity Analysis — BRD.md`.

```
In scope (this PRD):
├── Left-sidebar navigation: Tasks / Data Sources
├── Tasks page: list, create, edit, view result
├── New/Edit Task modal: 3-step wizard
├── Calculation Result modal: 4-section summary
└── Data Sources page: cards + preview / inline edit

Out of scope (see BRD):
├── Phase 2 algorithm upgrades (weighted priority, load leveling, cost optimization)
├── Phase 3 platformization (integer programming, rolling plan, approval flow, data lineage)
└── Real backend integration / Power BI visualization layer
```

---

## 2. User Roles & Scenarios

### 2.1 CPT (Capacity Planning Team)

| Scenario | Current Practice | With Product |
|----------|-----------------|--------------|
| Seasonal mold-add decision | Manually consolidate 88-column Excel, judge line by line | Upload standard files → auto-calculate → see constraints directly |
| Verify factory assumptions | Trust factory-calculated numbers with limited visibility | Use brand-side independent result to verify and challenge factory output |
| Re-run after forecast update | Rebuild Excel and re-run local scripts | Click Edit on a historical task, replace files, and submit again |

### 2.2 GSP (Global Supply Planning)

| Scenario | Current Practice | With Product |
|----------|-----------------|--------------|
| Adjust Buy Plan | Mold constraints are invisible, Buy Plan and capacity are decoupled | Review task results to know which SKU/factory has bottleneck before adjusting buy |

### 2.3 Admin / Data Owner

| Scenario | With Product |
|----------|--------------|
| Maintain reference data | Open Data Sources → preview Transportation Leadtime / Supplier Country → add, edit, delete rows in the preview modal |
| Monitor upstream sync | See sync status tags on Assets Master List (real-time) and LineSheet (daily) |

---

## 3. Product Architecture (Phase 1 Demo)

### 3.1 Frontend-Only Demo Stack

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

### 3.2 Data Flow (Target State for Phase 1)

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

### 3.3 Relationship with Factory Data

> **Principle**: Brand-side independent calculation, used to **verify** factory output, not to replace factory scheduling.

| Dimension | Brand-side Calculation | Factory Calculation |
|-----------|------------------------|---------------------|
| Perspective | Demand + risk (global) | Supply + execution (single factory) |
| Data | Forecast, SKU Plan, MOQ | Actual equipment status, changeover time, labor schedule |
| Purpose | Early gap detection, verify factory assumptions, unify multi-factory口径 | Fine scheduling, maximize equipment utilization |
| Usage | Final decision reference; brand must know "why this number and where the deviation is" | Execution baseline |

---

## 4. Functional Modules

### 4.1 Page Layout: Left Sidebar Navigation

| Element | Description |
|---------|-------------|
| Brand block | Icon + "Mold Capacity / Analysis" |
| Navigation | Tasks · Data Sources |
| Footer badge | Demo version label |
| Active state | Highlight current page |

### 4.2 Tasks Page

#### 4.2.1 Page Header

- Title: "Task List"
- Primary action: "+ New Calculation Task"

#### 4.2.2 Task List Table

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

#### 4.2.3 Action Rules

| Status | Available Actions |
|--------|-------------------|
| Done | View Result, Edit |
| Running | View Result (disabled), Cancel |
| Failed | Retry, Edit |

### 4.3 New / Edit Calculation Task Modal

A 3-step wizard launched from the Tasks page.

#### Step 1 — Basic Config

| Field | Required | Options / Type |
|-------|----------|----------------|
| Season | Yes | Fall 2027, Spring 2027, Fall 2028 |
| Round (after Buy) | Yes | after March buy, after April buy, after May buy |
| Remark | No | Free text textarea |

Edit mode pre-fills Season, Round, and Remark from the selected historical task.

#### Step 2 — Upload Data

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

#### Step 3 — Run Calculation

- Shows progress bar: "Uploading files → Validating data format → Creating calculation task → Task created".
- After completion, displays "Task Created Successfully" message:
  > "The calculation task has been submitted. Results are not generated instantly. Please wait a few minutes, then return to the task list to view the result."
- User clicks "Back to Task List" to close the modal.

> **Demo note**: Calculation is simulated; no real backend job is created.

### 4.4 Calculation Result Modal

Opened by clicking "View Result" on a Done task. Structured into four sections:

#### Section 1 — Mold Match Status

| Metric | Description |
|--------|-------------|
| Total Molds | Total mold lines in the task |
| Matched Molds | Mold lines successfully matched to data sources |
| Match Rate | Matched / Total |

#### Section 2 — Risk Without Additional Mold

| Metric | Description |
|--------|-------------|
| Total Delay Pairs | Total pairs that would be delayed if no additional molds are added |
| Total Delay Rate | Delay pairs / total pairs |
| Max Delay Day | Maximum delay days among delayed orders |

#### Section 3 — Additional Mold Result

| Metric | Description |
|--------|-------------|
| Total Matched Molds | Same as Section 1 Matched Molds |
| Molds Constraint | Number of mold lines with constraint |
| Mold Constraint Rate | Constraint molds / matched molds |
| Total Additional Mold Qty | Recommended total additional mold quantity |

#### Section 4 — Unmatched Result

**4.1 Old Mold Inventory Matched Report**
- Progress bar showing old-mold match rate.
- Breakdown: Matched (Assets Master List), Manual Supplement (uploaded), Unmatched.
- Action: "Download Full Mapping List".

**4.2 Data Source Issue**
- Count of unmatched molds caused by data-source mapping gaps.
- Action: "Download Detailed Unmatched List".

**Modal footer actions**: Close, Download Full Report.

> **Demo note**: Result numbers are static mock data differentiated by taskId (1, 2, 4).

### 4.5 Data Sources Page

#### 4.5.1 Page Header

- Title: "Data Source Configuration"
- Hint: "Click a data source card to preview · System-managed sources only"

#### 4.5.2 Data Source Cards

| Data Source | Source | Status | Preview Features |
|-------------|--------|--------|------------------|
| Assets Master List | Mold Asset System export | Real-time sync | Preview table, Export Excel (CSV) |
| LineSheet | PLM export | Daily sync | Preview table, Export Excel (CSV) |
| Transportation Leadtime | Manual maintenance | Configurable | Preview + inline add/edit/delete, range input as "X-Y days" |
| Supplier Country | Manual maintenance | Configurable | Preview + inline add/edit/delete |
| Factory Working Holiday | Future Phase 2 | Future | Disabled card |
| Mold Opening Leadtime | Future Phase 2 | Future | Disabled card |

#### 4.5.3 Preview Modal Behavior

- Title reflects selected data source.
- Renders first N rows as a table.
- Editable sources: cells become input/select fields; supports add row and delete row.
- "Save Changes" persists to in-memory `previewData`.
- "Export Excel" downloads the current preview as CSV.
- "Close" dismisses the modal.

---

## 5. Data Specifications

### 5.1 Input Standard: Mold Master Data Template (16 columns)

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

### 5.2 Other Required Upload Files

| File | Key Columns | Purpose |
|------|-------------|---------|
| Forecast | Season, style_color, factory, qty, buy_month, xf_date | Demand input |
| Style-Factory Allocation | factory, style_color, supplier | Maps styles to factories/suppliers for Share Mold scenario |
| Old Mold Manual Match (optional) | mold_code, factory, existing_qty | Supplements Assets Master List gaps |

### 5.3 System-Managed Reference Tables

| Table | Key Fields | Maintenance |
|-------|------------|-------------|
| Assets Master List | Brand, Mold Code, Component, Material, Bottom Supplier, Mold Type, Mold Pairs | Real-time sync from Mold Asset System |
| LineSheet | Season Name, Style Name, Division, Factory, Midsole, Outsole, Size Run | Daily sync from PLM |
| Transportation Leadtime | supplier_country, factory_country, lead_time_range (min-max days), transfer_lead_time | Manual editable in preview |
| Supplier Country | supplier, supplier_country | Manual editable in preview |

### 5.4 Output Metric Definitions

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

## 6. Non-Functional Requirements (Phase 1 Demo)

### 6.1 UI / UX

| Item | Requirement |
|------|-------------|
| Visual style | Premium, minimalist B-side enterprise style; fixed left sidebar; card-based layout |
| Responsiveness | Minimum 768px desktop; table columns use nowrap + horizontal scroll |
| Language | English UI |
| Feedback | Clear validation states, progress indication, success confirmation |

### 6.2 Permissions (Target)

| Role | Permissions |
|------|-------------|
| CPT / GSP | Create tasks, view own tasks, view results, download reports |
| Admin | All tasks, configure base data sources, view system logs |

### 6.3 Performance Targets (Future Backend)

| Indicator | Target | Note |
|-----------|--------|------|
| File validation | < 10s | Single file < 10k rows |
| Script calculation | < 5 min | Single season full calculation |
| Result refresh | < 2 min | From DB to frontend |
| Concurrent users | 3–5 | Phase 1 target |

### 6.4 Maintainability

| Item | Requirement |
|------|-------------|
| Logging | Record uploader, season, round, duration, result row count, errors |
| Versioning | Same Season + Round supports multiple calculations; keep history |
| Rollback | Can reference previous round's result |
| Monitoring | Calculation failure automatically notifies data team |

---

## 7. Out of Scope (Documented in BRD)

The following topics are intentionally excluded from this PRD and are covered in `Mold Capacity Analysis — BRD.md`:

- Phase 2 algorithm enhancements: weighted priority scheduling, load leveling, cost-optimal strategy recommendation, Factory Working Holiday, Mold Opening Leadtime.
- Phase 3 platformization: integer programming / linear programming global optimization, rolling plan + dynamic re-scheduling, approval workflow, cross-season comparison, data lineage.
- Real backend implementation, Defan module integration, script engine, database schema, and Power BI visualization layer.

---

*Document Version: v2.0*  
*Based on: current `demo/frontend/html-v2.html` implementation and iteration changelog*
