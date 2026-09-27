# Auditoría final de E54086B y ZBS vigente

**Fecha:** 27/09/2026  
**Conclusión:** no se encontró una instancia pública ni una capa oficial vigente que reúna código, nombre, geometría, vigencia, isla, área y licencia. Gate B permanece **RED**.

## E54086B

La [API oficial de la operación](https://datos.canarias.es/api/estadisticas/operations/v1.0/operations/E54086B) fue actualizada el 28/05/2026, pero declara `currentlyActive=false` y `status=PLANNING`. Su endpoint oficial de instancias devuelve `total=0`. La ficha web de actividades confirma planificación y ausencia de instancias metodológicas; la antigua página temática devuelve 404. No se encontró cubo, diccionario territorial ni sucesor API público.

Los snapshots consultados quedan identificados en [`zbs_phase2_audit.json`](../data/curated/zbs_phase2_audit.json), incluidos SHA-256 de operación e instancias. Esto distingue una operación catalogada de un dataset publicado: la existencia de E54086B no aporta observaciones ni identificadores reutilizables.

## Servicios geográficos oficiales

El [WMS Mapa Sanitario de IDECanarias](https://idecan2.grafcan.es/ServicioWMS/MapaSanitario?SERVICE=WMS&REQUEST=GetCapabilities) expone cinco capas de puntos —urgencias, consultorios, centros de salud, CAE y hospitales— y declara `RemoteWFS=0`. La petición WFS al mismo servicio responde `WFS request not enabled`; la ruta alternativa `/ServicioWFS/MapaSanitario` devuelve 404. No hay una capa poligonal ZBS en esas capacidades.

La búsqueda exacta del catálogo abierto devuelve E54086A con recuentos insulares, no E54086B ni geometría. Las páginas territoriales SCS aportan nombres y centros actuales, pero no el contrato completo necesario para una capa versionada.

## Decisión

Las 105 geometrías de 2017 conservan `historical_reference_only=true` y `routing_eligible=false`. Sirven para crosswalk y estudio histórico, no para perfiles actuales, agregación 2024 ni routing. Fuerteventura mantiene separados los cuatro ámbitos territoriales SCS 2026, seis unidades funcionales SIAP 2024 y cinco polígonos históricos; no se elige una cifra arbitraria.

No hay evidencia nueva que permita bajar Gate B a YELLOW o GREEN. Se adopta el modelo territorial sin ZBS descrito en `ZBS_FALLBACK_DECISION.md` y se preparan solicitudes institucionales sin enviarlas.
