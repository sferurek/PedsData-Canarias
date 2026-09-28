# Catálogo semántico de métricas

El catálogo contiene 20 métricas trazables y define qué preguntas, gráficos y mapas son válidos. `metric_compatibility.json` permite relaciones como pediatras × consultas y rechaza cruces directos incompatibles como estación PM10 × hospitalización regional.

El pipeline reproducible es:

1. `etl/build_phase8_semantic.py`
2. `etl/build_phase8_provenance.py`
3. `etl/enrich_phase8_map.py`

Los artefactos web son copias de build; los archivos canónicos permanecen en `data/semantic/` y `data/curated/`.
