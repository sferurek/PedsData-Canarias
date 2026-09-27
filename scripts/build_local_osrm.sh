#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
raw="$root/data/raw/osm"
graph="$root/data/staging/osrm"
name="canary-islands-260926"
url="https://download.geofabrik.de/africa/$name.osm.pbf"
image="ghcr.io/project-osrm/osrm-backend:v5.27.1@sha256:b1ca5d72da456e82f81b8732a095c2357b00710099efa844040d1eb40b4b5386"

mkdir -p "$raw" "$graph" "$root/data/manifests"
test -f "$raw/$name.osm.pbf" || curl -fL "$url" -o "$raw/$name.osm.pbf"
test -f "$raw/$name.osm.pbf.md5" || curl -fL "$url.md5" -o "$raw/$name.osm.pbf.md5"

expected=$(awk '{print $1}' "$raw/$name.osm.pbf.md5")
if command -v md5sum >/dev/null 2>&1; then
  actual=$(md5sum "$raw/$name.osm.pbf" | awk '{print $1}')
else
  actual=$(md5 -q "$raw/$name.osm.pbf")
fi
test "$expected" = "$actual"
cp "$raw/$name.osm.pbf" "$graph/$name.osm.pbf"

docker pull "$image"
docker run --rm -t -v "$graph:/data" "$image" \
  osrm-extract -p /opt/car.lua "/data/$name.osm.pbf"
docker run --rm -t -v "$graph:/data" "$image" \
  osrm-partition "/data/$name.osrm"
docker run --rm -t -v "$graph:/data" "$image" \
  osrm-customize "/data/$name.osrm"

"$root/.venv/bin/python" "$root/etl/build_osm_snapshot_manifest.py"
"$root/.venv/bin/python" "$root/etl/build_osrm_graph_manifest.py"
