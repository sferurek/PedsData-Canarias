#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "data/staging/osrm"
OUTPUT = ROOT / "data/manifests/osrm_canarias_graph.json"
OSM_SHA256 = "2c5f0f3c7b42fc68f6d1bf64679642edb86f546fe510e6f081a07a4d398379f9"
IMAGE = "ghcr.io/project-osrm/osrm-backend:v5.27.1"
IMAGE_DIGEST = "sha256:b1ca5d72da456e82f81b8732a095c2357b00710099efa844040d1eb40b4b5386"


def graph_digest(files):
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.name.encode() + b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def main():
    files = sorted(path for path in GRAPH_DIR.glob("canary-islands-260926.osrm*") if path.is_file())
    if not files:
        raise SystemExit("OSRM graph files not found")
    manifest = {
        "engine": "OSRM", "engine_version": "5.27.1",
        "container_image": IMAGE, "container_image_digest": IMAGE_DIGEST,
        "container_platform": "linux/amd64",
        "profile": "/opt/car.lua", "algorithm": "MLD",
        "graph_build_date": "2026-09-27",
        "osm_checksum_sha256": OSM_SHA256,
        "graph_file_count": len(files),
        "graph_size_bytes": sum(path.stat().st_size for path in files),
        "graph_bundle_sha256": graph_digest(files),
        "configuration": {
            "extract": "osrm-extract -p /opt/car.lua",
            "partition": "osrm-partition",
            "customize": "osrm-customize",
            "serve": "osrm-routed --algorithm mld",
        },
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
