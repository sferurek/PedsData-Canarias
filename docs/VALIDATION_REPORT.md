# Informe de pruebas ejecutadas

Fecha de descarga 27/09/2026 UTC en [api_audit.json](evidence/api_audit.json). Hash SHA256, URL exacta, bytes y content-type en cada registro. Esta auditoría de fuente es parte de FASE 0, no ETL productivo.

## Descargas comprobadas

- Malla 2024: HTTP 200, GeoJSON completo, 13.277 de 13.277 features, siete códigos insulares. MultiPolygon, CRS declarado EPSG:4326 y extensiones insulares plausibles. Cero nulos en 0–14; 0–17 nulo en todas las celdas.
- SIAP profesionales: 1.008 filas, 2004–2024. Población asignada: 10.584 filas, 2004–2024. Recuentos centros/ZBS: 504 filas, 2004–2024. CSV real con comas, no asumir TSV por etiqueta del catálogo.
- Catálogo de población por sexo/edad: v1.5 localizada con formatos; observaciones no descargadas.

|Isla|Celdas|Suma malla 0–14, 2024|Nulos 0–14|Nulos 0–17|Pediatras AP SIAP 2024|ZBS SIAP 2024|
|---|---:|---:|---:|---:|---:|---:|
|El Hierro|192|1214|0|192|1|2|
|La Gomera|285|2009|0|285|1|5|
|La Palma|1315|8823|0|1315|13|9|
|Tenerife|5442|110182|0|5442|148|40|
|Gran Canaria|3850|95208|0|3850|110|39|
|Fuerteventura|987|16945|0|987|19|6|
|Lanzarote|1206|21433|0|1206|26|7|

La suma malla es un resultado de control, no una estimación clínica ni una cifra censal conciliada. Datos 2024 provisionales según catálogo. No calcular automáticamente ratios mezclando malla y ratio TIS publicado; denominadores distintos.

## Inconsistencias documentales

Visualizador SIAP titula 2004–2023 mientras CSV auditado llega a 2024: prima el periodo observado para la descarga, conservar ambos metadatos. Fuerteventura: seis ZBS SIAP 2024, cuatro ZBS descritas por SCS en web actualizada 01/07/2026. Puede reflejar definiciones/fechas diferentes; no se ha resuelto la causa.

## Qué no se ha validado

Topología GIS completa, solapes, unicidad espacial de toda la malla, conciliación con censo, geometría ZBS actual, carteras/IDs/coordenadas vigentes exhaustivos, motor/red/rutas, series de aire/meteo, celdas de renta, todos los cubos perinatales/mortalidad/ESC y memorias de todos los hospitales. No hay métricas de accesibilidad calculadas.

La validación de geometrías realizada es estructural (tipo/CRS/extensión), no certificación topológica. La fecha de consulta de una página no es fecha de actualización de la cartera.

## Reproducción

Los tres CSV guardados son copias de fuentes oficiales con URLs y hashes en el manifiesto. El resumen de malla conserva URL, hash, recuentos y sumas; no se guarda el GeoJSON de 21,7 MB en Git. `scripts/verify_phase0.py` comprueba los documentos, siete columnas, hashes CSV y cobertura pediatras 2024 sin red. `scripts/recheck_grid.py` vuelve a consultar la URL oficial y calcula cobertura/nulos/sumas sin persistir el fichero ni desarrollar la aplicación. Una descarga futura puede cambiar el hash por timestamps/IDs generados; comparar además contenido estadístico y versión.

[Licencias y atribución](DATA_LICENSES.md), [fuentes](SOURCES.md).
