"""
VirusTotal Behaviour Downloader
Production Version

Author: Kavya Mishra
Project: Hybrid Static + Dynamic Ransomware Detection
"""

import json
import time
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

from config import (
    VT_API_KEYS,
    REQUEST_DELAY,
    MAX_REQUESTS_PER_DAY,
)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_CSV = BASE_DIR / "subset" / "family_subset.csv"

REPORT_ROOT = BASE_DIR / "reports" / "virustotal"

LOG_DIR = BASE_DIR / "logs"

PROGRESS_FILE = BASE_DIR / "progress.json"

SUCCESS_LOG = LOG_DIR / "success.csv"
FAILED_LOG = LOG_DIR / "failed.csv"
MISSING_LOG = LOG_DIR / "missing.csv"

REPORT_ROOT.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# API CONFIG
# ==========================================================

BASE_URL = "https://www.virustotal.com/api/v3/files"

CURRENT_API = 0

API_USAGE = [0] * len(VT_API_KEYS)

HEADERS = {
    "x-apikey": VT_API_KEYS[CURRENT_API]
}


def rotate_api():

    global CURRENT_API
    global HEADERS

    CURRENT_API += 1

    if CURRENT_API >= len(VT_API_KEYS):

        return False

    HEADERS = {
        "x-apikey": VT_API_KEYS[CURRENT_API]
    }

    print("\n" + "=" * 70)
    print(f"Switched To API #{CURRENT_API + 1}")
    print("=" * 70)

    return True


# ==========================================================
# LOAD DATASET
# ==========================================================

print("=" * 70)
print("VirusTotal Behaviour Downloader")
print("=" * 70)

df = pd.read_csv(
    INPUT_CSV,
    low_memory=False
)

print(f"Samples Loaded      : {len(df)}")
print(f"Available API Keys  : {len(VT_API_KEYS)}")

# ==========================================================
# RESUME SUPPORT
# ==========================================================

completed = set()

if PROGRESS_FILE.exists():

    try:

        completed = set(
            json.loads(
                PROGRESS_FILE.read_text()
            )
        )

    except Exception:

        completed = set()

print(f"Already Downloaded  : {len(completed)}")

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def append_csv(
    path: Path,
    family: str,
    sha256: str,
    status: str,
):

    if not path.exists():

        with open(path, "w") as f:

            f.write(
                "family,sha256,status\n"
            )

    with open(path, "a") as f:

        f.write(
            f"{family},{sha256},{status}\n"
        )


def save_progress():

    with open(PROGRESS_FILE, "w") as f:

        json.dump(
            sorted(list(completed)),
            f,
            indent=2
        )


def build_output_path(
    family: str,
    sha256: str
):

    folder = REPORT_ROOT / family

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder / f"{sha256}.json"


def already_downloaded(
    outfile: Path
):

    return outfile.exists()
# ==========================================================
# VIRUSTOTAL CLIENT
# ==========================================================

def download_behavior(sha256: str):

    """
    Downloads VirusTotal Behaviour Report

    Returns
    -------
    (True, json)
    (False, "NOT_FOUND")
    (False, "RATE_LIMIT")
    (False, "FAILED")
    """

    global CURRENT_API
    global API_USAGE

    url = f"{BASE_URL}/{sha256}/behaviour_summary"

    api_attempts = 0

    while api_attempts < len(VT_API_KEYS):

        for attempt in range(1, 4):

            try:

                response = requests.get(
                    url,
                    headers=HEADERS,
                    timeout=120,
                )

                API_USAGE[CURRENT_API] += 1

                if response.status_code == 200:

                    return True, response.json()

                elif response.status_code == 404:

                    return False, "NOT_FOUND"

                elif response.status_code == 429:

                    print(
                        f"\n[RATE LIMIT]"
                    )

                    print(
                        f"API #{CURRENT_API + 1} exhausted."
                    )

                    api_attempts += 1

                    switched = rotate_api()

                    if not switched:

                        print(
                            "\nAll API Keys Exhausted."
                        )

                        return False, "RATE_LIMIT"

                    break

                else:

                    print(
                        f"[HTTP {response.status_code}] "
                        f"{sha256[:12]} "
                        f"(Attempt {attempt}/3)"
                    )

            except requests.exceptions.Timeout:

                print(
                    f"[TIMEOUT] "
                    f"{sha256[:12]} "
                    f"(Attempt {attempt}/3)"
                )

            except requests.exceptions.ConnectionError:

                print(
                    f"[CONNECTION ERROR] "
                    f"{sha256[:12]} "
                    f"(Attempt {attempt}/3)"
                )

            except Exception as e:

                print(
                    f"[ERROR] "
                    f"{sha256[:12]} : {e}"
                )

            time.sleep(5)

    return False, "FAILED"
# ==========================================================
# SAVE REPORT
# ==========================================================

def save_report(
    outfile: Path,
    report: dict
):

    with open(outfile, "w") as f:

        json.dump(
            report,
            f,
            indent=2
        )


# ==========================================================
# PROCESS ONE SAMPLE
# ==========================================================

def process_sample(sample):

    sha256 = sample["sha256"]
    family = sample["family"]

    outfile = build_output_path(
        family,
        sha256
    )

    # ------------------------------------------
    # Already completed
    # ------------------------------------------

    if sha256 in completed:

        return "SKIPPED"

    # ------------------------------------------
    # JSON already exists
    # ------------------------------------------

    if already_downloaded(outfile):

        completed.add(sha256)

        save_progress()

        return "SKIPPED"

    # ------------------------------------------
    # Download Behaviour Report
    # ------------------------------------------

    success, result = download_behavior(
        sha256
    )

    # ------------------------------------------
    # SUCCESS
    # ------------------------------------------

    if success:

        save_report(
            outfile,
            result
        )

        completed.add(sha256)

        save_progress()

        append_csv(
            SUCCESS_LOG,
            family,
            sha256,
            "SUCCESS",
        )

        return "SUCCESS"

    # ------------------------------------------
    # NOT FOUND
    # ------------------------------------------

    if result == "NOT_FOUND":

        append_csv(
            MISSING_LOG,
            family,
            sha256,
            "MISSING",
        )

        return "MISSING"

    # ------------------------------------------
    # RATE LIMIT
    # ------------------------------------------

    if result == "RATE_LIMIT":

        return "RATE_LIMIT"

    # ------------------------------------------
    # FAILED
    # ------------------------------------------

    append_csv(
        FAILED_LOG,
        family,
        sha256,
        "FAILED",
    )

    return "FAILED"
# ==========================================================
# MAIN DOWNLOAD LOOP
# ==========================================================

print("\nStarting VirusTotal Behaviour Downloads...\n")

today_downloads = 0

success_count = 0
missing_count = 0
failed_count = 0
skipped_count = 0

try:

    for _, sample in tqdm(

        df.iterrows(),

        total=len(df),

        desc="Downloading Reports",

        unit="sample",

    ):

        if today_downloads >= MAX_REQUESTS_PER_DAY * len(VT_API_KEYS):

            print("\nDaily API quota exhausted.")

            break

        status = process_sample(sample)

        # --------------------------------------
        # SUCCESS
        # --------------------------------------

        if status == "SUCCESS":

            success_count += 1

            today_downloads += 1

            time.sleep(REQUEST_DELAY)

        # --------------------------------------
        # MISSING
        # --------------------------------------

        elif status == "MISSING":

            missing_count += 1

            today_downloads += 1

            time.sleep(REQUEST_DELAY)

        # --------------------------------------
        # FAILED
        # --------------------------------------

        elif status == "FAILED":

            failed_count += 1

        # --------------------------------------
        # SKIPPED
        # --------------------------------------

        elif status == "SKIPPED":

            skipped_count += 1

        # --------------------------------------
        # RATE LIMIT
        # --------------------------------------

        elif status == "RATE_LIMIT":

            print("\nAll VirusTotal API Keys Exhausted.")

            break

except KeyboardInterrupt:

    print("\nInterrupted By User.")

    print("Progress Saved.")

finally:

    print()

    print("=" * 70)

    print("DOWNLOAD SUMMARY")

    print("=" * 70)

    print(f"Total Samples        : {len(df)}")

    print(f"Downloaded Today     : {today_downloads}")

    print(f"Successful           : {success_count}")

    print(f"Missing Reports      : {missing_count}")

    print(f"Failed               : {failed_count}")

    print(f"Skipped              : {skipped_count}")

    print(f"Completed Overall    : {len(completed)}")

    print()

    print("-" * 70)

    print("API USAGE")

    print("-" * 70)

    for i, count in enumerate(API_USAGE):

        print(f"API #{i+1:<2} : {count} requests")

    print("=" * 70)
