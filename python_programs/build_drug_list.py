"""Build the spreadsheet of all available drugs used by the autocomplete.

Reads the DDInter severity spreadsheet (one row per drug pair) and writes
interactions/data/drug_names.csv with one row per unique drug.

Run from the repository root after unzipping interaction_csv.zip:

    python python_programs/build_drug_list.py
"""

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT / "interaction_csv" / "interaction_csv" / "severity.csv"
OUTPUT = REPO_ROOT / "interactions" / "data" / "drug_names.csv"


def collect_drugs(source):
    """Return {ddinter_id: name} for every drug in either column of the file."""
    drugs = {}
    with open(source, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            drugs[row["DDInterID_A"]] = row["Drug_A"].strip()
            drugs[row["DDInterID_B"]] = row["Drug_B"].strip()
    return drugs


def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    drugs = collect_drugs(source)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["DDInterID", "Name"])
        for ddinter_id, name in sorted(drugs.items(), key=lambda d: d[1].lower()):
            writer.writerow([ddinter_id, name])
    print(f"Wrote {len(drugs)} drugs to {OUTPUT}")


if __name__ == "__main__":
    main()
