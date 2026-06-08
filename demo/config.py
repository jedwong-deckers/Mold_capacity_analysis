"""Phase 1 Demo — 配置文件"""
from pathlib import Path

# === 基础数据目录（复用 Program basic data） ===
BASE_DATA_DIR = Path(__file__).resolve().parent.parent / "Program basic data"

# === 输入文件 ===
MOLD_MASTER_FILE = BASE_DATA_DIR / "Mold Master Data.xlsx"
FORECAST_FILE = BASE_DATA_DIR / "S27_FORECAST_0512.xlsx"
LINESHEET_FILE = BASE_DATA_DIR / "LineSheet_S27.xlsx"
ASSETS_FILE = BASE_DATA_DIR / "Assets Master List.xlsx"
LEADTIME_FILE = BASE_DATA_DIR / "factory_location_transportation_leadtime.xlsx"
ALLOCATION_FILE = BASE_DATA_DIR / "factory_style_color_supplier_allocation.xlsx"
SUPPLIER_COUNTRY_FILE = BASE_DATA_DIR / "supplier_country.xlsx"

# === 已有脚本目录 ===
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "Additioanl mold Python"

# === 输出目录 ===
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# === Mold Master Data 标准列定义 ===
MOLD_MASTER_COLUMNS = [
    "Brand", "Outsole/Midsole", "Mold Type", "New/Old", "Mold Code",
    "Mold Code#", "Mold Supplier", "Country of Origin", "Factory",
    "Share mold or single mold", "Master Style No#", "Size Grading",
    "Sole Special Process Leadtime", "Cycle Time (Pairs / Day)",
    "Initial Manufactoring Start Date", "T3 Ready Date",
]

MOLD_MASTER_REQUIRED = [
    "Brand", "Outsole/Midsole", "Mold Type", "New/Old", "Mold Code",
    "Mold Code#", "Mold Supplier", "Country of Origin", "Factory",
    "Share mold or single mold", "Master Style No#",
    "Cycle Time (Pairs / Day)", "Initial Manufactoring Start Date",
]

VALID_BRANDS = ["UGG", "HOKA", "TEVA"]
VALID_NEW_OLD = ["New", "Old", "CO"]

# === 计算参数 ===
MAX_ADDITIONAL_MOLD = 200
DAYS_PER_WEEK = 6
WEEK_CONVERSION = 7
MOLD_READY_BUFFER_DAYS = 7
EXTRA_LEADTIME_BUFFER = 30
