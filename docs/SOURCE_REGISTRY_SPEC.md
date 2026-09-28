# Source registry specification

Archivo canónico: `data/semantic/sources_catalog.json`. Copia de build: `apps/web/src/data/sources-catalog.json`.

Cada fuente contiene `source_id`, nombre, organismo, dominio, descripción, contenido, universo/edad, desagregación geográfica, periodo disponible, frecuencia, formato, licencia, versión usada, estado de integración, última adquisición, URL oficial directa, usos y checksum cuando existe.

Los IDs son estables y con espacio de nombres, por ejemplo `ISTAC:E54086A_000005`, `INE:ADRH`, `OSM:CANARY_2026_09_26`. Una nueva URL o versión no cambia el ID lógico; se registra en versión y manifiesto. Las fuentes `hold` o `research only` pueden catalogarse, pero no alimentan valores visibles hasta superar admisión.

`/fuentes` ofrece búsqueda y filtros por dominio. `/fuentes/[source_id]` muestra provenance completa y las métricas que la utilizan.
