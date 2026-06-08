# Mold Capacity Analysis — Phase 1 Demo

## 快速查看前端 Demo

直接用浏览器打开以下文件即可，无需任何环境配置：

```
demo/frontend/html-v2.html   ← 最新版 Demo（v2.0）
demo/frontend/index.html     ← 旧版 Demo（v1.0）
```

**推荐查看 `html-v2.html`**，包含：
- 计算任务清单（新建 / 编辑 / 查看结果）
- 基础数据源配置（含 Transportation Leadtime 可编辑维护）
- 三步计算任务配置向导
- 动态计算结果展示

## Python Demo（可选）

如需本地运行 Python 计算管线：

```bash
cd demo
python phase1_demo.py
```

依赖：`pandas`, `openpyxl`

## 文件说明

| 文件 | 说明 |
|------|------|
| `frontend/html-v2.html` | Phase 1 MVP 前端 Demo |
| `frontend/index.html` | 初版前端 Demo |
| `frontend/修改记录.md` | 迭代修改记录 |
| `phase1_demo.py` | CLI 计算管线入口 |
| `engine.py` | 结果合并引擎 |
| `validator.py` | 数据校验模块 |
| `reporter.py` | 报告生成器 |
| `config.py` | 配置常量 |
| `output/` | Demo 运行示例输出 |
