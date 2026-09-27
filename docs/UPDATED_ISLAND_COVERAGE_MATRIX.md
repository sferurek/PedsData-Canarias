# Matriz de cobertura insular actualizada — Fase 1

Corte 27/09/2026. `COMPLETE` se limita al contrato descrito. La matriz conserva
las siete islas aunque un gate esté rojo.

|Variable|El Hierro|La Gomera|La Palma|Tenerife|Gran Canaria|Fuerteventura|Lanzarote|
|---|---|---|---|---|---|---|---|
|Población 0–14, malla 2024|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|
|Pediatras AP, SIAP 2024|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|
|ZBS vigente con código y geometría|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|
|Centros AP U20 con coordenada oficial|COMPLETE|COMPLETE|COMPLETE|PARTIAL|COMPLETE|COMPLETE|PARTIAL|
|Tiempo real a Pediatría AP|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|
|Urgencias Pediátricas diferenciadas|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|PARTIAL|PARTIAL|NEEDS VALIDATION|NEEDS VALIDATION|
|Hospitalización pediátrica insular comparable|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|UCIP|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|PARTIAL|PARTIAL|NEEDS VALIDATION|NEEDS VALIDATION|
|UCIN|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|PARTIAL|PARTIAL|NEEDS VALIDATION|NEEDS VALIDATION|
|Mortalidad pediátrica|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Perinatalidad|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Salud mental infantil|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Calidad del aire|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Meteorología|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|
|Renta/vulnerabilidad|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|

## Cambios comprobados en Fase 1

|Isla|Recursos|VERIFIED|ZBS 2017|AP 2026|SIAP 2024|Rutas OSRM / Valhalla|
|---|---:|---:|---:|---:|---:|---:|
|El Hierro|3|3|2|2|2|4 / 4|
|La Gomera|2|2|5|5|5|4 / 4|
|La Palma|5|5|9|9|9|4 / 4|
|Tenerife|89|87|39|38|40|4 / 4|
|Gran Canaria|47|47|38|39|39|4 / 4|
|Fuerteventura|8|8|5|6|6|4 / 4|
|Lanzarote|14|14|7|7|7|4 / 4|

Los recuentos ZBS no son equivalentes. Fuerteventura conserva 4 zonas
territoriales SCS 2026, 6 unidades funcionales AP/SIAP y 5 polígonos
históricos; no se eligió una cifra única.

Tenerife mantiene dos recursos no plenamente verificados. Lanzarote es PARTIAL
porque hay niños en La Graciosa y no existe destino U20 verificado en ese
componente. El éxito de rutas no valida los tiempos.
