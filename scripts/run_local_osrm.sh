#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
graph="$root/data/staging/osrm"
name="canary-islands-260926"
image="ghcr.io/project-osrm/osrm-backend:v5.27.1@sha256:b1ca5d72da456e82f81b8732a095c2357b00710099efa844040d1eb40b4b5386"
port="${OSRM_PORT:-55000}"

docker rm -f pedsdata-osrm-phase2 >/dev/null 2>&1 || true
docker run --rm -d --name pedsdata-osrm-phase2 -p "$port:5000" \
  -v "$graph:/data" "$image" \
  osrm-routed --algorithm mld "/data/$name.osrm"
