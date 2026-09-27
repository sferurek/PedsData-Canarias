#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PBF = ROOT / "data/raw/osm/canary-islands-260926.osm.pbf"
MD5_FILE = ROOT / "data/raw/osm/canary-islands-260926.osm.pbf.md5"
POLY = ROOT / "data/raw/osm/canary-islands.poly"
OUTPUT = ROOT / "data/manifests/osm_canarias_snapshot.json"
SOURCE_URL = "https://download.geofabrik.de/africa/canary-islands-260926.osm.pbf"


def checksum(path, algorithm):
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bounding_box():
    coordinates = []
    for line in POLY.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 2:
            try:
                coordinates.append((float(parts[0]), float(parts[1])))
            except ValueError:
                pass
    return [min(x for x, _ in coordinates), min(y for _, y in coordinates),
            max(x for x, _ in coordinates), max(y for _, y in coordinates)]


def main():
    published_md5 = MD5_FILE.read_text(encoding="utf-8").split()[0]
    actual_md5 = checksum(PBF, "md5")
    if actual_md5 != published_md5:
        raise SystemExit("Geofabrik MD5 does not match downloaded PBF")
    manifest = {
        "dataset": "OpenStreetMap Canary Islands extract",
        "source_url": SOURCE_URL,
        "download_date": "2026-09-27",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
        "extract_version": "canary-islands-260926",
        "osm_data_timestamp": "2026-09-26T20:22:51Z",
        "format": "osm.pbf",
        "size_bytes": PBF.stat().st_size,
        "checksum_md5": actual_md5,
        "checksum_sha256": checksum(PBF, "sha256"),
        "bounding_box_wgs84": bounding_box(),
        "islands": ["el-hierro", "la-gomera", "la-palma", "tenerife",
                    "gran-canaria", "fuerteventura", "lanzarote"],
        "separate_road_components": ["la-graciosa"],
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
