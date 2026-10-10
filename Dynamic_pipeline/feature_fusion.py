"""
Feature Fusion Module

Merges:
    Static Features
        +
    Dynamic Features

Output:
    hybrid_dataset.csv
"""

from pathlib import Path
import pandas as pd

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

STATIC_CSV = PROJECT_DIR / "static_features" / "static_features.csv"

DYNAMIC_CSV = BASE_DIR / "features" / "dynamic_features.csv"

OUTPUT_DIR = BASE_DIR / "fusion"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "hybrid_dataset.csv"

# ==========================================================
# LOAD DATASETS
# ==========================================================

print("=" * 70)
print("Feature Fusion")
print("=" * 70)

static_df = pd.read_csv(
    STATIC_CSV,
    low_memory=False
)

dynamic_df = pd.read_csv(
    DYNAMIC_CSV
)

print(f"Static Samples  : {len(static_df)}")
print(f"Dynamic Samples : {len(dynamic_df)}")
# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

static_before = len(static_df)
dynamic_before = len(dynamic_df)

static_df = static_df.drop_duplicates(subset=["sha256"])
dynamic_df = dynamic_df.drop_duplicates(subset=["sha256"])

print("\nRemoving duplicate SHA256 values...")

print(f"Static Removed  : {static_before - len(static_df)}")
print(f"Dynamic Removed : {dynamic_before - len(dynamic_df)}")

# ==========================================================
# FEATURE FUSION
# ==========================================================

print("\nMerging datasets...")

hybrid_df = pd.merge(
    static_df,
    dynamic_df,
    on="sha256",
    how="inner",
    suffixes=("_static", "_dynamic")
)

print(f"Merged Samples : {len(hybrid_df)}")
# ==========================================================
# VALIDATION
# ==========================================================

print("\nValidating merged dataset...")

missing_static = len(dynamic_df) - len(hybrid_df)

print(f"Missing Matches : {missing_static}")

print(f"Total Columns   : {len(hybrid_df.columns)}")

# ==========================================================
# SAVE
# ==========================================================

hybrid_df.to_csv(
    OUTPUT_CSV,
    index=False
)

print("\n" + "=" * 70)
print("FEATURE FUSION COMPLETED")
print("=" * 70)

print(f"Hybrid Samples : {len(hybrid_df)}")
print(f"Output File    : {OUTPUT_CSV}")
print("=" * 70)
