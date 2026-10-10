import pandas as pd

df = pd.read_csv(
    "dynamic_pipeline/fusion/hybrid_dataset.csv",
    low_memory=False
)

mismatch = df[
    df["family_static"] != df["family_dynamic"]
]

print("="*70)
print("Family mismatches:", len(mismatch))
print("="*70)

print(
    mismatch[
        [
            "sha256",
            "family_static",
            "family_dynamic"
        ]
    ].head(30)
)
