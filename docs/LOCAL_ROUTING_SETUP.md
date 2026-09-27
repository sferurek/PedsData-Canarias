# Routing local reproducible

## Activos congelados

La red procede del extracto diario de OpenStreetMap para Canarias publicado por Geofabrik. La versión usada es `canary-islands-260926`, con datos OSM hasta `2026-09-26T20:22:51Z` y SHA-256 `2c5f0f3c7b42fc68f6d1bf64679642edb86f546fe510e6f081a07a4d398379f9`. Su licencia es ODbL 1.0. El binario no se versiona en Git; [el manifiesto](../data/manifests/osm_canarias_snapshot.json) registra URL, fecha, licencia, tamaño, checksums y caja envolvente.

El motor es OSRM 5.27.1, algoritmo MLD y perfil oficial `car.lua`. La imagen está fijada por versión y digest `ghcr.io/project-osrm/osrm-backend:v5.27.1@sha256:b1ca5d72da456e82f81b8732a095c2357b00710099efa844040d1eb40b4b5386`.

El [manifiesto del grafo](../data/manifests/osrm_canarias_graph.json) enlaza el grafo con el checksum OSM, la configuración y la fecha de construcción. El paquete contiene 26 archivos, ocupa 116.750.248 bytes y tiene checksum de conjunto `f0b0700b3224c76f6b62682102cbf2002936164d1de7bb28d8820af81578a37e`.

## Construcción y ejecución

Requisitos: Docker, `curl` y el entorno Python `.venv` del proyecto.

```bash
scripts/build_local_osrm.sh
scripts/run_local_osrm.sh
.venv/bin/python etl/run_local_routing_benchmark.py --base-url http://127.0.0.1:55000
.venv/bin/python etl/build_routing_reference_validation.py
```

El puerto por defecto es `55000`; puede cambiarse con `OSRM_PORT`. La reconstrucción descarga el PBF nombrado por fecha, verifica el MD5 publicado, ejecuta `osrm-extract`, `osrm-partition` y `osrm-customize`, y regenera ambos manifiestos. El SHA-256 fijado en el manifiesto es la comprobación de identidad usada por QA.

## Barrera topológica

Antes de consultar OSRM, cada origen y destino debe pertenecer al mismo componente terrestre. La Graciosa es un componente independiente. Los cruces marítimos no se envían al motor y conservan `requires_interisland_transfer` con tiempo y distancia nulos. Esta barrera también evita que enlaces ferry presentes en OSM se interpreten como acceso pediátrico por carretera.

Fuentes primarias: [extracto Canarias de Geofabrik](https://download.geofabrik.de/africa/canary-islands.html), [licencia ODbL](https://opendatacommons.org/licenses/odbl/1-0/) y [OSRM backend oficial](https://github.com/Project-OSRM/osrm-backend).
