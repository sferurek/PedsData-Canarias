-- Phase 6B admissions are regional; no island rows are permitted.
BEGIN;
CREATE TABLE phase6.bdcap_pediatric_indicator (
 id bigserial PRIMARY KEY,
 indicator_id text NOT NULL,
 reference_period smallint NOT NULL CHECK(reference_period BETWEEN 2011 AND 2024),
 geography_level text NOT NULL CHECK(geography_level='autonomous_community'),
 geography_id text NOT NULL CHECK(geography_id='canarias'),
 age_group_original text NOT NULL CHECK(age_group_original='00-14 años'),
 value numeric NOT NULL CHECK(value>=0),
 unit text NOT NULL CHECK(unit='persons_per_1000_assigned'),
 weighted_cases numeric NOT NULL CHECK(weighted_cases>=0),
 denominator numeric,
 value_status text NOT NULL CHECK(value_status='WEIGHTED_SAMPLE'),
 weighting text NOT NULL,
 source_id text NOT NULL, source_url text NOT NULL, dataset_version text NOT NULL,
 checksum text NOT NULL CHECK(length(checksum)=64), retrieved_at timestamptz NOT NULL,
 license_url text NOT NULL, method_id text NOT NULL
);
CREATE TABLE phase6.neonatal_screening_observation (
 id bigserial PRIMARY KEY,
 indicator_id text NOT NULL,
 reference_period smallint NOT NULL CHECK(reference_period=2024),
 geography_level text NOT NULL CHECK(geography_level='autonomous_community'),
 geography_id text NOT NULL CHECK(geography_id='canarias'),
 value numeric NOT NULL CHECK(value>=0),
 unit text NOT NULL,
 numerator numeric CHECK(numerator>=0),
 denominator numeric CHECK(denominator>0),
 value_status text NOT NULL CHECK(value_status='OBSERVED'),
 source_id text NOT NULL, source_url text NOT NULL, dataset_version text NOT NULL,
 checksum text NOT NULL CHECK(length(checksum)=64), retrieved_at timestamptz NOT NULL,
 license_url text NOT NULL, method_id text NOT NULL
);
CREATE TABLE phase6.adolescent_survey_observation_phase6b (
 id bigserial PRIMARY KEY,
 survey_id text NOT NULL CHECK(survey_id IN ('esde_2023','estudes_2023')),
 indicator_id text NOT NULL,
 reference_period smallint NOT NULL CHECK(reference_period=2023),
 geography_level text NOT NULL CHECK(geography_level='autonomous_community'),
 geography_id text NOT NULL CHECK(geography_id='canarias'),
 age_group_original text NOT NULL,
 sex text NOT NULL,
 value numeric NOT NULL CHECK(value BETWEEN 0 AND 100),
 unit text NOT NULL CHECK(unit='percent'),
 sample_size numeric CHECK(sample_size>=100),
 value_status text NOT NULL CHECK(value_status='SURVEY_ESTIMATE'),
 source_id text NOT NULL, source_url text NOT NULL, dataset_version text NOT NULL,
 checksum text NOT NULL CHECK(length(checksum)=64), retrieved_at timestamptz NOT NULL,
 license_url text NOT NULL, method_id text NOT NULL
);
COMMIT;
