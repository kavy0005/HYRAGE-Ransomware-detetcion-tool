"""
Behavior Graph Builder

Creates heterogeneous PyTorch Geometric graphs
from VirusTotal behavior entities.

Input
-----
fusion/hybrid_dataset.csv
graphs/graph_entities.json

Output
------
graph_dataset/*.pt
"""

# ==========================================================
# IMPORTS
# ==========================================================

import json
from pathlib import Path

import pandas as pd
import torch
from torch_geometric.data import HeteroData
from tqdm import tqdm

from ml_pipeline.utils.graph_utils import build_vocab

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

FUSION_CSV = BASE_DIR / "fusion" / "hybrid_dataset.csv"
ENTITY_JSON = BASE_DIR / "graphs" / "graph_entities.json"

OUTPUT_DIR = BASE_DIR / "graph_dataset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# LOAD VOCABULARY
# ==========================================================

VOCAB = build_vocab()

# ==========================================================
# LOAD DATA
# ==========================================================

print("=" * 70)
print("Behavior Graph Builder")
print("=" * 70)

fusion_df = pd.read_csv(
    FUSION_CSV,
    low_memory=False
)

with open(ENTITY_JSON, "r") as f:
    entity_data = json.load(f)

entity_lookup = {
    sample["sha256"]: sample
    for sample in entity_data
}

print(f"Hybrid Samples : {len(fusion_df)}")
print(f"Entity Samples : {len(entity_lookup)}")

# ==========================================================
# GRAPH HELPERS
# ==========================================================

NODE_TYPE_MAP = {
    "process": "processes",
    "file": "files",
    "registry": "registry",
    "dns": "dns",
    "ip": "ips",
    "command": "commands",
    "module": "modules",
    "mitre": "mitre"
}


def add_node_type(graph, node_type, values):
    """
    Adds behavior nodes using integer vocabulary IDs.
    """

    if not values:
        return 0

    vocab = VOCAB[NODE_TYPE_MAP[node_type]]

    node_ids = [
        vocab.get(value, 0)
        for value in values
    ]

    graph[node_type].x = torch.tensor(
        node_ids,
        dtype=torch.long
    ).view(-1, 1)

    return len(node_ids)


def add_edge(
    graph,
    src_type,
    relation,
    dst_type,
    reverse_relation,
    count
):
    """
    Creates forward and reverse edges.
    """

    if count == 0:
        return

    src = torch.zeros(
        count,
        dtype=torch.long
    )

    dst = torch.arange(
        count,
        dtype=torch.long
    )

    # Forward edge
    graph[
        (src_type, relation, dst_type)
    ].edge_index = torch.stack(
        [src, dst],
        dim=0
    )

    # Reverse edge
    graph[
        (dst_type, reverse_relation, src_type)
    ].edge_index = torch.stack(
        [dst, src],
        dim=0
    )


def add_behavior(
    graph,
    node_type,
    relation,
    values
):
    """
    Creates nodes + forward/reverse edges.
    """

    count = add_node_type(
        graph,
        node_type,
        values
    )

    add_edge(
        graph=graph,
        src_type="sample",
        relation=relation,
        dst_type=node_type,
        reverse_relation="belongs_to",
        count=count
    )
# ==========================================================
# BUILD GRAPH
# ==========================================================

def build_graph(sample, entity):

    graph = HeteroData()

    # ------------------------------------------------------
    # Sample Node
    # ------------------------------------------------------

    graph["sample"].x = torch.tensor(
        [[1]],
        dtype=torch.long
    )

    # ------------------------------------------------------
    # Process
    # ------------------------------------------------------

    add_behavior(
        graph,
        "process",
        "creates",
        entity["processes"]
    )

    # ------------------------------------------------------
    # File
    # ------------------------------------------------------

    add_behavior(
        graph,
        "file",
        "writes",
        entity["files"]
    )

    # ------------------------------------------------------
    # Registry
    # ------------------------------------------------------

    add_behavior(
        graph,
        "registry",
        "modifies",
        entity["registry"]
    )

    # ------------------------------------------------------
    # DNS
    # ------------------------------------------------------

    add_behavior(
        graph,
        "dns",
        "queries",
        entity["dns"]
    )

    # ------------------------------------------------------
    # IP
    # ------------------------------------------------------

    add_behavior(
        graph,
        "ip",
        "connects",
        entity["ips"]
    )

    # ------------------------------------------------------
    # Command
    # ------------------------------------------------------

    add_behavior(
        graph,
        "command",
        "executes",
        entity["commands"]
    )

    # ------------------------------------------------------
    # Module
    # ------------------------------------------------------

    add_behavior(
        graph,
        "module",
        "loads",
        entity["modules"]
    )

    # ------------------------------------------------------
    # MITRE
    # ------------------------------------------------------

    add_behavior(
        graph,
        "mitre",
        "uses",
        entity["mitre"]
    )

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    graph.sha256 = sample["sha256"]
    graph.family = sample["family_static"]

    return graph
# ==========================================================
# BUILD GRAPH DATASET
# ==========================================================

print("\nBuilding Behavior Graphs...\n")

graph_count = 0
missing_count = 0

for _, sample in tqdm(
    fusion_df.iterrows(),
    total=len(fusion_df),
    desc="Creating Graphs"
):

    sha256 = sample["sha256"]

    entity = entity_lookup.get(sha256)

    if entity is None:
        missing_count += 1
        continue

    graph = build_graph(
        sample,
        entity
    )

    torch.save(
        graph,
        OUTPUT_DIR / f"{sha256}.pt"
    )

    graph_count += 1
# ==========================================================
# SUMMARY
# ==========================================================

print("\n" + "=" * 70)
print("GRAPH DATASET CREATED")
print("=" * 70)

print(f"Graphs Created : {graph_count}")
print(f"Missing Graphs : {missing_count}")
print(f"Saved To       : {OUTPUT_DIR}")

print("=" * 70)
