DO $$
BEGIN
  IF (SELECT count(*) FROM island) <> 7 THEN
    RAISE EXCEPTION 'Expected exactly seven islands';
  END IF;
  IF (SELECT count(*) FROM island_facility_coverage) <> 7 THEN
    RAISE EXCEPTION 'LEFT JOIN coverage view dropped an island';
  END IF;
  IF EXISTS (SELECT 1 FROM verified_routing_facility WHERE verification_status <> 'VERIFIED') THEN
    RAISE EXCEPTION 'Unverified facility entered routing view';
  END IF;
END $$;

DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM accessibility_result
    WHERE route_status <> 'routed' AND (travel_seconds IS NOT NULL OR distance_metres IS NOT NULL)
  ) THEN
    RAISE EXCEPTION 'A non-route was represented as a numeric value';
  END IF;
END $$;

DO $$
BEGIN
  BEGIN
    INSERT INTO source VALUES ('qa', 'QA', 'test', 'https://example.invalid', 'test', now());
    INSERT INTO dataset_version (
      source_id, dataset_id, version, source_url, retrieved_at, parser_version, checksum_sha256
    ) VALUES ('qa', 'qa', '1', 'https://example.invalid', now(), 'qa', repeat('a', 64));
    INSERT INTO pediatric_facility (
      facility_id, name, island_id, facility_type, pediatrics_ap,
      pediatric_emergency, pediatric_inpatient, neonatology, nicu, picu,
      service_status, verification_status, routing_eligible, source_url, dataset_version_id
    ) SELECT 'bad-route', 'Bad route', 'el-hierro', 'health_centre',
      'observed', 'not_available', 'not_available', 'not_available',
      'not_available', 'needs_validation', 'active', 'NEEDS_VALIDATION', true,
      'https://example.invalid', dataset_version_id FROM dataset_version WHERE dataset_id = 'qa';
    RAISE EXCEPTION 'Expected routing eligibility constraint failure';
  EXCEPTION WHEN check_violation THEN NULL;
  END;
END $$;
