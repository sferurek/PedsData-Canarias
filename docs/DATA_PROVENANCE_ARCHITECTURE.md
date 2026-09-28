# Arquitectura de trazabilidad de datos

## Principio rector

**Every number must be traceable.** No source ID, no render. No indicador derivado sin fórmula. No mapa sin geografía, periodo y método.

## Flujo

`fuente primaria → source registry → dataset/version/checksum → métrica → linaje → resultado → visualización → /trazabilidad/[metric_id]`

`data/semantic/sources_catalog.json` registra las fuentes con identificadores estables. `data/semantic/metrics_catalog.json` declara definición, escala, periodo, unidad, método, fuentes y fórmula. La aplicación solo renderiza un `Metric` si el indicador existe y tiene `source_ids` resolubles.

Cada resultado enlaza a **Fuentes de este resultado**. La vista de trazabilidad incluye el valor o contexto mostrado, fuentes primarias, contribución de cada input, URL oficial, organismo, dataset, variable, periodo, geografía, versión, checksum, adquisición, fórmula, transformaciones, redondeo y limitaciones.

## Derivaciones

Las fórmulas conservan inputs con `source_id`. El cálculo se ejecuta en ETL o en el motor determinista; Ask PedsData no genera cifras. Accesibilidad registra malla ISTAC, catálogo U20, snapshot OSM, OSRM 5.27.1 y checksum de grafo.

## Controles

`etl/build_phase8_provenance.py` falla si una fuente referenciada no existe, una métrica derivada carece de fórmula o una capa no declara geografía, periodo y clasificación. `tests/test_phase8_provenance.py` verifica esos contratos y las rutas públicas.
