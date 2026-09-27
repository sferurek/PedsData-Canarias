# Informe QA de accesibilidad pediátrica 2024

**Fecha:** 27/09/2026  
**Resultado:** APROBADO tras una corrección explícita de cero no publicable.

## Reproducción

Se volvió a ejecutar `etl/prepare_accessibility.py` con OSRM 5.27.1, el grafo `f0b0700…15a37e`, el extracto `canary-islands-260926`, la malla ISTAC 0–14 de 2024 y los 158 destinos elegibles de Fase 2. Se realizaron 706 matrices locales, sin peticiones públicas y sin fallos del motor.

La primera pasada de QA detectó una celda de Agaete (`250mN098750E179225`, 4 niños) marcada `routed` con 0 segundos y 0 metros porque origen y centro coincidían en el mismo nodo OSRM. Se rechazó el cero: el pipeline la reclasifica como `not_evaluated` y mantiene tiempo, distancia y destino nulos. No se inventó un mínimo ni se escogió un centro más lejano.

## Controles finales

| Control | Resultado |
|---|---:|
| Celdas totales / únicas | 13.277 / 13.277 |
| Población 0–14 raw / staging | 255.814 / 255.814 |
| `routed` | 13.256 |
| `requires_interisland_transfer` | 20 |
| `no_route` | 0 |
| `not_evaluated` | 1 |
| Destinos elegibles | 158 |
| Islas presentes | 7 |
| Fallos QA | 0 |

Todas las rutas publicables tienen segundos y metros positivos, destino `VERIFIED`, coordenada oficial y el mismo componente terrestre. Los estados no routeables tienen segundos, minutos, distancia y destino nulos. Cada fila conserva OSRM 5.27.1, checksum del grafo, snapshot OSM y periodo.

## La Graciosa

Las 20 celdas de La Graciosa, con 91 niños, permanecen bajo Lanzarote con `requires_interisland_transfer`. No se enviaron al motor contra destinos de Lanzarote y no reciben ferry, avión, ambulancia ni tiempo clínico estimado.

## Promoción

El QA estructurado está en `data/manifests/accessibility_qa.json`. Solo después de obtener `passed=true` se generaron los tres exports `data/curated/`. Gate B sigue RED y no existe ningún agregado ZBS.
