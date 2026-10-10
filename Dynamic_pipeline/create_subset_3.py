"""
Create Remaining VirusTotal Download Subset
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

STATIC_CSV = BASE_DIR.parent / "static_features" / "static_features.csv"
REPORT_ROOT = BASE_DIR / "reports" / "virustotal"

OUTPUT = BASE_DIR / "subset" / "family_subset_3.csv"

print("=" * 70)
print("Creating Remaining VT Subset")
print("=" * 70)

df = pd.read_csv(STATIC_CSV, low_memory=False)

remaining = []

for _, row in df.iterrows():

    sha256 = row["sha256"]
    family = row["family"]

    report = REPORT_ROOT / family / f"{sha256}.json"

    if not report.exists():

        remaining.append(row)

remaining = pd.DataFrame(remaining)

remaining.to_csv(
    OUTPUT,
    index=False,
)

print(f"Original Samples : {len(df)}")
print(f"Remaining Samples: {len(remaining)}")
print(f"Saved To         : {OUTPUT}")
print("=" * 70)
