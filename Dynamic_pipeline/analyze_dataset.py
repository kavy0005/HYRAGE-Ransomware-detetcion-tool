import pandas as pd

df = pd.read_csv(
    "dynamic_pipeline/fusion/hybrid_dataset.csv",
    low_memory=False
)

# Safety check
if not (df["family_static"] == df["family_dynamic"]).all():
    print("WARNING: Family mismatch detected!")

family = "family_static"

print("=" * 70)
print("DATASET ANALYSIS")
print("=" * 70)

print(f"\nTotal Samples  : {len(df)}")
print(f"Total Families : {df[family].nunique()}")

family_counts = (
    df[family]
    .value_counts()
    .sort_values(ascending=False)
)

print("\nTop 20 Families")
print("-" * 70)
print(family_counts.head(20))

print("\nBottom 20 Families")
print("-" * 70)
print(family_counts.tail(20))

print("\nStatistics")
print("-" * 70)
print(family_counts.describe())

family_counts.to_csv(
    "dynamic_pipeline/output/family_distribution.csv"
)

print("\nSaved:")
print("dynamic_pipeline/output/family_distribution.csv")
