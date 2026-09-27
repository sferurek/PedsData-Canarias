"""Read-only recheck of the official grid. No application or production ingestion."""
from pathlib import Path
from urllib.request import urlopen
from collections import defaultdict
import json

root = Path(__file__).resolve().parents[1]
audit = json.loads((root / "docs/evidence/api_audit.json").read_text())
record = next(x for x in audit if x["id"] == "grid")
with urlopen(record["url"], timeout=90) as response:
    data = json.load(response)
summary = defaultdict(lambda: {"cells": 0, "sum_0_14": 0, "null_0_14": 0, "null_0_17": 0})
for feature in data["features"]:
    props = feature["properties"]
    item = summary[props["isla"]]
    item["cells"] += 1
    item["sum_0_14"] += props["poblacion_00a14"] or 0
    item["null_0_14"] += props["poblacion_00a14"] is None
    item["null_0_17"] += props["poblacion_00a17"] is None
assert set(summary) == {"ES703", "ES704", "ES705", "ES706", "ES707", "ES708", "ES709"}
assert len(data["features"]) == data["numberMatched"], "Incomplete WFS response; pagination required"
print(json.dumps(summary, ensure_ascii=False, indent=2))
