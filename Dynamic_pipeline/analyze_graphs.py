import os
import torch
from collections import Counter
from tqdm import tqdm

GRAPH_DIR = "dynamic_pipeline/graph_dataset"

graph_files = [
    os.path.join(GRAPH_DIR, f)
    for f in os.listdir(GRAPH_DIR)
    if f.endswith(".pt")
]

print("=" * 70)
print("GRAPH DATASET ANALYSIS")
print("=" * 70)

print("Graphs Found :", len(graph_files))

node_counter = Counter()
edge_counter = Counter()

total_nodes = 0
total_edges = 0

empty_graphs = 0

for graph_file in tqdm(graph_files):

    graph = torch.load(
        graph_file,
        weights_only=False
   )

    graph_nodes = 0
    graph_edges = 0

    for node_type in graph.node_types:

        n = graph[node_type].num_nodes

        node_counter[node_type] += n

        graph_nodes += n

    for edge_type in graph.edge_types:

        e = graph[edge_type].edge_index.size(1)

        edge_counter[str(edge_type)] += e

        graph_edges += e

    total_nodes += graph_nodes
    total_edges += graph_edges

    if graph_nodes == 0:
        empty_graphs += 1

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("Graphs           :", len(graph_files))
print("Empty Graphs     :", empty_graphs)

print("Total Nodes      :", total_nodes)
print("Total Edges      :", total_edges)

print("Average Nodes    :", round(total_nodes / len(graph_files),2))
print("Average Edges    :", round(total_edges / len(graph_files),2))

print("\n" + "=" * 70)
print("NODE TYPES")
print("=" * 70)

for k,v in node_counter.items():
    print(f"{k:20s} {v}")

print("\n" + "=" * 70)
print("EDGE TYPES")
print("=" * 70)

for k,v in edge_counter.items():
    print(f"{k:50s} {v}")
