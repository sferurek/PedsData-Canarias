#!/bin/sh
set -eu

container="${1:-pedsdata-db-1}"
port="${2:-5432}"
for file in sql/001_extensions_and_types.sql sql/002_core_schema.sql sql/003_clinical_and_routing.sql sql/004_seed_islands.sql sql/005_views.sql sql/tests/001_invariants.sql; do
  docker exec -i "$container" psql -p "$port" -v ON_ERROR_STOP=1 -U pedsdata -d pedsdata < "$file"
done
