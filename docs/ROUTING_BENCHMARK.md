# Benchmark de routing pediátrico

**Ejecución:** 27/09/2026. **Gate:** RED. El benchmark cubre las siete islas,
pero la discrepancia temporal entre motores y la falta de un grafo congelado
impiden usar los minutos como resultado asistencial reproducible.

## Motores y fuentes

- **OSRM**, perfil `driving`, servidor público de FOSSGIS.
- **Valhalla**, coste `auto`, servidor público FOSSGIS, `use_ferry=0`.
- **OpenRouteService** quedó `not_evaluated`: la API pública exige clave.

Referencias: [OSRM/FOSSGIS](https://routing.openstreetmap.de/about.html),
[Valhalla](https://github.com/valhalla/valhalla/blob/master/docs/docs/api/openapi.yaml),
[ORS](https://openrouteservice.org/dev/).

Los endpoints públicos sirven para este benchmark acotado. No se usarán para
calcular las 13.277 celdas ni como infraestructura del producto.

## Casos

`etl/build_routing_test_cases.py` crea cinco casos por isla desde la malla
ISTAC 0–14 de 2024 y destinos AP `VERIFIED`:

1. urbano: celda con más niños en un componente con destino;
2. rural: celda con 1–2 niños más alejada en línea recta del destino;
3. extremo: celda poblada más alejada del destino;
4. inverso: el caso extremo en sentido contrario;
5. no-ruta: cruce marítimo que el preflight bloquea.

Los destinos de los cuatro primeros casos pertenecen al mismo componente
terrestre. La selección es una prueba de cobertura y no una muestra
representativa de tiempos de toda la población.

La malla contiene población infantil en La Graciosa, pero el catálogo U20
verificado no contiene un destino pediátrico en ese componente. El caso se
marca `requires_interisland_transfer`; no se envía al motor y minutos y
distancia quedan nulos. En las otras seis islas el no-ruta cruza a otra isla y
se bloquea de igual forma.

## Resultado observado

Ambos motores devolvieron 28/28 rutas terrestres: cuatro en cada isla. Los 14
resultados no-ruta (siete por motor) fueron bloqueados antes de la petición.

|Isla|Rutas por motor|Mediana diferencia tiempo|Máxima diferencia tiempo|Mediana diferencia distancia|Máximo snapping OSRM|
|---|---:|---:|---:|---:|---:|
|El Hierro|4/4|40,0%|66,3%|25,3%|17,9 m|
|La Gomera|4/4|46,1%|50,9%|0,2%|55,5 m|
|La Palma|4/4|39,7%|60,7%|4,3%|78,6 m|
|Tenerife|4/4|54,2%|54,9%|14,6%|57,3 m|
|Gran Canaria|4/4|28,1%|36,9%|2,9%|27,8 m|
|Fuerteventura|4/4|30,6%|96,6%|0,2%|65,0 m|
|Lanzarote|4/4|44,3%|82,8%|0,2%|169,2 m|

Globalmente, la mediana de diferencia temporal absoluta es 43,4% y el máximo
96,6%; en distancia son 0,3% y 27,2%. La latencia mediana fue 245,5 ms en OSRM
y 313,0 ms en Valhalla. La cobertura de red es suficiente, pero los tiempos no
son intercambiables y falta validación contra trayectos de referencia.

## Decisión

No se selecciona aún motor para producción. Para poner el gate en verde se
requiere un extracto OSM con fecha y checksum, ejecución local fijada de OSRM o
Valhalla, umbrales de snapping y una muestra de tiempos contrastada. Después se
repetirán estos 35 casos. Hasta entonces no se genera accesibilidad ni mapa.

Archivos reproducibles:

- `data/curated/routing_test_cases.csv`: 35 entradas;
- `data/curated/routing_benchmark_results.csv`: 105 filas, incluidos los
  estados no evaluados de ORS;
- `data/curated/routing_benchmark_manifest.json`: hashes de inputs y output;
- `etl/run_routing_benchmark.py`: peticiones, preflight y captura de métricas.
