"""Create Phase 6B web payloads."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT / "data/curated" / name).open() as handle:
        return list(csv.DictReader(handle))


def write(name, payload):
    path = ROOT / "apps/web/src/data" / name
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


bdcap = read("bdcap_pediatric_indicators.csv")
screening = read("neonatal_screening_indicators.csv")
surveys = read("adolescent_survey_indicators_phase6b.csv")
write("phase6b-bdcap.json", bdcap)
write("phase6b-screening.json", screening)
write("phase6b-surveys.json", surveys)
print({"bdcap": len(bdcap), "screening": len(screening), "surveys": len(surveys)})
