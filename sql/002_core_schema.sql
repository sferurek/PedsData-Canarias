BEGIN;

CREATE TABLE source (
  source_id text PRIMARY KEY,
  name text NOT NULL,
  authority text NOT NULL,
  canonical_url text NOT NULL,
  license_status text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE dataset_version (
  dataset_version_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id text NOT NULL REFERENCES source(source_id),
  dataset_id text NOT NULL,
  version text NOT NULL,
  source_url text NOT NULL,
  retrieved_at timestamptz NOT NULL,
  reference_period_start date,
  reference_period_end date,
  parser_version text NOT NULL,
  checksum_sha256 text NOT NULL CHECK (checksum_sha256 ~ '^[0-9a-f]{64}$'),
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (source_id, dataset_id, version, checksum_sha256),
  CHECK (reference_period_end IS NULL OR reference_period_start IS NULL OR reference_period_end >= reference_period_start)
);

CREATE TABLE island (
  island_id text PRIMARY KEY CHECK (island_id IN ('el-hierro', 'la-gomera', 'la-palma', 'tenerife', 'gran-canaria', 'fuerteventura', 'lanzarote')),
  official_code text UNIQUE,
  name text NOT NULL UNIQUE,
  sort_order smallint NOT NULL UNIQUE CHECK (sort_order BETWEEN 1 AND 7)
);

CREATE TABLE coverage_status (
  dataset_version_id uuid NOT NULL REFERENCES dataset_version(dataset_version_id),
  island_id text NOT NULL REFERENCES island(island_id),
  variable_key text NOT NULL,
  status value_status NOT NULL,
  notes text,
  PRIMARY KEY (dataset_version_id, island_id, variable_key)
);

CREATE TABLE municipality (
  municipality_id text PRIMARY KEY,
  official_code text NOT NULL UNIQUE,
  name text NOT NULL,
  island_id text NOT NULL REFERENCES island(island_id),
  geometry geometry(MultiPolygon, 4326),
  verification_status verification_status NOT NULL,
  CHECK (geometry IS NULL OR ST_IsValid(geometry))
);

CREATE TABLE health_area (
  health_area_id text PRIMARY KEY,
  official_code text,
  name text NOT NULL,
  island_id text NOT NULL UNIQUE REFERENCES island(island_id),
  valid_from date,
  valid_to date,
  verification_status verification_status NOT NULL,
  CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);

CREATE TABLE health_zone (
  health_zone_id text PRIMARY KEY,
  official_code text,
  name text NOT NULL,
  island_id text NOT NULL REFERENCES island(island_id),
  health_area_id text REFERENCES health_area(health_area_id),
  valid_from date,
  valid_to date,
  geometry geometry(MultiPolygon, 4326),
  source_crs text,
  source_url text NOT NULL,
  source_date date,
  verification_status verification_status NOT NULL,
  routing_eligible boolean NOT NULL DEFAULT false,
  dataset_version_id uuid NOT NULL REFERENCES dataset_version(dataset_version_id),
  notes text,
  CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from),
  CHECK (geometry IS NULL OR ST_IsValid(geometry)),
  CHECK (NOT routing_eligible OR (verification_status = 'VERIFIED' AND geometry IS NOT NULL))
);

CREATE INDEX health_zone_geometry_gix ON health_zone USING gist (geometry);

COMMIT;
