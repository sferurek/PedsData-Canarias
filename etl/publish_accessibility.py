#!/usr/bin/env python3
"""Validate Phase 2 staging and promote defensible accessibility outputs."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from shapely.geometry import Point, shape

from prepare_accessibility import ISLAND_CODES, terrestrial_component, weighted_quantile

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "data/staging/pediatric_accessibility_2024.csv"
GRID = ROOT / "data/raw/child_population_grid_2024.geojson"
FACILITIES = ROOT / "data/curated/pediatric_facilities.csv"
MUNICIPALITIES = ROOT / "data/raw/municipios_desde2007_generalizada_20170101.geojson"
GRAPH_MANIFEST = ROOT / "data/manifests/osrm_canarias_graph.json"
OSM_MANIFEST = ROOT / "data/manifests/osm_canarias_snapshot.json"
PIPELINE_MANIFEST = ROOT / "data/manifests/accessibility_pipeline_benchmark.json"
PUBLICATION_MANIFEST = ROOT / "data/manifests/accessibility_publication_manifest.json"
QA_JSON = ROOT / "data/manifests/accessibility_qa.json"
CELL_OUTPUT = ROOT / "data/curated/pediatric_accessibility_2024.csv"
ISLAND_OUTPUT = ROOT / "data/curated/accessibility_by_island_2024.csv"
MUNICIPAL_OUTPUT = ROOT / "data/curated/accessibility_by_municipality_2024.csv"
EXPECTED_STATUS = {"routed": 13256, "requires_interisland_transfer": 20,
                   "no_route": 0, "not_evaluated": 1}
CELL_FIELDS = ("grid_id", "island_id", "municipality_id", "children_0_14",
               "nearest_facility_id", "travel_seconds", "travel_minutes",
               "travel_distance_m", "routing_status", "engine", "engine_version",
               "graph_snapshot", "osm_snapshot", "source_period")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict], fieldnames=None) -> None:
    names = fieldnames or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


def pct(numerator: int, denominator: int):
    return round(100 * numerator / denominator, 2) if denominator else None


def official_municipality_id(value: str) -> str:
    return value[:5] if len(value) == 6 and value.isdigit() else value


def qa_staging(rows, grid, facilities, graph, pipeline):
    failures = []
    grid_by_id = {feature["properties"]["geocode"]: feature for feature in grid["features"]}
    ids = [row["origin_id"] for row in rows]
    if len(rows) != 13277:
        failures.append(f"total_cells={len(rows)}")
    if len(ids) != len(set(ids)):
        failures.append("duplicate_grid_id")
    if set(ids) != set(grid_by_id):
        failures.append("grid_set_mismatch")
    raw_population = sum(int(feature["properties"]["poblacion_00a14"])
                         for feature in grid["features"])
    staged_population = sum(int(row["child_population_0_14"]) for row in rows)
    if staged_population != raw_population:
        failures.append("population_not_preserved")
    eligible = {row["facility_id"]: row for row in facilities
                if row["verification_status"] == "VERIFIED"
                and row["routing_eligible_pediatric_ap"] == "true"
                and row["geocoding_match_status"] == "official_registry_point"}
    status_counts = Counter(row["routing_status"] for row in rows)
    status_counts.update({key: 0 for key in EXPECTED_STATUS})
    if any(status_counts[key] != value for key, value in EXPECTED_STATUS.items()):
        failures.append("routing_status_counts")
    islands = Counter()
    for row in rows:
        raw = grid_by_id.get(row["origin_id"])
        if raw is None:
            continue
        expected_island = ISLAND_CODES[raw["properties"]["isla"]]
        if row["island_id"] != expected_island:
            failures.append(f"wrong_island:{row['origin_id']}")
        if int(row["child_population_0_14"]) != int(raw["properties"]["poblacion_00a14"]):
            failures.append(f"wrong_population:{row['origin_id']}")
        islands[row["island_id"]] += 1
        routed = row["routing_status"] == "routed"
        if routed:
            if float(row["travel_seconds"]) <= 0 or float(row["travel_distance_m"]) <= 0:
                failures.append(f"nonpositive_route:{row['origin_id']}")
            facility = eligible.get(row["nearest_facility_id"])
            if facility is None:
                failures.append(f"ineligible_destination:{row['origin_id']}")
            elif facility["island_id"] != row["terrestrial_component"]:
                failures.append(f"cross_component:{row['origin_id']}")
        elif row["travel_seconds"] or row["travel_distance_m"] or row["nearest_facility_id"]:
            failures.append(f"nonroute_has_values:{row['origin_id']}")
        if row["engine_version"] != graph["engine_version"]:
            failures.append(f"engine_version:{row['origin_id']}")
        if row["graph_snapshot"] != graph["graph_bundle_sha256"]:
            failures.append(f"graph_snapshot:{row['origin_id']}")
    if set(islands) != set(ISLAND_CODES.values()):
        failures.append("seven_islands")
    if sha256(STAGING) != pipeline["cell_result_sha256"]:
        failures.append("staging_checksum")
    return {
        "passed": not failures,
        "failures": failures[:100],
        "total_cells": len(rows),
        "unique_cells": len(set(ids)),
        "population_0_14_raw": raw_population,
        "population_0_14_staging": staged_population,
        "routing_status_counts": {key: status_counts[key] for key in EXPECTED_STATUS},
        "island_cell_counts": dict(sorted(islands.items())),
        "eligible_destination_count": len(eligible),
        "staging_sha256": sha256(STAGING),
    }


def promote_cells(rows, graph, osm):
    output = []
    for row in rows:
        seconds = float(row["travel_seconds"]) if row["travel_seconds"] else None
        distance = float(row["travel_distance_m"]) if row["travel_distance_m"] else None
        output.append({
            "grid_id": row["origin_id"], "island_id": row["island_id"],
            "municipality_id": row["municipality_id"],
            "children_0_14": int(row["child_population_0_14"]),
            "nearest_facility_id": row["nearest_facility_id"],
            "travel_seconds": round(seconds, 1) if seconds is not None else "",
            "travel_minutes": round(seconds / 60, 2) if seconds is not None else "",
            "travel_distance_m": round(distance, 1) if distance is not None else "",
            "routing_status": row["routing_status"], "engine": graph["engine"],
            "engine_version": graph["engine_version"],
            "graph_snapshot": graph["graph_bundle_sha256"],
            "osm_snapshot": osm["extract_version"], "source_period": "2024",
        })
    return sorted(output, key=lambda item: item["grid_id"])


def band(seconds: float) -> str:
    if seconds < 300:
        return "under_5"
    if seconds < 600:
        return "5_to_under_10"
    if seconds < 900:
        return "10_to_under_15"
    if seconds < 1200:
        return "15_to_under_20"
    if seconds < 1800:
        return "20_to_under_30"
    return "30_or_more"


def municipality_metadata():
    collection = json.loads(MUNICIPALITIES.read_text(encoding="utf-8"))
    result = {}
    for feature in collection["features"]:
        props = feature["properties"]
        result[props["geocode"]] = {
            "municipality_name": props["etiqueta"],
            "geometry_valid": shape(feature["geometry"]).is_valid,
            "island_id": ISLAND_CODES[props["gcd_isla"]],
            "geometry": shape(feature["geometry"]),
        }
    return result


def facility_counts(facilities, municipality_ids, municipal_meta):
    islands, municipalities = Counter(), Counter()
    base_lookup = defaultdict(list)
    for municipality_id in municipality_ids:
        base_lookup[municipality_id.split("_")[0]].append(municipality_id)
    for row in facilities:
        if not (row["verification_status"] == "VERIFIED"
                and row["routing_eligible_pediatric_ap"] == "true"
                and row["geocoding_match_status"] == "official_registry_point"):
            continue
        islands[row["island_id"]] += 1
        base = official_municipality_id(row["municipality_id"])
        candidates = base_lookup.get(base, [])
        if len(candidates) != 1:
            point = Point(float(row["longitude"]), float(row["latitude"]))
            candidates = [identifier for identifier, meta in municipal_meta.items()
                          if meta["island_id"] == row["island_id"]
                          and meta["geometry"].covers(point)]
        if len(candidates) == 1:
            municipalities[(row["island_id"], candidates[0])] += 1
    return islands, municipalities


def aggregate(rows, keys, facilities, municipal_meta):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    island_facilities, municipal_facilities = facility_counts(
        facilities, {row["municipality_id"] for row in rows}, municipal_meta)
    output = []
    bands = ("under_5", "5_to_under_10", "10_to_under_15",
             "15_to_under_20", "20_to_under_30", "30_or_more")
    for group, items in sorted(grouped.items()):
        record = dict(zip(keys, group))
        total = sum(int(row["children_0_14"]) for row in items)
        by_status = Counter()
        by_band = Counter()
        quantile_pairs = []
        populated_cells = 0
        for row in items:
            children = int(row["children_0_14"])
            populated_cells += children > 0
            by_status[row["routing_status"]] += children
            if row["routing_status"] == "routed":
                seconds = float(row["travel_seconds"])
                by_band[band(seconds)] += children
                quantile_pairs.append((seconds / 60, children))
        evaluable = by_status["routed"] + by_status["no_route"]
        routed = by_status["routed"]
        if keys == ("island_id",):
            count = island_facilities[group[0]]
            status = "validated"
            reason = ""
        else:
            count = municipal_facilities[(group[0], group[1])]
            meta = municipal_meta.get(group[1], {})
            valid = bool(meta.get("geometry_valid"))
            status = "publishable" if valid and total >= 100 and populated_cells >= 5 else "not_publishable"
            reasons = []
            if not valid:
                reasons.append("invalid_or_missing_geometry")
            if total < 100:
                reasons.append("population_below_100")
            if populated_cells < 5:
                reasons.append("fewer_than_5_populated_cells")
            reason = "|".join(reasons)
            record["municipality_name"] = meta.get("municipality_name", "")
        record.update({
            "publication_status": status, "publication_reason": reason,
            "children_0_14": total, "population_total": total,
            "population_evaluable": evaluable, "population_routed": routed,
            "population_requires_interisland_transfer": by_status["requires_interisland_transfer"],
            "population_no_route": by_status["no_route"],
            "population_not_evaluated": by_status["not_evaluated"],
            "eligible_pediatric_facilities": count,
            "children_per_verified_pediatric_facility": round(total / count, 1) if count else "",
            "median_travel_minutes": weighted_quantile(quantile_pairs, 0.5),
            "p90_travel_minutes": weighted_quantile(quantile_pairs, 0.9),
        })
        for name in bands:
            value = by_band[name]
            record[f"children_{name}"] = value
            record[f"pct_{name}_total"] = pct(value, total)
            record[f"pct_{name}_evaluable"] = pct(value, evaluable)
        record["pct_requires_interisland_transfer_total"] = pct(
            by_status["requires_interisland_transfer"], total)
        record["pct_no_route_total"] = pct(by_status["no_route"], total)
        record["pct_not_evaluated_total"] = pct(by_status["not_evaluated"], total)
        output.append(record)
    return output


def main():
    staging = read_csv(STAGING)
    grid = json.loads(GRID.read_text(encoding="utf-8"))
    facilities = read_csv(FACILITIES)
    graph = json.loads(GRAPH_MANIFEST.read_text())
    osm = json.loads(OSM_MANIFEST.read_text())
    pipeline = json.loads(PIPELINE_MANIFEST.read_text())
    qa = qa_staging(staging, grid, facilities, graph, pipeline)
    QA_JSON.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n")
    if not qa["passed"]:
        raise SystemExit("Accessibility QA failed: " + ", ".join(qa["failures"]))
    cells = promote_cells(staging, graph, osm)
    municipal_meta = municipality_metadata()
    islands = aggregate(cells, ("island_id",), facilities, municipal_meta)
    municipalities = aggregate(cells, ("island_id", "municipality_id"), facilities, municipal_meta)
    write_csv(CELL_OUTPUT, cells, CELL_FIELDS)
    write_csv(ISLAND_OUTPUT, islands)
    write_csv(MUNICIPAL_OUTPUT, municipalities)
    manifest = {
        "publication_status": "validated_rc1", "calculated_at": datetime.now(timezone.utc).isoformat(),
        "source_period": "2024", "age_group_original": "0-14",
        "pipeline": "etl/prepare_accessibility.py + etl/publish_accessibility.py",
        "pipeline_sha256": {"prepare": sha256(ROOT / "etl/prepare_accessibility.py"),
                            "publish": sha256(Path(__file__))},
        "sources": {
            "istac_grid": {"url": "https://datos.canarias.es/catalogos/estadisticas/dataset/indicadores-demograficos-malla-de-250m-canarias-01-01-2024",
                           "sha256": sha256(GRID), "period": "2024"},
            "pediatric_facilities": {"path": "data/curated/pediatric_facilities.csv",
                                     "sha256": sha256(FACILITIES), "catalog_date": "2026-09-27"},
            "osm": {"source_url": osm["source_url"], "extract_version": osm["extract_version"],
                    "sha256": osm["checksum_sha256"], "license": osm["license"]},
            "routing": {"engine": graph["engine"], "version": graph["engine_version"],
                        "profile": graph["profile"], "graph_snapshot": graph["graph_bundle_sha256"]},
        },
        "qa": qa,
        "outputs": {
            "cells": {"path": str(CELL_OUTPUT.relative_to(ROOT)), "rows": len(cells), "sha256": sha256(CELL_OUTPUT)},
            "islands": {"path": str(ISLAND_OUTPUT.relative_to(ROOT)), "rows": len(islands), "sha256": sha256(ISLAND_OUTPUT)},
            "municipalities": {"path": str(MUNICIPAL_OUTPUT.relative_to(ROOT)), "rows": len(municipalities),
                               "publishable": sum(row["publication_status"] == "publishable" for row in municipalities),
                               "sha256": sha256(MUNICIPAL_OUTPUT)},
        },
        "zbs_aggregation_enabled": False,
        "privacy": {"cell_exact_children_visible_in_ui": False,
                    "municipality_minimum_population": 100,
                    "municipality_minimum_populated_cells": 5},
    }
    PUBLICATION_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"qa": qa, "outputs": manifest["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
