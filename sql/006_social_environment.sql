BEGIN;
CREATE TABLE socioeconomic_indicator (
  socioeconomic_indicator_id text PRIMARY KEY, geography_level text NOT NULL, geography_id text NOT NULL,
  indicator_code text NOT NULL, unit text NOT NULL, value numeric, status coverage_state NOT NULL,
  source_id text NOT NULL REFERENCES source(source_id), dataset_version_id text NOT NULL REFERENCES dataset_version(dataset_version_id),
  period_start date NOT NULL, period_end date NOT NULL, retrieved_at timestamptz NOT NULL
);
CREATE TABLE territorial_indicator (
  territorial_indicator_id text PRIMARY KEY, geography_level text NOT NULL, geography_id text NOT NULL,
  indicator_code text NOT NULL, unit text NOT NULL, value numeric, status coverage_state NOT NULL,
  source_id text NOT NULL REFERENCES source(source_id), dataset_version_id text NOT NULL REFERENCES dataset_version(dataset_version_id),
  period_start date NOT NULL, period_end date NOT NULL, retrieved_at timestamptz NOT NULL
);
CREATE TABLE air_station (
  air_station_id text PRIMARY KEY, name text NOT NULL, island_id text NOT NULL REFERENCES island(island_id),
  municipality_id text, location geometry(Point,4326), station_type text, pollutants text[] NOT NULL,
  status coverage_state NOT NULL, source_id text NOT NULL REFERENCES source(source_id),
  dataset_version_id text NOT NULL REFERENCES dataset_version(dataset_version_id), period_start date, period_end date, retrieved_at timestamptz NOT NULL
);
CREATE TABLE air_observation (
  air_station_id text NOT NULL REFERENCES air_station(air_station_id), pollutant text NOT NULL,
  period_start date NOT NULL, period_end date NOT NULL, geography_level text NOT NULL DEFAULT 'station',
  geography_id text NOT NULL, unit text NOT NULL, value numeric, status coverage_state NOT NULL,
  source_id text NOT NULL REFERENCES source(source_id), dataset_version_id text NOT NULL REFERENCES dataset_version(dataset_version_id), retrieved_at timestamptz NOT NULL,
  PRIMARY KEY(air_station_id,pollutant,period_start)
);
CREATE TABLE weather_station (
  weather_station_id text PRIMARY KEY, name text NOT NULL, island_id text NOT NULL REFERENCES island(island_id),
  municipality_id text, location geometry(Point,4326), status coverage_state NOT NULL,
  source_id text NOT NULL REFERENCES source(source_id), dataset_version_id text NOT NULL REFERENCES dataset_version(dataset_version_id), period_start date, period_end date, retrieved_at timestamptz NOT NULL
);
CREATE TABLE weather_observation (
  weather_station_id text NOT NULL REFERENCES weather_station(weather_station_id), variable text NOT NULL,
  period_start timestamptz NOT NULL, period_end timestamptz NOT NULL, geography_level text NOT NULL DEFAULT 'station',
  geography_id text NOT NULL, unit text NOT NULL, value numeric, status coverage_state NOT NULL,
  source_id text NOT NULL REFERENCES source(source_id), dataset_version_id text NOT NULL REFERENCES dataset_version(dataset_version_id), retrieved_at timestamptz NOT NULL,
  PRIMARY KEY(weather_station_id,variable,period_start)
);
CREATE TABLE environment_event (
  environment_event_id text PRIMARY KEY, event_type text NOT NULL,
  period_start timestamptz NOT NULL, period_end timestamptz NOT NULL,
  geography_level text NOT NULL, geography_id text NOT NULL,
  status text NOT NULL CHECK(status IN ('no_event','possible_event','confirmed_event')),
  source_id text NOT NULL REFERENCES source(source_id), dataset_version_id text NOT NULL REFERENCES dataset_version(dataset_version_id), retrieved_at timestamptz NOT NULL
);
COMMIT;
