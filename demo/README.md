# Mold Capacity Analysis — Phase 1 Demo

## Quick Start — Frontend Demo

Open the following file directly in a browser. No environment setup is required:

```
demo/frontend/html-v2.html   ← Latest Demo (v2.0)
demo/frontend/index.html     ← Legacy Demo (v1.0)
```

**Recommended: `html-v2.html`**, which includes:
- Task list (create / edit / view results)
- Data source configuration (with editable Transportation Leadtime)
- 3-step task configuration wizard
- Dynamic calculation result display

## Python Demo (Optional)

To run the Python calculation pipeline locally:

```bash
cd demo
python phase1_demo.py
```

Dependencies: `pandas`, `openpyxl`

## File Overview

| File | Description |
|------|-------------|
| `frontend/html-v2.html` | Phase 1 MVP frontend demo |
| `frontend/index.html` | Initial frontend demo |
| `frontend/修改记录.md` | Change log (kept in Chinese for context) |
| `phase1_demo.py` | CLI pipeline entry point |
| `engine.py` | Result merge engine |
| `validator.py` | Data validation module |
| `reporter.py` | Report generator |
| `config.py` | Configuration constants |
| `output/` | Sample demo outputs |
