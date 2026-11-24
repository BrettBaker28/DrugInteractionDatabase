"""Drug-name autocomplete.

suggest("warf") returns the drug names that could complete what the user has
typed so far. Names come from interactions/data/drug_names.csv, the
spreadsheet of all available drugs (rebuilt by
python_programs/build_drug_list.py).
"""

import csv
from functools import lru_cache
from pathlib import Path

DRUG_LIST_PATH = Path(__file__).resolve().parent / "data" / "drug_names.csv"
DEFAULT_LIMIT = 10


@lru_cache(maxsize=None)
def load_drug_names(path=DRUG_LIST_PATH):
    """Read the drug spreadsheet once and return its names as a tuple."""
    with open(path, newline="", encoding="utf-8") as f:
        return tuple(row["Name"] for row in csv.DictReader(f) if row["Name"])


def suggest(query, names=None, limit=DEFAULT_LIMIT):
    """Return up to `limit` drug names matching `query`.

    Matching ignores case and surrounding spaces. Names that start with the
    query come first, then names that contain it elsewhere; each group is
    alphabetical. An empty query, or one that matches nothing, returns [].
    """
    if not isinstance(query, str):
        return []
    query = query.strip().lower()
    if not query or limit <= 0:
        return []
    if names is None:
        names = load_drug_names()

    starts_with = []
    contains = []
    for name in names:
        lowered = name.lower()
        if lowered.startswith(query):
            starts_with.append(name)
        elif query in lowered:
            contains.append(name)

    starts_with.sort(key=str.lower)
    contains.sort(key=str.lower)
    return (starts_with + contains)[:limit]
