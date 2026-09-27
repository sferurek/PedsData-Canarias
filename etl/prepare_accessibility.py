#!/usr/bin/env python3
"""Prepare cell-level pediatric AP accessibility on the frozen local OSRM graph."""

import argparse
import csv
import hashlib
import json
import resource
import time
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import urlopen

from shapely.geometry import shape

ROOT = Path(__file__).resolve().parents[1]
ISLAND_CODES = {"ES703": "el-hierro", "ES706": "la-gomera", "ES707": "la-palma",
                "ES709": "tenerife", "ES705": "gran-canaria", "ES704": "fuerteventura",
                "ES708": "lanzarote"}
ISLANDS = tuple(ISLAND_CODES.values())
FIELDS = ("origin_id", "island_id", "municipality_id", "terrestrial_component",
          "child_population_0_14", "longitude", "latitude", "nearest_facility_id",
          "travel_seconds", "travel_distance_m", "routing_status", "engine_version",
          "graph_snapshot")


def terrestrial_component(island, lon, lat):
    if island == "lanzarote" and lat > 29.20 and lon > -13.65:
        return "la-graciosa"
    return island


def chunks(values, size):
    for index in range(0, len(values), size):
        yield values[index:index + size]


def load_origins(path):
    collection = json.loads(path.read_text(encoding="utf-8"))
    origins = []
    for feature in collection["features"]:
        props = feature["properties"]
        point = shape(feature["geometry"]).representative_point()
        island = ISLAND_CODES[props["isla"]]
        origins.append({"origin_id": props["geocode"], "island_id": island,
                        "municipality_id": str(props["municipio"]),
                        "terrestrial_component": terrestrial_component(island, point.x, point.y),
                        "child_population_0_14": int(props["poblacion_00a14"]),
                        "longitude": point.x, "latitude": point.y})
    return origins


def load_destinations(path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row["verification_status"] == "VERIFIED"
            and row["pediatrics_ap"] == "observed"
            and row["routing_eligible_pediatric_ap"] == "true"
            and row["geocoding_match_status"] == "official_registry_point"
            and row["latitude"] and row["longitude"]]


def table_request(base_url, origin_batch, destination_batch):
    points = origin_batch + destination_batch
    coords = ";".join(f"{p['longitude']},{p['latitude']}" for p in points)
    sources = ";".join(str(i) for i in range(len(origin_batch)))
    offset = len(origin_batch)
    destinations = ";".join(str(offset + i) for i in range(len(destination_batch)))
    url = (f"{base_url}/table/v1/driving/{coords}?sources={sources}"
           f"&destinations={destinations}&annotations=duration,distance")
    with urlopen(url, timeout=60) as response:
        return json.load(response)


def route_component(base_url, origins, destinations, origin_size, destination_size):
    best = {row["origin_id"]: None for row in origins}
    requests = failures = 0
    for origin_batch in chunks(origins, origin_size):
        for destination_batch in chunks(destinations, destination_size):
            requests += 1
            try:
                payload = table_request(base_url, origin_batch, destination_batch)
                if payload.get("code") != "Ok":
                    raise ValueError(payload.get("code"))
            except Exception:
                failures += 1
                continue
            for oi, origin in enumerate(origin_batch):
                for di, facility in enumerate(destination_batch):
                    duration = payload["durations"][oi][di]
                    distance = payload["distances"][oi][di]
                    if duration is None or distance is None:
                        continue
                    candidate = (duration, distance, facility["facility_id"])
                    current = best[origin["origin_id"]]
                    if current is None or candidate[0] < current[0]:
                        best[origin["origin_id"]] = candidate
    return best, requests, failures


def weighted_quantile(pairs, quantile):
    pairs = sorted((value, weight) for value, weight in pairs if weight > 0)
    total = sum(weight for _, weight in pairs)
    if not total:
        return None
    target = total * quantile
    cumulative = 0
    for value, weight in pairs:
        cumulative += weight
        if cumulative >= target:
            return round(value, 1)


def aggregate(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    output = []
    for group, items in sorted(grouped.items()):
        routed = [r for r in items if r["routing_status"] == "routed"]
        population = sum(int(r["child_population_0_14"]) for r in items)
        evaluated = sum(int(r["child_population_0_14"]) for r in routed)
        record = dict(zip(keys, group))
        record.update(population_0_14=population, population_evaluated=evaluated)
        for minutes in (5, 10, 15, 20, 30):
            within = sum(int(r["child_population_0_14"]) for r in routed
                         if float(r["travel_seconds"]) < minutes * 60)
            record[f"pct_lt_{minutes}_min"] = round(100 * within / evaluated, 2) if evaluated else None
        over = sum(int(r["child_population_0_14"]) for r in routed
                   if float(r["travel_seconds"]) >= 1800)
        record["pct_ge_30_min"] = round(100 * over / evaluated, 2) if evaluated else None
        pairs = [(float(r["travel_seconds"]), int(r["child_population_0_14"])) for r in routed]
        record["median_seconds"] = weighted_quantile(pairs, 0.5)
        record["p90_seconds"] = weighted_quantile(pairs, 0.9)
        record["population_no_route"] = sum(int(r["child_population_0_14"]) for r in items
                                             if r["routing_status"] == "no_route")
        record["population_not_evaluable"] = population - evaluated - record["population_no_route"]
        output.append(record)
    return output


def write_csv(path, rows, fieldnames=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fieldnames or list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:55000")
    parser.add_argument("--origin-batch", type=int, default=40)
    parser.add_argument("--destination-batch", type=int, default=40)
    args = parser.parse_args()
    started = time.monotonic()
    origins = load_origins(ROOT / "data/raw/child_population_grid_2024.geojson")
    facilities = load_destinations(ROOT / "data/curated/pediatric_facilities.csv")
    graph = json.loads((ROOT / "data/manifests/osrm_canarias_graph.json").read_text())
    graph_snapshot = graph["graph_bundle_sha256"]
    destinations = defaultdict(list)
    for facility in facilities:
        destinations[facility["island_id"]].append(facility)
    origin_groups = defaultdict(list)
    for origin in origins:
        origin_groups[origin["terrestrial_component"]].append(origin)
    results = []
    request_count = failure_count = 0
    for component, component_origins in origin_groups.items():
        component_destinations = destinations.get(component, [])
        if not component_destinations:
            status = "requires_interisland_transfer" if component == "la-graciosa" else "not_evaluated"
            best = {row["origin_id"]: None for row in component_origins}
            failures = 0
        else:
            best, requests, failures = route_component(
                args.base_url.rstrip("/"), component_origins, component_destinations,
                args.origin_batch, args.destination_batch)
            request_count += requests
        failure_count += failures
        for origin in component_origins:
            match = best[origin["origin_id"]]
            if match:
                duration, distance, facility_id = match
                row_status = "routed"
            else:
                duration = distance = facility_id = ""
                row_status = status if not component_destinations else ("not_evaluated" if failures else "no_route")
            results.append({**origin, "nearest_facility_id": facility_id,
                            "travel_seconds": duration, "travel_distance_m": distance,
                            "routing_status": row_status, "engine_version": graph["engine_version"],
                            "graph_snapshot": graph_snapshot})
    results.sort(key=lambda row: row["origin_id"])
    staging = ROOT / "data/staging"
    cell_path = staging / "pediatric_accessibility_2024.csv"
    island_path = staging / "pediatric_accessibility_island_2024.csv"
    municipality_path = staging / "pediatric_accessibility_municipality_2024.csv"
    write_csv(staging / "accessibility_origins_2024.csv", origins, FIELDS[:7])
    write_csv(cell_path, results, FIELDS)
    island_rows = aggregate(results, ("island_id",))
    write_csv(island_path, island_rows)
    write_csv(municipality_path, aggregate(results, ("island_id", "municipality_id")))
    manifest = {
        "n_origins": len(origins), "n_destinations": len(facilities),
        "runtime_seconds": round(time.monotonic() - started, 3),
        "peak_memory_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024, 2),
        "failures": failure_count, "requests": request_count,
        "origin_batch_size": args.origin_batch, "destination_batch_size": args.destination_batch,
        "partitioning": "island_and_terrestrial_component", "public_server_requests": 0,
        "engine_version": graph["engine_version"], "graph_snapshot": graph_snapshot,
        "zbs_aggregation_enabled": False, "result_publication_status": "staging_only",
        "cell_result_sha256": sha256(cell_path),
        "routing_status_counts": dict(Counter(row["routing_status"] for row in results)),
        "island_aggregate_count": len(island_rows),
        "la_graciosa_cells": sum(row["terrestrial_component"] == "la-graciosa" for row in results),
        "la_graciosa_population_0_14": sum(row["child_population_0_14"] for row in results
                                              if row["terrestrial_component"] == "la-graciosa"),
    }
    manifest_path = ROOT / "data/manifests/accessibility_pipeline_benchmark.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
