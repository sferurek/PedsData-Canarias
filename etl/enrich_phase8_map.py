#!/usr/bin/env python3
import json
from pathlib import Path
from csv import DictReader
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/"apps/web/public/data/municipalities.geojson"
source=json.loads(path.read_text(encoding="utf-8"))
with (ROOT/"data/curated/territorial_context.csv").open(newline="",encoding="utf-8") as handle:
 context={row["municipality_id"]:row for row in DictReader(handle)}
fields=(("urban_centre","degurba_urban_centre_children_pct"),("urban_cluster","degurba_urban_cluster_children_pct"),("rural","degurba_rural_children_pct"))
for feature in source["features"]:
 row=context.get(feature["properties"]["municipality_id"])
 if row:
  feature["properties"]["degurba_class"]=max(fields,key=lambda item:float(row[item[1]]))[0]
  feature["properties"]["degurba_period"]=2021
path.write_text(json.dumps(source,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print("Enriched",len(source["features"]),"municipalities with dominant DEGURBA category")

