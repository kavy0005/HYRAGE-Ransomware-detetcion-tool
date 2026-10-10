"""
Module 1
Family-wise Stratified Sample Selector

Input:
    static_features/static_features.csv

Output:
    dynamic_pipeline/subset/family_subset.csv

Author:
    Kavya Research Pipeline
"""

from pathlib import Path
import pandas as pd

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

SAMPLES_PER_FAMILY = 20
RANDOM_SEED = 42

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_CSV = BASE_DIR / "static_features" / "static_features.csv"

OUTPUT_DIR = BASE_DIR / "dynamic_pipeline" / "subset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "family_subset.csv"

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

print("=" * 60)
print("Loading Static Dataset")
print("=" * 60)

df = pd.read_csv(STATIC_CSV)

print(f"Total Samples : {len(df)}")

# -------------------------------------------------------
# Remove invalid rows
# -------------------------------------------------------

df = df.dropna(subset=["family", "sha256"])

# -------------------------------------------------------
# Family Statistics
# -------------------------------------------------------

family_counts = df["family"].value_counts().sort_index()

print("\nFamilies Found\n")

for family, count in family_counts.items():
    print(f"{family:<20} {count}")

# -------------------------------------------------------
# Stratified Sampling
# -------------------------------------------------------
subset = []

for family in sorted(df["family"].unique()):

    family_df = df[df["family"] == family]

    count = len(family_df)

    if count <= 20:
        n = count

    elif count <= 50:
        n = 25

    elif count <= 100:
        n = 35

    elif count <= 300:
        n = 45

    else:
        n = 60

    # Never sample more than available
    n = min(n, count)

    sampled = family_df.sample(
        n=n,
        random_state=RANDOM_SEED
    )

    subset.append(sampled)
subset_df = pd.concat(subset)

subset_df = subset_df.sort_values(
    by=["family", "filename"]
)
# -------------------------------------------------------
# Save
# -------------------------------------------------------

subset_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("Subset Created Successfully")
print("=" * 60)

print(f"Families        : {subset_df.family.nunique()}")
print(f"Selected Samples: {len(subset_df)}")
print(f"Saved To        : {OUTPUT_FILE}")
print("=" * 60)
