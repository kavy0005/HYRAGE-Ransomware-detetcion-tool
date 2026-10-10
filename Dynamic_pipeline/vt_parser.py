"""
VirusTotal Behaviour Parser
Phase 1 - Scanner & Loader

Scans all VirusTotal behaviour reports and prepares them for
feature extraction.
"""

import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

REPORT_ROOT = BASE_DIR / "reports" / "virustotal"

FEATURE_DIR = BASE_DIR / "features"

GRAPH_DIR = BASE_DIR / "graphs"

FEATURE_DIR.mkdir(exist_ok=True)

GRAPH_DIR.mkdir(exist_ok=True)

OUTPUT_CSV = FEATURE_DIR / "dynamic_features.csv"

GRAPH_JSON = GRAPH_DIR / "graph_entities.json"

# ==========================================================
# FIND REPORTS
# ==========================================================

json_files = sorted(REPORT_ROOT.rglob("*.json"))

print("=" * 70)
print("VirusTotal Behaviour Parser")
print("=" * 70)
print(f"Reports Found : {len(json_files)}")

# ==========================================================
# HELPERS
# ==========================================================

def load_report(path):

    with open(path, "r") as f:

        return json.load(f)


def get_family(path):

    return path.parent.name


def get_sha256(path):

    return path.stem
# ==========================================================
# FEATURE EXTRACTION
# ==========================================================

def safe_len(data, key):
    """
    Safely returns length of a list.
    """

    try:
        return len(data.get(key, []))
    except Exception:
        return 0


def extract_features(report):

    data = report.get("data") or {}

    features = {}

    # -------------------------
    # File Behaviour
    # -------------------------

    features["files_opened"] = safe_len(data, "files_opened")
    features["files_written"] = safe_len(data, "files_written")
    features["files_deleted"] = safe_len(data, "files_deleted")
    features["files_dropped"] = safe_len(data, "files_dropped")

    # -------------------------
    # Registry
    # -------------------------

    features["registry_opened"] = safe_len(data, "registry_keys_opened")
    features["registry_set"] = safe_len(data, "registry_keys_set")
    features["registry_deleted"] = safe_len(data, "registry_keys_deleted")

    # -------------------------
    # Processes
    # -------------------------

    features["process_created"] = safe_len(data, "processes_created")
    features["process_terminated"] = safe_len(data, "processes_terminated")
    features["process_injected"] = safe_len(data, "processes_injected")
    features["process_tree"] = safe_len(data, "processes_tree")

    # -------------------------
    # Network
    # -------------------------

    features["dns_lookup"] = safe_len(data, "dns_lookups")
    features["ip_traffic"] = safe_len(data, "ip_traffic")
    features["memory_domains"] = safe_len(data, "memory_pattern_domains")
    features["memory_urls"] = safe_len(data, "memory_pattern_urls")

    # -------------------------
    # Mutex
    # -------------------------

    features["mutex_created"] = safe_len(data, "mutexes_created")
    features["mutex_opened"] = safe_len(data, "mutexes_opened")

    # -------------------------
    # Services
    # -------------------------

    features["services_started"] = safe_len(data, "services_started")
    features["services_opened"] = safe_len(data, "services_opened")

    # -------------------------
    # Threat Intelligence
    # -------------------------

    features["mitre"] = safe_len(data, "mitre_attack_techniques")
    features["attack_techniques"] = safe_len(data, "attack_techniques")
    features["sigma"] = safe_len(data, "sigma_analysis_results")
    features["mbc"] = safe_len(data, "mbc")
    features["signature_matches"] = safe_len(data, "signature_matches")

    # -------------------------
    # Commands
    # -------------------------

    features["command_execution"] = safe_len(data, "command_executions")
    features["modules_loaded"] = safe_len(data, "modules_loaded")
    features["system_property_lookup"] = safe_len(data, "system_property_lookups")
    features["calls_highlighted"] = safe_len(data, "calls_highlighted")

    # -------------------------
    # Verdict
    # -------------------------

    features["verdict_confidence"] = data.get("verdict_confidence", 0)

    features["verdict_labels"] = safe_len(data, "verdict_labels")
    features["verdicts"] = safe_len(data, "verdicts")
    features["tags"] = safe_len(data, "tags")

    return features
# ==========================================================
# PARSE ALL REPORTS
# ==========================================================

rows = []

print("\nExtracting dynamic features...\n")

for report_file in tqdm(json_files):

    try:

        report = load_report(report_file)

        family = get_family(report_file)

        sha256 = get_sha256(report_file)

        features = extract_features(report)

        row = {
            "sha256": sha256,
            "family": family
        }

        row.update(features)

        rows.append(row)

    except Exception as e:

        print(f"[ERROR] {report_file.name}: {e}")

print(f"\nSuccessfully Parsed : {len(rows)} Reports")
# ==========================================================
# EXPORT CSV
# ==========================================================

df = pd.DataFrame(rows)

df.to_csv(
    OUTPUT_CSV,
    index=False
)

print("\nDynamic feature file created:")
print(OUTPUT_CSV)

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())
# ==========================================================
# GRAPH ENTITY EXTRACTION
# ==========================================================

# ==========================================================
# ENTITY CLEANERS
# ==========================================================

def extract_process_names(processes):

    names = []

    for p in processes or []:

        if isinstance(p, dict):

            name = (
                p.get("process_name")
                or p.get("name")
                or p.get("image")
                or p.get("file")
            )

            if name:
                names.append(str(name))

        elif isinstance(p, str):

            names.append(p)

    return sorted(set(names))


def extract_strings(items, possible_keys):

    output = []

    for item in items or []:

        if isinstance(item, str):

            output.append(item)
            continue

        if isinstance(item, dict):

            for key in possible_keys:

                value = item.get(key)

                if value:

                    output.append(str(value))
                    break

    return sorted(set(output))


graph_entities = []

for report_file in tqdm(json_files, desc="Extracting Graph Entities"):

    try:

        report = load_report(report_file)

        data = report.get("data") or {}

        entity = {

            "sha256": get_sha256(report_file),

            "family": get_family(report_file),

            "processes": extract_process_names(
                data.get("processes_created", [])
            ),

            "files": extract_strings(
                data.get("files_written", []),
                ["path", "file", "name"]
            ),

            "registry": extract_strings(
                data.get("registry_keys_set", []),
                ["key", "path", "name"]
            ),

            "dns": extract_strings(
                data.get("dns_lookups", []),
                ["hostname", "domain", "host"]
            ),

            "ips": extract_strings(
                data.get("ip_traffic", []),
                ["destination_ip", "ip", "host"]
            ),

            "mitre": extract_strings(
                data.get("mitre_attack_techniques", []),
                ["id", "technique_id"]
            ),

            "commands": extract_strings(
                data.get("command_executions", []),
                ["command", "cmd"]
            ),

            "modules": extract_strings(
                data.get("modules_loaded", []),
                ["module", "path", "name"]
            )

        }

        graph_entities.append(entity)

    except Exception as e:

        print(f"[ENTITY ERROR] {report_file.name}: {e}")
# ==========================================================
# SAVE GRAPH ENTITIES
# ==========================================================

with open(GRAPH_JSON, "w") as f:

    json.dump(graph_entities, f, indent=2)

print("\nGraph entities saved:")
print(GRAPH_JSON)

print(f"\nGraph Samples : {len(graph_entities)}")
