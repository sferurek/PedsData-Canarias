#!/usr/bin/env python3
import csv
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from run_routing_benchmark import base_result, guarded_result, request_json

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data/curated/routing_test_cases.csv"
OUTPUT = ROOT / "data/curated/local_osrm_benchmark_results.csv"
MANIFEST = ROOT / "data/manifests/local_osrm_benchmark.json"
ENDPOINT = "http://127.0.0.1:55000"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_route(case):
    result = base_result(case, "osrm-local-5.27.1")
    coordinates = (f"{case['origin_longitude']},{case['origin_latitude']};"
                   f"{case['destination_longitude']},{case['destination_latitude']}")
    url = f"{ENDPOINT}/route/v1/driving/{coordinates}?overview=false&steps=false"
    payload, status, latency, error = request_json(url)
    result.update(request_sent="true", http_status=status, latency_ms=latency, error=error)
    if payload and payload.get("code") == "Ok" and payload.get("routes"):
        route, waypoints = payload["routes"][0], payload.get("waypoints", [{}, {}])
        result.update(route_status="routed", duration_seconds=round(route["duration"], 1),
                      distance_metres=round(route["distance"]), engine_code="Ok",
                      origin_snap_metres=round(waypoints[0].get("distance", 0), 1),
                      destination_snap_metres=round(waypoints[1].get("distance", 0), 1))
    elif payload:
        result.update(route_status="no_route", engine_code=payload.get("code", "unknown"))
    return result


def main():
    with CASES.open(encoding="utf-8") as handle:
        cases = list(csv.DictReader(handle))
    started = time.monotonic()
    rows = [guarded_result(case, "osrm-local-5.27.1")
            if case["expected_status"] != "routed" else run_route(case)
            for case in cases]
    runtime = round(time.monotonic() - started, 3)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    manifest = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "engine": "OSRM", "engine_version": "5.27.1",
        "graph_manifest_sha256": sha256(ROOT / "data/manifests/osrm_canarias_graph.json"),
        "test_cases_sha256": sha256(CASES),
        "output_sha256": sha256(OUTPUT),
        "case_count": len(cases), "requests_sent": 28,
        "runtime_seconds": runtime,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} cases in {runtime}s")


if __name__ == "__main__":
    main()
