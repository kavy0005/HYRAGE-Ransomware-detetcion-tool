import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent

CSV = BASE / "subset" / "family_subset.csv"
REPORTS = BASE / "reports" / "virustotal"
OUTPUT = BASE / "subset" / "missing_queue.csv"

df = pd.read_csv(CSV)

missing = []

for _, row in df.iterrows():

    sha = row["sha256"]
    family = row["family"]

    outfile = REPORTS / family / f"{sha}.json"

    if not outfile.exists():

        missing.append(row)

missing_df = pd.DataFrame(missing)

missing_df.to_csv(OUTPUT, index=False)

print("=" * 60)
print(f"Total Samples      : {len(df)}")
print(f"Already Downloaded : {len(df)-len(missing_df)}")
print(f"Missing Reports    : {len(missing_df)}")
print(f"Queue Saved To     : {OUTPUT}")
print("=" * 60)
