# Validación con trayectos de referencia

## Diseño

El archivo [`routing_reference_journeys.csv`](../data/curated/routing_reference_journeys.csv) contiene 21 trayectos: urbano, rural y extremo para cada una de las siete islas. Conserva origen, destino, distancia y tiempo de referencia, fuente, fecha, resultado local, diferencias, snapping y notas.

La referencia numérica es la mediana de las respuestas de OSRM público y Valhalla público registradas en Fase 1 para los mismos casos. Sirve como contraste entre implementaciones OSM; no se presenta como verdad de terreno. La comprobación topológica y cartográfica verifica que origen y destino pertenecen a la misma isla y componente terrestre.

## Resultados

| Control | Resultado |
|---|---:|
| Trayectos | 21 |
| Islas | 7 |
| GREEN temporal (<=20 %) | 10 |
| YELLOW temporal (>20 % y <=35 %) | 11 |
| RED temporal (>35 %) | 0 |
| Diferencia temporal mediana | 20,1 % |
| Diferencia temporal máxima | 32,6 % |
| Diferencia de distancia mediana | 0,1 % |
| Diferencia de distancia máxima | 14,5 % |
| GREEN de snapping | 14 |
| YELLOW de snapping | 7 |
| RED de snapping | 0 |

El mayor snapping observado fue 149,3 m para un punto representativo de celda y 169,2 m para la coordenada oficial del C.L. Playa Blanca. Ambos quedan en YELLOW; se mantienen las coordenadas originales y la advertencia.

## Interpretación

El motor no presenta fallos RED en la muestra y reproduce de forma razonable el contraste disponible. La dispersión temporal es compatible con diferencias de versión de red, perfil, velocidades y penalizaciones entre motores. La distancia, mucho más estable, respalda que las rutas siguen corredores equivalentes.

Esta validación permite cerrar Gate C para cálculo reproducible. No convierte los tiempos en estimaciones clínicas de traslado ni modela ferry, avión, ambulancia, tráfico en tiempo real o acceso intrahospitalario. Las futuras comprobaciones con routing institucional o conocimiento local documentado se añadirán como nuevas referencias sin reescribir estos resultados.
