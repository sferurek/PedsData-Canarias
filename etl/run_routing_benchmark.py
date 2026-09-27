#!/usr/bin/env python3
import csv
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data/curated/routing_test_cases.csv"
OUTPUT = ROOT / "data/curated/routing_benchmark_results.csv"
MANIFEST = ROOT / "data/curated/routing_benchmark_manifest.json"
USER_AGENT = "PedsData-Canarias/phase1 (github.com/sferurek/PedsData-Canarias)"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def request_json(url, body=None, headers=None):
    command = ["curl", "-sS", "--max-time", "45", "-A", USER_AGENT]
    for header in headers or []:
        command.extend(["-H", header])
    if body is not None:
        command.extend(["-X", "POST", "--data-binary", body])
    command.extend(["-w", "\n%{http_code}", url])
    started = time.monotonic()
    completed = subprocess.run(command, capture_output=True, text=True)
    elapsed = round((time.monotonic() - started) * 1000)
    raw, _, status = completed.stdout.rpartition("\n")
    try:
        return json.loads(raw), int(status), elapsed, completed.stderr.strip()
    except (json.JSONDecodeError, ValueError):
        return None, status, elapsed, completed.stderr.strip() or raw[:200]


def base_result(case, engine):
    return {
        "case_id": case["case_id"], "island_id": case["island_id"],
        "case_type": case["case_type"], "engine": engine,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "request_sent": "false", "route_status": "not_evaluated",
        "duration_seconds": "", "distance_metres": "",
        "origin_snap_metres": "", "destination_snap_metres": "",
        "http_status": "", "latency_ms": "", "engine_code": "", "error": "",
    }


def guarded_result(case, engine):
    result = base_result(case, engine)
    result["route_status"] = case["expected_status"]
    result["engine_code"] = "preflight_guard"
    result["error"] = case["guard_reason"]
    return result


def run_osrm(case):
    result = base_result(case, "osrm")
    coordinates = (f"{case['origin_longitude']},{case['origin_latitude']};"
                   f"{case['destination_longitude']},{case['destination_latitude']}")
    url = f"https://routing.openstreetmap.de/routed-car/route/v1/driving/{coordinates}?overview=false&steps=false"
    payload, status, latency, error = request_json(url)
    result.update(request_sent="true", http_status=status, latency_ms=latency, error=error)
    if payload and payload.get("code") == "Ok" and payload.get("routes"):
        route = payload["routes"][0]
        waypoints = payload.get("waypoints", [{}, {}])
        result.update(route_status="routed", duration_seconds=round(route["duration"], 1),
                      distance_metres=round(route["distance"]), engine_code="Ok",
                      origin_snap_metres=round(waypoints[0].get("distance", 0), 1),
                      destination_snap_metres=round(waypoints[1].get("distance", 0), 1))
    elif payload:
        result.update(route_status="no_route", engine_code=payload.get("code", "unknown"))
    return result


def run_valhalla(case):
    result = base_result(case, "valhalla")
    body = json.dumps({
        "locations": [
            {"lon": float(case["origin_longitude"]), "lat": float(case["origin_latitude"])},
            {"lon": float(case["destination_longitude"]), "lat": float(case["destination_latitude"])},
        ],
        "costing": "auto", "costing_options": {"auto": {"use_ferry": 0}},
        "units": "kilometers",
    })
    payload, status, latency, error = request_json(
        "https://valhalla1.openstreetmap.de/route", body,
        ["X-Client-Id: PedsData-Canarias", "Content-Type: application/json"])
    result.update(request_sent="true", http_status=status, latency_ms=latency, error=error)
    if payload and payload.get("trip", {}).get("status") == 0:
        summary = payload["trip"]["summary"]
        result.update(route_status="routed", duration_seconds=round(summary["time"], 1),
                      distance_metres=round(summary["length"] * 1000), engine_code="0")
    elif payload:
        result.update(route_status="no_route",
                      engine_code=payload.get("error_code", payload.get("trip", {}).get("status", "unknown")),
                      error=payload.get("error", error))
    return result


def run_benchmark():
    with CASES.open(encoding="utf-8") as handle:
        cases = list(csv.DictReader(handle))
    results = []
    for index, case in enumerate(cases, 1):
        if case["expected_status"] != "routed":
            results.extend(guarded_result(case, engine) for engine in ("osrm", "valhalla"))
        else:
            results.append(run_osrm(case))
            results.append(run_valhalla(case))
            time.sleep(1.05)
        ors = base_result(case, "openrouteservice")
        ors["error"] = "api_key_required"
        results.append(ors)
        print(f"{index}/{len(cases)} {case['case_id']}", flush=True)
    return results


def main():
    rows = run_benchmark()
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "age_group_original": "0-14",
        "case_count": 35,
        "result_row_count": len(rows),
        "inputs": {
            "routing_test_cases.csv": sha256(CASES),
            "pediatric_facilities.csv": sha256(ROOT / "data/curated/pediatric_facilities.csv"),
            "child_population_grid_2024.geojson": sha256(ROOT / "data/raw/child_population_grid_2024.geojson"),
        },
        "output_sha256": sha256(OUTPUT),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {OUTPUT}")


def refresh_manifest():
    with OUTPUT.open(encoding="utf-8") as handle:
        result_count = sum(1 for _ in csv.DictReader(handle))
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "age_group_original": "0-14", "case_count": 35,
        "result_row_count": result_count,
        "inputs": {
            "routing_test_cases.csv": sha256(CASES),
            "pediatric_facilities.csv": sha256(ROOT / "data/curated/pediatric_facilities.csv"),
            "child_population_grid_2024.geojson": sha256(ROOT / "data/raw/child_population_grid_2024.geojson"),
        },
        "output_sha256": sha256(OUTPUT),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if "--manifest-only" in sys.argv:
        refresh_manifest()
    else:
        main()
