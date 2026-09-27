"""Offline integrity checks for the phase-0 discovery artifacts, not application tests."""
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REQUIRED = "PROJECT_VISION PEDIATRIC_DATA_INVENTORY PEDIATRIC_DATA_MATRIX ISLAND_COVERAGE_MATRIX PEDIATRIC_DATA_WISHLIST DATA_GAPS ARCHITECTURE DATA_MODEL MVP_PLAN RESEARCH_OPPORTUNITIES RISKS".split()
ISLANDS = {"ES703", "ES704", "ES705", "ES706", "ES707", "ES708", "ES709"}
for name in REQUIRED:
    assert (DOCS / (name + ".md")).stat().st_size > 200, name
matrix = (DOCS / "ISLAND_COVERAGE_MATRIX.md").read_text()
for name in ["El Hierro", "La Gomera", "La Palma", "Tenerife", "Gran Canaria", "Fuerteventura", "Lanzarote"]:
    assert name in matrix
allowed = {"COMPLETE", "PARTIAL", "NOT AVAILABLE", "NEEDS VALIDATION"}
rows = [line.split("|")[1:-1] for line in matrix.splitlines() if line.startswith("|")]
status_rows = [row for row in rows if len(row) == 8 and row[1] in allowed]
assert len(status_rows) == 19
assert all(set(row[1:]) <= allowed for row in status_rows)
audit = json.loads((DOCS / "evidence/api_audit.json").read_text())
for record in audit:
    if record["id"].startswith("siap_"):
        file = DOCS / "evidence" / (record["id"] + ".csv")
        assert hashlib.sha256(file.read_bytes()).hexdigest() == record["sha256"]
grid = next(record for record in audit if record["id"] == "grid")
assert set(grid["by_island"]) == ISLANDS
assert sum(v["cells"] for v in grid["by_island"].values()) == grid["numberMatched"] == 13277
assert all(v["null_0_14"] == 0 for v in grid["by_island"].values())
with (DOCS / "evidence/siap_professionals.csv").open() as handle:
    professionals = [row for row in csv.DictReader(handle) if row["TIME_PERIOD_CODE"] == "2024" and row["TIPO_PROFESIONAL_ATENCION_PRIMARIA_CODE"] == "PEDIATRIA_AP" and row["MEDIDAS_CODE"] == "NUMERO_PROFESIONALES_AP"]
insular = [row for row in professionals if row["TERRITORIO_CODE"] in ISLANDS]
assert len(insular) == 7 and {row["TERRITORIO_CODE"] for row in insular} == ISLANDS
assert sum(int(row["OBS_VALUE"]) for row in insular) == 318
print("PASS: 11 required documents; 19 coverage contracts; 7 islands; CSV hashes; grid count; 2024 AP staff total.")
