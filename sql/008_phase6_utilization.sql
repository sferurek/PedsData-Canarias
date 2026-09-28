-- Self-contained additive schema; does not migrate or replace RC3 tables.
BEGIN;
CREATE SCHEMA phase6;
CREATE TABLE phase6.pediatric_primary_care_activity (
 id bigserial PRIMARY KEY, year smallint NOT NULL CHECK(year BETWEEN 2007 AND 2024),
 island_id text NOT NULL CHECK(island_id IN ('el-hierro','la-gomera','la-palma','tenerife','gran-canaria','fuerteventura','lanzarote')),
 service text NOT NULL CHECK(service='PEDIATRIA_AP'),
 activity_type text NOT NULL CHECK(activity_type IN ('consultations','distinct_persons','frequentation')),
 place text NOT NULL, value numeric CHECK(value>=0), unit text NOT NULL,
 value_status text NOT NULL CHECK(value_status IN ('OBSERVED','NOT_AVAILABLE','SUPPRESSED')),
 source_id text NOT NULL, source_url text NOT NULL, dataset_version text NOT NULL, checksum text NOT NULL CHECK(length(checksum)=64),
 reference_period text NOT NULL, retrieved_at timestamptz NOT NULL, license_url text NOT NULL, method_id text NOT NULL,
 CHECK((value_status='OBSERVED')=(value IS NOT NULL)),
 UNIQUE(year,island_id,service,activity_type,place,dataset_version)
);
CREATE TABLE phase6.pediatric_waiting_list (
 id bigserial PRIMARY KEY, reference_date date NOT NULL, specialty text NOT NULL CHECK(specialty IN ('PEDIATRIA','CIRUGIA_PEDIATRICA')),
 wait_type text NOT NULL CHECK(wait_type IN ('outpatient','surgical')),
 geography_level text NOT NULL CHECK(geography_level='autonomous_community'), geography_id text NOT NULL CHECK(geography_id='canarias'),
 pending_patients numeric CHECK(pending_patients>=0), time_band text NOT NULL,
 mean_wait_days_if_available numeric CHECK(mean_wait_days_if_available>=0),
 value_status text NOT NULL CHECK(value_status IN ('OBSERVED','ZERO_PUBLISHED','MISSING','NOT_COMPARABLE','SUPPRESSED')),
 comparability_status text NOT NULL, source_id text NOT NULL, source_url text NOT NULL,
 dataset_version text NOT NULL, checksum text NOT NULL CHECK(length(checksum)=64), reference_period text NOT NULL,
 retrieved_at timestamptz NOT NULL, license_url text NOT NULL, method_id text NOT NULL,
 CHECK((value_status IN ('OBSERVED','ZERO_PUBLISHED'))=(pending_patients IS NOT NULL)),
 CHECK(value_status!='ZERO_PUBLISHED' OR pending_patients=0)
);
CREATE TABLE phase6.adolescent_survey_indicator (
 id bigserial PRIMARY KEY, indicator_id text NOT NULL, reference_period text NOT NULL,
 geography_level text NOT NULL CHECK(geography_level='autonomous_community'), geography_id text NOT NULL CHECK(geography_id='canarias'),
 age_group_original text NOT NULL, universe text NOT NULL, weighting text NOT NULL,
 value numeric CHECK(value BETWEEN 0 AND 100), n_valid_published numeric CHECK(n_valid_published>=100),
 ci_lower numeric, ci_upper numeric, value_status text NOT NULL CHECK(value_status='SURVEY_ESTIMATE'),
 source_id text NOT NULL, source_url text NOT NULL, dataset_version text NOT NULL, checksum text NOT NULL CHECK(length(checksum)=64),
 retrieved_at timestamptz NOT NULL, license_url text NOT NULL, method_id text NOT NULL,
 UNIQUE(source_id,dataset_version,indicator_id,age_group_original)
);
-- Future domains remain HOLD: schema is not admission or permission to populate.
CREATE TABLE phase6.held_indicator (
 id bigserial PRIMARY KEY, reference_period text NOT NULL, geography_level text NOT NULL,
 geography_id text NOT NULL, age_group_original text NOT NULL, universe text NOT NULL,
 value numeric, numerator numeric, denominator numeric, unit text NOT NULL,
 source_id text NOT NULL, source_url text NOT NULL, dataset_version text NOT NULL,
 checksum text NOT NULL CHECK(length(checksum)=64), retrieved_at timestamptz NOT NULL,
 license_url text NOT NULL, method_id text NOT NULL, comparability_status text NOT NULL DEFAULT 'HOLD' CHECK(comparability_status='HOLD'),
 CHECK(value IS NULL AND numerator IS NULL AND denominator IS NULL)
);
CREATE TABLE phase6.bdcap_indicator (LIKE phase6.held_indicator INCLUDING ALL);
ALTER TABLE phase6.bdcap_indicator ADD COLUMN weighting text NOT NULL;
CREATE TABLE phase6.vaccination_indicator (LIKE phase6.held_indicator INCLUDING ALL);
ALTER TABLE phase6.vaccination_indicator ADD COLUMN cohort text NOT NULL;
ALTER TABLE phase6.vaccination_indicator ADD COLUMN vaccine text NOT NULL;
ALTER TABLE phase6.vaccination_indicator ADD COLUMN status text CHECK(status IN ('provisional','definitive'));
CREATE TABLE phase6.neonatal_screening_indicator (LIKE phase6.held_indicator INCLUDING ALL);
CREATE TABLE phase6.hospital_service_activity (LIKE phase6.held_indicator INCLUDING ALL);
COMMIT;
