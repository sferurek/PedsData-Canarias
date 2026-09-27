# Validación de Zonas Básicas de Salud

**Corte:** 27/09/2026  
**Gate B:** **RED para cálculo ZBS actual**. El cálculo insular y el benchmark de routing siguen siendo posibles, pero no se publicarán perfiles ni agregados ZBS.

## Hallazgo principal

No se ha localizado una geometría oficial vigente, con código estable y fechas de validez, para las siete islas. La evidencia disponible se conserva en dos artefactos distintos:

- [`health_zones_current_catalog.csv`](../data/curated/health_zones_current_catalog.csv): 106 nombres presentes en el Catálogo AP 2026, sin código estable ni geometría; todos `NEEDS_VALIDATION` y `routing_eligible=false`.
- [`health_zones.geojson`](../data/curated/health_zones.geojson): 105 polígonos IACS/AtlasVPM de referencia 2017; todos `NEEDS_VALIDATION` y `routing_eligible=false`. La colección se denomina `historical_2017_not_for_routing`.

El fichero histórico se entrega para trazabilidad y comparación, no como sustituto de la cartografía vigente.

## E54086B e IDECanarias

La API oficial de E54086B devuelve `currentlyActive=false`, estado `PLANNING` y **cero instancias**. La ficha estadística no acredita un cubo descargable ni códigos ZBS observados.

El `GetCapabilities` del WMS oficial Mapa Sanitario ofrece cinco capas de puntos: Hospital, C.A.E., Centro de Salud, Consultorio Local y Punto de Urgencia. No publica polígonos ZBS. El catálogo SITCAN tampoco devolvió un dataset ZBS al buscar “salud” o “zona básica de salud”.

## Recuentos incompatibles

| Isla | Polígonos 2017 | Nombres AP 2026 | SIAP 2024 | Lectura |
|---|---:|---:|---:|---|
| El Hierro | 2 | 2 | 2 | Recuento compatible; vigencia geométrica sin certificar |
| La Gomera | 5 | 5 | 5 | Recuento compatible; nomenclatura no idéntica |
| La Palma | 9 | 9 | 9 | Recuento compatible; vigencia geométrica sin certificar |
| Tenerife | 39 | 38 | 40 | Definiciones/agrupaciones incompatibles |
| Gran Canaria | 38 | 39 | 39 | Escaleritas–Schamann unido en 2017 y separado actualmente |
| Fuerteventura | 5 | 6 | 6 | El SCS 2026 publica además cuatro territorios |
| Lanzarote | 7 | 7 | 7 | Mismo total, distinta partición Arrecife/La Graciosa–Teguise |

## Fuerteventura: 4, 5 y 6 no son cifras intercambiables

- El shapefile histórico 2017 contiene cinco polígonos.
- SIAP 2024 informa seis ZBS.
- El Catálogo AP 2026 usa seis nombres: La Oliva, Península de Jandía, Tuineje-Pájara, Puerto del Rosario, II Puerto del Rosario (Sur) y Antigua-Betancuria.
- La página SCS actualizada el 01/07/2026 declara cuatro ZBS territoriales. Dentro de “Puerto del Rosario” enumera tres equipos: Puerto del Rosario I-Sur, Puerto del Rosario II-Norte y Antigua-Betancuria.

La discrepancia queda explicada como diferencia entre **cuatro territorios publicados por el SCS** y **seis unidades funcionales/equipos contados por SIAP y el catálogo AP**. Aún falta un nomenclátor oficial versionado que establezca códigos y correspondencias. El proyecto conserva las tres versiones y no elige una cifra como geometría vigente.

## QA GIS del fallback 2017

El QA completo está en [`health_zones_qa.json`](../data/curated/health_zones_qa.json).

- 105/105 geometrías válidas en origen; `make_valid` no se aplicó.
- Cero códigos fuente duplicados y cero pares con solape superior a 1 m² dentro de cada isla.
- CRS de origen EPSG:4258, exportación explícita a EPSG:4326 y cálculo de áreas en EPSG:32628.
- Cobertura frente a municipios ISTAC generalizados: 98,405%–99,815%. Las diferencias costeras entre productos generalizados impiden interpretar el residuo como hueco ZBS demostrado.

La comparación con el catálogo actual invalida el uso operativo del shapefile aunque su topología interna sea consistente.

## Decisión

Gate B permanece **RED** porque no puede relacionarse población 2024 con una
ZBS vigente sin fabricar límites. El benchmark de routing ya se ejecutó, pero
su gate también quedó rojo; no se calcula aún accesibilidad insular. Se preparó
una solicitud institucional, sin enviarla, para geometría, códigos, vigencias,
E54086B y el crosswalk territorial/funcional.
