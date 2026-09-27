# Modelo lógico de datos — contrato propuesto

La Fase 0 propuso este contrato. En Fase 1 las migraciones de `sql/` se
ejecutaron en PostgreSQL 18/PostGIS 3.6. Añaden estados de valor, verificación y
ruta, restricciones espaciales y vistas que preservan siete islas.

## Entidades y relaciones

|Entidad|Clave / relaciones|Contenido esencial|
|---|---|---|
|island|island_id PK; official_code único|Siete filas permanentes; nombre original, código de fuente, orden UI|
|municipality|id PK, island_id FK|INE code, nombre, geometría/versiones; excepciones geográficas conservadas|
|health_area|id PK; relación territorial versionada|Código SCS, nombre, vigencia, isla(s) servidas|
|health_zone|id PK; area_id FK|Código oficial, nombre, versión, valid_from/to, geometría y fuente|
|geography_version|id PK|Nivel, CRS, snapshot, licencia y vigencia|
|geography_crosswalk|source/target/version|Correspondencia municipio–ZBS–isla; peso, método, incertidumbre|
|child_population_grid|cell_id + dataset_version + age + sex|Geometría, municipio/isla, población original, estado y periodo|
|pediatric_facility|id PK; official_id+authority|Nombre/tipo, isla, municipio, ZBS, área, lat/lon, precisión, fuente, fecha de verificación|
|pediatric_resource|id PK; facility_id FK|Servicio confirmado, estado yes/no/unknown, edad atendida, horario, camas/FTE si existen, vigencia y evidencia|
|facility_referral|origin/destination/service/version|Derivaciones intrainsulares/interinsulares, fecha, fuente; no inferir destino por cercanía|
|pediatric_primary_care_activity|observation_id FK|TIS, profesionales, consultas, frecuentación, tipo de consulta y profesional|
|pediatric_emergency_activity|observation_id FK, facility_id|Episodios, ingreso/no ingreso/observación, definición de urgencia pediátrica|
|pediatric_hospital_activity|observation_id FK, facility_id|Altas/estancias/actividad de servicio; no residencia implícita|
|pediatric_hospital_discharge|observation_id FK|Agregado diagnóstico, CIE/version, residencia, hospital si disponible, carácter ingreso/motivo alta|
|perinatal_indicator|observation_id FK|Semanas, parto/bebé, edad materna, nacidos vivos/MFT y universo|
|pediatric_mortality|observation_id FK|Causa/version, edad días/años, residente/no residente y denominador|
|child_health_survey|observation_id FK|Edición, cuestionario, pesos, n sin ponderar, error estándar, diseño y elegibilidad|
|air_station / weather_station|station_id PK|Código organismo, coordenadas, altitud, tipología, isla, vigencia|
|air_observation / weather_observation|station+variable+period+version|Valor, unidad, calidad, validación provisional/definitiva, zona horaria|
|socioeconomic_indicator|observation_id FK|Renta/umbral/educación, población de referencia y escala territorial|
|source|source_id PK|Organismo, título, URL, licencia/condiciones, contacto institucional|
|dataset|dataset_id PK; source_id FK|Código oficial, definición, periodicidad, dimensiones|
|dataset_version|id PK; dataset_id FK|Versión proveedor, download_at, SHA256, URL exacta, parser_version, periodo, licencia snapshot|
|observation|id PK; dataset_version_id FK|Contrato común detallado debajo|
|indicator_definition|id+version|Fórmula, unidades, grupo edad, geografía, denominador, método IC y supresión|
|coverage_assessment|variable+island+period+age+version|COMPLETE/PARTIAL/NOT AVAILABLE/NEEDS VALIDATION, evidencia y missing_reason|
|routing_run / accessibility_result|run_id; origen/destino/servicio|Motor, grafo, perfil, snapping, duración, unreachable, población ponderada y fecha|
|transformation / lineage_edge|id; parent/child|Código versión, fórmula, inputs, supuestos y trazabilidad derivada|
|quality_issue|id; dataset_version/observation|Regla, severidad, evidencia, responsable y resolución|

## Observación común

Obligatorios salvo nulabilidad semántica explícita: `source_id`, `dataset_id`, `dataset_version_id`, `period_start`, `period_end`, `age_group_original`, `sex`, `geography_level`, `geography_id`, `island_id`, `unit`, `value`, `last_verified_at`. Además `original_code`, `value_status`, `missing_reason`, `universe`, `geography_role` (residencia/atención/estación), `method_id`, `numerator`, `denominator`, `ci_lower`, `ci_upper`, `unweighted_n` y `original_value`.

`age_group_original` puede ser «no aplica» para recursos y ambiente, sin inventar edad. `sex` conserva total/desconocido/no aplica por separado. `island_id` es nulo para Canarias y provincias. `value` numérico decimal nullable: observado cero es diferente de desconocido, suprimido, no aplicable o no disponible. Guardar símbolos originales y sus flags antes de convertirlos.

## Integridad

- PK de observación fuente: versión + dimensión territorial/version + periodo + edad + sexo + medida + otras dimensiones reales. No perder diagnóstico, lugar consulta o profesional de la clave.
- CHECK: inicio <= fin; estados sin dato exigen value NULL; observado requiere valor; tasas con denominador no positivo quedan indefinidas.
- FK compuesta o trigger verifica que source/dataset/version concuerden. Isla del municipio y geometría han de coincidir con versión temporal.
- No sumar total Canarias con sus islas; no sumar sexos totales con mujeres/hombres; no sumar grupos de edad solapados.
- Un recurso puede servir a varias islas, pero su emplazamiento físico es uno. Una lista de derivación no duplica el hospital como presente físicamente en otra isla.
- Toda cifra derivada tiene inputs versionados y fórmula; `last_verified_at` no sustituye a `period_end` ni `download_at`.
- `coverage_assessment` independiente de `resource_status`: un servicio confirmado ausente puede estar completamente documentado aunque su actividad sea no aplicable.

## Semilla territorial

|Código observado ISTAC|Isla|
|---|---|
|ES703|El Hierro|
|ES706|La Gomera|
|ES707|La Palma|
|ES709|Tenerife|
|ES705|Gran Canaria|
|ES704|Fuerteventura|
|ES708|Lanzarote|

Códigos comprobados en CSV SIAP. No deducir códigos ZBS ni confundirlos con numeración provincial. Referencias: [validación](VALIDATION_REPORT.md), [fuentes](SOURCES.md).
