#!/usr/bin/env python3
"""Build privacy-aware static web assets from validated curated outputs."""

import csv
import json
from pathlib import Path

from prepare_accessibility import weighted_quantile

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps/web"
PUBLIC = WEB / "public/data"
DATA = WEB / "src/data"
ISLANDS = {
    "el-hierro": ("El Hierro", "el-hierro"),
    "la-gomera": ("La Gomera", "la-gomera"),
    "la-palma": ("La Palma", "la-palma"),
    "tenerife": ("Tenerife", "tenerife"),
    "gran-canaria": ("Gran Canaria", "gran-canaria"),
    "fuerteventura": ("Fuerteventura", "fuerteventura"),
    "lanzarote": ("Lanzarote", "lanzarote"),
}
SIAP_CODES = {"ES703": "el-hierro", "ES706": "la-gomera", "ES707": "la-palma",
              "ES709": "tenerife", "ES705": "gran-canaria", "ES704": "fuerteventura",
              "ES708": "lanzarote"}


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def number(value):
    if value in (None, ""):
        return None
    parsed = float(value)
    return int(parsed) if parsed.is_integer() else parsed


def clean_row(row):
    return {key: number(value) if key not in {"island_id", "municipality_id",
            "municipality_name", "publication_status", "publication_reason"} else value
            for key, value in row.items()}


def band(row):
    status = row["routing_status"]
    if status != "routed":
        return status
    minutes = float(row["travel_minutes"])
    if minutes < 5:
        return "under_5"
    if minutes < 10:
        return "5_to_under_10"
    if minutes < 15:
        return "10_to_under_15"
    if minutes < 20:
        return "15_to_under_20"
    if minutes < 30:
        return "20_to_under_30"
    return "30_or_more"


def pediatricians():
    output = {}
    for row in csv_rows(ROOT / "docs/evidence/siap_professionals.csv"):
        if (row["TIME_PERIOD_CODE"] == "2024"
                and row["TIPO_PROFESIONAL_ATENCION_PRIMARIA_CODE"] == "PEDIATRIA_AP"
                and row["LUGAR_CONSULTA_CODE"] == "_T"
                and row["MEDIDAS_CODE"] == "NUMERO_PROFESIONALES_AP"
                and row["TERRITORIO_CODE"] in SIAP_CODES):
            output[SIAP_CODES[row["TERRITORIO_CODE"]]] = int(row["OBS_VALUE"])
    return output


def main():
    PUBLIC.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    cells = csv_rows(ROOT / "data/curated/pediatric_accessibility_2024.csv")
    islands = csv_rows(ROOT / "data/curated/accessibility_by_island_2024.csv")
    municipalities = csv_rows(ROOT / "data/curated/accessibility_by_municipality_2024.csv")
    facilities = csv_rows(ROOT / "data/curated/pediatric_facilities.csv")
    raw_grid = json.loads((ROOT / "data/raw/child_population_grid_2024.geojson").read_text())
    raw_municipalities = json.loads(
        (ROOT / "data/raw/municipios_desde2007_generalizada_20170101.geojson").read_text())
    cell_by_id = {row["grid_id"]: row for row in cells}
    facility_by_id = {row["facility_id"]: row for row in facilities}
    municipality_by_id = {(row["island_id"], row["municipality_id"]): row
                          for row in municipalities}

    grid_features = []
    for feature in raw_grid["features"]:
        row = cell_by_id[feature["properties"]["geocode"]]
        if int(row["children_0_14"]) == 0 and row["routing_status"] == "routed":
            continue
        facility = facility_by_id.get(row["nearest_facility_id"])
        grid_features.append({
            "type": "Feature", "geometry": feature["geometry"],
            "properties": {
                "grid_id": row["grid_id"], "island_id": row["island_id"],
                "municipality_id": row["municipality_id"], "band": band(row),
                "routing_status": row["routing_status"],
                "nearest_facility_name": facility["name"] if facility else None,
                "distance_km": round(float(row["travel_distance_m"]) / 1000, 1)
                               if row["travel_distance_m"] else None,
                "source_period": 2024,
            }})
    (PUBLIC / "accessibility-grid.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": grid_features},
        ensure_ascii=False, separators=(",", ":")))

    municipality_features = []
    for feature in raw_municipalities["features"]:
        props = feature["properties"]
        island_id = next(key for code, key in SIAP_CODES.items() if code == props["gcd_isla"])
        row = municipality_by_id[(island_id, props["geocode"])]
        public = row["publication_status"] == "publishable"
        metrics = clean_row(row) if public else {
            "island_id": island_id, "municipality_id": props["geocode"],
            "municipality_name": props["etiqueta"], "publication_status": "not_publishable",
            "publication_reason": row["publication_reason"]}
        municipality_features.append({"type": "Feature", "geometry": feature["geometry"],
                                      "properties": metrics})
    (PUBLIC / "municipalities.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": municipality_features},
        ensure_ascii=False, separators=(",", ":")))

    eligible_facilities = [row for row in facilities if row["routing_eligible_pediatric_ap"] == "true"]
    facility_features = [{"type": "Feature",
                          "geometry": {"type": "Point", "coordinates": [float(row["longitude"]), float(row["latitude"])]},
                          "properties": {"facility_id": row["facility_id"], "name": row["name"],
                                         "island_id": row["island_id"], "status": "VERIFIED"}}
                         for row in eligible_facilities]
    (PUBLIC / "facilities.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": facility_features},
        ensure_ascii=False, separators=(",", ":")))

    pediatrician_counts = pediatricians()
    island_profiles = []
    for row in islands:
        profile = clean_row(row)
        name, slug = ISLANDS[row["island_id"]]
        profile.update(name=name, slug=slug, pediatricians_ap_2024=pediatrician_counts[row["island_id"]])
        profile["pct_under_15_total"] = round(sum(float(row[key]) for key in (
            "pct_under_5_total", "pct_5_to_under_10_total", "pct_10_to_under_15_total")), 2)
        profile["pct_20_or_more_total"] = round(float(row["pct_20_to_under_30_total"])
                                                   + float(row["pct_30_or_more_total"]), 2)
        island_profiles.append(profile)
    municipal_profiles = []
    for row in municipalities:
        profile = clean_row(row)
        profile["slug"] = row["municipality_id"].lower()
        if row["publication_status"] != "publishable":
            profile = {key: profile[key] for key in ("island_id", "municipality_id",
                       "municipality_name", "publication_status", "publication_reason", "slug")}
        else:
            profile["pct_under_15_total"] = round(sum(float(row[key]) for key in (
                "pct_under_5_total", "pct_5_to_under_10_total", "pct_10_to_under_15_total")), 2)
            profile["pct_20_or_more_total"] = round(float(row["pct_20_to_under_30_total"])
                                                       + float(row["pct_30_or_more_total"]), 2)
        municipal_profiles.append(profile)

    routed = [row for row in cells if row["routing_status"] == "routed"]
    pairs = [(float(row["travel_minutes"]), int(row["children_0_14"])) for row in routed]
    total = sum(int(row["children_0_14"]) for row in cells)
    under_15 = sum(int(row["children_0_14"]) for row in routed if float(row["travel_minutes"]) < 15)
    over_30 = sum(int(row["children_0_14"]) for row in routed if float(row["travel_minutes"]) >= 30)
    profiles = {
        "summary": {"children_0_14": total, "eligible_pediatric_facilities": len(eligible_facilities),
                    "median_travel_minutes": weighted_quantile(pairs, .5),
                    "pct_under_15_total": round(100 * under_15 / total, 2),
                    "pct_30_or_more_total": round(100 * over_30 / total, 2),
                    "pediatricians_ap_2024": sum(pediatrician_counts.values())},
        "islands": island_profiles,
        "municipalities": municipal_profiles,
        "metadata": {"source_period": 2024, "catalog_date": "2026-09-27",
                     "engine": "OSRM", "engine_version": "5.27.1",
                     "osm_snapshot": "canary-islands-260926", "status": "RC1"},
    }
    (DATA / "profiles.json").write_text(json.dumps(profiles, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"map_features": len(grid_features), "islands": len(island_profiles),
                      "municipalities": len(municipal_profiles), "facilities": len(facility_features)}, indent=2))


if __name__ == "__main__":
    main()
