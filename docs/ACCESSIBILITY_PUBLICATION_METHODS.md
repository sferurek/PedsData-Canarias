# Métodos de publicación de accesibilidad

## Universo y rutas

El universo son 13.277 celdas ISTAC de 250 m con población original 0–14 a 01/01/2024. Cada polígono usa `representative_point`, no una distribución uniforme. Los destinos son 158 centros con Pediatría AP observada, estado `VERIFIED` y coordenada oficial. OSRM 5.27.1 calcula acceso geográfico potencial por carretera sobre el grafo congelado; no mide tiempo hasta recibir atención.

## Denominadores

Cada ámbito conserva `population_total`, `population_evaluable`, `population_routed`, `population_requires_interisland_transfer`, `population_no_route` y `population_not_evaluated`. `population_evaluable` suma rutas resueltas y `no_route` efectivamente consultado; excluye transferencias y fallos/no evaluados. Las bandas publican porcentaje sobre población total y sobre población evaluable.

## Bandas y cuantiles

Las bandas son `<5`, `5–<10`, `10–<15`, `15–<20`, `20–<30` y `>=30` minutos, más los estados sin tiempo. No se usa gradiente continuo.

Mediana y P90 se calculan solo en filas `routed`, ponderando por `children_0_14`. Tras ordenar por minutos, el cuantil `q` es el primer valor cuyo peso acumulado es mayor o igual a `q × suma de pesos`. Las celdas con cero niños no alteran el cuantil. Los tests cubren pesos desiguales y ausencia total de peso.

## Agregación territorial

Se generan siete filas insulares y 88 municipales. Las geometrías municipales oficiales fueron válidas; la regla de privacidad deja 85 perfiles publicables. Los centros municipales se asignan por punto-en-polígono porque REGCESS/eGeo no aporta código municipal en muchos registros AP. El conteo de centros es infraestructura y no se confunde con el número de pediatras SIAP.

No se crean perfiles, filtros ni ratios ZBS. La geometría 2017 continúa como referencia histórica no routeable.

## Provenance

`accessibility_publication_manifest.json` enlaza malla ISTAC, catálogo pediátrico, snapshot OSM, OSRM, perfil, grafo, checksums de código y de cada export, fecha de cálculo, grupo etario y reglas de privacidad.
