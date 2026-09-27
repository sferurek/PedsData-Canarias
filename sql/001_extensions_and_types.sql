BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE value_status AS ENUM (
  'observed', 'not_available', 'needs_validation', 'suppressed', 'no_route'
);

CREATE TYPE verification_status AS ENUM (
  'VERIFIED', 'PARTIAL', 'NEEDS_VALIDATION', 'NOT_AVAILABLE'
);

CREATE TYPE route_status AS ENUM (
  'routed', 'no_route', 'not_evaluated', 'requires_interisland_transfer'
);

COMMIT;
