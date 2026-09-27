BEGIN;

CREATE TABLE child_population_grid (
  grid_cell_id text PRIMARY KEY,
  island_id text NOT NULL REFERENCES island(island_id),
  municipality_id text REFERENCES municipality(municipality_id),
  health_zone_id text REFERENCES health_zone(health_zone_id),
  age_group_original text NOT NULL,
  source_geography_level text NOT NULL DEFAULT 'grid' CHECK (source_geography_level = 'grid'),
  reference_year smallint NOT NULL,
  child_count integer,
  value_status value_status NOT NULL,
  geometry geometry(Polygon, 4326) NOT NULL,
  representative_point geometry(Point, 4326) NOT NULL,
  dataset_version_id uuid NOT NULL REFERENCES dataset_version(dataset_version_id),
  CHECK (ST_IsValid(geometry)),
  CHECK (ST_Covers(geometry, representative_point)),
  CHECK ((value_status = 'observed' AND child_count IS NOT NULL AND child_count >= 0)
      OR (value_status <> 'observed' AND child_count IS NULL))
);

CREATE INDEX child_population_grid_geometry_gix ON child_population_grid USING gist (geometry);
CREATE INDEX child_population_grid_point_gix ON child_population_grid USING gist (representative_point);

CREATE TABLE pediatric_facility (
  facility_id text PRIMARY KEY,
  official_id text,
  name text NOT NULL,
  island_id text NOT NULL REFERENCES island(island_id),
  municipality_id text REFERENCES municipality(municipality_id),
  health_area_id text REFERENCES health_area(health_area_id),
  health_zone_id text REFERENCES health_zone(health_zone_id),
  facility_type text NOT NULL,
  location geometry(Point, 4326),
  latitude double precision GENERATED ALWAYS AS (ST_Y(location)) STORED,
  longitude double precision GENERATED ALWAYS AS (ST_X(location)) STORED,
  address text,
  pediatrics_ap value_status NOT NULL,
  pediatric_emergency value_status NOT NULL,
  pediatric_inpatient value_status NOT NULL,
  neonatology value_status NOT NULL,
  nicu value_status NOT NULL,
  picu value_status NOT NULL,
  service_status text NOT NULL,
  verification_status verification_status NOT NULL,
  routing_eligible boolean NOT NULL DEFAULT false,
  source_url text NOT NULL,
  source_date date,
  dataset_version_id uuid NOT NULL REFERENCES dataset_version(dataset_version_id),
  verified_at timestamptz,
  notes text,
  CHECK (location IS NULL OR ST_Within(location, ST_MakeEnvelope(-18.5, 27.3, -13.0, 29.6, 4326))),
  CHECK (NOT routing_eligible OR (verification_status = 'VERIFIED' AND location IS NOT NULL))
);

CREATE INDEX pediatric_facility_location_gix ON pediatric_facility USING gist (location);

CREATE TABLE pediatric_resource (
  pediatric_resource_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  facility_id text NOT NULL REFERENCES pediatric_facility(facility_id),
  resource_type text NOT NULL,
  availability value_status NOT NULL,
  verification_status verification_status NOT NULL,
  valid_from date,
  valid_to date,
  dataset_version_id uuid NOT NULL REFERENCES dataset_version(dataset_version_id),
  notes text,
  UNIQUE (facility_id, resource_type, valid_from),
  CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);

CREATE TABLE routing_snapshot (
  routing_snapshot_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  engine text NOT NULL,
  engine_version text,
  profile text NOT NULL,
  network_date date,
  executed_at timestamptz NOT NULL,
  configuration jsonb NOT NULL,
  checksum_sha256 text NOT NULL CHECK (checksum_sha256 ~ '^[0-9a-f]{64}$'),
  dataset_version_id uuid NOT NULL REFERENCES dataset_version(dataset_version_id)
);

CREATE TABLE accessibility_result (
  accessibility_result_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  grid_cell_id text NOT NULL REFERENCES child_population_grid(grid_cell_id),
  target_type text NOT NULL,
  destination_facility_id text REFERENCES pediatric_facility(facility_id),
  routing_snapshot_id uuid NOT NULL REFERENCES routing_snapshot(routing_snapshot_id),
  route_status route_status NOT NULL,
  travel_seconds integer,
  distance_metres integer,
  requires_interisland_transfer boolean NOT NULL DEFAULT false,
  dataset_version_id uuid NOT NULL REFERENCES dataset_version(dataset_version_id),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (grid_cell_id, target_type, routing_snapshot_id),
  CHECK (travel_seconds IS NULL OR travel_seconds > 0),
  CHECK (distance_metres IS NULL OR distance_metres > 0),
  CHECK ((route_status = 'routed' AND destination_facility_id IS NOT NULL
          AND travel_seconds IS NOT NULL AND distance_metres IS NOT NULL
          AND NOT requires_interisland_transfer)
      OR (route_status <> 'routed' AND travel_seconds IS NULL AND distance_metres IS NULL)),
  CHECK (NOT requires_interisland_transfer OR route_status = 'requires_interisland_transfer')
);

COMMIT;
