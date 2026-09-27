#!/usr/bin/env python3
import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data/curated/routing_test_cases.csv"
PUBLIC = ROOT / "data/curated/routing_benchmark_results.csv"
LOCAL = ROOT / "data/curated/local_osrm_benchmark_results.csv"
OUTPUT = ROOT / "data/curated/routing_reference_journeys.csv"


def time_status(value):
    return "GREEN" if value <= 20 else "YELLOW" if value <= 35 else "RED"


def point_status(value, red_limit):
    return "GREEN" if value <= 50 else "YELLOW" if value <= red_limit else "RED"


def worst_status(*values):
    order = {"GREEN": 0, "YELLOW": 1, "RED": 2}
    return max(values, key=order.get)


def main():
    with CASES.open(encoding="utf-8") as handle:
        cases = {row["case_id"]: row for row in csv.DictReader(handle)}
    public = {}
    with PUBLIC.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["route_status"] == "routed":
                public.setdefault(row["case_id"], {})[row["engine"]] = row
    with LOCAL.open(encoding="utf-8") as handle:
        local = {row["case_id"]: row for row in csv.DictReader(handle)}
    rows = []
    for case_id, case in cases.items():
        if case["case_type"] not in {"urban", "rural", "extreme"}:
            continue
        comparisons = public[case_id]
        reference_time = statistics.median(
            float(comparisons[engine]["duration_seconds"]) for engine in ("osrm", "valhalla"))
        reference_distance = statistics.median(
            float(comparisons[engine]["distance_metres"]) for engine in ("osrm", "valhalla"))
        observed = local[case_id]
        local_time, local_distance = float(observed["duration_seconds"]), float(observed["distance_metres"])
        time_difference = abs(local_time - reference_time) / reference_time * 100
        distance_difference = abs(local_distance - reference_distance) / reference_distance * 100
        cell_snap, facility_snap = float(observed["origin_snap_metres"]), float(observed["destination_snap_metres"])
        rows.append({
            "journey_id": case_id, "island_id": case["island_id"],
            "case_type": case["case_type"],
            "origin": f"{case['origin_latitude']},{case['origin_longitude']}",
            "destination": f"{case['destination_latitude']},{case['destination_longitude']}",
            "destination_name": case["destination_name"],
            "reference_distance_m": round(reference_distance),
            "reference_time_s": round(reference_time, 1),
            "reference_source": "median_phase1_public_osrm_valhalla",
            "reference_date": "2026-09-27",
            "local_distance_m": round(local_distance),
            "local_time_s": round(local_time, 1),
            "distance_difference_pct": round(distance_difference, 1),
            "time_difference_pct": round(time_difference, 1),
            "cell_snap_m": cell_snap, "facility_snap_m": facility_snap,
            "snap_status": worst_status(point_status(cell_snap, 150),
                                        point_status(facility_snap, 200)),
            "time_status": time_status(time_difference),
            "notes": "Contrast between two public OSM engines; not ground truth",
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} reference journeys")


if __name__ == "__main__":
    main()
