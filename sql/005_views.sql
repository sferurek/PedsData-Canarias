CREATE VIEW dataset_provenance AS
SELECT d.dataset_version_id, d.dataset_id, d.version, d.source_url,
       d.retrieved_at, d.reference_period_start, d.reference_period_end,
       d.parser_version, d.checksum_sha256, s.source_id, s.name AS source_name,
       s.authority, s.license_status
FROM dataset_version d
JOIN source s USING (source_id);

CREATE VIEW verified_routing_facility AS
SELECT f.*
FROM pediatric_facility f
WHERE f.routing_eligible
  AND f.verification_status = 'VERIFIED'
  AND f.location IS NOT NULL;

CREATE VIEW island_facility_coverage AS
SELECT i.island_id, i.name, i.sort_order,
       count(f.facility_id) FILTER (WHERE f.verification_status = 'VERIFIED') AS verified_facilities,
       count(f.facility_id) FILTER (WHERE f.routing_eligible) AS routing_facilities
FROM island i
LEFT JOIN pediatric_facility f USING (island_id)
GROUP BY i.island_id, i.name, i.sort_order;
