import os
import shutil
import pandas as pd

MIN_SAMPLES = 5

BASE = "dynamic_pipeline"

fusion_csv = os.path.join(BASE, "fusion", "hybrid_dataset.csv")
graph_dir = os.path.join(BASE, "graph_dataset")

output_csv = os.path.join(BASE, "fusion", "hybrid_dataset_filtered.csv")
output_graphs = os.path.join(BASE, "graph_dataset_filtered")

os.makedirs(output_graphs, exist_ok=True)

df = pd.read_csv(fusion_csv, low_memory=False)

counts = df["family_static"].value_counts()

valid = counts[counts >= MIN_SAMPLES].index

filtered = df[df["family_static"].isin(valid)].copy()

filtered.to_csv(output_csv, index=False)

copied = 0

for sha in filtered["sha256"]:

    src = os.path.join(graph_dir, f"{sha}.pt")
    dst = os.path.join(output_graphs, f"{sha}.pt")

    if os.path.exists(src):
        shutil.copy2(src, dst)
        copied += 1

print("=" * 70)
print("FILTER COMPLETED")
print("=" * 70)
print("Minimum Samples :", MIN_SAMPLES)
print("Remaining Families :", filtered["family_static"].nunique())
print("Remaining Samples :", len(filtered))
print("Graphs Copied :", copied)
print("Output CSV :", output_csv)
print("Output Graphs :", output_graphs)
print("=" * 70)
